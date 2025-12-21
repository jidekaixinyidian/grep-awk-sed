class GrepHandler:

    OPTIONS = {
        "无": "",
        "忽略大小写 (-i)": "-i",
        "反向匹配 (-v)": "-v",
        "显示行号 (-n)": "-n",
        "只统计命中行数 (-c)": "-c",
        "只输出文件名 (-l)": "-l",
        "整词匹配 (-w)": "-w",
        "递归子目录 (-r)": "-r",
        "输出命中行及后3行 (-A3)": "-A3",
        "输出命中行及前2行 (-B2)": "-B2",
        "启用扩展正则 (-E)": "-E",
        "忽略大小写+行号 (-in)": "-in",
        "整词+忽略大小写 (-iw)": "-iw",
        "递归+行号 (-rn)": "-rn"
    }

    EXAMPLES = {
        "无": "ERROR",
        "忽略大小写 (-i)": "error",
        "反向匹配 (-v)": "SUCCESS",
        "显示行号 (-n)": "INFO",
        "只统计命中行数 (-c)": "ERROR",
        "只输出文件名 (-l)": "pattern",
        "整词匹配 (-w)": "word",
        "递归子目录 (-r)": "pattern",
        "输出命中行及后3行 (-A3)": "ERROR",
        "输出命中行及前2行 (-B2)": "WARNING",
        "启用扩展正则 (-E)": "(ERROR|WARN)",
        "忽略大小写+行号 (-in)": "info",
        "整词+忽略大小写 (-iw)": "Error",
        "递归+行号 (-rn)": "pattern"
    }

    @staticmethod
    def get_example(option):
        return GrepHandler.EXAMPLES.get(option, "pattern")

    @staticmethod
    def build_command(option, pattern, filename=None):
        if not pattern:
            return None

        cmd_parts = ["grep"]

        if option in GrepHandler.OPTIONS:
            option_value = GrepHandler.OPTIONS[option]
            if option_value:
                cmd_parts.append(option_value)

        cmd_parts.append(pattern)

        if filename:
            cmd_parts.append(filename)

        return " ".join(cmd_parts)