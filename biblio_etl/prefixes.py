"""Namespace/prefix declarations used throughout the pipeline."""

from rdflib import Namespace

BASE = "https://iisg.amsterdam/"
AUTHORITY = BASE + "authority/"
ID = BASE + "id/"

# Core IISG namespaces
ITEM = Namespace(ID + "item/")
DATASET = Namespace(ID + "dataset/")
PERSON = Namespace(AUTHORITY + "person/")
ORGANIZATION = Namespace(AUTHORITY + "organization/")
EVENT = Namespace(AUTHORITY + "event/")
PLACE = Namespace(AUTHORITY + "place/")
TOPIC = Namespace(AUTHORITY + "topic/")
PERIOD = Namespace(AUTHORITY + "period/")
FORM = Namespace(AUTHORITY + "form/")
TITLE = Namespace(AUTHORITY + "title/")

IISGV = Namespace(BASE + "vocab/")
MARC = Namespace(BASE + "marc/")

# External vocabularies
SDO = Namespace("http://schema.org/")
RELATOR = Namespace("http://id.loc.gov/vocabulary/relators/")
IISG_REL = Namespace("https://iisg.amsterdam/relators/")
OCLC = Namespace("http://www.worldcat.org/oclc/")
WORLDCAT_FAST = Namespace("http://id.worldcat.org/fast/")
LEXVO_ISO639_3 = Namespace("http://lexvo.org/id/iso639-3/")
LEXVO_ISO639_5 = Namespace("http://lexvo.org/id/iso639-5/")
HANDLE = Namespace("http://hdl.handle.net/10622/")
AAT = Namespace("https://vocab.getty.edu/aat/")
DCM = Namespace("http://purl.org/dc/dcmitype/")

DEFAULT_GRAPH = "https://iisg.amsterdam/graph/biblio"

# All namespaces, used for Turtle/TriG serialization prefixes.
NAMESPACE_BINDINGS = {
    "item": ITEM,
    "dataset": DATASET,
    "person": PERSON,
    "organization": ORGANIZATION,
    "event": EVENT,
    "place": PLACE,
    "topic": TOPIC,
    "period": PERIOD,
    "form": FORM,
    "title": TITLE,
    "iisgv": IISGV,
    "marc": MARC,
    "sdo": SDO,
    "relator": RELATOR,
    "iisgRel": IISG_REL,
    "oclc": OCLC,
    "fast": WORLDCAT_FAST,
    "iso639-3": LEXVO_ISO639_3,
    "iso639-5": LEXVO_ISO639_5,
    "handle": HANDLE,
    "aat": AAT,
    "dcm": DCM,
}
