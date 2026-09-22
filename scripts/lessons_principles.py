# -*- coding: utf-8 -*-
"""Module 05 -- Design principles: gist, the OBO Foundry and the SemOps Manual."""
from ontocat import o, Query
import specs

M = "05-principles"

DECL = """
# Borrowed annotation properties, declared so the file is OWL 2 DL on its own.
skos:prefLabel      a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:scopeNote      a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
dct:source          a owl:AnnotationProperty .
"""

o(
    oid="o28", module=M,
    title="Minimal: as few terms as will answer the questions",
    decides="The Trail has twenty-five classes because ten questions need them; a class that no question needs is not added, and gist's ninety-six for a whole enterprise is the standard to be measured against.",
    corner="thought",
    why="gist describes itself as 'the maximum coverage of typical business "
        "ontology concepts with the fewest number of primitives and the "
        "least amount of ambiguity', and it does it in about a hundred "
        "classes, sixty-odd object properties and fifty datatype "
        "properties. That is an enterprise. The Trail, with ten questions "
        "to answer, has twenty-five classes and eighty-four properties, "
        "and the properties are the number to watch: every one is a column "
        "someone will have to fill.\n\n"
        "Every term costs the same whether it is used or not: a label in "
        "each language, a definition, a review, a place in the "
        "documentation, a check in the gate, and a decision every time "
        "someone wonders whether to use it or its neighbour. A term nobody "
        "uses is defined badly, because nobody finds out. The discipline is "
        "the one from o07: a term is admitted when a question needs it, and "
        "the question is written down beside it.\n\n"
        "The same discipline applies to axioms. gist keeps domains and "
        "ranges sparse and declares no inverses, not from laziness but "
        "because each one is a commitment that some future dataset will "
        "break, and o31 takes those two up. Minimal is not small for its "
        "own sake. It is the number of terms at which each one is still "
        "looked after.",
    diagram="""
                           classes   object props   datatype props   for
   gist 14                    ~96          ~66             ~50       an enterprise
   the Trail                   25           32              42       ten questions

   each term costs: a label per language, a definition, a review,
   a place in the docs, a check in the gate, and a decision every
   time someone wonders whether to use it
""",
    learn=[
        "A term is admitted by a question, not by a noun in the brief. Keep the question beside the term.",
        "Properties are the number to watch. Each is a column someone fills, and the Trail has nearly as many as gist has classes.",
        "Minimal means every term is still looked after. That is the size to aim for.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Twenty-five classes, thirty-two object properties, forty-two datatype properties, ten annotation properties, for ten competency questions. Compare gist 14: about ninety-six classes for an enterprise."@en .

# One class and its question, side by side.
bs:TrailSegment
    a                owl:Class ;
    skos:prefLabel   "Trail Segment"@en ;
    skos:definition  "A walking route between two bookshops, with a length."@en ;
    skos:scopeNote   "Exists for question 3: what can be walked to from a shop, and how far."@en .

# One that was proposed and refused.
bs:Festival
    a                   owl:Class ;
    owl:deprecated      true ;
    skos:prefLabel      "Festival"@en ;
    skos:editorialNote  "Proposed because Wigtown and Hay have festivals. Refused: no competency question mentions one. Kept as a deprecated stub so the refusal is on record."@en .
owl:deprecated  a owl:AnnotationProperty .
""",
    queries=[Query("Every class in the shipped vocabulary, with what it exists for", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class ?comment WHERE { ?class a owl:Class ; rdfs:comment ?comment . FILTER(STRSTARTS(STR(?class), "https://example.org/bookshop-trail/schema#")) } ORDER BY ?class""",
                   on="data", rows=17)],
    data="01-vocabulary.ttl",
    check=dict(profile=True, with_data="01-vocabulary.ttl", metrics=True),
    expect=dict(dl=True),
)
specs.register("o28", "gistReadme", "oboScope")

o(
    oid="o29", module=M,
    title="Meaning in the ontology, rules in the shapes",
    decides="An axiom is written only when it is true of every dataset the ontology could describe; anything that is a rule about this dataset, for this purpose, is a SHACL shape, and bs:founded stays non-functional for exactly that reason.",
    corner="referent",
    why="An OWL axiom is a claim about the world. It holds for every "
        "dataset that uses the term, forever, and a reasoner will draw "
        "conclusions from it whether or not anyone wanted them. A SHACL "
        "shape is a rule about a dataset: this data, for this website, "
        "must look like this, and a validator will report where it does "
        "not. The two look alike on the page and behave nothing alike, and "
        "gist's tenth rule for restrictions is the test that tells them "
        "apart: if an instance of X did not conform to Y, would it still be "
        "an X? If yes, Y is a rule, not meaning, and it belongs in a shape.\n\n"
        "The Trail's bs:founded is the case. Every shop has one founding "
        "year; that is surely true. But four shops have two recorded, "
        "because the guidebooks disagree, and the brief asks for both to "
        "be kept. Declare the property functional and the reasoner does "
        "not flag a disagreement: it concludes that 1921 and 1923 are the "
        "same value, which for literals is a contradiction, and the whole "
        "dataset is inconsistent. This lesson's file does exactly that, "
        "and HermiT says so. The shipped vocabulary leaves bs:founded "
        "non-functional and says why in its comment; the SHACL course's "
        "s04 carries 'exactly one founding year' as a shape, where a second "
        "value is a finding to read rather than a contradiction to "
        "resolve.\n\n"
        "The general habit is to constrain relationships less than feels "
        "natural. A domain that is too narrow retypes things (o38); a cardinality that is too tight merges or contradicts (o47); a "
        "property declared functional because 'it always is' becomes false "
        "the day a second source appears. gist keeps domains and ranges "
        "sparse for this reason, and puts data constraints in shapes. "
        "Meaning in the ontology, rules in the shapes, and when in doubt, "
        "a shape.",
    diagram="""
   "every shop has exactly one founding year"

   as an axiom                                    as a shape
   bs:founded a owl:FunctionalProperty            sh:path bs:founded ; sh:maxCount 1
   two values => the reasoner says                two values => the validator reports
   INCONSISTENT, for the whole dataset            one row, naming the shop; severity is yours

   the test (gist rule 10):
   if a shop had two founding years on record, would it still be a shop?  yes  => a shape
""",
    learn=[
        "An axiom holds for every dataset forever. A shape holds for this dataset for this purpose. Ask which you mean.",
        "Would it still be an X? If yes, it is a rule about data, and it belongs in SHACL.",
        "Constrain relationships less than feels natural. Every tight constraint is a future contradiction with a date on it.",
    ],
    body=DECL + """
bs:Bookshop  a owl:Class ; skos:prefLabel "Bookshop"@en .

# The axiom that turns a disagreement into a contradiction.
bs:founded
    a                owl:DatatypeProperty, owl:FunctionalProperty ;
    rdfs:domain      bs:Bookshop ;
    skos:prefLabel   "founded"@en ;
    skos:definition  "The year a shop began trading."@en ;
    skos:editorialNote "Declared functional here to show what happens. The shipped vocabulary does not, because sources disagree for four shops."@en .

bt:shop-ex-libris
    a           bs:Bookshop ;
    bs:founded  "1921"^^xsd:integer, "1923"^^xsd:integer .
""",
    companions={"founded-shape.ttl": """
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix bs: <https://example.org/bookshop-trail/schema#> .
@prefix bt: <https://example.org/bookshop-trail/> .

# The same intention as a rule about the data: one founding year expected,
# a second one reported for someone to look at, and the dataset stays
# consistent. The SHACL course's s04 is the full version.
bt:FoundedShape
    a               sh:NodeShape ;
    sh:targetClass  bs:Bookshop ;
    sh:property [
        sh:path      bs:founded ;
        sh:maxCount  1 ;
        sh:severity  sh:Warning ;
        sh:message   "{$this} has more than one founding year on record; the sources disagree." ;
    ] .
"""},
    shapes="founded-shape.ttl",
    notes="Open in the editor opens founded-shape.ttl in a second tab. Validate: one warning. The editor's engine says conforms, because "
          "only violations count against conformance there; pySHACL, which measured this lesson, says does not conform for the same "
          "report, because the specification's default counts warnings too. The SHACL course's s03 is about that difference. Either way "
          "the shop is named and the graph is not contradicted; the reasoner's verdict on the same two triples is that the whole graph is "
          "inconsistent.",
    check=dict(profile=True, reason=True, shacl="""
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix bs: <https://example.org/bookshop-trail/schema#> .
@prefix bt: <https://example.org/bookshop-trail/> .
bt:FoundedShape a sh:NodeShape ; sh:targetClass bs:Bookshop ;
    sh:property [ sh:path bs:founded ; sh:maxCount 1 ; sh:severity sh:Warning ; sh:message "more than one founding year" ] .
"""),
    expect=dict(dl=True, consistent=False, shacl_conforms=False, shacl_violations=0),
)
specs.register("o29", "gistRestrictions", "shaclSpec")

o(
    oid="o30", module=M,
    title="Pragmatism and purity",
    decides="A departure from a principle is allowed when it changes only a name or a convenience, refused when it changes an inference or a query, and written on the term either way.",
    corner="thought",
    why="Every ontology that is used has compromises in it, and the good "
        "ones have them written down. The Trail has five. bs:Work is a "
        "work and an edition. Four properties are named against the gist "
        "standard. Inverses are declared, which gist forbids, so that a "
        "reasoning lesson has something to infer. xsd:gYear is kept for "
        "years although it puts the data outside OWL 2 DL, because the "
        "portability trap it creates is one of the SPARQL course's best "
        "lessons. Authors are minted under a role name. Each is on the term "
        "as an editorial note, and this file collects them.\n\n"
        "The rule that decides is about consequences. A departure that "
        "changes only a name or a convenience is cheap: nothing a reasoner "
        "does depends on whether the property is called author or "
        "hasAuthor, and 145 queries depend on the first. A departure that "
        "changes an inference or a query result is not cheap, because it "
        "will be paid by someone who does not know it is there. Declaring "
        "inverses changes what a reasoner derives; the Trail does it on "
        "purpose and says so, and the note is what makes that a decision.\n\n"
        "Purity has its own costs. BFO is philosophically rigorous and its "
        "IRIs are numbers; gist chose everyday words and a hundred classes, "
        "and both are used by people who had to ship something. Chapter 14 of the SemOps Manual is a ledger of what a toolchain does not do, and that is the model: an ontology should carry its own "
        "ledger. The unrecorded compromise is the only kind that is a "
        "mistake.",
    diagram="""
   compromise                          changes           verdict          recorded on

   Work = work + edition               an identity        allowed, noted   bs:Work
   author, not hasAuthor               a name only        allowed, noted   the property
   inverses declared                   an inference       allowed on purpose, noted
   xsd:gYear kept                      a profile          allowed for the lesson, noted
   author- as an instance infix        a name only        allowed, noted   bs:Author

   rule: cheap if it changes a name; dear if it changes an inference or a result; write it down either way
""",
    learn=[
        "The unrecorded compromise is the only kind that is a mistake. Write each one on the term it affects.",
        "Weigh a departure by what it changes: a name is cheap, an inference or a query result is dear.",
        "Rigour and usefulness are both virtues, and an ontology carries a ledger of where it traded one for the other.",
    ],
    body=DECL + """
bs:Work       a owl:Class ;
    skos:editorialNote "Compromise: work and edition in one class. Changes an identity criterion; allowed because the dataset never needs two editions of one work. Split the day it does."@en .
bs:author     a owl:ObjectProperty ;
    skos:editorialNote "Compromise: gist style would be hasAuthor. Changes a name only; 145 queries use this one."@en .
bs:wrote      a owl:ObjectProperty ; owl:inverseOf bs:author ;
    skos:editorialNote "Compromise: gist declares no inverses. Changes what a reasoner derives; kept on purpose so that module 08 has an inference to show, and the SPARQL course's q44 something to construct."@en .
bs:founded    a owl:DatatypeProperty ;
    skos:editorialNote "Compromise: values are xsd:gYear, outside the OWL 2 datatype map. Changes the profile of the data, not the vocabulary; kept for the SPARQL course's portability lesson. A conformant copy ships beside it."@en .
bs:Author     a owl:Class ;
    skos:editorialNote "Compromise: instances minted as author-, a role name. Changes a name only."@en .
""",
    queries=[Query("The ledger: every recorded compromise", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?term ?note WHERE { ?term skos:editorialNote ?note . FILTER(STRSTARTS(?note, "Compromise:")) } ORDER BY ?term""", rows=5)],
    check=dict(profile=True),
    expect=dict(dl=True),
)
specs.register("o30", "gistReadme", "blogUpper")

o(
    oid="o31", module=M,
    title="Disjoint at the top, sparse in the middle, no inverses",
    decides="The top-level kinds are declared pairwise disjoint, domains and ranges are declared only where every use will agree, and inverses are not declared unless a lesson needs one.",
    corner="referent",
    why="gist's README lists its structural habits in one breath: sparse "
        "domain and range specifications for broader applicability, no "
        "inverse properties, and extensive fine-grained disjointness at the "
        "highest level. The three go together and each is a bet about the "
        "future.\n\n"
        "Disjointness at the top is the cheap axiom that catches the "
        "expensive mistake. Nothing is both a place and a bookshop, and "
        "saying so lets a reasoner notice when a data load types one thing "
        "as both. The Trail declares its ten top-level kinds disjoint in one "
        "owl:AllDisjointClasses, and four subkinds of Place disjoint in "
        "another. Below that it stops: Author and TrailMember are roles and "
        "a shop can be both a member and a shop, so disjointness lower down "
        "is where the tenth rule from o29 starts to bite.\n\n"
        "Sparse domains and ranges are the opposite bet. A domain is an "
        "inference rule: whatever has this property is of this class. State "
        "bs:locatedIn's domain as Bookshop and every publisher with an "
        "address becomes a bookshop; the Trail states a union instead, and "
        "leaves bs:claimedBy with no domain at all because its subject is a "
        "statement. gist goes further and leaves most domains open, on the "
        "principle that a property is more reusable than any class it was "
        "first used with.\n\n"
        "No inverses is the bet that one direction is enough. Every "
        "inverse doubles the query paths, the data, the shapes and the "
        "reasoner's work, and buys nothing a SPARQL caret or a SHACL "
        "inverse path does not. gist removed all of them in version 12 and "
        "picks the direction with fewer results, child to parent. The "
        "Trail keeps two on purpose (o30).",
    diagram="""
   disjoint at the top      [] a owl:AllDisjointClasses ; owl:members ( Place Bookshop Person Publisher Work ... )
                            cheap; catches a thing typed as two kinds at once

   sparse in the middle     bs:locatedIn  rdfs:domain [ unionOf ( Bookshop Publisher ) ]
                            bs:claimedBy  no domain: its subject is a statement
                            a domain is an inference rule, and a narrow one retypes things

   no inverses              isPartOf, not hasPart; ^bs:imprintOf in SPARQL, sh:inversePath in SHACL
                            one direction, fewer results, half the paths
""",
    learn=[
        "Declare the top-level kinds disjoint. It is one axiom and it catches the worst data error there is.",
        "A domain is an inference rule. Declare one only when every use of the property will agree with it, and use a union when two will not.",
        "One direction per relationship. The query language and the shapes language both walk it backwards for free.",
    ],
    body=DECL + """
bs:Place a owl:Class . bs:Bookshop a owl:Class . bs:Person a owl:Class .
bs:Publisher a owl:Class . bs:Work a owl:Class . bs:Event a owl:Class .
[] a owl:AllDisjointClasses ; owl:members ( bs:Place bs:Bookshop bs:Person bs:Publisher bs:Work bs:Event ) .

bs:locatedIn
    a            owl:ObjectProperty ;
    rdfs:domain  [ a owl:Class ; owl:unionOf ( bs:Bookshop bs:Publisher ) ] ;
    rdfs:range   bs:Place ;
    skos:scopeNote "Domain is a union: shops and publishers both have one. A domain of Bookshop alone would retype every publisher."@en .

bs:claimedBy
    a            owl:ObjectProperty ;
    rdfs:range   bs:Source ;
    skos:scopeNote "No domain. The subject is a claim about a statement, which no class here describes."@en .
bs:Source  a owl:Class .

bs:imprintOf
    a            owl:ObjectProperty ;
    rdfs:domain  bs:Publisher ;
    rdfs:range   bs:Publisher ;
    skos:scopeNote "Child to parent, the direction with fewer results. No hasImprint declared here; ask for ^bs:imprintOf."@en .

# What the disjointness catches: one thing typed as two kinds.
bt:oddity  a bs:Place, bs:Bookshop .
""",
    check=dict(profile=True, reason=True),
    expect=dict(dl=True, consistent=False),
)
specs.register("o31", "gistInverses", "primerDisjoint")

o(
    oid="o32", module=M,
    title="One parent, mostly",
    decides="Every backbone class has one parent; a second parent is allowed only for a rigid subkind that is both things in every circumstance, and the tangledness is measured rather than assumed.",
    corner="referent",
    why="Multiple inheritance is legal in OWL and usually a sign that two "
        "questions have been answered with one class. A class with two "
        "parents has two identity criteria to reconcile and two sets of "
        "inherited axioms to keep consistent, and a reader has to hold both "
        "in mind to know what it means. OQuaRE measures the habit as tangledness, TMOnto, the mean number of parents per class, and gives full marks only at two or fewer.\n\n"
        "The legitimate case is a rigid subkind that is both things in every circumstance. "
        "bs:Translation is a Work; it is not also something else. A "
        "hypothetical bs:PublisherBookshop, a shop that also publishes, "
        "would be tempting and wrong: it is a Bookshop that plays the "
        "publishing role, and the role goes on the instance, not into the "
        "class tree. OntoClean's rule from module 02 sorts these out before "
        "the tree is drawn.\n\n"
        "gist's answer is a different one. Its classes are mostly single-"
        "parented, and where a class has several conditions it is defined "
        "by an owl:equivalentClass over an intersection, which the reasoner "
        "classifies rather than a human asserting a second parent. That is "
        "not tangledness; it is the reasoner doing the tangling and showing "
        "its work. The metric run on this lesson's file counts the one "
        "seeded second parent; run on gist it finds the classes whose "
        "asserted parents number more than one, and there are few.",
    diagram="""
   single inheritance            seeded second parent                   the alternative

   Work                          Bookshop   Publisher                   Bookshop
     Translation                     \\       /                             ^
                                 PublisherBookshop  (two parents)     bt:shop-x a bs:Bookshop ;
                                 two identity criteria, two axiom          bs:publishes bt:work-y   (a role, on the instance)
                                 sets, one confused reader

   TMOnto: mean parents per class, over classes with a parent. Score 5 at 2 or below.
""",
    learn=[
        "One parent per backbone class. A second parent is usually a role that belongs on the instance.",
        "Let the reasoner do the tangling: define a class by an intersection and classify, rather than assert two parents.",
        "Measure tangledness rather than guess. TMOnto is one number and it is easy to read.",
    ],
    body=DECL + """
bs:Work         a owl:Class .
bs:Translation  a owl:Class ; rdfs:subClassOf bs:Work ;
    skos:scopeNote "One parent. A translation is a work in every circumstance."@en .
bs:Bookshop     a owl:Class .
bs:Publisher    a owl:Class .

# The seeded second parent, for the metric to count.
bs:PublisherBookshop  a owl:Class ; rdfs:subClassOf bs:Bookshop, bs:Publisher ;
    skos:editorialNote "Two parents: a shop that also publishes. Wrong: publishing is a role, and belongs on the instance."@en .

# The alternative: the role on the instance.
bs:publishes  a owl:ObjectProperty ; rdfs:range bs:Work .
bt:shop-marginalia  a bs:Bookshop ; bs:publishes bt:work-pamphlet .
bt:work-pamphlet    a bs:Work .
""",
    queries=[Query("Classes with more than one asserted parent", """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class (COUNT(?parent) AS ?parents) WHERE { ?class rdfs:subClassOf ?parent . FILTER(isIRI(?parent)) }
GROUP BY ?class HAVING (COUNT(?parent) > 1)""", rows=1)],
    check=dict(profile=True, metrics=True),
    expect=dict(dl=True),
)
specs.register("o32", "oquare", "ontocleanHb")

o(
    oid="o33", module=M,
    title="Built with the people who will read it",
    decides="Every definition records who agreed it and when, the domain experts review the model in a form they can read, and a disagreement about territory is modelled rather than adjudicated by the modeller.",
    corner="thought",
    why="The process of bringing an ontology into an organisation is a "
        "social one. People have to get together and work out what kinds "
        "of things they have, what words are used for them across the "
        "business, and how each can be defined without going round in a "
        "circle. That process builds a team, and sometimes it exposes a "
        "fault line that was already there. The output is a vocabulary in "
        "common; the process is at least half the value.\n\n"
        "The SemOps Manual names the two ways it goes wrong. Definitions "
        "are territory: when two departments disagree about a term, each "
        "definition is load-bearing for someone, and a modeller who picks one without saying so has made a decision they had no authority to make. Model "
        "the disagreement, get the adjudication from someone who can make "
        "it stick, and record who decided. And the priesthood problem: "
        "when only three people can read the model, the domain experts "
        "stop correcting it, and the model records the modeller's "
        "understanding rather than theirs. The remedy is not to teach "
        "everyone OWL. It is to put the model in front of them in a form "
        "they can check, which is what the editor's graph view is for, and "
        "why every lesson in this course opens in it.\n\n"
        "OBO Foundry principles FP-010 and FP-011 say the same from the "
        "other side: development is collaborative, and a named person is "
        "responsible for communication. This file puts both on the ontology "
        "node, and puts the decision trail on the terms.",
    diagram="""
   the workshop                                   the record

   who has what kinds of thing ---.               skos:editorialNote "Agreed by the committee, 12 March 2025 ..."
   what words are used for them ---+--> terms --> dct:contributor  bt:committee-2025-03-12
   how each is defined, non-circularly            a named person responsible (FP-011)

   the graph view: the form a domain expert can check without reading OWL
   territory: model both meanings; someone with authority chooses; write down who
""",
    learn=[
        "Building the vocabulary is a social process, and the team it builds is part of the return.",
        "Model a disagreement about territory; do not settle it. Get a decision from someone who can make it stick, and record who.",
        "If the experts cannot read the model, they cannot correct it. Show them the graph, not the axioms.",
    ],
    body=DECL + """
dct:contributor  a owl:AnnotationProperty .
dct:created      a owl:AnnotationProperty .

<https://example.org/bookshop-trail/schema>
    a                owl:Ontology ;
    skos:prefLabel   "The Bookshop Trail schema"@en ;
    dct:contributor  bt:committee-2025-03-12, bt:person-events-secretary ;
    skos:editorialNote "Responsible for communication about this vocabulary: the events secretary (FP-011). Reviewed by the committee in the editor's graph view before each release."@en .

bt:committee-2025-03-12   skos:prefLabel "Trail committee, 12 March 2025"@en .
bt:person-events-secretary skos:prefLabel "The events secretary"@en .

# A term with its decision trail.
bs:Bookshop
    a                   owl:Class ;
    skos:prefLabel      "Bookshop"@en ;
    skos:definition     "A business that sells books to the public from premises."@en ;
    skos:editorialNote  "Agreed by the committee, 12 March 2025. The Hay shops asked whether a market stall counts; decided no, and 'from premises' was added."@en ;
    dct:contributor     bt:committee-2025-03-12 .

# A disagreement modelled rather than settled: two meanings of 'in stock'.
bs:stocks
    a                   owl:ObjectProperty ;
    skos:prefLabel      "stocks"@en ;
    skos:definition     "The shop has at least one copy of the work on the shelf now."@en ;
    skos:editorialNote  "The website team and the buyers disagreed: on the shelf now, or on the list to order. Both terms kept; the website uses this one. Decided by the chair, 9 April 2025."@en .
bs:lists
    a                   owl:ObjectProperty ;
    skos:prefLabel      "lists"@en ;
    skos:definition     "The shop lists the work for sale and can order it."@en .
""",
    queries=[Query("Every decision on record, with who made it", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?term ?note WHERE { ?term skos:editorialNote ?note . FILTER(CONTAINS(?note, "ecided") || CONTAINS(?note, "Agreed")) }""", rows=2)],
    check=dict(profile=True),
    expect=dict(dl=True),
)
specs.register("o33", "semopsTerritory", "blogTeam")

o(
    oid="o34", module=M,
    title="Ontologies like code: the loop and the gate",
    decides="The vocabulary lives in version control, is checked in the editor as it is written and at the gate before it merges, and the checks are asserted by identifier and scoped to the Trail's own namespace.",
    corner="thought",
    why="The SemOps Manual's maturity model has five levels and says most "
        "of the return is in the step from two to three: from 'we treat "
        "ontologies like code' to 'the standards are enforced without "
        "anyone remembering to enforce them'. Level two is a decision: put "
        "the files in git, check them in the editor as you type, run the "
        "checks locally. Level three is a gate: the same checks in CI, with "
        "a non-zero exit code when something is wrong.\n\n"
        "Two lessons from the manual's chapter 9 decide whether the gate "
        "survives its first month. First, scope the findings to your own "
        "namespace. The Trail borrows SKOS, GeoSPARQL and PROV terms; a "
        "gate that reports the W3C's documentation habits alongside the "
        "Trail's will be switched off by the second week. The Quality "
        "Suite's --own-namespace flag keeps the imports resolved and "
        "filters the report to the terms you control. Second, assert on "
        "check identifiers, not counts: 'LOG-001 must fire on the fixture "
        "with the seeded contradiction' survives a registry upgrade; "
        "'expected 23 findings' does not.\n\n"
        "This course is built that way. Every lesson is generated from a "
        "catalogue, every measured line comes from a run, the checker "
        "fails on any expectation that does not hold, and the seeded "
        "faults exist so that the checks can be seen to fire. That is the "
        "practice the manual describes, applied to a course about "
        "ontologies rather than to an ontology.",
    diagram="""
   level 2: ontologies like code            level 3: the gate

   files in git                             the same checks in CI
   check in the editor, in seconds          --fail-on Violation, non-zero exit
   competency questions as .cq.rq tests     --own-namespace: findings about your terms only
   review in the graph view                 assert by check id, never by count

   this lesson's file, through the suite with --own-namespace: the ids below, and only those
""",
    learn=[
        "Put the vocabulary in version control and check it as you type. That is level two, and it is a decision, not a project.",
        "The gate reports your namespace only, and tests assert check identifiers. Both are what keep a gate switched on.",
        "A check that has never fired is indistinguishable from a clean model. Keep a fixture that makes each one fire.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a               owl:Ontology ;
    skos:prefLabel  "The Bookshop Trail schema"@en ;
    skos:editorialNote "Checked in the editor as written; gated in CI with the Ontology Quality Suite, scoped to the bs: namespace, failing on Violation."@en .

# A seeded fault for the gate to find: a class disjoint with its own ancestor.
bs:Work         a owl:Class ; skos:prefLabel "Work"@en ; skos:definition "A book."@en .
bs:Translation  a owl:Class ; rdfs:subClassOf bs:Work ; owl:disjointWith bs:Work ;
    skos:prefLabel "Translation"@en ; skos:definition "A work that is a translation of another."@en ;
    skos:editorialNote "Seeded: disjoint with its own parent. LOG-001 must fire, and REA-021 when the reasoner runs."@en .
""",
    local="the gate itself is the Ontology Quality Suite from the command line: pip install ontology-quality-suite",
    check=dict(profile=True, reason=True, oqs="ontology"),
    expect=dict(dl=True, unsat=["Translation"], oqs=["LOG-001"]),
)
specs.register("o34", "semopsMaturity", "semopsGate")
