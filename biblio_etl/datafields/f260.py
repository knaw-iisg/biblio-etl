"""MARC datafield 260 (publication, distribution, etc.).

$c (date of publication) is parsed several ways, and every parse that
succeeds is asserted as an additional ``iisgv:dateOfPublication`` value: a
specific day/month/year reading when the text has that shape, plus a
generically typed (``xsd:date``/``gYearMonth``/``gYear``/``string``) reading
of the whole cleaned string.
"""

from __future__ import annotations

import re

from rdflib import XSD, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, replace_first, try_literal
from ..prefixes import IISGV

_MONTHS = {
    "januari": "01", "january": "01",
    "februari": "02", "february": "02",
    "maart": "03", "march": "03",
    "april": "04",
    "mei": "05", "may": "05",
    "juni": "06", "june": "06",
    "juli": "07", "july": "07",
    "augustus": "08", "august": "08",
    "september": "09",
    "oktober": "10", "october": "10",
    "november": "11",
    "december": "12",
}

_NON_DIGIT_RUN_RE = re.compile(r"\D+")


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        code = get_code(sub)
        text = get_text(sub)
        if not text:
            continue
        if code == "c":
            _process_date_issued(g, item, text)
        elif code == "b":
            publisher = replace_first(text, ",")
            if publisher:
                g.add((item, IISGV.publisher, Literal(publisher)))
        elif code == "a":
            place = replace_first(text, " :")
            if place:
                g.add((item, IISGV.placeOfPublication, Literal(place)))
        elif code == "g":
            digits = _NON_DIGIT_RUN_RE.sub("", text, count=1)
            literal = try_literal(digits, [XSD.date, XSD.gYearMonth, XSD.gYear, XSD.string])
            if literal is not None:
                g.add((item, IISGV.dateOfManufacture, literal))
        elif code == "f":
            manufacturer = text.split(")", 1)[0]
            if manufacturer:
                g.add((item, IISGV.manufacturer, Literal(manufacturer)))
        elif code == "e":
            place = re.sub(r"[^a-zA-Z']", "", text)
            if place:
                g.add((item, IISGV.placeOfManufacture, Literal(place)))


def _process_date_issued(g: Graph, item: URIRef, text: str) -> None:
    text_c = replace_first(text, ".")
    if not text_c:
        return

    separated = text_c.split(", ")
    year = separated[0] if separated else None
    rest = separated[1] if len(separated) > 1 else None

    if rest:
        rest_parts = rest.split(" ")
        if len(rest_parts) >= 2:
            month = _MONTHS.get(rest_parts[1])
            if month:
                day_parts = rest_parts[0].split("-")
                day = day_parts[0] if day_parts else None
                if day and day.isdigit():
                    day_num = int(day)
                    padded_day = f"0{day}" if day_num < 10 else day
                    if year:
                        g.add((item, IISGV.dateOfPublication, Literal(f"{year}-{month}-{padded_day}")))
        elif len(rest_parts) == 1:
            month = _MONTHS.get(rest_parts[0])
            if month and year:
                g.add((item, IISGV.dateOfPublication, Literal(f"{year}-{month}")))

    literal = try_literal(text_c, [XSD.date, XSD.gYearMonth, XSD.gYear, XSD.string])
    if literal is not None:
        g.add((item, IISGV.dateOfPublication, literal))
