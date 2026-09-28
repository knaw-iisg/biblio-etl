"""Unit tests for a handful of individual datafield handlers, using small
hand-built MARC subfield snippets (independent of the OAI fixtures)."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import Namespace

from biblio_etl.datafields import f035, f044, f100, f245, f260, f902

SDO = Namespace("https://schema.org/")
IISGV = Namespace("https://iisg.amsterdam/vocab/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
PERSON = Namespace("https://iisg.amsterdam/authority/person/")

ITEM = URIRef("https://iisg.amsterdam/id/item/1")


def test_f044_country():
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "Turkey"}}
    f044.process(ITEM, datafield, g)
    assert (ITEM, IISGV.country, Literal("Turkey")) in g


def test_f035_oclc_sameas():
    g = Graph()
    datafield = {"marc:subfield": [
        {"@code": "a", "$text": "(IISG)IISGb10691325"},
        {"@code": "a", "$text": "(OCoLC)81515467"},
    ]}
    f035.process(ITEM, datafield, g)
    assert (ITEM, OWL.sameAs, URIRef("http://www.worldcat.org/oclc/81515467")) in g


def test_f245_title_with_subtitle():
    g = Graph()
    datafield = {"marc:subfield": [
        {"@code": "a", "$text": "Sanayi ve üniversite :"},
        {"@code": "b", "$text": "haberleşme ve işbirliğinin yeni şekilleri /"},
        {"@code": "c", "$text": "DPT Sosyal Planlama Başkanliği."},
    ]}
    f245.process(ITEM, datafield, g)
    names = list(g.objects(ITEM, SDO.name))
    assert len(names) == 1
    assert str(names[0]) == "Sanayi ve üniversite : haberleşme ve işbirliğinin yeni şekilleri /"


def test_f100_creator_with_relator():
    g = Graph()
    datafield = {"marc:subfield": [
        {"@code": "0", "$text": "(NL-AMISG)176035"},
        {"@code": "a", "$text": "Kulin, Nikolaj Ernestovič"},
        {"@code": "e", "$text": "editor."},
    ]}
    f100.process(ITEM, datafield, g)
    person = PERSON["176035"]
    assert (ITEM, SDO.creator, person) in g
    assert (person, SDO.name, Literal("Kulin, Nikolaj Ernestovič")) in g
    relator_edt = URIRef("http://id.loc.gov/vocabulary/relators/edt")
    assert (ITEM, relator_edt, person) in g


def test_f260_publication():
    g = Graph()
    datafield = {"marc:subfield": [
        {"@code": "a", "$text": "Ankara :"},
        {"@code": "b", "$text": "DPT,"},
        {"@code": "c", "$text": "1989."},
    ]}
    f260.process(ITEM, datafield, g)
    assert (ITEM, IISGV.placeOfPublication, Literal("Ankara")) in g
    assert (ITEM, IISGV.publisher, Literal("DPT")) in g
    dates = {str(o) for o in g.objects(ITEM, IISGV.dateOfPublication)}
    assert "1989" in dates


def test_f245_falls_back_to_untagged_on_invalid_lang():
    """Defense-in-depth regression test: even if an invalid BCP47 tag ever
    reaches a datafield handler (language.py validates before returning
    one, but this is the independent second line of defense that actually
    stopped a full-harvest crash), the handler must fall back to an
    untagged literal instead of raising."""
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "Some title"}}
    f245.process(ITEM, datafield, g, lang="not a real tag")
    names = list(g.objects(ITEM, SDO.name))
    assert names == [Literal("Some title")]


def test_f902_handle_url():
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "10622\\615E1D29-8D79-4B1D-AF85-56814F99937B"}}
    f902.process(ITEM, datafield, g)
    values = list(g.objects(ITEM, IISGV.nativeViewer))
    assert len(values) == 1
    assert str(values[0]) == "http://hdl.handle.net/10622/615E1D29-8D79-4B1D-AF85-56814F99937B"
