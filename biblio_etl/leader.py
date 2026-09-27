"""MARC leader positions 6-7 -> ``rdf:type``. The item's type is determined
once per record, from the leader, before any datafield is processed."""

from __future__ import annotations

from rdflib import Namespace

from .prefixes import DCM, SDO

LEADER_TYPE = {
    "am": SDO.Book,
    "ac": SDO.Book,
    "as": SDO.CreativeWorkSeries,
    "ab": SDO.Article,
    "gm": SDO.VideoObject,
    "gc": SDO.VideoObject,
    "im": SDO.AudioObject,
    "ic": SDO.AudioObject,
    "jm": SDO.MusicRecording,
    "jc": SDO.MusicRecording,
    "km": SDO.ImageObject,
    "kc": SDO.ImageObject,
    "rm": DCM.PhysicalObject,
    "rc": DCM.PhysicalObject,
}


def type_from_leader(leader_text: str) -> Namespace | None:
    """``leader_text`` is the full MARC leader string; positions 6-7
    (0-indexed) give the type-of-record + bibliographic-level code pair."""
    type_of_record = leader_text[6:8]
    return LEADER_TYPE.get(type_of_record)
