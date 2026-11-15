#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for placement_baseline.py. No visual pass is claimed."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "placement_baseline.py"
BIBLE = ROOT / "examples" / "placement-baseline" / "example-art-bible.json"
PLAN = ROOT / "examples" / "placement-baseline" / "example-scene-plan.json"

PATH_EDGE = (255, 148, 40, 230)
PATH_FILL = (255, 148, 40, 150)


def run(args, check=True):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=check,
    )


class PlacementBaselineTests(unittest.TestCase):
    def test_example_writes_transparent_overlay(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "overlay.png"
            result = run(["--bible", str(BIBLE), "--plan", str(PLAN), "--out", str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            im = Image.open(out)
            self.assertEqual(im.size, (480, 270))
            self.assertEqual(im.mode, "RGBA")
            extrema = im.getextrema()
            self.assertEqual(extrema[3][0], 0, "overlay must keep transparent pixels")
            self.assertGreater(extrema[3][1], 0, "overlay must draw some visible strokes")

    def test_refuses_missing_layout_object(self):
        with tempfile.TemporaryDirectory() as td:
            bible = Path(td) / "empty.json"
            bible.write_text(json.dumps({"projection": {"kind": "orthographic-front-top"}}), encoding="utf-8")
            out = Path(td) / "x.png"
            result = run(["--bible", str(bible), "--plan", str(PLAN), "--out", str(out)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("layout", result.stderr.lower())

    def test_refuses_unset_scene_type(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            plan = json.loads(PLAN.read_text(encoding="utf-8"))
            plan["scene_type"] = None
            plan_path = td / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            out = td / "x.png"
            result = run(["--bible", str(BIBLE), "--plan", str(plan_path), "--out", str(out)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("scene_type", result.stderr.lower())
            result = run(["--bible", str(BIBLE), "--plan", str(plan_path), "--prompt"], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("scene_type", result.stderr.lower())

    def test_refuses_unset_primary_path(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            plan = json.loads(PLAN.read_text(encoding="utf-8"))
            plan["primary_path"] = None
            plan_path = td / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            out = td / "x.png"
            result = run(["--bible", str(BIBLE), "--plan", str(plan_path), "--out", str(out)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("primary_path", result.stderr.lower())

    def test_demo_plate(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "demo.png"
            result = run(["--demo", "--out", str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(out) as im:
                self.assertEqual(im.size, (640, 360))

    def _small_bible(self, directory, **layout):
        path = Path(directory) / "bible.json"
        path.write_text(json.dumps({"layout": layout}), encoding="utf-8")
        return path

    def _small_plan(self, directory, **updates):
        plan = {
            "scene_type": "gate-courtyard",
            "required_elements": ["gate-opening", "boundary-wall"],
            "primary_path": {
                "entrance": "south",
                "route": "gate",
                "destination": "courtyard",
                "kind": "main",
                "units": "px",
                "polyline": [[32, 60], [32, 8]],
            },
        }
        plan.update(updates)
        path = Path(directory) / "plan.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        return path

    def test_under_same_size_keeps_pixels_beneath_overlay(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bible = self._small_bible(
                td, grid_unit_px=8, overlay_size=[64, 64],
                path_widths={"main": 2},
                character_footprint_tiles=[1, 1],
            )
            plan = self._small_plan(td, primary_path={
                "entrance": "south", "route": "mid", "destination": "north",
                "kind": "main", "units": "px", "polyline": [[32, 60], [32, 8]],
            })
            overlay_path = td / "overlay.png"
            result = run(["--bible", str(bible), "--plan", str(plan), "--out", str(overlay_path)])
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(overlay_path) as overlay:
                overlay = overlay.convert("RGBA")
                pixels = list(overlay.getdata())
            w, h = overlay.size
            clear = next(i for i, px in enumerate(pixels) if px[3] == 0)
            covered = next(i for i, px in enumerate(pixels) if px[3] > 0)
            under = Image.new("RGBA", (w, h), (20, 40, 60, 255))
            under.putpixel((clear % w, clear // w), (11, 22, 33, 255))
            under_path = td / "under.png"
            under.save(under_path)
            out = td / "compare.png"
            result = run(["--bible", str(bible), "--plan", str(plan), "--under", str(under_path), "--out", str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            blob = (result.stdout + result.stderr).lower()
            self.assertNotIn("pass", blob)
            self.assertNotIn("fail", blob)
            self.assertNotIn("approv", blob)
            with Image.open(out) as got:
                got = got.convert("RGBA")
            self.assertEqual(got.getpixel((clear % w, clear // w)), (11, 22, 33, 255))
            reference = under.copy()
            reference.alpha_composite(overlay)
            self.assertEqual(list(got.getdata()), list(reference.getdata()))
            on_black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
            on_black.alpha_composite(overlay)
            self.assertNotEqual(got.getpixel((covered % w, covered // w)), on_black.getpixel((covered % w, covered // w)))

    def test_under_integer_scale_uses_nearest_neighbor(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bible = self._small_bible(
                td, grid_unit_px=8, overlay_size=[32, 32],
                path_widths={"main": 2},
            )
            plan = self._small_plan(td, primary_path={
                "entrance": "south", "route": "mid", "destination": "north",
                "kind": "main", "units": "px", "polyline": [[16, 28], [16, 4]],
            })
            overlay_path = td / "overlay.png"
            result = run(["--bible", str(bible), "--plan", str(plan), "--out", str(overlay_path)])
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(overlay_path) as overlay:
                overlay = overlay.convert("RGBA")
            under = Image.new("RGBA", (64, 64), (0, 0, 0, 255))
            for y in range(64):
                for x in range(64):
                    under.putpixel((x, y), ((x * 13) % 256, (y * 17) % 256, 40, 255))
            under_path = td / "under.png"
            under.save(under_path)
            out = td / "scaled.png"
            result = run(["--bible", str(bible), "--plan", str(plan), "--under", str(under_path), "--out", str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(out) as got:
                got = got.convert("RGBA")
            nearest = overlay.resize((64, 64), Image.Resampling.NEAREST)
            expected = under.copy()
            expected.alpha_composite(nearest)
            self.assertEqual(list(got.getdata()), list(expected.getdata()))
            bilinear = overlay.resize((64, 64), Image.Resampling.BILINEAR)
            other = under.copy()
            other.alpha_composite(bilinear)
            self.assertNotEqual(list(got.getdata()), list(other.getdata()))

            small = Image.new("RGBA", (16, 16), (0, 0, 0, 255))
            for y in range(16):
                for x in range(16):
                    small.putpixel((x, y), (255 if x % 2 == 0 else 0, 10, 255 if y % 2 == 0 else 0, 255))
            small_path = td / "small.png"
            small.save(small_path)
            out_up = td / "up.png"
            result = run(["--bible", str(bible), "--plan", str(plan), "--under", str(small_path), "--out", str(out_up)])
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(out_up) as got_up:
                got_up = got_up.convert("RGBA")
            grown = small.resize((32, 32), Image.Resampling.NEAREST)
            expected_up = grown.copy()
            expected_up.alpha_composite(overlay)
            self.assertEqual(list(got_up.getdata()), list(expected_up.getdata()))
            soft = small.resize((32, 32), Image.Resampling.BILINEAR)
            other_up = soft.copy()
            other_up.alpha_composite(overlay)
            self.assertNotEqual(list(got_up.getdata()), list(other_up.getdata()))

    def test_under_non_integer_mismatch_writes_no_file(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bible = self._small_bible(
                td, grid_unit_px=8, overlay_size=[32, 32], path_widths={"main": 2},
            )
            plan = self._small_plan(td)
            under = Image.new("RGBA", (48, 40), (90, 90, 90, 255))
            under_path = td / "odd.png"
            under.save(under_path)
            out = td / "nope.png"
            result = run(
                ["--bible", str(bible), "--plan", str(plan), "--under", str(under_path), "--out", str(out)],
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("integer", result.stderr.lower())
            self.assertIn("canvas", result.stderr.lower())
            part = Image.new("RGBA", (12, 12), (1, 2, 3, 255))
            part_path = td / "part.png"
            part.save(part_path)
            out_part = td / "part-out.png"
            result = run(
                ["--bible", str(bible), "--plan", str(plan), "--under", str(part_path), "--out", str(out_part)],
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out_part.exists())

    def test_prompt_prints_filled_terms_and_skips_nulls(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            result = run(["--bible", str(BIBLE), "--plan", str(PLAN), "--prompt"])
            self.assertEqual(result.returncode, 0, result.stderr)
            for term in (
                "摆放", "格宽 16", "480", "270", "主路宽：3 格", "巷宽：2 格",
                "桥或石阶宽：2 格", "住宅 3×3 格", "公共 4×4 格",
                "gate-courtyard", "gate-opening", "boundary-wall",
                "south road", "courtyard landmark", "stele",
                "接头：", "west-gate-post（boundary-wall → gate-opening）",
                "east-gate-post（boundary-wall → gate-opening）",
            ):
                self.assertIn(term, result.stdout)
            blob = (result.stdout + result.stderr).lower()
            self.assertNotIn("pass", blob)
            self.assertNotIn("fail", blob)
            self.assertNotIn("approv", blob)
            self.assertNotIn("null", result.stdout.lower())
            self.assertNotIn("None", result.stdout)

            sparse = self._small_bible(
                td, grid_unit_px=8, path_widths={"main": 3, "alley": None, "bridge_or_steps": None},
                door_clearances={"residential": None, "public": None},
                building_gap=None, overlay_size=None, character_footprint_tiles=None,
            )
            result = run(["--bible", str(sparse), "--prompt", "--size", "320x180"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("主路宽：3 格", result.stdout)
            self.assertIn("格宽 8", result.stdout)
            self.assertIn("320×180", result.stdout)
            self.assertNotIn("巷宽", result.stdout)
            self.assertNotIn("门前净空", result.stdout)
            self.assertNotIn("场景类型", result.stdout)
            self.assertNotIn("接头", result.stdout)
            self.assertNotIn("null", result.stdout.lower())
            self.assertNotIn("None", result.stdout)

            empty = self._small_bible(td)
            # overwrite with an all-null layout
            empty.write_text(json.dumps({
                "layout": {
                    "grid_unit_px": None,
                    "path_widths": {"main": None},
                    "overlay_size": None,
                }
            }), encoding="utf-8")
            out = td / "should-not-exist.png"
            result = run(["--bible", str(empty), "--prompt", "--out", str(out)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())

    def test_joints_are_a_checklist_and_do_not_change_the_overlay(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bible = self._small_bible(
                td, grid_unit_px=8, overlay_size=[64, 64], path_widths={"main": 2},
            )
            plan = self._small_plan(td)
            plain = td / "plain.png"
            result = run(["--bible", str(bible), "--plan", str(plan), "--out", str(plain)])
            self.assertEqual(result.returncode, 0, result.stderr)
            noted = json.loads(plan.read_text(encoding="utf-8"))
            noted["joints"] = [
                {"name": "west-gate-post", "from": "boundary-wall", "to": "gate-opening"},
                {"name": None, "from": "boundary-wall", "to": "gate-opening"},
                {"from": "boundary-wall", "to": "gate-opening"},
                "courtyard-corner",
            ]
            noted_path = td / "noted.json"
            noted_path.write_text(json.dumps(noted), encoding="utf-8")
            marked = td / "marked.png"
            result = run(["--bible", str(bible), "--plan", str(noted_path), "--out", str(marked)])
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(plain) as a, Image.open(marked) as b:
                self.assertEqual(list(a.convert("RGBA").getdata()), list(b.convert("RGBA").getdata()))
            result = run(["--bible", str(bible), "--plan", str(noted_path), "--prompt"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("接头：west-gate-post（boundary-wall → gate-opening）、courtyard-corner", result.stdout)
            self.assertNotIn("null", result.stdout.lower())
            self.assertNotIn("None", result.stdout)
            blob = (result.stdout + result.stderr).lower()
            self.assertNotIn("pass", blob)
            self.assertNotIn("fail", blob)
            self.assertNotIn("approv", blob)
            omitted = dict(noted)
            omitted["joints"] = None
            omitted_path = td / "omitted.json"
            omitted_path.write_text(json.dumps(omitted), encoding="utf-8")
            result = run(["--bible", str(bible), "--plan", str(omitted_path), "--prompt"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("接头", result.stdout)
            self.assertIn("gate-courtyard", result.stdout)

    def test_corridor_keeps_declared_width_no_taper(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bible = self._small_bible(
                td, grid_unit_px=8, overlay_size=[96, 96], path_widths={"main": 3},
            )
            plan = self._small_plan(td, primary_path={
                "entrance": "south", "route": "mid", "destination": "north",
                "kind": "main", "units": "px", "polyline": [[48, 88], [48, 8]],
            })
            out = td / "path.png"
            result = run(["--bible", str(bible), "--plan", str(plan), "--out", str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            im = Image.open(out).convert("RGBA")
            widths = []
            for y in range(16, 80):
                xs = [x for x in range(96) if im.getpixel((x, y))[3] > 0]
                if xs:
                    widths.append(max(xs) - min(xs) + 1)
            self.assertGreater(len(widths), 10)
            # Declared width is 3 tiles * 8 px = 24. Allow 1 px of outline raster.
            self.assertGreaterEqual(min(widths), 23)
            self.assertLessEqual(max(widths), 25)
            self.assertLessEqual(max(widths) - min(widths), 1, "corridor tapered: %s" % widths)

    def test_walkable_reports_data_not_a_score(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bible = self._small_bible(
                td, grid_unit_px=8, overlay_size=[64, 64], path_widths={"main": 2},
            )
            plan = self._small_plan(td, primary_path={
                "entrance": "south", "route": "mid", "destination": "north",
                "kind": "main", "units": "px", "polyline": [[16, 56], [16, 8]],
            })
            mask = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            d = ImageDraw.Draw(mask)
            d.rectangle([8, 4, 24, 60], fill=(255, 255, 255, 255))
            mask_path = td / "mask.png"
            mask.save(mask_path)
            result = run([
                "--bible", str(bible), "--plan", str(plan),
                "--walkable", str(mask_path), "--json",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            blob = (result.stdout + result.stderr).lower()
            self.assertNotIn("pass", blob)
            self.assertNotIn("fail", blob)
            self.assertNotIn("approv", blob)
            data = json.loads(result.stdout.strip().splitlines()[-1])
            self.assertTrue(data["reachable"])
            # Block the route and confirm the destination is reported unreachable.
            blocked = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            bd = ImageDraw.Draw(blocked)
            bd.rectangle([8, 40, 24, 60], fill=(255, 255, 255, 255))
            blocked_path = td / "blocked.png"
            blocked.save(blocked_path)
            result = run([
                "--bible", str(bible), "--plan", str(plan),
                "--walkable", str(blocked_path),
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("unreachable", result.stdout)
            self.assertNotIn("PASS", result.stdout)
            self.assertNotIn("FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
