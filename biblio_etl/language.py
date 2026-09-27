"""MARC 008 control field -> ``sdo:inLanguage``, plus resolving the same
language into a BCP47 tag for use on ``sdo:name``/``sdo:description``
literals elsewhere in the pipeline (NDE AP requires those language-tagged)."""

from __future__ import annotations

from rdflib import Graph, URIRef

from .prefixes import LEXVO_ISO639_3, LEXVO_ISO639_5, SDO

# ISO 639-5 (language family/group) codes: MARC language codes that are
# actually ISO 639-5 rather than 639-3 get minted under the 639-5 namespace.
IS_ISO_639_5 = {
    "afa", "alg", "apa", "art", "ath", "aus", "bad", "bai", "bat", "ber",
    "bnt", "btk", "cai", "cau", "cel", "cmc", "cpe", "cpf", "cpp", "crp",
    "cus", "day", "dra", "fiu", "gem", "ijo", "inc", "ine", "ira", "iro",
    "kar", "khi", "kro", "map", "mkh", "mno", "mun", "myn", "nah", "nai",
    "nic", "nub", "oto", "paa", "phi", "pra", "roa", "sai", "sal", "sem",
    "sgn", "sio", "sit", "sla", "smi", "son", "ssa", "tai", "tup", "tut",
    "wak", "wen", "ypk", "znd",
}

# MARC bibliographic language codes that differ from their ISO 639-3
# terminology-code equivalent.
MAPPING_ISO_639_3 = {
    "alb": "sqi", "arm": "hye", "baq": "eus", "bur": "mya", "cam": "khm",
    "chi": "zho", "cze": "ces", "dut": "nld", "esp": "epo", "eth": "gez",
    "far": "fao", "fre": "fra", "fri": "fry", "gae": "gla", "gag": "glg",
    "gal": "orm", "geo": "kat", "ger": "deu", "gre": "ell", "gua": "grn",
    "ice": "isl", "int": "ina", "iri": "gle", "kus": "kos", "lan": "oci",
    "mac": "mkd", "mao": "mri", "max": "glv", "may": "msa", "mla": "mlg",
    "per": "fas", "rum": "ron", "sao": "smo", "sho": "sna", "slo": "slk",
    "snh": "sin", "sso": "sot", "swz": "ssw", "tag": "tgl", "taj": "tgk",
    "tar": "tat", "tib": "bod", "tru": "chk", "tsw": "tsn", "wel": "cym",
}


# Small ISO 639-3 -> BCP47 primary-language-subtag map for the languages
# most common in the IISG catalogue. Codes not listed here fall back to
# using the ISO 639-3 code itself, which is valid BCP47 (RFC 5646 permits a
# 3-letter primary subtag from ISO 639-3 when no 2-letter ISO 639-1 code
# exists) even if less idiomatic than e.g. "nl" for Dutch.
ISO_639_3_TO_BCP47 = {
    "eng": "en", "nld": "nl", "dut": "nl", "fra": "fr", "fre": "fr",
    "deu": "de", "ger": "de", "spa": "es", "ita": "it", "por": "pt",
    "rus": "ru", "tur": "tr", "ara": "ar", "zho": "zh", "chi": "zh",
    "jpn": "ja",
}


def language_code_from_008(text_008: str) -> str | None:
    """Extract the MARC language code from control field 008 (characters
    35-38, 0-indexed). Returns ``None`` when the field is too short, the
    slot contains a space (meaning "no language given"), or the slot isn't
    3 plain ASCII letters -- confirmed necessary against real data twice:
    an 008 field with language slot "NL-" (3 chars, no space, not a real
    code), and separately "ìnd" (an accented "i" -- some encoding
    mangling of "ind", presumably) -- str.isalpha() alone accepts accented
    Unicode letters, which are not valid in a BCP47 primary language
    subtag (ASCII only per RFC 5646), so that check alone wasn't enough.
    Both reached rdflib's BCP47 literal-tag validation as an invalid tag,
    which raises rather than being skipped.
    """
    lang = text_008[35:38]
    if len(lang) != 3 or not lang.isascii() or not lang.isalpha():
        return None
    return lang


def language_iri(lang_code: str) -> URIRef:
    resolved = MAPPING_ISO_639_3.get(lang_code, lang_code)
    ns = LEXVO_ISO639_5 if lang_code in IS_ISO_639_5 else LEXVO_ISO639_3
    return ns[resolved]


def bcp47_tag(lang_code: str) -> str:
    return ISO_639_3_TO_BCP47.get(lang_code, lang_code)


def process(item: URIRef, text_008: str, g: Graph) -> str | None:
    """Add ``sdo:inLanguage`` and return the resolved BCP47 tag (or
    ``None`` if 008 doesn't resolve to a language), so the caller can thread
    it into ``sdo:name``/``sdo:description`` literals."""
    lang_code = language_code_from_008(text_008)
    if lang_code is None:
        return None
    g.add((item, SDO.inLanguage, language_iri(lang_code)))
    return bcp47_tag(lang_code)
