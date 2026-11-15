#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draw a transparent placement/circulation review overlay.

This writes a review aid, not a game asset. It does not score or approve art.
Unset required contract or scene-plan fields are refused; the script will not
guess widths, clearances, or typological elements.
--under only composites that overlay onto an existing picture. --prompt only
prints a clause from fields that are already filled.
Optional scene-plan joints are named in that clause for a human checklist.
They are not drawn, measured, or scored. Missing joints are skipped.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

# Review-only colours, documented in references/placement-baseline.md.
# Chosen to stay distinct from the camera overlay (cyan grid, yellow plumbs,
# magenta scale, white house wireframe).
PATH = (255, 148, 40, 150)
PATH_EDGE = (255, 148, 40, 230)
DOOR = (70, 200, 130, 90)
DOOR_EDGE = (70, 200, 130, 230)
STAND = (170, 110, 255, 220)
LANDMARK = (230, 72, 64, 230)
ELEMENT = (70, 150, 230, 220)
LABEL = (230, 230, 230, 255)
BG_DEMO = (28, 30, 34, 255)
FAIL = (220, 60, 60, 230)
OK = (90, 200, 110, 230)
WATER = (64, 110, 150, 180)
WALL = (200, 200, 210, 255)
ROAD = (168, 140, 96, 255)
GRASS = (62, 86, 58, 255)


def die(msg: str, code: int = 2) -> None:
    print("placement_baseline: " + msg, file=sys.stderr)
    raise SystemExit(code)


def _missing(value) -> bool:
    return value is None or value == "" or value == [] or value == {} or value == "UNDETERMINED"


def parse_size(text: str) -> tuple[int, int]:
    if "x" not in text.lower():
        die("size must look like 480x270")
    w, h = text.lower().split("x", 1)
    try:
        ww, hh = int(w), int(h)
    except ValueError:
        die("size must be integers, like 480x270")
    if ww < 16 or hh < 16:
        die("size is too small to draw a useful overlay")
    return ww, hh


def load_json(path: Path, label: str) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        die(f"cannot read {label}: {exc}")
    if not isinstance(data, dict):
        die(f"{label} must be a JSON object")
    return data


def load_layout(bible_path: Path | None) -> tuple[dict, dict]:
    """Return (layout, projection) from an art bible. Layout may be empty."""
    if bible_path is None:
        return {}, {}
    data = load_json(bible_path, "art bible")
    layout = data.get("layout")
    if layout is None:
        die("art bible has no layout object; fill the layout contract first")
    if not isinstance(layout, dict):
        die("art bible layout must be an object")
    proj = data.get("projection") if isinstance(data.get("projection"), dict) else {}
    return layout, proj


def load_plan(plan_path: Path | None) -> dict:
    if plan_path is None:
        return {}
    plan = load_json(plan_path, "scene plan")
    return plan


def tiles_value(value) -> list[int] | None:
    if _missing(value):
        return None
    if isinstance(value, (int, float)) and value > 0:
        n = int(value)
        return [n, n]
    if isinstance(value, (list, tuple)) and len(value) == 2:
        try:
            a, b = int(value[0]), int(value[1])
        except (TypeError, ValueError):
            return None
        if a > 0 and b > 0:
            return [a, b]
    return None


def as_int(value) -> int | None:
    if isinstance(value, bool) or _missing(value):
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0:
        return int(value)
    return None


def resolve_unit(layout: dict, proj: dict, args: argparse.Namespace) -> int | None:
    unit = args.unit
    if not isinstance(unit, int) or unit < 4:
        unit = layout.get("grid_unit_px", layout.get("grid_unit"))
    if not isinstance(unit, int) or unit < 4:
        baseline = proj.get("baseline") if isinstance(proj.get("baseline"), dict) else {}
        unit = baseline.get("grid_unit_px")
    if isinstance(unit, int) and unit >= 4:
        return unit
    return None


def resolve_size(layout: dict, proj: dict, args: argparse.Namespace) -> tuple[int, int] | None:
    if args.size:
        return parse_size(args.size)
    for src in (layout, proj.get("baseline") if isinstance(proj.get("baseline"), dict) else {}):
        overlay = src.get("overlay_size") if isinstance(src, dict) else None
        if isinstance(overlay, list) and len(overlay) == 2 and all(isinstance(x, int) and x > 0 for x in overlay):
            return (overlay[0], overlay[1])
    return None


def require_plan_fields(plan: dict) -> None:
    if not plan:
        die("scene plan is unset; pass --plan with scene_type, required typological elements, and a primary path")
    if _missing(plan.get("scene_type")):
        die("scene_type is unset; fill the scene plan, do not guess a typological kind")
    elements = plan.get("required_elements", plan.get("required_typological_elements"))
    if _missing(elements):
        die("required typological elements are unset; fill required_elements on the scene plan")
    path = plan.get("primary_path")
    if _missing(path):
        die("primary_path is unset; declare entrance, route, and destination")
    if isinstance(path, dict):
        if _missing(path.get("entrance")) or _missing(path.get("destination")):
            die("primary_path must declare entrance and destination")
        if _missing(path.get("polyline")) and _missing(path.get("route_polyline")):
            die("primary_path.polyline is unset; give a centerline in logical px or tiles")


def path_records(plan: dict) -> list[dict]:
    recs = []
    primary = plan.get("primary_path")
    if isinstance(primary, dict):
        recs.append(dict(primary, name=primary.get("name") or "primary", is_primary=True))
    extra = plan.get("paths")
    if isinstance(extra, list):
        for i, item in enumerate(extra):
            if isinstance(item, dict):
                recs.append(dict(item, name=item.get("name") or f"path-{i + 1}", is_primary=False))
    return recs


def joint_labels(plan: dict) -> list[str]:
    """Names of declared joints. Not a measurement and not a pass or fail."""
    raw = plan.get("joints") if isinstance(plan, dict) else None
    if not isinstance(raw, list):
        return []
    labels = []
    for item in raw:
        if isinstance(item, str) and not _missing(item):
            labels.append(item)
            continue
        if not isinstance(item, dict) or _missing(item.get("name")):
            continue
        label = str(item["name"])
        src = item.get("from")
        dst = item.get("to")
        if not _missing(src) and not _missing(dst):
            label = f"{label}（{src} → {dst}）"
        labels.append(label)
    return labels


def element_records(plan: dict) -> list[dict]:
    raw = plan.get("required_elements", plan.get("required_typological_elements")) or []
    out = []
    if isinstance(raw, list):
        for i, item in enumerate(raw):
            if isinstance(item, str) and not _missing(item):
                out.append({"name": item})
            elif isinstance(item, dict) and not _missing(item.get("name") or item.get("id")):
                rec = dict(item)
                rec["name"] = item.get("name") or item.get("id")
                out.append(rec)
    return out


def to_px(pt, unit: int, units: str) -> tuple[int, int]:
    x, y = pt[0], pt[1]
    if units == "tiles":
        return int(round(float(x) * unit)), int(round(float(y) * unit))
    return int(round(float(x))), int(round(float(y)))


def polyline_px(rec: dict, unit: int) -> list[tuple[int, int]]:
    pts = rec.get("polyline") or rec.get("route_polyline") or []
    units = str(rec.get("units") or "px").lower()
    if units in {"tile", "tiles"}:
        units = "tiles"
    else:
        units = "px"
    out = []
    for pt in pts:
        if isinstance(pt, (list, tuple)) and len(pt) >= 2:
            out.append(to_px(pt, unit, units))
    return out


def width_px(rec: dict, layout: dict, unit: int) -> int | None:
    direct = rec.get("width_px")
    if isinstance(direct, int) and direct > 0:
        return direct
    tiles = rec.get("width_tiles")
    if tiles is None:
        kind = rec.get("kind") or rec.get("width_kind") or ("main" if rec.get("is_primary") else None)
        widths = layout.get("path_widths") if isinstance(layout.get("path_widths"), dict) else {}
        if kind in ("bridge", "steps", "bridge_or_steps", "bridge-or-steps"):
            tiles = widths.get("bridge_or_steps")
        elif kind:
            tiles = widths.get(kind)
        if tiles is None and rec.get("is_primary"):
            tiles = widths.get("main")
    n = as_int(tiles)
    if n:
        return n * unit
    return None


def _line(draw: ImageDraw.ImageDraw, a, b, color, width=1):
    draw.line([a, b], fill=color, width=width)


def constant_width_strip(points: list[tuple[int, int]], width: int) -> list[tuple[int, int]]:
    """Offset a centerline left and right by width/2. Edges stay parallel; no taper."""
    if len(points) < 2 or width < 1:
        return []
    half = width / 2.0
    left, right = [], []

    def normal(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        if length == 0:
            return (0.0, 0.0)
        return (-dy / length, dx / length)

    for i, p in enumerate(points):
        if i == 0:
            nx, ny = normal(points[0], points[1])
        elif i == len(points) - 1:
            nx, ny = normal(points[-2], points[-1])
        else:
            n1 = normal(points[i - 1], p)
            n2 = normal(p, points[i + 1])
            nx, ny = n1[0] + n2[0], n1[1] + n2[1]
            length = math.hypot(nx, ny)
            if length == 0:
                nx, ny = n2
            else:
                # Keep a constant half-width (miter, but cap extreme joins).
                nx, ny = nx / length, ny / length
                dot = max(-1.0, min(1.0, n1[0] * nx + n1[1] * ny))
                scale = 1.0 / max(0.4, abs(dot) if dot else 0.4)
                nx, ny = nx * min(scale, 2.0), ny * min(scale, 2.0)
        left.append((int(round(p[0] + nx * half)), int(round(p[1] + ny * half))))
        right.append((int(round(p[0] - nx * half)), int(round(p[1] - ny * half))))
    return left + right[::-1]


def draw_corridors(draw, plan: dict, layout: dict, unit: int):
    for rec in path_records(plan):
        pts = polyline_px(rec, unit)
        width = width_px(rec, layout, unit)
        if len(pts) < 2 or not width:
            continue
        poly = constant_width_strip(pts, width)
        if len(poly) >= 3:
            draw.polygon(poly, fill=PATH, outline=PATH_EDGE)
        # Centerline for readability; same constant width, not a taper cue.
        draw.line(pts, fill=PATH_EDGE, width=1)


def door_clearance_box(door: dict, layout: dict, unit: int) -> tuple[int, int, int, int] | None:
    rect = door.get("clearance_rect") or door.get("clearance")
    units = str(door.get("units") or "px").lower()
    if units in {"tile", "tiles"}:
        units = "tiles"
    else:
        units = "px"
    if isinstance(rect, (list, tuple)) and len(rect) == 4:
        x, y, w, h = rect
        if units == "tiles":
            x, y, w, h = x * unit, y * unit, w * unit, h * unit
        return int(x), int(y), int(x + w), int(y + h)
    leaf = door.get("rect") or door.get("door_rect")
    if not (isinstance(leaf, (list, tuple)) and len(leaf) == 4):
        return None
    x, y, w, h = leaf
    if units == "tiles":
        x, y, w, h = x * unit, y * unit, w * unit, h * unit
    x, y, w, h = int(x), int(y), int(w), int(h)
    kind = door.get("kind") or door.get("clearance_kind") or "residential"
    clearances = layout.get("door_clearances") if isinstance(layout.get("door_clearances"), dict) else {}
    tiles = tiles_value(clearances.get(kind)) or tiles_value(door.get("clearance_tiles"))
    if not tiles:
        return None
    cw, ch = tiles[0] * unit, tiles[1] * unit
    facing = str(door.get("facing") or "south").lower()
    if facing in {"s", "south", "down"}:
        return x + w // 2 - cw // 2, y + h, x + w // 2 - cw // 2 + cw, y + h + ch
    if facing in {"n", "north", "up"}:
        return x + w // 2 - cw // 2, y - ch, x + w // 2 - cw // 2 + cw, y
    if facing in {"e", "east", "right"}:
        return x + w, y + h // 2 - ch // 2, x + w + cw, y + h // 2 - ch // 2 + ch
    if facing in {"w", "west", "left"}:
        return x - cw, y + h // 2 - ch // 2, x, y + h // 2 - ch // 2 + ch
    return x + w // 2 - cw // 2, y + h, x + w // 2 - cw // 2 + cw, y + h + ch


def draw_doors(draw, plan: dict, layout: dict, unit: int):
    doors = plan.get("doors") or plan.get("door_rects") or []
    if not isinstance(doors, list):
        return
    for door in doors:
        if not isinstance(door, dict):
            continue
        box = door_clearance_box(door, layout, unit)
        if not box:
            continue
        x0, y0, x1, y1 = box
        draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=DOOR, outline=DOOR_EDGE)


def footprint_px(layout: dict, unit: int) -> tuple[int, int]:
    tiles = tiles_value(layout.get("character_footprint_tiles"))
    if not tiles:
        tiles = [1, 1]
    return tiles[0] * unit, tiles[1] * unit


def point_xy(item: dict, unit: int) -> tuple[int, int] | None:
    units = str(item.get("units") or "px").lower()
    if units in {"tile", "tiles"}:
        units = "tiles"
    else:
        units = "px"
    if "xy" in item and isinstance(item["xy"], (list, tuple)) and len(item["xy"]) >= 2:
        return to_px(item["xy"], unit, units)
    if "x" in item and "y" in item and not _missing(item.get("x")) and not _missing(item.get("y")):
        return to_px((item["x"], item["y"]), unit, units)
    return None


def draw_stands(draw, plan: dict, layout: dict, unit: int):
    stands = plan.get("stand_points") or plan.get("standing_spots") or []
    if not isinstance(stands, list):
        return
    fw, fh = footprint_px(layout, unit)
    for item in stands:
        if not isinstance(item, dict):
            continue
        pt = point_xy(item, unit)
        if not pt:
            continue
        x, y = pt
        x0, y0 = x - fw // 2, y - fh // 2
        draw.ellipse([x0, y0, x0 + fw - 1, y0 + fh - 1], outline=STAND, width=2)
        # A small cross so the reserved stand tile stays readable at 1x.
        _line(draw, (x - fw // 2, y), (x + fw // 2 - 1, y), STAND)
        _line(draw, (x, y - fh // 2), (x, y + fh // 2 - 1), STAND)


def draw_landmarks(draw, plan: dict, unit: int):
    marks = plan.get("landmarks") or plan.get("weenies") or []
    if not isinstance(marks, list):
        return
    r = max(4, unit // 2)
    for item in marks:
        if not isinstance(item, dict):
            continue
        pt = point_xy(item, unit)
        if not pt:
            continue
        x, y = pt
        draw.polygon(
            [(x, y - r), (x + r, y), (x, y + r), (x - r, y)],
            outline=LANDMARK,
        )
        _line(draw, (x, y - r - 2), (x, y + r + 2), LANDMARK)
        _line(draw, (x - r - 2, y), (x + r + 2, y), LANDMARK)


def draw_elements(draw, plan: dict, unit: int):
    for item in element_records(plan):
        rect = item.get("rect")
        units = str(item.get("units") or "px").lower()
        if units in {"tile", "tiles"}:
            units = "tiles"
        else:
            units = "px"
        if isinstance(rect, (list, tuple)) and len(rect) == 4:
            x, y, w, h = rect
            if units == "tiles":
                x, y, w, h = x * unit, y * unit, w * unit, h * unit
            draw.rectangle([int(x), int(y), int(x + w) - 1, int(y + h) - 1], outline=ELEMENT, width=1)
            continue
        pt = point_xy(item, unit)
        if pt:
            x, y = pt
            s = max(6, unit)
            draw.rectangle([x - s // 2, y - s // 2, x + s // 2, y + s // 2], outline=ELEMENT, width=1)


def render(cfg: dict, *, opaque_bg=False) -> Image.Image:
    w, h = cfg["size"]
    bg = BG_DEMO if opaque_bg else (0, 0, 0, 0)
    im = Image.new("RGBA", (w, h), bg)
    draw = ImageDraw.Draw(im)
    layout, plan, unit = cfg["layout"], cfg["plan"], cfg["unit"]
    draw_corridors(draw, plan, layout, unit)
    draw_doors(draw, plan, layout, unit)
    draw_stands(draw, plan, layout, unit)
    draw_landmarks(draw, plan, unit)
    draw_elements(draw, plan, unit)
    return im


def format_prompt(layout: dict, plan: dict, args: argparse.Namespace, proj: dict | None = None) -> str:
    """Paste-ready placement clause. Null fields are omitted, never invented."""
    proj = proj or {}
    if args.plan and _missing((plan or {}).get("scene_type")):
        die("scene_type is unset; pass a filled scene plan, do not guess a typological kind")
    if not layout and not plan:
        die("layout contract is unset; fill the art bible layout or pass --plan")

    parts: list[str] = []

    def add(label, value):
        if _missing(value):
            return
        if isinstance(value, bool):
            text = "是" if value else "否"
        elif isinstance(value, list):
            if value and all(not isinstance(v, (dict, list)) for v in value):
                text = "×".join(str(v) for v in value) if label.endswith("占地") or "净空" in label or "格" in label and len(value) == 2 and all(isinstance(v, (int, float)) for v in value) else "、".join(str(v) for v in value if not _missing(v))
            else:
                text = "、".join(str(v) for v in value if not _missing(v))
            if not text:
                return
        else:
            text = str(value)
        parts.append(f"{label}：{text}")

    unit = resolve_unit(layout, proj, args)
    size = resolve_size(layout, proj, args)
    bits = []
    if size:
        bits.append(f"{size[0]}×{size[1]}")
    if unit:
        bits.append(f"格宽 {unit} 逻辑像素")
    if bits:
        parts.append("基准：" + "，".join(bits))

    fp = tiles_value(layout.get("character_footprint_tiles"))
    if fp:
        parts.append(f"角色占地：{fp[0]}×{fp[1]} 格")

    widths = layout.get("path_widths") if isinstance(layout.get("path_widths"), dict) else {}
    if not _missing(widths.get("main")):
        parts.append(f"主路宽：{widths['main']} 格")
    if not _missing(widths.get("alley")):
        parts.append(f"巷宽：{widths['alley']} 格")
    if not _missing(widths.get("bridge_or_steps")):
        parts.append(f"桥或石阶宽：{widths['bridge_or_steps']} 格")

    clears = layout.get("door_clearances") if isinstance(layout.get("door_clearances"), dict) else {}
    door_bits = []
    for key, label in (("residential", "住宅"), ("public", "公共")):
        tiles = tiles_value(clears.get(key))
        if tiles:
            door_bits.append(f"{label} {tiles[0]}×{tiles[1]} 格")
        elif not _missing(clears.get(key)) and not tiles:
            door_bits.append(f"{label} {clears[key]}")
    if door_bits:
        parts.append("门前净空：" + "，".join(door_bits))

    add("建筑间距", None if _missing(layout.get("building_gap")) else f"{layout.get('building_gap')} 格")
    add("建筑距地图边", None if _missing(layout.get("building_to_map_edge")) else f"{layout.get('building_to_map_edge')} 格")
    if not _missing(layout.get("building_to_water")):
        water = f"{layout.get('building_to_water')} 格"
        exc = layout.get("building_to_water_exception")
        if not _missing(exc):
            water += "，" + str(exc)
        else:
            water += "，埠头、码头、桥梁须有石阶或护栏"
        parts.append("建筑距水：" + water)
    add("互动物间距", None if _missing(layout.get("interact_gap")) else f"{layout.get('interact_gap')} 格")
    if layout.get("reserved_stand_tile") is True:
        parts.append("留出站立格：是")
    elif layout.get("reserved_stand_tile") is False:
        parts.append("留出站立格：否")

    cluster = layout.get("cluster") if isinstance(layout.get("cluster"), dict) else {}
    cluster_bits = []
    if not _missing(cluster.get("size")):
        cluster_bits.append(f"最多 {cluster['size']} 件")
    if not _missing(cluster.get("radius")):
        cluster_bits.append(f"半径 {cluster['radius']} 格")
    if not _missing(cluster.get("gap")):
        cluster_bits.append(f"簇距 {cluster['gap']} 格")
    if cluster_bits:
        parts.append("簇：" + "，".join(cluster_bits))

    if plan:
        add("场景类型", plan.get("scene_type"))
        names = [e["name"] for e in element_records(plan)]
        if names:
            parts.append("必有类型要素：" + "、".join(names))
        primary = plan.get("primary_path") if isinstance(plan.get("primary_path"), dict) else {}
        if primary:
            e, r, d = primary.get("entrance"), primary.get("route"), primary.get("destination")
            segs = [str(x) for x in (e, r, d) if not _missing(x)]
            if segs:
                parts.append("主路：" + " → ".join(segs))
        marks = []
        for item in (plan.get("landmarks") or plan.get("weenies") or []):
            if isinstance(item, dict) and not _missing(item.get("name")):
                marks.append(str(item["name"]))
            elif isinstance(item, str) and not _missing(item):
                marks.append(item)
        if marks:
            parts.append("地标：" + "、".join(marks))
        stands = []
        for item in (plan.get("stand_points") or plan.get("standing_spots") or []):
            if isinstance(item, dict) and not _missing(item.get("name")):
                stands.append(str(item["name"]))
        if stands:
            parts.append("站立点：" + "、".join(stands))
        joints = joint_labels(plan)
        if joints:
            parts.append("接头：" + "、".join(joints))

    if not parts:
        die("layout contract has no filled fields; unset values are not guessed")
    return "摆放：" + "。".join(parts) + "。"


def uniform_integer_factor(small: tuple[int, int], large: tuple[int, int]) -> int | None:
    """Return n>=1 when large is exactly n times small on both axes."""
    sw, sh = small
    lw, lh = large
    if sw <= 0 or sh <= 0 or lw <= 0 or lh <= 0:
        return None
    if lw % sw or lh % sh:
        return None
    sx, sy = lw // sw, lh // sh
    if sx == sy and sx >= 1:
        return sx
    return None


def composite_under(overlay: Image.Image, under_path: Path) -> Image.Image:
    """Lay the transparent overlay over an existing picture. Review image only.

    Same size composites directly. A uniform integer multiple is scaled with
    nearest-neighbor and then composited. Any other size is refused. Parts
    smaller than the canvas are not given an automatic position.
    """
    try:
        with Image.open(under_path) as src:
            under = src.convert("RGBA")
    except (OSError, ValueError) as exc:
        die(f"cannot read --under image: {exc}")
    ow, oh = overlay.size
    uw, uh = under.size
    if uw < 1 or uh < 1:
        die("--under image has no pixels")
    if (uw, uh) == (ow, oh):
        base, layer = under, overlay
    else:
        grow_overlay = uniform_integer_factor((ow, oh), (uw, uh))
        grow_under = uniform_integer_factor((uw, uh), (ow, oh))
        if grow_overlay and grow_overlay > 1:
            layer = overlay.resize((uw, uh), Image.Resampling.NEAREST)
            base = under
        elif grow_under and grow_under > 1:
            base = under.resize((ow, oh), Image.Resampling.NEAREST)
            layer = overlay
        else:
            die(
                "--under is %dx%d and the overlay is %dx%d. "
                "Sizes must match, or one side must be a uniform integer multiple of the other. "
                "Refusing to stretch or bilinear-scale. "
                "A part smaller than the canvas is not auto-placed: "
                "lay it onto a same-size canvas first, then overlay."
                % (uw, uh, ow, oh)
            )
    out = base.copy()
    out.alpha_composite(layer)
    return out


def walkable_report(mask_path: Path, plan: dict, layout: dict, unit: int, size: tuple[int, int]) -> dict:
    """Flood-fill a walkable mask and report reachability as data, not a style score."""
    try:
        with Image.open(mask_path) as src:
            mask_im = src.convert("RGBA")
    except (OSError, ValueError) as exc:
        die(f"cannot read --walkable mask: {exc}")
    if mask_im.size != size:
        factor = uniform_integer_factor(mask_im.size, size) or uniform_integer_factor(size, mask_im.size)
        if factor and mask_im.size[0] * factor == size[0]:
            mask_im = mask_im.resize(size, Image.Resampling.NEAREST)
        elif factor and size[0] * factor == mask_im.size[0]:
            # shrink only by integer nearest-neighbor for the data check
            mask_im = mask_im.resize(size, Image.Resampling.NEAREST)
        else:
            die(
                "--walkable is %dx%d and the overlay is %dx%d; sizes must match or be a uniform integer multiple"
                % (mask_im.size[0], mask_im.size[1], size[0], size[1])
            )
    pix = mask_im.load()
    w, h = mask_im.size

    def is_walk(x, y):
        if x < 0 or y < 0 or x >= w or y >= h:
            return False
        r, g, b, a = pix[x, y]
        return a > 127 and (r + g + b) > 40

    def neighbors(x, y):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yield x + dx, y + dy

    seeds = []
    primary = plan.get("primary_path") if isinstance(plan.get("primary_path"), dict) else {}
    pts = polyline_px(primary, unit) if primary else []
    if pts:
        seeds.append(("entrance", pts[0]))
    goals = []
    if len(pts) >= 2:
        goals.append(("destination", pts[-1]))
    for door in plan.get("doors") or []:
        if isinstance(door, dict):
            box = door_clearance_box(door, layout, unit)
            if box:
                cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
                goals.append((str(door.get("name") or "door"), (cx, cy)))
    for item in plan.get("stand_points") or plan.get("standing_spots") or []:
        if isinstance(item, dict):
            pt = point_xy(item, unit)
            if pt:
                goals.append((str(item.get("name") or "stand"), pt))
    for item in plan.get("landmarks") or []:
        if isinstance(item, dict):
            pt = point_xy(item, unit)
            if pt:
                goals.append((str(item.get("name") or "landmark"), pt))

    visited = set()
    stack = []
    used_seed = None
    for name, (sx, sy) in seeds:
        if is_walk(sx, sy):
            stack.append((sx, sy))
            used_seed = (name, (sx, sy))
            break
        # If the exact centerline pixel is drawn on an edge, search a small window.
        found = None
        for rad in range(1, max(2, unit // 2 + 1)):
            for y in range(sy - rad, sy + rad + 1):
                for x in range(sx - rad, sx + rad + 1):
                    if is_walk(x, y):
                        found = (x, y)
                        break
                if found:
                    break
            if found:
                break
        if found:
            stack.append(found)
            used_seed = (name, found)
            break

    while stack:
        x, y = stack.pop()
        if (x, y) in visited or not is_walk(x, y):
            continue
        visited.add((x, y))
        for nx, ny in neighbors(x, y):
            if (nx, ny) not in visited:
                stack.append((nx, ny))

    def reachable(pt):
        x, y = pt
        if (x, y) in visited:
            return True
        for rad in range(0, max(2, unit // 2 + 1)):
            for yy in range(y - rad, y + rad + 1):
                for xx in range(x - rad, x + rad + 1):
                    if (xx, yy) in visited:
                        return True
        return False

    rec = {
        "start": None if not used_seed else {"name": used_seed[0], "xy": list(used_seed[1])},
        "walkable_pixels": len(visited),
        "reachable": [],
        "unreachable": [],
    }
    if used_seed is None:
        rec["note"] = "no walkable seed pixel was found at the declared entrance"
    for name, pt in goals:
        entry = {"name": name, "xy": list(pt)}
        if used_seed is not None and reachable(pt):
            rec["reachable"].append(entry)
        else:
            rec["unreachable"].append(entry)
    return rec


def print_walkable(report: dict) -> None:
    start = report.get("start")
    if start:
        print("walkable start %s at %d,%d (%d pixels reached)" % (
            start["name"], start["xy"][0], start["xy"][1], report.get("walkable_pixels", 0)
        ))
    else:
        print("walkable: " + (report.get("note") or "no start"))
    if report["reachable"]:
        print("reachable: " + ", ".join("%s (%d,%d)" % (g["name"], g["xy"][0], g["xy"][1]) for g in report["reachable"]))
    if report["unreachable"]:
        print("unreachable: " + ", ".join("%s (%d,%d)" % (g["name"], g["xy"][0], g["xy"][1]) for g in report["unreachable"]))


def render_demo(_cfg: dict | None = None) -> Image.Image:
    """Side-by-side teaching plate: pass layout vs blocked/missing typological fail."""
    w, h = 640, 360
    im = Image.new("RGBA", (w, h), BG_DEMO)
    draw = ImageDraw.Draw(im)
    mid = w // 2
    _line(draw, (mid, 0), (mid, h - 1), (70, 72, 80, 255), 2)

    def panel(x0, x1, fail: bool, title: str, color):
        draw.rectangle([x0, 0, x1, 40], fill=(22, 24, 28, 255))
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
            draw.text((x0 + 16, 12), title, fill=color, font=font)
        except Exception:
            draw.text((x0 + 16, 12), title, fill=color)
        # Ground
        draw.rectangle([x0 + 16, 48, x1 - 16, h - 24], fill=GRASS)
        # Horizontal water band on the fail side only (door into water).
        if fail:
            draw.rectangle([x0 + 16, 200, x1 - 16, 248], fill=WATER)
        # Road: constant width on the pass side; necks on the fail side.
        top_y, bot_y = 64, h - 40
        cx = (x0 + x1) // 2
        if fail:
            # Incorrect circulation: width shrinks, then the path hits a wall.
            pts = [
                (cx - 50, bot_y),
                (cx + 50, bot_y),
                (cx + 16, 200),
                (cx - 16, 200),
            ]
            draw.polygon(pts, fill=ROAD)
            # A solid wall with no gate, blocking the remaining route.
            draw.rectangle([x0 + 24, 150, x1 - 24, 172], fill=(120, 118, 122, 255), outline=FAIL)
        else:
            half = 24  # 48 px road, constant
            pts = [
                (cx - half, bot_y),
                (cx + half, bot_y),
                (cx + half, top_y),
                (cx - half, top_y),
            ]
            draw.polygon(pts, fill=ROAD, outline=OK)
            # Boundary wall with a 48 px gate opening aligned to the road.
            draw.rectangle([x0 + 24, 150, cx - half, 172], fill=(186, 186, 190, 255), outline=WALL)
            draw.rectangle([cx + half, 150, x1 - 24, 172], fill=(186, 186, 190, 255), outline=WALL)
            # Simple gate posts, not a game asset.
            draw.rectangle([cx - half - 6, 132, cx - half, 172], fill=(90, 90, 96, 255))
            draw.rectangle([cx + half, 132, cx + half + 6, 172], fill=(90, 90, 96, 255))
            # Side building + door clearance south of the door, empty.
            bx0, by0, bx1, by1 = x0 + 36, 96, x0 + 84, 144
            draw.rectangle([bx0, by0, bx1, by1], outline=WALL)
            draw.rectangle([bx0 + 16, by1 - 18, bx0 + 32, by1], outline=WALL)
            # 3x3 tile clearance (here 24 px demo cells would be large; use 24x24 readable box)
            draw.rectangle([bx0 + 4, by1, bx1 - 4, by1 + 28], outline=DOOR_EDGE)
            # Weenie / stand in the courtyard
            wx, wy = cx, 100
            draw.polygon([(wx, wy - 10), (wx + 8, wy), (wx, wy + 10), (wx - 8, wy)], outline=LANDMARK)
            draw.ellipse([wx - 8, wy + 14, wx + 8, wy + 30], outline=STAND)
        # Overlay a constant-width corridor on the pass path only, as the review aid.
        if not fail:
            overlay = Image.new("RGBA", (x1 - x0, h), (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            poly = constant_width_strip([(cx - x0, bot_y), (cx - x0, top_y)], 48)
            if poly:
                od.polygon(poly, fill=PATH, outline=PATH_EDGE)
            im.alpha_composite(overlay, (x0, 0))
        else:
            # A house door that opens into the water band, no clearance.
            dx0 = x0 + 40
            draw.rectangle([dx0, 168, dx0 + 36, 204], outline=(200, 200, 210, 255))
            draw.rectangle([dx0 + 12, 186, dx0 + 24, 204], fill=FAIL)

    panel(0, mid, False, "PASS  even-width path, door clear, gate", OK)
    panel(mid, w, True, "FAIL  necked path, door into water, no gate", FAIL)
    return im


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bible", type=Path, help="art-bible.json containing a layout contract")
    p.add_argument("--plan", type=Path, help="scene-plan JSON (scene type, typological elements, paths, doors, stands, landmarks)")
    p.add_argument("--size", help="WxH logical pixels, e.g. 480x270")
    p.add_argument("--unit", type=int, help="grid unit in logical pixels")
    p.add_argument("--out", type=Path, help="write a review overlay or comparison image; omitted for --prompt text only")
    p.add_argument("--under", type=Path, help="composite the transparent overlay onto this source or scene image (review comparison only; nearest-neighbor integer scale)")
    p.add_argument("--prompt", "--print-prompt", action="store_true", help="print a paste-ready placement clause from filled fields; does not draw an image unless --out is also set")
    p.add_argument("--demo", action="store_true", help="draw a pass/fail teaching plate instead of a transparent overlay")
    p.add_argument("--walkable", type=Path, help="optional walkable mask; flood-fill and report reachability as data, not a style score")
    p.add_argument("--json", action="store_true", dest="as_json", help="print the optional walkable report as JSON")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.demo and (args.under or args.prompt or args.walkable):
        die("--demo cannot be combined with --under, --prompt, or --walkable")
    if args.demo and not args.out:
        die("pass --out to write the teaching plate")
    if args.under and not args.out:
        die("--under needs --out; the comparison image is not written without it")
    if not args.out and not args.prompt and not args.demo and not args.walkable:
        die("pass --out to write a review overlay, --prompt to print a placement clause, or --walkable to report reachability")

    clause = None
    im = None
    report = None
    if args.demo:
        im = render_demo()
    else:
        if not args.bible and not args.plan:
            die("pass --bible and/or --plan; the script will not invent a layout contract")
        layout, proj = load_layout(args.bible) if args.bible else ({}, {})
        plan = load_plan(args.plan)
        if args.out or args.walkable:
            require_plan_fields(plan if plan else {})
            size = resolve_size(layout, proj, args)
            unit = resolve_unit(layout, proj, args)
            if not size:
                die("overlay size is unset; pass --size WxH or layout.overlay_size")
            if not unit:
                die("grid unit is unset or too small; pass --unit, layout.grid_unit_px, or projection.baseline.grid_unit_px")
            cfg = {"layout": layout, "plan": plan, "size": size, "unit": unit}
            if args.out:
                im = render(cfg, opaque_bg=False)
                if args.under:
                    im = composite_under(im, args.under.expanduser())
            if args.walkable:
                report = walkable_report(args.walkable.expanduser(), plan, layout, unit, size)
        if args.prompt:
            # Prompt may run with a bible alone (filled layout fields) or with a plan.
            if args.plan:
                if _missing(plan.get("scene_type")):
                    die("scene_type is unset; fill the scene plan, do not guess a typological kind")
            clause = format_prompt(layout, plan, args, proj)

    if im is not None:
        args.out = args.out.expanduser()
        args.out.parent.mkdir(parents=True, exist_ok=True)
        im.save(args.out)
        print(f"wrote {args.out} {im.size[0]}x{im.size[1]} {im.mode}")
    if clause:
        print(clause)
    if report is not None:
        if args.as_json:
            print(json.dumps(report, ensure_ascii=False))
        else:
            print_walkable(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
