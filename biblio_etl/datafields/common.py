"""Shared "linked authority entity" pattern used by most 1XX/6XX/7XX/8XX
datafield handlers: a subfield ``$0`` carries an ``(NL-AMISG)<id>`` authority
reference, from which an entity IRI is minted and linked from the item; a
sibling subfield ``$a`` (usually) supplies that entity's display name/label.
"""

from __future__ import annotations

from rdflib import RDF, Graph, Literal, Namespace, URIRef

from ..context import get_code, get_text, replace_first, mint_id, nl_amisg_id


def link_authority_entity(
    g: Graph,
    item: URIRef,
    subfields: list[dict],
    *,
    predicate: URIRef,
    ns: Namespace,
    cls: URIRef | None,
    name_predicate: URIRef | None = None,
    id_code: str | None = "0",
    name_code: str = "a",
) -> list[URIRef]:
    """Mint/link one entity per matching subfield, then (optionally) apply
    a name/label from sibling ``name_code`` subfields to every entity minted
    this call. Returns the minted entity IRIs."""
    entities: list[URIRef] = []
    for sub in subfields:
        if id_code is not None and get_code(sub) != id_code:
            continue
        entity_id = nl_amisg_id(get_text(sub))
        if entity_id is None:
            continue
        entity = ns[mint_id(entity_id)]
        g.add((item, predicate, entity))
        if cls is not None:
            g.add((entity, RDF.type, cls))
        entities.append(entity)

    if name_predicate is not None and entities:
        for sub in subfields:
            if get_code(sub) != name_code:
                continue
            text = get_text(sub)
            if not text:
                continue
            name = replace_first(text, ".")
            if not name:
                continue
            for entity in entities:
                g.add((entity, name_predicate, Literal(name)))

    return entities
