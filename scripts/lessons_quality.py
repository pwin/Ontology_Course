# -*- coding: utf-8 -*-
"""Module 10 -- Quality: OQuaRE, the checks by identifier, style shapes, and the limits."""
from ontocat import o, Query, DVOCAB
import specs

M = "10-quality"

DECL = """
skos:prefLabel      a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
"""

o(
    oid="o63", module=M,
    title="OQuaRE in a page",
    decides="Quality is assessed with a published model rather than a feeling: OQuaRE's characteristics, sub-characteristics and metrics, each metric scored one to five against the paper's thresholds, and the scores read as a map of strengths rather than a mark.",
    corner="thought",
    why="OQuaRE takes the software quality standard SQuaRE, ISO/IEC 25000, "
        "and adapts it to ontologies. The shape is three layers. "
        "Characteristics at the top: structural, functional adequacy, "
        "reliability, operability, maintainability, compatibility, "
        "transferability, quality in use. Sub-characteristics under each: "
        "cohesion, tangledness, redundancy and consistency under "
        "structural; modularity, reusability, analysability, changeability "
        "under maintainability; the intended uses of an ontology, from "
        "controlled vocabulary to inferencing, under functional adequacy. "
        "And metrics at the bottom, fourteen of them, most adapted from "
        "object-oriented software metrics: depth of inheritance, number of "
        "children, coupling, cohesion, richness of attributes, relations "
        "and annotations.\n\n"
        "Each metric is scored one to five, where one is not acceptable, "
        "three minimally acceptable and five exceeds requirements, against "
        "thresholds the paper proposes. A sub-characteristic's score is "
        "the mean of its metrics; a characteristic's is the mean of its "
        "sub-characteristics. The authors are careful to say that the "
        "result is meant to show strengths and weaknesses, not to rank "
        "ontologies, and that the thresholds are proposals from software "
        "practice awaiting validation. Both cautions are worth keeping.\n\n"
        "The metrics are computed in this course by scripts/metrics.py, "
        "which follows the paper's formulas and states its own choices "
        "where the paper is silent. The measured line has the Trail's "
        "scores; o64 and o65 read them, and o68 says what they miss.",
    diagram="""
   SQuaRE (ISO/IEC 25000)  ->  OQuaRE

   characteristic      sub-characteristics                         metrics (examples)
   structural          formalisation, cohesion, tangledness, ...   LCOMOnto, TMOnto, DITOnto
   functional adequacy controlled vocabulary, reasoning, ...       RROnto, AROnto, INROnto, ANOnto, CROnto
   maintainability     modularity, reusability, analysability, ... WMCOnto, DITOnto, NOCOnto, RFCOnto, NOMOnto, CBOOnto
   reliability, operability, compatibility, transferability, quality in use

   score 1..5 per metric, by threshold; means upward; strengths and weaknesses, not a rank
""",
    learn=[
        "A quality model is three layers: characteristics, sub-characteristics, metrics. The metrics are the only part a script computes.",
        "Scores are one to five against proposed thresholds. Read them as a map, not a mark.",
        "The authors' own caveat: the thresholds came from software practice and await validation. Keep it in mind.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Assessed with OQuaRE (Duque-Ramos et al., 2011). Scores are in the course document beside this lesson; the script that computed them is scripts/metrics.py."@en .
""",
    data=DVOCAB,
    check=dict(with_data=DVOCAB, metrics=True),
    expect=dict(),
    local="the scores come from scripts/metrics.py on data/01-vocabulary.ttl",
)
specs.register("o63", "oquare", "oqs")

o(
    oid="o64", module=M,
    title="Structure: depth, breadth, tangledness, cohesion",
    decides="The Trail's hierarchy is two deep, one wide on average, untangled and cohesive, which the structural metrics confirm; and gist, measured the same way, shows sixty-two roots because its structure lives in definitions the metrics do not read.",
    corner="referent",
    why="Five metrics describe the shape of the class tree. DITOnto is "
        "the longest path from the root to a leaf: the Trail's is 2 "
        "(Place, then Settlement), which scores 5, and gist's is 3. "
        "NOCOnto is the mean number of children per non-root class: 1 for "
        "both. NACOnto is the mean number of ancestors per leaf: under "
        "half for both, because most classes are roots. TMOnto is the mean "
        "number of parents per class that has one: 1 for both, which is "
        "to say no multiple inheritance anywhere, and o32 said why. "
        "LCOMOnto, the paper's cohesion measure, is the mean path length "
        "from leaf to root: about 1.4 for both.\n\n"
        "The number that stands out is gist's sixty-two root classes out of ninety-six. "
        "gist is not flat; it is defined. gist:Contract is Agreement and "
        "isUnderJurisdictionOf some GovernmentOrganization, by "
        "owl:equivalentClass, and a reasoner places it under Agreement. "
        "The metric reads rdfs:subClassOf and sees a root. Run the metrics "
        "on the reasoned ontology and the tree appears; run them on the "
        "asserted one and gist looks like a list. That is the first thing "
        "to know about structural metrics: they measure what was written, "
        "and an ontology that lets the reasoner do the tangling (o32, o55) "
        "will score as if it had no structure at all.\n\n"
        "The scores themselves are on the measured line for the Trail and "
        "in the diagram for both. On structure, both ontologies score 5 on "
        "nearly everything, which says less than it seems: a small, "
        "shallow, single-parented hierarchy is the easy case, and OQuaRE's "
        "thresholds were set for ontologies with thousands of classes.",
    diagram="""
   metric      what                                  Trail        gist        threshold for 5
   DITOnto     longest root-to-leaf path             2  (5)       3  (4)      at most 2
   NOCOnto     mean children per non-root class      1  (5)       1  (5)      at most 3
   NACOnto     mean ancestors per leaf               0.43 (5)     0.46 (5)    at most 2
   TMOnto      mean parents per class with a parent  1  (5)       1  (5)      at most 2
   LCOMOnto    mean leaf-to-root path length         1.43 (5)     1.46 (5)    at most 2

   gist: 62 roots of 96 classes, asserted. Reasoned, most of them have a parent.
   the metrics read rdfs:subClassOf; a defined hierarchy is invisible to them
""",
    learn=[
        "Depth, breadth, ancestors, tangledness, cohesion: five numbers, and for a small ontology all five come out well.",
        "Structural metrics read what is asserted. An ontology that defines its classes and lets the reasoner classify looks flat to them.",
        "Measure the reasoned ontology as well as the written one when the structure is in the definitions.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Structural metrics: see the MEASURED line, computed over the shipped vocabulary. gist's, for comparison, are in this lesson's diagram."@en .
""",
    data=DVOCAB,
    queries=[Query("Depth of every class in the shipped vocabulary", """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?class (COUNT(?up) AS ?depth) WHERE {
  ?class a owl:Class . FILTER(STRSTARTS(STR(?class), "https://example.org/bookshop-trail/schema#"))
  OPTIONAL { ?class rdfs:subClassOf+ ?up . FILTER(isIRI(?up)) }
} GROUP BY ?class ORDER BY DESC(?depth) ?class""", on="data", rows=17)],
    check=dict(with_data=DVOCAB, metrics=True),
    expect=dict(),
    local="the metrics come from scripts/metrics.py; the gist column from the same script on gistCore.ttl",
)
specs.register("o64", "oquare", "ontocleanHb")

o(
    oid="o65", module=M,
    title="Richness and coupling: what the metrics count, and what a style choice does to them",
    decides="The richness metrics are read with their small print: they count properties by declared domain, so an ontology that keeps domains sparse on principle scores low on richness, and gist does.",
    corner="referent",
    why="AROnto is attributes per class, INROnto relationships per class, "
        "RROnto the share of properties that are attributes, ANOnto "
        "annotations per class, CROnto individuals per class. The paper "
        "does not say how a property is assigned to a class, and the only "
        "workable reading is by rdfs:domain: a property belongs to the "
        "class it is declared on. scripts/metrics.py does that, and counts "
        "each member of a union domain.\n\n"
        "The consequence is on the diagram. The Trail declares a domain on "
        "nearly every property, so it scores 5 on attribute and "
        "relationship richness. gist declares domains sparingly, as a "
        "matter of principle set out in its README and in o31, so it "
        "scores 1 and 2 on the same metrics with sixty-six object "
        "properties and fifty datatype properties in the file. Nothing is "
        "poorer about gist; a design choice the metric cannot see has "
        "been counted as an absence. That is the general lesson about "
        "richness metrics, and it applies to CROnto too, which scores "
        "every pure vocabulary 1 because a schema has no individuals.\n\n"
        "ANOnto is the one to watch, because it measures the thing most "
        "ontologies neglect. The Trail has a label and a comment on every "
        "class, so it scores 5; gist has a preferred label, a definition, "
        "and often an example and a scope note, and scores higher still. "
        "The coupling metrics, CBOOnto, RFCOnto, WMCOnto and NOMOnto, are "
        "the software ones with the least ontological content: they add "
        "superclasses and properties per class, and for both ontologies "
        "come out low, which the thresholds read as good.",
    diagram="""
   metric      what                                    Trail         gist         note
   AROnto      datatype properties per class           1.82 (5)      0.31 (2)     by declared domain
   INROnto     object properties per class             1.47 (5)      0.12 (1)     gist keeps domains sparse, on purpose
   RROnto      attributes among all properties         74% (4)       28% (2)
   ANOnto      annotations per class                   2.0  (5)      3.6  (5)     the one that measures care
   CROnto      individuals per class                   0    (1)      0.08 (1)     a schema has no individuals
   RFCOnto     properties + superclasses per class     6.2  (3)      1.9  (5)
   WMCOnto     properties and relationships per class  3.3  (5)      0.4  (5)

   a metric counts what it can see; a principle it cannot see is counted as an absence
""",
    learn=[
        "Richness metrics assign properties to classes by domain. Read their small print before reading their scores.",
        "gist scores low on richness because it keeps domains sparse on principle. The metric measured the principle, not the quality.",
        "ANOnto is the metric that tracks care. It is the one to put in a gate.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Richness and coupling metrics: MEASURED line for the Trail; gist in the diagram. Properties are assigned to classes by rdfs:domain, each member of a union counted; that is scripts/metrics.py's reading of a formula the paper leaves open."@en .
""",
    check=dict(imports=["gist/gistCore.ttl"], metrics=True, metrics_namespace="https://w3id.org/semanticarts/ns/ontology/gist/"),
    expect=dict(),
    local="the gist metrics on the MEASURED line come from scripts/metrics.py over gistCore.ttl",
)
specs.register("o65", "oquare", "gistReadme")

o(
    oid="o66", module=M,
    title="The checks, by identifier",
    decides="The shipped vocabulary goes through the Ontology Quality Suite scoped to its own namespace, and the findings are read by identifier: a check that fires on every term is a policy not adopted, not a hundred mistakes.",
    corner="thought",
    why="The Ontology Quality Suite runs sixty-one checks in ten "
        "categories, each with an identifier, a severity, a message and a "
        "remediation: STR for structure, LOG for logic, QUA for "
        "documentation and metadata, STY for naming style, REA for what a "
        "reasoner finds, and so on. The SemOps Manual's chapter 9 is about "
        "running it as a gate, and its two rules are the ones o34 gave: "
        "scope to your own namespace, and assert on identifiers.\n\n"
        "Run on the shipped vocabulary with --own-namespace set to bs:, it "
        "reports a small set of identifiers, on the measured line. Two of "
        "them fire on nearly every term: QUA-009, no skos:prefLabel per "
        "language, and QUA-010, no skos:definition. The Trail uses "
        "rdfs:label and rdfs:comment, the pair gist's guide says not to "
        "use, so from the registry's point of view it has no labels or "
        "definitions at all. That is the manual's point exactly: a check "
        "that fires on every term is telling you about a policy you have "
        "not adopted. Adopt SKOS annotations, one pass of work, or drop the "
        "two checks from the registry with a note saying why. Either is a "
        "decision; leaving a hundred warnings in the report is not.\n\n"
        "The other findings are worth reading one at a time, with their "
        "remediation text, which is where the suite's knowledge lives. "
        "STR-003, a property with neither domain nor range, fires on bs:statedOn, whose subject is a reifier and whose value is a date the datatype map cannot hold, so o31 and o50 left both open on purpose; the right response is an editorial note the check can "
        "be pointed at, not a domain. A gate reports; a person decides.",
    diagram="""
   python -m ontology_suite checks --ontology data/01-vocabulary.ttl --own-namespace https://example.org/bookshop-trail/schema# --engine sparql

   identifier   fires on               reading
   QUA-009      nearly every term      a policy not adopted: skos:prefLabel per language
   QUA-010      nearly every term      the same: skos:definition
   STR-003      bs:statedOn            no domain or range, on purpose (o31, o50); note it, do not fix it
   STR-004      every class            no formal definition; most kinds are primitive, and should be (o46)

   assert on identifiers, never counts; scope to your namespace; read the remediation
""",
    learn=[
        "Read a report by identifier. Each has a remediation, and the remediation is the knowledge.",
        "A check that fires on every term is a policy question. Adopt the policy or drop the check, and write down which.",
        "Some findings are correct and wanted. STR-003 on a property left open on purpose is one; the answer is a note, not a change.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Checked with the Ontology Quality Suite, scoped to this namespace. QUA-009 and QUA-010 fire on most terms because the vocabulary uses rdfs:label and rdfs:comment; adopting SKOS annotations is one pass of work and is recorded as a decision to take."@en .
""",
    data=DVOCAB,
    check=dict(with_data=DVOCAB, oqs="checks"),
    expect=dict(oqs=["QUA-009", "QUA-010", "STR-003"]),
    local="the identifiers on the MEASURED line come from the Ontology Quality Suite: pip install ontology-quality-suite",
)
specs.register("o66", "oqs", "semopsGate")

STYLE_SHAPES = """
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix bt:   <https://example.org/bookshop-trail/> .

# Style shapes for a vocabulary, after gist's validation/shapes/ontologyShapes.ttl,
# written in SHACL Core so that the editor runs them. Open data/01-vocabulary.ttl
# in one tab and this file in another, choose it under Shapes, Validate.

# The targets are scoped to the Trail's own namespace, as gist's are to
# gist's: a borrowed class is declared here but documented upstream, and a
# finding about it would be about someone else's file.
bt:ClassStyleShape
    a          sh:NodeShape ;
    sh:target  [ a sh:SPARQLTarget ;
                 sh:select \"\"\"SELECT $this WHERE { $this a <http://www.w3.org/2002/07/owl#Class> .
                              FILTER(STRSTARTS(STR($this), "https://example.org/bookshop-trail/schema#")) }\"\"\" ] ;
    sh:property [ sh:path rdfs:label ; sh:minCount 1 ; sh:message "Every class has a label." ] ;
    sh:property [ sh:path rdfs:comment ; sh:minCount 1 ; sh:message "Every class has a comment or definition." ] ;
    sh:property [ sh:path skos:definition ; sh:minCount 1 ; sh:severity sh:Warning ;
                  sh:message "gist style: a skos:definition rather than rdfs:comment." ] .

bt:PropertyStyleShape
    a          sh:NodeShape ;
    sh:target  [ a sh:SPARQLTarget ;
                 sh:select \"\"\"SELECT $this WHERE { $this a ?t . FILTER(?t IN (<http://www.w3.org/2002/07/owl#ObjectProperty>, <http://www.w3.org/2002/07/owl#DatatypeProperty>))
                              FILTER(STRSTARTS(STR($this), "https://example.org/bookshop-trail/schema#")) }\"\"\" ] ;
    sh:property [ sh:path rdfs:label ; sh:minCount 1 ; sh:severity sh:Warning ; sh:message "Every property has a label." ] .

# Every rdf:type value in the file is a declared class: the instance shape.
bt:DeclaredTypeShape
    a                    sh:NodeShape ;
    sh:targetObjectsOf   rdf:type ;
    sh:or ( [ sh:class owl:Class ]
            [ sh:in ( owl:Class owl:ObjectProperty owl:DatatypeProperty owl:AnnotationProperty owl:Ontology
                      owl:TransitiveProperty owl:SymmetricProperty owl:FunctionalProperty owl:AllDisjointClasses
                      owl:Restriction rdfs:Datatype owl:NamedIndividual ) ] ) ;
    sh:message "A type that is not a declared class." .
"""

o(
    oid="o67", module=M,
    title="Style shapes: the vocabulary validated like data",
    decides="The house style is written as SHACL shapes that target owl:Class and the property types, as gist does for itself, and the shipped vocabulary is validated against them in the editor.",
    corner="symbol and thought",
    why="An ontology is an RDF graph, so a shape can target it. gist's "
        "repository has validation/shapes/ontologyShapes.ttl, run on every "
        "commit: a class shape that requires title-case preferred labels "
        "and a definition, a property shape that requires lower-case "
        "labels, and an instance shape that requires every rdf:type value "
        "to be a declared class. The targets are SPARQL-based, selecting "
        "terms in the gist namespace; the version here uses "
        "sh:targetClass owl:Class and sh:targetObjectsOf rdf:type so that "
        "it stays in SHACL Core and runs in the editor.\n\n"
        "On the shipped vocabulary the shapes report what o66's checks "
        "reported, in the vocabulary of the SHACL course: every class has "
        "a label and a comment, so the two Violation-level constraints "
        "pass; no class has a skos:definition, so the Warning fires "
        "seventeen times, once per Trail class; every type in the file is a declared class, "
        "so the instance shape is quiet. The report is the same fact as "
        "QUA-010 from a different tool, and the SemOps Manual's advice is "
        "to write a check both ways, as a query and as a shape, so that two engines corroborate rather than agree by construction.\n\n"
        "This is the SHACL course's whole method turned on the vocabulary: "
        "a shapes graph, a report, a severity chosen by whoever owns the "
        "policy. It runs on any vocabulary you are handed, which is how "
        "to form a first opinion of one.",
    diagram="""
   shape                  targets                   checks                          on the Trail
   ClassStyleShape        owl:Class in bs:          rdfs:label (Violation)          17 pass
                                                    rdfs:comment (Violation)        17 pass
                                                    skos:definition (Warning)       17 warnings: the policy not adopted
   PropertyStyleShape     properties in bs:         rdfs:label (Warning)            all pass
   DeclaredTypeShape      every rdf:type value      is a declared class             quiet

   the editor: vocabulary in one tab, shapes in another, Validate
""",
    learn=[
        "A vocabulary is a graph; shapes can target it. gist validates its own style that way on every commit.",
        "Write a check as a shape and as a query. Two engines that corroborate are worth more than one that agrees with itself.",
        "Run style shapes on any vocabulary you are handed. It is the fastest first opinion there is.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Validated against style-shapes.ttl beside this lesson. The vocabulary passes every Violation-level constraint and collects a warning per class for the missing skos:definition."@en .
""",
    data=DVOCAB,
    companions={"style-shapes.ttl": STYLE_SHAPES},
    shapes="style-shapes.ttl",
    check=dict(with_data=DVOCAB, shacl=STYLE_SHAPES),
    expect=dict(shacl_violations=0),
    notes="Open in the editor opens this lesson with the shapes in a second tab; to validate the whole vocabulary, load data/01-vocabulary.ttl "
          "in the first tab instead, keep the shapes tab, and press Validate.",
)
specs.register("o67", "gistShapes", "semopsHouseRules")

o(
    oid="o68", module=M,
    title="What the metrics cannot see",
    decides="Metrics and checks are one part of a gate that also runs the reasoner, the OntoClean queries, the style shapes and the competency questions, because a five-out-of-five ontology can still be wrong and no metric sees rigidity or meaning.",
    corner="thought",
    why="OQuaRE scores the Trail 5 on almost everything, and the Quality "
        "Suite's violations come out at zero once the policy questions "
        "are decided. Neither knows whether Author is a role, whether Work "
        "is one class or two, whether the definitions are circular, "
        "whether bs:founded should be functional, or whether the ontology "
        "can answer question 7 in the brief. Metrics count what is "
        "written; checks pattern-match it. Meaning is not in the graph "
        "unless someone put it there, and the parts of this course that "
        "put it there, modules 02 and 04, are the parts no metric "
        "reads.\n\n"
        "So a gate has more than one instrument. The reasoner: "
        "consistent, no unsatisfiable classes, with the whole dataset "
        "loaded (o57). The OntoClean queries over the rigidity annotations "
        "(o13). The definition audit (o22). The style shapes (o67) and "
        "the checks by identifier (o66). And the competency questions, "
        "run as queries against the data, which are the only instrument "
        "that tests whether the ontology does its job. The SemOps Manual "
        "calls them the closest thing ontology work has to a requirement, "
        "and makes them executable as .cq.rq tests; this lesson runs three "
        "of the brief's questions against the Trail's data as its "
        "measured line, and module 12 runs more.\n\n"
        "The critical literature on OQuaRE says the same from the other "
        "side: the thresholds were proposed rather than validated, the "
        "metrics overlap, and several measure a style choice as if it "
        "were a defect, which o65 showed on gist. None of that makes the "
        "metrics useless. It makes them one instrument among six, and the "
        "one to trust least on its own.",
    diagram="""
   instrument                    sees                                  blind to
   OQuaRE metrics                shape and counts                      meaning, rigidity, style choices it counts as absences
   OQS checks                    patterns, by identifier               whether the pattern is wanted
   style shapes                  the house style                       whether a definition is true
   the reasoner                  contradiction, dead classes           errors that are consistent
   OntoClean queries             rigidity, identity, dependence        anything not annotated
   competency questions          whether the questions get answered    questions nobody wrote down

   a gate is all six; the last is the one that tests the job
""",
    learn=[
        "A five-out-of-five ontology can be wrong. Metrics count; they do not read.",
        "Six instruments in the gate, and the competency questions are the one that tests whether the ontology does its job.",
        "Trust the metrics least on their own. Their authors said so first.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "The gate: HermiT over the whole dataset; the OntoClean queries; the definition audit; style-shapes.ttl; the Quality Suite scoped to bs:; and the competency questions as queries. Three of the questions run below."@en .
""",
    data="bookshop-trail-1.1.ttl",
    queries=[
        Query("Question 2: towns on the trail with no bookshop", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?town WHERE { ?town a bs:Settlement . FILTER NOT EXISTS { ?shop bs:locatedIn ?town } } ORDER BY ?town""", on="data", rows=4),
        Query("Question 1: shops in Wales, by the path", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?shop WHERE { ?shop a bs:Bookshop ; bs:locatedIn ?town . ?town bs:within+ bt:place-wales } ORDER BY ?shop""", on="data", rows=4),
        Query("Question 7: authors influenced, at any remove, by Rhona Blackwood", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?author WHERE { ?author bs:influencedBy+ bt:author-rhona-blackwood } ORDER BY ?author""", on="data"),
    ],
    check=dict(with_data="bookshop-trail-1.1.ttl"),
    expect=dict(),
)
specs.register("o68", "semopsCq", "oquare")
