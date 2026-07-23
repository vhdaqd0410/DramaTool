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
适用于：

抖音短剧

快手短剧

番茄短剧

红果短剧

海外短剧

MCN工作室

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

计划新增

 拖拽导入

 EXE 单文件发布

 OCR字幕识别

 Premiere Pro 插件

 DaVinci Resolve 插件

 XML 时间线工具

 批量改帧率

 批量改视频速度

 AI 自动整理素材

 AI 剧本分析

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
❤️ 为什么开发这个工具？
作为短剧剪辑师，每天需要处理几十甚至上百集素材。

传统方式需要：

手动查看集数

手动修改文件名

手动对应字幕

手动检查遗漏

不仅效率低，而且容易出错。

DramaTool 的目标就是：

把重复劳动交给程序，把时间留给创作。

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

我建议再升级一下项目定位
你这个项目现在已经不仅仅是一个「重命名工具」了，根据我们前面规划的路线（Checker V2、PR、AI 等），README 可以直接定位成一个完整的短剧工作流工具，例如：

DramaTool —— 一站式短剧后期工具箱

未来可包含：

🎬 智能素材整理

📝 AI 字幕处理

✂️ 拆集合并

🔤 批量重命名

🎨 DaVinci / Premiere 工作流

🤖 AI 辅助剪辑

📦 XML / EDL 工具

🚀 EXE 开箱即用
