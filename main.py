import tkinter as tk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from tkinter import ttk, scrolledtext, filedialog, messagebox
import tkinter.font as tkfont
import os
import threading
import platform

from AwkHandler import AwkHandler
from GrepHandler import GrepHandler
from SedHandler import SedHandler
from PlatformMode import PlatformMode
from CommandExecutor import CommandExecutor
from UIManager import UIManager


class Main:
    """主应用类"""

    def __init__(self, root):
        self.root = root

        # 初始化处理器
        self.grep_handler = GrepHandler
        self.awk_handler = AwkHandler
        self.sed_handler = SedHandler

        # 初始化执行器（默认自动检测）
        self.executor = CommandExecutor()

        # 初始化UI
        self.ui = UIManager(root, self)

        # 更新平台信息显示
        self._update_platform_info()

    def _update_platform_info(self):
        """更新平台信息显示"""
        cat_cmd = self.executor.get_cat_command()
        platform_text = f"检测到: {platform.system()} (使用 {cat_cmd} 命令)"
        self.ui.platform_info.config(text=platform_text)

    def on_platform_changed(self, event=None):
        """平台模式改变事件"""
        mode_str = self.ui.platform_var.get()

        match mode_str:
            case "auto":
                mode = PlatformMode.AUTO
            case "windows":
                mode = PlatformMode.WINDOWS
            case "linux":
                mode = PlatformMode.LINUX
            case _:
                mode = PlatformMode.AUTO

        self.executor = CommandExecutor(mode)
        self._update_platform_info()

        # 显示提示
        cat_cmd = self.executor.get_cat_command()
        messagebox.showinfo(
            "平台模式已切换",
            f"已切换到 {mode_str} 模式\n"
            f"将使用 {cat_cmd} 命令读取文件"
        )

    def on_grep_option_changed(self, event=None):
        """grep选项改变事件"""
        option = self.ui.grep_option_var.get()
        example = GrepHandler.get_example(option)
        self.ui.grep_example_label.config(text=f"示例: {example}")

    def on_awk_option_changed(self, event=None):
        """awk选项改变事件"""
        option = self.ui.awk_option_var.get()
        example = AwkHandler.get_example(option)
        self.ui.awk_example_label.config(text=f"示例: {example}")

    def on_sed_option_changed(self, event=None):
        """sed选项改变事件"""
        option = self.ui.sed_option_var.get()
        example = SedHandler.get_example(option)
        self.ui.sed_example_label.config(text=f"示例: {example}")

    def browse_file(self):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("日志文件", "*.log"),
                ("CSV文件", "*.csv"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.ui.file_var.set(filename)

    def copy_command(self):
        """复制命令到剪贴板"""
        command = self.ui.command_var.get()
        if command:
            self.root.clipboard_clear()
            self.root.clipboard_append(command)
            messagebox.showinfo("复制成功", "命令已复制到剪贴板")
        else:
            messagebox.showwarning("提示", "没有可复制的命令")

    def save_script(self):
        """保存脚本到文件"""
        # 构建命令
        commands = self._get_selected_commands()
        if not commands:
            messagebox.showwarning("提示", "没有可保存的命令")
            return

        input_file = self.ui.file_var.get().strip()

        # 确定文件扩展名
        default_ext = ".sh" if "linux" in self.executor.current_platform else ".bat"
        filetypes = [
            ("Shell脚本", "*.sh"),
            ("批处理文件", "*.bat"),
            ("文本文件", "*.txt"),
            ("所有文件", "*.*")
        ]

        # 选择保存位置
        filename = filedialog.asksaveasfilename(
            title="保存脚本",
            defaultextension=default_ext,
            filetypes=filetypes
        )

        if filename:
            success, result = self.executor.save_to_file(
                commands, input_file, filename
            )

            if success:
                messagebox.showinfo(
                    "保存成功",
                    f"脚本已保存到:\n{filename}\n\n"
                    f"文件已{'添加执行权限' if filename.endswith('.sh') else '保存为文本'}"
                )
            else:
                messagebox.showerror("保存失败", f"保存失败: {result}")

    def _get_selected_commands(self):
        """获取选中的命令"""
        commands = []

        # grep命令
        grep_option = self.ui.grep_option_var.get()
        grep_pattern = self.ui.grep_pattern_var.get().strip()
        if grep_pattern:
            cmd = GrepHandler.build_command(grep_option, grep_pattern)
            if cmd:
                commands.append(cmd)

        # awk命令
        awk_option = self.ui.awk_option_var.get()
        awk_script = self.ui.awk_script_var.get().strip()
        if awk_option or awk_script:
            cmd = AwkHandler.build_command(awk_option, awk_script)
            if cmd:
                commands.append(cmd)

        # sed命令
        sed_option = self.ui.sed_option_var.get()
        sed_command = self.ui.sed_command_var.get().strip()
        if sed_option or sed_command:
            cmd = SedHandler.build_command(sed_option, sed_command)
            if cmd:
                commands.append(cmd)

        return commands

    def execute_command(self):
        """执行命令"""
        # 获取命令
        commands = self._get_selected_commands()
        input_file = self.ui.file_var.get().strip()

        # 清空输出区域
        self.ui.output_text.delete(1.0, tk.END)
        self.ui.command_var.set("")

        if not commands:
            self.ui.output_text.insert(tk.END, "请至少配置一个命令\n")
            return

        # 显示命令
        pipeline = self.executor._build_pipeline(commands, input_file)
        self.ui.command_var.set(pipeline)

        # 显示执行信息
        self.ui.output_text.insert(tk.END, "生成的命令:\n")
        self.ui.output_text.insert(tk.END, "-" * 50 + "\n")
        self.ui.output_text.insert(tk.END, pipeline + "\n\n")

        # 检查文件是否存在
        if input_file and not os.path.exists(input_file):
            self.ui.output_text.insert(tk.END, f"警告: 文件 '{input_file}' 不存在\n")
            self.ui.output_text.insert(tk.END, "将只显示命令，不执行\n")
            return

        # 在新线程中执行命令
        self.ui.output_text.insert(tk.END, "执行结果:\n")
        self.ui.output_text.insert(tk.END, "-" * 50 + "\n")

        threading.Thread(
            target=self._run_commands_thread,
            args=(commands, input_file),
            daemon=True
        ).start()

    def _run_commands_thread(self, commands, input_file):
        """在后台线程中运行命令"""
        stdout, stderr, returncode = self.executor.execute(
            commands, input_file, timeout=30
        )

        # 在主线程中更新UI
        def update_ui():
            if stdout:
                self.ui.output_text.insert(tk.END, stdout)
                if not stdout.endswith('\n'):
                    self.ui.output_text.insert(tk.END, '\n')

            if stderr:
                self.ui.output_text.insert(tk.END, "\n错误信息:\n")
                self.ui.output_text.insert(tk.END, "-" * 30 + "\n")
                self.ui.output_text.insert(tk.END, stderr + "\n")

            if returncode != 0:
                self.ui.output_text.insert(
                    tk.END,
                    f"\n命令返回码: {returncode}\n"
                )

            if not stdout and not stderr:
                self.ui.output_text.insert(tk.END, "(无输出)\n")

            self.ui.output_text.see(tk.END)

        self.root.after(0, update_ui)

def main():
    """主函数"""
    root = tkb.Window()
    app = Main(root)
    print(tkfont.families())
    root.mainloop()

if __name__ == "__main__":
    main()