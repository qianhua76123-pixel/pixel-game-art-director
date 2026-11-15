# 视角基准线示例

这些文件只用来演示如何从已填写的投影合同生成审查叠加层，**不是游戏成品素材**，也不能当作某套画风已经通过的证据。

- [example-art-bible.json](example-art-bible.json)：一个已填好的正交正面俯视合同（无消失点，竖线垂直，地面边平行等距）。
- `orthographic-front-top.png`：对应 480×270 的透明叠加层。
- `orthographic-front-top-preview.png`：同一张叠加层铺在深色底上，便于在文档里查看。
- `ortho-vs-taper-demo.png`：教学对照。左：正交网格下道路左右边平行（合格形态）；右：同一套格子上道路向上收窄（不合格）。图内标注为英文，便于在未安装中文字体的环境里出图。

生成：

```bash
python3 scripts/camera_baseline.py --bible examples/camera-baseline/example-art-bible.json --out examples/camera-baseline/orthographic-front-top.png
python3 scripts/camera_baseline.py --bible examples/camera-baseline/example-art-bible.json --under /path/to/scene.png --out /tmp/camera-baseline-on-scene.png
python3 scripts/camera_baseline.py --bible examples/camera-baseline/example-art-bible.json --prompt
python3 scripts/camera_baseline.py --demo --out examples/camera-baseline/ortho-vs-taper-demo.png
```

`--under` 把透明基准线叠到一张已有原图或合成稿上，只接受同尺寸，或一边正好是另一边的整数倍（最近邻，不拉伸）。对不上就不写文件。比画布小的单件要先铺进同尺寸画布，脚本不会自动摆放。`--prompt` 按合同打出可粘贴的机位条款，空字段略过，不判定透视通过。本目录的图不证明任何项目已经验收。
