# 重建索引与更新资料

日常阅读无需安装依赖。离线搜索只使用Python标准库。转换、图片验证与切块需要 [requirements.txt](requirements.txt) 中列出的依赖。

## 安装工具环境

建议将虚拟环境放在系统盘，资料继续放在当前目录。部分外置卷会生成AppleDouble文件，放置Python环境可能导致`.pth`读取问题。

```bash
python3 -m venv /tmp/pixel-tutorial-library-venv
/tmp/pixel-tutorial-library-venv/bin/python -m pip install -r requirements.txt
```

## 不联网重建

在教程库根目录运行：

```bash
/tmp/pixel-tutorial-library-venv/bin/python tools/build_catalog.py
/tmp/pixel-tutorial-library-venv/bin/python tools/build_chunks.py
/tmp/pixel-tutorial-library-venv/bin/python tools/validate_library.py
python3 tools/search.py '俯视 行走' --json --top 5
```

主文档在`tutorials/`，原图与派生关键帧在`assets/`，分组清单在`manifests/`。不要编辑`catalog.json`或`chunks.jsonl`来改教程；它们由主文档和清单重建。

## 重新采集

`tools/collect_*.py` 是本次使用的采集/生成脚本。先检查脚本内的来源、版本、目标目录与缓存逻辑，再运行。下载过程可能覆盖对应分组的生成稿，手动修改前应备份。脚本不应被当作持续爬取全站的任务。

Saint11固定仓库提交；Godot固定4.5文档。Krita页面上记录了本次所见的手册版本和每页源信息。若刷新到新版，重新核对中文菜单说明、版本变更和授权，再更新采集日期；不能仅把日期改成今天而保留旧内容。

每次重新整理后，重新生成索引、检查来源链接和图片、打开代表性MD实看。人工图文解读仍需审阅，结构验证不能代替视觉和技术核对。
