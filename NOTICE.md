# Notices, attribution and provenance

## What is in this repository, and who owns it

Everything committed here, the lessons, the explanations, the diagrams, the
brief, the build scripts, the checkers and the course document, was written
for this project and is copyright © 2026 Peter Winstanley, released under the
MIT License in [LICENSE](LICENSE).

The dataset in `data/` is the [SPARQL course](https://github.com/pwin/SPARQL_Course)'s
Bookshop Trail, by the same author under the same licence, copied here
unchanged so that this repository stands on its own. The one file this course
adds to `data/` is `the-brief.md`, written for this project.

No third-party text, data or code is copied into this repository. Where a
lesson quotes a definition or a sentence from a published source, it is a short
quotation with the source named beside it.

## The dataset is fiction

**The places are real. Everything else is invented.** The
[SPARQL course's NOTICE](https://github.com/pwin/SPARQL_Course/blob/main/NOTICE.md)
sets this out in full. The brief and the lessons name the same invented shops,
people, publishers and works, and add a few more in the same spirit: a
committee, its meetings, a renamed shop, a second edition.

> Any resemblance between a bookshop, publisher, author or book in this course
> and a real one is coincidental. Names were chosen to sound plausible for their
> setting, and with a plausible name in a real town some collision is
> statistically inevitable; none is intended, and nothing here is a statement
> about any real business or person. If you find a collision that troubles you,
> open an issue and it will be renamed.

## Vocabularies and ontologies referenced

The lessons use terms from published vocabularies by IRI and, where a file must
stand on its own in OWL 2 DL, declare them locally with `rdfs:isDefinedBy`
pointing at the owner. No definitions are copied.

| Vocabulary or ontology | Publisher | Licence |
|---|---|---|
| RDF, RDFS, OWL 2, SKOS, SHACL, PROV-O | W3C | W3C Document Licence |
| Dublin Core Terms (`dct:`) | DCMI | CC-BY 4.0 |
| VANN (`vann:`) | Ian Davis | CC-BY |
| GeoSPARQL (`geo:`, `sf:`), WGS84 (`wgs84:`) | OGC, W3C | as published |
| gist (`gist:`, `gistd:`), gistBFO, gistUFO | Semantic Arts | CC-BY 4.0 |
| gUFO (`gufo:`) | NEMO, Universidade Federal do Espírito Santo | CC-BY 4.0 |
| BFO 2020 (`obo:BFO_*`) | The BFO Consortium | CC-BY 4.0 |
| Wikidata (`wd:`), one IRI in o39 | Wikimedia | CC0 |

The course's own annotation namespace for the OntoClean marks,
`https://example.org/bookshop-trail/ontoclean#`, and the Trail's schema and
data namespaces use `https://example.org/`, which RFC 6761 reserves for
documentation and examples. Nothing at those IRIs resolves, and lesson o72
says so.

## Sources cited

The lessons cite, by link, the OWL 2, RDF 1.2, SKOS and SHACL Recommendations;
the Web Architecture, Cool URIs, Linked Data and Vocabulary Publishing notes;
Ogden and Richards' triangle of reference; Guarino and Welty's OntoClean
papers; Guizzardi's gUFO; Duque-Ramos, Fernández-Breis, Stevens and
Aussenac-Gilles' OQuaRE; ANSI/NISO Z39.19; the OBO Foundry principles; the
gist Style Guide, Namespace document and Deprecation and Deletion Policy; the
gistBFO README and mapping notes; the SemOps Manual; the Ontology Quality
Suite; a Semantic Arts blog post; and a conference paper, Is an upper ontology useful? (ISKO UK 2023, CEUR-WS). `scripts/check_links.py` confirms
each link still lands. Quotations are short and attributed where they occur.

## Tools used, and not redistributed

Nothing under `lib/` is committed. `scripts/setup-tools.ps1` fetches each item
from where its owner publishes it, under its own licence:

| Item | What for | Licence |
|---|---|---|
| [ROBOT](https://github.com/ontodev/robot) | the OWL API, HermiT and the OWL 2 profile checker: every "in profile", "consistent" and "inferred" in the course | BSD-3-Clause |
| gistCore, gistBFO, gistUFO | reasoning over the bridges in module 09 | CC-BY 4.0 |
| gUFO | typing the Trail's classes in o62 | CC-BY 4.0 |
| BFO 2020 core | reasoning over the gistBFO bridge in o61 | CC-BY 4.0 |

`scripts/requirements.txt` names the Python packages the checker uses, fetched
from PyPI: [rdflib](https://github.com/RDFLib/rdflib) (BSD-3-Clause),
[owlrl](https://github.com/RDFLib/OWL-RL) (W3C), [pySHACL](https://github.com/RDFLib/pySHACL)
(Apache-2.0) and the [Ontology Quality Suite](https://pypi.org/project/ontology-quality-suite/)
(as published). None is needed to do the course.

The **Turtle Editor Viewer** at <https://semantechs.co.uk/turtle-editor-viewer/>
is used online and is not part of this repository. Its source is at
<https://github.com/pwin/turtle-editor-viewer>, MIT.

The **Semantechs name and mark** in `assets/` are excluded from the MIT grant.
