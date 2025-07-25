import os
from utils import load_json


def validate(output_dir):
    path_indexing_pages = os.path.join(output_dir, "indexing_pages.json")
    path_full_name_mapping = os.path.join(output_dir, "full_name_mapping.json")
    assert os.path.exists(path_indexing_pages)
    assert os.path.exists(path_full_name_mapping)
    indexing_pages = load_json(path_indexing_pages)
    full_name_mapping = load_json(path_full_name_mapping)
    assert set(indexing_pages.keys()) == set(full_name_mapping.keys())
    for key in indexing_pages.keys():
        typ, index = key.split("/")
        path_paper_list = os.path.join(output_dir, "paper_lists", typ, f"{index}.json")
        assert os.path.exists(path_paper_list)
        paper_list = load_json(path_paper_list)
        links = indexing_pages[key]["links"]
        s1, s2 = set(links), set(paper_list.keys())
        if s1 != s2:
            print(f"[!] {key}: Links in indexing_page do not match paper_list.keys(), the difference links are:")
            for link in s1 ^ s2:
                print(" " * 4, link)
            print(" " * 4, f"You can remove them from {path_indexing_pages} and run the script again.")
        print(f"[*] {key} validated successfully.")


if __name__ == "__main__":
    validate(output_dir="./output")
