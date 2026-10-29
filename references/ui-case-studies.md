# 游戏 UI 案例：14 款游戏、28 个参考画面

每例区分静态可见事实、原创设计判断与未验证项。图像通过原始 URL 加载，需联网；商业图像不随公开 skill 打包，不授予素材再利用许可。

## 索引

| ID | 游戏 | 观察任务 |
|---|---|---|
| UI-CASE-001 | Stardew Valley | 木框对话：同一组件融入明亮节庆与室内场景 |
| UI-CASE-002 | Eastward | 场景对白与轻量战斗HUD：让世界保持主角 |
| UI-CASE-003 | Moonlighter | 书页背包与药水商店：同一材质服务不同信息任务 |
| UI-CASE-004 | Into the Breach | 战术HUD与机甲配置：让危险、动作和后果可对照 |
| UI-CASE-005 | Sea of Stars | 战斗命令与升级选择：状态与决策分别占据清楚位置 |
| UI-CASE-006 | Backpack Hero | 空间背包与出售面板：界面直接承载核心决策 |
| UI-CASE-007 | Papers, Please | 证件桌面：让比对对象、操作工具和决定位置建立映射 |
| UI-CASE-008 | Return of the Obra Dinn | 双色调查工具：把场景线索与人物记录分成不同阅读任务 |
| UI-CASE-009 | Loop Hero | 磨损像素面板：把建筑依赖、资源条件和卡组约束分层 |
| UI-CASE-010 | Caves of Qud | 终端感菜单：用身体映射、分类清单和任务地图组织大量内容 |
| UI-CASE-011 | Factorio | 工业管理：地图抽象与物品/配方分工（含历史设计稿） |
| UI-CASE-012 | FTL: Faster Than Light | 舰船管理：锁定原因、升级层级与提交动作的可见表达 |
| UI-CASE-013 | Inscryption | 桌面卡牌与纸面路线：空间化界面的气氛收益与阅读代价 |
| UI-CASE-014 | Dead Space (2023) | 官方设置页：主题面板也必须说明选项含义和条件关系 |

## UI-CASE-001 · Stardew Valley

木框对话：同一组件融入明亮节庆与室内场景

作者/项目：ConcernedApe。[官方来源](https://store.steampowered.com/app/413150/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：材质暗示：木框、暖色正文区、像素文字。
- 世界关系：屏幕叠加；木框本身不能证明是世界中存在的物件。
- 系统关联：dialogue-choice
- 迁移范围：参考任务组织、材质与像素层级；需按项目重新绘制资产和验证中文/输入。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![明亮节庆场景中的木框对白与右侧人物肖像。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/413150/ss_10628b4a811c0a925a1433d4323f78c7017dbbe4.1920x1080.jpg?t=1786554168)

明亮节庆场景中的木框对白与右侧人物肖像。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/413150/ss_10628b4a811c0a925a1433d4323f78c7017dbbe4.1920x1080.jpg?t=1786554168) · [出处](https://store.steampowered.com/app/413150/?l=english)

- 明亮节庆场景中的木框对白与右侧人物肖像。

### 官方游戏截图 2

![室内场景使用同样的木框、暖色正文底和右侧肖像布局。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/413150/ss_30aeedc47e731232ade368831a598d6545346f70.1920x1080.jpg?t=1786554168)

室内场景使用同样的木框、暖色正文底和右侧肖像布局。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/413150/ss_30aeedc47e731232ade368831a598d6545346f70.1920x1080.jpg?t=1786554168) · [出处](https://store.steampowered.com/app/413150/?l=english)

- 室内场景使用同样的木框、暖色正文底和右侧肖像布局。

### 可见事实

- 正文、头像、名字分别占固定区域；边框以棕橙色像素块建立厚度。
- 两张图的对白组件结构一致，场景色彩和人物头像则各不相同。

### 设计判断与可借鉴项

- 适合借鉴组件一致性：同一框体跨环境复用，人物身份仍突出。
- 暖色不透明正文区能隔开繁杂场景；木材质呼应乡村世界。

### 代价与未验证项

- 只观察了对白截图，没有观察背包、商店、焦点或中文排版。
- 较厚边框与大头像占用屏幕，移植到小屏需重新分配文本面积。

可供 wood-paper 的对白结构和材质关系参考；不是该配方的官方实现。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-002 · Eastward

场景对白与轻量战斗HUD：让世界保持主角

作者/项目：Pixpil / Chucklefish。[官方来源](https://store.steampowered.com/app/977880/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：轻量平面图形与像素世界并用。
- 世界关系：角色附近对白与角落HUD并存；叙事归属需项目证据。
- 系统关联：dialogue-choice, hud
- 迁移范围：参考任务组织、材质与像素层级；需按项目重新绘制资产和验证中文/输入。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![市集中的浅色对白气泡，尾部指向说话角色。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/977880/ss_ddd76431b1df70e234494c92370e2391680c98ef.1920x1080.jpg?t=1782290198)

市集中的浅色对白气泡，尾部指向说话角色。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/977880/ss_ddd76431b1df70e234494c92370e2391680c98ef.1920x1080.jpg?t=1782290198) · [出处](https://store.steampowered.com/app/977880/?l=english)

- 市集中的浅色对白气泡，尾部指向说话角色。

### 官方游戏截图 2

![战斗中生命与弹药位于左下，资源数在右上，中央区域保留给行动。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/977880/ss_d33bc97134437987ed89194d04b39f2e4658df20.1920x1080.jpg?t=1782290198)

战斗中生命与弹药位于左下，资源数在右上，中央区域保留给行动。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/977880/ss_d33bc97134437987ed89194d04b39f2e4658df20.1920x1080.jpg?t=1782290198) · [出处](https://store.steampowered.com/app/977880/?l=english)

- 战斗中生命与弹药位于左下，资源数在右上，中央区域保留给行动。

### 可见事实

- 对白以角色附近的浅色气泡呈现，角色名和正文有视觉层级。
- 战斗HUD采用细轮廓、亮色心形与数字，集中在角落。

### 设计判断与可借鉴项

- 适合借鉴低遮挡HUD：信息量克制，画面中部仍展示角色和攻击。
- 气泡位置把说话人和文字连接起来，减少视线寻找。

### 代价与未验证项

- 截图中的滤镜、细字与弱化角色名不能证明最终尺寸的可读性。
- 没有背包与菜单样本；这里只给 holo-terminal 借鉴线条和HUD组织，不把整套风格归类为全息终端。

只参考 holo-terminal 的角落HUD与细轮廓组织；对白不属于全息材质。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-003 · Moonlighter

书页背包与药水商店：同一材质服务不同信息任务

作者/项目：Digital Sun / 11 bit studios。[官方来源](https://store.steampowered.com/app/606150/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：物件式书页隐喻与清楚网格内容。
- 世界关系：书页形面板正对屏幕；不能因书形判定角色持有此书。
- 系统关联：inventory-equipment, shop-trade, crafting
- 迁移范围：参考任务组织、材质与像素层级；需按项目重新绘制资产和验证中文/输入。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![打开的书页承载背包与装备，绿色角标表示当前格子，底部显示手柄操作提示。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/606150/ss_c7c33eb041627f7a5fdbdefb0e41269178faf372.1920x1080.jpg?t=1790860598)

打开的书页承载背包与装备，绿色角标表示当前格子，底部显示手柄操作提示。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/606150/ss_c7c33eb041627f7a5fdbdefb0e41269178faf372.1920x1080.jpg?t=1790860598) · [出处](https://store.steampowered.com/app/606150/?l=english)

- 打开的书页承载背包与装备，绿色角标表示当前格子，底部显示手柄操作提示。

### 官方游戏截图 2

![药水列表与详情分栏；配方材料以数量、勾叉和颜色表示是否足够。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/606150/ss_99f46056bb1d647adf3ea8f044bf016a8a3da428.1920x1080.jpg?t=1790860598)

药水列表与详情分栏；配方材料以数量、勾叉和颜色表示是否足够。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/606150/ss_99f46056bb1d647adf3ea8f044bf016a8a3da428.1920x1080.jpg?t=1790860598) · [出处](https://store.steampowered.com/app/606150/?l=english)

- 药水列表与详情分栏；配方材料以数量、勾叉和颜色表示是否足够。

### 可见事实

- 背包使用米色书页、绿色语义线条和规则网格，装备人物在右页。
- 商店复用纸面、绿色选中角标和底部操作提示，但把列表与配方详情分开。

### 设计判断与可借鉴项

- 适合借鉴跨页面一致性：材质、色彩角色和强调角标在两个任务中延续；角标的具体输入状态未由静态图确认。
- 材料状态同时用数量、勾叉和色块表达，具有可迁移的信息冗余。

### 代价与未验证项

- 书本装饰和人物展示占较大面积，密集物品列表需控制每屏数量。
- 只看到一个选择状态；未操作手柄、测试焦点移动或中文长文案。

wood-paper 借鉴纸面与网格；ornate-fantasy 借鉴装饰分布。不要照搬书页资产。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-004 · Into the Breach

战术HUD与机甲配置：让危险、动作和后果可对照

作者/项目：Subset Games。[官方来源](https://store.steampowered.com/app/590380/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：平面信息模块、棋盘图式、少量科幻框形。
- 世界关系：世界标记与屏幕面板混合；角色感知为UNDETERMINED。
- 系统关联：hud, battle-command, inventory-equipment
- 迁移范围：参考任务组织、材质与像素层级；需按项目重新绘制资产和验证中文/输入。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![战术画面把全局资源、回合动作、任务和地块提示分在边缘，棋盘上显示箭头与顺序数字。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/590380/ss_4b985c7747c1ff0b7fbbf3eaf8ca5a1272f0dadb.1920x1080.jpg?t=1755610784)

战术画面把全局资源、回合动作、任务和地块提示分在边缘，棋盘上显示箭头与顺序数字。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/590380/ss_4b985c7747c1ff0b7fbbf3eaf8ca5a1272f0dadb.1920x1080.jpg?t=1755610784) · [出处](https://store.steampowered.com/app/590380/?l=english)

- 战术画面把全局资源、回合动作、任务和地块提示分在边缘，棋盘上显示箭头与顺序数字。

### 官方游戏截图 2

![机甲配置页以模块化区域并列显示人物、武器、升级和存储。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/590380/ss_f3ca4120fe01efcdd4cd355b7e5798f98b695233.1920x1080.jpg?t=1755610784)

机甲配置页以模块化区域并列显示人物、武器、升级和存储。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/590380/ss_f3ca4120fe01efcdd4cd355b7e5798f98b695233.1920x1080.jpg?t=1755610784) · [出处](https://store.steampowered.com/app/590380/?l=english)

- 机甲配置页以模块化区域并列显示人物、武器、升级和存储。

### 可见事实

- 深色底、细框与白字构成信息面板，黄色数字与红色区域用于棋盘提示。
- 战术画面的结束回合按钮较突出，单位操作和地块说明分开。

### 设计判断与可借鉴项

- 适合借鉴信息分层：全局、单位、格子三个尺度各有稳定位置。
- 棋盘提示结合形状、箭头、数字，能作为风险预览结构的参考。

### 代价与未验证项

- 多区域同时出现会提高初次理解成本，需要教学和按需提示。
- 这是克制的科幻仪表风格，并无全息发光材质；holo-terminal 仅作信息结构借鉴。

不照搬霓虹；主要借鉴终端式面板的信息组织和战术标记。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-005 · Sea of Stars

战斗命令与升级选择：状态与决策分别占据清楚位置

作者/项目：Sabotage Studio。[官方来源](https://store.steampowered.com/app/1244090/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：平面信息区、少量金色装饰与重点强调。
- 世界关系：命令/状态/升级画面面向玩家；完整叙事解释未验证。
- 系统关联：battle-command, progression
- 迁移范围：参考任务组织、材质与像素层级；需按项目重新绘制资产和验证中文/输入。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![战斗命令靠近当前角色，左下按队员列出生命和魔法，敌方头顶显示图标信息。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1244090/ss_f756ff477590284c7192ffcef99237de056e4aeb.1920x1080.jpg?t=1780931183)

战斗命令靠近当前角色，左下按队员列出生命和魔法，敌方头顶显示图标信息。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1244090/ss_f756ff477590284c7192ffcef99237de056e4aeb.1920x1080.jpg?t=1780931183) · [出处](https://store.steampowered.com/app/1244090/?l=english)

- 战斗命令靠近当前角色，左下按队员列出生命和魔法，敌方头顶显示图标信息。

### 官方游戏截图 2

![升级页以四个大图标展示选择，底部列出属性变化，手形指针标记当前项。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1244090/ss_3fe41c00a7122c63aa05b4ea331c6f995e356788.1920x1080.jpg?t=1780931183)

升级页以四个大图标展示选择，底部列出属性变化，手形指针标记当前项。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1244090/ss_3fe41c00a7122c63aa05b4ea331c6f995e356788.1920x1080.jpg?t=1780931183) · [出处](https://store.steampowered.com/app/1244090/?l=english)

- 升级页以四个大图标展示选择，底部列出属性变化，手形指针标记当前项。

### 可见事实

- 战斗面板采用深色矩形底和较细边框，命令选中项有色块及指针。
- 升级页扩大图标和留白，以金色标题、少量装饰和底部数值摘要建立层级。

### 设计判断与可借鉴项

- 适合借鉴任务驱动的密度变化：战斗保持紧凑，奖励选择释放空间。
- 升级前后数值与选择图标同屏，便于比较当前决策。

### 代价与未验证项

- 两张静态图不能说明切换动画、焦点顺序或动态信息是否清楚。
- 英文缩写较多；中文和辅助说明需单独验证，不宜机械套用字体与间距。

ornate-fantasy 可借鉴装饰克制与关键奖励的强调，不意味着游戏官方遵循此配方。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-006 · Backpack Hero

空间背包与出售面板：界面直接承载核心决策

作者/项目：Jaspel / Pretty Soon / IndieArk。[官方来源](https://store.steampowered.com/app/1970580/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：棕色框形、格子和强像素字；不是纸纹证据。
- 世界关系：背包/交易面板与战斗图景同屏；叙事归属未验证。
- 系统关联：inventory-equipment, shop-trade
- 迁移范围：参考任务组织、材质与像素层级；需按项目重新绘制资产和验证中文/输入。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![战斗上方的背包显示多格物品，浮层展示选中护甲的规则与数值。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1970580/ss_e39025fae7fd8cc1f0f9c15cc7c66748e92d4773.1920x1080.jpg?t=1771527569)

战斗上方的背包显示多格物品，浮层展示选中护甲的规则与数值。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1970580/ss_e39025fae7fd8cc1f0f9c15cc7c66748e92d4773.1920x1080.jpg?t=1771527569) · [出处](https://store.steampowered.com/app/1970580/?l=english)

- 战斗上方的背包显示多格物品，浮层展示选中护甲的规则与数值。

### 官方游戏截图 2

![出售页把持有物品与待售物品分栏，中间有转移箭头，右侧显示资源收益。](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1970580/ss_507d43eec5d1b81ac876d25619e058a1672e64b0.1920x1080.jpg?t=1771527569)

出售页把持有物品与待售物品分栏，中间有转移箭头，右侧显示资源收益。 · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1970580/ss_507d43eec5d1b81ac876d25619e058a1672e64b0.1920x1080.jpg?t=1771527569) · [出处](https://store.steampowered.com/app/1970580/?l=english)

- 出售页把持有物品与待售物品分栏，中间有转移箭头，右侧显示资源收益。

### 可见事实

- 背包物品的长度和占格直接可见；说明浮层把标题、稀有度和规则分段。
- 出售页使用统一棕色框、卡格和粗体标题，并把转移方向画在两栏之间。

### 设计判断与可借鉴项

- 适合借鉴让UI服务玩法：占格与物品形状是决策信息，不只是装饰。
- 待售清单与收益预览同屏，可作为交易确认前的结构参考。

### 代价与未验证项

- 长规则浮层会遮挡战斗与背包，需检查定位和可关闭行为。
- 粗像素字与密集行文在小屏/中文下风险较高；未验证实际交互。

wood-paper 仅借鉴棕色框体和一致组件；实际背景是棕色平面，不应声称具有纸纹。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-007 · Papers, Please

证件桌面：让比对对象、操作工具和决定位置建立映射

作者/项目：Lucas Pope / 3909。[官方来源](https://store.steampowered.com/app/239030/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：观察：低分辨率像素字、有限色阶、纸张与机械印章等物件外形；包含材质拟物和操作隐喻两个维度。
- 世界关系：观察：文件与印章被画成工作台中的对象，同时上方有俯视关卡视图。推断：工作台具有叙事内工具语义；角色是否能感知每个高亮框与提示文字为 UNDETERMINED，不能给整屏统一标为世界内 UI。
- 系统关联：当前系统模式尚未细分此任务。
- 迁移范围：像素适用性较高：可迁移并排比对、视觉高亮和道具化控件。纸张/印章原图只供研究；中文长文本、触屏和手柄操作需另做布局与输入验证。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。
- 关联边界：核心任务是文书核验，暂未纳入当前16个系统模式；不强行归为对话或收藏。

### 官方游戏截图 1

![差异比对：亮色人像框、连线与询问入口（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/239030/ss_6c095a8ff86f9ebf8f796d23b1186c176fd21991.1920x1080.jpg?t=1678266428)

差异比对：亮色人像框、连线与询问入口（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/239030/ss_6c095a8ff86f9ebf8f796d23b1186c176fd21991.1920x1080.jpg?t=1678266428) · [出处](https://store.steampowered.com/app/239030/?l=english)

- 两个人像比较区被亮框强调，背景压暗。
- 差异文字位于比较连线附近，询问入口在左侧接待区。
- 这是已显示差异的静态状态，触发过程未观察。

### 官方游戏截图 2

![文书决策：批准/拒绝印章与待盖章区域（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/239030/ss_c133e1bf1da17a3f3719c74696c61da23e38eefe.1920x1080.jpg?t=1678266428)

文书决策：批准/拒绝印章与待盖章区域（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/239030/ss_c133e1bf1da17a3f3719c74696c61da23e38eefe.1920x1080.jpg?t=1678266428) · [出处](https://store.steampowered.com/app/239030/?l=english)

- 两枚印章同时有颜色和文字标签；护照位于右下方。
- 纸面显示待盖章位置，印章横梁下有对齐说明。
- 尚未显示盖章完成结果；不能据此宣称成功反馈或撤销机制。

### 可见事实

- 观察：画面上方保留关卡与队伍，下方把人物接待区和文件桌面分开；桌面同时容纳护照、通缉名单或规则册。
- 观察：差异模式将其余画面压暗，用亮色框和连线标出两张人像；第二张图让红绿印章位于证件的盖章区域上方。

### 设计判断与可借鉴项

- 设计推断：对照材料与判断目标同屏，减少来回翻页的记忆负担；聚焦、连线和文字一起说明本次比较关系。
- 设计推断：印章的标签、形状与位置共同表达批准/拒绝动作，拟物结构服务文书任务，具有比单纯纸纹装饰更明确的操作映射。

### 代价与未验证项

- 代价推断：桌面对象会争夺空间，密集的小字与多份文件增加寻找成本；移植到小屏必须重新验证字号和遮挡。
- 证据边界：截图未展示盖章后的成功状态，也无法证明输入命中范围、撤销、错误恢复或对色觉差异的支持。
- 文书核验是本库当前16模式之外的任务，需独立定义比对字段、审批后果与恢复规则。

适用于经营、边检、鉴定、交易审核等以比较文书为核心的像素任务。先规定比较字段、工具位置与结果反馈，再决定纸张和桌面材质；不要把所有背包都改成会遮挡内容的纸堆。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-008 · Return of the Obra Dinn

双色调查工具：把场景线索与人物记录分成不同阅读任务

作者/项目：Lucas Pope / 3909。[官方来源](https://store.steampowered.com/app/653530/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：观察：双色/单色调外观、抖动与排线、书页式记录框；这两张画面的风格描述不能替代引擎渲染和资产技术规格。
- 世界关系：观察：怀表具有手持物件的空间位置；人物记录以面向屏幕的矩形卡片覆盖在书页背景上。叙事归属的细分为设计推断，具体控件是否被角色感知为 UNDETERMINED。
- 系统关联：collection-codex
- 迁移范围：非标准二维像素制作对照。可迁移“物件负责情境、干净面板负责密集阅读”和双色层级；需要单独制定本项目像素大小、字形与纹理密度。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。
- 关联边界：仅参考人物调查记录的肖像、身份/命运句子与记忆计数；不是常驻HUD或任务阶段/追踪流程的证据。调查推理与证据核验不等同一般收藏系统，尚需独立任务模式。

### 官方游戏截图 1

![怀表与调查现场的空间关系（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/653530/ss_380dc35237fde7d3863a44270abafc37924d1db4.1920x1080.jpg?t=1686697594)

怀表与调查现场的空间关系（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/653530/ss_380dc35237fde7d3863a44270abafc37924d1db4.1920x1080.jpg?t=1686697594) · [出处](https://store.steampowered.com/app/653530/?l=english)

- 怀表、手与现场处于同一画面，物件轮廓从地面纹理中凸显。
- 表盘中央是图形符号；此图没有完整操作提示或激活前后状态。

### 官方游戏截图 2

![人物记录卡：肖像、叙述与记忆数量（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/653530/ss_80149ba9e106d3c4bfe717e280806bc0daa6c5b7.1920x1080.jpg?t=1686697594)

人物记录卡：肖像、叙述与记忆数量（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/653530/ss_80149ba9e106d3c4bfe717e280806bc0daa6c5b7.1920x1080.jpg?t=1686697594) · [出处](https://store.steampowered.com/app/653530/?l=english)

- 肖像在左，身份与死亡相关句子在右，底部有记忆计数。
- 纯净卡片底与粗边框减少书页背景纹理对正文的干扰。

### 可见事实

- 观察：一张图的前景是手持圆形怀表，背景是船上人物与地面；另一张图的中心记录卡由人物肖像、命运句子和记忆计数组成。
- 观察：中心卡片使用较纯净的浅底和粗边框，把文本从底层密集线条与抖动纹理中分离。

### 设计判断与可借鉴项

- 设计推断：肖像与身份/命运句子并置，让记录围绕“这个人是谁、发生了什么”而组织，减少与调查目标无关的栏目。
- 设计推断：有限颜色下以留白、轮廓与区域隔离保持层级，说明层级不必依赖大量色相。

### 代价与未验证项

- 代价推断：世界画面的大量抖动纹理可能与细小轮廓竞争；同类双色设计需要分别测试环境识别和长文阅读。
- 证据边界：静态图不能确认怀表交互步骤、人物记录编辑方式或正确性反馈；双色观感不等于整套素材采用同一像素网格。

适合像素推理游戏的证据册、人物关系和知识状态设计。迁移记录结构与留白规则；不要直接把三维双色渲染截图当作可复用像素资产或据此判断其全流程可用性。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-009 · Loop Hero

磨损像素面板：把建筑依赖、资源条件和卡组约束分层

作者/项目：Four Quarters / Devolver Digital。[官方来源](https://store.steampowered.com/app/1282730/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：观察：像素卡片、灰色磨损边框、暗红底、装饰纹样和较粗像素字。卡片式信息组织与磨损材质是两个可独立替换的维度。
- 世界关系：观察：建筑树和卡组以正对屏幕的菜单显示，未见其作为场景物件的证据。可以描述为屏幕菜单；是否具有叙事内解释为 UNDETERMINED。
- 系统关联：progression
- 迁移范围：可迁移像素面板与建筑/配置结构；本例观察到的是建筑依赖菜单，不是放置预览、碰撞或确认建造全过程。卡组任务也不能仅凭卡片外形归为背包。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。
- 关联边界：仅参考建筑依赖目录、条件和解释区；未观察空间定位、旋转、占地或提交放置。另一图是出发前卡组配置，当前16模式尚未细分此任务，不因卡片排列归为收藏或背包。

### 官方游戏截图 1

![建筑菜单：依赖线、资源数字与固定详情栏（官方游戏截图，含旧版本标记）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1282730/ss_455789884ed94fd20410ac5a139e8c3bb8f6f369.1920x1080.jpg?t=1751489185)

建筑菜单：依赖线、资源数字与固定详情栏（官方游戏截图，含旧版本标记） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1282730/ss_455789884ed94fd20410ac5a139e8c3bb8f6f369.1920x1080.jpg?t=1751489185) · [出处](https://store.steampowered.com/app/1282730/?l=english)

- 中心建筑卡之间有连接线，主区域与右侧说明栏分离。
- 鼠标所指建筑有浅色装饰边框；其他卡片可见不同明暗和资源数字。
- 这些外观能证明存在状态差别，不能单凭截图还原全部解锁规则。

### 官方游戏截图 2

![卡组配置：分组计数、总量和确认（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1282730/ss_58039fc526fe3f2006826a8ea11ca64c145b7a24.1920x1080.jpg?t=1751489185)

卡组配置：分组计数、总量和确认（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1282730/ss_58039fc526fe3f2006826a8ea11ca64c145b7a24.1920x1080.jpg?t=1751489185) · [出处](https://store.steampowered.com/app/1282730/?l=english)

- 牌以多行排列；每行左侧存在数值组，底部集中显示总数与确认。
- 当前高亮卡片有边框，说明位于固定右栏，正文不塞进小牌面。

### 可见事实

- 观察：建筑菜单将建筑卡和连接线放在主区域，右栏显示所指建筑的名称、说明和资源；部分资源数字以不同颜色显示。
- 观察：卡组菜单按行组织卡牌，左侧有分组计数，底部有总数和确认按钮，右栏解释当前高亮卡牌。

### 设计判断与可借鉴项

- 设计推断：依赖关系使用连接线，单个建筑的解释交给固定详情栏，能让“关系”和“属性”各有阅读区域。
- 设计推断：局部计数与总计并存，适合存在多组约束的配置任务；装饰高亮边框提供了与明暗不同的视觉线索；它对应悬停、选中还是输入焦点尚未验证。

### 代价与未验证项

- 代价推断：磨损纹理、扫描线观感和装饰框与较密正文同时出现，可能降低小屏阅读；迁移时要优先保证文字与状态可辨。
- 证据边界：图中可见不同明暗、边框和数字，但未完整验证它们对应的全部状态；官方商店画面带旧版本号，不能代表当前版本每一处布局。

适用于俯视生存/营地经营中的建筑解锁，以及出发前卡组或工具配置。先固定前置、费用、当前库存、焦点、已选和不可用的独立编码，再选择磨损金属或其他材质。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-010 · Caves of Qud

终端感菜单：用身体映射、分类清单和任务地图组织大量内容

作者/项目：Freehold Games / Kitfox Games。[官方来源](https://store.steampowered.com/app/333640/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：观察：暗青色平面面板、细边线、近等宽文字、少量高饱和像素符号；终端感主要来自排版与配色，并非只有绿色单色终端一种样式。
- 世界关系：观察：菜单覆盖世界背景并保持屏幕对齐；界面是否是角色使用的设备没有可见证据，标记 UNDETERMINED，不能因终端外观自动归为世界内。
- 系统关联：inventory-equipment, quest-journal, map-navigation
- 迁移范围：与俯视像素 RPG 直接相关：优先迁移组织方式和键盘提示结构。密度、色阶和字号需按本项目的逻辑分辨率重新制定，不照搬截图缩小。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![装备与库存：身体槽位图和分类列表（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/333640/ss_796b188786b8978574444587bf9f4198fb18f724.1920x1080.jpg?t=1790186617)

装备与库存：身体槽位图和分类列表（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/333640/ss_796b188786b8978574444587bf9f4198fb18f724.1920x1080.jpg?t=1790186617) · [出处](https://store.steampowered.com/app/333640/?l=english)

- 左侧槽位带身体位置标签，右侧列表包含类别、数量、重量或装备相关文字。
- 上方系统页签和物品类别图标是不同层级；底部有搜索与操作提示。

### 官方游戏截图 2

![任务页：文本目标与地图地点并排（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/333640/ss_ea6b9000da700c6bb5fa2afe9770ecf99082b9b5.1920x1080.jpg?t=1790186617)

任务页：文本目标与地图地点并排（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/333640/ss_ea6b9000da700c6bb5fa2afe9770ecf99082b9b5.1920x1080.jpg?t=1790186617) · [出处](https://store.steampowered.com/app/333640/?l=english)

- 任务标题、委托人、目标与说明采用不同缩进和颜色。
- 地图上能看到地点与任务名称；本图不证明选择任务后地图必然自动追踪。

### 可见事实

- 观察：装备页左侧按身体位置布置槽位，右侧物品按类别折叠分组；顶部有跨系统页签，底部有搜索框与按键提示。
- 观察：任务页以任务标题、委托人/地点、目标和补充说明形成文本层级，右侧地图显示地点和任务标签。

### 设计判断与可借鉴项

- 设计推断：身体位置图负责空间映射，分类列表负责大量物品扫描，避免让一种组织方式承担全部任务。
- 设计推断：任务摘要与位置并排可以把“要做什么”与“去哪里”关联；重复使用页签、分栏和底部提示有助于形成操作习惯。

### 代价与未验证项

- 代价推断：深色底上的细线、较暗文字和众多颜色状态需要在目标显示条件下测量；不能因有键盘提示就宣称无障碍合格。
- 证据边界：截图未展示搜索结果、滚动边界、折叠后的状态或所有身体类型；颜色的全部语义和地图同步机制尚未验证。

适用于内容量大、身体槽位复杂或文本任务多的像素 RPG。先定义类别、搜索字段、身体映射和任务句法，再选择终端配色；中文长名、重绑定按键和手柄焦点需要独立验收。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-011 · Factorio

工业管理：地图抽象与物品/配方分工（含历史设计稿）

作者/项目：Wube Software LTD.。[官方来源](https://store.steampowered.com/app/427520/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：观察：地图用抽象色块、线和工具图标；历史制作稿用深灰模块与有体积感的物品图标。工业感不要求所有区域都模拟金属面板。
- 世界关系：观察：地图控制和制作稿为屏幕对齐界面。是否作为角色持有的设备或世界内对象无法仅凭这两张图确认，标记 UNDETERMINED。
- 系统关联：map-navigation, hud, inventory-equipment, crafting
- 迁移范围：俯视建造结构相关性高，图标并非本库可直接复用的像素资产。可迁移地图抽象、分类与制作语义；历史设计稿需作为过程案例而非当前成品标准。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![地图：网络、地形与定位警告（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/427520/ss_5903f8ff243e9a89b4f1e15e6e7982159578f8ec.1920x1080.jpg?t=1792752343)

地图：网络、地形与定位警告（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/427520/ss_5903f8ff243e9a89b4f1e15e6e7982159578f8ec.1920x1080.jpg?t=1792752343) · [出处](https://store.steampowered.com/app/427520/?l=english)

- 地图大面积显示地形色块、运输/工厂线条与警告符号。
- 工具按钮集中在右上与下方，警告同时出现在地图位置及边缘提示区域。

### 开发者设计稿 2

![库存与制作分区（开发者 2019 年设计稿，非当前运行截图）](https://cdn.factorio.com/assets/img/blog/fff-289-crafting-tab.png)

库存与制作分区（开发者 2019 年设计稿，非当前运行截图） · [原图](https://cdn.factorio.com/assets/img/blog/fff-289-crafting-tab.png) · [出处](https://www.factorio.com/blog/post/fff-289)

- 左侧库存和右侧制作区共用网格语言，但区块标题、页签与槽位视觉不同。
- 黑灰圆点中的编号是博客注释编号，不能纳入交互组件清单。
- 开发者文章解释了物品槽与制作按钮的语义差异；本图不证明方案全部落地。

### 可见事实

- 观察：商店截图把地形和工厂网络压缩成色块与线，警告三角形直接标在地图位置上；快捷栏与工具仍贴近屏幕边缘。
- 观察：2019 年官方制作页设计稿将库存与制作区左右分开，使用分类页签、图标格和数量；稿中的数字标注属于设计说明，不能当作游戏控件。

### 设计判断与可借鉴项

- 设计推断：抽象地图减少建筑细节以便观察网络与异常位置，体现“当前任务决定信息粒度”，而非一味复用世界美术。
- 来源事实＋推断：开发者在历史文章中区分库存物品和制作的虚拟按钮；设计上这能帮助区分“拥有多少”和“可以执行什么”，但具体成效未由本次测试验证。

### 代价与未验证项

- 代价推断：地图依赖多种色块和少量图标，新用户需要图例、筛选或说明；复杂世界缩略后也可能产生过密符号。
- 证据边界：制作图是 2019-04-05 公开的设计稿，不是当前运行截图；不能据此断言当前版本行为、响应速度或最终实现细节。

适用于俯视建造/物流游戏的地图、库存和制作任务。可学习“资产列表”与“行动列表”的语义分离，以及地图尺度变化时的信息简化；美术材质和功能层级应分别验收。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-012 · FTL: Faster Than Light

舰船管理：锁定原因、升级层级与提交动作的可见表达

作者/项目：Subset Games。[官方来源](https://store.steampowered.com/app/212680/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：观察：浅亮框、切角面板、细格仪表与像素式标题构成科幻控制台感；多数信息仍按平面模块排布，不必模拟真实驾驶舱。
- 世界关系：观察：选择与升级面板覆盖游戏背景且正对屏幕。其叙事内设备归属没有静态证据，标记 UNDETERMINED；科幻外观并不等于世界内交互。
- 系统关联：progression, collection-codex
- 迁移范围：可迁移给二维像素战术/经营：解锁状态、模块分组、费用与可撤销入口。截图中图标和字体为参考，不作为开源素材；语义相似的图标需测试识别而非只审风格。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。
- 关联边界：progression仅参考升级分组、等级、费用及提交入口；collection-codex仅参考舰船解锁条目与条件展示，不代表完整图鉴、获取或收藏提交流程。

### 官方游戏截图 1

![舰船解锁：高亮、锁图标和条件说明（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/212680/ss_a97ea1950b4e1a61b07c5a44cbbbb50a3c29dc27.1920x1080.jpg?t=1748969356)

舰船解锁：高亮、锁图标和条件说明（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/212680/ss_a97ea1950b4e1a61b07c5a44cbbbb50a3c29dc27.1920x1080.jpg?t=1748969356) · [出处](https://store.steampowered.com/app/212680/?l=english)

- 明亮边框圈出鼠标所指的黑色舰船轮廓，中心有锁。
- 下方说明框提供该条目的条件；其他舰船展示不同可见状态。

### 官方游戏截图 2

![系统升级：等级、费用、说明和接受入口（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/212680/ss_d0fe8166c0e95f0fd369b6bac59c38b2fb562f3f.1920x1080.jpg?t=1748969356)

系统升级：等级、费用、说明和接受入口（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/212680/ss_d0fe8166c0e95f0fd369b6bac59c38b2fb562f3f.1920x1080.jpg?t=1748969356) · [出处](https://store.steampowered.com/app/212680/?l=english)

- 系统、子系统、反应堆分组；费用图标和数值接近每个升级模块。
- 右栏对应当前高亮系统，底部可见撤销和接受；仅据截图不能还原提交语义。

### 可见事实

- 观察：舰船选择页使用可见舰船、黑色轮廓和锁图标区分条目；鼠标所指条目有黄色边框，说明框描述对应舰船及解锁条件。
- 观察：升级页将系统、子系统和反应堆分组，以柱状格数与费用呈现升级信息；右侧提供功能与层级说明，底部有撤销和接受按钮。

### 设计判断与可借鉴项

- 设计推断：锁图标与轮廓并用，使“尚未获得”区别于普通未选中；让条件说明对应当前高亮条目，可能比让玩家猜测灰色条目更容易理解；这需要实际任务验证。
- 设计推断：当前资源、每项成本、等级格数和提交入口同时可见，有利于做升级方案比较；分组比仅换颜色更能说明系统类别。

### 代价与未验证项

- 代价推断：多个系统以相似小图标和绿色格数表达，玩家仍需学习符号；浓重发光边缘和全大写字形不宜直接缩到更小的像素画布。
- 证据边界：可以确认撤销/接受入口的存在，但没有运行验证资源扣除时机、批量撤销范围、手柄导航或错误处理。

适合俯视战术、船舶/基地经营中的载具解锁与模块升级。迁移锁定状态的解释和费用比较结构；为项目明确“预览、暂存、提交、取消”的状态机后再实现。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-013 · Inscryption

桌面卡牌与纸面路线：空间化界面的气氛收益与阅读代价

作者/项目：Daniel Mullins Games / Devolver Digital。[官方来源](https://store.steampowered.com/app/1092790/?l=english)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：观察：三维桌面、纸牌与地图的材质拟物，叠加低分辨率/颗粒观感；这些图不能视为标准二维像素素材制作示范。
- 世界关系：观察：卡牌与地图具有桌面中的空间位置，顶端字幕采用单独的屏幕层。可确认呈现方式混合；角色对字幕及所有数值的感知为 UNDETERMINED。
- 系统关联：battle-command, map-navigation
- 迁移范围：非像素对照，只迁移信息摆位、空间隐喻及代价评估。俯视项目可保留桌面物件语义而减小透视，重新制定卡牌栅格、字体与命中区域。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方游戏截图 1

![桌面牌局：近景手牌、牌位与远端对手（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1092790/ss_0191a69b0e94a9a7784f5b81e27f06379910645a.1920x1080.jpg?t=1777572925)

桌面牌局：近景手牌、牌位与远端对手（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1092790/ss_0191a69b0e94a9a7784f5b81e27f06379910645a.1920x1080.jpg?t=1777572925) · [出处](https://store.steampowered.com/app/1092790/?l=english)

- 近景卡片互相遮挡，桌面牌位形成明确行列。
- 卡片上的名称和符号受距离、照明与透视影响；未观察放大后的状态。

### 官方游戏截图 2

![路线地图：路径节点与屏幕叙述层并存（官方游戏截图）](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1092790/ss_3b714682e9e0a214df1630a234e9f6764528eece.1920x1080.jpg?t=1777572925)

路线地图：路径节点与屏幕叙述层并存（官方游戏截图） · [原图](https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1092790/ss_3b714682e9e0a214df1630a234e9f6764528eece.1920x1080.jpg?t=1777572925) · [出处](https://store.steampowered.com/app/1092790/?l=english)

- 虚线路线连接图形节点，树木和纸面提供物件情境。
- 顶端文字未随桌面透视倾斜，说明本画面并非所有信息都采用同一空间关系。

### 可见事实

- 观察：牌局中手牌位于近景下方，桌面有规则排列的牌位，对手位于远端；卡面包含名称、数字和符号。
- 观察：路线页的路径与节点画在桌面地图上，立体树木围绕路径；叙述文字仍位于画面顶端，与桌面地图有不同朝向。

### 设计判断与可借鉴项

- 设计推断：可操作对象与游戏情境使用同一种物件语言，桌面位置为牌位和前进路线提供空间结构。
- 设计推断：地图路径是决策信息，树木与桌面是情境信息；分离这两层后可以保留气氛而简化阅读区域。

### 代价与未验证项

- 代价推断：昏暗照明、透视缩短与手牌相互遮挡会影响卡面阅读；空间感不能替代选中、目标合法性和结果反馈。
- 证据边界：静态图不能证明每个物件可操作，也不能确认自动放大、镜头过渡、输入命中范围或信息是否被角色感知。

作为非像素对照，适合像素卡牌、桌游工作台、纸面旅行图的布局研究。先用平视可读的卡牌与清楚路径验证任务，再决定要加入多少透视、阴影和装饰；不把所有信息都强行放进场景。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。


## UI-CASE-014 · Dead Space (2023)

官方设置页：主题面板也必须说明选项含义和条件关系

作者/项目：Motive / Electronic Arts。[官方来源](https://www.ea.com/able/resources/dead-space/dead-space/pc/gameplay)。

**分类观察（不代表整款游戏统一分类）**

- 视觉：观察：蓝青发光、切角、半透明与透视叠层构成科幻投影外观；选项内容仍遵循列表、条目高亮、说明区的常规信息结构。
- 世界关系：观察：面板以带透视的形式显示并叠放菜单层。是否真实锚定于游戏世界、是否被角色感知不能仅凭设置图确认，标记 UNDETERMINED；“看似全息”不是世界内 UI 的充分证据。
- 系统关联：settings-accessibility
- 迁移范围：非像素对照，迁移设置的信息架构、控件语义与状态覆盖。将外观改为项目一致的像素组件，同时保留文字解释和输入提示，不能以复古为由省去可读性。
- 输入语义：UNDETERMINED：本案未运行输入测试。静态高亮不能单独确定悬停、选中、键盘/手柄焦点及命中区域；应用建议中的焦点要求是待实现和验证的设计要求。

### 官方设置指南 1

![Gameplay 设置：多种控件与高亮条目说明（EA 官方设置指南画面）](https://media.contentapi.ea.com/content/dam/eacom/ea-accessibility/dead-space/pc/dead-space-pc-gameplay-picture-1.png.adapt.crop16x9.1920w.png)

Gameplay 设置：多种控件与高亮条目说明（EA 官方设置指南画面） · [原图](https://media.contentapi.ea.com/content/dam/eacom/ea-accessibility/dead-space/pc/dead-space-pc-gameplay-picture-1.png.adapt.crop16x9.1920w.png) · [出处](https://www.ea.com/able/resources/dead-space/dead-space/pc/gameplay)

- 难度选项处于高亮状态，右侧显示当前难度及说明；列表同时包含开关、选值和数值滑条。
- 底部可见选择、重置、返回的输入提示。

### 官方设置指南 2

![教程与视角设置：选项依赖需要结合文档（EA 官方设置指南画面）](https://media.contentapi.ea.com/content/dam/eacom/ea-accessibility/dead-space/pc/dead-space-pc-gameplay-picture-2.png.adapt.crop16x9.1920w.png)

教程与视角设置：选项依赖需要结合文档（EA 官方设置指南画面） · [原图](https://media.contentapi.ea.com/content/dam/eacom/ea-accessibility/dead-space/pc/dead-space-pc-gameplay-picture-2.png.adapt.crop16x9.1920w.png) · [出处](https://www.ea.com/able/resources/dead-space/dead-space/pc/gameplay)

- 教程重置动作处于高亮状态，右侧描述重置用途；同页还列出显示教程、视角朝向与回正。
- 依赖关系来自官方文字说明，而不是仅靠这张启用状态截图推导。

### 可见事实

- 观察：Gameplay 设置页以纵向列表排列选项，右侧留出解释区；列表中同时有开关、左右选值、滑条数值与进入下级页面的箭头。
- 来源事实：EA 官方说明记载了部分设置间的条件关系，例如启用定位路径朝向时不能使用另一项视角回正；教程重置也依赖显示教程设置。两张图未覆盖所有禁用状态。

### 设计判断与可借鉴项

- 设计推断：当前行的高亮与右侧解释形成位置稳定的阅读路径，使短标签承担检索、解释区承担后果说明。
- 设计推断：把选项关系写入规格能够避免看似能操作却不起效的控件；开关、枚举与动作入口应按语义区分。

### 代价与未验证项

- 代价推断：透视、发光、叠放的背景菜单形成科幻气氛，也增加视觉复杂度；长中文标签和低分辨率适配需要重新排版。
- 证据边界：这是 EA 官方设置指南中的画面，不能用来证明整个游戏 HUD 的世界内设计，或宣布全部无障碍能力已通过用户测试。

作为非像素设置系统对照，适用于任何像素游戏的难度、输入方式、教程与辅助选项。迁移选项分类、后果说明和条件依赖；不必复制倾斜发光外观。验收时覆盖开启、关闭、不可用、恢复默认和返回。

图像权利：No open-content license verified for game screenshots。仅作来源引用与设计评论。
