"""YAML composition helpers for Is it YAML? (no Django request types)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from yaml import SafeLoader, compose_all, serialize_all
from yaml.error import YAMLError
from yaml.scanner import ScannerError

# The following code updates the scanner so that it can deal with Unicode
# anchors and aliases.
#
# PKM2017 - hopefully this will be removed in future versions of the code
# as the YAML parser will be updated to sort out this bug.
#
# Stock PyYAML (through at least 6.x) still restricts anchor/alias names to
# ASCII; subclass SafeLoader so compose_all's Loader type stays satisfied.


class Loader12(SafeLoader):
    """SafeLoader with Unicode-capable anchors and aliases."""

    def scan_anchor(self, TokenClass: type[Any]) -> Any:
        """Scan an anchor or alias name per YAML 1.2 character rules.

        Commas and flow indicators are not allowed in anchor/alias names.
        Unlike the stock scanner, names need not be ASCII alphanumeric only.
        """
        start_mark = self.get_mark()
        indicator = self.peek()
        if indicator == "*":
            name = "alias"
        else:
            name = "anchor"
        self.forward()
        length = 0
        ch = self.peek(length)
        while ch not in "\0 \t\r\n\x85\u2028\u2029,[]{}":
            length += 1
            ch = self.peek(length)
        if not length:
            raise ScannerError(
                f"while scanning an {name}",
                start_mark,
                "expected alphabetic or numeric character, but found {!r}".format(
                    ch.encode("utf-8")
                ),
                self.get_mark(),
            )
        value = self.prefix(length)
        self.forward(length)
        ch = self.peek()
        if ch not in "\0 \t\r\n\x85\u2028\u2029?:,]}%@`":
            raise ScannerError(
                f"while scanning an {name}",
                start_mark,
                "expected alphabetic or numeric character, but found {!r}".format(
                    ch.encode("utf-8")
                ),
                self.get_mark(),
            )
        end_mark = self.get_mark()
        return TokenClass(value, start_mark, end_mark)


STATE_GET = 0  # Used only for get requests / no check yet.
STATE_POST_YES = 1  # Successful parse (YAML composed).
STATE_POST_NO = 2  # Failed parse.
COMMENTSTR = (
    "# This is a comment. Your YAML stream is good, but contains no documents. "
)


@dataclass(frozen=True)
class YamlCheckResult:
    """Outcome of checking a YAML text blob."""

    yamlstate: int
    yamlcanon: str = ""
    yamlerror: str = ""
    yamloriginal: str = ""

    def as_context(self) -> dict[str, int | str]:
        """Return a dict suitable for Django template context."""
        return {
            "yamlstate": self.yamlstate,
            "yamlcanon": self.yamlcanon,
            "yamlerror": self.yamlerror,
            "yamloriginal": self.yamloriginal,
        }


def empty_check_result() -> YamlCheckResult:
    """Return the default GET / unused-checker result."""
    return YamlCheckResult(yamlstate=STATE_GET)


def check_yaml(text: str | None) -> YamlCheckResult:
    """Compose *text* as YAML and return canonical form or an error.

    Args:
        text: Raw YAML source (typically from a form field). ``None`` is
            treated as a failed check.

    Returns:
        ``YamlCheckResult`` with success (canonical YAML) or failure details.
    """
    try:
        composition = compose_all(text, Loader12)
        yamlcanon = serialize_all(composition, canonical=True, allow_unicode=True)
        if len(yamlcanon) == 0:
            yamlcanon = COMMENTSTR
        return YamlCheckResult(yamlstate=STATE_POST_YES, yamlcanon=yamlcanon)
    except (YAMLError, AttributeError, TypeError) as e:
        return YamlCheckResult(
            yamlstate=STATE_POST_NO,
            yamlerror=str(e),
            yamloriginal=text if text is not None else "",
        )
