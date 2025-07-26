from concurrent.futures import ThreadPoolExecutor
from utils import save_json, load_json, retry
from lxml import etree
import requests
import time
import re
import os


def get(url):
    resp = requests.get(url, timeout=10)
    assert resp.status_code != 404, f"{url} Not Found"
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url}, status {resp.status_code}")
    return resp


@retry(max_retries=3)
def run_get_indexing_page(typ, index):
    url = f"https://dblp.org/db/{typ}/{index}/index.html"
    print(f"Fetching indexing links for {url} ...\n", end="")
    resp = get(url)
    tree = etree.HTML(resp.text)
    hrefs = []
    if typ == "conf":
        # 会议，直接爬a标签，用text == "[contents]"来验证
        anchors = tree.xpath("//a[@class='toc-link']")
        for anchor in anchors:
            text = anchor.xpath("./text()")[0]
            assert text == "[contents]", f'{text} != "[contents]", check {url}'
            href = anchor.xpath("./@href")[0]
            hrefs.append(href)
    elif typ == "journals":
        # 期刊，爬所有a标签的href，用前缀筛选，是否包含index验证
        hrefs = tree.xpath("//a/@href")
        prefix = f"https://dblp.org/db/journals/"
        hrefs = list(filter(
            lambda href:
            href.startswith(prefix)
            and href.endswith(".html")
            and not href.endswith("index.html"),
            hrefs
        ))
    header = tree.xpath("//header[@id='headline']/h1")[0].xpath("string(.)")
    return {
        "header": header,
        "links": hrefs
    }


@retry(max_retries=3)
def run_get_paper_list(url, throttle_delay=15):
    print(f"Fetching paper list for {url} ...\n", end="")
    resp = get(url)
    tree = etree.HTML(resp.text)
    publ_list_li = tree.xpath("//ul[@class='publ-list']/li")
    assert len(publ_list_li) > 0, f"No publ-list found, check {url}"
    papers = []
    for li in publ_list_li:
        # 不考虑以下项：
        # 1.li中的<div class="box">，不是"Journal Articles"或"Conference and Workshop Papers"
        # 2.作者为空
        box_title = li.xpath("./div[@class='box']/img/@title")[0]
        if box_title not in ["Journal Articles", "Conference and Workshop Papers"]:
            continue
        authors = li.xpath("./cite/span[@itemprop='author']//span[@itemprop='name']/text()")
        if len(authors) == 0:
            continue
        title_span = li.xpath("./cite/span[@class='title']")
        assert len(title_span) == 1, f"Found len(title_span) != 1, check {url}"
        title = title_span[0].xpath("string(.)")
        papers.append({
            "title": title,
            "authors": authors,
        })
    header = tree.xpath("//header[@id='headline']/h1")[0].xpath("string(.)")
    # 确定年份：正则提取1900-2099的数字组合
    # 1.从url中提取
    pattern = r"(?<!\d)(19\d{2}|20\d{2})(?!\d)"
    matches = re.findall(pattern, url)
    # 2.如果url中没有，从一级标题中提取
    if len(matches) == 0:
        matches = re.findall(pattern, header)
    # 3.如果一级标题中没有，从二级标题中提取
    if len(matches) == 0:
        h2_texts = tree.xpath("//div[@id='main']/header/h2/text()")
        matches = re.findall(pattern, ";".join(h2_texts))
    matches = list(set(matches))
    # 4.如果以上都没有匹配，从页面中提取出现次数最多的年份
    if len(matches) == 0:
        matches = re.findall(pattern, resp.text)
        assert len(matches) > 0, f"No matching year found in {url}"
        year = max(set(matches), key=matches.count)
    else:
        year = ",".join(sorted(matches))

    time.sleep(throttle_delay)

    return {
        "header": header,
        "year": year,
        "papers": papers
    }


def update_indexing_pages(typ, index, indexing_page, output_dir=None):
    links_new = indexing_page["links"]

    if output_dir is None:
        return links_new

    key = f"{typ}/{index}"
    path_indexing_pages = os.path.join(output_dir, "indexing_pages.json")
    path_full_name_mapping = os.path.join(output_dir, "full_name_mapping.json")

    indexing_pages = load_json(path_indexing_pages)
    links_old = indexing_pages[key]["links"] if key in indexing_pages else []
    links_diff = list(set(links_new) - set(links_old))

    if len(links_diff) != 0:
        print(f"[*] New indexing link found for {key}:")
        for link in links_diff:
            print(" " * 4, link)

    def update_indexing_pages_callback():
        if len(links_diff) == 0:
            return

        indexing_pages[key] = indexing_page
        save_json(indexing_pages, path_indexing_pages)
        print(f"[+] Updated {path_indexing_pages} with {len(links_diff)} new links for {key}.")

        full_name_mapping = load_json(path_full_name_mapping)
        if key not in full_name_mapping or full_name_mapping[key] != indexing_page["header"]:
            full_name_mapping[key] = indexing_page["header"]
            save_json(full_name_mapping, path_full_name_mapping)
            print(f"[+] Updated {path_full_name_mapping} for {key}.")

    return links_diff, update_indexing_pages_callback


def update_paper_list(typ, index, paper_list, output_dir=None):
    if output_dir is None or len(paper_list) == 0:
        return

    path_paper_list = os.path.join(output_dir, "paper_lists", typ, f"{index}.json")
    paper_list_old = load_json(path_paper_list)
    paper_list = {**paper_list, **paper_list_old}

    save_json(paper_list, path_paper_list, sort_fn=lambda item: (item[1]["year"], item[0]), reverse=True)
    print(f"[+] Updated {path_paper_list}.")


def validate_and_fix_corrupted(output_dir):
    path_indexing_pages = os.path.join(output_dir, "indexing_pages.json")
    path_full_name_mapping = os.path.join(output_dir, "full_name_mapping.json")
    indexing_pages = load_json(path_indexing_pages)
    full_name_mapping = load_json(path_full_name_mapping)
    if set(indexing_pages.keys()) != set(full_name_mapping.keys()):
        print(f"[!] Keys in {path_indexing_pages} and {path_full_name_mapping} do not match.")
    has_corrupted = False
    for key in indexing_pages.keys():
        typ, index = key.split("/")
        path_paper_list = os.path.join(output_dir, "paper_lists", typ, f"{index}.json")
        paper_list = load_json(path_paper_list)
        links = indexing_pages[key]["links"]
        s1, s2 = set(links), set(paper_list.keys())
        if len(s1 - s2) > 0:
            has_corrupted = True
            print(f"[!] The following links in {path_indexing_pages} are missing in {path_paper_list}:")
            for link in s1 - s2:
                print(" " * 4, link)
                indexing_pages[key]["links"].remove(link)
            print(" " * 4, f"These links will be removed from {path_indexing_pages}.")
    if not has_corrupted:
        print("[*] No corrupted data found.")
    else:
        save_json(indexing_pages, path_indexing_pages)
        print(f"[+] The changes have been saved to {path_indexing_pages}.")


def get_paper_lists(indices, output_dir=None):
    validate_and_fix_corrupted(output_dir)
    for typ in indices:
        for index in indices[typ]:
            indexing_page = run_get_indexing_page(typ, index)
            if indexing_page is None:
                continue
            # 此处不直接更新而是返回一个callback函数，确保paper_list更新成功后才更新indexing_pages
            links_diff, update_indexing_pages_callback = \
                update_indexing_pages(typ, index, indexing_page, output_dir)
            with ThreadPoolExecutor(max_workers=10) as executor:
                result = executor.map(run_get_paper_list, links_diff)
            paper_list = {link: paper for link, paper in zip(links_diff, result) if paper is not None}
            update_paper_list(typ, index, paper_list, output_dir)
            update_indexing_pages_callback()
