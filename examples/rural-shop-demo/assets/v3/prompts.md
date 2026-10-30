# 本轮完整提示词

内置 image_gen；以下四次成功导出组成原创引用链。商业游戏截图只用于人工比较，没有作为生成输入。源 PNG 保留原样；图集坐标是只读边界测量。

## scene_initial

```text
Use case: ui-mockup.
Create the original full-screen background artwork for a beautifully art-directed southern Chinese village seed shop game interface. Landscape EXACT 16:9 composition, preferred output 1280x720. This is the complete cohesive original art layer for a working pixel RPG shop, not a web dashboard, no text anywhere. Expert deliberate low-resolution pixel art, imagined native 640x360 doubled 2x: clearly visible square pixel clusters, economical strong silhouettes, flat stepped shading, beautiful restrained warm ochre, burnt sienna, deep plum-brown shadows, cream, sage and jade greens. 2-4 well-chosen shades per material. Sharp clean pixel contours and large intentional clusters, avoid fuzzy stippling, dithering, micro grain, photographic or painterly detail.

Composition coordinates given in logical 640x360, proportionally match precisely:
LEFT 235px: an intimate welcoming shop counter scene, strong lovely character silhouette and readable face. A friendly middle-aged Chinese woman shopkeeper with a black hair bun, warm rosy round face, dark sage apron over ivory sleeves and russet blouse, waist-up, leaning comfortably toward viewer over a wooden counter. Her head occupies x72..153 y78..147, hair and face large and expressive, one hand presenting a small kraft seed envelope bearing a simple painted green leaf (no letters), other hand resting on counter. Shoulders and elbows x32..216 y146..254. Counter top at y246..274, naturally occludes her waist; never a detached floating sticker. Pared-down carefully shaped face, hands, large fabric folds, all same crisp pixel language. Behind her: quiet dark wooden shelves with organized ceramics, a few burlap sacks, hanging garlic, a small muted red knot; upper left warm window light. Foreground left corners: woven basket of cabbages, sealed rice sack, clay pot. Crafted readable clusters, not busy scattered clutter. Character is the focus of this side. Scene continues subtly behind UI right; no oversized irrelevant decorations.

RIGHT 378px: one beautiful EMPTY PARCHMENT SHOP BOARD occupying exactly x240..621, y24..330. This blank uninterrupted parchment is the UI surface for runtime text and icons. Thin layered dark chestnut and terracotta pixel wood rim about 4 logical pixels thick, square stepped corners, a subtle small cut or notch in paper corners. Warm pale cream inside, quiet and uniform, no texture noise. A narrow sage cloth bookmark with plain leaf motif peeks from TOP EDGE around x280; only a tiny identity accent, no ornate fantasy metal/gems. Interior usable x250..611 y35..319 MUST be completely EMPTY, flat quiet parchment: no words, no numbers, no rows, no slots, no goods, no plants, no lines, no buttons. Do not draw any UI content inside; code will place real Chinese text, goods and controls there later. No artificial blank white rectangle, make board feel physically crafted within this same pixel world.
LEFT BOTTOM: small blank cream paper conversational strip at x22..219 y300..344, restrained stepped thin dark brown outline, empty inside. It belongs to character, no text.
BOTTOM RIGHT under main board y337..355 leave dark quiet wood background to display one line of interface guidance later.

Overall quality: a charming premium indie farming RPG screenshot art layer, nuanced designed shapes, tasteful controlled saturation, painter's composition expressed in crisp pixel blocks. Beautiful face and fingers and contact/occlusion, iconic cabbage leaves and ceramics. All art and frame edges use the same pixel cadence. No UI typography, no fake glyphs, no logo, no watermark. Do NOT copy a named game's assets.
```

## scene_composition

```text
Use case: precise-object-edit. This is an ORIGINAL pixel game background artwork. Keep the lovely shopkeeper identity, welcoming eyes and smile, dark hair bun, sage apron, clothing palette, seed envelope gesture, wooden counter contact, cabbage basket and window. Keep landscape 16:9. Correct the composition so the EMPTY SHOP BOARD occupies the RIGHT SIXTY PERCENT of the image. Its left border must start at 37% of image width; right border at 97%. Top 7%, bottom 92%. Current board is too narrow, starting around48%; enlarge it LEFTWARD substantially. Recompose the merchant and shop scene to the LEFT THIRD; keep her face large and clear, seated/leaning behind counter with a naturally resting hand. Do not simply overlay board over her arm. Her face centered at x20% y35%, shoulders within x5..34%; the counter occludes her waist naturally. Small blank merchant speech strip at x3..34%, y84..96%. Main board usable paper interior x39..95% y10..88% remains entirely EMPTY; reduce the green bookmark to a small leaf tab pinned on its TOP LEFT corner, no long downward overhang into the writing surface. Background detail quietly supports character. Hand-crafted thin wood rim and cream paper same original. Increase deliberate visible PIXEL CLUSTERS and flat stepped shading; simplify face shading and apron into stronger clean shapes while retaining attractive expression and volume. Preserve crisp edges, avoid dusty noisy speckles/micrograin. No text, glyphs, numbers, rows, slots, goods, labels or buttons inside blank main paper; these will be real live UI. This is a single targeted layout/pixel simplification refinement, not a new style.
```

## goods

```text
Use case: stylized-concept. Create ONE original professional pixel RPG inventory sprite sheet, 3 equal columns by 2 equal rows, on genuine transparent background. Preferred image 1536x1024 (square cells512x512), six separate sprites centered in their cell, no overlap, ample clear gutters. The attached original shop image is ONLY the shared material, color and pixel art direction reference. Match warm parchment, russet, sage/leaf green and deep brown cluster shading, charming southern-Chinese village shop. These are intended to be displayed only 36x36 logical pixels each, so think expertly hand-pixeled 36px inventory icons enlarged to512px: LARGE simple deliberate pixel clusters, bold one-pixel dark colored silhouette contour and 2-3 flat stepped shade clusters per material, NO fine grain, no photographic light, no soft gradients or tiny decorative hatchmarks, no fuzzy edges or glow, no black shadow disks.

ROW1 left: a kraft paper SEED ENVELOPE, warm cream face, folded sealed top, simple very clear GREEN BOK CHOY pictogram painted on front (3 big green leaves, pale stem), small sage square seal. 
ROW1 middle: same family kraft SEED ENVELOPE, with clear WHITE DAIKON RADISH pictogram, white tapering root and green leafy top. 
ROW1 right: squat open BURLAP RICE-SEED SACK with rolled rim, a mound of golden rice grains expressed as few clean clusters, two short rice stalks; brown cloth, cream leaf patch.
ROW2 left: same kraft SEED ENVELOPE with bold pair of RED CHILI PEPPERS painted on front, green stem.
ROW2 middle: BLUEBERRY SEEDLING in small terracotta clay pot, compact green foliage and 3 large readable indigo-blue round berries, same upper-left light. Not a big tree.
ROW2 right: plump tied BROWN COMPOST SACK with sage green rectangular leaf patch on front, folded cloth creases as 2 clean shade shapes.

All six same size of visual mass, 3/4 very shallow top-front view, aligned resting bottom and consistent upper-left light. Beautiful compact iconic silhouette and convincing material through economical pixel planes. Keep sprite around60-70% cell height and60-70%cellwidth, SAME object scale across envelopes/sacks/pot. Transparent surrounding background, no UI panels, no gridlines, no letters/numbers, no labels, no background scenes. These are actual game inventory assets, not a high-resolution illustration masquerading as pixels.
```

## scene_pixel_refinement

```text
Use case: precise-object-edit. Refine this ORIGINAL finished shop art layer while keeping its EXACT composition, all empty paper board edges and positions, bookmark position, left dialogue paper positions, seed shop props and merchant hand/counter contact unchanged. Keep entire right board EMPTY and undisturbed. Landscape16:9.

Change only the artwork rendering into true DELIBERATE COARSE PIXEL ART and mature the merchant. The current face looks like a smooth young anime illustration with a pixel filter. Make her a warm Chinese shop aunt in her early forties: slightly fuller adult cheek/jaw proportions, modest smaller eyes, gentle smile creases, a few grey hair strokes at temples, practical pinned bun. Still pretty, kind and welcoming, same wardrobe and seed-envelope gesture, NOT an elderly caricature. Face should be hand-built from LARGE square clusters with 3 clear skin shades and one broad restrained warm cheek cluster; eyes made of only a few bold dark pixel shapes. No glossy gradient eyes, airbrushed nose highlight, tiny flecks of blush or individual hair filaments.

Apply same art discipline everywhere: imagined 320x180 native pixel image nearest-neighbor enlarged to output. Each visible square block is about5-6 OUTPUT pixels, large deliberate contiguous shapes, no1px output noise. Pixelated diagonal steps consistent across apron, hands, leaf symbol, cabbages, ceramics, wood rim. Fabric uses few large readable folds and2-3tones, cabbage leaves use bold distinct flatshapes. Light retains warm window mood through discrete value blocks. Eliminate smooth gradations and dither/fine grain, simplify noisy shelf/wood texture. Preserve pleasing original composition and volumes while making actual pixel illustration rather than noisy highres anime. Right paper remains pale cream and completely empty; frame remains same exact silhouette and placement. No text or invented glyphs.
```
