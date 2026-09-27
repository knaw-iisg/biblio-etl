"""Small shared utilities used across the ``datafields`` handlers: normalizing
MARC subfield shapes, extracting IISG authority ids, minting safe IRIs, and
coercing text into typed RDF literals."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote, urlparse

from rdflib import XSD, Literal

PAREN_RE = re.compile(r"\([^()]*\)")

_DATATYPE_PATTERNS = {
    XSD.date: re.compile(r"^-?\d{4}-\d{2}-\d{2}$"),
    XSD.gYearMonth: re.compile(r"^-?\d{4}-\d{2}$"),
    XSD.gYear: re.compile(r"^-?\d{4}$"),
    XSD.integer: re.compile(r"^-?\d+$"),
}


def as_array(value: Any) -> list:
    """MARC subfields/datafields are a single dict when there's exactly one,
    or a list when there are several -- this normalizes both to a list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def get_code(subfield: dict) -> str | None:
    return subfield.get("@code")


def get_text(subfield: dict) -> str | None:
    text = subfield.get("$text")
    if text is None:
        return None
    return str(text)


def find_subfields(subfields: list[dict], code: str) -> list[dict]:
    return [s for s in subfields if get_code(s) == code]


def strip_parens(text: str) -> str:
    """Strip bracketed authority-source markers such as ``(NL-AMISG)`` from
    an identifier, e.g. ``(NL-AMISG)176035`` -> ``176035``."""
    return PAREN_RE.sub("", text)


def nl_amisg_id(text: str | None) -> str | None:
    """If ``text`` is an IISG-local authority reference (``(NL-AMISG)...`` or
    the ``(NL-AmISG)`` casing variant also seen in the source data), return
    the bare identifier; otherwise ``None``."""
    if not text:
        return None
    if text.startswith("(NL-AMISG)") or text.startswith("(NL-AmISG)"):
        stripped = strip_parens(text)
        return stripped or None
    return None


def replace_first(text: str, old: str, new: str = "") -> str:
    """Replace only the first occurrence of ``old`` (unlike ``str.replace``,
    which replaces all occurrences unless ``count`` is given explicitly)."""
    return text.replace(old, new, 1)


def mint_id(local_id: str) -> str:
    """Percent-encode characters that aren't valid in an IRI path segment,
    so an extracted identifier is safe to use as the local part of a minted
    IRI even when the source MARC data is messy (stray parentheses, spaces,
    slashes, ...)."""
    return quote(local_id, safe="")


def try_literal(text: str | None, datatypes: list) -> Literal | None:
    """Port of RATT's ``tryLiteral``: try each datatype in order (by
    lexical-form pattern, e.g. ``YYYY-MM-DD`` for ``xsd:date``) and return
    the value typed as the first one that matches; falls back to a plain
    ``xsd:string`` literal if ``XSD.string`` is in ``datatypes`` and nothing
    more specific matched, otherwise ``None``."""
    if not text:
        return None
    for dt in datatypes:
        if dt == XSD.string:
            return Literal(text)
        pattern = _DATATYPE_PATTERNS.get(dt)
        if pattern is not None and pattern.match(text):
            return Literal(text, datatype=dt)
    return None


def is_valid_authority_id(candidate: str | None) -> bool:
    """Sanity-check that an extracted identifier is safe to mint an IRI
    from: it must parse as a valid URL either as-is, or once appended to a
    throwaway ``https://`` base (the base itself is irrelevant -- this is
    purely a well-formedness probe, not a real namespace choice)."""
    if not candidate:
        return False
    url = candidate if candidate.startswith("https") else f"https://iisg.amsterdam/{candidate}"
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)
