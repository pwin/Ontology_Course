# -*- coding: utf-8 -*-
"""Module 06 -- The ladder: RDFS and SKOS, one idea at rising commitment."""
from ontocat import o, Query, DGENRES, DPLACES
import specs

M = "06-the-ladder"

DECL = """
skos:prefLabel      a owl:AnnotationProperty .
skos:altLabel       a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:scopeNote      a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
"""

o(
    oid="o35", module=M,
    title="A class is a set, in every model",
    decides="Classes are read as sets and the vocabulary's structural words as set operations: rdf:type is membership, rdfs:subClassOf is subset, equivalence is equality, disjointness is an empty intersection.",
    corner="referent",
    why="OWL 2's Direct Semantics says what an interpretation is: a domain "
        "of things, and for every class a subset of that domain, which is "
        "called its extension, with an individual in the class when it is "
        "in the subset. rdfs:subClassOf then means that the one subset is "
        "contained in the other, owl:equivalentClass that they are the same "
        "subset, and owl:disjointWith that they share nothing at all; a "
        "restriction is a set defined by a condition on its members, such "
        "as the things that have some bs:locatedIn value in Settlement. "
        "Every construct from here to the top of the ladder is a way of "
        "saying something about sets, and reading them that way is what "
        "makes RDFS, SKOS and OWL one idea rather than three.\n\n"
        "Two cautions keep the picture straight. The first is the open "
        "world, since the extension is not the thirty-three shops in the "
        "file but a set that the axioms constrain and the data merely "
        "samples, so that a shop the file never mentions is in it just the "
        "same, and 'every Bookshop is located in some Settlement' is true "
        "of the set even where the file records no town. The second is that "
        "a class is not its extension: two classes that happen to have the "
        "same members in this data are not thereby the same class, because "
        "in another interpretation they need not be, and OWL 2's punning "
        "lets the same IRI be a class and an individual, read separately, "
        "which is how o14 typed bs:Author as a gufo:Role.\n\n"
        "SKOS does not use sets at all. A skos:Concept is a particular and "
        "skos:broader is a relation between two particulars that promises "
        "nothing whatever about members, which is no weakness, and is the "
        "reason the concept scheme sits on the rung below the class "
        "hierarchy and why o40 has to do some work to climb from the one to "
        "the other.",
    diagram="""
   in every interpretation                      set reading

   bs:Bookshop                                   a subset B of the domain
   bt:shop-inkwell a bs:Bookshop                 inkwell is in B
   bs:Settlement rdfs:subClassOf bs:Place        S is a subset of P
   bs:Work owl:equivalentClass bs:Book           W = K
   bs:Place owl:disjointWith bs:Bookshop         P and B share no member
   owl:Thing, owl:Nothing                        the whole domain; the empty set
   [ owl:onProperty bs:locatedIn ;               { x : some y with locatedIn(x, y), y in S }
     owl:someValuesFrom bs:Settlement ]

   cautions: the data samples the set; it does not enumerate it
             a class is not its extension; two with the same members here may differ elsewhere
""",
    learn=[
        "Read every class as a set and every structural axiom as a claim about sets, since that is the reading the specification gives and it is what makes the ladder one ladder.",
        "Under the open world the set is constrained by the axioms and sampled by the data, so absence from the file is not absence from the set.",
        "A concept is a particular and broader is a relation between particulars, with no sets involved anywhere, which is why it is a lower rung.",
    ],
    body=DECL + """
# owl:Thing is the whole domain; every class is a subset of it, and saying
# so is harmless and occasionally clarifying.
bs:Place       a owl:Class ; rdfs:subClassOf owl:Thing ; skos:prefLabel "Place"@en .
bs:Settlement  a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Settlement"@en .
bs:Bookshop    a owl:Class ; owl:disjointWith bs:Place ; skos:prefLabel "Bookshop"@en .

bt:place-wigtown  a bs:Settlement ; skos:prefLabel "Wigtown"@en .
bt:shop-inkwell   a bs:Bookshop ;   skos:prefLabel "The Inkwell"@en .

# A concept is a particular. No set is involved.
skos:Concept  a owl:Class .
skos:broader  a owl:ObjectProperty .
bt:genre-crime-fiction  a skos:Concept ; skos:broader bt:genre-fiction .
bt:genre-fiction        a skos:Concept .
""",
    queries=[Query("Membership by subset: what is a Place, after the closure", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?place WHERE { ?place a bs:Place }""", on="reasoned", rows=1)],
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True, rl_inferred=["bt:place-wigtown rdf:type bs:Place"]),
    tryit="Press Show Facts, and among the implicit triples you will find "
          "bt:place-wigtown rdf:type bs:Place, which is the set reading "
          "computed for you. Nothing is said about the concepts, because "
          "broader promises nothing about members.",
)
specs.register("o35", "directSemantics", "primerOpenWorld")

o(
    oid="o36", module=M,
    title="Rung one, a list; rung two, a concept scheme",
    decides="The genres are a SKOS concept scheme: particulars with labels, arranged by broader and narrower, promising nothing about the works in them; and the scheme's uneven depth is kept because it is true.",
    corner="symbol and thought",
    why="The lowest rung is a list of terms with IRIs and labels, which is "
        "where module 01 started, and it promises only that the terms exist "
        "and are distinct from one another. The next rung up is a concept "
        "scheme, where each genre is a skos:Concept in a "
        "skos:ConceptScheme, each has one preferred label per language and "
        "as many alternatives as you like, and broader and narrower arrange "
        "them into a tree, or a lattice, since SKOS is content to let a "
        "concept have two broader ones. What has been promised is that "
        "these particulars are related in this way, and nothing has been "
        "said about any work at all; a reasoner given the scheme will not "
        "conclude that a cosy crime novel is a work of fiction, because the "
        "scheme has no members to conclude it about.\n\n"
        "This is why SKOS is the right rung for a shelf plan. Curators move "
        "genres about and broader changes, and no data needs retyping on "
        "that account. The Trail's scheme has thirty-one concepts, two to "
        "four levels deep, and the depth is uneven because crime fiction "
        "has kinds that poetry does not; a model that forced every branch "
        "to the same depth would be tidier and false.\n\n"
        "That unevenness carries the SPARQL course's best-known lesson, "
        "made on the place hierarchy in q28 and on this tree in q33: a "
        "fixed chain of two broader hops from Fiction finds some of the "
        "genres and silently misses the rest, while skos:broader+ finds "
        "them all. skos:broader is deliberately not transitive, "
        "skos:broaderTransitive is, and a path operator computes the "
        "closure without a reasoner anywhere in sight, which module 08 "
        "comes back to as the first of three routes to the same inference.",
    diagram="""
   rung 1  a list         bt:genre-cosy-crime  skos:prefLabel "Cosy Crime"@en          exists, is distinct
   rung 2  a scheme       bt:genre-cosy-crime  skos:broader  bt:genre-crime-fiction   related, as particulars
                          bt:genre-crime-fiction skos:broader bt:genre-fiction
                          bt:genre-poetry      skos:broader  bt:genre-literature       (two levels, not four)

   promised: these particulars relate thus.  not promised: anything about a work.

   q33:  skos:broader/skos:broader  from Fiction   misses the branches of other depths
         skos:broader+              from Fiction   finds every descendant
""",
    learn=[
        "A concept scheme relates particulars and promises nothing about members, which is exactly why it can be rearranged without retyping any data.",
        "Keep a hierarchy as uneven as the world is, because a fixed depth is a lie that some query will eventually trip over.",
        "skos:broader is not transitive on purpose, and a path operator, or broaderTransitive, gives you the closure on the day a question needs it.",
    ],
    body=DECL + """
skos:Concept        a owl:Class .
skos:ConceptScheme  a owl:Class .
skos:inScheme       a owl:ObjectProperty .
skos:hasTopConcept  a owl:ObjectProperty .
skos:broader        a owl:ObjectProperty .

bt:genre-scheme  a skos:ConceptScheme ; skos:prefLabel "Bookshop Trail genre scheme"@en ; skos:hasTopConcept bt:genre-literature .

bt:genre-literature     a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Literature"@en .
bt:genre-fiction        a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Fiction"@en, "Ffuglen"@cy ; skos:broader bt:genre-literature .
bt:genre-poetry         a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Poetry"@en, "Barddoniaeth"@cy ; skos:altLabel "Verse"@en ; skos:broader bt:genre-literature .
bt:genre-crime-fiction  a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Crime Fiction"@en ; skos:altLabel "Mystery"@en ; skos:broader bt:genre-fiction .
bt:genre-cosy-crime     a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Cosy Crime"@en ; skos:altLabel "Cozy Mystery"@en ; skos:broader bt:genre-crime-fiction .
bt:genre-tartan-noir    a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Tartan Noir"@en ; skos:broader bt:genre-crime-fiction .
""",
    data=DGENRES,
    queries=[
        Query("Two hops down from Fiction, in the full scheme", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT (COUNT(DISTINCT ?g) AS ?found) WHERE { ?g skos:broader/skos:broader bt:genre-fiction }""", on="data"),
        Query("Every descendant of Fiction, however deep", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT (COUNT(DISTINCT ?g) AS ?found) WHERE { ?g skos:broader+ bt:genre-fiction }""", on="data"),
        Query("Depth of every leaf, to see the unevenness", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?leaf (COUNT(?up) AS ?depth) WHERE {
  ?leaf a skos:Concept ; skos:broader+ ?up .
  FILTER NOT EXISTS { ?below skos:broader ?leaf }
} GROUP BY ?leaf ORDER BY DESC(?depth)""", on="data"),
    ],
    check=dict(profile=True, with_data=DGENRES),
    expect=dict(dl=True),
    notes="The counts in the AFTERWARDS queries are for the full scheme, data/02-genres.ttl; open it in the editor to run them. The two "
          "COUNT queries return one row each, and the numbers inside differ: that difference is q33, and q28 is the same lesson on places.",
)
specs.register("o36", "skosSchemes", "skosSemantic")

o(
    oid="o37", module=M,
    title="Rung three, a class hierarchy: membership is inherited",
    decides="Places are a class hierarchy, not a concept scheme, because a query about Places must find every Settlement without being told; rdfs:subClassOf commits to that and a reasoner delivers it.",
    corner="referent",
    why="rdfs:subClassOf is the first promise about members. Settlement "
        "under Place means that every settlement is a place, and a "
        "reasoner, any reasoner at all, will type Wigtown as a Place "
        "without being told to; RDF Semantics writes the rule down, that if "
        "x is in A and A is a subclass of B then x is in B. The editor's "
        "Show Facts does it in the browser, and the OWL 2 RL closure this "
        "lesson was measured with does the same over the place file, adding "
        "the typing for every settlement, council area, region and country "
        "in it.\n\n"
        "The Trail chose a class hierarchy for places and a concept scheme "
        "for genres, and the reason lies in what each of them is asked. A "
        "question about places, such as which shops are in Wales, needs "
        "every kind of place to be a place and never needs to say which "
        "kind on the way down; a question about genres, such as which shops "
        "specialise in crime fiction including its kinds, needs the tree "
        "walked explicitly and is answered by a path over particulars. So: "
        "a class hierarchy where membership must be inherited, and a "
        "concept scheme where the tree must be walked.\n\n"
        "The subclass rule is transitive as well, so that Settlement under "
        "Place under Feature makes every town a feature, and it is depth "
        "that makes deep hierarchies risky and shallow ones cheap, which is "
        "why the backbone from o12 is only two levels deep.",
    diagram="""
   rung 3  a class hierarchy

   bs:Settlement rdfs:subClassOf bs:Place       every settlement is a place: a promise about members
   bt:place-wigtown a bs:Settlement             ... so the reasoner adds:
                                                bt:place-wigtown a bs:Place

   the rule (RDF Semantics, rdfs9):  x type A . A subClassOf B  =>  x type B

   places: a class hierarchy, membership inherited, 'which shops are in Wales' just works
   genres: a concept scheme, tree walked by a path, 'including its kinds' is explicit
""",
    learn=[
        "rdfs:subClassOf is the first promise about members, and the reasoner keeps it, typing every instance of the subclass with the superclass.",
        "Use a class hierarchy where membership has to be inherited silently, and a concept scheme where the tree has to be walked explicitly.",
        "Subclass is transitive, so depth multiplies inferences, which is a good reason to keep the backbone shallow.",
    ],
    body=DECL + """
geo:Feature     a owl:Class ; skos:prefLabel "Feature"@en .
bs:Place        a owl:Class ; rdfs:subClassOf geo:Feature ; skos:prefLabel "Place"@en .
bs:Settlement   a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Settlement"@en .
bs:CouncilArea  a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Council Area"@en .
bs:Region       a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Region"@en .
bs:Country      a owl:Class ; rdfs:subClassOf bs:Place ; skos:prefLabel "Country"@en .

bt:place-wigtown            a bs:Settlement ;  skos:prefLabel "Wigtown"@en .
bt:place-dumfries-galloway  a bs:CouncilArea ; skos:prefLabel "Dumfries and Galloway"@en .
bt:place-scotland           a bs:Country ;     skos:prefLabel "Scotland"@en .
""",
    data=DPLACES,
    queries=[Query("What is a Place, after the closure", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT (COUNT(DISTINCT ?p) AS ?places) WHERE { ?p a bs:Place }""", on="reasoned")],
    check=dict(profile=True, rl=True),
    expect=dict(dl=True, rl_inferred=["bt:place-wigtown rdf:type bs:Place", "bt:place-wigtown rdf:type geo:Feature",
                                       "bt:place-scotland rdf:type bs:Place"]),
    tryit="Load data/03-places.ttl, hide the types and annotations and choose "
          "the dot engine, and you are looking at the containment hierarchy. "
          "Then press Show Facts and count how many things are now typed "
          "bs:Place that the file never said were.",
)
specs.register("o37", "rdfsSubClassOf", "rdfsRules")

o(
    oid="o38", module=M,
    title="Rung four, domain and range: inference rules, not constraints",
    decides="A domain is declared only when everything that will ever have the property is of that class, because the reasoner will type whatever has it; the Trail's bs:locatedIn gets a union domain for that reason.",
    corner="referent",
    why="Every newcomer reads rdfs:domain as a constraint, as though it "
        "said that only bookshops may have a location, whereas RDF "
        "Semantics reads it as a rule, saying that whatever has a location "
        "is a bookshop. The two readings agree on clean data and part "
        "company at the first publisher with an address: declare "
        "bs:locatedIn's domain as bs:Bookshop, load the people file, and "
        "the reasoner types Northwind Press as a bookshop without error or "
        "warning. This lesson's file does exactly that, and the closure "
        "measured on it contains the triple.\n\n"
        "Range is the same rule running in the other direction, so that "
        "whatever is the value of bs:locatedIn is a Settlement. That one is "
        "usually what you wanted, and it still bites, because a range of "
        "xsd:integer on a property whose values are strings does not reject "
        "the strings but declares them to be integers.\n\n"
        "The habit that follows is the one from o31: declare a domain only "
        "where every use will agree with it, and where two classes will "
        "share a property, declare the union, which is the next rung's "
        "vocabulary; or declare nothing at all, as gist mostly does, and "
        "let the shapes say what the data must look like. The retyping is "
        "not a bug in RDFS but RDFS doing exactly what it says, and the "
        "SHACL course's s59, the inference that hides an error, is the same "
        "fact seen from the validator's side of the fence.",
    diagram="""
   rdfs:domain, read as a constraint (wrong)       rdfs:domain, read as a rule (right)

   only Bookshops may be locatedIn                 whatever is locatedIn is a Bookshop
   Northwind Press locatedIn Edinburgh => error    Northwind Press locatedIn Edinburgh
                                                     => Northwind Press a Bookshop   (no error, no warning)

   the rule (rdfs2):  p domain C . x p y  =>  x type C

   the fix: a union domain, or none, and a shape for the constraint
""",
    learn=[
        "rdfs:domain and rdfs:range add types, and they never reject anything at all.",
        "Declare a domain only where every use of the property will agree with it, since two classes sharing a property want a union, or nothing.",
        "The constraint you had in mind is a shape, and the SHACL course's s59 shows the other half of this lesson.",
    ],
    body=DECL + """
bs:Bookshop    a owl:Class ; skos:prefLabel "Bookshop"@en .
bs:Publisher   a owl:Class ; skos:prefLabel "Publisher"@en .
bs:Settlement  a owl:Class ; skos:prefLabel "Settlement"@en .

# The narrow domain, declared to show what it does.
bs:locatedIn
    a            owl:ObjectProperty ;
    rdfs:domain  bs:Bookshop ;
    rdfs:range   bs:Settlement ;
    skos:editorialNote "Domain too narrow, on purpose: the reasoner will type every publisher with an address as a bookshop."@en .

bt:shop-inkwell   a bs:Bookshop ;  bs:locatedIn bt:place-wigtown .
bt:pub-northwind  a bs:Publisher ; bs:locatedIn bt:place-edinburgh .
bt:place-wigtown    skos:prefLabel "Wigtown"@en .
bt:place-edinburgh  skos:prefLabel "Edinburgh"@en .
""",
    queries=[Query("Every bookshop, after the closure", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?shop WHERE { ?shop a bs:Bookshop }""", on="reasoned", rows=2)],
    check=dict(profile=True, rl=True),
    expect=dict(dl=True, rl_inferred=["bt:pub-northwind rdf:type bs:Bookshop", "bt:place-edinburgh rdf:type bs:Settlement"]),
    tryit="Press Show Facts and Northwind Press is now a bs:Bookshop. Change "
          "the domain to a union of Bookshop and Publisher, press Get All and "
          "Show Facts again: the union is a class with no name, so Northwind "
          "is typed with that instead, which is true and useless. Then remove "
          "the domain altogether.",
)
specs.register("o38", "rdfsDomain", "rdfsRange")

SKOS_SHAPES = """
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix bt:   <https://example.org/bookshop-trail/> .

# The SKOS integrity conditions the editor can check, as shapes.
bt:ConceptShape
    a               sh:NodeShape ;
    sh:targetClass  skos:Concept ;
    sh:property [ sh:path skos:prefLabel ; sh:minCount 1 ; sh:uniqueLang true ;
                  sh:message "S14: at most one preferred label per language." ] ;
    sh:property [ sh:path skos:inScheme ; sh:minCount 1 ;
                  sh:message "Every concept is in a scheme." ] ;
    sh:property [ sh:path skos:related ; sh:disjoint skos:broader ;
                  sh:message "S27: related and broader are disjoint." ] ;
    sh:property [ sh:path [ sh:oneOrMorePath skos:broader ] ; sh:disjoint [ sh:zeroOrOnePath skos:narrower ] ;
                  sh:message "No cycles: nothing is broader than itself." ] ;
    sh:sparql [
        sh:message "A concept is not its own ancestor." ;
        sh:prefixes <https://example.org/bookshop-trail/> ;
        sh:select \"\"\"
            SELECT $this WHERE { $this <http://www.w3.org/2004/02/skos/core#broader>+ $this }
        \"\"\" ;
    ] .
"""

o(
    oid="o39", module=M,
    title="SKOS in full: labels, notes, related, mapping, and the integrity conditions",
    decides="The genre scheme carries one preferred label per language, alternatives, scope notes, associative links kept apart from hierarchy, and mappings to outside schemes by match properties rather than owl:sameAs; and its integrity is checked by shapes.",
    corner="all three",
    why="SKOS is small and complete, and it divides into six kinds of "
        "statement. There are labels, prefLabel and altLabel and "
        "hiddenLabel for the misspellings, with the condition S14 that a "
        "concept has at most one preferred label per language. There are "
        "notes, definition and scopeNote and example and historyNote and "
        "changeNote and editorialNote, which is the same set gist "
        "recommends for ontologies, and that is no coincidence. There is "
        "hierarchy, broader and narrower, with transitive versions for "
        "queries. There is association, skos:related, for Tartan Noir and "
        "Scottish Interest, which are neither above nor below one another, "
        "subject to the condition S27 that a concept is not both related "
        "and broader to the same thing. There is grouping, skos:Collection, "
        "for something like the Welsh-language shelf, a set of concepts "
        "that is not itself a concept. And there is mapping, exactMatch and "
        "closeMatch and broadMatch, to concepts in other schemes.\n\n"
        "The mapping properties are the ones worth getting right. "
        "owl:sameAs says that two IRIs have one referent, so that "
        "everything true of the one becomes true of the other, in both "
        "directions and for ever, whereas skos:exactMatch says only that "
        "two concepts in two schemes can be used interchangeably for "
        "retrieval, which is a smaller and safer claim about two "
        "particulars that remain two. The Trail's crime fiction is a "
        "closeMatch to Wikidata's crime fiction, which covers film and "
        "theatre as well as books, so that the scopes overlap and differ, "
        "which is what closeMatch is for.\n\n"
        "The integrity conditions are checkable, and this lesson's shapes "
        "check the ones that matter: one preferred label per language, "
        "every concept in a scheme, related disjoint from broader, and no "
        "concept its own ancestor. Run against the shipped scheme they "
        "report conformance, and run against this file, with its seeded "
        "cycle and doubled label, they report both; the SHACL course's s30 "
        "does the cycle check in the very same way.",
    diagram="""
   labels     prefLabel (one per language, S14)   altLabel   hiddenLabel
   notes      definition  scopeNote  example  historyNote  changeNote  editorialNote
   hierarchy  broader  narrower       (broaderTransitive for the closure)
   association related                 (disjoint from broaderTransitive, S27)
   grouping   Collection, member       (not a concept)
   mapping    exactMatch  closeMatch  broadMatch  narrowMatch  relatedMatch

   owl:sameAs      one referent, two names, everything transfers
   skos:closeMatch two concepts, interchangeable for retrieval, nothing else transfers
""",
    learn=[
        "SKOS has six kinds of statement and a property for each: labels, notes, hierarchy, association, grouping and mapping.",
        "Map between schemes with the match properties, since owl:sameAs merges the referents where exactMatch leaves them two.",
        "The integrity conditions are shapes, so run them in the editor before publishing a scheme, and keep a file that breaks them.",
    ],
    body=DECL + """
skos:Concept        a owl:Class .
skos:ConceptScheme  a owl:Class .
skos:Collection     a owl:Class .
skos:inScheme       a owl:ObjectProperty .
skos:broader        a owl:ObjectProperty .
skos:related        a owl:ObjectProperty, owl:SymmetricProperty .
skos:member         a owl:ObjectProperty .
skos:closeMatch     a owl:ObjectProperty .
skos:hiddenLabel    a owl:AnnotationProperty .

bt:genre-scheme         a skos:ConceptScheme ; skos:prefLabel "Bookshop Trail genre scheme"@en .
bt:genre-fiction        a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Fiction"@en .
bt:genre-crime-fiction  a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Crime Fiction"@en ;
    skos:altLabel "Mystery"@en ; skos:hiddenLabel "Crime fition"@en ;
    skos:scopeNote "Works whose plot turns on a crime and its investigation."@en ;
    skos:broader bt:genre-fiction ;
    skos:closeMatch wd:Q5937792 .
bt:genre-tartan-noir    a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Tartan Noir"@en ;
    skos:broader bt:genre-crime-fiction ; skos:related bt:genre-scottish-interest .
bt:genre-scottish-interest a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Scottish Interest"@en ;
    skos:broader bt:genre-literature .
bt:genre-literature     a skos:Concept ; skos:inScheme bt:genre-scheme ; skos:prefLabel "Literature"@en .

bt:shelf-welsh  a skos:Collection ; skos:prefLabel "The Welsh-language shelf"@en ;
    skos:member bt:genre-fiction, bt:genre-crime-fiction .

# Two seeded faults for the shapes: a doubled English label, and a cycle.
bt:genre-cosy-crime  a skos:Concept ; skos:inScheme bt:genre-scheme ;
    skos:prefLabel "Cosy Crime"@en, "Cozy Crime"@en ;
    skos:broader bt:genre-crime-fiction .
bt:genre-fiction     skos:broader bt:genre-cosy-crime .
""",
    companions={"skos-shapes.ttl": SKOS_SHAPES},
    shapes="skos-shapes.ttl",
    check=dict(profile=True, shacl=SKOS_SHAPES),
    expect=dict(dl=True, shacl_conforms=False),
    queries=[Query("Concepts that are their own ancestor", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT DISTINCT ?c WHERE { ?c skos:broader+ ?c }""", rows=3)],
)
specs.register("o39", "skosMapping", "skosS27")

o(
    oid="o40", module=M,
    title="Climbing a rung: when a concept becomes a class",
    decides="Where an axiom about members is needed, the concept is punned into a class as well, with rdfs:subClassOf running beside skos:broader, and the reasoner then types works by their genre's ancestors.",
    corner="referent",
    why="o24 gave the test, which is to promote a concept to a class when "
        "the first axiom about its members is needed. Suppose the website "
        "must show every work of fiction on one page and the works are "
        "tagged with the leaf genre only: a path over the scheme answers "
        "that in SPARQL and nothing more is called for. But suppose instead "
        "that a downstream consumer will only ever see the closure, or that "
        "a shape must target every work of fiction; then the concept scheme "
        "is a rung too low, and the promotion is mechanical. The same IRI "
        "becomes an owl:Class as well as a skos:Concept, rdfs:subClassOf is "
        "written beside every skos:broader, the works are typed with the "
        "class, and the reasoner does the rest. This lesson's file has "
        "three works typed with genres, two of them leaves, and the closure "
        "types each of them with every ancestor.\n\n"
        "This is punning, and OWL 2 DL permits it, since the class reading "
        "and the individual reading of bt:genre-crime-fiction are kept "
        "apart by the reasoner, so that bs:specialises can still point at "
        "the individual while works are members of the class; the profile "
        "checker confirms that the file is DL. What it costs is that every "
        "genre now has two readings to maintain, and every change to the "
        "shelf plan becomes a change to a class hierarchy, with all the "
        "retyping that implies. That is the price of the higher rung, and "
        "it is why the Trail does not pay it for genres.\n\n"
        "The set reading makes the promotion exact: the concept was a "
        "particular, the class is the set of works in that genre, broader "
        "between particulars becomes subset between sets, and a work typed "
        "with the leaf is, by inheritance, in every set above it.",
    diagram="""
   before: a particular                        after: a particular and a set

   bt:genre-cosy-crime a skos:Concept          bt:genre-cosy-crime a skos:Concept, owl:Class ;
     skos:broader bt:genre-crime-fiction           skos:broader     bt:genre-crime-fiction ;
                                                   rdfs:subClassOf  bt:genre-crime-fiction .
   bt:book-x bs:genre bt:genre-cosy-crime      bt:book-x a bt:genre-cosy-crime .
                                                 => bt:book-x a bt:genre-crime-fiction, bt:genre-fiction   (the reasoner)

   one IRI, two readings, kept apart: punning. The shelf plan is now a class hierarchy.
""",
    learn=[
        "Promotion is mechanical: add owl:Class, mirror broader with subClassOf, type the members, and the reasoner types them with every ancestor.",
        "Punning lets the concept keep its uses while the class gains members, and the profile checker confirms that this stays inside DL.",
        "The cost is two readings per term and retyping on every rearrangement, so pay it only where an axiom about members is needed.",
    ],
    body=DECL + """
skos:Concept  a owl:Class .
skos:broader  a owl:ObjectProperty .
bs:Work       a owl:Class ; skos:prefLabel "Work"@en .

bt:genre-fiction        a skos:Concept, owl:Class ; skos:prefLabel "Fiction"@en ;
    rdfs:subClassOf bs:Work .
bt:genre-crime-fiction  a skos:Concept, owl:Class ; skos:prefLabel "Crime Fiction"@en ;
    skos:broader bt:genre-fiction ;        rdfs:subClassOf bt:genre-fiction .
bt:genre-cosy-crime     a skos:Concept, owl:Class ; skos:prefLabel "Cosy Crime"@en ;
    skos:broader bt:genre-crime-fiction ;  rdfs:subClassOf bt:genre-crime-fiction .
bt:genre-tartan-noir    a skos:Concept, owl:Class ; skos:prefLabel "Tartan Noir"@en ;
    skos:broader bt:genre-crime-fiction ;  rdfs:subClassOf bt:genre-crime-fiction .

bt:book-the-book-town   a bt:genre-cosy-crime ;  skos:prefLabel "The Book Town"@en .
bt:book-the-clyde-tapes a bt:genre-tartan-noir ; skos:prefLabel "The Clyde Tapes"@en .
bt:book-a-margin        a bt:genre-fiction ;     skos:prefLabel "A Margin of Error"@en .
""",
    queries=[Query("Every work of fiction, after the closure", """
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?work WHERE { ?work a bt:genre-fiction }""", on="reasoned", rows=3)],
    check=dict(profile=True, reason=True, rl=True),
    expect=dict(dl=True, consistent=True,
                rl_inferred=["bt:book-the-book-town rdf:type bt:genre-crime-fiction", "bt:book-the-book-town rdf:type bt:genre-fiction",
                             "bt:book-the-book-town rdf:type bs:Work"],
                inferred=["bt:book-the-book-town rdf:type bt:genre-fiction"]),
)
specs.register("o40", "syntaxMetamodeling", "primerPunning")

o(
    oid="o41", module=M,
    title="What RDFS cannot say",
    decides="Disjointness, cardinality, inverses, defined classes and 'exactly one' are wanted and RDFS has none of them, so the list of what it cannot say becomes the agenda for the top of the ladder.",
    corner="referent",
    why="RDFS gives us classes and subclasses, properties and "
        "subproperties, domains and ranges, and labels, and with those it "
        "can say that every settlement is a place and that whatever is "
        "located somewhere is a shop. It cannot say that nothing is both a "
        "place and a shop; it cannot say that a shop is in one town, that a "
        "segment has two ends, that wrote and author are the same relation "
        "read in opposite directions, or that an author is a person who "
        "wrote something. Most of all it cannot be contradicted: assert "
        "that one thing is a Place and a Bookshop, run the RDFS closure, "
        "and it will type the thing with both and with their superclasses "
        "and report nothing at all, because in RDFS there is nothing to "
        "report.\n\n"
        "None of which is a flaw. A language in which you cannot be wrong "
        "is a language in which data from anywhere merges without an "
        "argument, and that is what RDFS was for; the cost is simply that "
        "the errors it cannot see stay in the data until a query finds "
        "them, and the SPARQL course's module 13 is the collection of "
        "queries that do.\n\n"
        "The list of what we wanted and could not say is the agenda for "
        "module 07, in order: disjointness first, because it is the "
        "cheapest and catches the most; then restrictions, which say what a "
        "member must have; then defined classes, which let the reasoner "
        "decide membership; then the property characteristics; and last the "
        "datatypes and profiles, which are where the language draws its own "
        "limits.",
    diagram="""
   wanted                                          RDFS       OWL 2 (module 07)

   nothing is both a Place and a Bookshop          --         owl:disjointWith            o43
   every Bookshop is in some Settlement            --         owl:someValuesFrom          o44
   a Bookshop stocks only Works                    --         owl:allValuesFrom           o45
   an Author is a Person who wrote something       --         owl:equivalentClass         o46
   a segment has exactly two ends                  --         owl:cardinality             o47
   wrote is author, backwards                      --         owl:inverseOf               o49
   within is transitive                            --         owl:TransitiveProperty      o48

   a language in which you cannot be wrong merges anything; the errors wait for a query
""",
    learn=[
        "RDFS cannot be contradicted, so a thing typed as two disjoint kinds is typed with both and nothing is reported.",
        "That is the design rather than an oversight, since data from anywhere merges; the cost is that the errors wait for a query to find them.",
        "The list of what RDFS cannot say is the order to learn OWL in, and disjointness comes first.",
    ],
    body=DECL + """
bs:Place       a rdfs:Class ; skos:prefLabel "Place"@en .
bs:Bookshop    a rdfs:Class ; skos:prefLabel "Bookshop"@en .
bs:Settlement  a rdfs:Class ; rdfs:subClassOf bs:Place .

# Both at once. RDFS has no way to object, and the closure types it with everything.
bt:oddity  a bs:Settlement, bs:Bookshop ; skos:prefLabel "A thing that is a town and a shop"@en .
""",
    queries=[Query("What the oddity is, after the RDFS closure", """
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?type WHERE { bt:oddity a ?type }""", on="reasoned", rows=3)],
    check=dict(rl=True),
    expect=dict(rl_inferred=["bt:oddity rdf:type bs:Place"]),
)
specs.register("o41", "rdfsEntailment", "primerDisjoint")
