import requests,concurrent.futures,json
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
D=[('introduction','建立项目、地图与外置图块集','从新建项目、创建地图到首次绘制图块，适合作为入门起点。'),('projects','组织地图项目','集中组织地图、图块、对象模板和团队项目配置。'),('maps','选择地图与投影类型','比较正交、等距和其他地图方向，先固定项目使用的投影。'),('layers','规划地图图层','区分图块、对象、图像和组图层的职责。'),('editing-tile-layers','使用图块笔刷与选区','学习批量绘制和修改地图布局。'),('objects','使用对象层标注交互','用形状和图块对象表达出生点、触发区域及可交互物。'),('editing-tilesets','图块集、动画与碰撞','在图块层面维护重用信息，阅读时重点查动画和碰撞编辑器。'),('custom-properties','让地图数据可被游戏读取','为地图和对象附加自定义字段并统一数据约定。'),('using-templates','对象模板复用','把重复对象的共同属性整理成模板。'),('terrain','自动连接地形边界','学习角、边及混合 terrain set 的标记和连接方式。'),('using-infinite-maps','无限地图与分块','理解不同于固定宽高地图的编辑方式。'),('worlds','把多张地图放入同一世界','在更大的空间中布置相邻地图。'),('automapping','自动映射规则','用规则地图处理重复地形和局部模式。'),('export','地图导出与消费方兼容','核对目标引擎能读取的格式及导出选项。')]
def fetch(x):
 slug,title,summary=x;u='https://doc.mapeditor.org/en/stable/manual/'+slug+'/'
 r=requests.get(u,timeout=45);r.raise_for_status();s=BeautifulSoup(r.content,'html.parser')
 return {'title':title,'summary':summary,'url':r.url,'source_title':s.title.get_text(),'status':r.status_code}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:rows=list(e.map(fetch,D))
p=R/'guides'/'asset-production';p.mkdir(parents=True,exist_ok=True)
t='# Tiled 场景地图补充阅读导航\n\n核验日期：2026-10-29。以下是 14 个已成功访问的官方页面，仅提供短导读与链接，不计入 24 篇 Krita 完整图文教程。\n\n## 为什么这里保留导航\n\n本次检查了 Tiled 官网页脚、仓库 `COPYING`、文档目录和 README：`COPYING` 列明软件部分的 GPL/BSD；TMX 格式参考页明确注明 CC BY-SA 3.0，但没有查到可明确覆盖整部用户手册的统一再发布声明。因此这里没有复制整部 Tiled 手册正文或教学截图，也没有把软件许可证套用到手册。可从下列原站链接继续阅读。\n\n- [仓库 COPYING](https://github.com/mapeditor/tiled/blob/master/COPYING)\n- [文档 README](https://github.com/mapeditor/tiled/blob/master/docs/README.md)\n- [TMX 格式参考及其许可声明](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/)\n\n## 按工作任务选读\n\n| 任务 | 官方页面 | 阅读用途 |\n|---|---|---|\n'
for row in rows:t+='| '+row['title']+' | ['+row['source_title'].split(' — ')[0]+']('+row['url']+') | '+row['summary']+' |\n'
t+='\n## 版本与引擎边界\n\n抓取时页面标题标为 Tiled 1.12.2。Tiled 负责地图编辑和数据输出；目标引擎是否识别某项自定义属性、对象模板、碰撞或地形数据，需要单独核对导入器。先做一张含图块、碰撞和交互对象的小测试地图，再扩展到完整场景。以上导读由整理者编写，未声称已在本机运行或验证引擎导入。\n'
(p/'TILED-READING-LIST.md').write_text(t,encoding='utf-8')
(R/'logs'/'asset-production'/'tiled-reading-links.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Tiled verified',len(rows))
