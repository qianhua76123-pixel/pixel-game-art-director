#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draw a transparent camera/perspective baseline overlay for visual review.

This writes a review aid, not a game asset. It does not score or approve art.
Unspecified projection fields are refused; the script will not invent a camera.
--under only composites that overlay onto an existing picture. --prompt only
prints a clause from fields that are already filled.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

KINDS = {
    "orthographic-front-top": "orthographic-front-top",
    "orthographic-34": "orthographic-front-top",
    "front-top-down": "orthographic-front-top",
    "orthographic-top": "orthographic-top",
    "top-down": "orthographic-top",
    "isometric": "isometric",
    "iso": "isometric",
    "perspective-1p": "perspective-1p",
    "one-point": "perspective-1p",
    "perspective-2p": "perspective-2p",
    "two-point": "perspective-2p",
}

# Review-only colours, documented in references/camera-baseline.md
GRID = (80, 200, 220, 200)
PLUMB = (240, 220, 80, 210)
SCALE = (240, 80, 180, 230)
WIRE = (245, 245, 245, 220)
FAIL = (220, 60, 60, 230)
OK = (90, 200, 110, 230)
LABEL = (230, 230, 230, 255)
BG_DEMO = (28, 30, 34, 255)


def die(msg: str, code: int = 2) -> None:
    print("camera_baseline: " + msg, file=sys.stderr)
    raise SystemExit(code)


def parse_size(text: str) -> tuple[int, int]:
    if "x" not in text.lower():
        die("size must look like 480x270")
    w, h = text.lower().split("x", 1)
    try:
        ww, hh = int(w), int(h)
    except ValueError:
        die("size must be integers, like 480x270")
    if ww < 16 or hh < 16:
        die("size is too small to draw a useful baseline")
    return ww, hh


def load_projection(bible_path: Path | None) -> dict:
    if bible_path is None:
        return {}
    try:
        data = json.loads(bible_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        die(f"cannot read art bible: {exc}")
    proj = data.get("projection")
    if not isinstance(proj, dict):
        die("art bible has no projection object")
    return proj


def resolve(proj: dict, args: argparse.Namespace) -> dict:
    kind_raw = args.kind or proj.get("kind")
    if not kind_raw or kind_raw in (None, "", "UNDETERMINED"):
        die("projection.kind is unset; pass --kind or fill the art bible")
    kind = KINDS.get(str(kind_raw).strip().lower())
    if not kind:
        die("unknown kind %r; expected one of: %s" % (kind_raw, ", ".join(sorted(set(KINDS.values())))))

    baseline = proj.get("baseline") if isinstance(proj.get("baseline"), dict) else {}
    size = None
    if args.size:
        size = parse_size(args.size)
    else:
        overlay = baseline.get("overlay_size")
        if isinstance(overlay, list) and len(overlay) == 2 and all(isinstance(x, int) and x for x in overlay):
            size = (overlay[0], overlay[1])
    if not size:
        die("overlay size is unset; pass --size WxH or baseline.overlay_size")

    unit = args.unit or baseline.get("grid_unit_px")
    if not isinstance(unit, int) or unit < 4:
        die("grid unit is unset or too small; pass --unit or baseline.grid_unit_px")

    char_h = args.character_height
    if char_h is None:
        char_h = baseline.get("character_height_px")
    storey = baseline.get("storey_height_px") if args.storey_height is None else args.storey_height

    vanishing = proj.get("vanishing")
    if kind.startswith("perspective"):
        if vanishing in (None, "", "none", "UNDETERMINED") and not args.allow_implied_vanishing:
            die("%s requires projection.vanishing to be set (not none)" % kind)
    else:
        # Orthographic / isometric: vanishing must be none if specified
        if vanishing not in (None, "", "none", "UNDETERMINED") and str(vanishing).lower() not in {"none", "null"}:
            die("kind %s cannot be combined with vanishing=%r" % (kind, vanishing))

    return {
        "kind": kind,
        "size": size,
        "unit": unit,
        "character_height_px": char_h if isinstance(char_h, int) and char_h > 0 else None,
        "storey_height_px": storey if isinstance(storey, int) and storey > 0 else None,
        "front_to_top_ratio": proj.get("front_to_top_ratio"),
        "vanishing": vanishing,
    }


def _line(draw: ImageDraw.ImageDraw, a, b, color, width=1):
    draw.line([a, b], fill=color, width=width)


def draw_orthographic_top(draw, w, h, unit):
    for x in range(0, w + 1, unit):
        _line(draw, (x, 0), (x, h - 1), GRID)
    for y in range(0, h + 1, unit):
        _line(draw, (0, y), (w - 1, y), GRID)


def draw_orthographic_front_top(draw, w, h, unit):
    # Rectangular ground grid: receding edges stay parallel and equally spaced.
    # This is the main anti-taper baseline for front-facing 3/4 worlds.
    draw_orthographic_top(draw, w, h, unit)
    # Plumb lines every two cells
    step = unit * 2
    for x in range(0, w + 1, step):
        _line(draw, (x, 0), (x, h - 1), PLUMB)


def draw_isometric(draw, w, h, unit):
    # 2:1 isometric diamonds. Verticals stay vertical.
    half_w, half_h = unit, max(2, unit // 2)
    # / lines (slope 1/2)
    # Cover the plane with two families of 2:1 lines.
    # Line family A: y = (1/2)x + b, family B: y = -(1/2)x + b
    # Use steps of half_h in intercept.
    min_b = -half_w * (h // half_h + w // half_w + 4)
    max_b = h + w
    b = -h - w
    while b <= max_b:
        # y = x/2 + b  -> points at x=0 and x=w
        _line(draw, (0, b), (w, b + w / 2), GRID)
        _line(draw, (0, b), (w, b - w / 2), GRID)
        b += half_h
    for x in range(0, w + 1, unit * 2):
        _line(draw, (x, 0), (x, h - 1), PLUMB)


def draw_perspective_1p(draw, w, h, unit, vp=None):
    if vp is None:
        vp = (w // 2, int(h * 0.28))
    vx, vy = vp
    # Horizon
    _line(draw, (0, vy), (w - 1, vy), PLUMB, 2)
    # Radiating ground lines
    for x in range(0, w + 1, unit):
        _line(draw, (x, h - 1), (vx, vy), GRID)
    # Horizontal depth cues below the horizon
    y = vy + unit
    while y < h:
        _line(draw, (0, y), (w - 1, y), GRID)
        y += unit
    # Plumbs
    for x in range(0, w + 1, unit * 2):
        _line(draw, (x, vy), (x, h - 1), PLUMB)


def draw_perspective_2p(draw, w, h, unit):
    vy = int(h * 0.28)
    vp1 = (int(-0.15 * w), vy)
    vp2 = (int(1.15 * w), vy)
    _line(draw, (0, vy), (w - 1, vy), PLUMB, 2)
    for x in range(0, w + 1, unit * 2):
        _line(draw, (x, h - 1), vp1, GRID)
        _line(draw, (x, h - 1), vp2, GRID)
        _line(draw, (x, vy), (x, h - 1), PLUMB)


def draw_scale(draw, w, h, unit, char_h, storey):
    x = unit
    y0 = h - unit
    _line(draw, (x, y0), (x, unit), SCALE, 2)
    # Tick every unit
    y = y0
    while y >= unit:
        _line(draw, (x - 3, y), (x + 3, y), SCALE)
        y -= unit
    marks = []
    if char_h:
        marks.append((char_h, "char"))
    if storey:
        marks.append((storey, "storey"))
    for height, _name in marks:
        yy = y0 - height
        if 0 <= yy < h:
            _line(draw, (x - 6, yy), (x + 10, yy), SCALE, 2)


def parse_ratio(value) -> float | None:
    if value is None or value in ("", "UNDETERMINED"):
        return None
    if isinstance(value, (int, float)):
        return float(value) if value > 0 else None
    if isinstance(value, str) and ":" in value:
        a, b = value.split(":", 1)
        try:
            fa, fb = float(a), float(b)
        except ValueError:
            return None
        if fb == 0:
            return None
        return fa / fb
    return None


def draw_wireframe(draw, w, h, unit, ratio):
    # A small front + top house gizmo in the lower-right, not a game building.
    front_h = unit * 3
    if ratio and ratio > 0:
        top_h = max(unit, int(front_h / ratio))
    else:
        top_h = unit * 2
    box_w = unit * 4
    x1 = w - unit * 2
    x0 = x1 - box_w
    y1 = h - unit * 2
    y_eave = y1 - front_h
    y_ridge = y_eave - top_h
    # Front face
    draw.rectangle([x0, y_eave, x1, y1], outline=WIRE)
    # Top plane (foreshortened rectangle, no side faces, no taper)
    draw.rectangle([x0, y_ridge, x1, y_eave], outline=WIRE)
    # Ridge tick at mid-top (still no vanishing)
    mid = (x0 + x1) // 2
    _line(draw, (mid, y_ridge), (mid, y_eave), WIRE)


def render(cfg: dict, *, opaque_bg=False) -> Image.Image:
    w, h = cfg["size"]
    bg = BG_DEMO if opaque_bg else (0, 0, 0, 0)
    im = Image.new("RGBA", (w, h), bg)
    draw = ImageDraw.Draw(im)
    kind = cfg["kind"]
    unit = cfg["unit"]
    if kind == "orthographic-front-top":
        draw_orthographic_front_top(draw, w, h, unit)
    elif kind == "orthographic-top":
        draw_orthographic_top(draw, w, h, unit)
    elif kind == "isometric":
        draw_isometric(draw, w, h, unit)
    elif kind == "perspective-1p":
        draw_perspective_1p(draw, w, h, unit)
    elif kind == "perspective-2p":
        draw_perspective_2p(draw, w, h, unit)
    else:
        die("unsupported kind " + kind)
    if kind != "orthographic-top":
        draw_scale(draw, w, h, unit, cfg["character_height_px"], cfg["storey_height_px"])
    if kind == "orthographic-front-top":
        draw_wireframe(draw, w, h, unit, parse_ratio(cfg.get("front_to_top_ratio")))
    return im


def _missing(value) -> bool:
    return value is None or value == "" or value == [] or value == {} or value == "UNDETERMINED"


def _resolved_kind(kind_raw):
    if not kind_raw or kind_raw in (None, "", "UNDETERMINED"):
        die("projection.kind is unset; pass --kind or fill the art bible")
    kind = KINDS.get(str(kind_raw).strip().lower())
    if not kind:
        die("unknown kind %r; expected one of: %s" % (kind_raw, ", ".join(sorted(set(KINDS.values())))))
    return kind


def format_prompt(proj: dict, args: argparse.Namespace) -> str:
    """Paste-ready camera clause. Null fields are omitted, never invented."""
    kind = _resolved_kind(args.kind or proj.get("kind"))
    parts = [f"投影：{kind}"]

    def add(label, value):
        if _missing(value):
            return
        if isinstance(value, list):
            text = "、".join(str(item) for item in value if not _missing(item))
            if not text:
                return
        else:
            text = str(value)
        parts.append(f"{label}：{text}")

    add("消失点", proj.get("vanishing"))
    add("竖线", proj.get("verticals"))
    add("可见面", proj.get("visible_planes"))
    add("地面边", proj.get("ground_edges"))
    add("立面与顶面高度比", proj.get("front_to_top_ratio"))

    baseline = proj.get("baseline") if isinstance(proj.get("baseline"), dict) else {}
    size = None
    if args.size:
        size = parse_size(args.size)
    else:
        overlay = baseline.get("overlay_size")
        if isinstance(overlay, list) and len(overlay) == 2 and all(isinstance(x, int) and x > 0 for x in overlay):
            size = (overlay[0], overlay[1])
    unit = args.unit if args.unit is not None else baseline.get("grid_unit_px")
    if not isinstance(unit, int) or unit <= 0:
        unit = None
    bits = []
    if size:
        bits.append(f"{size[0]}×{size[1]}")
    if unit:
        bits.append(f"格宽 {unit} 逻辑像素")
    if bits:
        parts.append("基准：" + "，".join(bits))
    return "。".join(parts) + "。"


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
    """Lay the transparent baseline over an existing picture. Review image only.

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
                "--under is %dx%d and the baseline is %dx%d. "
                "Sizes must match, or one side must be a uniform integer multiple of the other. "
                "Refusing to stretch or bilinear-scale. "
                "A part smaller than the canvas is not auto-placed: "
                "lay it onto a same-size canvas first, then overlay."
                % (uw, uh, ow, oh)
            )
    out = base.copy()
    out.alpha_composite(layer)
    return out


def render_demo(cfg: dict) -> Image.Image:
    """Side-by-side teaching plate: parallel road vs tapering road under the same grid."""
    w, h = 640, 360
    im = Image.new("RGBA", (w, h), BG_DEMO)
    draw = ImageDraw.Draw(im)
    mid = w // 2
    _line(draw, (mid, 0), (mid, h - 1), (70, 72, 80, 255), 2)

    def panel(x0, x1, taper: bool, title: str, color):
        # Ground
        draw.rectangle([x0 + 16, 48, x1 - 16, h - 24], fill=(48, 52, 48, 255))
        # Road
        top_y, bot_y = 64, h - 40
        if taper:
            # Incorrect for orthographic: width shrinks toward the top
            pts = [
                (x0 + 90, bot_y),
                (x1 - 90, bot_y),
                (x1 - 150, top_y),
                (x0 + 150, top_y),
            ]
        else:
            pts = [
                (x0 + 110, bot_y),
                (x1 - 110, bot_y),
                (x1 - 110, top_y),
                (x0 + 110, top_y),
            ]
        draw.polygon(pts, fill=(168, 140, 96, 255), outline=color)
        # Overlay a local grid that must stay parallel
        unit = 16
        overlay = Image.new("RGBA", (x1 - x0, h), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for x in range(0, x1 - x0, unit):
            _line(od, (x, 48), (x, h - 24), GRID)
        for y in range(48, h - 23, unit):
            _line(od, (16, y), (x1 - x0 - 16, y), GRID)
        im.alpha_composite(overlay, (x0, 0))
        # Title bar
        draw.rectangle([x0, 0, x1, 40], fill=(22, 24, 28, 255))
        # We cannot assume a CJK font is installed in every environment;
        # use English labels on the plate, Chinese in the README.
        draw.text((x0 + 16, 12), title, fill=color)

    panel(0, mid, False, "PASS  parallel edges (no vanishing)", OK)
    panel(mid, w, True, "FAIL  tapering road on ortho grid", FAIL)
    return im


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bible", type=Path, help="art-bible.json containing projection")
    p.add_argument("--kind", help="camera kind; overrides the bible when both are given")
    p.add_argument("--size", help="WxH logical pixels, e.g. 480x270")
    p.add_argument("--unit", type=int, help="grid unit in logical pixels")
    p.add_argument("--character-height", type=int, dest="character_height")
    p.add_argument("--storey-height", type=int, dest="storey_height")
    p.add_argument("--out", type=Path, help="write a review overlay or comparison image; omitted for --prompt text only")
    p.add_argument("--under", type=Path, help="composite the transparent baseline onto this source or scene image (review comparison only; nearest-neighbor integer scale)")
    p.add_argument("--prompt", "--print-prompt", action="store_true", help="print a paste-ready camera clause from filled fields; does not draw an image unless --out is also set")
    p.add_argument("--demo", action="store_true", help="draw a pass/fail teaching plate instead of a transparent overlay")
    p.add_argument("--allow-implied-vanishing", action="store_true", help=argparse.SUPPRESS)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.demo and (args.under or args.prompt):
        die("--demo cannot be combined with --under or --prompt")
    if args.demo and not args.out:
        die("pass --out to write the teaching plate")
    if args.under and not args.out:
        die("--under needs --out; the comparison image is not written without it")
    if not args.out and not args.prompt and not args.demo:
        die("pass --out to write a review overlay, or --prompt to print a camera clause")

    clause = None
    im = None
    if args.demo:
        im = render_demo({
            "kind": "orthographic-front-top",
            "size": (640, 360),
            "unit": 16,
            "character_height_px": 32,
            "storey_height_px": 48,
            "front_to_top_ratio": "3:2",
            "vanishing": "none",
        })
    else:
        proj = load_projection(args.bible) if (args.out or args.prompt) else {}
        if args.out:
            cfg = resolve(proj, args)
            im = render(cfg, opaque_bg=False)
            if args.under:
                im = composite_under(im, args.under.expanduser())
        if args.prompt:
            clause = format_prompt(proj, args)

    if im is not None:
        args.out = args.out.expanduser()
        args.out.parent.mkdir(parents=True, exist_ok=True)
        im.save(args.out)
        print(f"wrote {args.out} {im.size[0]}x{im.size[1]} {im.mode}")
    if clause:
        print(clause)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
