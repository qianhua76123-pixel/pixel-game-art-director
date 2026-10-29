# 安装与使用

本包包含完整的本地图文知识库、风格配方、检索脚本和技术检查器，无需连接原素材盘或远端知识服务。

## Codex

将整个 `pixel-game-art-director` 文件夹放到 Codex 的 `skills` 目录，保留 `SKILL.md`、`scripts/`、`references/`、`assets/` 和 `library/` 的相对位置。例如可安装于 `~/.codex/skills/pixel-game-art-director`。新会话可用 `$pixel-game-art-director` 显式调用；若当前客户端尚未刷新技能目录，开启新会话后使用。

其他 agent 可读取 `SKILL.md` 并运行脚本；不支持skill自动发现的系统也可直接使用这些文件。不要只复制 `SKILL.md`，否则图片和索引将缺失。

## 典型请求

- “用 $pixel-game-art-director 为乡村俯视游戏检索农舍、树木与水岸教程，建立统一美术规范并制作素材。”
- “用 $pixel-game-art-director 设计暗黑背包UI，支持长中文名称与手柄焦点。”
- “用 $pixel-game-art-director 检查这批素材的尺寸、调色板和透明边缘，再查看光源、视角与材质一致性。”

## 命令行

从解压后的skill目录运行：

```bash
python3 scripts/search.py --list styles --json
python3 scripts/search.py --list ui-styles --json
python3 scripts/search.py --task '俯视农舍和树木' --limit 6 --json
python3 scripts/task_bundle.py --task '暗黑背包UI与九宫格' --style dark-gothic --ui-style dark-stone --out /tmp/dungeon-ui-brief --copy-figures
python3 scripts/init_art_bible.py --style cozy-rural --ui-style wood-paper --out /tmp/village-art-bible
```

检索、资料包和规范草案脚本只用Python标准库。检查图片需要Pillow，依赖列在 `requirements.txt`。草案初始化器默认不把建议色板和未知尺寸写成强制机器规则；按项目填写审查合同后再运行 `audit_assets.py`。无需生成服务即可检索或检查，实际图片生成使用调用agent所在环境可用的工具。

[技术检查输出示例](examples/audit-demo/EXAMPLE.md) 使用明确标记的测试夹具。[完整教程目录](library/CATALOG.md) 保留作者、来源和许可；风格配方是整理者可调建议，引用图只讲解特定技法，不冒充该风格的完整成品图。
