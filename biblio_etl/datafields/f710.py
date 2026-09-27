"""MARC datafield 710 (added entry - corporate name), linked with the
``relator:cre`` predicate."""

from __future__ import annotations

from rdflib import RDF, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, is_valid_authority_id, replace_first, mint_id, nl_amisg_id
from ..prefixes import ORGANIZATION, RELATOR, SDO


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    for sub in subfields:
        if get_code(sub) != "0":
            continue
        org_id = nl_amisg_id(get_text(sub))
        if org_id is None or not is_valid_authority_id(org_id):
            continue
        org = ORGANIZATION[mint_id(org_id)]
        g.add((item, RELATOR.cre, org))
        g.add((org, RDF.type, SDO.Organization))
        for s2 in subfields:
            if get_code(s2) != "a":
                continue
            text2 = get_text(s2)
            if not text2:
                continue
            name = replace_first(text2, ".")
            if name:
                g.add((org, SDO.name, Literal(name)))
