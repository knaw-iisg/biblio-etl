# biblio-etl

Maps IISG's OAI-PMH-harvested MARCXML biblio catalogue to RDF: mostly
schema.org, plus a small `iisgv:` vocabulary for fields with no natural
schema.org home, and conforming to the [NDE Schema.org Application
Profile](https://docs.nde.nl/schema-profile/) (SCHEMA-AP-NDE) -- persistent
item URIs, language-tagged `sdo:name`/`sdo:description`,
`sdo:sdDatePublished`, `sdo:isPartOf` a dataset, and `sdo:DefinedTerm`
typing for controlled-vocabulary subject/genre/form terms (see
`biblio_etl/nde_ap.py`'s docstring for exactly what's covered and what's
left as a `TODO(IISG)`, namely the dataset's NDE Dataset Register
registration -- license, catalog and access-rights IRIs aren't derivable
from this codebase).

## Install

```bash
python -m venv .venv
.venv/bin/pip install -e ".[test]"
```

## Run

```bash
# All sample records under static/biblio/sourceData/:
python -m biblio_etl.cli --source fixtures --out biblio.ttl

# Just one record, printed to stdout:
python -m biblio_etl.cli --source fixtures --record-id 978600

# Live OAI-PMH harvest of the full iish.evergreen.biblio set (slow -- add --limit):
python -m biblio_etl.cli --source oai --limit 50 --out biblio.ttl
```

## Test

```bash
.venv/bin/pytest
```

`tests/test_pipeline_fixtures.py` runs every fixture under
`static/biblio/sourceData/` through the pipeline and spot-checks known
fields (title, publisher, place, date, language tag, AP enrichment) for
`collections978600.json`. `tests/test_datafields.py` unit-tests individual
field handlers directly.

## Layout

- `biblio_etl/datafields/f<tag>.py` -- one MARC datafield tag per module.
- `biblio_etl/pipeline.py` -- per-record orchestration: leader -> type,
  008 -> language, then dispatches each datafield by tag.
- `biblio_etl/nde_ap.py` -- record-level NDE AP enrichment (dataset link,
  `sdDatePublished`, `DefinedTerm` typing), applied after field mapping.
- `biblio_etl/harvest.py` -- OAI-PMH client; `static/biblio/sourceData/`
  fixtures are interchangeable inputs with it for `pipeline.process_record`.
