# -*- coding: utf-8 -*-
"""Module 08 -- Logic and inference: what follows, and three ways to reach it."""
from ontocat import o, Query, DPLACES
import specs

M = "08-reasoning"

DECL = """
skos:prefLabel      a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
"""

o(
    oid="o51", module=M,
    title="What follows from what you said",
    decides="An inference is a statement true in every interpretation that satisfies the ontology; a reasoner finds them; adding axioms never removes one; and 'not said' is not 'false'.",
    corner="referent",
    why="Every settlement is a place. Wigtown is a settlement. So Wigtown "
        "is a place. Nobody wrote the third sentence and it is true anyway, "
        "because there is no way for the first two to hold and the third "
        "to fail. That is entailment, and it is the whole of what a "
        "reasoner does: find the statements that hold in every "
        "interpretation the axioms allow. The set reading makes it plain. "
        "S is inside P; w is in S; so w is in P. There is nothing to "
        "decide.\n\n"
        "Three things can follow. A new triple, which a materialising "
        "reasoner writes into the graph, as the editor's Show Facts does. "
        "A classification, that one class is inside another though nobody "
        "said so. And a contradiction, that no interpretation exists at "
        "all. RDFS can give the first; OWL 2 gives all three.\n\n"
        "Two properties of the logic decide how it feels to use. It is "
        "monotonic: adding an axiom can add conclusions and never remove "
        "one, so a conclusion drawn today stays drawn. Monotonicity is what makes materialisation safe, and it is why a SHACL rule with a negation "
        "in it, which the SHACL course's s52 shows going stale, is a "
        "different kind of thing. And it is open-world: a statement not "
        "in the graph is not false, it is unknown, so absence entails "
        "nothing. The reasoner will never tell you that a shop has no "
        "website. A query will, and the difference is the subject of the "
        "next lesson.",
    diagram="""
   axioms                                     what follows

   bs:Settlement rdfs:subClassOf bs:Place     w in S, S inside P  =>  w in P
   bt:place-wigtown a bs:Settlement            a new triple:      bt:place-wigtown a bs:Place

   three kinds of consequence:  a triple  |  a classification  |  a contradiction
   monotonic:  more axioms, never fewer conclusions
   open world: not said is not false; absence entails nothing
""",
    learn=[
        "Entailment is what holds in every interpretation the axioms allow. A reasoner finds it; a query finds what is written.",
        "Monotonic: nothing you add takes a conclusion away. That is why materialising is safe and why rules with negation are not the same thing.",
        "Open world: the reasoner never concludes from absence. For 'has no website', ask a query.",
    ],
    body=DECL + """
bs:Place       a owl:Class ; skos:prefLabel "Place"@en .
bs:Settlement  a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Settlement"@en .
bs:Bookshop    a owl:Class .
bs:website     a owl:DatatypeProperty .

bt:place-wigtown  a bs:Settlement .
bt:shop-marginalia a bs:Bookshop .     # no website recorded: the reasoner concludes nothing
""",
    queries=[Query("What the reasoner cannot say: shops with no website", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?shop WHERE { ?shop a bs:Bookshop . FILTER NOT EXISTS { ?shop bs:website ?w } }""", rows=1)],
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True, inferred=["bt:place-wigtown rdf:type bs:Place"], rl_inferred=["bt:place-wigtown rdf:type bs:Place"]),
)
specs.register("o51", "directSemantics", "primerOpenWorld")

WITHIN_RULE = """
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix bs:  <https://example.org/bookshop-trail/schema#> .
@prefix bt:  <https://example.org/bookshop-trail/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# The transitive closure of bs:within as a SHACL rule, after the SHACL
# course's s51. One pass adds one hop; iterated to a fixpoint, it adds
# them all. Set the editor's Inference dropdown to 'rules, iterated'.
bt:prefixes  a owl:Ontology ;
    sh:declare [ sh:prefix "bs" ; sh:namespace "https://example.org/bookshop-trail/schema#"^^xsd:anyURI ] .

bt:WithinClosureShape
    a               sh:NodeShape ;
    sh:targetClass  bs:Place ;
    sh:rule [
        a           sh:SPARQLRule ;
        sh:prefixes bt:prefixes ;
        sh:construct \"\"\"
            CONSTRUCT { $this bs:within ?z }
            WHERE     { $this bs:within ?y . ?y bs:within ?z }
        \"\"\" ;
    ] .
"""

o(
    oid="o52", module=M,
    title="Three routes to one inference",
    decides="The transitive closure of bs:within, sixty-three pairs becoming a hundred and eighty-six, is reached by an OWL reasoner, by a SPARQL property path, and by a SHACL rule iterated to a fixpoint; each is measured, and the choice between them is a matter of when and where the work is done.",
    corner="referent",
    why="Wigtown is within Dumfries and Galloway, which is within "
        "Scotland, which is within Great Britain. The data says the first "
        "three links; question 1 in the brief wants the fourth. There are "
        "three ways to get it, and they give the same answer.\n\n"
        "An OWL reasoner, given bs:within a owl:TransitiveProperty, writes the missing pairs into the graph. The editor's Show Facts does it in the browser; the RL closure this lesson was measured with adds the 123 missing pairs among the Trail's own places, and HermiT agrees. Both add more than that, because the place file links each town to its DBpedia page with owl:sameAs and a reasoner copies every pair onto the alias; the queries count the Trail's own IRIs, and o04 said why sameAs does this. The "
        "work is done once, up front, and the result is stored; it goes "
        "stale when a place moves, and a reasoner has to run again.\n\n"
        "A SPARQL property path, bs:within+, computes the closure at query "
        "time. Nothing is stored, nothing goes stale, and it runs on any "
        "SPARQL 1.1 engine with no reasoner at all. The SPARQL course's "
        "module 05 is built on it. The cost is paid on every query, which "
        "for a few hundred places is nothing and for a few million is a "
        "design decision.\n\n"
        "A SHACL rule, a CONSTRUCT that adds one hop, iterated until "
        "nothing new appears, materialises the same closure, and the "
        "editor's Inference dropdown runs it. The SHACL course's s51 is "
        "that rule; the SemOps Manual's chapter 11 calls this the third "
        "way to derive a triple and says when it is the right one: when "
        "the rule is a governed artefact that someone owns, and when the "
        "closure must be visible to a validator that has no reasoner. This "
        "lesson's companion file is the rule, and pySHACL iterating it "
        "adds exactly the 123 triples the reasoner did.\n\n"
        "Same 186 pairs, three engines, three times to pay. The SPARQL "
        "course's lab set the reasoner and the path side by side; the "
        "table in the diagram adds the rule.",
    diagram="""
                     OWL reasoner              SPARQL path             SHACL rule (iterated)
   what you write    owl:TransitiveProperty    bs:within+              CONSTRUCT one hop; iterate
   when it runs      once, before queries      every query             once, before validation
   what is stored    186 triples               nothing                 186 triples
   goes stale?       yes; re-run               never                   yes; re-run
   needs             a reasoner (Show Facts)   any SPARQL 1.1 engine   a SHACL-AF engine (Inference: rules, iterated)
   explains itself?  a DL reasoner can (o56)   the path is the reason  the rule is the reason

   measured on data/03-places.ttl:  63 asserted  ->  186  by all three routes
""",
    learn=[
        "Materialise (reasoner or rule) when many queries will read the closure and the data is slow to change. Query (a path) when it is not.",
        "A path needs no reasoner and never goes stale. It is the portable route and the one to reach for first.",
        "A rule is a governed artefact: someone owns it, a validator can see its output, and it is the route when the consumer has no reasoner.",
    ],
    body=DECL + """
bs:Place   a owl:Class ; skos:prefLabel "Place"@en .
bs:within  a owl:ObjectProperty, owl:TransitiveProperty ;
    rdfs:domain bs:Place ; rdfs:range bs:Place ;
    skos:definition "Directly inside another place. Transitive, so a reasoner closes the chain; bs:within+ does the same at query time."@en .
""",
    data=DPLACES,
    companions={"within-rule.ttl": WITHIN_RULE},
    shapes="within-rule.ttl",
    queries=[
        Query("Route 2, the path: every Trail place and everything it is within", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?a ?b WHERE { ?a bs:within+ ?b . FILTER(STRSTARTS(STR(?a), "https://example.org/bookshop-trail/") && STRSTARTS(STR(?b), "https://example.org/bookshop-trail/")) }""", on="data", rows=186),
        Query("Route 1, the reasoner: the same pairs, asserted after the closure", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?a ?b WHERE { ?a bs:within ?b . FILTER(STRSTARTS(STR(?a), "https://example.org/bookshop-trail/") && STRSTARTS(STR(?b), "https://example.org/bookshop-trail/")) }""", on="reasoned", rows=186),
        Query("Question 1: which settlements are in Scotland, by the path", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?place WHERE { ?place a bs:Settlement ; bs:within+ bt:place-scotland } ORDER BY ?place""", on="data"),
    ],
    check=dict(profile=True, with_data=DPLACES, reason=True, rl=True, rules=WITHIN_RULE),
    expect=dict(dl=True, consistent=True, rl_min_added=123, rules_added=123,
                rl_inferred=["bt:place-wigtown bs:within bt:place-scotland"],
                inferred=["bt:place-wigtown bs:within bt:place-scotland"]),
    notes="Open in the editor opens this file with the rule in a second tab; to see the closure on the whole place hierarchy, load "
          "data/03-places.ttl instead, set Inference to 'rules, iterated', and validate; or press Show Facts for the reasoner's route. "
          "The AFTERWARDS queries run on the place file.",
)
specs.register("o52", "semopsRules", "sparqlCourseInference")

o(
    oid="o53", module=M,
    title="Inconsistency: the three usual causes",
    decides="A contradiction is traced to one of three habits: a thing typed with two disjoint kinds, a functional property with two values declared different, or a value that its datatype cannot hold; each is seeded, and the reasoner names the axioms responsible.",
    corner="referent",
    why="An ontology is inconsistent when no interpretation satisfies it. "
        "It is one verdict for the whole graph, and the first thing to "
        "know is that it is rarely subtle. Almost every inconsistency in "
        "practice has one of three shapes. A thing typed with two classes "
        "declared disjoint, usually a data load with the wrong kind (o43). "
        "A functional property with two values that are declared, or can "
        "be proved, different: two towns for one shop with "
        "owl:differentFrom between them, or two integers, since literals "
        "are different when they differ (o47). Or a value a datatype "
        "cannot hold, 'four' as an xsd:integer, which the reasoner treats "
        "as no value at all and the axiom that requires one then fails.\n\n"
        "This file seeds all three, so that HermiT's verdict is "
        "unmistakable, and the reasoner can be asked to explain. ROBOT's "
        "explain command in inconsistency mode returns the smallest sets "
        "of axioms that produce the contradiction, one per cause, and the "
        "measured line carries the first of them. That is the tool to "
        "reach for when a large ontology turns inconsistent after a "
        "change: not reading the ontology, but asking which few axioms are "
        "to blame.\n\n"
        "The editor's RL closure will show the sameAs and the types and "
        "say nothing about a contradiction. For the browser, each cause "
        "is a query, and the three queries here find the three seeds.",
    diagram="""
   cause                                   seed                                               query
   two disjoint kinds                      bt:oddity a bs:Place, bs:Bookshop                  ?x a ?a, ?b . ?a owl:disjointWith ?b
   functional, two values, different       bt:shop-x locatedIn wigtown, hay ; wigtown differentFrom hay
                                                                                              ?x ?p ?a, ?b . ?p a owl:FunctionalProperty . ?a owl:differentFrom ?b
   a value outside its datatype            bt:shop-y bs:staffCount -3 ; range: integer >= 0   FILTER(?v < 0) on the restricted property

   HermiT: inconsistent.  robot explain --mode inconsistency: the axioms responsible, one set per cause
""",
    learn=[
        "Inconsistency is one verdict for the whole graph, and it almost always has one of three shapes.",
        "Ask the reasoner to explain. The smallest set of axioms behind a contradiction is a few lines, however large the ontology.",
        "The browser cannot report a contradiction, but each cause is a query, and the queries belong in the gate.",
    ],
    body=DECL + """
bs:Place a owl:Class . bs:Bookshop a owl:Class . bs:Settlement a owl:Class .
bs:Place  owl:disjointWith  bs:Bookshop .
bs:locatedIn   a owl:ObjectProperty, owl:FunctionalProperty ; rdfs:range bs:Settlement .
bs:staffCount  a owl:DatatypeProperty ;
    rdfs:range [ a rdfs:Datatype ; owl:onDatatype xsd:integer ; owl:withRestrictions ( [ xsd:minInclusive 0 ] ) ] .

# 1. two disjoint kinds
bt:oddity  a bs:Place, bs:Bookshop .

# 2. functional, two values, declared different
bt:shop-x         a bs:Bookshop ; bs:locatedIn bt:place-wigtown, bt:place-hay .
bt:place-wigtown  a bs:Settlement ; owl:differentFrom bt:place-hay .
bt:place-hay      a bs:Settlement .
# The plural form, for a whole list of things that are pairwise distinct:
[] a owl:AllDifferent ; owl:members ( bt:place-wigtown bt:place-hay bt:place-sedbergh ) .
bt:place-sedbergh a bs:Settlement .

# 3. a value outside its datatype
bt:shop-y  a bs:Bookshop ; bs:staffCount -3 .
""",
    queries=[
        Query("Cause 1: a thing with two disjoint types", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?x WHERE { ?a owl:disjointWith ?b . ?x a ?a, ?b }""", rows=1),
        Query("Cause 2: a functional property with two values known to differ", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?x ?p WHERE { ?p a owl:FunctionalProperty . ?x ?p ?a, ?b . ?a owl:differentFrom ?b }""", rows=1),
        Query("Cause 3: a staff count below zero", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?x ?v WHERE { ?x bs:staffCount ?v . FILTER(?v < 0) }""", rows=1),
    ],
    check=dict(profile=True, reason=True, explain="inconsistency"),
    expect=dict(dl=True, consistent=False),
    local="HermiT's verdict and the explanation come from ROBOT",
)
specs.register("o53", "directSemantics", "primerDisjoint")

o(
    oid="o54", module=M,
    title="Unsatisfiable classes: consistent, and dead",
    decides="A class that can have no instances is found by the reasoner before any data arrives; the ontology stays consistent, and the class is fixed rather than shipped.",
    corner="referent",
    why="An unsatisfiable class is one whose extension is empty in every "
        "interpretation: no possible thing could be a member. The ontology "
        "is consistent, since nothing has been asserted to be in the "
        "class, and that is what makes the fault a quiet one. It sits there "
        "until the first individual is typed with it, and then the whole "
        "graph is inconsistent and the cause is a class defined months "
        "ago.\n\n"
        "The usual shapes: a class under two disjoint parents, like the "
        "Translation that o34 seeded disjoint from Work; a class whose "
        "restrictions contradict, located in some Settlement and located "
        "in only Publishers; a class defined as the intersection of two "
        "disjoint classes. All are found by classification with no data "
        "at all, and ROBOT's reason command lists them and refuses to "
        "write the reasoned file until they are fixed, which is the right "
        "default for a gate. The Quality Suite reports the same as "
        "REA-021, and LOG-001 catches the disjoint-parent case without a "
        "reasoner.\n\n"
        "The set reading: an unsatisfiable class is a subset of the empty "
        "set. owl:Nothing is the empty set's name, and 'equivalent to "
        "owl:Nothing' is what a reasoner says when it finds one.",
    diagram="""
   bs:Work owl:disjointWith bs:Person
   bs:Memoir rdfs:subClassOf bs:Work, bs:Person          M inside W and inside P, and W and P share nothing
                                                          => M is empty in every interpretation
                                                          => M is equivalent to owl:Nothing

   consistent (nobody is a Memoir yet); unsatisfiable (nobody ever can be)
   the first bt:book-x a bs:Memoir makes the whole graph inconsistent
""",
    learn=[
        "An unsatisfiable class is a fault with no data in it yet. Classify before you load, and fix what the reasoner names.",
        "The gate should refuse an ontology with one. ROBOT does by default; the Quality Suite reports REA-021.",
        "Under two disjoint parents, or two restrictions that contradict: those are the shapes to look for when a class comes back empty.",
    ],
    body=DECL + """
bs:Work a owl:Class . bs:Person a owl:Class . bs:Settlement a owl:Class . bs:Publisher a owl:Class .
bs:Work  owl:disjointWith  bs:Person .
bs:locatedIn  a owl:ObjectProperty .

# Under two disjoint parents.
bs:Memoir  a owl:Class ; rdfs:subClassOf bs:Work, bs:Person ;
    skos:editorialNote "A memoir is a work about a person; someone made it both. Unsatisfiable."@en .

# The trivial case: a class declared empty outright.
bs:Ghost  a owl:Class ; rdfs:subClassOf owl:Nothing .

# Restrictions that contradict.
bs:Settlement  owl:disjointWith  bs:Publisher .
bs:OddShop  a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ; owl:onProperty bs:locatedIn ; owl:someValuesFrom bs:Settlement ] ,
                    [ a owl:Restriction ; owl:onProperty bs:locatedIn ; owl:allValuesFrom  bs:Publisher ] .
""",
    check=dict(profile=True, reason=True, oqs="ontology"),
    expect=dict(dl=True, unsat=["Memoir", "OddShop", "Ghost"], oqs=["REA-021"], oqs_not=["LOG-001"]),
    local="the unsatisfiable classes on the MEASURED line come from HermiT through ROBOT, and REA-021 from the Quality Suite",
)
specs.register("o54", "directSemantics", "semopsTestGate")

o(
    oid="o55", module=M,
    title="Classification: the hierarchy the reasoner infers",
    decides="Subclass relations that follow from definitions are left for the reasoner to infer rather than asserted, and the inferred hierarchy is compared with the asserted one as a check on both.",
    corner="referent",
    why="Classification is the reasoner working out the subclass "
        "relations between every pair of classes, asserted or not. Define "
        "Author as Person and wrote some Work, and Author is under Person "
        "without anyone writing rdfs:subClassOf. Define LocalPublisher as "
        "Publisher and locatedIn some Settlement, and PublisherInWigtown as "
        "Publisher and locatedIn value Wigtown, and the reasoner places "
        "the second under the first, because a value is a special case of "
        "some. Nobody said so. It follows.\n\n"
        "That is the reason to define rather than declare wherever a "
        "definition is possible. An asserted hierarchy records what "
        "somebody believed; an inferred one records what the definitions "
        "entail, and the two can be compared. Where they differ, one of "
        "them is wrong, and it is usually the assertion. gist's habit of "
        "defining classes by equivalence to an intersection (o32) is this "
        "habit at scale.\n\n"
        "ROBOT's reason command writes the inferred axioms into the "
        "ontology; the measured line counts them. The editor's RL closure "
        "does not classify, since deriving a subclass axiom from "
        "restrictions is outside RL; it types individuals, which is the "
        "other half of the same work, and o56 sets the two side by side.",
    diagram="""
   asserted                                              inferred (HermiT)

   bs:Author = Person and (wrote some Work)              bs:Author rdfs:subClassOf bs:Person
   bs:LocalPublisher = Publisher and (locatedIn some Settlement)
   bs:WigtownPublisher = Publisher and (locatedIn value bt:place-wigtown)
                                                          bs:WigtownPublisher rdfs:subClassOf bs:LocalPublisher
   (bt:place-wigtown a bs:Settlement)                     because 'value w' is a case of 'some S' when w is in S

   define where you can; assert where you must; compare the two
""",
    learn=[
        "Classification infers the subclass relations the definitions entail. Define rather than assert, and let it.",
        "Compare the inferred hierarchy with the asserted one. A difference means a belief and a definition disagree.",
        "The RL closure types individuals; it does not classify classes. That is the line between the editor's reasoner and a DL one.",
    ],
    body=DECL + """
bs:Person a owl:Class . bs:Work a owl:Class . bs:Publisher a owl:Class . bs:Settlement a owl:Class .
bs:wrote     a owl:ObjectProperty .
bs:locatedIn a owl:ObjectProperty .

bs:Author  a owl:Class ;
    owl:equivalentClass [ owl:intersectionOf ( bs:Person [ a owl:Restriction ; owl:onProperty bs:wrote ; owl:someValuesFrom bs:Work ] ) ] .

bs:LocalPublisher  a owl:Class ;
    owl:equivalentClass [ owl:intersectionOf ( bs:Publisher [ a owl:Restriction ; owl:onProperty bs:locatedIn ; owl:someValuesFrom bs:Settlement ] ) ] .

bs:WigtownPublisher  a owl:Class ;
    owl:equivalentClass [ owl:intersectionOf ( bs:Publisher [ a owl:Restriction ; owl:onProperty bs:locatedIn ; owl:hasValue bt:place-wigtown ] ) ] .

bt:place-wigtown  a bs:Settlement .
""",
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True,
                inferred=["bs:Author rdfs:subClassOf bs:Person", "bs:WigtownPublisher rdfs:subClassOf bs:LocalPublisher"],
                rl_not_inferred=["bs:WigtownPublisher rdfs:subClassOf bs:LocalPublisher"]),
    local="the inferred hierarchy comes from HermiT through ROBOT; Show Facts will not derive it",
)
specs.register("o55", "primerComplex", "profilesRL")

o(
    oid="o56", module=M,
    title="Two reasoners: the rule engine and the description logic",
    decides="The editor's OWL 2 RL closure is used for what it does well, typing individuals and closing properties, and a description-logic reasoner for what only it does, which is to classify, to find the dead classes, and to explain.",
    corner="referent",
    why="Two kinds of reasoner, and it pays to know which you are "
        "holding. An OWL 2 RL engine, the editor's HyLAR and the owlrl "
        "closure this course measures with, applies rules to triples until "
        "nothing new appears: subclass typing, domain and range, "
        "transitive and symmetric closure, inverses, chains, sameAs from "
        "functional properties, allValuesFrom typing, and membership of "
        "defined classes when the fillers are named. It is fast, it "
        "scales, it runs in a browser, and it never says no.\n\n"
        "A description-logic reasoner, HermiT here, decides entailment by "
        "searching for a model. It classifies classes, finds unsatisfiable "
        "ones, reports inconsistency, and explains: it can say which few "
        "axioms make an inference true. It handles existentials in "
        "superclass position and everything else DL allows. It is slower, "
        "it does not stream, and it needs the whole ontology in memory.\n\n"
        "This file shows the line between them on two examples. "
        "Translation is a Work that is a translation of some Work; "
        "EnglishTranslation is a Work that is a translation of some "
        "EnglishWork, and EnglishWork is a kind of Work. Both engines type "
        "bt:book-x as a Translation, since its fillers are named, and both "
        "derive that Translation is under Work, since RL has a rule that an "
        "intersection lies inside each of its parts. Only HermiT derives "
        "that EnglishTranslation is under Translation, because that needs "
        "the two definitions compared as wholes, and RL has no rule for "
        "that. The measured line has both results. Use the RL engine for "
        "the data and the DL engine for the ontology, and run the DL "
        "engine in the gate, where somebody will read what it says.",
    diagram="""
                            OWL 2 RL (editor, owlrl)      DL (HermiT)
   types individuals        yes                            yes
   closes properties        yes                            yes
   sameAs from functional   yes                            yes
   classifies classes       no                             yes
   finds unsatisfiable      no                             yes
   reports inconsistency    no (materialises past it)      yes
   explains                 no                             yes (robot explain)
   runs in the browser      yes                            no
   cost                     linear-ish, streams            exponential worst case, whole ontology

   measured here:  bt:book-x a bs:Translation                        both
                   bs:Translation subClassOf bs:Work                 both (RL: an intersection is inside each part)
                   bs:EnglishTranslation subClassOf bs:Translation   HermiT only
""",
    learn=[
        "RL: rules over triples; fast, browser-sized, never says no. DL: models; classifies, finds the dead classes, explains.",
        "RL has schema rules too, and derives more of the hierarchy than people expect. What it cannot do is compare two definitions as wholes.",
        "Use RL for the data and DL for the ontology. Run DL in the gate.",
        "When a book says 'the reasoner infers', ask which kind. The answer changes what you can rely on.",
    ],
    body=DECL + """
bs:Work  a owl:Class .
bs:translationOf  a owl:ObjectProperty .

bs:Translation  a owl:Class ;
    owl:equivalentClass [ owl:intersectionOf ( bs:Work [ a owl:Restriction ; owl:onProperty bs:translationOf ; owl:someValuesFrom bs:Work ] ) ] .

bs:EnglishWork  a owl:Class ; rdfs:subClassOf bs:Work .
bs:EnglishTranslation  a owl:Class ;
    owl:equivalentClass [ owl:intersectionOf ( bs:Work [ a owl:Restriction ; owl:onProperty bs:translationOf ; owl:someValuesFrom bs:EnglishWork ] ) ] .

bt:book-x  a bs:Work ; bs:translationOf bt:book-w .
bt:book-w  a bs:Work .
""",
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True,
                inferred=["bt:book-x rdf:type bs:Translation", "bs:Translation rdfs:subClassOf bs:Work",
                          "bs:EnglishTranslation rdfs:subClassOf bs:Translation"],
                rl_inferred=["bt:book-x rdf:type bs:Translation", "bs:Translation rdfs:subClassOf bs:Work"],
                rl_not_inferred=["bs:EnglishTranslation rdfs:subClassOf bs:Translation"]),
)
specs.register("o56", "profilesRL", "primerDlFull")

o(
    oid="o57", module=M,
    title="Reasoning over the whole Trail",
    decides="The shipped vocabulary and the whole dataset go through a description-logic reasoner together: consistent, one hundred and eighty-six within pairs, the reversed segments and inverses materialised, and not one new type, because the data types everything already.",
    corner="referent",
    why="Everything in this module has been done on a few triples. The "
        "shipped vocabulary with the whole dataset is four thousand eight "
        "hundred, and HermiT classifies and realises it in about two "
        "seconds, which is the number to have in hand before anyone says a DL reasoner is too slow for real data. The OWL 2 DL copy of the dataset is used, so that the profile verdict and the reasoning are about one file; run on the copy with the xsd:gYear values, HermiT reports consistent as well, treating the unknown datatype as opaque.\n\n"
        "What it adds is exactly what the axioms promise and nothing "
        "else. bs:within is transitive, so sixty-three pairs become a "
        "hundred and eighty-six. bs:connectsTo is symmetric, so "
        "thirty-three segments gain their reverse. bs:hasImprint is the "
        "inverse of bs:imprintOf and asserted nowhere, so nine appear. "
        "bs:wrote is the inverse of bs:author, so six appear where the "
        "data used author. And not one new rdf:type on a Trail term, "
        "because the data types every individual already and the "
        "vocabulary defines no class by equivalence. The SPARQL course's "
        "module 18 measured the same and drew the same conclusion: the "
        "closure is real, and a property path gets most of it without a "
        "reasoner.\n\n"
        "Consistent, too, which is the quiet confirmation that a "
        "vocabulary written with the habits of module 05, sparse domains, "
        "no functional property where sources disagree, disjointness only "
        "at the top, does not fight its own data. Change one of those "
        "habits, as o29 did, and the same run says inconsistent.",
    diagram="""
   data/bookshop-trail-owl-dl.ttl: 4,796 triples, through HermiT, about two seconds

   inferred                         count   from
   bs:within                        +123    owl:TransitiveProperty      63 -> 186
   bs:connectsTo                    +33     owl:SymmetricProperty
   bs:hasImprint                    +9      owl:inverseOf bs:imprintOf  (asserted nowhere in the data)
   bs:wrote                         +6      owl:inverseOf bs:author
   rdf:type on a Trail class        0       everything is typed already

   verdict: consistent
""",
    learn=[
        "A DL reasoner on a few thousand triples takes seconds. Measure before assuming it will not scale.",
        "What it adds is what the axioms promise: closures and inverses. Where the data is already typed, no types.",
        "Consistency on the whole dataset is the cheapest end-to-end test an ontology has. Run it in the gate.",
    ],
    body=DECL + """
# This lesson's own model is the ontology header; the checker merges the
# whole OWL 2 DL copy of the dataset before reasoning.
<https://example.org/bookshop-trail/schema>
    a               owl:Ontology ;
    skos:prefLabel  "The Bookshop Trail schema"@en .
""",
    data="bookshop-trail-owl-dl.ttl",
    queries=[Query("Places within Scotland, after the closure", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT (COUNT(*) AS ?n) WHERE { ?p bs:within bt:place-scotland }""", on="reasoned", rows=1)],
    check=dict(with_data="bookshop-trail-owl-dl.ttl", reason=True, rl=True),
    expect=dict(consistent=True, rl_min_added=170,
                inferred=["bt:place-wigtown bs:within bt:place-scotland", "bt:pub-lodestone-group bs:hasImprint bt:pub-northwind"],
                rl_inferred=["bt:place-wigtown bs:within bt:place-scotland"]),
    local="the reasoning over the whole dataset is HermiT through ROBOT; in the browser, load the file and press Show Facts for the RL closure",
)
specs.register("o57", "sparqlCourseInference", "primerDlFull")
