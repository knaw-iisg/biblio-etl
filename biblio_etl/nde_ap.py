"""NDE Schema.org Application Profile (SCHEMA-AP-NDE) enrichment, applied to
every record after its MARC fields are mapped.

Reference: https://docs.nde.nl/schema-profile/ -- per-item (``CreativeWork``)
requirements used here:

- required: persistent URI (items are minted at ``item:<id>``),
  language-tagged ``sdo:name``/``sdo:description`` (handled directly by
  ``datafields/f245.py``/``f500.py`` via the language resolved from MARC 008
  -- see ``pipeline.py``), ``sdo:sdDatePublished``.
- recommended: ``sdo:isPartOf`` linking to the dataset; controlled-vocabulary
  terms (``sdo:about``, ``iisgv:topic``, etc.) modeled as ``sdo:DefinedTerm``
  with ``sdo:sameAs`` to an authoritative IRI where one is known.

What this deliberately does *not* do: register the Biblio dataset in the NDE
Dataset Register. That needs a license IRI, catalog IRI and access-rights
statement that aren't derivable from this codebase -- see the ``# TODO(IISG)``
markers below. A minimal ``sdo:Dataset`` node is still emitted so that
``sdo:isPartOf`` resolves to something.
"""

from __future__ import annotations

from rdflib import OWL, RDF, Graph, Literal, URIRef

from .prefixes import DATASET, IISGV, SDO

DATASET_IRI = DATASET["biblio"]

# Predicates whose objects are IISG-minted controlled-vocabulary authority
# entities (people, places, topics, forms, ...) that the item is "about" in
# some sense -- as opposed to sdo:creator/relator:* predicates, which name a
# contributor rather than a subject term, and are left untouched.
CONTROLLED_VOCAB_PREDICATES = (
    SDO.about,
    IISGV.topic,
    IISGV.form,
    IISGV.period,
    IISGV.title,
    IISGV.seriesTitle,
)


def _emit_dataset_description(g: Graph) -> None:
    if (DATASET_IRI, RDF.type, SDO.Dataset) in g:
        return
    g.add((DATASET_IRI, RDF.type, SDO.Dataset))
    g.add((DATASET_IRI, SDO.name, Literal("IISG Bibliotheekcatalogus", lang="nl")))
    g.add((DATASET_IRI, SDO.name, Literal("IISH Library Catalogue", lang="en")))
    g.add((DATASET_IRI, SDO.description, Literal(
        "Bibliografische beschrijvingen uit de bibliotheekcatalogus van het "
        "Internationaal Instituut voor Sociale Geschiedenis (IISG).", lang="nl",
    )))
    # TODO(IISG): sdo:license (a license IRI), sdo:includedInDataCatalog (the
    # NDE Dataset Register catalog IRI this dataset is registered under) and
    # sdo:accessRights aren't in the source pipeline or its config, and
    # shouldn't be guessed -- fill in once known.


def enrich(item: URIRef, record: dict, g: Graph, *, dataset_iri: URIRef = DATASET_IRI) -> None:
    datestamp = record.get("header", {}).get("datestamp")
    if datestamp:
        g.add((item, SDO.sdDatePublished, Literal(str(datestamp))))

    g.add((item, SDO.isPartOf, dataset_iri))
    _emit_dataset_description(g)

    # iisgv:dateOfPublication already carries a (sometimes typed) date value
    # from f260.py; mirror it under the standard schema.org property too, so
    # it's visible to AP-conformant consumers that don't know the iisgv:
    # vocabulary.
    for date_value in g.objects(item, IISGV.dateOfPublication):
        g.add((item, SDO.datePublished, date_value))
        break

    for predicate in CONTROLLED_VOCAB_PREDICATES:
        for obj in g.objects(item, predicate):
            if not isinstance(obj, URIRef):
                continue
            g.add((obj, RDF.type, SDO.DefinedTerm))
            # If the entity already carries an owl:sameAs to an external
            # authority (Getty AAT, WorldCat FAST, ...), mirror it as
            # sdo:sameAs -- the property the AP expects DefinedTerm nodes to
            # carry. A *new* sameAs is deliberately not invented when no
            # external authority link exists: the node's own IRI already is
            # its stable identity, so a self sdo:sameAs would be redundant.
            for external in g.objects(obj, OWL.sameAs):
                g.add((obj, SDO.sameAs, external))
