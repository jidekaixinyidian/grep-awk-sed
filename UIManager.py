# 这段直接照搬V1.0 毕竟我Tkinter学的一塌糊涂

import platform
import tkinter as tk
from tkinter import ttk, scrolledtext

from AwkHandler import AwkHandler
from GrepHandler import GrepHandler
from SedHandler import SedHandler


class UIManager:

    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        self.root.title("脚本生成工具")
        self.root.geometry("900x900")
        self.root.minsize(800, 600)

        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 创建各个UI部分
        self._create_header(main_frame)
        self._create_platform_selector(main_frame)
        self._create_command_sections(main_frame)
        self._create_file_selector(main_frame)
        self._create_action_buttons(main_frame)
        self._create_output_area(main_frame)

        # 设置行权重
        main_frame.rowconfigure(4, weight=1)

    def _create_header(self, parent):
        """创建标题"""
        title_label = ttk.Label(
            parent,
            text="脚本生成工具",
            font=("Minecraft AE", 23, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

    def _create_platform_selector(self, parent):
        """创建平台选择器"""
        platform_frame = ttk.Frame(parent)
        platform_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(platform_frame, text="平台模式:").grid(
            row=0, column=0, padx=(0, 5)
        )

        self.platform_var = tk.StringVar(value="auto")
        platform_combo = ttk.Combobox(
            platform_frame,
            textvariable=self.platform_var,
            values=["auto", "windows", "linux"],
            state="readonly",
            width=10
        )
        platform_combo.grid(row=0, column=1, padx=(0, 10))

        # 显示当前检测到的平台
        self.platform_info = ttk.Label(
            platform_frame,
            text=f"检测到: {platform.system()}",
            foreground="gray"
        )
        self.platform_info.grid(row=0, column=2)

        # 绑定事件
        platform_combo.bind('<<ComboboxSelected>>', self.app.on_platform_changed)

    def _create_command_sections(self, parent):
        """创建命令区域"""
        commands_frame = ttk.Frame(parent)
        commands_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        commands_frame.columnconfigure((0, 1, 2), weight=1)

        # grep区域
        self._create_grep_section(commands_frame, 0)

        # awk区域
        self._create_awk_section(commands_frame, 1)

        # sed区域
        self._create_sed_section(commands_frame, 2)

    def _create_grep_section(self, parent, column):
        """创建grep区域"""
        frame = ttk.LabelFrame(parent, text="grep 命令", padding="10")
        frame.grid(row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        frame.columnconfigure(0, weight=1)

        # 参数选择
        ttk.Label(frame, text="参数选项:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )

        self.grep_option_var = tk.StringVar(value="无")
        grep_combo = ttk.Combobox(
            frame,
            textvariable=self.grep_option_var,
            values=list(GrepHandler.OPTIONS.keys()),
            state="readonly"
        )
        grep_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        grep_combo.bind('<<ComboboxSelected>>', self.app.on_grep_option_changed)

        # 模式输入
        ttk.Label(frame, text="搜索内容:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )

        self.grep_pattern_var = tk.StringVar()
        grep_entry = ttk.Entry(frame, textvariable=self.grep_pattern_var)
        grep_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # 示例标签
        self.grep_example_label = ttk.Label(
            frame,
            text="示例: INFO",
            foreground="gray",
            font=("Minecraft AE", 14)
        )
        self.grep_example_label.grid(row=4, column=0, sticky=tk.W)

    def _create_awk_section(self, parent, column):
        """创建awk区域"""
        frame = ttk.LabelFrame(parent, text="awk 命令", padding="10")
        frame.grid(row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        frame.columnconfigure(0, weight=1)

        # 操作选择
        ttk.Label(frame, text="操作类型:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )

        self.awk_option_var = tk.StringVar(value="无")
        awk_combo = ttk.Combobox(
            frame,
            textvariable=self.awk_option_var,
            values=list(AwkHandler.OPTIONS.keys()),
            state="readonly"
        )
        awk_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        awk_combo.bind('<<ComboboxSelected>>', self.app.on_awk_option_changed)

        # 参数输入
        ttk.Label(frame, text="参数/脚本:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )

        self.awk_script_var = tk.StringVar()
        awk_entry = ttk.Entry(frame, textvariable=self.awk_script_var)
        awk_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # 示例标签
        self.awk_example_label = ttk.Label(
            frame,
            text="示例: 1",
            foreground="gray",
            font=("Minecraft AE", 14)
        )
        self.awk_example_label.grid(row=4, column=0, sticky=tk.W)

    def _create_sed_section(self, parent, column):
        """创建sed区域"""
        frame = ttk.LabelFrame(parent, text="sed 命令", padding="10")
        frame.grid(row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        frame.columnconfigure(0, weight=1)

        # 操作选择
        ttk.Label(frame, text="操作类型:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )

        self.sed_option_var = tk.StringVar(value="无")
        sed_combo = ttk.Combobox(
            frame,
            textvariable=self.sed_option_var,
            values=list(SedHandler.OPTIONS.keys()),
            state="readonly"
        )
        sed_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        sed_combo.bind('<<ComboboxSelected>>', self.app.on_sed_option_changed)

        # 参数输入
        ttk.Label(frame, text="参数/命令:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )

        self.sed_command_var = tk.StringVar()
        sed_entry = ttk.Entry(frame, textvariable=self.sed_command_var)
        sed_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # 示例标签
        self.sed_example_label = ttk.Label(
            frame,
            text="示例: old/new",
            foreground="gray",
            font=("Minecraft AE", 14)
        )
        self.sed_example_label.grid(row=4, column=0, sticky=tk.W)

    def _create_file_selector(self, parent):
        """创建文件选择器"""
        file_frame = ttk.Frame(parent)
        file_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text="输入文件:").grid(
            row=0, column=0, padx=(0, 5)
        )

        self.file_var = tk.StringVar(value="sample_data.txt")
        self.file_entry = ttk.Entry(
            file_frame,
            textvariable=self.file_var
        )
        self.file_entry.grid(
            row=0, column=1,
            sticky=(tk.W, tk.E),
            padx=(0, 5)
        )

        ttk.Button(
            file_frame,
            text="浏览",
            command=self.app.browse_file
        ).grid(row=0, column=2)

    def _create_action_buttons(self, parent):
        """创建操作按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, pady=(0, 10))

        # 执行按钮
        self.execute_btn = ttk.Button(
            button_frame,
            text="执行命令",
            command=self.app.execute_command,
            width=15
        )
        self.execute_btn.grid(row=0, column=0, padx=5)

        # 保存按钮
        self.save_btn = ttk.Button(
            button_frame,
            text="保存脚本",
            command=self.app.save_script,
            width=15
        )
        self.save_btn.grid(row=0, column=1, padx=5)

        # 复制按钮
        self.copy_btn = ttk.Button(
            button_frame,
            text="复制命令",
            command=self.app.copy_command,
            width=15
        )
        self.copy_btn.grid(row=0, column=2, padx=5)

    def _create_output_area(self, parent):
        """创建输出区域"""
        output_frame = ttk.LabelFrame(
            parent,
            text="输出结果",
            padding="10"
        )
        output_frame.grid(
            row=5, column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            pady=(0, 10)
        )
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)

        # 命令显示区域
        command_frame = ttk.Frame(output_frame)
        command_frame.grid(
            row=0, column=0,
            sticky=(tk.W, tk.E),
            pady=(0, 10)
        )
        command_frame.columnconfigure(0, weight=1)

        ttk.Label(command_frame, text="生成的命令:").grid(
            row=0, column=0, sticky=tk.W
        )

        self.command_var = tk.StringVar()
        self.command_entry = ttk.Entry(
            command_frame,
            textvariable=self.command_var,
            state="readonly",
            font=("Consolas", 15)
        )
        self.command_entry.grid(
            row=1, column=0,
            sticky=(tk.W, tk.E),
            padx=(0, 5)
        )

        # 执行结果显示区域
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 15)
        )
        self.output_text.grid(
            row=1, column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S)
        )