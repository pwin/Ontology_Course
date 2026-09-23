# -*- coding: utf-8 -*-
"""The lesson catalogue: one place where every lesson is defined.

Each Lesson below becomes a .ttl file with a structured header, and the same
object drives the course document, the module READMEs, FEATURES.md and the
checker. Keeping the explanation and the model in one object is what stops
them drifting apart.

    python scripts/build_lessons.py    # write lessons/**/*.ttl and the READMEs
    python scripts/check_lessons.py    # parse, reason over and measure every lesson
"""
from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

import specs

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"
DATA = ROOT / "data"
LIB = ROOT / "lib"

# Where the three courses live. The hosted copies are the ones a reader is
# sent to; the GitHub repositories hold the files. The editor fetches lesson
# files from raw.githubusercontent.com, which sends the CORS header it needs.
REPO = "https://github.com/pwin/Ontology_Course"
SPARQL_REPO = "https://github.com/pwin/SPARQL_Course"
SHACL_REPO = "https://github.com/pwin/SHACL_Course"
SITE = "https://www.semantechs.co.uk/Ontology_Course/"
SPARQL_SITE = "https://www.semantechs.co.uk/SPARQL_Course/"
SHACL_SITE = "https://www.semantechs.co.uk/SHACL_Course/"
SEMOPS = "https://github.com/pwin/SemOpsManual"
RAW_BASE = "https://raw.githubusercontent.com/pwin/Ontology_Course/main/"
EDITOR_BASE = "https://semantechs.co.uk/turtle-editor-viewer/"

# The data files a lesson can name. They are the SPARQL course's, byte for byte.
D11 = "bookshop-trail-1.1.ttl"
DVOCAB = "01-vocabulary.ttl"
DGENRES = "02-genres.ttl"
DPLACES = "03-places.ttl"
DSHOPS = "04-bookshops.ttl"
DPEOPLE = "05-people.ttl"
DBOOKS = "06-books.ttl"
DEVENTS = "07-events.ttl"

# Every prefix the course knows about, in the order a file declares them. A
# lesson declares only the ones its model uses.
KNOWN_PREFIXES = [
    ("bt",     "https://example.org/bookshop-trail/"),
    ("bs",     "https://example.org/bookshop-trail/schema#"),
    ("oc",     "https://example.org/bookshop-trail/ontoclean#"),
    ("rdf",    "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    ("rdfs",   "http://www.w3.org/2000/01/rdf-schema#"),
    ("owl",    "http://www.w3.org/2002/07/owl#"),
    ("xsd",    "http://www.w3.org/2001/XMLSchema#"),
    ("skos",   "http://www.w3.org/2004/02/skos/core#"),
    ("dct",    "http://purl.org/dc/terms/"),
    ("vann",   "http://purl.org/vocab/vann/"),
    ("sh",     "http://www.w3.org/ns/shacl#"),
    ("geo",    "http://www.opengis.net/ont/geosparql#"),
    ("sf",     "http://www.opengis.net/ont/sf#"),
    ("wgs84",  "http://www.w3.org/2003/01/geo/wgs84_pos#"),
    ("prov",   "http://www.w3.org/ns/prov#"),
    ("schema", "https://schema.org/"),
    ("gist",   "https://w3id.org/semanticarts/ns/ontology/gist/"),
    ("gistd",  "https://w3id.org/semanticarts/ns/data/gist/"),
    ("gufo",   "http://purl.org/nemo/gufo#"),
    ("obo",    "http://purl.obolibrary.org/obo/"),
    ("wd",     "http://www.wikidata.org/entity/"),
]
PREFIX_URI = dict(KNOWN_PREFIXES)

_IRI = re.compile(r"<[^>\s]*>")
# Double-quoted strings only: the course never writes a single-quoted
# literal, and an apostrophe in a comment must not start one.
_STR = re.compile(r"\"\"\".*?\"\"\"|\"(?:[^\"\\]|\\.)*\"", re.S)
_COMMENT = re.compile("#[^" + chr(10) + "]*")
_PNAME = re.compile(r"(?<![A-Za-z0-9_-])([A-Za-z][A-Za-z0-9._-]*):")


def prefixes_used(text: str) -> set:
    """Which known prefixes a Turtle body actually mentions."""
    stripped = _COMMENT.sub(" ", _STR.sub(" ", _IRI.sub(" ", text)))
    return {m.group(1) for m in _PNAME.finditer(stripped)} & set(PREFIX_URI)


def prologue_for(names) -> str:
    names = set(names)
    rows = [(p, u) for p, u in KNOWN_PREFIXES if p in names]
    if not rows:
        return ""
    width = max(len(p) for p, _ in rows) + 1
    return chr(10).join(f"@prefix {(p + ':').ljust(width)} <{u}> ." for p, u in rows)


@dataclass
class Query:
    """A companion SPARQL query. `on` is "model" (the lesson's own graph),
    "data" (the lesson's graph merged with the data file it names) or
    "reasoned" (the graph after the OWL 2 RL closure). `rows` is what the
    checker expects it to return; None means run it and report."""
    title: str
    text: str
    on: str = "model"
    rows: int | None = None


@dataclass
class Lesson:
    oid: str                    # "o07"
    module: str                 # folder name, e.g. "02-systematics"
    title: str
    decides: str                # the decision this lesson makes, one sentence
    why: str                    # the reasoning, in paragraphs
    diagram: str                # an ASCII diagram of the idea
    learn: list[str]            # takeaways
    body: str                   # the model, in Turtle, without the prefixes
    corner: str = ""            # which corner of the triangle: symbol, thought, referent
    notes: str = ""             # caveats
    tryit: str = ""             # edits to make in the editor, and what changes
    data: str = ""              # a data file the lesson is read alongside, if any
    local: str = ""             # what needs local tooling, if anything; "" means the browser does it all
    companions: dict = field(default_factory=dict)  # extra files written beside the lesson: name -> text
    shapes: str = ""            # the companion that Open in the editor opens as a shapes tab, if any
    inference: str = ""         # the editor's Inference setting for that tab: rdfs, rules or rules-iterated
    extra_prefixes: tuple = ()
    # What the checker runs. Keys: profile, profiles, reason, rl, oqs, shacl
    # (shapes text), metrics, names, with_data (a file in data/), imports (files
    # in lib/), definitions (circularity audit).
    check: dict = field(default_factory=dict)
    # What it must find. Keys: dl, el, ql, rl (bools), consistent, unsat (local
    # names), inferred / not_inferred / rl_inferred (prefixed triples as
    # strings), rl_sameas (pairs), oqs / oqs_not (check ids), shacl_conforms,
    # shacl_violations, classes, object_properties, datatype_properties,
    # annotation_properties, individuals, min_triples, names_bad, circular.
    expect: dict = field(default_factory=dict)
    queries: list = field(default_factory=list)
    place: float = 0.0
    measured: str = ""          # filled in by check_lessons.py
    order: int = 0

    @property
    def sort_key(self) -> float:
        return self.place or float(self.oid[1:])

    @property
    def filename(self) -> str:
        slug = self.title.lower()
        for ch in " ,;'()/?*:\"<>|!$&":
            slug = slug.replace(ch, "-")
        while "--" in slug:
            slug = slug.replace("--", "-")
        return f"{self.oid}-{slug.strip('-')}.ttl"

    @property
    def path(self) -> Path:
        return LESSONS / self.module / self.filename

    @property
    def prologue(self) -> str:
        names = prefixes_used(self.body) | set(self.extra_prefixes)
        return prologue_for(names)

    @property
    def raw_url(self) -> str:
        return RAW_BASE + "lessons/" + self.module + "/" + self.filename

    @property
    def editor_url(self) -> str:
        """A link that opens the editor with the lesson file loaded, a
        companion shapes file in a second tab where the lesson has one, and
        the Inference dropdown preset where the shapes hold a rule."""
        url = EDITOR_BASE + "?dot=" + quote(self.raw_url, safe="")
        if self.shapes:
            url += "&shapes=" + quote(RAW_BASE + "lessons/" + self.module + "/" + self.shapes, safe="")
        if self.inference:
            url += "&inference=" + self.inference
        return url

    @property
    def model_text(self) -> str:
        """The model as a learner should paste it: prefixes, then the Turtle."""
        parts = [self.prologue, "", self.body.strip(), ""]
        return chr(10).join(parts)

    @property
    def copy_text(self) -> str:
        nl = chr(10)
        head = [
            "# " + self.oid.upper() + "  " + self.title,
            "# " + self.decides,
            "# The Bookshop Trail, ontology course -- " + SITE,
        ]
        return nl.join(head) + nl * 2 + self.model_text

    def text(self) -> str:
        """The .ttl file: a header a learner can read, then the model."""
        rule = "# " + "=" * 74
        out = [rule, f"#  {self.oid.upper()}  {self.title}", rule, "#"]

        def block(label, content, bullet=False):
            out.append(f"#  {label}")
            if bullet:
                for item in content:
                    wrapped = textwrap.wrap(item, 66)
                    out.append(f"#    - {wrapped[0]}")
                    for cont in wrapped[1:]:
                        out.append(f"#      {cont}")
            else:
                for para in content.split(chr(10) + chr(10)):
                    for line in textwrap.wrap(" ".join(para.split()), 70):
                        out.append(f"#    {line}")
                    out.append("#")
                out.pop()
            out.append("#")

        block("DECIDES", self.decides)
        block("WHY", self.why)
        out.append("#  DIAGRAM")
        for line in self.diagram.strip(chr(10)).splitlines():
            out.append(f"#    {line}".rstrip())
        out.append("#")
        block("WHAT TO TAKE AWAY", self.learn, bullet=True)
        if self.notes:
            block("NOTE", self.notes)
        if self.tryit:
            block("TRY IT", self.tryit)
        if self.corner:
            out.append(f"#  CORNER    {self.corner}")
        if self.data:
            out.append(f"#  DATA      {self.data}")
        out.append(f"#  RUNS IN   {'the browser' if not self.local else 'the browser; ' + self.local}")
        out.append("#  OPEN IN THE EDITOR")
        out.append(f"#            {self.editor_url}")
        for i, (label, url) in enumerate(specs.for_lesson(self.oid, self.module, limit=2)):
            out.append(f"#  {'SOURCES  ' if i == 0 else '         '} {label}")
            out.append(f"#            {url}")
        if self.measured:
            out.append(f"#  MEASURED  {self.measured}")
        out.append(rule)
        out.append("")
        out.append(self.model_text)
        if self.queries:
            out.append("")
            out.append("# " + "-" * 72)
            out.append("#  AFTERWARDS.  Queries to run in the SPARQL panel, on this file (press")
            out.append("#  Add Prefixes first) or on the data file it names.")
            out.append("# " + "-" * 72)
            for q in self.queries:
                out.append("#")
                out.append(f"#  -- {q.title}  (on the {q.on})")
                for line in q.text.strip().splitlines():
                    out.append(("#  " + line).rstrip())
            out.append("")
        return chr(10).join(out)


CATALOGUE: list[Lesson] = []


def o(**kwargs) -> Lesson:
    item = Lesson(**kwargs)
    item.order = len(CATALOGUE)
    CATALOGUE.append(item)
    return item


# Module title, blurb, and the corner of the triangle it mostly works on.
MODULE_INFO = {
    "01-meaning": (
        "Meaning",
        "Before there is a class or a property there is a word, the thing it "
        "stands for, and the idea in between. The triangle of reference is "
        "the oldest picture of that, and it is the picture this whole course "
        "is drawn on; so this module puts the Bookshop Trail's nouns onto it, "
        "shows the two ways in which a word fails, and introduces the one "
        "kind of symbol that is globally unique and that a machine can "
        "compare, which is the IRI, and which is what takes us from strings "
        "to things.",
    ),
    "02-systematics": (
        "Systematics",
        "A taxonomy is a set of claims about what things are, and some of "
        "those claims are wrong in ways that do not show until the ontology "
        "is being used. OntoClean gives us four questions to ask of every "
        "class, which are whether an instance could stop being one, what "
        "makes two of them the same, whether each one is a whole, and whether "
        "it exists only in relation to something else; and the answers decide "
        "which subclass links will bear weight. The module ends with those "
        "checks written as queries, and with gist read through them.",
    ),
    "03-naming": (
        "Naming",
        "This is the symbol corner. An IRI identifies, a label names, and a "
        "definition says what is meant, and keeping the three of them apart "
        "is what lets a shop be renamed without becoming a different shop, "
        "and lets two organisations use the same word for different things "
        "without colliding. The module sets out the conventions the Trail "
        "follows beside the ones gist follows, and audits the one against the "
        "other.",
    ),
    "04-definitions": (
        "Definitions and controlled vocabularies",
        "This is the thought corner, written down. A definition is the "
        "agreement that makes a shared symbol carry a shared meaning, and a "
        "controlled vocabulary is a list of terms whose definitions somebody "
        "has agreed to look after; so the module covers the form of a good "
        "definition, the ways in which one fails, the set of annotations that "
        "carry it, and the decision that comes before any taxonomy at all, "
        "which is whether this thing is a class or a category.",
    ),
    "05-principles": (
        "Design principles",
        "What well-made ontologies have in common, drawn from three places "
        "that agree rather more than they differ: the gist style guide, the "
        "OBO Foundry principles, and the SemOps Manual. Minimal, reused "
        "before invented, disjoint at the top, sparse in its domains and "
        "ranges, carrying meaning rather than integrity rules, and built "
        "alongside the people who will have to read it.",
    ),
    "06-the-ladder": (
        "The ladder: RDFS and SKOS",
        "RDFS, SKOS and OWL 2 are one idea at rising degrees of commitment. A "
        "list of labelled terms says almost nothing; a concept scheme says "
        "how the terms relate without saying what they are; and a class "
        "hierarchy says that membership is inherited, at which point a "
        "reasoner begins to draw conclusions. This module climbs the first of "
        "those rungs with the genre scheme and the place hierarchy, saying at "
        "each one what has just been promised.",
    ),
    "07-owl": (
        "The ladder: OWL 2",
        "The top rungs, where OWL 2 lets an ontology say enough that a "
        "reasoner can contradict it, which is the first point at which the "
        "model can be wrong rather than incomplete. Each lesson takes "
        "one construct, states what it commits you to, and shows what the "
        "reasoner then does with it; and the surprises are the point, whether "
        "a maximum cardinality that merges two towns instead of flagging an "
        "error, a universal restriction that infers nothing at all, or a "
        "transitive property that cannot also be functional.",
    ),
    "08-reasoning": (
        "Reasoning",
        "What follows from what you said, which covers consistency, "
        "unsatisfiable classes, the inferred hierarchy, an explanation traced "
        "back to the axioms that caused it, and the difference between an OWL "
        "2 RL closure like the editor's and a description-logic reasoner like "
        "HermiT. The module ends by reasoning over the whole Trail, where it "
        "finds the reason one property was left non-functional.",
    ),
    "09-upper-ontologies": (
        "Standing on gist",
        "An upper ontology is a vocabulary in common, so this module hooks "
        "the Trail's classes onto gist, decides which of gist's patterns are "
        "worth adopting, and reads two published alignments, gistBFO and "
        "gistUFO, as worked examples of how a class comes to be placed under "
        "a foundational one and why. Two of the placements disagree with one "
        "another, which is instructive in itself.",
    ),
    "10-quality": (
        "Quality",
        "Measuring what has been built, and knowing what the measurements "
        "cannot see: OQuaRE's metrics scored on the Trail and on gist, the "
        "Ontology Quality Suite's checks read by identifier, style shapes "
        "like the ones gist runs against itself, and competency questions "
        "used as tests. Then the limits of all that, since an ontology can "
        "score five out of five and still be wrong, and no metric sees "
        "rigidity.",
    ),
    "11-change": (
        "Release and change",
        "An ontology is for life, so this module covers the header that says "
        "what it is, the policy that retires a term without deleting it, the "
        "version number decided by evidence rather than by opinion, and the "
        "one principle that every source agrees on, which is that once "
        "published a term must always mean the same thing.",
    ),
    "12-putting-it-together": (
        "Putting it together",
        "The whole Trail vocabulary, rebuilt and compared with the shipped "
        "one decision by decision; the genre scheme with its integrity "
        "checked; the competency questions the SPARQL course answers and the "
        "constraints the SHACL course enforces, taken together as the test "
        "suite this ontology exists to pass; and then a challenge to finish "
        "with.",
    ),
}
