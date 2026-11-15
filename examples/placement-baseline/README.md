# 摆放与动线叠加层示例

这些文件只用来演示如何从已填写的布局合同和场景计划生成审查叠加层，**不是游戏成品素材**，也不能当作某套布局已经通过的证据。

- [example-art-bible.json](example-art-bible.json)：一个已填好的布局合同（格宽 16，主路 3 格，住宅门前净空 3×3 格，建筑距水 2 格并写明埠头例外）。
- [example-scene-plan.json](example-scene-plan.json)：一场门院示例计划（类型要素为门洞与围墙，主路从南路经门洞到达院中地标）。`joints` 只列出要人核对的墙与门柱，叠加层不画、不量、不打分。
- `placement-overlay.png`：对应 480×270 的透明叠加层。橙条是等宽道路走廊，绿框是门前净空，紫记号是站位占地，红菱形是地标，蓝框是已定位的类型要素。
- `placement-overlay-preview.png`：同一张叠加层铺在深色底上，便于在文档里查看。
- `pass-vs-fail-demo.png`：教学对照。左：等宽主路、门前净空、墙上门洞（合格形态）；右：道路中途收窄、门开进水里、有墙无门洞（不合格）。图内标注为英文，便于在未安装中文字体的环境里出图。

生成：

```bash
python3 scripts/placement_baseline.py --bible examples/placement-baseline/example-art-bible.json --plan examples/placement-baseline/example-scene-plan.json --out examples/placement-baseline/placement-overlay.png
python3 scripts/placement_baseline.py --bible examples/placement-baseline/example-art-bible.json --plan examples/placement-baseline/example-scene-plan.json --under /path/to/scene.png --out /tmp/placement-baseline-on-scene.png
python3 scripts/placement_baseline.py --bible examples/placement-baseline/example-art-bible.json --plan examples/placement-baseline/example-scene-plan.json --prompt
python3 scripts/placement_baseline.py --demo --out examples/placement-baseline/pass-vs-fail-demo.png
```

`--under` 把透明叠加层叠到一张已有原图或合成稿上，只接受同尺寸，或一边正好是另一边的整数倍（最近邻，不拉伸）。对不上就不写文件。比画布小的单件要先铺进同尺寸画布，脚本不会自动摆放。`--prompt` 按合同和场景计划打出可粘贴的摆放条款，空字段略过，不判定布局通过。已填写的接头只列出名称和两端构件，不表示接缝已经通过。本目录的图不证明任何项目已经验收。
