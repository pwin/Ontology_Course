# -*- coding: utf-8 -*-
"""Module 07 -- The ladder: OWL 2. One construct per lesson, and what it commits you to."""
from ontocat import o, Query
import specs

M = "07-owl"

DECL = """
skos:prefLabel      a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
"""

o(
    oid="o42", module=M,
    title="owl:Class, owl:Ontology, and the rule that everything is declared",
    decides="The vocabulary becomes an OWL 2 DL ontology: an owl:Ontology node, every class an owl:Class, every property exactly one of object, datatype or annotation, every borrowed term declared, and the profile checker as referee.",
    corner="referent",
    why="The step from RDFS to OWL 2 DL is mostly a matter of declarations. "
        "rdfs:Class becomes owl:Class, and rdf:Property becomes one of "
        "owl:ObjectProperty, owl:DatatypeProperty or "
        "owl:AnnotationProperty, and exactly one of them, because a DL "
        "reasoner needs to know whether a property's values are things, "
        "values or commentary before it can reason at all. Every term the "
        "file mentions is declared, including the borrowed ones, since the "
        "profile is checked over the imports closure and the Trail imports "
        "nothing; and an owl:Ontology node says what the document is.\n\n"
        "The reward for that discipline is that a checker can now tell you "
        "whether the file is OWL 2 DL, and this one is. The SPARQL course's "
        "README records what it took to get the shipped vocabulary there, "
        "and the rules that bit were all of them rules RDFS never mentions: "
        "everything must be declared; a property is of one kind only; a "
        "transitive property is non-simple and may not be functional; and "
        "an RDF 1.2 triple term has no OWL type at all, so the property "
        "that points at one has to be an annotation property. Each of those "
        "is a lesson in this module.\n\n"
        "The set reading from o35 now has teeth, since an owl:Class is a "
        "set the reasoner will draw conclusions about, where a class that "
        "was rdfs:Class in module 06 was a set nobody could contradict. The "
        "profiles table in the measured line shows where this small file "
        "sits, which is in DL, and in EL, QL and RL besides, because it "
        "says so little.",
    diagram="""
   RDFS                                OWL 2 DL

   bs:Bookshop a rdfs:Class            bs:Bookshop a owl:Class
   bs:locatedIn a rdf:Property         bs:locatedIn a owl:ObjectProperty      (values are things)
   bs:founded a rdf:Property           bs:founded a owl:DatatypeProperty      (values are values)
   rdfs:comment (used, undeclared)     rdfs:comment is built in; skos:definition a owl:AnnotationProperty
   (no header)                         <.../schema> a owl:Ontology

   the referee:  robot validate-profile --profile DL      in profile / NOT in profile, with the reason
""",
    learn=[
        "OWL 2 DL is RDFS plus declarations, and it is the declarations that let a reasoner and a checker do their work.",
        "A property is object, datatype or annotation, and only one of them; decide by asking whether its values are things, values or commentary.",
        "Declare whatever you borrow, since the profile is checked over what is imported and here nothing is.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a               owl:Ontology ;
    skos:prefLabel  "The Bookshop Trail schema"@en .

bs:Place       a owl:Class ; skos:prefLabel "Place"@en .
bs:Settlement  a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Settlement"@en .
bs:Bookshop    a owl:Class ; skos:prefLabel "Bookshop"@en .

bs:locatedIn   a owl:ObjectProperty ;   rdfs:range bs:Settlement ; skos:prefLabel "located in"@en .
bs:founded     a owl:DatatypeProperty ; rdfs:range xsd:integer ;   skos:prefLabel "founded"@en .
bs:website     a owl:DatatypeProperty ; rdfs:range xsd:anyURI ;    skos:prefLabel "website"@en .
skos:Concept   a owl:Class .

bt:shop-inkwell  a bs:Bookshop ; bs:locatedIn bt:place-wigtown ; bs:founded 1979 .
bt:place-wigtown a bs:Settlement .
""",
    check=dict(profiles=True, reason=True),
    expect=dict(dl=True, el=True, ql=True, rl=True, consistent=True),
    tryit="Delete the line declaring bs:locatedIn and run python scripts/check_lessons.py o42: the file falls out of DL, and the "
          "checker says why: 'use of undeclared annotation property bs:locatedIn'. With no declaration, the OWL API reads the "
          "assertion as an annotation, and DL requires annotation properties to be declared too. Deleting bs:website's line "
          "changes nothing, because nothing uses it. Put the line back. The editor will not object either way; only the referee does.",
    local="the OWL 2 profile verdicts on the MEASURED line come from ROBOT",
)
specs.register("o42", "syntaxDeclarations", "syntaxTyping")

o(
    oid="o43", module=M,
    title="Disjointness: now you can be wrong",
    decides="The top-level kinds are declared pairwise disjoint, so that one thing typed as two of them is a contradiction a reasoner reports, and a query finds in the browser.",
    corner="referent",
    why="Disjointness comes first among the OWL constructs because it is "
        "the first thing that can be contradicted. Place and Bookshop "
        "declared disjoint says that the two sets share no member, so that "
        "if you type one thing with both there is no interpretation in "
        "which the axioms hold, the ontology is inconsistent, and HermiT "
        "says so. This is the thing RDFS could not do in o41, and it is "
        "cheap, since one owl:AllDisjointClasses over the backbone catches "
        "the commonest data-loading error there is, which is a row typed as "
        "the wrong kind.\n\n"
        "The editor's reasoner is an OWL 2 RL engine and materialises "
        "rather than judges, so it will not put up a sign saying "
        "inconsistent. The same contradiction is a query, though, and the "
        "query runs perfectly well in the browser: find anything typed with "
        "two classes that are declared disjoint. That query is the SHACL "
        "course's s25, sh:not, seen from the other side, and it is the one "
        "to keep in the gate.\n\n"
        "Below the backbone, disjointness gets harder to justify, because "
        "Author and TrailMember are roles and a shop can be a member as "
        "well as a shop, just as a person can be an author and a translator "
        "at once. gist declares disjointness extensively at the highest "
        "level and sparingly below it, and that is the shape to copy.",
    diagram="""
   bs:Place  owl:disjointWith  bs:Bookshop        the sets share no member

   bt:oddity a bs:Place, bs:Bookshop              no interpretation satisfies this
                                                  HermiT: the ontology is inconsistent

   in the browser, the same fact as a query:
   SELECT ?x WHERE { ?a owl:disjointWith ?b . ?x a ?a, ?b }     -> bt:oddity
""",
    learn=[
        "Disjointness is the cheapest axiom there is and the first that can be contradicted, so declare it across the backbone.",
        "A DL reasoner reports the contradiction where an RL reasoner materialises straight past it, so keep the query that finds it.",
        "Disjointness below the backbone is where the roles start to overlap, so declare it there only with a reason.",
    ],
    body=DECL + """
bs:Place a owl:Class . bs:Bookshop a owl:Class . bs:Person a owl:Class . bs:Work a owl:Class .
[] a owl:AllDisjointClasses ; owl:members ( bs:Place bs:Bookshop bs:Person bs:Work ) .

# For the query, which reads pairwise disjointness: the same fact stated
# pairwise for the two classes the oddity breaks.
bs:Place  owl:disjointWith  bs:Bookshop .

bt:oddity  a bs:Place, bs:Bookshop ; skos:prefLabel "A row loaded with the wrong kind"@en .
""",
    queries=[Query("Anything typed with two disjoint classes", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?x ?a ?b WHERE { ?a owl:disjointWith ?b . ?x a ?a, ?b }""", rows=1)],
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=False),
)
specs.register("o43", "primerDisjoint", "shaclCourseInference")

o(
    oid="o44", module=M,
    title="Existential restrictions: a necessary condition, and the open world",
    decides="'Every bookshop is located in some settlement' is written as a subclass axiom with owl:someValuesFrom, which constrains the set without producing a triple, and a shop with no recorded town is not an error.",
    corner="referent",
    why="A restriction is a set defined by a condition, in this case the "
        "things that have some bs:locatedIn value in bs:Settlement, and "
        "writing bs:Bookshop rdfs:subClassOf that set says every bookshop "
        "is such a thing. It is a necessary condition, that to be a "
        "bookshop you must be located in a settlement, and it is not a "
        "sufficient one, since other things are located in settlements too; "
        "nor is it a defined class, which o46 is.\n\n"
        "What does the reasoner do with it? Rather less than newcomers "
        "expect. Given a bookshop with no recorded town it does not "
        "complain, because the open world says the town exists and is "
        "simply not in the file; given a bookshop located in something it "
        "does not type that something as a Settlement, because the axiom "
        "says that some value is a settlement rather than that every value "
        "is. HermiT reports the file consistent and infers nothing visible, "
        "and that is correct: the axiom has narrowed the set of "
        "interpretations, which is what an axiom does, and nothing in the "
        "data happened to be decided by it.\n\n"
        "Which is why gist's rules say to use someValuesFrom in an "
        "equivalence when you want to infer into a class, and why the shape "
        "that says every shop must have a town in this dataset is SHACL "
        "rather than this. The SHACL course's s04 is that shape, and it "
        "reports the shop with no town; this axiom never will.",
    diagram="""
   bs:Bookshop rdfs:subClassOf [ owl:onProperty bs:locatedIn ; owl:someValuesFrom bs:Settlement ]

   set reading:  B is a subset of { x : some y, locatedIn(x, y), y in S }

   a shop with no town in the file      consistent: the town exists, unrecorded (open world)
   a shop located in something          the something is not typed: 'some', not 'every'
   HermiT: consistent, nothing new      correct, and the point

   want to find shops with no town?     a shape: sh:path bs:locatedIn ; sh:minCount 1   (SHACL course s04)
""",
    learn=[
        "A subclass existential is a necessary condition on the set, and it rejects nothing and types nothing, merely narrowing what the world could be.",
        "Absence is not error, because the open world says the missing value exists and is unrecorded.",
        "To find the missing value, write a shape; to infer membership from a value, use an equivalence, as o46 does.",
    ],
    body=DECL + """
bs:Settlement  a owl:Class .
bs:Bookshop    a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ; owl:onProperty bs:locatedIn ; owl:someValuesFrom bs:Settlement ] .
bs:locatedIn   a owl:ObjectProperty .

bt:shop-inkwell   a bs:Bookshop ; bs:locatedIn bt:place-wigtown .   # the town's type is not inferred
bt:shop-errata    a bs:Bookshop .                                   # no town recorded: not an error
bt:place-wigtown  skos:prefLabel "Wigtown"@en .
""",
    queries=[Query("Shops with no recorded town (what a shape would report)", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?shop WHERE { ?shop a bs:Bookshop . FILTER NOT EXISTS { ?shop bs:locatedIn ?town } }""", rows=1)],
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True, not_inferred=["bt:place-wigtown rdf:type bs:Settlement"],
                rl_not_inferred=["bt:place-wigtown rdf:type bs:Settlement"]),
)
specs.register("o44", "primerExistential", "primerOpenWorld")

o(
    oid="o45", module=M,
    title="Universal restrictions: types the values, and is true of nothing",
    decides="'A bookshop stocks only works' is written with owl:allValuesFrom, which types every value of bs:stocks on a bookshop as a Work and is trivially satisfied by a shop that stocks nothing.",
    corner="referent",
    why="The universal restriction picks out the set of things all of whose "
        "bs:stocks values are Works, and that includes the things which "
        "have no values at all. Put bs:Bookshop under it and the reasoner "
        "types every stocked thing as a Work, which makes this a local "
        "range, and both HermiT and the RL closure produce the triple; a "
        "shop that stocks nothing satisfies it vacuously, which tends to "
        "surprise anyone who reads 'only' as 'at least one, and only'.\n\n"
        "gist's fifth rule says what a subclass universal is good for, "
        "which is to add information about the class without inferring "
        "anything into it, and its first two rules say what an equivalence "
        "to a universal is good for, which is inferring into the "
        "complement: since nothing can be shown to have only Work values "
        "under the open world, no individual is ever classified into the "
        "class, while one with a non-Work value can be classified out of "
        "it. That is a subtle tool, and o47 uses its cousin.\n\n"
        "The everyday use is the range you cannot declare globally. "
        "bs:stocks on a bookshop points at works, while the same property "
        "on a library, if the vocabulary had one, might point at editions; "
        "a global rdfs:range would type both of them, where the local "
        "universal types only the bookshop's values.",
    diagram="""
   bs:Bookshop rdfs:subClassOf [ owl:onProperty bs:stocks ; owl:allValuesFrom bs:Work ]

   set reading:  B is a subset of { x : for every y, stocks(x, y) implies y in W }

   bt:shop-inkwell bs:stocks bt:thing     =>  bt:thing a bs:Work         (HermiT and the RL closure)
   bt:shop-errata stocks nothing          =>  satisfied, vacuously

   a local range: types the values of this property on this class only
""",
    learn=[
        "allValuesFrom types the values, which makes it a range scoped to one class.",
        "'Only' includes 'none', since a thing with no values at all satisfies every universal restriction going.",
        "Under the open world nothing can be proved to have only such values, so an equivalence to a universal never infers into the class, though it can infer out of it.",
    ],
    body=DECL + """
bs:Work      a owl:Class .
bs:Bookshop  a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ; owl:onProperty bs:stocks ; owl:allValuesFrom bs:Work ] .
bs:stocks    a owl:ObjectProperty .

bt:shop-inkwell  a bs:Bookshop ; bs:stocks bt:thing .
bt:thing         skos:prefLabel "Something the shop stocks; the axiom will say what"@en .
bt:shop-errata   a bs:Bookshop .
""",
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True, inferred=["bt:thing rdf:type bs:Work"], rl_inferred=["bt:thing rdf:type bs:Work"]),
    tryit="Show Facts: bt:thing is a bs:Work. Add a second value that is declared a bs:Person, with Person disjoint from Work, and the "
          "RL closure will type it a Work anyway; HermiT will call the file inconsistent. Same axiom, two engines, o43's lesson again.",
)
specs.register("o45", "primerUniversal", "gistRestrictions")

o(
    oid="o46", module=M,
    title="Defined classes: the reasoner decides membership",
    decides="Author is defined rather than declared: equivalent to a Person who wrote some Work, so that the reasoner types every such person an Author without being told, and the role from module 02 has its formal definition.",
    corner="referent",
    why="A subclass axiom gives a necessary condition, whereas an "
        "equivalence gives necessary and sufficient ones, so that Author is "
        "exactly the set of Persons with some bs:wrote value in Work and "
        "membership is now decided by the reasoner. Rhona Blackwood is a "
        "Person and wrote a Work, so she is an Author, and HermiT and the "
        "RL closure both say so from the data alone; this is the construct "
        "gist's sixth rule points at, that to infer instances into a class "
        "you define it with someValuesFrom, hasValue or a minimum "
        "cardinality.\n\n"
        "It is also the formalisation of o08, where Author was a role, "
        "anti-rigid and dependent on Work: the definition says the "
        "dependence exactly, and the anti-rigidity follows, since a person "
        "with no works is not classified and stops being classified when "
        "the works go. Rigidity is not in the axiom, but the axiom respects "
        "it.\n\n"
        "The habit that follows is to define the roles and phases with "
        "equivalences and leave the kinds as primitive classes, because a "
        "Person cannot be defined by any condition a reasoner could check "
        "where an Author can. gist's Task is an Event with hasGoal some "
        "Intention, its HistoricalEvent is an Event with actualEndDateTime "
        "some dateTime, and its Person is primitive; the reasoner "
        "classifies the defined ones and leaves the primitive ones to the "
        "data, which is just the division of labour a backbone taxonomy "
        "wants.\n\n"
        "Two further ways of defining a class are in the file for "
        "completeness. An enumeration, owl:oneOf, defines bs:Country as "
        "exactly Scotland, England and Wales, which is a closed set and the "
        "one place OWL lets you close the world, and it is right for a list "
        "that will not change. A complement, owl:complementOf, defines "
        "bs:NonFiction as a Work that is not Fiction, and under the open "
        "world no individual is ever proved into it, because nothing can be "
        "proved not to be fiction; gist's second rule says that a "
        "complement is for inferring out of a class rather than into one, "
        "and the measured line bears that out.",
    diagram="""
   bs:Author owl:equivalentClass [ owl:intersectionOf ( bs:Person
                                    [ owl:onProperty bs:wrote ; owl:someValuesFrom bs:Work ] ) ]

   set reading:  A = P intersect { x : some y, wrote(x, y), y in W }

   bt:author-rhona-blackwood a bs:Person ; bs:wrote bt:book-x .    bt:book-x a bs:Work .
     =>  bt:author-rhona-blackwood a bs:Author            (HermiT; and the RL closure)

   define roles and phases; leave kinds primitive
""",
    learn=[
        "An equivalence to an intersection with someValuesFrom lets the reasoner decide membership, where a subclass axiom gives a necessary condition only.",
        "Roles and phases are the things to define, since kinds are primitive and no condition a reasoner can check makes something a person.",
        "The definition of Author states the dependence from module 02 exactly, and respects the anti-rigidity without having to state it.",
    ],
    body=DECL + """
bs:Person  a owl:Class .
bs:Work    a owl:Class .
bs:wrote   a owl:ObjectProperty .

bs:Author
    a                    owl:Class ;
    skos:prefLabel       "Author"@en ;
    skos:definition      "A person who wrote at least one work."@en ;
    owl:equivalentClass  [ a owl:Class ;
                           owl:intersectionOf ( bs:Person
                                                [ a owl:Restriction ; owl:onProperty bs:wrote ; owl:someValuesFrom bs:Work ] ) ] .

bt:author-rhona-blackwood  a bs:Person ; bs:wrote bt:book-the-loom .
bt:book-the-loom           a bs:Work .
bt:person-reader           a bs:Person .    # wrote nothing recorded: not classified

# An enumeration: a closed set, by definition.
bs:Country  a owl:Class ;
    owl:equivalentClass [ a owl:Class ; owl:oneOf ( bt:place-scotland bt:place-england bt:place-wales ) ] .
bt:place-scotland a owl:NamedIndividual . bt:place-england a owl:NamedIndividual . bt:place-wales a owl:NamedIndividual .

# A complement: a Work that is not Fiction. Nothing is ever proved into it.
bs:Fiction     a owl:Class ; rdfs:subClassOf bs:Work .
bs:NonFiction  a owl:Class ;
    owl:equivalentClass [ a owl:Class ; owl:intersectionOf ( bs:Work [ a owl:Class ; owl:complementOf bs:Fiction ] ) ] .
# bt:book-the-loom is a Work; fiction or not, the file does not say, so NonFiction gets no member.
""",
    queries=[Query("Who is an Author, after the closure", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?who WHERE { ?who a bs:Author }""", on="reasoned", rows=1)],
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True, inferred=["bt:author-rhona-blackwood rdf:type bs:Author", "bt:place-scotland rdf:type bs:Country"],
                not_inferred=["bt:book-the-loom rdf:type bs:NonFiction"],
                rl_inferred=["bt:author-rhona-blackwood rdf:type bs:Author"]),
)
specs.register("o46", "primerComplex", "gistRestrictions")

o(
    oid="o47", module=M,
    title="Cardinality: the reasoner merges before it complains",
    decides="Cardinality restrictions are written for meaning and never for validation, because two values under a maximum of one make the reasoner conclude they are the same thing, not that the data is wrong.",
    corner="referent",
    why="'A shop is in exactly one settlement.' Written as a cardinality "
        "restriction or as a functional property that means what it says, "
        "and what it says has a consequence nobody wants at first: a shop "
        "recorded in Wigtown and in Hay-on-Wye is no error at all, and the "
        "reasoner reads it as evidence that Wigtown and Hay-on-Wye are one "
        "place. The RL closure of this file contains owl:sameAs between the "
        "two towns and HermiT agrees that the file is consistent, because "
        "OWL makes no unique name assumption and two IRIs may name one "
        "thing until something says otherwise. Add owl:differentFrom "
        "between the towns and the very same file becomes inconsistent.\n\n"
        "That is the whole argument behind gist's rules seven to eleven, "
        "and behind o29. Use someValuesFrom rather than a minimum of one; "
        "use minimum cardinalities above one where you mean them; never a "
        "minimum of zero, which says nothing at all; and express data "
        "constraints with SHACL, where more than one town is a row in a "
        "report and the two towns stay two.\n\n"
        "Qualified cardinality is the useful cousin of all this, since a "
        "TrailSegment has exactly two bs:end values that are Bookshops, "
        "which carries meaning, a segment being a pair; and the reasoner "
        "uses it in just the same way, so that a third end merges with one "
        "of the other two.",
    diagram="""
   bs:locatedIn a owl:FunctionalProperty          at most one value, in every interpretation

   bt:shop-x bs:locatedIn bt:place-wigtown, bt:place-hay
     =>  bt:place-wigtown owl:sameAs bt:place-hay      (the RL closure; HermiT: consistent)

   + bt:place-wigtown owl:differentFrom bt:place-hay
     =>  inconsistent

   the shape that was meant:  sh:path bs:locatedIn ; sh:maxCount 1   (SHACL course s04)
""",
    learn=[
        "There is no unique name assumption, so two IRIs may turn out to be one thing, and a maximum cardinality merges before ever it contradicts.",
        "Cardinality is for meaning: that a segment has two ends is meaning, while a shop row having one town is a shape.",
        "differentFrom, AllDifferent and inverse-functional keys are how you tell the reasoner that two things really are two.",
    ],
    body=DECL + """
bs:Settlement  a owl:Class .
bs:Bookshop    a owl:Class .
bs:locatedIn   a owl:ObjectProperty, owl:FunctionalProperty ; rdfs:range bs:Settlement .

# The same commitment as restrictions, in the three unqualified forms: a
# bookshop is located in at most one, at least one, and so exactly one.
bs:Bookshop
    rdfs:subClassOf [ a owl:Restriction ; owl:onProperty bs:locatedIn ; owl:maxCardinality 1 ] ,
                    [ a owl:Restriction ; owl:onProperty bs:locatedIn ; owl:minCardinality 1 ] ,
                    [ a owl:Restriction ; owl:onProperty bs:locatedIn ; owl:cardinality 1 ] .

bt:shop-x         a bs:Bookshop ; bs:locatedIn bt:place-wigtown, bt:place-hay .
bt:place-wigtown  a bs:Settlement ; skos:prefLabel "Wigtown"@en .
bt:place-hay      a bs:Settlement ; skos:prefLabel "Hay-on-Wye"@en .

# A segment is a pair: qualified cardinality carrying meaning.
bs:TrailSegment  a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ; owl:onProperty bs:end ; owl:qualifiedCardinality 2 ; owl:onClass bs:Bookshop ] .
bs:end  a owl:ObjectProperty .
""",
    queries=[Query("Things the closure has decided are the same", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?a ?b WHERE { ?a owl:sameAs ?b . FILTER(?a != ?b && STR(?a) < STR(?b)) }""", on="reasoned", rows=1)],
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True, rl_sameas=[["bt:place-hay", "bt:place-wigtown"]]),
    tryit="Show Facts: the two towns are owl:sameAs. Add 'bt:place-wigtown owl:differentFrom bt:place-hay .', Get All, and run the "
          "checker: HermiT now reports the file inconsistent. The editor's closure will show both triples and say nothing.",
)
specs.register("o47", "primerCardinality", "primerEquality")

o(
    oid="o48", module=M,
    title="Property characteristics, and the property that cannot be two things",
    decides="bs:within is transitive, bs:connectsTo symmetric, bs:imprintOf asymmetric and irreflexive; and because a transitive property is non-simple, bs:within may not also be functional, which the profile checker enforces.",
    corner="referent",
    why="A property characteristic is an axiom about the relation as a "
        "whole. Transitive says that if Wigtown is within Dumfries and "
        "Galloway and that is within Scotland then Wigtown is within "
        "Scotland, and the reasoner writes the triple; symmetric says that "
        "a segment from A to B is a segment from B to A, so that "
        "bs:connectsTo asserted once holds both ways; asymmetric and "
        "irreflexive say that nothing is an imprint of itself or of its own "
        "imprint, and asserting either is a contradiction; functional and "
        "inverse-functional say at most one value, or at most one subject, "
        "with the merging behaviour of o47. Reflexive is rare, and the "
        "Trail has none.\n\n"
        "OWL 2 DL has a rule about combining them, and it is the rule that "
        "bit the Trail's vocabulary first: a transitive property is non- "
        "simple, and a non-simple property may not be functional, inverse- "
        "functional, irreflexive, asymmetric, disjoint with another, or "
        "used in a cardinality restriction. The reason is decidability, and "
        "the practical effect is that bs:within, being transitive, cannot "
        "also be declared functional, however natural 'directly within one "
        "place' may sound. This lesson's file declares both and the profile "
        "checker refuses it, naming the property; the fix is either to drop "
        "the functional declaration or to keep a separate non-transitive "
        "'directlyWithin' that is functional beneath a transitive 'within' "
        "above it.\n\n"
        "An RL engine does not enforce the global restriction, and this "
        "file shows why the restriction exists. The closure takes "
        "transitivity first, so that Wigtown is within Scotland, and then "
        "functionality, so that Wigtown's two within values must be one "
        "place, and it concludes that Dumfries and Galloway is Scotland, "
        "owl:sameAs, and that Scotland is within itself. The measured line "
        "has those triples, and nothing was wrong with the data.\n\n"
        "The SPARQL course's module 18 measures what a reasoner does with "
        "bs:within across the whole Trail, where sixty-three asserted pairs "
        "become a hundred and eighty-six, and module 08 reaches that same "
        "number three different ways.",
    diagram="""
   characteristic        axiom                                   consequence

   transitive            bs:within a owl:TransitiveProperty      within chains close: 63 pairs -> 186
   symmetric             bs:connectsTo a owl:SymmetricProperty   A connectsTo B => B connectsTo A
   asymmetric            bs:imprintOf a owl:AsymmetricProperty   A imprintOf B and B imprintOf A: contradiction
   irreflexive           bs:imprintOf a owl:IrreflexiveProperty  A imprintOf A: contradiction
   functional            bs:locatedIn a owl:FunctionalProperty   two values merge (o47)

   the global restriction: transitive => non-simple => not functional, not in a cardinality
   bs:within a owl:TransitiveProperty, owl:FunctionalProperty     NOT in OWL 2 DL
   ... and an RL engine, which does not check, concludes:
   bt:place-dumfries-galloway owl:sameAs bt:place-scotland
""",
    learn=[
        "A characteristic is an axiom about the whole relation, and each of them has a consequence the reasoner will act on.",
        "Transitive makes a property non-simple, and non-simple properties cannot be functional or counted; the checker enforces that, while an RL engine does not and merges a council area with a country instead.",
        "When you want both, split the property into a functional direct relation with a transitive closure above it.",
    ],
    body=DECL + """
bs:Place       a owl:Class .
bs:Bookshop    a owl:Class .
bs:Publisher   a owl:Class .

bs:connectsTo  a owl:ObjectProperty, owl:SymmetricProperty ;   rdfs:domain bs:Bookshop ;  rdfs:range bs:Bookshop .
bs:imprintOf   a owl:ObjectProperty, owl:AsymmetricProperty, owl:IrreflexiveProperty ; rdfs:domain bs:Publisher ; rdfs:range bs:Publisher .

# The combination OWL 2 DL forbids, declared to show the refusal.
bs:within      a owl:ObjectProperty, owl:TransitiveProperty, owl:FunctionalProperty ; rdfs:domain bs:Place ; rdfs:range bs:Place ;
    skos:editorialNote "Transitive and functional at once: outside OWL 2 DL. The shipped vocabulary drops the functional declaration."@en .

bt:place-wigtown            a bs:Place ; bs:within bt:place-dumfries-galloway .
bt:place-dumfries-galloway  a bs:Place ; bs:within bt:place-scotland .
bt:place-scotland           a bs:Place .
bt:shop-inkwell             a bs:Bookshop ; bs:connectsTo bt:shop-marginalia .
bt:shop-marginalia          a bs:Bookshop .
""",
    queries=[Query("What the closure adds: the transitive and symmetric consequences", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?s ?p ?o WHERE { ?s ?p ?o . FILTER(?p IN (bs:within, bs:connectsTo)) } ORDER BY ?p ?s""", on="reasoned", rows=8)],
    check=dict(profile=True, rl=True),
    expect=dict(dl=False, rl_inferred=["bt:place-wigtown bs:within bt:place-scotland",
                                        "bt:shop-marginalia bs:connectsTo bt:shop-inkwell"],
                rl_sameas=[["bt:place-dumfries-galloway", "bt:place-scotland"]]),
    local="the profile refusal on the MEASURED line comes from ROBOT",
)
specs.register("o48", "primerCharacteristics", "syntaxGlobal")

o(
    oid="o49", module=M,
    title="Inverses, chains and keys",
    decides="bs:wrote is declared the inverse of bs:author so that one assertion yields both directions; a property chain gives an event its town; and a key on ISBN says what identifies a work, without leaving OWL 2 DL.",
    corner="referent",
    why="owl:inverseOf says that two properties are one relation read in "
        "opposite directions, so that every bs:author triple yields a "
        "bs:wrote triple and the other way about, and the reasoner "
        "materialises whichever half was not asserted. That is what the "
        "SPARQL course's q44 constructs by hand, and what gist declines to "
        "do at all on the grounds that a caret in a query costs nothing, as "
        "o31 explains; the Trail declares two inverses deliberately so that "
        "this lesson and module 08 have something to show.\n\n"
        "A property chain is an inverse's larger sibling, since bs:heldAt "
        "followed by bs:locatedIn implies bs:eventTown, so that an event "
        "held at a shop in Wigtown is an event in Wigtown and the reasoner "
        "adds the triple; the RL closure supports chains and so does the "
        "editor, and the global restriction from o48 applies here too, a "
        "property defined by a chain being non-simple. rdfs:subPropertyOf "
        "is the property hierarchy's own inheritance, and since bs:author "
        "and bs:translatedBy both sit under bs:hasContributor, a query for "
        "everyone who contributed to a work in any capacity is a single "
        "pattern once the closure has run.\n\n"
        "A key is the DL-safe way of saying that a value identifies a "
        "thing. An inverse-functional datatype property would say it too, "
        "that no two works share an ISBN, and it falls outside OWL 2 DL for "
        "datatype properties; owl:hasKey says it from inside DL, so that "
        "two Works with the same bs:isbn are one Work, with the merging "
        "behaviour of o47. That is meaning, an ISBN really does identify an "
        "edition, and the shape that says no two rows share an ISBN is the "
        "SHACL course's s39, which checks the check digit into the bargain.",
    diagram="""
   inverse     bs:wrote owl:inverseOf bs:author
               bt:book-x bs:author bt:person-y   =>  bt:person-y bs:wrote bt:book-x

   chain       bs:heldAt o bs:locatedIn  =>  bs:eventTown
               bt:event-1 bs:heldAt bt:shop-inkwell . bt:shop-inkwell bs:locatedIn bt:place-wigtown .
                 =>  bt:event-1 bs:eventTown bt:place-wigtown

   key         bs:Work owl:hasKey ( bs:isbn )
               two Works, one ISBN  =>  one Work (sameAs)        inside OWL 2 DL
               bs:isbn a owl:InverseFunctionalProperty           outside OWL 2 DL for a datatype property
""",
    learn=[
        "An inverse is one relation read both ways, so declare it where a reasoner will be there to use it, and otherwise let the query language walk it backwards for nothing.",
        "A property chain derives a relation from a path, and the RL closure and the editor both compute it.",
        "owl:hasKey is how you say that a value identifies a thing while staying inside DL, and like every identity axiom it merges.",
    ],
    body=DECL + """
bs:Work      a owl:Class .
bs:Person    a owl:Class .
bs:Event     a owl:Class .
bs:Bookshop  a owl:Class .

bs:author    a owl:ObjectProperty ; rdfs:subPropertyOf bs:hasContributor .
bs:wrote     a owl:ObjectProperty ; owl:inverseOf bs:author .
bs:translatedBy   a owl:ObjectProperty ; rdfs:subPropertyOf bs:hasContributor .
bs:hasContributor a owl:ObjectProperty .   # anyone who contributed in any capacity: a sub-property hierarchy

bs:heldAt     a owl:ObjectProperty .
bs:locatedIn  a owl:ObjectProperty .
bs:eventTown  a owl:ObjectProperty ; owl:propertyChainAxiom ( bs:heldAt bs:locatedIn ) .

bs:isbn  a owl:DatatypeProperty .
bs:Work  owl:hasKey ( bs:isbn ) .

# Inverse-functional on an object property is inside DL: a website resource
# identifies its shop. On a datatype property it is not, which is why the
# ISBN is a key instead.
bs:hasWebsite  a owl:ObjectProperty, owl:InverseFunctionalProperty ; rdfs:domain bs:Bookshop .

bt:book-the-loom  a bs:Work ; bs:author bt:author-rhona-blackwood ; bs:isbn "9787063088596" .
bt:book-duplicate a bs:Work ; bs:isbn "9787063088596" .
bt:author-rhona-blackwood  a bs:Person .
bt:event-1        a bs:Event ; bs:heldAt bt:shop-inkwell .
bt:shop-inkwell   a bs:Bookshop ; bs:locatedIn bt:place-wigtown .
""",
    queries=[Query("The inferred inverse, the chain, and the key's merge", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?s ?p ?o WHERE { ?s ?p ?o . FILTER(?p IN (bs:wrote, bs:eventTown, owl:sameAs) && ?s != ?o) } ORDER BY ?p""", on="reasoned")],
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True,
                rl_inferred=["bt:author-rhona-blackwood bs:wrote bt:book-the-loom", "bt:event-1 bs:eventTown bt:place-wigtown",
                             "bt:book-the-loom bs:hasContributor bt:author-rhona-blackwood"],
                rl_sameas=[["bt:book-duplicate", "bt:book-the-loom"]]),
)
specs.register("o49", "primerInverse", "primerKeys")

o(
    oid="o50", module=M,
    title="Datatypes and profiles: where the language draws its lines",
    decides="Values are typed only with datatypes in the OWL 2 map, which excludes xsd:gYear and xsd:date; the year properties are left without a range for that reason; and the profile a consumer needs is checked, not assumed.",
    corner="referent",
    why="OWL 2 has a datatype map, and it is a good deal shorter than XML "
        "Schema's. xsd:integer, xsd:decimal, xsd:string, xsd:boolean, "
        "xsd:dateTime and xsd:anyURI are on it; xsd:gYear and xsd:date are "
        "not. A range of xsd:gYear on bs:founded therefore puts the "
        "vocabulary outside OWL 2 DL, and declaring xsd:gYear as an "
        "rdfs:Datatype makes matters worse rather than better, since it "
        "becomes a user-defined datatype and using one in an assertion is a "
        "second violation. So the shipped vocabulary declares no range at "
        "all on its four year properties and its two date properties and "
        "says why in each comment, while the SPARQL course keeps the gYear "
        "values in the data because the portability lesson they teach is "
        "worth more than the conformance. This file states the range and "
        "takes the consequence, which the profile checker duly reports.\n\n"
        "Datatype restrictions are the useful part of the map, since a "
        "staff count is an integer of at least zero, written as a "
        "restriction on xsd:integer with xsd:minInclusive, and that is "
        "meaning, which a reasoner will use.\n\n"
        "The profiles are three smaller languages inside DL, each with a "
        "reasoning guarantee of its own: EL for large class hierarchies "
        "with existentials, QL for querying data through the ontology, and "
        "RL for rule engines, which is what the editor's reasoner and the "
        "owlrl closure both are. Each of them drops something, so that EL "
        "has no universals or inverses, QL no existentials on the right, "
        "and RL no existentials on the right either and no class as a "
        "superclass expression with a someValuesFrom in it. The measured "
        "line says which profiles this file is in, and the shipped "
        "vocabulary is in DL and in none of the three, EL and QL refusing "
        "its functional object properties and RL the union domain of "
        "bs:locatedIn. Pick the profile that the consumer's reasoner runs, "
        "and then check it.",
    diagram="""
   in the OWL 2 datatype map              not in it
   xsd:integer xsd:decimal xsd:string     xsd:gYear   xsd:date   xsd:gMonth ...
   xsd:boolean xsd:dateTime xsd:anyURI    (a range of one: not DL; declaring it: worse)

   a datatype restriction:  bs:staffCount rdfs:range [ owl:onDatatype xsd:integer ; owl:withRestrictions ( [ xsd:minInclusive 0 ] ) ]

   profile   guarantee                          drops
   EL        polynomial classification          universals, inverses, disjunction
   QL        query rewriting over data          existentials on the right, chains
   RL        rule-based closure (the editor)    existentials on the right; someValuesFrom in a superclass
""",
    learn=[
        "The datatype map is the list, and xsd:gYear and xsd:date are not on it, so a range naming them leaves DL, while declaring them makes it worse.",
        "A datatype restriction is meaning about values and it is cheap, whereas a missing range is often the right choice.",
        "Choose a profile by the reasoner that will actually run, and then check it; the editor's is RL.",
    ],
    body=DECL + """
bs:Bookshop  a owl:Class .

# Outside the map: the range the shipped vocabulary declines to state.
bs:founded  a owl:DatatypeProperty ; rdfs:domain bs:Bookshop ; rdfs:range xsd:gYear ;
    skos:editorialNote "xsd:gYear is not in the OWL 2 datatype map. The profile checker refuses this file for it."@en .

# Inside the map, with a restriction: a staff count is an integer of at least zero.
bs:staffCount  a owl:DatatypeProperty ; rdfs:domain bs:Bookshop ;
    rdfs:range [ a rdfs:Datatype ; owl:onDatatype xsd:integer ; owl:withRestrictions ( [ xsd:minInclusive 0 ] ) ] .

bt:shop-inkwell  a bs:Bookshop ; bs:founded "1979"^^xsd:gYear ; bs:staffCount 4 .
""",
    check=dict(profiles=True),
    expect=dict(dl=False),
    local="the profile verdicts come from ROBOT; the editor parses the file without complaint",
)
specs.register("o50", "syntaxDatatypeMap", "primerProfiles")
