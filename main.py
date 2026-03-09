from crawler import scrape_paper_lists

indices = {
    # 期刊
    "journals": [
        # 网络与信息安全，CCF A类
        "tdsc", "tifs", "joc",

        # 网络与信息安全，CCF B类
        "tissec", "compsec", "dcc", "jcs", "cybersec",

        # 网络与信息安全，CCF C类
        "clsr", "ejisec", "iet-ifs", "imcs", "ijics", "ijisp", "istr", "scn",

        # 计算机网络，CCF A类
        "jsac", "tmc", "ton",

        # 计算机网络，CCF B类
        "toit", "tomccap", "tosn", "cn", "tcom", "twc",

        # 计算机网络，CCF C类
        "adhoc", "comcom", "tnsm", "iet-com", "jnca", "monet", "networks", "ppna", "wicomm", "winet", "iotj", "tiot",

        # 软件工程/系统软件/程序设计语言，CCF A类
        "toplas", "tosem", "tse", "tsc",

        # 软件工程/系统软件/程序设计语言，CCF B类
        "ase", "ese", "iet-sen", "infsof", "jfp", "smr", "jss", "re", "scp", "sosym", "stvr", "spe",

        # 软件工程/系统软件/程序设计语言，CCF C类
        "cl", "ijseke", "sttt", "jlap", "jwe", "soca", "sqj", "tplp", "pacmpl",

        # 其他
        "pacmse",  # Proceedings of the ACM on Software Engineering
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
        "codaspy", "blocksys", "cscloud",

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
        "icws", "middleware", "sas", "esem", "issre", "hotos", "cc",

        # 软件工程/系统软件/程序设计语言，CCF C类
        "pepm", "paste", "aplas", "apsec", "ease", "iceccs", "icst", "ispass", "scam", "compsac", "icfem", "IEEEscc",
        "ispw", "seke", "qrs", "icsr", "icwe", "spin", "atva", "lopstr", "tase", "msr", "refsq", "wicsa",
        "internetware", "rv", "memocode"
    ],
}

if __name__ == "__main__":
    scrape_paper_lists(indices, output_dir="./output", max_workers=10)
