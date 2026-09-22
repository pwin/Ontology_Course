# -*- coding: utf-8 -*-
"""Module 11 -- Release and change: the header, deprecation, evidence-based versions, publishing."""
from ontocat import o, Query
import specs

M = "11-change"

DECL = """
skos:prefLabel      a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
skos:changeNote     a owl:AnnotationProperty .
skos:historyNote    a owl:AnnotationProperty .
dct:title           a owl:AnnotationProperty .
dct:description     a owl:AnnotationProperty .
dct:creator         a owl:AnnotationProperty .
dct:contributor     a owl:AnnotationProperty .
dct:created         a owl:AnnotationProperty .
dct:modified        a owl:AnnotationProperty .
dct:license         a owl:AnnotationProperty .
dct:isReplacedBy    a owl:AnnotationProperty .
vann:preferredNamespacePrefix  a owl:AnnotationProperty .
vann:preferredNamespaceUri     a owl:AnnotationProperty .
owl:deprecated      a owl:AnnotationProperty .
"""

HEADER = """
<https://example.org/bookshop-trail/schema>
    a                              owl:Ontology ;
    owl:versionIRI                 <https://example.org/bookshop-trail/schema/2.0.0> ;
    owl:versionInfo                "2.0.0" ;
    owl:priorVersion               <https://example.org/bookshop-trail/schema/1.1.0> ;
    dct:title                      "The Bookshop Trail schema"@en ;
    skos:prefLabel                 "The Bookshop Trail schema"@en ;
    dct:description                "A vocabulary for a fictional network of independent bookshops at real British locations: shops, places, works, people, events, trail segments, stock and sources. OWL 2 DL."@en ;
    dct:creator                    <https://github.com/pwin> ;
    dct:created                    "2025-09-09"^^xsd:date ;
    dct:modified                   "2026-09-21"^^xsd:date ;
    dct:license                    <https://opensource.org/license/mit> ;
    vann:preferredNamespacePrefix  "bs" ;
    vann:preferredNamespaceUri     "https://example.org/bookshop-trail/schema#" ;
    rdfs:seeAlso                   <https://www.semantechs.co.uk/Ontology_Course/> ;
    skos:editorialNote             "Responsible for this vocabulary and for answering questions about it: the Trail committee, via the repository's issue tracker."@en .
"""

o(
    oid="o69", module=M,
    title="The header: what an ontology says about itself",
    decides="The ontology node carries a version IRI, a version number, its prior version, a title, a description, a creator, dates, a licence, its preferred prefix and namespace, and a named point of contact; the Quality Suite's metadata checks confirm nothing is missing.",
    corner="symbol and thought",
    why="An ontology's header is the part read by the most tools and "
        "written with the least care. owl:versionIRI names this release, "
        "and OWL 2 says how it relates to the ontology IRI: the ontology "
        "IRI is the thing, the version IRI is one edition of it, and an "
        "importer may ask for either. owl:versionInfo carries the number "
        "for people; owl:priorVersion the one before. The Dublin Core "
        "terms say what it is, who made it, when, and under what licence, "
        "which is OBO principle FP-001: openly available, and stated so. "
        "vann gives the preferred prefix, so that nobody guesses. And a "
        "point of contact, FP-011, because an ontology with nobody to ask "
        "is an ontology with a clock running.\n\n"
        "gist's header is the model: a version IRI with the number in it, "
        "a definition, a history note listing every release with its "
        "date, and a licence IRI. Nothing in it is decorative; each line "
        "answers a question someone will ask. The Quality Suite has five "
        "checks for the header alone, QUA-002 and QUA-005 to QUA-008: no "
        "versioning metadata, no identifying IRI, an ontology IRI reused "
        "as a namespace, no version IRI, a non-https IRI. Run on this "
        "file, none fires, and that is the measured line.\n\n"
        "The version IRI pattern matters more than it looks. gist uses "
        "gistCore14.1.0 as the version IRI and gist/ as the term "
        "namespace; the Trail uses schema/2.0.0 and schema#. Both keep "
        "the term IRIs stable across versions, which is what lets data "
        "written against 1.1.0 remain true under 2.0.0, and is the "
        "principle o27 gave.",
    diagram="""
   <.../schema>  a owl:Ontology ;                   the ontology: the thing
     owl:versionIRI <.../schema/2.0.0> ;            this edition; importable by name
     owl:versionInfo "2.0.0" ;                      the number, for people
     owl:priorVersion <.../schema/1.1.0> ;          the one before
     dct:title, dct:description                     what it is
     dct:creator, dct:created, dct:modified         who, when
     dct:license                                    FP-001: open, and stated
     vann:preferredNamespacePrefix "bs"             so nobody guesses
     skos:editorialNote "Responsible: ..."          FP-011: someone to ask

   QUA-002, QUA-005, QUA-006, QUA-007, QUA-008: the checks; none fires here
""",
    learn=[
        "The ontology IRI is the thing; the version IRI is an edition of it. Term IRIs stay the same across editions.",
        "Title, description, creator, dates, licence, prefix, contact. Each line answers a question someone will ask.",
        "Five checks cover the header. Run them; a header is the easiest thing to get right and the commonest to leave out.",
    ],
    body=DECL + HEADER + """
bs:Bookshop  a owl:Class ; skos:prefLabel "Bookshop"@en ; skos:definition "A business that sells books to the public from premises."@en .
""",
    check=dict(profile=True, oqs="checks"),
    expect=dict(dl=True, oqs_not=["QUA-002", "QUA-005", "QUA-006", "QUA-007", "QUA-008"]),
)
specs.register("o69", "syntaxOntologyIri", "oboVersioning")

o(
    oid="o70", module=M,
    title="Deprecate; do not delete",
    decides="A term whose meaning has moved is marked deprecated, kept for a full major version, given a change note and a replacement, and the migration is asserted from the retiring IRI so that tooling can find it.",
    corner="symbol",
    why="gist's deprecation policy is short and worth copying whole. A "
        "term that is to go is marked owl:deprecated true in the next "
        "release, with a note saying why and what to use instead. It "
        "stays, deprecated, for at least one full major version, so that "
        "nobody's data breaks between one release and the next. Only at a "
        "later major release is it deleted, and the release notes say so. "
        "The Trail's bs:PublishedWork in o27 followed the first half; this "
        "lesson adds the mechanics.\n\n"
        "The migration annotation is the part that tooling reads. The "
        "SemOps Manual's chapter 12 found that the Quality Suite's rename "
        "detection recognises owl:equivalentClass from the old IRI to the "
        "new one and not the other way round, and that writing it "
        "backwards, which reads more naturally, silently drops a "
        "hundred-percent-confidence repair to a guess. owl:equivalentClass "
        "is symmetric to a reasoner and directional to a tool, and the "
        "rule is: assert it from the retiring IRI. dct:isReplacedBy says "
        "the same to a person.\n\n"
        "A deprecated term still in use is a finding, QUA-003, and the "
        "measured line has it: this file types a work with the deprecated "
        "class so the check can be seen to fire. It did not fire at first, "
        "and the reason is worth a sentence. The finding's focus node is "
        "the work, in the data namespace, and the gate was scoped to the "
        "schema namespace, so the finding was filtered out as somebody "
        "else's. Scope the gate to the whole Trail for this check, or it "
        "will never see a deprecated term in use, which is the check's "
        "whole purpose. That is the finding to watch for in the release "
        "before a deletion. If it fires, the deletion waits.",
    diagram="""
   release N          bs:PublishedWork in use
   release N+1        bs:PublishedWork owl:deprecated true ;
                        skos:changeNote "..." ; dct:isReplacedBy bs:Edition ;
                        owl:equivalentClass bs:Edition .        <- from the retiring IRI, for the tooling
                      bs:Edition a owl:Class ...
   release N+1 .. M   both present; QUA-003 reports any use of the old one
   release M+1        bs:PublishedWork deleted; the release notes say so

   gist: deprecated for a full major version; deleted only at a major release
""",
    learn=[
        "Deprecate in one release, keep for a full major version, delete in a later major one, and say so in the notes.",
        "Assert the migration from the retiring IRI: old owl:equivalentClass new. To a reasoner it is symmetric; to the tooling it is not.",
        "QUA-003, a deprecated term still in use, is the check that decides whether a deletion can go ahead.",
    ],
    body=DECL + HEADER + """
bs:Work  a owl:Class ; skos:prefLabel "Work"@en .

bs:PublishedWork
    a                    owl:Class ;
    owl:deprecated       true ;
    skos:prefLabel       "Published Work"@en ;
    skos:changeNote      "Deprecated in 2.0.0: works acquired more than one edition, and the meaning moved to bs:Edition. Retained through 2.x; to be deleted in 3.0.0."@en ;
    dct:isReplacedBy     bs:Edition ;
    owl:equivalentClass  bs:Edition .

bs:Edition
    a                owl:Class ;
    skos:prefLabel   "Edition"@en ;
    skos:definition  "A printing of a Work by a publisher, with an ISBN if made after 1970."@en .

# Still in use, for QUA-003 to find.
bt:book-old  a bs:PublishedWork .
""",
    queries=[Query("Deprecated terms still in use", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?term (COUNT(?x) AS ?uses) WHERE { ?term owl:deprecated true . ?x a ?term } GROUP BY ?term""", rows=1)],
    check=dict(profile=True, oqs="checks", own_namespace="https://example.org/bookshop-trail/"),
    expect=dict(dl=True, oqs=["QUA-003"]),
    local="QUA-003 on the MEASURED line comes from the Ontology Quality Suite, scoped to the whole Trail namespace",
)
specs.register("o70", "gistDeprecation", "semopsMigration")

V1 = """
@prefix bs:   <https://example.org/bookshop-trail/schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<https://example.org/bookshop-trail/schema> a owl:Ontology ; owl:versionInfo "1.1.0" .
skos:prefLabel a owl:AnnotationProperty .

bs:Place        a owl:Class ; skos:prefLabel "Place"@en .
bs:Settlement   a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Settlement"@en .
bs:Bookshop     a owl:Class ; skos:prefLabel "Bookshop"@en .
bs:Work         a owl:Class ; skos:prefLabel "Work"@en .
bs:PublishedWork a owl:Class ; rdfs:subClassOf bs:Work ; skos:prefLabel "Published Work"@en .
bs:locatedIn    a owl:ObjectProperty ; rdfs:domain bs:Bookshop ; rdfs:range bs:Settlement .
bs:isbn         a owl:DatatypeProperty ; rdfs:domain bs:PublishedWork .
"""

V2 = """
@prefix bs:   <https://example.org/bookshop-trail/schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<https://example.org/bookshop-trail/schema> a owl:Ontology ; owl:versionInfo "2.0.0" ;
    owl:imports <https://w3id.org/semanticarts/ontology/gistCore14.1.0> .   # new in 2.0.0: stands on gist (o59)
skos:prefLabel a owl:AnnotationProperty .

bs:Place        a owl:Class ; skos:prefLabel "Place"@en .
bs:Settlement   a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Settlement"@en .
bs:Bookshop     a owl:Class ; skos:prefLabel "Bookshop"@en .
bs:Work         a owl:Class ; skos:prefLabel "Work"@en .
bs:Edition      a owl:Class ; rdfs:subClassOf bs:Work ; skos:prefLabel "Edition"@en .      # added
bs:locatedIn    a owl:ObjectProperty ; rdfs:domain bs:Bookshop ; rdfs:range bs:Settlement .
bs:isbn         a owl:DatatypeProperty ; rdfs:domain bs:Edition .
bs:website      a owl:DatatypeProperty ; rdfs:domain bs:Bookshop .                         # added
# bs:PublishedWork removed: a MAJOR change, whatever the seven additions around it
"""

o(
    oid="o71", module=M,
    title="The version number decided by evidence",
    decides="A release's version number is derived from what happened to the axioms, by diffing the old and new files, rather than from what the author believed the change was; a removed class makes it major whatever else was added.",
    corner="thought",
    why="Semantic versioning for an ontology follows the software rule "
        "with the terms translated: a change that can break a consumer is "
        "major, an addition is minor, a wording change is a patch. The "
        "hard part is knowing which a given release is, and the SemOps "
        "Manual's answer is not to ask the author. The Quality Suite's "
        "version-diff compares two files axiom by axiom and reports what "
        "was removed, what was added, and the bump that follows: one "
        "removed class makes it MAJOR regardless of the seven additive "
        "changes around it, and regardless of anyone's view that nobody "
        "was using it.\n\n"
        "This lesson's two companion files are version 1.1.0 and 2.0.0 of "
        "a small vocabulary. Between them bs:PublishedWork is gone, "
        "bs:Edition and bs:website have arrived, and bs:isbn's domain has "
        "moved. The diff on the measured line says MAJOR, and the lines it "
        "prints are the evidence a steward signs off on. --fail-on major "
        "makes it a gate: a pull request that removes a class cannot merge "
        "without a named reviewer, and the argument in the meeting becomes "
        "'the diff says major; who signs off', which is a better argument "
        "than 'do you think this is breaking'.\n\n"
        "OBO Foundry FP-004 asks for documented versioning procedures; "
        "gist has release notes per version and a major-version migration "
        "guide. The procedure that costs least is the one where the "
        "number is computed.",
    diagram="""
   1.1.0                                   2.0.0                              version-diff
   bs:PublishedWork                        (gone)                             Removed classes [MAJOR]
   bs:isbn domain PublishedWork            bs:isbn domain Edition             changed
   --                                      bs:Edition                         Added classes [minor]
   --                                      bs:website                         Added properties [minor]

   Suggested version bump: MAJOR           one removal outweighs any number of additions
   --fail-on major: the gate; a named reviewer signs off
""",
    learn=[
        "Major if a consumer can break, minor if only additions, patch if only wording. Derive it from the diff, not the author.",
        "One removal makes a release major whatever else it contains. That is the property that makes the number trustworthy.",
        "Make it a gate with --fail-on major. The decision stays human; the basis stops being who argued hardest.",
    ],
    body=DECL + HEADER,
    companions={"schema-1.1.0.ttl": V1, "schema-2.0.0.ttl": V2},
    check=dict(profile=True, version_diff=("schema-1.1.0.ttl", "schema-2.0.0.ttl")),
    expect=dict(dl=True, bump="MAJOR"),
    local="the verdict on the MEASURED line is the Ontology Quality Suite's version-diff over the two companion files beside this lesson",
    notes="The two versions are schema-1.1.0.ttl and schema-2.0.0.ttl beside this lesson. Open either in the editor; to run the diff, "
          "python -m ontology_suite version-diff schema-1.1.0.ttl schema-2.0.0.ttl --exclude-imports. Old first, then new.",
)
specs.register("o71", "semopsSemver", "oboVersioning")

o(
    oid="o72", module=M,
    title="Publishing the IRIs, and keeping them alive",
    decides="The vocabulary is published where its IRIs resolve, with a persistent redirector in front, documentation generated from the file, a channel for requests, and notice of changes; and where the Trail cannot do that, it says so.",
    corner="symbol",
    why="An IRI that resolves is the last leg of o04's promise: fetch it "
        "and get the definition. Cool URIs sets out how, with a hash "
        "namespace served as one document or a slash namespace served a "
        "resource at a time, and content negotiation returning Turtle to "
        "a program and HTML to a person. The Best Practice Recipes note "
        "gives the server configuration for each case. A persistent "
        "redirector, w3id.org for gist, sits in front so that the "
        "hosting can move and the IRIs need not; gist's IRIs have "
        "survived three hosts that way.\n\n"
        "Documentation is generated, not written, so that it cannot "
        "drift: the Quality Suite's docgen produces a reference page from "
        "the file, classes, properties and diagrams, and the SemOps "
        "Manual's chapter 13 makes it a build step. Then the OBO Foundry's "
        "social principles: a channel for community participation "
        "(FP-020), responsiveness to requests (FP-016), and notice of "
        "major changes to those who depend on the ontology (FP-013). None "
        "is technical and each is the reason an ontology is still used in "
        "five years.\n\n"
        "The Trail says which of these it does. Its namespace "
        "is example.org, reserved for documentation, so nothing resolves "
        "and nothing ever will; the point of the course is the thinking, "
        "not the hosting. Its documentation is generated; its channel is "
        "the repository's issue tracker; its notice of change is the "
        "commit log and this course document. That is stated on the "
        "header, which is the SemOps ledger again: say what you do not "
        "do, in the place someone will look.",
    diagram="""
   a program asks for bs:Bookshop     Accept: text/turtle        ->  the schema document, Turtle
   a person asks for bs:Bookshop      Accept: text/html          ->  the generated documentation, at #Bookshop
   the host moves                     w3id.org redirects         ->  the IRIs do not change

   docgen  ->  reference page from the file, every build       (SemOps 13.2)
   FP-020  a channel        FP-016  responsiveness        FP-013  notice of major changes

   the Trail: example.org, so nothing resolves; the header says so
""",
    learn=[
        "Resolving IRIs close the loop from symbol to definition. A redirector in front is what keeps them resolving when the host changes.",
        "Generate the documentation from the file. Written documentation drifts; generated documentation cannot.",
        "The last three principles are social: a channel, responsiveness, notice of change. They decide whether the ontology is alive in five years.",
    ],
    body=DECL + HEADER + """
<https://example.org/bookshop-trail/schema>
    skos:editorialNote  "Not published at a resolving IRI: example.org is reserved for documentation, and this vocabulary is a teaching one. Documentation is generated by scripts/build_docs.py and the Quality Suite's docgen; requests and questions go to the repository's issue tracker; changes are announced in the release notes and the course document."@en .
""",
    check=dict(profile=True),
    expect=dict(dl=True),
)
specs.register("o72", "vocabPub", "oboNotification")
