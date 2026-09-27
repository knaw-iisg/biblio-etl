"""Runs every static/biblio/sourceData fixture through the full pipeline."""

from __future__ import annotations

from pathlib import Path

import pytest
from rdflib import Graph, URIRef
from rdflib.namespace import Namespace

from biblio_etl.fixtures import load_fixture
from biblio_etl.pipeline import process_record

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "static" / "biblio" / "sourceData"
SDO = Namespace("http://schema.org/")
IISGV = Namespace("https://iisg.amsterdam/vocab/")


def _fixture_paths():
    return sorted(FIXTURES_DIR.glob("*.json"))


@pytest.mark.parametrize("path", _fixture_paths(), ids=lambda p: p.stem)
def test_record_processes_without_error(path: Path):
    record = load_fixture(path)
    g = Graph()
    item = process_record(record, g)
    assert item is not None
    assert len(g) > 0


def test_item_978600_known_fields():
    record = load_fixture(FIXTURES_DIR / "collections978600.json")
    g = Graph()
    item = process_record(record, g)

    assert item == URIRef("https://iisg.amsterdam/id/item/978600")

    names = {str(o) for o in g.objects(item, SDO.name)}
    assert any("Sanayi ve üniversite" in n for n in names)

    publishers = {str(o) for o in g.objects(item, IISGV.publisher)}
    assert "DPT" in publishers

    places = {str(o) for o in g.objects(item, IISGV.placeOfPublication)}
    assert "Ankara" in places

    dates = {str(o) for o in g.objects(item, IISGV.dateOfPublication)}
    assert any(d.startswith("1989") for d in dates)


def test_name_is_language_tagged_from_008():
    record = load_fixture(FIXTURES_DIR / "collections978600.json")
    g = Graph()
    item = process_record(record, g)

    names = list(g.objects(item, SDO.name))
    assert names
    assert names[0].language == "tr"


def test_nde_ap_dataset_link_and_sd_date_published():
    record = load_fixture(FIXTURES_DIR / "collections978600.json")
    g = Graph()
    item = process_record(record, g)

    assert (item, SDO.isPartOf, URIRef("https://iisg.amsterdam/id/dataset/biblio")) in g
    assert list(g.objects(item, SDO.sdDatePublished))
