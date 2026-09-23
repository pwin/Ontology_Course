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
        "and OWL 2 says how it relates to the ontology IRI, the ontology "
        "IRI being the thing and the version IRI one edition of it, with an "
        "importer free to ask for either; owl:versionInfo carries the "
        "number for people to read and owl:priorVersion the one before it. "
        "The Dublin Core terms say what it is, who made it, when, and under "
        "what licence, which is OBO principle FP-001, openly available and "
        "stated so; vann gives the preferred prefix so that nobody has to "
        "guess; and a point of contact answers FP-011, because an ontology "
        "with nobody to ask is an ontology with a clock running on it.\n\n"
        "gist's header is the model to copy, with a version IRI that has "
        "the number in it, a definition, a history note listing every "
        "release and its date, and a licence IRI. Nothing in it is "
        "decorative, and each line answers a question that somebody will "
        "ask. The Quality Suite has five checks for the header alone, "
        "QUA-002 and QUA-005 through QUA-008, covering no versioning "
        "metadata, no identifying IRI, an ontology IRI reused as a "
        "namespace, no version IRI and a non-https IRI; run over this file "
        "not one of them fires, which is the measured line.\n\n"
        "The version IRI pattern matters rather more than it looks. gist "
        "uses gistCore14.1.0 as its version IRI with gist/ as the term "
        "namespace, and the Trail uses schema/2.0.0 with schema#, and both "
        "of them keep the term IRIs stable across versions, which is what "
        "lets data written against 1.1.0 stay true under 2.0.0, and is the "
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
        "The ontology IRI is the thing and the version IRI is an edition of it, while the term IRIs stay the same across editions.",
        "Title, description, creator, dates, licence, prefix and contact: each of those lines answers a question somebody will ask.",
        "Five checks cover the header, so run them, since a header is the easiest thing in an ontology to get right and the commonest to leave out.",
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
    why="gist's deprecation and deletion policy is short and worth copying "
        "whole. Deprecation is a minor change, so a term that is to go is "
        "marked owl:deprecated true in the next minor release, with a note "
        "saying why and what to use instead, and it stays available through "
        "the rest of that major version, so that nobody's data breaks "
        "between one release and the next. A major release then contains no "
        "deprecations at all, since every term deprecated during the "
        "previous major version is deleted in it and the release notes say "
        "so; and renaming a term counts as a deletion plus an addition, "
        "which makes it major too. The Trail's bs:PublishedWork in o27 "
        "followed the first half of that, and this lesson adds the "
        "mechanics.\n\n"
        "The migration annotation is the part the tooling reads. The SemOps "
        "Manual's chapter 12 found that the Quality Suite's rename "
        "detection recognises owl:equivalentClass asserted from the old IRI "
        "to the new one and not the other way about, and that writing it "
        "backwards, which reads more naturally, silently drops a hundred- "
        "percent-confidence repair down to a guess. owl:equivalentClass is "
        "symmetric to a reasoner and directional to a tool, so the rule is "
        "to assert it from the retiring IRI; gist adds gist:isSupersededBy "
        "for the same purpose, and dct:isReplacedBy says the same thing to "
        "a person.\n\n"
        "A deprecated term still in use is a finding, QUA-003, and the "
        "measured line has it, since this file types a work with the "
        "deprecated class so that the check can be seen to fire. It did not "
        "fire at first, and the reason is worth a sentence: the finding's "
        "focus node is the work, which lives in the data namespace, while "
        "the gate was scoped to the schema namespace, so the finding was "
        "filtered out as somebody else's. Scope the gate to the whole Trail "
        "for this check, or it will never see a deprecated term in use, "
        "which is the check's whole purpose. That is the finding to watch "
        "for in the release before a deletion, and if it fires then the "
        "deletion waits.",
    diagram="""
   release N          bs:PublishedWork in use
   release N+1        bs:PublishedWork owl:deprecated true ;
                        skos:changeNote "..." ; dct:isReplacedBy bs:Edition ;
                        owl:equivalentClass bs:Edition .        <- from the retiring IRI, for the tooling
                      bs:Edition a owl:Class ...
   release N+1 .. M   both present; QUA-003 reports any use of the old one
   release M+1        bs:PublishedWork deleted; the release notes say so

   gist: deprecation is a minor change; a major release deletes every deprecated term and adds none
""",
    learn=[
        "Deprecate in a minor release, keep the term for the rest of the major version, delete at the next major one, and say so in the notes.",
        "Assert the migration from the retiring IRI, old owl:equivalentClass new, because to a reasoner it is symmetric and to the tooling it is not.",
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
    notes="Scoped to the whole Trail namespace, the suite also reports the undocumented individual and the references it "
          "cannot resolve in a file this small (QUA-004, STR-006, DAT-002). The wider scope costs you those, which is the reason to scope narrowly by default and to widen only for the checks that need it. QUA-003 is the one this lesson is about.",
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
    why="Semantic versioning for an ontology follows the software rule with "
        "the terms translated: a change that can break a consumer is major, "
        "an addition is minor, and a wording change is a patch. The hard "
        "part is knowing which of the three a given release is, and the "
        "SemOps Manual's answer is not to ask the author. The Quality "
        "Suite's version-diff compares two files axiom by axiom and reports "
        "what was removed, what was added, and the bump that follows, so "
        "that one removed class makes the release MAJOR regardless of the "
        "seven additive changes around it, and regardless of anybody's view "
        "that nobody was using it.\n\n"
        "This lesson's two companion files are version 1.1.0 and 2.0.0 of a "
        "small vocabulary. Between them bs:PublishedWork has gone, "
        "bs:Edition and bs:website have arrived, and bs:isbn's domain has "
        "moved; the diff on the measured line says MAJOR, and the lines it "
        "prints are the evidence a steward signs off on. --fail-on major "
        "turns that into a gate, so that a pull request removing a class "
        "cannot merge without a named reviewer, and the argument in the "
        "meeting becomes 'the diff says major, so who signs off', which is "
        "a better argument than 'do you think this is breaking'.\n\n"
        "OBO Foundry FP-004 asks for documented versioning procedures, and "
        "gist has release notes for every version and a migration guide for "
        "the major ones. The procedure that costs least, though, is the one "
        "where the number is computed rather than argued over.",
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
        "Major if a consumer can break, minor if there are only additions, patch if only the wording moved, and derive it from the diff rather than from the author.",
        "One removal makes a release major whatever else it contains, and that is the property which makes the number trustworthy.",
        "Make it a gate with --fail-on major, so that the decision stays human while the basis for it stops being who argued hardest.",
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
    why="An IRI that resolves is the last leg of o04's promise, that you "
        "can fetch it and get the definition back. Cool URIs sets out how, "
        "with a hash namespace served as one document or a slash namespace "
        "served a resource at a time, and content negotiation returning "
        "Turtle to a program and HTML to a person, while the Best Practice "
        "Recipes note gives the server configuration for either case. A "
        "persistent redirector, w3id.org in gist's case, sits in front of "
        "the lot so that the hosting can move and the IRIs need not.\n\n"
        "Documentation is generated rather than written, so that it cannot "
        "drift: the Quality Suite's docgen produces a reference page from "
        "the file, with its classes and properties and diagrams, and the "
        "SemOps Manual's chapter 13 makes that a build step. Then come the "
        "OBO Foundry's social principles, a channel for community "
        "participation in FP-020, responsiveness to requests in FP-016, and "
        "notice of major changes to those who depend on the ontology in "
        "FP-013; none of them is technical, and each of them is a reason an "
        "ontology is still being used in five years' time.\n\n"
        "The Trail says which of these it does. Its namespace is "
        "example.org, which is reserved for documentation, so nothing "
        "resolves and nothing ever will, the point of the course being the "
        "thinking rather than the hosting; its documentation is generated, "
        "its channel is the repository's issue tracker, and its notice of "
        "change is the commit log together with this course document. All "
        "of which is stated on the header, which is the SemOps ledger "
        "again: say what you do not do, in the place where somebody will "
        "look for it.",
    diagram="""
   a program asks for bs:Bookshop     Accept: text/turtle        ->  the schema document, Turtle
   a person asks for bs:Bookshop      Accept: text/html          ->  the generated documentation, at #Bookshop
   the host moves                     w3id.org redirects         ->  the IRIs do not change

   docgen  ->  reference page from the file, every build       (SemOps 13.2)
   FP-020  a channel        FP-016  responsiveness        FP-013  notice of major changes

   the Trail: example.org, so nothing resolves; the header says so
""",
    learn=[
        "Resolving IRIs close the loop from symbol to definition, and a redirector in front is what keeps them resolving when the host changes.",
        "Generate the documentation from the file, because written documentation drifts and generated documentation cannot.",
        "The last three principles are social ones, a channel and responsiveness and notice of change, and they decide whether the ontology is still alive in five years.",
    ],
    body=DECL + HEADER + """
<https://example.org/bookshop-trail/schema>
    skos:editorialNote  "Not published at a resolving IRI: example.org is reserved for documentation, and this vocabulary is a teaching one. Documentation is generated by scripts/build_docs.py and the Quality Suite's docgen; requests and questions go to the repository's issue tracker; changes are announced in the release notes and the course document."@en .
""",
    check=dict(profile=True),
    expect=dict(dl=True),
)
specs.register("o72", "vocabPub", "oboNotification")
