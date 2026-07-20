import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from core.analyzer import build_rename_plan, infer_episode_number


class RenamePlanTests(unittest.TestCase):
    def test_infer_episode_number_from_chinese_format(self) -> None:
        self.assertEqual(infer_episode_number("第12集.mp4"), 12)
        self.assertEqual(infer_episode_number("第3集.mkv"), 3)

    def test_infer_episode_number_from_plain_numeric_format(self) -> None:
        self.assertEqual(infer_episode_number("01.mp4"), 1)
        self.assertEqual(infer_episode_number("S01E02.mkv"), 2)

    def test_infer_episode_number_from_common_variants(self) -> None:
        self.assertEqual(infer_episode_number("第 03 集.mkv"), 3)
        self.assertEqual(infer_episode_number("EP01.mp4"), 1)

    def test_build_rename_plan_renames_files_in_same_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "1集.mp4").write_bytes(b"a")
            (tmp_path / "2集.mkv").write_bytes(b"b")

            plan = build_rename_plan(tmp_path)

            self.assertEqual(len(plan), 2)
            self.assertEqual(plan[0].target.name, "01.mp4")
            self.assertEqual(plan[1].target.name, "02.mkv")
            self.assertTrue(plan[0].source.exists())
            self.assertTrue(plan[0].target.parent.exists())
            self.assertIn(tmp_path.name + "_renamed", str(plan[0].target))

    def test_build_rename_plan_groups_multiple_versions_under_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            version_one = tmp_path / "00成片"
            version_two = tmp_path / "1.有音乐无字幕版本"
            version_one.mkdir(parents=True)
            version_two.mkdir(parents=True)
            (version_one / "1集.mp4").write_bytes(b"a")
            (version_two / "2集.mp4").write_bytes(b"b")

            plan = build_rename_plan(tmp_path)

            self.assertEqual(len(plan), 2)
            self.assertIn(tmp_path.name + "_renamed", str(plan[0].target))
            self.assertEqual(plan[0].target.name, "01.mp4")
            self.assertEqual(plan[1].target.name, "01.mp4")


if __name__ == "__main__":
    unittest.main()
