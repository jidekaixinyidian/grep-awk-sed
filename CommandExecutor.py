import platform
import subprocess
from datetime import datetime
import os

from PlatformMode import PlatformMode

class CommandExecutor:

    def __init__(self, platform_mode=PlatformMode.AUTO):
        self.platform_mode = platform_mode
        self._detect_platform()

    def _detect_platform(self):
        if self.platform_mode == PlatformMode.AUTO:
            self.current_platform = platform.system().lower()
        else:
            self.current_platform = self.platform_mode.value

    # HOTFIX: 获取cat命令 如果没有这个 在Windows上会报错
    def get_cat_command(self):
        return "type" if "windows" in self.current_platform else "cat"

    def execute(self, commands, input_file=None, timeout=30):
        if not commands:
            return None, None, "没有命令需要执行"

        full_command = self._build_pipeline(commands, input_file)

        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout
            ) # 感谢某神秘Subprocess命令生成器
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return None, "命令执行超时", -1
        except Exception as e:
            return None, str(e), -1

    def _build_pipeline(self, commands, input_file):
        if not commands:
            return ""

        cat_cmd = self.get_cat_command()

        if input_file and os.path.exists(input_file):
            if len(commands) == 1:
                # 单个命令 直接接文件名
                if any(cmd.startswith(('grep', 'sed')) for cmd in commands):
                    return commands[0]
                else:
                    return f"{cat_cmd} \"{input_file}\" | {commands[0]}"
            else:
                # 多个命令管道连接
                return f"{cat_cmd} \"{input_file}\" | " + " | ".join(commands)
        elif input_file:
            return f"# 文件不存在: {input_file}"
        else:
            # HOTFIX: 无文件名输入时 直接输出命令内容
            return " | ".join(commands) if len(commands) > 1 else commands[0]

    def save_to_file(self, commands, input_file, output_file):
        pipeline = self._build_pipeline(commands, input_file)

        # HOTFIX: Linux需要添加"#!/bin/bash"调用Shell
        if "linux" in self.current_platform and output_file.endswith('.sh'):
            content = "#!/bin/bash\n\n"
            content += f"# 生成时间: {datetime.now()}\n"
            content += f"# 输入文件: {input_file}\n\n"
            content += pipeline + "\n"
        else:
            content = f"# 命令生成时间: {datetime.now()}\n"
            content += f"# 输入文件: {input_file}\n\n"
            content += pipeline + "\n"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

            # HOTFIX: Linux脚本需要添加执行权限
            if "linux" in self.current_platform and output_file.endswith('.sh'):
                os.chmod(output_file, 0o755)

            return True, output_file
        except Exception as e:
            return False, str(e)