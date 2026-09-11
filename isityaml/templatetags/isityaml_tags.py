"""Template tags for embedding the Is it YAML? checker UI."""

from django import template
from django.urls import NoReverseMatch, reverse

from isityaml.copy import COPY_KEYS, resolve_copy
from isityaml.yaml_check import STATE_GET

register = template.Library()


@register.inclusion_tag("isityaml/_checker.html", takes_context=True)
def isityaml_checker(context, action_url=None, copy=None, **kwargs):
    """Render the YAML result (if any) and the checker form.

    The form POSTs to the named ``isityaml:index`` URL by default, so hosts
    can mount the app under any path. Pass ``action_url`` to override.

    Checker wording comes from ``resolve_copy()``: defaults, then
    ``settings.ISITYAML_COPY``, then optional ``copy=`` / keyword overrides
    (for example ``success_heading="Looks good!"``).

    Args:
        context: Parent template context (may include check results).
        action_url: Optional explicit form ``action`` URL.
        copy: Optional dict of copy-key overrides.
        **kwargs: Optional individual copy-key overrides.

    Returns:
        Context for ``_checker.html``.
    """
    if action_url:
        form_action = action_url
    else:
        try:
            form_action = reverse("isityaml:index")
        except NoReverseMatch:
            form_action = "."

    copy_kwargs = {key: kwargs[key] for key in kwargs if key in COPY_KEYS}

    return {
        "yamlstate": context.get("yamlstate", STATE_GET),
        "yamlcanon": context.get("yamlcanon", ""),
        "yamlerror": context.get("yamlerror", ""),
        "yamloriginal": context.get("yamloriginal", ""),
        "form_action": form_action,
        "copy": resolve_copy(copy=copy, **copy_kwargs),
    }
