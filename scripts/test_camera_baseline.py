#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for camera_baseline.py. No visual pass is claimed."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "camera_baseline.py"
BIBLE = ROOT / "examples" / "camera-baseline" / "example-art-bible.json"


def run(args, check=True):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=check,
    )


class CameraBaselineTests(unittest.TestCase):
    def test_bible_writes_transparent_overlay(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "grid.png"
            result = run(["--bible", str(BIBLE), "--out", str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            im = Image.open(out)
            self.assertEqual(im.size, (480, 270))
            self.assertEqual(im.mode, "RGBA")
            extrema = im.getextrema()
            self.assertEqual(extrema[3][0], 0, "overlay must keep transparent pixels")
            self.assertGreater(extrema[3][1], 0, "overlay must draw some visible strokes")

    def test_refuses_missing_kind(self):
        with tempfile.TemporaryDirectory() as td:
            bible = Path(td) / "empty.json"
            bible.write_text(json.dumps({"projection": {"kind": None, "baseline": {"overlay_size": [64, 64], "grid_unit_px": 16}}}), encoding="utf-8")
            out = Path(td) / "x.png"
            result = run(["--bible", str(bible), "--out", str(out)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("kind", result.stderr.lower())

    def test_refuses_vanishing_on_ortho(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "x.png"
            bible = Path(td) / "bad.json"
            data = json.loads(BIBLE.read_text(encoding="utf-8"))
            data["projection"]["vanishing"] = "one-point"
            bible.write_text(json.dumps(data), encoding="utf-8")
            result = run(["--bible", str(bible), "--out", str(out)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())

    def test_demo_plate(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "demo.png"
            result = run(["--demo", "--out", str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(out) as im:
                self.assertEqual(im.size, (640, 360))

    def _small_bible(self, directory, **projection):
        path = Path(directory) / "bible.json"
        path.write_text(json.dumps({"projection": projection}), encoding="utf-8")
        return path

    def test_under_same_size_keeps_pixels_beneath_grid(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            bible = self._small_bible(
                td, kind="orthographic-front-top", vanishing="none",
                baseline={"overlay_size": [64, 64], "grid_unit_px": 8},
            )
            overlay_path = td / "overlay.png"
            result = run(["--bible", str(bible), "--out", str(overlay_path)])
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
            result = run(["--bible", str(bible), "--under", str(under_path), "--out", str(out)])
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
                td, kind="orthographic-top", vanishing="none",
                baseline={"overlay_size": [32, 32], "grid_unit_px": 8},
            )
            overlay_path = td / "overlay.png"
            result = run(["--bible", str(bible), "--out", str(overlay_path)])
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
            result = run(["--bible", str(bible), "--under", str(under_path), "--out", str(out)])
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
            result = run(["--bible", str(bible), "--under", str(small_path), "--out", str(out_up)])
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
                td, kind="orthographic-top", vanishing="none",
                baseline={"overlay_size": [32, 32], "grid_unit_px": 8},
            )
            under = Image.new("RGBA", (48, 40), (90, 90, 90, 255))
            under_path = td / "odd.png"
            under.save(under_path)
            out = td / "nope.png"
            result = run(["--bible", str(bible), "--under", str(under_path), "--out", str(out)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("integer", result.stderr.lower())
            self.assertIn("canvas", result.stderr.lower())
            part = Image.new("RGBA", (12, 12), (1, 2, 3, 255))
            part_path = td / "part.png"
            part.save(part_path)
            out_part = td / "part-out.png"
            result = run(["--bible", str(bible), "--under", str(part_path), "--out", str(out_part)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out_part.exists())

    def test_prompt_prints_filled_terms_and_refuses_unset_kind(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            result = run(["--bible", str(BIBLE), "--prompt"])
            self.assertEqual(result.returncode, 0, result.stderr)
            for term in (
                "orthographic-front-top", "none", "remain-vertical", "front", "top",
                "parallel-equal-spacing", "3:2", "480", "270", "16",
            ):
                self.assertIn(term, result.stdout)
            self.assertNotIn("null", result.stdout.lower())
            self.assertNotIn("Front-facing", result.stdout)
            overridden = run([
                "--bible", str(BIBLE), "--print-prompt", "--kind", "top-down",
                "--size", "320x180", "--unit", "8",
            ])
            self.assertEqual(overridden.returncode, 0, overridden.stderr)
            self.assertIn("orthographic-top", overridden.stdout)
            self.assertIn("320×180", overridden.stdout)
            self.assertIn("格宽 8", overridden.stdout)
            self.assertNotIn("480", overridden.stdout)
            sparse = self._small_bible(
                td, kind="orthographic-top", vanishing=None, verticals=None,
                visible_planes=None, ground_edges="parallel-equal-spacing",
                front_to_top_ratio=None, baseline={"grid_unit_px": None, "overlay_size": None},
            )
            result = run(["--bible", str(sparse), "--prompt"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("orthographic-top", result.stdout)
            self.assertIn("parallel-equal-spacing", result.stdout)
            self.assertNotIn("消失点", result.stdout)
            self.assertNotIn("None", result.stdout)
            empty = self._small_bible(td, kind=None, baseline={"overlay_size": [64, 64], "grid_unit_px": 16})
            out = td / "should-not-exist.png"
            result = run(["--bible", str(empty), "--prompt", "--out", str(out)], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("kind", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
