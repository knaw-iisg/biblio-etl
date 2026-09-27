"""Per-record OAI/MARC-JSON -> RDF pipeline."""

from __future__ import annotations

from rdflib import RDF, Graph, URIRef

from . import nde_ap
from .context import as_array
from .datafields import DATAFIELD_HANDLERS, f008
from .leader import type_from_leader
from .prefixes import ITEM

_OAI_ID_PREFIX = "oai:socialhistoryservices.org:"

# Datafield handlers that need the record's resolved language (from 008) to
# language-tag the literals they write.
_LANG_AWARE_TAGS = {"245", "500"}


def item_iri_from_record(record: dict) -> URIRef | None:
    identifier = record.get("header", {}).get("identifier")
    if not identifier:
        return None
    local_id = identifier[len(_OAI_ID_PREFIX):] if identifier.startswith(_OAI_ID_PREFIX) else identifier
    if not local_id:
        return None
    return ITEM[local_id]


def process_record(record: dict, g: Graph) -> URIRef | None:
    """Process a single OAI-harvested biblio record (already parsed from
    MARCXML into the ``marc:record``-style JSON shape used by
    ``static/biblio/sourceData/*.json``) into ``g``. Returns the minted
    item IRI, or ``None`` if the record has no usable identifier."""
    item = item_iri_from_record(record)
    if item is None:
        return None

    marc_record = record.get("metadata", {}).get("marc:record", {})

    leader = marc_record.get("marc:leader", {})
    leader_text = leader.get("$text") if isinstance(leader, dict) else None
    if leader_text:
        rdf_type = type_from_leader(str(leader_text))
        if rdf_type is not None:
            g.add((item, RDF.type, rdf_type))

    lang: str | None = None
    for controlfield in as_array(marc_record.get("marc:controlfield")):
        if controlfield.get("@tag") == "008":
            text_008 = controlfield.get("$text")
            if text_008:
                lang = f008.process(item, str(text_008), g)

    for datafield in as_array(marc_record.get("marc:datafield")):
        tag = datafield.get("@tag")
        for handler in DATAFIELD_HANDLERS.get(tag, []):
            if tag in _LANG_AWARE_TAGS:
                handler(item, datafield, g, lang=lang)
            else:
                handler(item, datafield, g)

    nde_ap.enrich(item, record, g)

    return item
