#!/usr/bin/env python3
"""Reproduce the 24 illustrated Saint11 drawing lessons from a pinned source.

Run with the project Python environment. --offline rebuilds Markdown and
metadata from already downloaded assets without network traffic. Original
GIF bytes are never resized, recolored, or recompressed. Static sheets only
extract frames and add labels outside the original image area.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

import requests
import yaml
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "ce1393eb2c46441d917134a9fd52e15575ee10a7"
REPO = "https://github.com/saint11/Saint11Tutorials"
RAW = f"https://raw.githubusercontent.com/saint11/Saint11Tutorials/{COMMIT}/"
DATE = "2026-10-29"
LICENSE = "CC-BY-4.0"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(url: str, dest: Path, offline: bool) -> None:
    if dest.exists():
        return
    if offline:
        raise FileNotFoundError(f"Offline asset missing: {dest}")
    response = requests.get(url, timeout=(15, 90))
    response.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(response.content)


def extract_frames(source: Path, outdir: Path) -> dict:
    with Image.open(source) as im:
        durations = []
        for index in range(im.n_frames):
            im.seek(index)
            durations.append(im.info.get("duration", 100))
        total = sum(durations)
        selected = []
        for fraction in [0, 0.33, 0.66, 0.99]:
            elapsed = 0
            index = len(durations) - 1
            for candidate, duration in enumerate(durations):
                if elapsed + duration > total * fraction:
                    index = candidate
                    break
                elapsed += duration
            selected.append({"frame": index, "time_ms": elapsed})
        width, height = im.size
        sheet = Image.new("RGB", (2 * (width + 8), 2 * (height + 33)), "#e8e8e8")
        draw = ImageDraw.Draw(sheet)
        for position, frame in enumerate(selected):
            im.seek(frame["frame"])
            x, y = position % 2 * (width + 8), position // 2 * (height + 33)
            sheet.paste(im.convert("RGB"), (x, y + 25))
            label = f'{outdir.name} | frame {frame["frame"]}/{im.n_frames - 1} | {frame["time_ms"] / 1000:.2f}s'
            draw.text((x + 5, y + 5), label, fill="black")
        sheet.save(outdir / "keyframes.png")
        im.seek(0)
        im.convert("RGB").save(outdir / "preview.png")
        frame_info = {
            "original": source.name, "width": width, "height": height,
            "frames": im.n_frames, "duration_ms": total, "selected": selected,
            "operation": "Extract original frames at 0/33/66/99 percent of duration; add labels outside frames; no interpolation or art recoloring.",
        }
        (outdir / "frames.json").write_text(json.dumps(frame_info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return frame_info


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    lessons = json.loads((ROOT / "tools/drawing_lessons.json").read_text(encoding="utf-8"))
    if len(lessons) != 24:
        raise ValueError("Expected exactly 24 curated source tutorials")
    fetch(RAW + "README.md", ROOT / "licenses/saint11-README.md", args.offline)
    license_text = (ROOT / "licenses/saint11-README.md").read_text(encoding="utf-8")
    if "Creative Commons Attribution 4.0 International License" not in license_text:
        raise ValueError("Pinned source no longer has the expected license statement")
    manifest = []
    for sequence, lesson in enumerate(lessons, 1):
        lesson_id = f"ART-{sequence:03d}"
        relative_asset_dir = Path("assets/drawing") / lesson_id
        asset_dir = ROOT / relative_asset_dir
        asset_dir.mkdir(parents=True, exist_ok=True)
        file_url = RAW + quote(lesson["file"])
        original = asset_dir / lesson["file"]
        fetch(file_url, original, args.offline)
        frames = extract_frames(original, asset_dir)
        path = Path("tutorials/drawing") / f'{lesson_id}-{lesson["slug"]}.md'
        (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
        source_url = f'{REPO}/blob/{COMMIT}/{quote(lesson["file"])}'
        figure_relative = f"../../{relative_asset_dir.as_posix()}"
        images = []
        for name, role, caption, derived in [
            (lesson["file"], "original", lesson["figure_reading"], False),
            ("keyframes.png", "keyframes", "原GIF按总时长0%、33%、66%、99%抽取的四帧，按左上、右上、左下、右下阅读；图外标注帧号和时间。", True),
            ("preview.png", "preview", "原GIF首帧静态预览；分步骤教程的首帧可能尚未显示成品。", True),
        ]:
            images.append({"path": (relative_asset_dir / name).as_posix(), "source_url": file_url,
                           "caption": caption, "role": role, "derived": derived,
                           "sha256": digest(asset_dir / name), "license": LICENSE,
                           "author": "Pedro Medeiros (Saint11)"})
        entry = {
            "id": lesson_id, "title": lesson["title"], "category": "drawing", "path": path.as_posix(),
            "source_url": source_url, "source_title": lesson["file"].rsplit(".", 1)[0],
            "author": "Pedro Medeiros (Saint11)", "license": LICENSE, "license_url": LICENSE_URL,
            "license_evidence_url": f"{REPO}/blob/{COMMIT}/README.md",
            "retrieved_at": DATE, "language": "zh-CN", "source_language": "en", "level": lesson["level"],
            "tags": lesson["tags"], "summary": lesson["summary"], "images": images,
            "content_mode": "translated-image-tutorial", "version": f"git:{COMMIT}",
            "prerequisites": lesson["prerequisites"], "learning_objectives": lesson["learning_objectives"],
            "source_sha256": digest(original), "source_bytes": original.stat().st_size,
            "original_animation": frames,
            "translation_scope": "Chinese explanatory paraphrase of the source image's main instructions, with original GIF retained; not an asserted complete OCR transcript.",
            "editorial_additions": ["practice exercise", "acceptance checklist", "scope and pitfalls", "cross-references", "static keyframe sheet"],
        }
        frontmatter = {key: value for key, value in entry.items() if key not in ["images", "original_animation"]}
        frontmatter["image_count"] = len(images)
        frontmatter["original_image"] = images[0]["path"]
        frontmatter["keyframes_image"] = images[1]["path"]
        frontmatter["visual_review"] = "Source first frame visually read; progressive keyframes additionally reviewed for house, wood, and cloud tutorials."
        markdown = "---\n" + yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False, width=1000) + "---\n\n"
        markdown += f'# {lesson_id} · {lesson["title"]}\n\n{lesson["summary"]}\n\n'
        markdown += "## 使用前先读\n\n"
        markdown += f'**适用层级：** {"入门" if lesson["level"] == "beginner" else "进阶"}。**前置：** ' + "、".join(lesson["prerequisites"]) + "。\n\n"
        markdown += "本篇依据原图中的主要说明和示例编写中文讲解，保留原始英文动态图；不是逐字全文OCR。原作者的经验性建议不自动等于所有项目的硬性规则。练习、验收与适用边界是整理者补充。\n\n"
        markdown += "## 学习目标\n\n" + "\n".join(f"- {objective}" for objective in lesson["learning_objectives"]) + "\n\n"
        markdown += f'## 原始图文教程\n\n![{lesson["title"]}：{lesson["figure_reading"]}]({figure_relative}/{lesson["file"]})\n\n'
        markdown += f'图1：Pedro Medeiros / Saint11 原始GIF，{frames["width"]}×{frames["height"]}，{frames["frames"]}帧，总时长{frames["duration_ms"] / 1000:.2f}秒。原文件未改像素或重编码。部分阅读器只显示首帧，请结合下面的静态图和说明。\n\n'
        markdown += f'![{lesson["title"]}的四个抽样关键帧，保留每帧原始像素，标注原始帧号和时间]({figure_relative}/keyframes.png)\n\n'
        markdown += "图2：整理者从原GIF按时间抽取的静态辅助图，阅读顺序为左上→右上→左下→右下。只选取四个时间点，并不代表完整动画或所有中间步骤；原始帧未缩放，标签加在图外。\n\n"
        markdown += f'## 图示读法\n\n{lesson["figure_reading"]}\n\n'
        markdown += f'## 关键概念\n\n{lesson["concepts"]}\n\n'
        markdown += "## 根据原图整理的步骤\n\n" + "\n\n".join(f"{i}. {step}" for i, step in enumerate(lesson["steps"], 1)) + "\n\n"
        markdown += f'## 实作练习（整理者补充）\n\n{lesson["exercise"]}\n\n'
        markdown += "## 验收清单（整理者补充）\n\n" + "\n".join(f"- [ ] {check}" for check in lesson["checks"]) + "\n\n"
        markdown += f'## 适用边界与常见误区（整理者补充）\n\n{lesson["pitfalls"]}\n\n'
        markdown += "## 来源与授权\n\n"
        markdown += f'- 原作者：**Pedro Medeiros（Saint11）**。\n- 原图：[固定版本的 {lesson["file"]}]({source_url})；[原始文件]({file_url})。\n'
        markdown += f'- 作者教程入口：[Pixel Art Tutorials](https://saint11.art/blog/pixel-art-tutorials/)。\n- 授权：[Creative Commons Attribution 4.0 International]({LICENSE_URL})。\n'
        markdown += f'- 授权证据：[仓库README固定版本]({REPO}/blob/{COMMIT}/README.md)；[本地证据副本](../../licenses/saint11-README.md)。\n'
        markdown += f'- 固定提交：`{COMMIT}`。收集日期：`{DATE}`。\n- 原始GIF SHA-256：`{entry["source_sha256"]}`。\n'
        markdown += "- 变更声明：原始GIF字节保留；新增中文解释性转述、练习、验收和适用范围说明；另从GIF抽帧生成静态辅助图。新增中文整理和派生图按CC BY 4.0提供，继续署名原作者并说明这些改动。\n"
        markdown += "- 使用边界：这份开放授权针对仓库中的教程图文；教程中出现的软件名称和商标仍属于其权利人。授权不表示原作者认可本中文整理。\n"
        (ROOT / path).write_text(markdown, encoding="utf-8")
        manifest.append(entry)
    (ROOT / "manifests").mkdir(exist_ok=True)
    (ROOT / "manifests/drawing.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    source_meta = {"repository": REPO, "commit": COMMIT, "license": LICENSE,
                   "license_url": LICENSE_URL, "evidence_url": f"{REPO}/blob/{COMMIT}/README.md",
                   "evidence_file": "licenses/saint11-README.md", "retrieved_at": DATE,
                   "evidence_sha256": digest(ROOT / "licenses/saint11-README.md")}
    (ROOT / "licenses/saint11-source.json").write_text(json.dumps(source_meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"tutorials": len(manifest), "original_gifs": len(manifest),
                      "keyframe_sheets": len(manifest), "preview_pngs": len(manifest),
                      "manifest": "manifests/drawing.json", "commit": COMMIT}, ensure_ascii=False))


if __name__ == "__main__":
    main()
