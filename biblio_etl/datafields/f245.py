"""MARC datafield 245 (title statement) -> language-tagged ``sdo:name``.

Picking which subfields make up the title collapses to two cases:

- subfield 0 has code 'a': use its text, plus subfield 1's text appended
  with a space if subfield 1 has code 'b'.
- exactly 4 subfields, subfield 0 has code '6' (alternate-graphic linkage)
  and subfield 1 has code 'a': use subfield 1's text, plus subfield 2's text
  appended with a space if subfield 2 has code 'b'.
"""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array, get_code, get_text, lang_literal
from ..prefixes import SDO


def process(item: URIRef, datafield: dict, g: Graph, lang: str | None = None) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    codes = [get_code(s) for s in subfields]
    texts = [get_text(s) for s in subfields]

    def add(name: str | None) -> None:
        if name:
            g.add((item, SDO.name, lang_literal(name, lang)))

    if not codes:
        return

    if codes[0] == "a":
        if len(codes) >= 2 and codes[1] == "b" and texts[1]:
            add(f"{texts[0]} {texts[1]}")
        else:
            add(texts[0])
    elif len(codes) == 4 and codes[1] == "a":
        if codes[0] == "6" and codes[2] == "b" and texts[2]:
            add(f"{texts[1]} {texts[2]}")
        else:
            add(texts[1])
