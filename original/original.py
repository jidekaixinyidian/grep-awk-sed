#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本输出工具 - sed、awk、grep 命令快速编写与执行
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import os
import threading

class ScriptOutputTool:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("脚本输出")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="脚本输出", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 命令区域框架
        commands_frame = ttk.Frame(main_frame)
        commands_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        commands_frame.columnconfigure((0, 1, 2), weight=1)
        
        # grep 区域
        self.setup_grep_section(commands_frame, 0)
        
        # awk 区域  
        self.setup_awk_section(commands_frame, 1)
        
        # sed 区域
        self.setup_sed_section(commands_frame, 2)
        
        # 文件选择区域
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="文件名:").grid(row=0, column=0, padx=(0, 5))
        self.file_var = tk.StringVar(value="sample_data.txt")
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var)
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(file_frame, text="浏览", command=self.browse_file).grid(row=0, column=2)
        
        # 执行按钮
        execute_btn = ttk.Button(main_frame, text="执行", command=self.execute_command)
        execute_btn.grid(row=3, column=0, pady=(0, 10))
        
        # 输出区域
        output_frame = ttk.LabelFrame(main_frame, text="输出结果", padding="5")
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)
        
        # 命令显示和复制区域
        command_frame = ttk.Frame(output_frame)
        command_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        command_frame.columnconfigure(0, weight=1)
        
        ttk.Label(command_frame, text="生成的命令:").grid(row=0, column=0, sticky=tk.W)
        
        command_display_frame = ttk.Frame(command_frame)
        command_display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        command_display_frame.columnconfigure(0, weight=1)
        
        self.command_var = tk.StringVar()
        self.command_entry = ttk.Entry(command_display_frame, textvariable=self.command_var, 
                                      state="readonly", font=("Consolas", 10))
        self.command_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.copy_button = ttk.Button(command_display_frame, text="复制", command=self.copy_command)
        self.copy_button.grid(row=0, column=1)
        
        # 执行结果显示区域
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, wrap=tk.WORD)
        self.output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        main_frame.rowconfigure(4, weight=1)

    def setup_grep_section(self, parent, column):
        """设置 grep 命令区域"""
        frame = ttk.LabelFrame(parent, text="grep", padding="5")
        frame.grid(row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        frame.columnconfigure(0, weight=1)
        
        # grep 参数选项 (纯过滤)
        grep_options = [
            ("无", ""),
            ("忽略大小写 (-i)", "-i"),
            ("反向匹配 (-v)", "-v"),
            ("显示行号 (-n)", "-n"),
            ("只统计命中行数 (-c)", "-c"),
            ("只输出文件名 (-l)", "-l"),
            ("整词匹配 (-w)", "-w"),
            ("递归子目录 (-r)", "-r"),
            ("输出命中行及后3行 (-A3)", "-A3"),
            ("输出命中行及前2行 (-B2)", "-B2"),
            ("启用扩展正则 (-E)", "-E"),
            ("忽略大小写+行号 (-in)", "-in"),
            ("整词+忽略大小写 (-iw)", "-iw"),
            ("递归+行号 (-rn)", "-rn")
        ]
        
        ttk.Label(frame, text="参数:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.grep_option_var = tk.StringVar(value="")
        grep_combo = ttk.Combobox(frame, textvariable=self.grep_option_var, 
                                 values=[opt[0] for opt in grep_options], state="readonly")
        grep_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 设置选项映射
        self.grep_options_map = {opt[0]: opt[1] for opt in grep_options}
        
        ttk.Label(frame, text="模式/参数:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.grep_pattern_var = tk.StringVar()
        grep_entry = ttk.Entry(frame, textvariable=self.grep_pattern_var)
        grep_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 示例标签
        self.grep_example_label = ttk.Label(frame, text="示例: ERROR", foreground="gray", font=("Arial", 8))
        self.grep_example_label.grid(row=4, column=0, sticky=tk.W)
        
        # 绑定下拉框选择事件
        grep_combo.bind('<<ComboboxSelected>>', self.on_grep_option_changed)
        
    def setup_awk_section(self, parent, column):
        """设置 awk 命令区域"""
        frame = ttk.LabelFrame(parent, text="awk", padding="5")
        frame.grid(row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        frame.columnconfigure(0, weight=1)
        
        # awk 选项 (列处理+统计)
        awk_options = [
            ("无", ""),
            ("取第N列", "print_column"),
            ("逗号分隔符取列", "csv_column"),
            ("TAB分隔符取列", "tsv_column"),
            ("带行号全行输出", "number_lines"),
            ("只保留列数>N的行", "filter_columns"),
            ("第N列数值过滤", "filter_value"),
            ("输出换分隔符", "change_separator"),
            ("累加求和", "sum_column"),
            ("按第N列去重", "unique_column"),
            ("外部传参过滤", "external_var"),
            ("自定义", "custom")
        ]
        
        ttk.Label(frame, text="操作:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.awk_option_var = tk.StringVar(value="")
        awk_combo = ttk.Combobox(frame, textvariable=self.awk_option_var,
                                values=[opt[0] for opt in awk_options], state="readonly")
        awk_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.awk_options_map = {opt[0]: opt[1] for opt in awk_options}
        
        ttk.Label(frame, text="参数 (列号/分隔符/条件等):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.awk_script_var = tk.StringVar()
        awk_entry = ttk.Entry(frame, textvariable=self.awk_script_var)
        awk_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 示例标签
        self.awk_example_label = ttk.Label(frame, text="示例: 1", foreground="gray", font=("Arial", 8))
        self.awk_example_label.grid(row=4, column=0, sticky=tk.W)
        
        # 绑定下拉框选择事件
        awk_combo.bind('<<ComboboxSelected>>', self.on_awk_option_changed)
        
    def setup_sed_section(self, parent, column):
        """设置 sed 命令区域"""
        frame = ttk.LabelFrame(parent, text="sed", padding="5")
        frame.grid(row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        frame.columnconfigure(0, weight=1)
        
        # sed 选项 (行内替换/增删)
        sed_options = [
            ("无", ""),
            ("全局替换", "replace_global"),
            ("忽略大小写替换", "replace_ignore_case"),
            ("删除首行", "delete_first"),
            ("删除末行", "delete_last"),
            ("删除注释行", "delete_comments"),
            ("原地备份修改", "inplace_backup"),
            ("只输出指定行范围", "print_range"),
            ("去掉行首空格", "trim_left"),
            ("去掉行尾空格", "trim_right"),
            ("在第1行前插入", "insert_header"),
            ("删除空行", "delete_empty"),
            ("自定义", "custom")
        ]
        
        ttk.Label(frame, text="操作:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.sed_option_var = tk.StringVar(value="")
        sed_combo = ttk.Combobox(frame, textvariable=self.sed_option_var,
                                values=[opt[0] for opt in sed_options], state="readonly")
        sed_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.sed_options_map = {opt[0]: opt[1] for opt in sed_options}
        
        ttk.Label(frame, text="参数 (替换内容/模式/行号等):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.sed_command_var = tk.StringVar()
        sed_entry = ttk.Entry(frame, textvariable=self.sed_command_var)
        sed_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 示例标签
        self.sed_example_label = ttk.Label(frame, text="示例: old/new", foreground="gray", font=("Arial", 8))
        self.sed_example_label.grid(row=4, column=0, sticky=tk.W)
        
        # 绑定下拉框选择事件
        sed_combo.bind('<<ComboboxSelected>>', self.on_sed_option_changed)

    def on_grep_option_changed(self, event=None):
        """grep 选项改变时更新示例"""
        option = self.grep_option_var.get()
        examples = {
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
        example = examples.get(option, "pattern")
        self.grep_example_label.config(text=f"示例: {example}")
    
    def on_awk_option_changed(self, event=None):
        """awk 选项改变时更新示例"""
        option = self.awk_option_var.get()
        examples = {
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
        example = examples.get(option, "1")
        self.awk_example_label.config(text=f"示例: {example}")
    
    def on_sed_option_changed(self, event=None):
        """sed 选项改变时更新示例"""
        option = self.sed_option_var.get()
        examples = {
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
        example = examples.get(option, "old/new")
        self.sed_example_label.config(text=f"示例: {example}")

    def _parse_columns(self, column_input):
        """解析列输入，支持多种格式"""
        if not column_input:
            return "$1"
        
        # 去除空格
        column_input = column_input.strip()
        
        # 处理范围格式 (如 2-4)
        if '-' in column_input and ',' not in column_input:
            try:
                start, end = map(int, column_input.split('-'))
                columns = [f"${i}" for i in range(start, end + 1)]
                return ','.join(columns)
            except ValueError:
                pass
        
        # 处理逗号分隔的多列 (如 1,3,5)
        if ',' in column_input:
            try:
                column_numbers = [int(x.strip()) for x in column_input.split(',')]
                columns = [f"${num}" for num in column_numbers]
                return ','.join(columns)
            except ValueError:
                pass
        
        # 处理单列 (如 1)
        try:
            column_num = int(column_input)
            return f"${column_num}"
        except ValueError:
            # 如果解析失败，返回原始输入（可能是复杂表达式）
            return column_input

    def copy_command(self):
        """复制命令到剪贴板"""
        command = self.command_var.get()
        if command:
            self.root.clipboard_clear()
            self.root.clipboard_append(command)
            messagebox.showinfo("复制成功", "命令已复制到剪贴板")
        else:
            messagebox.showwarning("提示", "没有可复制的命令")

    def browse_file(self):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("日志文件", "*.log"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.file_var.set(filename)
    
    def get_selected_command(self):
        """获取当前选中的命令"""
        commands = []
        
        # grep 命令
        grep_option = self.grep_option_var.get()
        grep_pattern = self.grep_pattern_var.get().strip()
        if grep_pattern:
            grep_cmd = "grep"
            if grep_option in self.grep_options_map:
                option_value = self.grep_options_map[grep_option]
                if option_value:
                    grep_cmd += f" {option_value}"
            grep_cmd += f" {grep_pattern}"
            commands.append(grep_cmd)
        
        # awk 命令
        awk_option = self.awk_option_var.get()
        awk_script = self.awk_script_var.get().strip()
        if awk_option in self.awk_options_map:
            option_value = self.awk_options_map[awk_option]
            if option_value == "print_column" and awk_script:
                # 取第N列，支持多列输入
                columns = self._parse_columns(awk_script)
                commands.append(f"awk '{{print {columns}}}'")
            elif option_value == "csv_column" and awk_script:
                # 逗号分隔符取列，支持多列输入
                columns = self._parse_columns(awk_script)
                commands.append(f"awk -F',' '{{print {columns}}}'")
            elif option_value == "tsv_column" and awk_script:
                # TAB分隔符取列，支持多列输入
                columns = self._parse_columns(awk_script)
                commands.append(f"awk -F'\\t' '{{print {columns}}}'")
            elif option_value == "number_lines":
                # 带行号全行输出 awk '{print NR,$0}'
                commands.append("awk '{print NR,$0}'")
            elif option_value == "filter_columns" and awk_script:
                # 只保留列数>N的行，如输入 "5" 生成 awk 'NF>5'
                commands.append(f"awk 'NF>{awk_script}'")
            elif option_value == "filter_value" and awk_script:
                # 第N列数值过滤，如输入 "3>100" 生成 awk '$3>100'
                if ">" in awk_script or "<" in awk_script or "=" in awk_script:
                    commands.append(f"awk '${awk_script}'")
                else:
                    commands.append(f"awk '${awk_script}>0'")
            elif option_value == "change_separator" and awk_script:
                # 输出换分隔符，如输入 ";" 生成 awk 'BEGIN{OFS=";"} {print $1,$2}'
                if "," in awk_script:
                    sep, cols = awk_script.split(",", 1)
                    commands.append(f"awk 'BEGIN{{OFS=\"{sep}\"}} {{print {cols}}}'")
                else:
                    commands.append(f"awk 'BEGIN{{OFS=\"{awk_script}\"}} {{print $1,$2}}'")
            elif option_value == "sum_column" and awk_script:
                # 累加求和，如输入 "4" 生成 awk '{sum+=$4} END{print sum}'
                commands.append(f"awk '{{sum+=${awk_script}}} END{{print sum}}'")
            elif option_value == "unique_column" and awk_script:
                # 按第N列去重，如输入 "1" 生成 awk '!a[$1]++'
                commands.append(f"awk '!a[${awk_script}]++'")
            elif option_value == "external_var" and awk_script:
                # 外部传参，如输入 "TH=100,3>TH" 生成 awk -v TH=100 '$3>TH'
                if "," in awk_script:
                    var_def, condition = awk_script.split(",", 1)
                    commands.append(f"awk -v {var_def} '{condition}'")
                else:
                    commands.append(f"awk -v {awk_script} '1'")
            elif option_value == "custom" and awk_script:
                commands.append(f"awk '{awk_script}'")
            elif awk_script and not option_value:
                # 如果只有脚本输入，没有选择预设模式
                commands.append(f"awk '{awk_script}'")
        
        # sed 命令
        sed_option = self.sed_option_var.get()
        sed_command = self.sed_command_var.get().strip()
        if sed_option in self.sed_options_map:
            option_value = self.sed_options_map[sed_option]
            if option_value == "replace_global" and sed_command:
                # 全局替换，如输入 "old/new" 生成 sed 's/old/new/g'
                if "/" in sed_command:
                    commands.append(f"sed 's/{sed_command}/g'")
                else:
                    commands.append(f"sed 's/{sed_command}//g'")
            elif option_value == "replace_ignore_case" and sed_command:
                # 忽略大小写替换，如输入 "old/new" 生成 sed 's/old/new/ig'
                if "/" in sed_command:
                    commands.append(f"sed 's/{sed_command}/ig'")
                else:
                    commands.append(f"sed 's/{sed_command}//ig'")
            elif option_value == "delete_first":
                # 删除首行 sed '1d'
                commands.append("sed '1d'")
            elif option_value == "delete_last":
                # 删除末行 sed '$d'
                commands.append("sed '$d'")
            elif option_value == "delete_comments":
                # 删除注释行 sed '/^#/d'
                commands.append("sed '/^#/d'")
            elif option_value == "inplace_backup" and sed_command:
                # 原地备份修改，如输入 "old/new" 生成 sed -i.bak 's/old/new/g'
                if "/" in sed_command:
                    commands.append(f"sed -i.bak 's/{sed_command}/g'")
                else:
                    commands.append(f"sed -i.bak 's/{sed_command}//g'")
            elif option_value == "print_range" and sed_command:
                # 只输出指定行范围，如输入 "5,10" 生成 sed -n '5,10p'
                commands.append(f"sed -n '{sed_command}p'")
            elif option_value == "trim_left":
                # 去掉行首空格 sed 's/^ *//'
                commands.append("sed 's/^ *//'")
            elif option_value == "trim_right":
                # 去掉行尾空格 sed 's/ *$//'
                commands.append("sed 's/ *$//'")
            elif option_value == "insert_header" and sed_command:
                # 在第1行前插入，如输入 "header" 生成 sed '1i\header'
                commands.append(f"sed '1i\\{sed_command}'")
            elif option_value == "delete_empty":
                # 删除空行 sed '/^$/d'
                commands.append("sed '/^$/d'")
            elif option_value == "custom" and sed_command:
                commands.append(f"sed '{sed_command}'")
            elif sed_command and not option_value:
                # 如果只有命令输入，没有选择预设操作
                commands.append(f"sed '{sed_command}'")
        
        return commands
    
    def execute_command(self):
        """执行命令"""
        commands = self.get_selected_command()
        input_file = self.file_var.get().strip()
        
        # 清空输出区域
        self.output_text.delete(1.0, tk.END)
        self.command_var.set("")
        
        if not commands:
            self.output_text.insert(tk.END, "请至少配置一个命令\n")
            return
        
        # 构建管道格式的命令
        if input_file:
            if len(commands) == 1:
                # 单个命令：cat filename | command 或 command filename
                if any(cmd.startswith(('grep', 'sed')) for cmd in commands):
                    # grep 和 sed 可以直接接文件名
                    pipeline_command = f"{commands[0]} {input_file}"
                else:
                    # awk 等使用管道
                    pipeline_command = f"cat {input_file} | {commands[0]}"
            else:
                # 多个命令：cat filename | cmd1 | cmd2 | cmd3
                pipeline_command = f"cat {input_file} | " + " | ".join(commands)
        else:
            # 没有文件名，只显示命令结构
            if len(commands) == 1:
                pipeline_command = commands[0]
            else:
                pipeline_command = " | ".join(commands)
        
        # 显示在命令框中
        self.command_var.set(pipeline_command)
        
        # 显示执行信息
        self.output_text.insert(tk.END, f"生成的管道命令:\n{pipeline_command}\n\n")
        
        # 如果有输入文件且文件存在，执行命令
        if input_file and os.path.exists(input_file):
            self.output_text.insert(tk.END, "执行结果:\n")
            self.output_text.insert(tk.END, "-" * 40 + "\n")
            # 在新线程中执行命令，避免界面冻结
            threading.Thread(target=self._run_commands, args=(commands, input_file), daemon=True).start()
        elif input_file and not os.path.exists(input_file):
            self.output_text.insert(tk.END, f"注意: 文件 '{input_file}' 不存在，无法执行\n")
        else:
            self.output_text.insert(tk.END, "提示: 输入文件名后可执行命令查看结果\n")
    
    def _run_commands(self, commands, input_file):
        """在后台线程中运行命令"""
        try:
            # 构建执行命令
            if len(commands) == 1:
                # 单个命令处理
                if any(cmd.startswith(('grep', 'sed')) for cmd in commands):
                    # grep 和 sed 可以直接接文件名
                    full_command = f"{commands[0]} \"{input_file}\""
                else:
                    # awk 等使用管道
                    full_command = f"type \"{input_file}\" | {commands[0]}"
            else:
                # 多个命令用管道连接
                full_command = f"type \"{input_file}\" | " + " | ".join(commands)
            
            # 执行命令
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            # 显示结果
            if result.stdout:
                self.root.after(0, lambda: self.output_text.insert(tk.END, result.stdout))
            else:
                self.root.after(0, lambda: self.output_text.insert(tk.END, "(无输出结果)\n"))
            
            if result.stderr:
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"\n错误信息:\n{result.stderr}"))
            
            if result.returncode != 0:
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"\n命令执行失败，返回码: {result.returncode}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.output_text.insert(tk.END, f"\n执行错误: {str(e)}"))
        
        self.root.after(0, lambda: self.output_text.see(tk.END))

def main():
    root = tk.Tk()
    app = ScriptOutputTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
