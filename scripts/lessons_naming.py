# -*- coding: utf-8 -*-
"""Module 03 -- Naming: identifiers, local names, labels."""
from ontocat import o, Query
import specs

M = "03-naming"

DECL = """
# Borrowed annotation properties, declared so the file is OWL 2 DL on its own.
skos:prefLabel      a owl:AnnotationProperty .
skos:altLabel       a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
skos:notation       a owl:AnnotationProperty .
"""

o(
    oid="o15", module=M,
    title="An IRI is not a name",
    decides="The IRI identifies and the label names; a shop can be renamed without becoming a different shop, and an IRI may be readable or opaque as long as nothing depends on reading it.",
    corner="symbol",
    why="The Inkwell might well change its name to The Wigtown Inkwell next "
        "year, and if the IRI were the name then every link to the shop "
        "would break and every dataset that mentioned it would need "
        "editing. Because the IRI is bt:shop-inkwell and the name is a "
        "label, the label changes and nothing else does, while the old name "
        "stays on as an altLabel so that a search still finds it. This is "
        "the practical content of the Web Architecture's URI opacity, which "
        "asks that agents infer nothing from the spelling of an IRI, and "
        "from which it follows that nothing should depend on the spelling "
        "staying true.\n\n"
        "People do read IRIs, though, and the two big upper ontologies took "
        "opposite views about that. gist writes gist:Content and "
        "gist:Organization, readable at a glance, while BFO writes "
        "obo:BFO_0000031 for 'generically dependent continuant', a number "
        "that will never go stale because it never said anything in the "
        "first place; gistBFO, the file that maps the one to the other, has "
        "both styles on every line. Neither is wrong. A readable IRI is "
        "kinder to whoever is writing the query and a small liability on "
        "the day the meaning drifts away from the word, whereas an opaque "
        "one puts all the meaning in the label and the definition, where it "
        "can be edited. The OBO Foundry requires the opaque form of its "
        "members and gist requires the readable one, and both of them "
        "forbid changing an IRI once it has been published.\n\n"
        "The Trail's IRIs are readable and lower-case with a type prefix, "
        "as in shop-inkwell, place-wigtown and author-rhona-blackwood, and "
        "o20 compares that with gist's convention. What matters here is "
        "only that the reader can tell which of the three things on the "
        "screen is which: the IRI identifies, the label names, and the "
        "comment carries the meaning.",
    diagram="""
   the shop is renamed                     the IRI                  the label

   before                                  bt:shop-inkwell          "The Inkwell"@en
   after                                   bt:shop-inkwell          "The Wigtown Inkwell"@en
                                                                    altLabel "The Inkwell"@en
   every link still works; the search still finds the old name

   readable                                opaque
   gist:Content                            obo:BFO_0000031
   the meaning is in the IRI and the       the meaning is in the label
   label; drift is a small liability       and definition only; drift is free
""",
    learn=[
        "The IRI identifies and the label names, so a rename is a change of label, with the old one kept as an alternative.",
        "Opacity is a rule for machines, which should infer nothing from the spelling, and it is also advice for modellers, who should depend on nothing in it.",
        "Readable and opaque IRIs are both respectable; pick one convention, and never change an IRI once it is published.",
    ],
    tryit="In the SPARQL panel, ask for every label of bt:shop-inkwell, then "
          "change the prefLabel in the editor, press Get All and ask again: "
          "the IRI in the answer has not moved.",
    body=DECL + """
bt:shop-inkwell
    a               bs:Bookshop ;
    skos:prefLabel  "The Wigtown Inkwell"@en ;
    skos:altLabel   "The Inkwell"@en ;
    skos:definition "The crime fiction shop on Wigtown's main street, opened in 1979. Renamed in 2026; the IRI did not change."@en .

bs:Bookshop
    a               owl:Class ;
    skos:prefLabel  "Bookshop"@en .

# The two styles side by side, as gistBFO has them.
gist:Content
    a                owl:Class ;
    skos:prefLabel   "Content"@en ;
    rdfs:subClassOf  obo:BFO_0000031 .

obo:BFO_0000031
    a               owl:Class ;
    skos:prefLabel  "generically dependent continuant"@en .
""",
    queries=[Query("Every name of the shop, with the IRI beside it", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?shop ?name WHERE { ?shop skos:prefLabel|skos:altLabel ?name . FILTER(CONTAINS(STR(?shop), "/shop-")) }""", rows=2)],
    check=dict(profile=True),
    expect=dict(dl=True),
)
specs.register("o15", "webarchOpacity", "oboUris")

o(
    oid="o16", module=M,
    title="Namespaces: one for the vocabulary, one for the data",
    decides="The schema lives in a hash namespace and the data in a slash namespace, the ontology IRI is not the namespace IRI, and both are declared on the ontology node.",
    corner="symbol",
    why="A namespace is a prefix that an owner mints names under, and the "
        "Trail has two of them: https://example.org/bookshop-trail/schema# "
        "for the classes and properties, and https://example.org/bookshop- "
        "trail/ for the particulars. gist has three, and its Namespace "
        "document explains why, which is that ontology terms, taxonomy "
        "terms and instance data change at different rates and are governed "
        "by different people, so that a namespace is really a unit of "
        "governance.\n\n"
        "Hash or slash is the other choice to make. With a hash, everything "
        "after the # is a fragment, so a browser asking for bs:Bookshop "
        "fetches the whole schema document and finds the term inside it, "
        "which suits a vocabulary of a few hundred terms that is read as a "
        "whole; with a slash, each IRI can be served on its own, which "
        "suits thirty-three shops and will still suit thirty thousand. Cool "
        "URIs for the Semantic Web sets the two out and, sensibly enough, "
        "declines to pick one for every case.\n\n"
        "The ontology's own IRI, https://example.org/bookshop-trail/schema "
        "without the hash, names the document rather than the namespace, "
        "and the Ontology Quality Suite's QUA-006 fires when the two are "
        "conflated, because a term whose IRI is the ontology IRI and "
        "nothing more cannot be told apart from the ontology. The vann "
        "vocabulary then gives us somewhere to write the preferred prefix "
        "and namespace on the ontology node, so that tools and people can "
        "agree on 'bs:' without having to be told.",
    diagram="""
   https://example.org/bookshop-trail/schema        the ontology IRI: the document
   https://example.org/bookshop-trail/schema#       the schema namespace   (hash)   bs:
   https://example.org/bookshop-trail/              the data namespace     (slash)  bt:

   bs:Bookshop   = schema# + Bookshop     fetch the document, find the fragment
   bt:shop-inkwell = / + shop-inkwell     fetch the one resource

   gist's three:   .../ns/ontology/gist/   .../ns/taxonomy/gist/   .../ns/data/gist/
   a namespace is a unit of governance
""",
    learn=[
        "Keep vocabulary and data in different namespaces, because the two are governed and versioned differently.",
        "Hash for a vocabulary that is read as a document, slash for data that is served a resource at a time.",
        "The ontology IRI names the document and is not the namespace, so declare the prefix and the namespace on the ontology node with vann.",
    ],
    body=DECL + """
vann:preferredNamespacePrefix  a owl:AnnotationProperty .
vann:preferredNamespaceUri     a owl:AnnotationProperty .
dct:title                      a owl:AnnotationProperty .

<https://example.org/bookshop-trail/schema>
    a                              owl:Ontology ;
    dct:title                      "The Bookshop Trail schema"@en ;
    vann:preferredNamespacePrefix  "bs" ;
    vann:preferredNamespaceUri     "https://example.org/bookshop-trail/schema#" ;
    skos:editorialNote             "Instance data is minted under https://example.org/bookshop-trail/ with the prefix bt. The two are governed separately."@en .

bs:Bookshop
    a               owl:Class ;
    skos:prefLabel  "Bookshop"@en .

bt:shop-inkwell
    a               bs:Bookshop ;
    skos:prefLabel  "The Inkwell"@en .
""",
    check=dict(profile=True, oqs="checks"),
    expect=dict(dl=True, oqs_not=["QUA-006", "QUA-005"]),
)
specs.register("o16", "gistNamespaces", "coolChoosing")

o(
    oid="o17", module=M,
    title="Local names",
    decides="Classes are UpperCamelCase, properties lowerCamelCase, letters and digits only, acronyms camel-cased, no home-made abbreviations; a draft that breaks each rule is corrected.",
    corner="symbol",
    why="The gist style guide's orthographic rules fit on a card. Classes "
        "start with a capital and properties with a lower-case letter, both "
        "of them camel-cased; only letters and digits are allowed, so "
        "Isbn10 rather than ISBN-10, because a hyphen ends a prefixed name "
        "in Turtle and an underscore is a word boundary nobody ever agreed "
        "on; acronyms are camel-cased too, so that word boundaries stay "
        "unambiguous, giving UriScheme rather than URIScheme, with ID as "
        "the one exception because the dictionary spells it that way; and "
        "there are to be no abbreviations of your own devising, so "
        "hasUnitOfMeasure rather than hasUoM, since the person reading the "
        "query in five years was not in the room when you invented it.\n\n"
        "None of this is arbitrary, and none of it is about taste. A "
        "convention that every term follows is a convention a tool can "
        "check, and a tool that checks it is what stops the one hyphenated "
        "name from turning up in production. The Ontology Quality Suite's "
        "STY-001 and STY-002 check exactly these two rules, and this file "
        "is written to make them fire.\n\n"
        "What the file holds is the committee's draft, with four names that "
        "break a rule each, set beside the corrected forms. The audit "
        "counts three of them, because noOfStaff is perfectly good "
        "lowerCamelCase and no pattern can tell an abbreviation from a "
        "word; that one is caught by a reader, or by a list of forbidden "
        "abbreviations, which is how gist handles it. The corrected names "
        "are the Trail's real ones.",
    diagram="""
   rule                                    draft             corrected

   classes UpperCamelCase                  bs:Book_shop      bs:Bookshop
   properties lowerCamelCase               bs:StaffCount     bs:staffCount
   letters and digits only                 bs:ISBN13         bs:isbn13  (and camel-case the acronym)
   no home-made abbreviations              bs:noOfStaff      bs:staffCount
                                           bs:hasUoM         bs:hasUnitOfMeasure

   a convention every term follows is a convention a tool can check
""",
    learn=[
        "UpperCamelCase for classes, lowerCamelCase for properties, letters and digits only: four rules, with no exceptions worth having.",
        "Camel-case the acronyms too, so that word boundaries stay unambiguous, as in Isbn13 and UriScheme; ID is the one exception the dictionary allows.",
        "Never abbreviate on your own account, because the reader in five years was not in the room and no regular expression will catch it for you.",
    ],
    body=DECL + """
# The draft, kept so the audit can count it.
bs:Book_shop   a owl:Class ;            skos:prefLabel "Book shop"@en ;      skos:editorialNote "Underscore; and the two words are one."@en .
bs:StaffCount  a owl:DatatypeProperty ; skos:prefLabel "staff count"@en ;    skos:editorialNote "A property with a capital."@en .
bs:ISBN13      a owl:DatatypeProperty ; skos:prefLabel "ISBN-13"@en ;        skos:editorialNote "An acronym in capitals; the word boundary is lost."@en .
bs:noOfStaff   a owl:DatatypeProperty ; skos:prefLabel "no. of staff"@en ;   skos:editorialNote "An abbreviation nobody agreed."@en .

# The corrected names: the Trail's own.
bs:Bookshop    a owl:Class ;            skos:prefLabel "Bookshop"@en .
bs:staffCount  a owl:DatatypeProperty ; skos:prefLabel "staff count"@en .
bs:isbn        a owl:DatatypeProperty ; skos:prefLabel "ISBN"@en ;
    skos:editorialNote "The Trail calls it isbn rather than isbn13, since every ISBN in the data is thirteen digits. gist would say Isbn13 for a class."@en .
""",
    check=dict(profile=True, names=True, oqs="checks"),
    expect=dict(dl=True, names_bad=3, oqs=["STY-001", "STY-002"]),
)
specs.register("o17", "gistLocalNames", "oboNaming")

o(
    oid="o18", module=M,
    title="Naming a property so that it reads",
    decides="Object properties are verb-initial and read as a sentence, datatype properties are nouns, direction is unambiguous and runs up the tree; the Trail's departures from that are listed rather than hidden.",
    corner="symbol",
    why="A property name is read in the middle of a triple, so the test is "
        "simply whether the triple reads. 'The Inkwell isLocatedIn Wigtown' "
        "reads, 'The Inkwell locatedIn Wigtown' very nearly does, and 'The "
        "Inkwell location Wigtown' does not. The gist guide's textual "
        "standards come down to that test and a handful of tie-breakers: "
        "object properties verb-initial, so isAbout rather than about; the "
        "'is' prefix on -ed forms, as in isGovernedBy; an ordinary verb in "
        "preference to hasX, so precedes rather than isFollowedBy; datatype "
        "properties as nouns, so baseConversionFactor rather than "
        "convertToBase; the present tense; and a final preposition where it "
        "helps, as in hasJurisdictionOver.\n\n"
        "Two of the rules are about direction. Make it unambiguous, so "
        "hasBroader rather than broader, which SKOS itself gets wrong by "
        "this standard; and where there is a hierarchy, name the property "
        "going up it, from child to parent, because that is the direction "
        "with fewer results, which gives isPartOf rather than hasPart and "
        "hasSuperCategory rather than hasSubCategory. That last rule is "
        "what lets gist do without inverses altogether, as o31 comes to.\n\n"
        "The Trail's vocabulary was written before these rules were adopted "
        "here and departs from them in four places, since locatedIn, "
        "publishedBy, author and genre would be isLocatedIn, isPublishedBy, "
        "hasAuthor and hasGenre; the departures are recorded on each "
        "property as an editorial note. Renaming them would break 145 "
        "queries in the SPARQL course for a gain in consistency, and that "
        "trade is discussed under pragmatism in o30. The point here is that "
        "the departure is written down.",
    diagram="""
   test: does the triple read as a sentence?

   bt:shop-inkwell   bs:locatedIn     bt:place-wigtown     nearly; gist: isLocatedIn
   bt:book-x         bs:publishedBy   bt:pub-bell-rock     nearly; gist: isPublishedBy
   bt:book-x         bs:author        bt:author-y          no;     gist: hasAuthor
   bt:pub-northwind  bs:imprintOf     bt:pub-lodestone     yes, and up the tree
   bt:shop-a         bs:connectsTo    bt:shop-b            yes

   datatype properties are nouns:  bs:floorArea  bs:staffCount  bs:founded
""",
    learn=[
        "Read the triple aloud, and if it is not a sentence then rename the property.",
        "Name a hierarchical property going up, as in isPartOf, isMemberOf and hasBroader: one direction, fewer results, and no inverse needed.",
        "Where an ontology departs from its own rules, say so on the term, because a recorded departure is a decision and a silent one is drift.",
    ],
    body=DECL + """
bs:locatedIn    a owl:ObjectProperty ; skos:prefLabel "located in"@en ;
    skos:editorialNote "gist style would be isLocatedIn. Kept for the queries that use it."@en .
bs:publishedBy  a owl:ObjectProperty ; skos:prefLabel "published by"@en ;
    skos:editorialNote "gist style would be isPublishedBy."@en .
bs:author       a owl:ObjectProperty ; skos:prefLabel "author"@en ;
    skos:editorialNote "gist style would be hasAuthor: a noun does not read in the middle of a triple."@en .
bs:genre        a owl:ObjectProperty ; skos:prefLabel "genre"@en ;
    skos:editorialNote "gist style would be hasGenre, or isCategorizedBy."@en .
bs:imprintOf    a owl:ObjectProperty ; skos:prefLabel "imprint of"@en ;
    skos:editorialNote "Reads, and runs up the tree: child to parent."@en .
bs:connectsTo   a owl:ObjectProperty ; skos:prefLabel "connects to"@en .
bs:floorArea    a owl:DatatypeProperty ; skos:prefLabel "floor area"@en .
bs:staffCount   a owl:DatatypeProperty ; skos:prefLabel "staff count"@en .
""",
    queries=[Query("Properties whose name departs from the gist standard", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?property ?note WHERE { ?property skos:editorialNote ?note . FILTER(CONTAINS(?note, "gist style would be")) }""", rows=4)],
    check=dict(profile=True, names=True),
    expect=dict(dl=True, names_bad=0),
)
specs.register("o18", "gistPropertyNames", "gistInverses")

TITLE_CASE_SHAPES = """
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix bt:   <https://example.org/bookshop-trail/> .

# The label rules as shapes, after gist's own validation/shapes/ontologyShapes.ttl.
bt:ClassLabelShape
    a               sh:NodeShape ;
    sh:targetClass  owl:Class ;
    sh:property [
        sh:path        skos:prefLabel ;
        sh:minCount    1 ;
        sh:uniqueLang  true ;
        sh:message     "A class has exactly one preferred label per language." ;
    ] ;
    sh:property [
        sh:path     skos:prefLabel ;
        sh:pattern  "^([A-Z]([a-z]+|[A-Z]+)|[0-9]+)([ -]([A-Z]([a-z]+|[A-Z]+)|[0-9]+|a|an|the|and|but|or|nor|for|so|yet|as|at|by|in|of|off|on|out|per|to|up|via))*$" ;
        sh:message  "A class label is in title case: {$value}" ;
    ] .

bt:PropertyLabelShape
    a               sh:NodeShape ;
    sh:targetClass  owl:ObjectProperty, owl:DatatypeProperty ;
    sh:property [
        sh:path     skos:prefLabel ;
        sh:pattern  "^([a-z]+|[A-Z][A-Z]+)([- ]([a-z]+|[A-Z][A-Z]+|[0-9]+))*$" ;
        sh:message  "A property label is lower case, acronyms excepted: {$value}" ;
    ] .
"""

o(
    oid="o19", module=M,
    title="Labels: one per language, in the right case",
    decides="Every term has exactly one skos:prefLabel per language, classes in title case and properties in lower case, alternatives in skos:altLabel; the rules are shapes, and they run in the editor.",
    corner="symbol",
    why="A preferred label is the one name a term shows in a list, and a "
        "list with two names for one thing is a list with a bug in it, "
        "which is why SKOS makes it an integrity condition, S14: at most "
        "one preferred label per language tag. gist asks for exactly one, "
        "and adds cases, with title case for classes, as in Physical "
        "Identifiable Item, lower case for properties, as in has unit of "
        "measure, and acronyms in capitals in either. Alternative labels "
        "are free-form and as plural as you please, which is what they are "
        "for.\n\n"
        "gist enforces its label rules with SHACL shapes run on every "
        "commit, and the escape hatch for a label that is right and non- "
        "conforming, a proper noun say, is an annotation, "
        "gist:nonConformingLabel true, that the shape reads and respects. "
        "The same shapes, simplified, are in this lesson and in the editor: "
        "open them in a second tab, pick them in the Shapes dropdown and "
        "press Validate. Two of the labels here are wrong on purpose and "
        "the report names them. This is the SHACL course's whole method "
        "applied to a vocabulary instead of to data, and the file is one "
        "you could run against any ontology somebody hands you.\n\n"
        "Language tags are the other half of it. The Trail labels places in "
        "Welsh and Gaelic where those names exist, and a query for @cy "
        "labels is what the Welsh page of the website will run; a label "
        "with no tag at all is a label in no language, and STY-003 in the "
        "Quality Suite says so, as an Info.",
    diagram="""
   term             prefLabel                          rule

   bs:Bookshop      "Bookshop"@en                      title case, one per language
   bs:Settlement    "Settlement"@en  "Anheddiad"@cy    two languages, one each
   bs:floorArea     "floor area"@en                    lower case
   bs:isbn          "ISBN"@en                          acronym in capitals, allowed

   seeded:  bs:Publisher  "publisher"@en               not title case      -> a violation
            bs:heldAt     "Held at"@en                 not lower case      -> a violation
            bs:Region     "Region"@en  "Rhanbarth"@cy  fine
""",
    learn=[
        "One preferred label per language, with altLabels for everything else, and SKOS S14 makes the first of those a hard rule.",
        "Title case for classes, lower case for properties, acronyms in capitals, and gist's shapes check it, which the editor will run for you.",
        "A label with no language tag is a label in no language, so tag every one of them.",
    ],
    body=DECL + """
bs:Bookshop    a owl:Class ;            skos:prefLabel "Bookshop"@en ;    skos:altLabel "Shop"@en, "Store"@en .
bs:Settlement  a owl:Class ;            skos:prefLabel "Settlement"@en, "Anheddiad"@cy .
bs:Region      a owl:Class ;            skos:prefLabel "Region"@en, "Rhanbarth"@cy .
bs:floorArea   a owl:DatatypeProperty ; skos:prefLabel "floor area"@en .
bs:isbn        a owl:DatatypeProperty ; skos:prefLabel "ISBN"@en .

# Two labels wrong on purpose, for the shapes to find.
bs:Publisher   a owl:Class ;            skos:prefLabel "publisher"@en .
bs:heldAt      a owl:ObjectProperty ;   skos:prefLabel "Held at"@en .
""",
    check=dict(profile=True, shacl=TITLE_CASE_SHAPES),
    companions={"label-shapes.ttl": TITLE_CASE_SHAPES},
    shapes="label-shapes.ttl",
    expect=dict(dl=True, shacl_conforms=False, shacl_violations=2),
    notes="The shapes are in label-shapes.ttl beside this lesson, and Open in the editor opens them in a second tab already selected; press Validate. The SHACL course's s16 covers sh:uniqueLang and s15 sh:pattern.",
)
specs.register("o19", "gistLabels", "skosS14")

o(
    oid="o20", module=M,
    title="Naming the particulars",
    decides="Instance IRIs carry a type infix and a slug, never a role, and are minted once; the Trail's shop-inkwell and gist's _Bookshop_The_Inkwell are the same rule in two spellings.",
    corner="symbol",
    why="The Trail names its particulars with a lower-case type and a slug, "
        "as in shop-inkwell, place-wigtown, author-rhona-blackwood and "
        "event-inkwell-2025-03-08, while gist's convention is a leading "
        "underscore, the type, an underscore, and then the name with its "
        "case kept, giving _Bookshop_The_Inkwell. The spelling differs and "
        "the rule is the same, and it is the rule from module 02: the infix "
        "is the most specific rigid class the instance belongs to, and "
        "never a role, because the role may end and the IRI may not.\n\n"
        "The Trail breaks its own rule exactly once, and the break is worth "
        "looking at. Authors are named author-rhona-blackwood, and Author "
        "is a role; gist's guide would have _Person_Rhona_Blackwood. The "
        "Trail's defence is that its Person class exists only to have "
        "authors in it, so that the role never ends within the dataset, "
        "which is a pragmatic argument, openly made, and the editorial note "
        "records it.\n\n"
        "gist's guide allows a fallback as well, which is that when the "
        "data being mapped does not say which specific kind a row is, you "
        "use a higher class as the infix for the whole table, "
        "_Organization_ rather than guessing between corporations and "
        "charities. That is the same rule applied with a little humility, "
        "and it is better than an infix that is wrong for a third of the "
        "rows.",
    diagram="""
   the Trail                        gist                              the rule

   bt:shop-inkwell                  gistd:_Bookshop_The_Inkwell       most specific rigid class + name
   bt:place-wigtown                 gistd:_Settlement_Wigtown
   bt:author-rhona-blackwood        gistd:_Person_Rhona_Blackwood     never a role (Author is one)
   bt:event-inkwell-2025-03-08      gistd:_Event_...                  a slug that will not change

   fallback when the kind is not known from the data: the nearest rigid class
""",
    learn=[
        "Infix the most specific rigid class, since it is the one thing about the instance that will not change.",
        "Never name an instance after a role; the Trail does exactly that for its authors, and says why on the class.",
        "When the source data cannot tell you the kind, use a higher one for the whole table rather than guess row by row.",
    ],
    body=DECL + """
bs:Person  a owl:Class ; skos:prefLabel "Person"@en .
bs:Author  a owl:Class ; rdfs:subClassOf bs:Person ; skos:prefLabel "Author"@en ;
    skos:editorialNote "Instances are minted as author-<name>, against the rule that an infix is a rigid class. Person exists in the Trail only to hold authors, so the role never ends inside the dataset. Mint under person- the day a non-author person appears."@en .

bt:author-rhona-blackwood  a bs:Author, bs:Person ; skos:prefLabel "Rhona Blackwood"@en .
bt:shop-inkwell            a bs:Bookshop ;          skos:prefLabel "The Inkwell"@en .
bt:place-wigtown           a bs:Settlement ;        skos:prefLabel "Wigtown"@en .
bs:Bookshop    a owl:Class ; skos:prefLabel "Bookshop"@en .
bs:Settlement  a owl:Class ; skos:prefLabel "Settlement"@en .

# The same three, as gist would mint them.
gistd:_Person_Rhona_Blackwood  a bs:Person ;     skos:prefLabel "Rhona Blackwood"@en ; owl:sameAs bt:author-rhona-blackwood .
gistd:_Bookshop_The_Inkwell    a bs:Bookshop ;   skos:prefLabel "The Inkwell"@en ;     owl:sameAs bt:shop-inkwell .
gistd:_Settlement_Wigtown      a bs:Settlement ; skos:prefLabel "Wigtown"@en ;         owl:sameAs bt:place-wigtown .
""",
    queries=[Query("Instances whose IRI names a role", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
SELECT DISTINCT ?instance WHERE { ?instance a ?class . FILTER(CONTAINS(STR(?instance), "/author-")) }""", rows=1)],
    check=dict(profile=True, reason=True),
    expect=dict(dl=True, consistent=True),
)
specs.register("o20", "gistInstanceNames", "gistNsDoc")
