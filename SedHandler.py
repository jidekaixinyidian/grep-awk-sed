class SedHandler:

    OPTIONS = {
        "无": "",
        "全局替换": "replace_global",
        "忽略大小写替换": "replace_ignore_case",
        "删除首行": "delete_first",
        "删除末行": "delete_last",
        "删除注释行": "delete_comments",
        "原地备份修改": "inplace_backup",
        "只输出指定行范围": "print_range",
        "去掉行首空格": "trim_left",
        "去掉行尾空格": "trim_right",
        "在第1行前插入": "insert_header",
        "删除空行": "delete_empty",
        "自定义": "custom"
    }

    EXAMPLES = {
        "无": "old/new",
        "全局替换": "old/new",
        "忽略大小写替换": "Error/Warning",
        "删除首行": "(无需参数)",
        "删除末行": "(无需参数)",
        "删除注释行": "(无需参数)",
        "原地备份修改": "old/new",
        "只输出指定行范围": "5,10",
        "去掉行首空格": "(无需参数)",
        "去掉行尾空格": "(无需参数)",
        "在第1行前插入": "Header Text",
        "删除空行": "(无需参数)",
        "自定义": "s/old/new/g"
    }

    @staticmethod
    def get_example(option):
        return SedHandler.EXAMPLES.get(option, "old/new")

    @staticmethod
    def build_command(option, command, filename=None):
        cmd = None
        option_value = SedHandler.OPTIONS.get(option, "")

        match option_value:
            case "replace_global" if command:
                if "/" in command:
                    cmd = f"sed 's/{command}/g'"
                else:
                    cmd = f"sed 's/{command}//g'"
            case "replace_ignore_case" if command:
                if "/" in command:
                    cmd = f"sed 's/{command}/ig'"
                else:
                    cmd = f"sed 's/{command}//ig'"
            case "delete_first":
                cmd = "sed '1d'"
            case "delete_last":
                cmd = "sed '$d'"
            case "delete_comments":
                cmd = "sed '/^#/d'"
            case "inplace_backup" if command:
                if "/" in command:
                    cmd = f"sed -i.bak 's/{command}/g'"
                else:
                    cmd = f"sed -i.bak 's/{command}//g'"
            case "print_range" if command:
                cmd = f"sed -n '{command}p'"
            case "trim_left":
                cmd = "sed 's/^ *//'"
            case "trim_right":
                cmd = "sed 's/ *$//'"
            case "insert_header" if command:
                cmd = f"sed '1i\\{command}'"
            case "delete_empty":
                cmd = "sed '/^$/d'"
            case "custom" if command:
                cmd = f"sed '{command}'"
            case "" if command:
                cmd = f"sed '{command}'"

        if cmd and filename:
            cmd += f" {filename}"

        return cmd