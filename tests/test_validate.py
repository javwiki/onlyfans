"""Regression tests for publishing checks, using isolated documentation fixtures."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

spec = importlib.util.spec_from_file_location(
    "validate", Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
)
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.docs = self.root / "docs"
        (self.docs / "0_meta").mkdir(parents=True)
        for letter in validate.LETTERS:
            directory = self.docs / letter
            directory.mkdir()
            (directory / "index.md").write_text("# List\n", encoding="utf-8")
        self.index = self.docs / "A" / "index.md"
        self.index.write_text("[Alice](./Alice.md)\n", encoding="utf-8")
        self.page = self.docs / "A" / "Alice.md"
        self.page.write_text(
            "## 简介\n介绍\n## 相关链接\n[返回](./index.md#list) · 首页\n",
            encoding="utf-8",
        )
        self.data = {"Alice": {
            "name": "Alice", "region": "日本", "file": "docs/A/Alice.md", "status": 80,
        }}
        self.list_file = self.docs / "0_meta" / "list.yaml"
        self.save()

    def save(self):
        self.list_file.write_text(yaml.safe_dump(self.data, allow_unicode=True), encoding="utf-8")

    def run_validator(self, strict=False):
        output = io.StringIO()
        with patch.multiple(validate, ROOT=str(self.root), SRC=str(self.docs),
                            LIST_YAML=str(self.list_file)), \
                patch("sys.argv", ["validate.py"] + (["--strict"] if strict else [])), \
                contextlib.redirect_stdout(output):
            code = validate.main()
        return code, output.getvalue()

    def test_strict_passes_without_warnings(self):
        code, output = self.run_validator(strict=True)
        self.assertEqual(code, 0, output)
        self.assertIn("errors=0, warnings=0", output)

    def test_real_warnings_fail_only_in_strict_mode(self):
        del self.data["Alice"]["region"]
        self.save()
        self.page.write_text(self.page.read_text() + "网络搜索未找到", encoding="utf-8")
        self.assertEqual(self.run_validator()[0], 0)
        code, output = self.run_validator(strict=True)
        self.assertEqual(code, 1)
        self.assertIn("warnings=2", output)

    def test_plain_name_and_wrong_link_do_not_satisfy_index(self):
        for content in ("Alice", "[Alice](./index.md)", "![Alice](./Alice.md)"):
            with self.subTest(content=content):
                self.index.write_text(content, encoding="utf-8")
                code, output = self.run_validator()
                self.assertEqual(code, 1)
                self.assertIn("E3", output)

    def test_missing_name_does_not_hide_missing_link(self):
        del self.data["Alice"]["name"]
        self.save()
        self.index.write_text("# Empty", encoding="utf-8")
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("缺少 name", output)
        self.assertIn("E3", output)

    def test_missing_file_prints_error(self):
        self.page.unlink()
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("指向不存在的文件 docs/A/Alice.md", output)
        self.assertIn("共 1 个条目", output)

    def test_duplicate_yaml_keys_are_rejected(self):
        for text in ("Alice: {}\nAlice: {}\n", "Alice:\n  status: 70\n  status: 80\n"):
            with self.subTest(text=text):
                self.list_file.write_text(text, encoding="utf-8")
                code, output = self.run_validator()
                self.assertEqual(code, 1)
                self.assertIn("重复键", output)

    def test_malformed_root_and_entry_report_errors(self):
        for text in ("[]", "{}", "Alice: null", "Alice: [one, two]", "Alice: ["):
            with self.subTest(text=text):
                self.list_file.write_text(text, encoding="utf-8")
                code, output = self.run_validator()
                self.assertEqual(code, 1)
                self.assertIn("[ERROR] E1", output)

    def test_invalid_status_is_rejected(self):
        for status in (-1, 101, True, "80", 80.5, None):
            with self.subTest(status=status):
                self.data["Alice"]["status"] = status
                self.save()
                code, output = self.run_validator()
                self.assertEqual(code, 1)
                self.assertIn("status 必须", output)

    def test_invalid_fields_are_rejected(self):
        for field, value in (("name", 12), ("region", []), ("x", ""),
                             ("file", None), ("file", "docs/A/index.md")):
            with self.subTest(field=field):
                previous = self.data["Alice"].copy()
                self.data["Alice"][field] = value
                self.save()
                code, output = self.run_validator()
                self.assertEqual(code, 1)
                self.assertIn("E1", output)
                self.data["Alice"] = previous

    def test_encoded_index_link_and_broken_relative_link(self):
        self.index.write_text('[Alice](./%41lice.md#profile "Profile")', encoding="utf-8")
        self.assertEqual(self.run_validator(strict=True)[0], 0)
        self.page.write_text(self.page.read_text() + "[Missing](./missing.md)", encoding="utf-8")
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("E6", output)


if __name__ == "__main__":
    unittest.main()
