# 青禾种子铺 v3：春日柜台

v1.5.0 将人物、商品与 UI 一起重做。店主以半身姿态靠在柜台后，脸、双手和种子包有共同的场景关系；六件商品重做包装与轮廓，右侧用一张纸木账板容纳选货、说明和结算。v1.4.0 的 v2 视觉稿已被用户否定，保留为历史。**本版供看图审核，用户尚未接受视觉效果。**

![当前柜台画面](screenshots/v3-counter.jpg)

[并排对照板](../../review/shop-benchmark/index.html) 使用 Moonlighter 商人服务与 Stardew Valley 买种菜单的官方远程截图。参考用于比较人物、商品、文字和框体的关系，没有被提取为项目素材或用于本轮生成。

## 运行与操作

在仓库根目录执行：

```bash
python3 scripts/preview_shop.py
```

打开 <http://127.0.0.1:8775/>。当前入口 [index.html](index.html) 加载 [shop-v3.css](shop-v3.css) 与 [shop-v3.mjs](shop-v3.mjs)，也可直接访问 [shop-v3.html](shop-v3.html)。ES modules 需要 HTTP；两张当前图与字体均从本地加载，对照板的商业参考图需要联网。

- 点击六件商品，或用方向键、`Home`／`End` 选择；数量可输入 1–99 整数，或用加减按钮调整。
- 商品格显示名称、价格和当前余量，售罄仍保留价格。选中货品的完整名称、已有量和种植／使用条件紧邻结算。
- 条件采用不改变机制的简短表述，完整原文保留在该行悬停提示。季节说明不会额外禁止本例购买。
- 数量、计算式和唯一购买按钮同处账板底部。原 `quote()`／`purchase()` 负责购买；每份商品占一格，行囊容量 24 是演示规则。
- 成功更新余额、库存、持有量和行囊，并保留店主的成交反馈。缺款、满包、售罄或非法数量时不扣款。
- `Esc` 收起商店并回到入口，`E` 重新打开。“对照与演示”中可切换审核状态和恢复初始数据。

刷新重置内存数据。小样没有游戏存档、漫游、种植或出售系统；数据范围见 [原数据合同](data-contract.json)。

## 本轮制作

[美术方向](art-direction-v3.md) 说明构图和素材取舍。当前只使用两张新源图：

| 当前源图 | 用途 |
|---|---|
| [shop-scene.png](assets/v3/shop-scene.png) | 半身店主、柜台、环境、空白纸框合为一张场景；不烘焙商品价格与操作文字 |
| [goods-source.png](assets/v3/goods-source.png) | 六商品图集；[atlas.json](assets/v3/atlas.json) 只记录主体范围，源 PNG 保持原样 |

来源与全部提示词见 [provenance.json](assets/v3/provenance.json)、[prompts.md](assets/v3/prompts.md)。四次成功的内置 `image_gen` 调用包含初始场景、构图修改、商品图集、像素简化修改；当前分发的最终图像为上表两张。商品图集使用本项目原创场景作配色和画法参考，商业截图未作为生成输入。

运行时将整合场景取样到 640×360 逻辑舞台；商品分别复制到 42×42 逻辑画布，关闭图像平滑。Canvas 只搬运光栅素材，未用代码绘画店主、商品或环境。动态中文、数量、库存和按钮由 DOM 层负责。主中文为 12 逻辑像素 Fusion Pixel，1280×720 显示时为 24 屏幕像素。

640px 以下保留原尺寸并提供横向查看与横屏提示，尚未完成独立的竖屏布局。源图的严格原生网格、硬 alpha 和生产导出未获认证；运行显示约定不能替代最终画面的判断，也不能把本小样称为生产级像素素材包。

## 看图与历史

- [正常选货](screenshots/v3-counter.jpg)、[成交反馈](screenshots/v3-receipt.jpg)、[售罄状态](screenshots/v3-sold-out.jpg) 用于看当前实际画面；单张截图不证明全部操作。
- 本版实际走查见 [v1.5 审阅记录](../../validation/SHOP-REDESIGN-V1.5.md)。交易测试或结构记录不会自动产生视觉通过结论。
- [shop-v2.html](shop-v2.html)、v2 CSS／JS、三张 v2 源图和 [v1.4 记录](../../validation/SHOP-BENCHMARK-V1.4.md) 作为用户已否定的历史视觉稿保留。
- 旧 A/B/C 页面代码、五张旧图及 [v1.3.1](../../validation/UI-REVISION-V1.3.1.md)、[v1.3](../../validation/SHOP-COHESION-V1.3.md) 记录继续保留。新图不为旧版作验收证据。

仓库共保留十张 AI 源 PNG，当前使用两张；字体及上游声明保持 SIL OFL 1.1。AI 图仅在项目实际持有权利的范围内按根 MIT 提供，不保证独占性或独立版权保护。商业参考图仍归原权利人，详见 [第三方声明](../../THIRD_PARTY_NOTICES.md)。
