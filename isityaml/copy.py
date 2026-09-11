"""User-facing copy for the Is it YAML? checker UI.

Override site-wide with ``settings.ISITYAML_COPY`` (a dict of string keys),
or per-embed via kwargs / a ``copy`` dict on ``{% isityaml_checker %}``.
Resolution order: defaults → settings → explicit overrides.
"""

from __future__ import annotations

from django.conf import settings

DEFAULT_COPY: dict[str, str] = {
    "success_heading": "Yes, it is YAML!",
    "success_body": (
        "The file you entered is properly formatted and has been presented "
        "in 'canonical' form for your perusal."
    ),
    "error_heading": "No, it is not YAML!",
    "error_body": (
        "I'm afraid the text you entered is not legitimate YAML. "
        "Here's an error message."
    ),
    "original_body": (
        "Here's the original text, just so you can check where things went wrong."
    ),
    "another_go_heading": "Do you want to have another go?",
    "form_intro": (
        "Enter some text in the text field below and click \"Submit\" to check "
        "if it is YAML. Hit \"Reset\" to restore the default sample text."
    ),
    "form_legend": "Put yer YAML here!",
    "form_label": "But is it properly formatted?",
    "textarea_default": "Hello world!",
    "submit_label": "Submit",
    "reset_label": "Reset",
}

COPY_KEYS = frozenset(DEFAULT_COPY)


def resolve_copy(
    copy: dict[str, str] | None = None,
    **overrides: str,
) -> dict[str, str]:
    """Build the effective copy dict for the checker templates.

    Args:
        copy: Optional mapping of copy keys (same role as kwargs).
        **overrides: Individual copy keys to override (e.g. ``success_heading=...``).

    Returns:
        A new dict with all ``DEFAULT_COPY`` keys filled.
    """
    result = dict(DEFAULT_COPY)
    settings_copy = getattr(settings, "ISITYAML_COPY", None) or {}
    for key, value in settings_copy.items():
        if key in COPY_KEYS and value is not None:
            result[key] = str(value)
    if copy:
        for key, value in copy.items():
            if key in COPY_KEYS and value is not None:
                result[key] = str(value)
    for key, value in overrides.items():
        if key in COPY_KEYS and value is not None:
            result[key] = str(value)
    return result
