"""Tests for isityaml.yaml_check, including Unicode anchors/aliases."""

from __future__ import annotations

import unittest

from isityaml.yaml_check import (
    COMMENTSTR,
    STATE_GET,
    STATE_POST_NO,
    STATE_POST_YES,
    Loader12,
    check_yaml,
    empty_check_result,
)
from yaml import SafeLoader, compose_all
from yaml.scanner import ScannerError


class TestEmptyAndBasics(unittest.TestCase):
    def test_empty_check_result(self):
        result = empty_check_result()
        self.assertEqual(result.yamlstate, STATE_GET)
        self.assertEqual(result.yamlcanon, "")
        self.assertEqual(result.as_context()["yamlstate"], STATE_GET)

    def test_simple_mapping_succeeds(self):
        result = check_yaml("foo: bar")
        self.assertEqual(result.yamlstate, STATE_POST_YES)
        self.assertIn("foo", result.yamlcanon)
        self.assertIn("bar", result.yamlcanon)
        self.assertEqual(result.yamlerror, "")

    def test_empty_stream_uses_comment_placeholder(self):
        result = check_yaml("")
        self.assertEqual(result.yamlstate, STATE_POST_YES)
        self.assertEqual(result.yamlcanon, COMMENTSTR)

    def test_invalid_yaml_fails(self):
        text = "a: [1, 2"
        result = check_yaml(text)
        self.assertEqual(result.yamlstate, STATE_POST_NO)
        self.assertTrue(result.yamlerror)
        self.assertEqual(result.yamloriginal, text)

    def test_none_input_fails(self):
        result = check_yaml(None)
        self.assertEqual(result.yamlstate, STATE_POST_NO)
        self.assertEqual(result.yamloriginal, "")


class TestUnicodeAnchorsAndAliases(unittest.TestCase):
    """Loader12 must accept Unicode anchor/alias names that SafeLoader rejects."""

    UNICODE_SAMPLES = (
        ("latin-1", "x: &über y\nz: *über\n"),
        ("greek", "x: &α y\nz: *α\n"),
        ("cjk", 'items:\n  - &汉 "bittersweet"\n  - *汉\n'),
        ("cafe", "label: &café value\nother: *café\n"),
    )

    def test_stock_safeloader_rejects_unicode_anchors(self):
        for name, sample in self.UNICODE_SAMPLES:
            with self.subTest(sample=name), self.assertRaises(ScannerError):
                list(compose_all(sample, Loader=SafeLoader))

    def test_loader12_accepts_unicode_anchors(self):
        for name, sample in self.UNICODE_SAMPLES:
            with self.subTest(sample=name):
                docs = list(compose_all(sample, Loader=Loader12))
                self.assertGreaterEqual(len(docs), 1)

    def test_check_yaml_accepts_unicode_anchors(self):
        for name, sample in self.UNICODE_SAMPLES:
            with self.subTest(sample=name):
                result = check_yaml(sample)
                self.assertEqual(
                    result.yamlstate,
                    STATE_POST_YES,
                    msg=f"{name}: {result.yamlerror!r}",
                )
                self.assertTrue(result.yamlcanon)
                self.assertEqual(result.yamlerror, "")

    def test_ascii_anchors_still_work(self):
        sample = "x: &anchor y\nz: *anchor\n"
        result = check_yaml(sample)
        self.assertEqual(result.yamlstate, STATE_POST_YES)
        # Stock loader should also accept ASCII
        docs = list(compose_all(sample, Loader=SafeLoader))
        self.assertGreaterEqual(len(docs), 1)


if __name__ == "__main__":
    unittest.main()
