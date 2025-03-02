import requests
import threading
from lxml import etree
from time import sleep
import urllib3
import json
import re

urllib3.disable_warnings()

indices = {
    # 期刊
    "journals": [
        # 网络与信息安全，CCF A类
        "tdsc", "tifs", "joc",

        # 网络与信息安全，CCF B类
        "tissec", "compsec", "dcc", "jcs",

        # 网络与信息安全，CCF C类
        "clsr", "ejisec", "iet-ifs", "imcs", "ijics", "ijisp", "istr", "scn", "cybersec",

        # 计算机网络，CCF A类
        "jsac", "tmc", "ton",

        # 计算机网络，CCF B类
        "toit", "tomccap", "tosn", "cn", "tcom", "twc",

        # 计算机网络，CCF C类
        "adhoc", "comcom", "tnsm", "iet-com", "jnca", "monet", "networks", "ppna", "wicomm", "winet", "iotj",

        # 软件工程/系统软件/程序设计语言，CCF A类
        "toplas", "tosem", "tse", "tsc",

        # 软件工程/系统软件/程序设计语言，CCF B类
        "ase", "ese", "iet-sen", "infsof", "jfp", "smr", "jss", "re", "scp", "sosym", "stvr", "spe",

        # 软件工程/系统软件/程序设计语言，CCF C类
        "cl", "ijseke", "sttt", "jlap", "jwe", "soca", "sqj", "tplp", "pacmpl",
    ],
    # 学术会议
    "conf": [
        # 网络与信息安全，CCF A类
        "ccs", "ndss", "uss", "sp", "eurocrypt", "crypto",

        # 网络与信息安全，CCF B类
        "acsac", "asiacrypt", "esorics", "fse", "csfw", "srds", "ches", "dsn", "raid", "pkc", "tcc",

        # 网络与信息安全，CCF C类
        "wisec", "sacmat", "drm", "ih", "acns", "asiaccs", "acisp", "ctrsa", "dimva", "dfrws", "fc", "trustcom", "sec",
        "ifip11-9", "isw", "icdf2c", "icics", "securecomm", "nspw", "pam", "pet", "sacrypt", "soups", "eurosp", "cisc",

        # 计算机网络，CCF A类
        "sigcomm", "mobicom", "infocom", "nsdi",

        # 计算机网络，CCF B类
        "sensys", "conext", "secon", "ipsn", "mobisys", "icnp", "mobihoc", "nossdav", "iwqos", "imc",

        # 计算机网络，CCF C类
        "ancs", "apnoms", "forte", "lcn", "globecom", "icc", "icccn", "mass", "p2p", "ipccc", "wowmom", "iscc", "wcnc",
        "networking", "im", "msn", "mswim", "wasa", "hotnets", "apnet",

        # 软件工程/系统软件/程序设计语言，CCF A类
        "pldi", "popl", "sigsoft", "sosp", "oopsla", "kbse", "icse", "issta", "osdi", "fm",

        # 软件工程/系统软件/程序设计语言，CCF B类
        "ecoop", "etaps", "iwpc", "re", "caise", "icfp", "lctrts", "models", "cp", "icsoc", "wcre", "icsm", "vmcai",
        "icws", "middleware", "sas", "esem", "issre", "hotos",

        # 软件工程/系统软件/程序设计语言，CCF C类
        "pepm", "paste", "aplas", "apsec", "ease", "iceccs", "icst", "ispass", "scam", "compsac", "icfem", "IEEEscc",
        "ispw", "seke", "qrs", "icsr", "icwe", "spin", "atva", "lopstr", "tase", "msr", "refsq", "wicsa",
        "internetware", "rv",
    ],
}


def multithread_run(func, args_list, max_threads=10):
    assert isinstance(args_list, list) and all(isinstance(arg, tuple) for arg in args_list), \
        "args_list must be a list of tuples"

    semaphore = threading.Semaphore(max_threads)

    def target(*args):
        with semaphore:
            func(*args)

    threads = []
    for arg in args_list:
        thread = threading.Thread(target=target, args=arg)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("All threads are finished.")


def ping():
    print("=" * 20, "ping", "=" * 20)
    retry_list = []

    def run_ping(typ, index):
        try:
            url = f"https://dblp.org/db/{typ}/{index}/index.html"
            print(f"run_ping {url} ...\n", end="")
            resp = requests.get(url, timeout=10)
            assert resp.status_code == 200, f"{url} does not exist."
        except AssertionError as ae:
            print(f"[!] {ae}\n", end="")
        except Exception:
            retry_list.append((typ, index))

    for typ in indices:
        for index in indices[typ]:
            retry_list.append((typ, index))

    while retry_list:
        params = retry_list
        retry_list = []
        multithread_run(run_ping, params, 10)


def get_detail_url():
    print("=" * 20, "get_detail_url", "=" * 20)
    retry_list = []
    dblp_detail_url = {}
    lock = threading.Lock()

    def run_get_detail_url(typ, index):
        try:
            url = f"https://dblp.org/db/{typ}/{index}/index.html"
            print(f"run_get_detail_url {url} ...\n", end="")
            resp = requests.get(url, timeout=10)
            tree = etree.HTML(resp.text)
            hrefs = []
            if typ == "conf":
                # 会议，直接爬a标签，用text == "[contents]"来验证
                anchors = tree.xpath("//a[@class='toc-link']")
                for anchor in anchors:
                    text = anchor.xpath("./text()")[0]
                    assert text == "[contents]", f"{text} != [contents], check {url}"
                    href = anchor.xpath("./@href")[0]
                    hrefs.append(href)
            elif typ == "journals":
                # 期刊，爬所有a标签的href，用前缀筛选，是否包含index验证
                hrefs = tree.xpath("//a/@href")
                prefix = f"https://dblp.org/db/journals/"
                hrefs = list(filter(lambda href: href.startswith(prefix) and not href == prefix, hrefs))
                for href in hrefs:
                    # assert index in href, f"{index} not in {href}, check {url}"
                    pass
            header = tree.xpath("//header[@id='headline']/h1")[0].xpath("string(.)")
            with lock:
                dblp_detail_url[f"{typ}/{index}"] = {
                    "header": header,
                    "links": hrefs
                }
        except AssertionError as ae:
            print(f"[!] {ae}\n", end="")
        except Exception as e:
            print(f"[x] {e}\n", end="")
            retry_list.append((typ, index))

    for typ in indices:
        for index in indices[typ]:
            retry_list.append((typ, index))

    while retry_list:
        params = retry_list
        retry_list = []
        multithread_run(run_get_detail_url, params, 10)

    with open("./output/dblp_detail_url.json", "w", encoding="utf-8") as f:
        json.dump(dblp_detail_url, f, indent=2, ensure_ascii=False)

    # <typ-index>到期刊/会议全称的映射
    full_name_mapping = {k: v["header"] for k, v in dblp_detail_url.items()}
    with open("./output/full_name_mapping.json", "w", encoding="utf-8") as f:
        json.dump(full_name_mapping, f, indent=2, ensure_ascii=False)


def get_paper_list(key, links):
    print("=" * 20, f"get_paper_list - {key}", "=" * 20)
    retry_list = []
    paperlist = {}
    lock = threading.Lock()

    def run_get_paper_list(url):
        try:
            # 不考虑以下项：
            # 1.li中的<div class="box">，不是"Journal Articles"或"Conference and Workshop Papers"
            # 2.作者为空
            print(f"run_get_paper_list {url} ...\n", end="")
            resp = requests.get(url, timeout=10)
            tree = etree.HTML(resp.text)
            publ_list_li = tree.xpath("//ul[@class='publ-list']/li")
            assert len(publ_list_li) > 0, f"no publ-list found, check {url}"
            papers = []
            for li in publ_list_li:
                box_title = li.xpath("./div[@class='box']/img/@title")[0]
                if box_title not in ["Journal Articles", "Conference and Workshop Papers"]:
                    continue
                authors = li.xpath("./cite/span[@itemprop='author']//span[@itemprop='name']/text()")
                if len(authors) == 0:
                    continue
                title_span = li.xpath("./cite/span[@class='title']")
                assert len(title_span) == 1, f"len(title_span) != 1, check {url}"
                title = title_span[0].xpath("string(.)")
                papers.append({
                    "title": title,
                    "authors": authors,
                })
            header = tree.xpath("//header[@id='headline']/h1")[0].xpath("string(.)")
            # 推测年份：正则提取1900-2099的数字组合
            # 1. 从url中提取
            # 2. 如果url中没有，从页面中提取，取重复次数最多的组合
            pattern = r"(?<!\d)(19\d{2}|20\d{2})(?!\d)"
            predicated_years = re.findall(pattern, url)
            assert len(predicated_years) <= 1, f"len(predicated_years) > 1, check {url}"
            if len(predicated_years) == 1:
                predicated_year = predicated_years[0]
            else:
                years = re.findall(pattern, resp.text)
                predicated_year = max(set(years), key=years.count)
            with lock:
                paperlist[url] = {
                    "header": header,
                    "year": predicated_year,
                    "papers": papers
                }
        except AssertionError as ae:
            print(f"[!] {ae}\n", end="")
        except Exception as e:
            print(f"[x] {e}\n", end="")
            retry_list.append((url,))

    for link in links:
        retry_list.append((link,))

    while retry_list:
        params = retry_list
        retry_list = []
        # multithread_run(run_get_paper_list, params, 10)

        # 有时会被限制速率
        for i in range(0, len(params), 10):
            multithread_run(run_get_paper_list, params[i:i + 10], 10)
            sleep(10)

    paperlist = dict(sorted(paperlist.items(), key=lambda x: x[1]["year"], reverse=True))
    with open(f"output/paperlists/{key.replace('/', '-')}.json", "w", encoding="utf-8") as f:
        json.dump(paperlist, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # 测试链接有效性
    # ping()

    # 获取所有会议年份/期刊卷的链接，保存到output/dblp_detail_url.json
    # get_detail_url()

    # 获取论文列表，由于任务量大，逐个期刊/会议进行，保存到output/paperlists/<typ-index>
    # with open("output/dblp_detail_url.json", "r", encoding="utf-8") as f:
    #     dblp_detail_url = json.load(f)
    # for key, detail in dblp_detail_url.items():
    #     get_paper_list(key, detail["links"])

    pass
