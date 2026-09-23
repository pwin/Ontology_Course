# Module 00 · The lab

Twenty minutes on the tool before the first lesson. Everything in this course runs in the **Turtle Editor Viewer**, used online at <https://semantechs.co.uk/turtle-editor-viewer/>. Nothing is installed and nothing you load leaves your browser: the parser, the graph view, the SPARQL engine, the OWL 2 RL reasoner behind **Show Facts** and the SHACL engine all run inside the page.

If you did the SPARQL course, its [module 00](https://www.semantechs.co.uk/SPARQL_Course/#m00) covers the graph view, the layout engines and format conversion, and the SHACL course's [module 00](https://www.semantechs.co.uk/SHACL_Course/#m00) covers the validator panel. This page covers what those two touched only in passing: using the editor to look at a *vocabulary* rather than at data, and to watch a reasoner do something with it.

## One file, one tab

Every lesson is one Turtle file. The header, in comments, carries the whole lesson: what it decides, why, a diagram, what to take away, sometimes something to try, and an Open in the editor link. Below the header is the model, a few dozen triples, and sometimes a set of queries to run afterwards.

1. Follow the **Open in the editor** link at the foot of a lesson's header, or press the button of the same name in the [course document](https://www.semantechs.co.uk/Ontology_Course/). The file arrives in the first tab.
2. Look at the graph pane. For a vocabulary the `rdf:type` edges are the point, so leave **Hide Types** off; **Hide Annotations** clears the labels and comments and leaves the structure.
3. Press **Add Prefixes** in the SPARQL panel, paste a query from the end of the file, press **Execute**.

Edit anything and press **Get All** before you query again. The SPARQL panel runs against a store built when the file was parsed, and an edit without Get All gives you the old answer, which looks exactly like the query being wrong.

## Show Facts is a reasoner, of one kind

**Show Facts** in the graph toolbar runs HyLAR, an OWL 2 RL reasoner, and lists the triples you wrote beside the triples it worked out. It does what a rule engine over triples does: types individuals down a subclass chain, applies domains and ranges, closes transitive and symmetric properties, follows inverses and property chains, merges two individuals under a functional property, and puts individuals into a defined class when the fillers are named.

It does not do what a description-logic reasoner does. It will not tell you an ontology is inconsistent (it materialises the contradiction and carries on), will not find a class that can have no instances, will not infer that one class is under another from their definitions, and will not explain. Lessons [o43](../07-owl/) and [o53](../08-reasoning/) give a SPARQL query that finds in the browser what the DL reasoner would report; [o54](../08-reasoning/), [o55](../08-reasoning/) and [o56](../08-reasoning/) are about what only a DL reasoner does.

The **Measured** block under every lesson in the course document says what an OWL 2 RL closure added to that lesson's file. It is what Show Facts will show you, computed with `owlrl` rather than HyLAR, and the two agree on everything this course asks of them.

## Shapes, and the Inference dropdown

Some lessons carry a companion shapes file: the label rules of [o19](../03-naming/), the SKOS integrity conditions of [o39](../06-the-ladder/), the style shapes of [o67](../10-quality/), the transitive-closure rule of [o52](../08-reasoning/). Open in the editor opens the companion in a second tab already selected under **Shapes**; press **Validate** and read the report as the SHACL course taught. The rule lesson's link also sets the **Inference** dropdown to *rules, iterated*, where the report counts all 186 pairs of the closure; set it to *rules* for the 123 of one pass and to *none* for the 63 asserted.

Validating a vocabulary is the SHACL course's method turned on the ontology itself, and it is how to form a first opinion of any vocabulary you are handed.

## The brief

Read [data/the-brief.md](../../data/the-brief.md) before o01. It is a page from the Trail's committee: what they have, what they want, the words they use, and ten questions they would like answered. It is loose on purpose. Every ambiguity in it is a lesson.

## The data

The dataset is the SPARQL course's [Bookshop Trail](https://www.semantechs.co.uk/SPARQL_Course/#the-data), unchanged and byte for byte: real towns, real coordinates, and an invented network of independent bookshops, authors, publishers, books and events. Everything except the geography is fiction. `data/01-vocabulary.ttl` is the OWL 2 DL schema this course rebuilds, and `data/02-genres.ttl` is the SKOS scheme; the lessons in modules 06 to 12 open them beside the lesson file where a claim is about the whole of either.

## What needs a terminal

Nothing, to do the course. Every claim the tools could check has been checked already, and the results are in each lesson's MEASURED line and in the course document. To check them yourself, or to measure your own answer to the challenge in [o76](../12-putting-it-together/):

```powershell
./scripts/setup-tools.ps1                   # fetches ROBOT, gist, gistBFO, gistUFO, gUFO and BFO into lib/
pip install -r scripts/requirements.txt     # rdflib, owlrl, shacl, ontology-quality-suite
python scripts/check_lessons.py             # every lesson, every instrument; about two minutes
python scripts/check_lessons.py o47 --show  # one lesson, with the inferred triples printed
```

ROBOT wraps the OWL API, the OWL 2 profile checker and HermiT, and is the referee for every "in profile", "consistent" and "inferred" in the course. The Ontology Quality Suite is the source of every check identifier. `scripts/metrics.py` computes the OQuaRE metrics. And the SHACL numbers come from `shacl`, which is the engine behind the editor's Validate button: one Rust engine, compiled to WebAssembly for the browser and bound to Python for the checker, so the results in a Measured block are the results the editor will show you. Both run 0.3.2, in which a warning or an info breaks conformance as the specification has it, so the verdict agrees as well as the results. None of them needs the internet after setup.

## What is where

```
lessons/NN-module/oNN-title.ttl    one lesson: header, then the model, then queries to run afterwards
lessons/NN-module/*.ttl            companion files: shapes, a rule, two versions, an answer
lessons/NN-module/README.md        the module's lessons, blurb and sources
data/                              the brief; the Bookshop Trail, clean, as the SPARQL course ships it
docs/index.html                    the whole course as one document, with everything measured
FEATURES.md                        every term, and which lesson shows it
scripts/                           the catalogue the lessons are generated from, and the checkers
```

Start with [module 01](../01-meaning/), and the triangle.
