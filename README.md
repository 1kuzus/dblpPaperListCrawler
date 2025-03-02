# SecurityPapers-dblp

`dblp.org上的网络安全等领域论文数据`

## 简介

爬取了[https://dblp.org](https://dblp.org)
上的网络安全等领域论文数据（标题&作者），具体会议和期刊主要参考了[中国计算机学会推荐国际学术会议和期刊目录-2022更名版](https://www.ccf.org.cn/ccf/contentcore/resource/download?ID=FE0A8E6CB2A39A42BE7701819F54CBB01DD9A874BD99C2BEC97A342E61629613)。

## 文件说明

一般来说，需要的文件都在`output/paperlists`目录下。

| 路径                                   | 说明                                                                                              |
|:-------------------------------------|:------------------------------------------------------------------------------------------------|
| `main.py`                            | 爬虫脚本                                                                                            |
| `output/paperlists/<typ-index>.json` | 每个期刊/会议提取到的论文列表，包含标题和作者。`typ`应为`conf`或`journals`，`index`为期刊/会议在网站上的索引，如`sp`、`ccs`、`uss`、`ndss`。 |   
| `output/dblp_detail_url.json`        | 从`<typ/index>`（每个期刊/会议）到全称和站内详情URL的映射。详情URL是期刊的各卷/各年份的会议。                                       |
| `output/full_name_mapping.json`      | `dblp_detail_url.json`的子集，仅包含从`<typ/index>`到全称的映射，便于核对（有些期刊/会议会用旧的名称简写做`index`）。                |

<br>

**1kuzus**
