"""Tests for isityaml.copy.resolve_copy."""

from __future__ import annotations

import unittest

from django.test import SimpleTestCase, override_settings

from tests.django_setup import setup_django

setup_django()

from isityaml.copy import COPY_KEYS, DEFAULT_COPY, resolve_copy


class TestResolveCopy(SimpleTestCase):
    def test_defaults(self):
        copy = resolve_copy()
        self.assertEqual(copy["success_heading"], DEFAULT_COPY["success_heading"])
        self.assertEqual(set(copy), set(COPY_KEYS))

    @override_settings(ISITYAML_COPY={"success_heading": "Valid YAML", "bogus": "x"})
    def test_settings_override(self):
        copy = resolve_copy()
        self.assertEqual(copy["success_heading"], "Valid YAML")
        self.assertNotIn("bogus", copy)

    @override_settings(ISITYAML_COPY={"submit_label": "FromSettings"})
    def test_kwargs_beat_settings(self):
        copy = resolve_copy(submit_label="FromKwarg")
        self.assertEqual(copy["submit_label"], "FromKwarg")

    def test_copy_dict_and_kwargs(self):
        copy = resolve_copy(
            copy={"form_legend": "Paste"},
            success_heading="OK",
        )
        self.assertEqual(copy["form_legend"], "Paste")
        self.assertEqual(copy["success_heading"], "OK")


if __name__ == "__main__":
    unittest.main()
