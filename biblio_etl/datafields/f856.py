"""MARC datafield 856 ($u electronic location) -> ``sdo:contentUrl``, as a
link into IISG's IIIF Universal Viewer.

IISG puts a digitised item's digital-object handle in 856 $u
(``https://hdl.handle.net/10622/N30051001508412``), separate from the
catalogue record's own handle in 902 ($a). With ``?locatt=view:manifest``
that handle resolves to the item's IIIF manifest. The link is emitted in
exactly the shape findingaid-etl uses for EAD ``<daoloc>`` manifests, so
iisg-iiif can harvest both the same way. Non-IISG URLs in 856 aren't
mapped.
"""

from __future__ import annotations

import re

from rdflib import Graph, URIRef

from ..context import as_array, get_code, get_text
from ..prefixes import SDO

UNIVERSAL_VIEWER_PREFIX = "https://access.iisg.amsterdam/universalviewer/#?manifest="

_HANDLE_RE = re.compile(r"^https?://hdl\.handle\.net/10622/([^?#\s]+)")


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        if get_code(sub) != "u":
            continue
        match = _HANDLE_RE.match((get_text(sub) or "").strip())
        if not match:
            continue
        manifest = f"https://hdl.handle.net/10622/{match.group(1)}?locatt=view:manifest"
        g.add((item, SDO.contentUrl, URIRef(UNIVERSAL_VIEWER_PREFIX + manifest)))
