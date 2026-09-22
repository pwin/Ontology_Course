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
        "of things, and for every class a subset of that domain, called its "
        "extension. An individual is in the class if it is in the subset. "
        "rdfs:subClassOf means the one subset is contained in the other. "
        "owl:equivalentClass means they are the same subset. "
        "owl:disjointWith means they share nothing. A restriction is a set "
        "defined by a condition on its members: the things that have some "
        "bs:locatedIn value in Settlement. Every construct from here to the "
        "top of the ladder is a way of saying something about sets, and "
        "reading them that way is what makes RDFS, SKOS and OWL one idea "
        "rather than three.\n\n"
        "Two cautions keep the picture straight. First, the open world: the "
        "extension is not the thirty-three shops in the file. It is a set "
        "the axioms constrain and the data samples, and a shop the file "
        "does not mention is in it just the same. 'Every Bookshop is "
        "located in some Settlement' is true of the set even where the "
        "file records no town. Second, a class is not its extension. Two "
        "classes that happen to have the same members in this data are "
        "not the same class, because in another interpretation they need "
        "not; and OWL 2's punning lets the same IRI be a class and an "
        "individual, read separately, which is how o14 typed bs:Author as "
        "a gufo:Role.\n\n"
        "SKOS does not use sets. A skos:Concept is a particular, and "
        "skos:broader is a relation between two particulars that promises "
        "nothing about any members. That is no weakness, and it is the reason the concept scheme is the rung below the class hierarchy, "
        "and why o40 has to do work to climb from one to the other.",
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
        "Read every class as a set and every structural axiom as a set claim. It is the reading the specification gives, and it makes the ladder one ladder.",
        "The open world: the set is constrained by the axioms and sampled by the data. Absence in the file is not absence from the set.",
        "A concept is a particular and broader is a relation between particulars. No sets are involved, which is why it is a lower rung.",
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
    tryit="Press Show Facts. The implicit triples include bt:place-wigtown rdf:type bs:Place: the set reading, computed. Nothing is said "
          "about the concepts, because broader promises nothing about members.",
)
specs.register("o35", "directSemantics", "primerOpenWorld")

o(
    oid="o36", module=M,
    title="Rung one, a list; rung two, a concept scheme",
    decides="The genres are a SKOS concept scheme: particulars with labels, arranged by broader and narrower, promising nothing about the works in them; and the scheme's uneven depth is kept because it is true.",
    corner="symbol and thought",
    why="The lowest rung is a list of terms with IRIs and labels, which is "
        "where module 01 started: it promises only that the terms exist "
        "and are distinct. The next rung is a concept scheme. Each genre "
        "is a skos:Concept in a skos:ConceptScheme; each has one preferred "
        "label per language and any number of alternatives; broader and "
        "narrower arrange them in a tree, or a lattice, since SKOS allows "
        "a concept two broader ones. What has been promised is this: these "
        "particulars are related in this way. Nothing has been said about "
        "any work. A reasoner given the scheme will not conclude that a "
        "cosy crime novel is a work of fiction, because the scheme has no "
        "members to conclude it about.\n\n"
        "This is why SKOS is the right rung for a shelf plan. Curators "
        "move genres about; broader changes; no data needs retyping. The "
        "Trail's scheme has thirty-one concepts, two to four levels deep, "
        "and the depth is uneven because crime fiction has kinds that "
        "poetry does not. A model that forced every branch to the same "
        "depth would be tidier and false.\n\n"
        "The unevenness carries the SPARQL course's best-known lesson, made on the place hierarchy in q28 and on this tree in q33: a fixed chain of two broader hops from Fiction finds some genres and silently misses the rest, while skos:broader+ finds them all. skos:broader is deliberately not transitive; "
        "skos:broaderTransitive is, and a path operator computes it "
        "without a reasoner. Module 08 comes back to that as the first of "
        "three routes to the same inference.",
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
        "A concept scheme relates particulars. It promises nothing about members, which is why it can be rearranged without retyping data.",
        "Keep a hierarchy as uneven as the world is. A fixed depth is a lie a query will trip on.",
        "skos:broader is not transitive on purpose. A path operator, or broaderTransitive, gives the closure when a question needs it.",
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
        "under Place means every settlement is a place, and a reasoner, "
        "any reasoner, will type Wigtown as a Place without being told. "
        "RDF Semantics writes the rule down: if x is in A and A is a "
        "subclass of B, x is in B. The editor's Show Facts does it in the "
        "browser; the OWL 2 RL closure this lesson was measured with does "
        "the same on the place file and adds the typing for every "
        "settlement, council area, region and country in it.\n\n"
        "The Trail chose a class hierarchy for places and a concept scheme "
        "for genres, and the reason is what each is asked. A question "
        "about places, 'which shops are in Wales', needs every kind of "
        "place to be a place and never needs to say which kind on the way "
        "down. A question about genres, 'which shops specialise in crime "
        "fiction including its kinds', needs to walk the tree explicitly, "
        "and is answered by a path over particulars. Class hierarchy where "
        "membership must be inherited; concept scheme where the tree must "
        "be walked.\n\n"
        "The subclass rule is also transitive: Settlement under Place "
        "under Feature makes every town a feature. Depth is what makes deep hierarchies risky and shallow ones cheap, and it is why the "
        "backbone from o12 is two levels deep.",
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
        "rdfs:subClassOf is the first promise about members, and the reasoner keeps it: every instance of the subclass is typed with the superclass.",
        "Use a class hierarchy where membership must be inherited silently; a concept scheme where the tree must be walked explicitly.",
        "Subclass is transitive. Depth multiplies inferences, which is a reason to keep the backbone shallow.",
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
    tryit="Load data/03-places.ttl, hide types and annotations, choose the dot engine: the containment hierarchy. Then Show Facts, and count "
          "how many things are now typed bs:Place that the file never said were.",
)
specs.register("o37", "rdfsSubClassOf", "rdfsRules")

o(
    oid="o38", module=M,
    title="Rung four, domain and range: inference rules, not constraints",
    decides="A domain is declared only when everything that will ever have the property is of that class, because the reasoner will type whatever has it; the Trail's bs:locatedIn gets a union domain for that reason.",
    corner="referent",
    why="Every newcomer reads rdfs:domain as a constraint: 'only bookshops "
        "may have a location'. RDF Semantics reads it as a rule: 'whatever "
        "has a location is a bookshop'. The two agree on clean data and "
        "part company on the first publisher with an address. Declare "
        "bs:locatedIn's domain as bs:Bookshop, load the people file, and "
        "the reasoner types Northwind Press as a bookshop, without error "
        "or warning. This lesson's file does that, and the closure "
        "measured on it contains the triple.\n\n"
        "Range is the same rule in the other direction: whatever is the "
        "value of bs:locatedIn is a Settlement. That one is usually "
        "wanted, and it still bites: a range of xsd:integer on a property "
        "whose values are strings does not reject the strings, it "
        "declares them integers.\n\n"
        "The habit that follows is the one from o31. Declare a domain only "
        "when every use will agree with it, and when two classes will "
        "share a property, declare the union, which is the next rung's "
        "vocabulary. Or declare nothing, as gist mostly does, and let the "
        "shapes say what the data must look like. The retyping is not a "
        "bug in RDFS. It is RDFS doing exactly what it says, and the "
        "SHACL course's s59, the inference that hides an error, is the "
        "same fact seen from the validator's side.",
    diagram="""
   rdfs:domain, read as a constraint (wrong)       rdfs:domain, read as a rule (right)

   only Bookshops may be locatedIn                 whatever is locatedIn is a Bookshop
   Northwind Press locatedIn Edinburgh => error    Northwind Press locatedIn Edinburgh
                                                     => Northwind Press a Bookshop   (no error, no warning)

   the rule (rdfs2):  p domain C . x p y  =>  x type C

   the fix: a union domain, or none, and a shape for the constraint
""",
    learn=[
        "rdfs:domain and rdfs:range add types. They never reject anything.",
        "Declare a domain only when every use of the property will agree with it. Two classes sharing a property want a union or nothing.",
        "The constraint you meant is a shape. The SHACL course's s59 shows the other half of this lesson.",
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
    tryit="Show Facts. Northwind Press is now a bs:Bookshop. Change the domain to a union of Bookshop and Publisher, press Get All, Show Facts "
          "again: the union is a class with no name, and Northwind is typed with that instead, which is true and useless. Remove the domain.",
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
    why="SKOS is small and complete. Labels: prefLabel, altLabel, "
        "hiddenLabel for misspellings, with the condition S14 that a "
        "concept has at most one preferred label per language. Notes: "
        "definition, scopeNote, example, historyNote, changeNote, "
        "editorialNote, the same set gist recommends for ontologies, which "
        "is not a coincidence. Hierarchy: broader and narrower, and the "
        "transitive versions for queries. Association: skos:related, for "
        "Tartan Noir and Scottish Interest, which are neither above nor "
        "below each other, with the condition S27 that a concept is not "
        "both related and broader to another. Grouping: skos:Collection, "
        "for 'the Welsh-language shelf', a set of concepts that is not "
        "itself a concept. And mapping: exactMatch, closeMatch, broadMatch "
        "to concepts in other schemes.\n\n"
        "The mapping properties are the ones to get right. owl:sameAs says "
        "two IRIs have one referent, and everything true of one becomes "
        "true of the other, in both directions, forever. skos:exactMatch "
        "says two concepts in two schemes can be used interchangeably for "
        "retrieval, which is a smaller and safer claim about two "
        "particulars that remain two. The Trail's crime fiction is closeMatch to Wikidata's crime fiction, which covers film and theatre as well as books; the scopes overlap and differ, which is what closeMatch is for.\n\n"
        "The integrity conditions are checkable, and this lesson's shapes "
        "check the ones that matter: one preferred label per language, "
        "every concept in a scheme, related disjoint from broader, and no "
        "concept its own ancestor. Run on the shipped scheme they report "
        "conformance; on this file, with a seeded cycle and a doubled "
        "label, they report both. The SHACL course's s30 does the cycle "
        "check in the same way.",
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
        "SKOS has six kinds of statement and each has its property. Labels, notes, hierarchy, association, grouping, mapping.",
        "Map between schemes with match properties. owl:sameAs merges referents; exactMatch leaves them two.",
        "The integrity conditions are shapes. Run them in the editor before publishing a scheme, and keep a file that breaks them.",
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
    why="o24 gave the test: promote a concept to a class when the first "
        "axiom about its members is needed. Suppose the website must show "
        "every work of fiction on one page, and works are tagged with the "
        "leaf genre only. A path over the scheme answers it in SPARQL. But "
        "suppose a downstream consumer will only see the closure, or a "
        "shape must target 'every work of fiction'. Then the concept "
        "scheme is a rung too low, and the promotion is mechanical: the "
        "same IRI becomes an owl:Class as well as a skos:Concept, "
        "rdfs:subClassOf is written beside every skos:broader, and works "
        "are typed with the class. The reasoner does the rest. This "
        "lesson's file has three works typed with genres, two of them leaves, and the closure types each with every ancestor.\n\n"
        "This is punning, and OWL 2 DL permits it: the class reading and "
        "the individual reading of bt:genre-crime-fiction are kept apart "
        "by the reasoner, so bs:specialises can still point at the "
        "individual while works are members of the class. The profile "
        "checker confirms the file is DL. The cost is that every genre now "
        "has two readings to maintain, and every change to the shelf plan "
        "is a change to a class hierarchy, with the retyping that implies. "
        "The price of the higher rung is that, and it is why the Trail "
        "does not pay it for genres.\n\n"
        "The set reading makes the promotion exact. The concept was a "
        "particular; the class is the set of works in that genre; broader "
        "between particulars becomes subset between sets; and a work "
        "typed with the leaf is, by inheritance, in every set above it.",
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
        "Promotion is mechanical: add owl:Class, mirror broader with subClassOf, type the members. The reasoner types them with every ancestor.",
        "Punning lets the concept keep its uses while the class gains members. The profile checker confirms it is DL.",
        "The cost is two readings per term and retyping on every rearrangement. Pay it only where an axiom about members is needed.",
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
    why="RDFS has classes, subclasses, properties, subproperties, domains "
        "and ranges, and labels. With those it can say that every "
        "settlement is a place and that whatever is located somewhere is a "
        "shop. It cannot say that nothing is both a place and a shop. It "
        "cannot say that a shop is in one town, that a segment has two "
        "ends, that wrote and author are the same relation in opposite "
        "directions, or that an author is a person who wrote something. "
        "Most of all it cannot be contradicted: assert that one thing is a "
        "Place and a Bookshop, run the RDFS closure, and it types the "
        "thing with both and their superclasses and reports nothing, "
        "because in RDFS there is nothing to report.\n\n"
        "That is not a flaw. A language in which you cannot be wrong is a "
        "language in which data from anywhere merges without argument, "
        "which is what RDFS was for. It means the cost of RDFS is that "
        "the errors it cannot see stay in the data until a query finds "
        "them, and the SPARQL course's module 13 is the collection of "
        "queries that do.\n\n"
        "The list of what was wanted and could not be said is the agenda "
        "for module 07, in order: disjointness first, because it is the "
        "cheapest and catches the most; then restrictions, which say what "
        "a member must have; then defined classes, which let the reasoner "
        "decide membership; then the property characteristics; and last "
        "the datatypes and profiles, which are where the language draws "
        "its own limits.",
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
        "RDFS cannot be contradicted. A thing typed as two disjoint kinds is typed with both, and nothing is reported.",
        "That is the design: data from anywhere merges. The cost is that errors wait for a query.",
        "The list of what RDFS cannot say is the order to learn OWL in. Disjointness first.",
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
