"""MARC datafield 650 (subject added entry - topical term) ->
``iisgv:topic`` / ``iisgv:form``, depending on which authority the subfield
``$0``/``$a`` reference points at:

- ``(NL-AMISG)...`` / ``(NL-AmISG)...``: an IISG-local topic authority id.
- ``(NL-LeOCL)...``: an external topic reference, minted from the full
  bracketed string (there's no separate numeric id to extract here).
- ``(OCoLC)fst0...`` / ``(OCoLC)...``: a WorldCat FAST id, recorded as a
  ``iisgv:form`` link.
"""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array, get_text, mint_id, nl_amisg_id
from ..prefixes import IISGV, TOPIC, WORLDCAT_FAST

_LEOCL_PREFIX = "(NL-LeOCL)"
_OCLC_PREFIX = "(OCoLC)"
_OCLC_FST0_PREFIX = "(OCoLC)fst0"


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        text = get_text(sub)
        if not text:
            continue

        if text.startswith("(NL-AMISG)") or text.startswith("(NL-AmISG)"):
            topic_id = nl_amisg_id(text)
            if topic_id:
                g.add((item, IISGV.topic, TOPIC[mint_id(topic_id)]))
        elif text.startswith(_LEOCL_PREFIX):
            g.add((item, IISGV.topic, TOPIC[mint_id(text)]))
        elif text.startswith(_OCLC_PREFIX):
            suffix = text[len(_OCLC_FST0_PREFIX):] if text.startswith(_OCLC_FST0_PREFIX) else text[len(_OCLC_PREFIX):]
            if suffix:
                g.add((item, IISGV.form, WORLDCAT_FAST[mint_id(suffix)]))
