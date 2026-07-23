# DramaTool
🎬 DramaTool
一款专为 短剧后期剪辑 打造的素材整理工具。

DramaTool 用于解决短剧制作过程中素材命名混乱、拆集后无法对应、字幕不同步等问题，实现一键整理、一键重命名，大幅提高剪辑效率。

✨ 功能特点
✅ 自动识别原始剧集

✅ 自动匹配拆集文件

✅ 视频批量重命名

✅ 字幕同步重命名

✅ 支持拖拽文件夹

✅ 支持递归扫描子目录

✅ 自动跳过异常文件

✅ 支持大批量素材（1000+文件）

📷 使用场景

例如：


原始素材

01.mp4
02.mp4
03.mp4
...
拆集后


001-1.mp4
001-2.mp4
001-3.mp4
...
DramaTool 会自动匹配对应关系，并批量完成命名。

🚀 功能规划
目前已完成

 批量重命名

 字幕同步

 文件扫描

 日志输出

 GUI 图形界面
 
 拖拽导入

 EXE 单文件发布

📦 下载
前往 Releases 下载最新版：

👉 Releases

（发布后 GitHub 会自动显示下载页面）

🖥️ 运行环境
Windows 10 / 11

Python 3.10+

安装依赖

Bash

pip install -r requirements.txt
运行

Bash

python main.py
打包

Bash

pyinstaller -F -w main.py
📁 项目结构

DramaTool
│
├── main.py
├── checker.py
├── renamer.py
├── utils.py
├── requirements.txt
├── assets/
├── icons/
└── README.md

🤝 欢迎贡献
欢迎提交：

Issue

Pull Request

Bug反馈

功能建议

如果这个项目对你有帮助，欢迎点一个 ⭐ Star 支持一下！

📄 License
MIT License

⭐ Star History
如果觉得项目不错，欢迎点一个 Star，这是持续更新最大的动力！


