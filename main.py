from crawler import ping, get_detail_url, get_paper_list
import json

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

indices = {"journals": ["tifs"], "no": ["no"]}

if __name__ == "__main__":
    # 测试链接有效性，如果修改了indices可以重新测试
    ping(indices)

    # 获取所有会议年份/期刊卷的链接，保存到./output/dblp_detail_url.json
    get_detail_url(indices, output_dir="./output")

    exit(0)
    # 获取论文列表，由于任务量大，逐个期刊/会议进行，保存到output/paperlists/<typ-index>
    with open("output/dblp_detail_url.json", "r", encoding="utf-8") as f:
        dblp_detail_url = json.load(f)
    for key, detail in dblp_detail_url.items():
        get_paper_list(key, detail["links"])
