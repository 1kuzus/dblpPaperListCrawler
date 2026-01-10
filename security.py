from crawler import scrape_paper_lists

indices = {
    "journals": ["tdsc", "tifs", "joc"],
    "conf": ["ccs", "ndss", "uss", "sp"],
}

if __name__ == "__main__":
    scrape_paper_lists(indices, output_dir="./output")
