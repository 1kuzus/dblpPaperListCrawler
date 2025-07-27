z# dblpPaperListCrawler

`A web crawler for collecting paper lists from dblp.org`

## 简介

爬取[dblp.org](https://dblp.org)上论文列表的脚本，支持指定期刊/会议爬取，获取的数据为论文列表，包含标题和作者。

如需全量论文数据可以下载[官方XML文件](https://dblp.org/xml/)（每日更新，解压缩后约5G）。

## 已有数据

仓库中已经包含了[中国计算机学会推荐国际学术会议和期刊目录-2022更名版](https://www.ccf.org.cn/ccf/contentcore/resource/download?ID=FE0A8E6CB2A39A42BE7701819F54CBB01DD9A874BD99C2BEC97A342E61629613)
（此文件的发布时间是2024年6月）中**网络与信息安全**、**计算机网络**、**软件工程/系统软件/程序设计语言**
三个方向的A类、B类、C类共`192`个期刊/会议的爬取结果。最近更新时间为`2025-07-27`。

仓库中已爬取的期刊/会议列表见[`output/full_name_mapping.json`](output/full_name_mapping.json)
，每个期刊/会议的论文列表见[`output/paper_lists/`](output/paper_lists)。

## 使用方法

安装依赖：

```
pip install requests lxml
```

想要自定义爬取的期刊/会议，只需要参照[`main.py`](main.py)修改`indices`即可。

```python
from crawler import get_paper_lists

indices = {
    "journals": ["pami"],
    "conf": ["cvpr", "iccv", "eccv"],
}

if __name__ == "__main__":
    get_paper_lists(indices, output_dir="./path/to/output")
```

`indices`中的值应该与[dblp.org](https://dblp.org)
中各个期刊/会议的URL路径一致，具体路径可以参考[`ccf2022.pdf`](ccf2022.pdf)。
