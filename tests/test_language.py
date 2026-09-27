"""Unit tests for MARC 008 -> sdo:inLanguage / BCP47 tag resolution."""

from __future__ import annotations

from rdflib import Graph, URIRef
from rdflib.namespace import Namespace

from biblio_etl.language import language_code_from_008, process

SDO = Namespace("http://schema.org/")
ITEM = URIRef("https://iisg.amsterdam/id/item/1")


def _text_008(lang_slot: str) -> str:
    """Build a synthetic 008 field with the given 3-char language code at
    the real position (characters 35-38)."""
    return " " * 35 + lang_slot + "x" * 5


def test_normal_language_code():
    assert language_code_from_008(_text_008("eng")) == "eng"


def test_space_means_no_language():
    assert language_code_from_008(_text_008("   ")) is None


def test_malformed_code_with_embedded_punctuation_is_rejected():
    """Regression test: real data hit an 008 whose language slot was
    'NL-' -- 3 characters, no space, but not alphabetic. Passing that
    straight through as a BCP47 language tag crashed a ~920,000-record-in
    full harvest (rdflib raises ValueError on an invalid tag rather than
    skipping it)."""
    assert language_code_from_008(_text_008("NL-")) is None

    g = Graph()
    lang_tag = process(ITEM, _text_008("NL-"), g)
    assert lang_tag is None
    assert len(g) == 0


def test_malformed_code_with_accented_letter_is_rejected():
    """Regression test: real data separately hit 'ìnd' (an accented
    'i' -- some encoding mangling of 'ind', presumably). str.isalpha()
    alone accepts accented Unicode letters, which BCP47 doesn't (ASCII
    only), so this crashed a later full-harvest run the same way."""
    assert language_code_from_008(_text_008("ìnd")) is None


def test_process_adds_in_language_and_returns_bcp47_tag():
    g = Graph()
    lang_tag = process(ITEM, _text_008("dut"), g)
    assert lang_tag == "nl"
    assert (ITEM, SDO.inLanguage, None) in g
