"""MARC datafield 700 (added entry - personal name / contributor).

Unlike ``f100.py``'s big cleaned/translated relator table, this field
matches a handful of *exact* relator strings verbatim (trailing period,
unstripped) against any sibling subfield's raw text.
"""

from __future__ import annotations

from rdflib import RDF, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, replace_first, mint_id, nl_amisg_id
from ..prefixes import IISGV, PERSON, RELATOR, SDO

_RELATOR_LITERALS = {
    "editor.": RELATOR.edt,
    "writer of afterword.": RELATOR.aft,
    "organizer.": RELATOR.orm,
    "collector.": RELATOR.col,
    "speaker.": RELATOR.spk,
    "editor of compilation.": RELATOR.edc,
}


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    for sub in subfields:
        if get_code(sub) != "0":
            continue
        person_id = nl_amisg_id(get_text(sub))
        if person_id is None:
            continue
        person = PERSON[mint_id(person_id)]

        for s2 in subfields:
            code2 = get_code(s2)
            text2 = get_text(s2)
            if text2 in _RELATOR_LITERALS:
                g.add((item, _RELATOR_LITERALS[text2], person))
                g.add((person, RDF.type, SDO.Person))
            if code2 == "a" and text2:
                name = replace_first(text2, ".")
                if name:
                    g.add((person, SDO.name, Literal(name)))
            elif code2 == "d" and text2:
                g.add((person, IISGV.date, Literal(text2)))
