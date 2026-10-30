# 同家族纸木面板提示词

使用内置 `image_gen` 单次生成。输入 `merchant-and-goods-source.png` 仅作为颜色与像素簇的风格参考，不作为角色或商品复制目标。`transparent_background: false`，生成后保留原始 RGB PNG，未裁切、重绘、重采样或量化。下方为完整实际提示词；实际边缘测量与偏离见 `panel-provenance.json`。

```text
Use case: stylized-concept
Asset type: ONE original raster nine-slice UI panel for the same rural seed-shop pixel game.
Input image: merchant-and-goods-source.png is a STYLE AND COLOR REFERENCE ONLY. Match its warm cream paper, dark colored outline, restrained brown family and clear stepped square pixel clusters. Do NOT copy or include the woman, any goods, vegetable emblems, objects, silhouettes, shadows, or layout from the reference.

Primary request: one complete flat FRONT-FACING rectangular warm-cream paper panel filling the whole canvas, landscape 3:2, ideally 1536 x 1024. No scene and no exterior padding. Opaque RGB-style background is acceptable; no transparency is required.

Frame: an extremely narrow humble brown wood border around all four edges, with a dark brown outer contour and only TWO clearly separated brown wood shades. Keep it flat and matte, without modeled bevels. Aim for roughly 16 source pixels total border thickness at 1536px canvas width. Corners use just one tiny rectangular stair-step/chamfer; otherwise square joins, with no ornament. The border must be continuous and completely visible, never cropped. This source will be displayed as a 4-logical-pixel-wide nine-slice border, so the frame must stay modest, simple and clean.

Center: almost the entire image is one uniform quiet warm-cream paper color. Use the reference's cream family, approximately #f5e7bb or #fff4d2. NO paper fibers, marks, mottling, stains, folds, lighting gradients, shadows, noise, writing, decoration or internal divisions. This central area is an empty readable interface surface, not an illustration.

Shared palette direction: dark outline around #2e3b32 / #1e2b28; subdued warm brown border around #6e4731 / #996441; warm cream center #f5e7bb / #fff4d2. Flat discrete color steps, clear square pixel rhythm, no soft edges.
Avoid: text, letters, numbers, lines inside the center, grid, rules, icons, buttons, badges, handles, nails, gems, gold, metal, shiny bevels, carved corners, botanical motifs, props, shop background, perspective, 3D depth, cast shadows, gradients, antialiasing, blur, realistic texture, dither, or any item copied from the reference. Generate a new original panel only.
```
