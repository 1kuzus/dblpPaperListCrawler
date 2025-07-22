# dblpPaperlistCrawler

`A web crawler for collecting paper lists from dblp.org`

## 简介

爬取了[https://dblp.org](https://dblp.org)上的网络安全等领域的论文数据（标题&作者），具体会议和期刊主要参考了[中国计算机学会推荐国际学术会议和期刊目录-2022更名版](https://www.ccf.org.cn/ccf/contentcore/resource/download?ID=FE0A8E6CB2A39A42BE7701819F54CBB01DD9A874BD99C2BEC97A342E61629613)。

## 文件说明

一般来说，需要的文件是`output/paperlists/`目录下的`<typ-index>.json`。这些是每个期刊/会议提取到的论文列表，包含标题和作者。`typ`应为`conf`或`journals`，`index`为期刊/会议在网站上的索引，如`sp`、`ccs`、`uss`、`ndss`。

下面是仓库中的其他文件：

| 文件                              | 说明                                                                               |
|:--------------------------------|:---------------------------------------------------------------------------------|
| `main.py`                       | 爬虫脚本                                                                             |
| `ccf2022.pdf`                   | 中国计算机学会推荐国际学术会议和期刊目录-2022更名版。（注：此文件的发布时间是2024年6月）                                |
| `output/dblp_detail_url.json`   | 从`<typ/index>`（每个期刊/会议）到全称和站内详情URL的映射。详情URL是期刊的各卷/各年份的会议。                        |
| `output/full_name_mapping.json` | `dblp_detail_url.json`的子集，仅包含从`<typ/index>`到全称的映射，便于核对（有些期刊/会议会用旧的名称简写做`index`）。 |

## 使用方法

### 只需要数据

论文数据保存于`output/paperlists/`目录下的`<typ-index>.json`。目前包括了CCF推荐期刊/会议中的**网络与信息安全**、**软件工程/系统软件/程序设计语言**、**计算机网络**三个类别下的A、B、C类期刊/会议。

### 补充其他期刊/会议

1. 参照原有格式，修改`main.py`中的`indices`；
2. 在主函数中：
    ```python
    if __name__ == "__main__":
        # 测试链接有效性
        ping()
    
        # 获取所有会议年份/期刊卷的链接，保存到output/dblp_detail_url.json
        get_detail_url()
    
        # 获取论文列表，由于任务量大，逐个期刊/会议进行，保存到output/paperlists/<typ-index>
        with open("output/dblp_detail_url.json", "r", encoding="utf-8") as f:
            dblp_detail_url = json.load(f)
        for key, detail in dblp_detail_url.items():
            get_paper_list(key, detail["links"])
    ```
   - `ping()`仅测试`indices`中的索引是否有效，并把无效的索引输出到控制台，不会影响结果，不起过滤作用。请确保执行后续逻辑时`indices`中的索引均是有效的。
   - `get_detail_url()`获取站内详情URL。
   - `get_paper_list()`获取论文列表。

   三个步骤可独立运行，使用时解注释对应的逻辑即可。注意`ping()`非必需，`get_paper_list()`需要先生成`dblp_detail_url.json`。

<br>

**1kuzus**
