"""MARC datafield 655 (index term - genre/form) -> ``iisgv:form``, typed
and labeled from a sibling ``$a`` subfield, or a WorldCat FAST id."""

from __future__ import annotations

from rdflib import OWL, RDF, RDFS, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, is_valid_authority_id, mint_id, nl_amisg_id
from ..prefixes import AAT, FORM, IISGV, WORLDCAT_FAST

_OCLC_FST0_PREFIX = "(OCoLC)fst0"

# The single AAT term ("Print") the original data associates with this field.
_PRINT_AAT = AAT["300041273"]


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    for sub in subfields:
        text = get_text(sub)
        if not text:
            continue

        form_id = nl_amisg_id(text)
        if form_id is not None:
            if is_valid_authority_id(form_id):
                form = FORM[mint_id(form_id)]
                g.add((item, IISGV.form, form))
                g.add((form, RDF.type, IISGV.Form))
                g.add((form, OWL.sameAs, _PRINT_AAT))
                for s2 in subfields:
                    if get_code(s2) == "a" and get_text(s2):
                        g.add((form, RDFS.label, Literal(get_text(s2))))
            continue

        if text.startswith(_OCLC_FST0_PREFIX):
            suffix = text[len(_OCLC_FST0_PREFIX):]
            if suffix and is_valid_authority_id(suffix):
                g.add((item, IISGV.form, WORLDCAT_FAST[mint_id(suffix)]))
