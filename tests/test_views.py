"""Django view / template-tag smoke tests for isityaml."""

from __future__ import annotations

import unittest

from django.template import Context, Template
from django.test import Client, SimpleTestCase
from django.urls import clear_url_caches

from tests.django_setup import setup_django

setup_django()


class TestIndexView(SimpleTestCase):
    def setUp(self):
        clear_url_caches()
        self.client = Client(enforce_csrf_checks=False)

    def test_get_shows_form(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("yamlarea", content)
        self.assertIn('action="/"', content)
        self.assertNotIn("Yes, it is YAML!", content)

    def test_post_valid_yaml(self):
        response = self.client.post("/", {"yamlarea": "foo: bar"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Yes, it is YAML!", response.content.decode())

    def test_post_invalid_yaml(self):
        response = self.client.post("/", {"yamlarea": "[[[("})
        self.assertEqual(response.status_code, 200)
        self.assertIn("No, it is not YAML!", response.content.decode())

    def test_post_unicode_anchor(self):
        sample = "x: &über y\nz: *über\n"
        response = self.client.post("/", {"yamlarea": sample})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Yes, it is YAML!", response.content.decode())


class TestInclusionTag(SimpleTestCase):
    def test_named_url_and_copy_kwarg(self):
        template = Template(
            "{% load isityaml_tags %}"
            '{% isityaml_checker success_heading="Custom OK" %}'
        )
        html = template.render(Context({"yamlstate": 1, "yamlcanon": "---\n"}))
        self.assertIn("Custom OK", html)
        self.assertIn('action="/"', html)


if __name__ == "__main__":
    unittest.main()
