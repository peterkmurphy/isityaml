"""Shared Django setup for isityaml package tests."""

from __future__ import annotations

from pathlib import Path

import django
from django.conf import settings

TEST_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def setup_django() -> None:
    if settings.configured:
        return
    settings.configure(
        SECRET_KEY="isityaml-test",
        ROOT_URLCONF="tests.test_urls",
        ALLOWED_HOSTS=["*"],
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.staticfiles",
            "isityaml",
        ],
        STATIC_URL="static/",
        MIDDLEWARE=[
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.middleware.common.CommonMiddleware",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [str(TEST_TEMPLATES_DIR)],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.request",
                    ],
                },
            }
        ],
    )
    django.setup()
