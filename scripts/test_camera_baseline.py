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
            im = Image.open(out)
            self.assertEqual(im.size, (640, 360))


if __name__ == "__main__":
    unittest.main()
