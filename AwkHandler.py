class AwkHandler:

    OPTIONS = {
        "无": "",
        "取第N列": "print_column",
        "逗号分隔符取列": "csv_column",
        "TAB分隔符取列": "tsv_column",
        "带行号全行输出": "number_lines",
        "只保留列数>N的行": "filter_columns",
        "第N列数值过滤": "filter_value",
        "输出换分隔符": "change_separator",
        "累加求和": "sum_column",
        "按第N列去重": "unique_column",
        "外部传参过滤": "external_var",
        "自定义": "custom"
    }

    EXAMPLES = {
        "无": "1",
        "取第N列": "1,3,5 或 2-4",
        "逗号分隔符取列": "2,5 或 1-3",
        "TAB分隔符取列": "1,2",
        "带行号全行输出": "(无需参数)",
        "只保留列数>N的行": "5",
        "第N列数值过滤": "3>100",
        "输出换分隔符": ";,$1,$2",
        "累加求和": "4",
        "按第N列去重": "1",
        "外部传参过滤": "TH=100,$3>TH",
        "自定义": "{print $1}"
    }

    @staticmethod
    def get_example(option):
        return AwkHandler.EXAMPLES.get(option, "1")

    @staticmethod
    def _parse_columns(column_input):
        if not column_input:
            return "$1"

        column_input = column_input.strip()

        # 处理范围格式
        if '-' in column_input and ',' not in column_input:
            try:
                start, end = map(int, column_input.split('-'))
                columns = [f"${i}" for i in range(start, end + 1)]
                return ','.join(columns)
            except ValueError:
                pass

        # 处理逗号分隔内容
        if ',' in column_input:
            try:
                column_numbers = [int(x.strip()) for x in column_input.split(',')]
                columns = [f"${num}" for num in column_numbers]
                return ','.join(columns)
            except ValueError:
                pass

        # HOTFIX: 处理单列
        try:
            column_num = int(column_input)
            return f"${column_num}"
        except ValueError:
            return column_input

    @staticmethod
    def build_command(option, script, filename=None):
        cmd = None
        option_value = AwkHandler.OPTIONS.get(option, "")

        match option_value:
            case "print_column" if script:
                columns = AwkHandler._parse_columns(script)
                cmd = f"awk '{{print {columns}}}'"
            case "csv_column" if script:
                columns = AwkHandler._parse_columns(script)
                cmd = f"awk -F',' '{{print {columns}}}'"
            case "tsv_column" if script:
                columns = AwkHandler._parse_columns(script)
                cmd = f"awk -F'\\t' '{{print {columns}}}'"
            case "number_lines":
                cmd = "awk '{print NR,$0}'"
            case "filter_columns" if script:
                cmd = f"awk 'NF>{script}'"
            case "filter_value" if script:
                if any(op in script for op in ['>', '<', '=', '!']):
                    cmd = f"awk '${script}'"
                else:
                    cmd = f"awk '${script}>0'"
            case "change_separator" if script:
                if "," in script:
                    sep, cols = script.split(",", 1)
                    cmd = f"awk 'BEGIN{{OFS=\"{sep}\"}} {{print {cols}}}'"
                else:
                    cmd = f"awk 'BEGIN{{OFS=\"{script}\"}} {{print $1,$2}}'"
            case "sum_column" if script:
                cmd = f"awk '{{sum+=${script}}} END{{print sum}}'"
            case "unique_column" if script:
                cmd = f"awk '!a[${script}]++'"
            case "external_var" if script:
                if "," in script:
                    var_def, condition = script.split(",", 1)
                    cmd = f"awk -v {var_def} '{condition}'"
                else:
                    cmd = f"awk -v {script} '1'"
            case "custom" if script:
                cmd = f"awk '{script}'"
            case "" if script:
                cmd = f"awk '{script}'"

        if cmd and filename:
            cmd += f" {filename}"

        return cmd