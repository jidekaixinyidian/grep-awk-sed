# grep-awk-sed

### 快速生成三件套语句的小工具

### V1.0 by [jidekaixinyidian @ github.com](https://github.com/jidekaixinyidian/)

### V1.1 by [Liziyu352 @ github.com](https://github.com/Liziyu352/)


## 脚本输出工具

#### 一个桌面 GUI 应用程序, 用于快速编写和执行 sed、awk、grep 命令。

## 功能特性

- **直观的图形界面**: 简洁的三栏布局, 分别对应 ```grep```, ```awk``` 和 ```sed``` 命令
- **预设参数选项**: 每个命令都提供常用参数的下拉选择
- **灵活的输入**: 支持自定义命令参数和模式
- **文件浏览**: 内置文件选择器, 方便选择输入文件
- **实时输出**: 命令执行结果实时显示在输出区域
- **管道支持**: 支持多个命令的管道组合执行
- **跨平台**: 基于 Python + Tkinter, 包含操作系统选择(V1.1加入), 支持 Windows、macOS 和 Linux

## 界面布局

<table><thead>
  <tr>
    <th colspan="3">脚本生成工具</th>
  </tr></thead>
<tbody>
  <tr>
    <td>平台模式:(默认auto)</td>
    <td colspan="2">检测到:(当前系统) 使用xx命令</td>
  </tr>
  <tr>
    <td rowspan="4">grep命令<br>参数选项:(默认无)<br>搜索内容:<br>示例:INFO</td>
    <td rowspan="4">awk命令<br>操作类型:(默认无)<br>参数/脚本:<br>示例:1</td>
    <td rowspan="4">sed命令<br>操作类型:(默认无)<br>参数/命令:<br>示例:old/new</td>
  </tr>
  <tr>
  </tr>
  <tr>
  </tr>
  <tr>
  </tr>
  <tr>
    <td colspan="2">输入文件:(默认sample_data.txt)</td>
    <td>浏览</td>
  </tr>
  <tr>
    <td>执行命令</td>
    <td>保存命令</td>
    <td>复制命令</td>
  </tr>
  <tr>
    <td colspan="3">输出结果:</td>
  </tr>
  <tr>
    <td>生成的命令:</td>
    <td colspan="2"></td>
  </tr>
  <tr>
    <td colspan="3">(此处为执行结果)</td>
  </tr>
</tbody>
</table>
<!-- 感谢列表生成器 -->

## 使用方法

### 1. 运行程序

```bash
python main.py
```

### 2. 配置命令

#### grep 区域:

- **参数选择**: 选择常用的 grep 参数（如 -i 忽略大小写、-n 显示行号等）
- **模式输入**: 输入要搜索的模式或正则表达式

#### awk 区域:

- **模式选择**: 选择预设的 awk 操作模式
- **脚本输入**: 输入自定义的 awk 脚本或参数

#### sed 区域:

- **操作选择**: 选择常用的 sed 操作（替换、删除、插入等）
- **命令输入**: 输入具体的 sed 命令参数

### 3. 选择输入文件

点击"浏览"按钮选择要处理的文本文件, 或直接在输入框中输入文件路径。

### 4. 执行/保存/复制命令

若点击"执行"按钮, 命令输出将显示在下方文本框

## 预设选项说明

### grep 参数选项

- `-i`: 忽略大小写
- `-v`: 反向匹配（显示不匹配的行）
- `-n`: 显示行号
- `-r`: 递归搜索目录
- `-l`: 只显示匹配的文件名
- `-c`: 显示匹配行数
- `-F`: 固定字符串匹配
- `-E`: 扩展正则表达式

### awk 模式选项

- `{print $1}`: 打印第一列
- `{print $NF}`: 打印最后一列
- `{print NR, $0}`: 打印行号和内容
- `{sum+=$1} END {print sum}`: 计算第一列总和
- `-F:`: 使用冒号作为字段分隔符

### sed 操作选项

- `s/old/new/`: 替换第一个匹配
- `s/old/new/g`: 替换所有匹配
- `/pattern/d`: 删除匹配行
- `/pattern/p`: 打印匹配行
- `/^$/d`: 删除空行

## 系统要求

- Python 3.6 或更高版本
- tkinter（通常随 Python 一起安装）
- 支持 sed、awk、grep 命令的操作系统（Linux、macOS、Windows with WSL/Git Bash）

## 提醒事项

1. **Windows 用户**: 需要安装 Git Bash、WSL 或 Cygwin 来支持 sed、awk、grep 命令
2. **文件路径**: 包含空格的文件路径会自动加引号处理
3. **命令组合**: 可以同时配置多个命令, 程序会自动用管道连接
4. **错误处理**: 命令执行错误会在输出区域显示错误信息

## 扩展功能

程序支持以下高级功能：

- **管道组合**: 多个命令自动组合成管道执行
- **异步执行**: 命令在台线程执行, 不会冻结界面
- **错误显示**: 详细的错误信息和返回码显示