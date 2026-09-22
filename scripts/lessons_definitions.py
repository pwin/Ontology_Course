# -*- coding: utf-8 -*-
"""Module 04 -- Definitions and controlled vocabularies."""
from ontocat import o, Query
import specs

M = "04-definitions"

DECL = """
# Borrowed annotation properties, declared so the file is OWL 2 DL on its own.
skos:prefLabel      a owl:AnnotationProperty .
skos:altLabel       a owl:AnnotationProperty .
skos:hiddenLabel    a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:scopeNote      a owl:AnnotationProperty .
skos:example        a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
skos:historyNote    a owl:AnnotationProperty .
skos:changeNote     a owl:AnnotationProperty .
skos:notation       a owl:AnnotationProperty .
dct:source          a owl:AnnotationProperty .
dct:isReplacedBy    a owl:AnnotationProperty .
"""

o(
    oid="o21", module=M,
    title="A definition is not a label",
    decides="Every class and property gets a definition in the form 'a genus that differs thus', one sentence, and anything else that was in the comment moves to a scope note.",
    corner="thought",
    why="A label is a symbol. A definition is the thought written down, and "
        "it has a shape that has served since Aristotle: name the nearest "
        "kind the thing belongs to, then say what distinguishes it from the "
        "other things of that kind. 'A Settlement is a Place that is a town "
        "or city.' Genus, Place; differentia, town or city. Someone who has "
        "never seen the data can now decide whether a given thing is one, "
        "which is the whole test of a definition. OBO Foundry principle "
        "FP-006 asks for exactly this form, and for a definition on most "
        "classes as a condition of membership; gist's guide asks for exactly "
        "one, as a full sentence ending in a period, subject optional.\n\n"
        "The Trail's shipped comments are a mixture. 'A town or city' is a "
        "definition. 'The only kind of Place a bookshop sits in' is true and "
        "useful and is not one; it is a note about how the term is used. "
        "SKOS gives the two their own properties, skos:definition and "
        "skos:scopeNote, and keeping them apart is what stops a definition "
        "growing into a paragraph nobody reads. Examples go in skos:example, "
        "including negative ones: gist's LivingThing gives 'unicorns or "
        "Mickey Mouse' as what it is not.\n\n"
        "The audit in this lesson is rough and deliberate. It flags a "
        "definition whose first sentence contains the term's own name, which "
        "catches circularity (o22) and nothing subtler. It finds none here.",
    diagram="""
   "A Settlement is a Place that is a town or city."
                      -----       -----------------
                      genus       differentia

   skos:definition   one sentence, genus and differentia, ends with a period
   skos:scopeNote    how the term is used, what it does not cover
   skos:example      instances, and negative examples
   skos:prefLabel    the symbol; never a substitute for the sentence
""",
    learn=[
        "Genus and differentia: the nearest kind, then what distinguishes. One sentence.",
        "A definition decides membership for someone who has never seen the data. If it cannot, it is a note.",
        "Definition, scope note and example are three properties because they are three jobs.",
    ],
    body=DECL + """
bs:Place
    a                owl:Class ;
    skos:prefLabel   "Place"@en ;
    skos:definition  "A named area or point on the map, at any scale."@en ;
    skos:scopeNote   "Covers settlements, council areas, regions and countries. A shop's premises are not a Place; the shop is located in one."@en ;
    skos:example     "Wigtown; Dumfries and Galloway; Yorkshire; Wales."@en .

bs:Settlement
    a                owl:Class ;
    rdfs:subClassOf  bs:Place ;
    skos:prefLabel   "Settlement"@en ;
    skos:definition  "A Place that is a town or city."@en ;
    skos:scopeNote   "The only kind of Place a bookshop is located in."@en ;
    skos:example     "Wigtown, Hay-on-Wye, Sedbergh; negative examples: Scotland, the Lake District."@en .

bs:TrailSegment
    a                owl:Class ;
    skos:prefLabel   "Trail Segment"@en ;
    skos:definition  "A walking route between two bookshops, with a length."@en ;
    skos:scopeNote   "Asserted once per pair; walkable in either direction."@en .

bs:locatedIn
    a                owl:ObjectProperty ;
    skos:prefLabel   "located in"@en ;
    skos:definition  "Relates a shop or publisher to the settlement it trades in."@en .
""",
    check=dict(profile=True, definitions=True),
    expect=dict(dl=True, circular=0),
)
specs.register("o21", "oboDefinitions", "gistAnnotationFormat")

o(
    oid="o22", module=M,
    title="How a definition fails",
    decides="Five failing definitions from the draft are named for what they are, circular, too broad, by example, negative and by IRI, and each is rewritten.",
    corner="thought",
    why="Circular: 'A publisher is an organisation that publishes.' The "
        "reader who did not know what publishing was is no further on. "
        "Too broad: 'An event is something that happens.' True of a "
        "sneeze. By example only: 'Genre: crime, poetry, nature writing and "
        "so on.' The list is not the meaning, and 'and so on' is where the "
        "next disagreement lives. Negative: 'A bookshop is a business that "
        "is not a publisher.' Says what it is not, which leaves everything "
        "else. By IRI: 'The class bs:Bookshop.' A definition that could only "
        "be read by someone who already had the ontology open.\n\n"
        "Each has a repair and it is the same repair: find the genus, find "
        "the differentia, write one sentence. 'A publisher is an "
        "organisation that issues works for sale under its own name.' 'An "
        "event is an occasion held at a bookshop on a given day, open to "
        "the public.' 'A genre is a category of works by their subject and "
        "manner, used to shelve books and to describe what a shop is known "
        "for.'\n\n"
        "The audit catches three by looking for the term's own stem in the "
        "first sentence: the two circular ones, and the one by IRI, which "
        "is circular in the plainest way, since it names the term. The "
        "other two need a reader, and "
        "the SemOps Manual's point about cognitive budget applies: a "
        "definition is read by many people once each, so a minute spent on "
        "it is repaid many times, and a definition that makes the reader do "
        "the work is a cost paid by everyone.",
    diagram="""
   failure          draft                                           repair

   circular         a publisher is an organisation that publishes    ... that issues works for sale under its own name
   too broad        an event is something that happens               ... an occasion held at a bookshop on a given day
   by example       genre: crime, poetry, and so on                  ... a category of works by subject and manner
   negative         a bookshop is a business that is not a publisher ... a business that sells books from premises
   by IRI           the class bs:Bookshop                            (the same)

   the audit finds three (circular twice, and by IRI); a reader finds the rest
""",
    learn=[
        "The reader who does not already know must be able to decide membership from the sentence. Every failure here breaks that.",
        "Circularity is mechanical to find and common. Too broad and by example are commoner and need a reader.",
        "A definition is read many times by many people. It is the cheapest place to spend a careful minute.",
    ],
    body=DECL + """
# The draft, kept so the audit can find its circular members.
bs:Publisher  a owl:Class ; skos:prefLabel "Publisher"@en ;
    skos:definition "An organisation that publishes books."@en ;
    skos:editorialNote "Circular. Repair: an organisation that issues works for sale under its own name."@en .
bs:Event      a owl:Class ; skos:prefLabel "Event"@en ;
    skos:definition "Something that happens at an event venue."@en ;
    skos:editorialNote "Circular and too broad. Repair: an occasion held at a bookshop on a given day, open to the public."@en .
bs:Genre      a owl:Class ; skos:prefLabel "Genre"@en ;
    skos:definition "Crime, poetry, nature writing, history and so on."@en ;
    skos:editorialNote "By example only. Repair: a category of works by subject and manner, used to shelve books and to describe what a shop is known for."@en .
bs:Bookshop   a owl:Class ; skos:prefLabel "Bookshop"@en ;
    skos:definition "A business that is not a publisher."@en ;
    skos:editorialNote "Negative. Repair: a business that sells books to the public from premises."@en .
bs:Source     a owl:Class ; skos:prefLabel "Source"@en ;
    skos:definition "The class bs:Source."@en ;
    skos:editorialNote "By IRI. Repair: a document or organisation that makes claims about shops, such as a guidebook, a survey or a register."@en .
""",
    check=dict(profile=True, definitions=True),
    expect=dict(dl=True, circular=3),
)
specs.register("o22", "oboDefinitions", "semopsBudget")

ANNOTATION_SHAPES = """
@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix bt:   <https://example.org/bookshop-trail/> .

# gist's annotation cardinalities as shapes: exactly one preferred label per
# language (gist's own shape says one, because gist is in one language),
# exactly one definition.
bt:AnnotatedTermShape
    a               sh:NodeShape ;
    sh:targetClass  owl:Class, owl:ObjectProperty, owl:DatatypeProperty ;
    sh:property [ sh:path skos:prefLabel ;  sh:minCount 1 ; sh:uniqueLang true ; sh:message "Exactly one preferred label per language." ] ;
    sh:property [ sh:path skos:definition ; sh:minCount 1 ; sh:maxCount 1 ; sh:message "Exactly one definition." ] .
"""

o(
    oid="o23", module=M,
    title="The annotation set",
    decides="Each term carries prefLabel and definition exactly once, scopeNote and example where they help, editorialNote for the maintainers, and never rdfs:comment as a dumping ground.",
    corner="thought",
    why="gist's guide sorts the annotations into required, recommended, use "
        "where relevant, use rarely, and do not use, and the sorting is more "
        "useful than any single rule. Required: skos:prefLabel and "
        "skos:definition, exactly one each. Recommended: skos:scopeNote and "
        "skos:example. Where relevant: skos:altLabel and skos:editorialNote, "
        "the last being for the maintainers rather than the users. Rarely: "
        "skos:changeNote and skos:historyNote, because the version control "
        "system usually has that. Do not use: rdfs:label and rdfs:comment, "
        "because SKOS gives a finer set and a comment becomes the place "
        "everything goes.\n\n"
        "The Trail's shipped vocabulary uses rdfs:label and rdfs:comment, "
        "and its comments carry definitions, usage notes and provenance in "
        "one string. That was a reasonable choice for a teaching dataset "
        "whose queries wanted one property to read, and it is exactly the "
        "case the guide warns about. This lesson shows bs:Bookshop with the "
        "full set, beside a term with the minimum missing, and the shapes "
        "find the gap. The Quality Suite's QUA-010 fires for the same "
        "reason.\n\n"
        "Cardinality is the rule that pays. One label per language and one "
        "definition per term means a tool can pick the label and print the "
        "definition without deciding between candidates, and a reader never "
        "wonders which of two sentences is current.",
    diagram="""
   required           skos:prefLabel     exactly one per language
                      skos:definition    exactly one
   recommended        skos:scopeNote     usage, boundaries
                      skos:example       instances, negative examples
   where relevant     skos:altLabel      any number
                      skos:editorialNote for the maintainers
   rarely             skos:changeNote, skos:historyNote
   do not use         rdfs:label, rdfs:comment   (the Trail does; o30 says why)
""",
    learn=[
        "Two annotations are required and have a cardinality of one. Everything else is optional and plural.",
        "An editorial note is for whoever maintains the term; a scope note is for whoever uses it. Different readers, different property.",
        "rdfs:comment is where everything ends up if nothing else is provided. Provide something else.",
    ],
    body=DECL + """
bs:Bookshop
    a                   owl:Class ;
    skos:prefLabel      "Bookshop"@en, "Siop Lyfrau"@cy ;
    skos:altLabel       "Shop"@en, "Store"@en ;
    skos:definition     "A business that sells books to the public from premises."@en ;
    skos:scopeNote      "The business, not the building. A shop that moves premises keeps its identity; a building that changes hands does not become the new tenant."@en ;
    skos:example        "The Inkwell; Marginalia. Negative examples: a publisher's warehouse; an online-only seller."@en ;
    skos:editorialNote  "Definition agreed 12 March 2025. Chains are out of scope; revisit if one joins the trail."@en ;
    rdfs:seeAlso        <https://en.wikipedia.org/wiki/Bookselling> .

# The minimum missing, for the shapes to find.
bs:Series
    a                   owl:Class ;
    skos:prefLabel      "Series"@en .
""",
    check=dict(profile=True, shacl=ANNOTATION_SHAPES, oqs="checks"),
    companions={"annotation-shapes.ttl": ANNOTATION_SHAPES},
    shapes="annotation-shapes.ttl",
    expect=dict(dl=True, shacl_conforms=False, shacl_violations=1, oqs=["QUA-010"]),
)
specs.register("o23", "gistAnnotations", "gistAnnotationCard")

o(
    oid="o24", module=M,
    title="Class or category: when a concept becomes a class",
    decides="A genre stays a concept, a particular that a work belongs to and a shop specialises in, and is promoted to a class only when something must be said about its members as a set.",
    corner="referent",
    why="Every ontology has things that could be a class or an individual, "
        "and the choice is the most consequential one it makes. Crime "
        "fiction is the Trail's case. As a class, bs:CrimeFiction is a set "
        "of works: every crime novel is a member, and anything true of the "
        "set, that its members have a detective say, can be written as an "
        "axiom and inherited. As a particular, bt:genre-crime-fiction is a "
        "thing in its own right, with a Welsh label, a broader concept, a "
        "scope note, and, decisively, the property of being what The "
        "Inkwell specialises in. A shop cannot specialise in a set of "
        "works by being a member of it.\n\n"
        "The test is set-theoretic. Do you need to say things about the "
        "members, as a set, that a reasoner should apply to each? Then it "
        "is a class, and rdfs:subClassOf is subset. Do you need to say "
        "things about the category itself, point other kinds of thing at "
        "it, arrange it in a hierarchy that curators will rearrange, or "
        "carry a few thousand of them? Then it is a concept or a category, "
        "and skos:broader is a relation between two particulars that "
        "promises nothing about members. gist says it outright in the scope note on gist:Category: use a category 'if you don't care much "
        "about the formal structure of the different types, or if there is "
        "a whole hierarchy of them'.\n\n"
        "The promotion happens when the first axiom about members is "
        "needed. OWL 2 allows both at once by punning: one IRI that is an "
        "owl:Class and a skos:Concept, with rdfs:subClassOf and skos:broader "
        "running in parallel. It costs a second reading of every term and "
        "it is the right answer for a vocabulary that is both a shelf plan "
        "and a reasoning target. The Trail needs only the shelf plan, so it "
        "stops at the concept, and the query at the end shows the cost of "
        "the other choice: as a class, the shop's specialism has nowhere to "
        "point.",
    diagram="""
   as a concept (a particular)                 as a class (a set)

   bt:genre-crime-fiction                      bs:CrimeFiction
     a skos:Concept                              a owl:Class ; rdfs:subClassOf bs:Work
     skos:broader bt:genre-fiction               members: every crime novel
     skos:prefLabel "Crime Fiction"@en           axioms about members are inherited
     <- bt:shop-inkwell bs:specialises           <- a shop cannot be a member of it
     <- bt:book-x bs:genre

   promote when the first axiom about the members is needed
   both at once: punning, subClassOf and broader in parallel
""",
    learn=[
        "A class is a set you need to say things about. A concept is a thing you need to point at. Ask which you need before you type owl:Class.",
        "Promotion is triggered by the first axiom about members. Until then, a concept scheme is cheaper, more flexible, and truer to what is known.",
        "Punning lets one IRI be both. Pay for it only when the vocabulary is both a shelf plan and a reasoning target.",
    ],
    body=DECL + """
skos:Concept    a owl:Class .
skos:broader    a owl:ObjectProperty .

bs:Work         a owl:Class ; skos:prefLabel "Work"@en .
bs:Bookshop     a owl:Class ; skos:prefLabel "Bookshop"@en .
bs:genre        a owl:ObjectProperty ; rdfs:domain bs:Work ;     rdfs:range skos:Concept .
bs:specialises  a owl:ObjectProperty ; rdfs:domain bs:Bookshop ; rdfs:range skos:Concept .

# The genre as a concept: what the Trail does.
bt:genre-fiction        a skos:Concept ; skos:prefLabel "Fiction"@en, "Ffuglen"@cy .
bt:genre-crime-fiction  a skos:Concept ; skos:prefLabel "Crime Fiction"@en ; skos:altLabel "Mystery"@en ;
    skos:broader bt:genre-fiction ;
    skos:scopeNote "Works whose plot turns on a crime and its investigation. Includes cosy crime and tartan noir."@en .

bt:book-the-book-town  a bs:Work ;     skos:prefLabel "The Book Town"@en ; bs:genre bt:genre-crime-fiction .
bt:shop-inkwell        a bs:Bookshop ; skos:prefLabel "The Inkwell"@en ;   bs:specialises bt:genre-crime-fiction .

# The same genre promoted to a class: what you would write if you needed
# to say something about every crime novel. A shop has no way to specialise
# in it, and the query below shows the asymmetry.
bs:CrimeFiction  a owl:Class ; rdfs:subClassOf bs:Work ; skos:prefLabel "Crime Fiction (as a class)"@en ;
    skos:definition "A Work whose plot turns on a crime and its investigation."@en .
bt:book-the-book-town  a bs:CrimeFiction .
""",
    queries=[
        Query("What points at the genre as a concept", """
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?thing ?property WHERE { ?thing ?property bt:genre-crime-fiction }""", rows=2),
        Query("What is a member of the genre as a class", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT ?member WHERE { ?member a bs:CrimeFiction }""", rows=1),
    ],
    check=dict(profile=True, reason=True),
    expect=dict(dl=True, consistent=True),
)
specs.register("o24", "skosConcepts", "skosPrimerOwl")

o(
    oid="o25", module=M,
    title="A controlled vocabulary before a taxonomy",
    decides="The event kinds stop being strings in the data and become a controlled list of seven terms with one preferred label each, synonyms, a scope note and a maintainer.",
    corner="thought",
    why="The Trail's events carry bs:eventKind as a string: 'Reading', "
        "'Signing', 'Launch', 'Workshop', 'Panel', 'Book Club', 'Lecture'. "
        "The vocabulary lists the seven in a comment, which is the only "
        "thing stopping an eighth spelt 'reading' from appearing. A string "
        "that should be a thing is the commonest smell in a dataset, and "
        "the cure is the oldest technique in information science: a "
        "controlled vocabulary. ANSI/NISO Z39.19 sets out what one is. Each "
        "concept has exactly one preferred term; every synonym is recorded "
        "and points at it; each term has a scope note saying what it does "
        "and does not cover; and somebody is named as responsible for the "
        "list.\n\n"
        "None of that needs a hierarchy. A controlled vocabulary is a flat "
        "list with discipline, and it is where most vocabularies should "
        "start and where many should stop. The hierarchy, when it is "
        "needed, is the next rung of the ladder, module 06. gist has the "
        "same shape in its own terms: a gist:ControlledVocabulary is a "
        "collection of gist:Category instances governed by an organisation "
        "or person.\n\n"
        "The seven kinds become seven particulars in this file, each with a "
        "notation, a preferred label, its synonyms as alternative labels, "
        "and a scope note. 'Talk' and 'Author event' are recorded as "
        "synonyms of Lecture and Reading, because the spreadsheet had them. "
        "The query at the end counts events by kind after the migration, "
        "which is what the website will do and what the strings could not "
        "do reliably.",
    diagram="""
   before                                    after

   bs:eventKind  "Reading"                   bs:eventKind  bt:kind-reading
   bs:eventKind  "reading"    (an eighth)    bt:kind-reading  a bs:EventKind ;
   bs:eventKind  "Author event"                 skos:notation "RD" ;
                                                skos:prefLabel "Reading"@en ;
                                                skos:altLabel "Author event"@en, "reading"@en ;
                                                skos:scopeNote "An author reads from a work ..." .

   one preferred term, synonyms recorded, a scope note, a named maintainer
""",
    learn=[
        "A string that is one of a fixed set is a thing pretending to be a value. Give it an IRI.",
        "A controlled vocabulary is a flat list with four disciplines: one preferred term, recorded synonyms, scope notes, a maintainer.",
        "Start flat. Add the hierarchy when a question needs it, and not before.",
    ],
    body=DECL + """
bs:EventKind  a owl:Class ; skos:prefLabel "Event Kind"@en ;
    skos:definition "A kind of event a bookshop holds, from the Trail's controlled list."@en ;
    skos:editorialNote "Maintained by the events secretary. Additions by committee only."@en .
bs:eventKind  a owl:ObjectProperty ; rdfs:range bs:EventKind ; skos:prefLabel "event kind"@en .

bt:kind-reading   a bs:EventKind ; skos:notation "RD" ; skos:prefLabel "Reading"@en ;   skos:altLabel "Author event"@en, "reading"@en ;
    skos:scopeNote "An author reads from a work and takes questions. Not a signing, though one may follow."@en .
bt:kind-signing   a bs:EventKind ; skos:notation "SG" ; skos:prefLabel "Signing"@en ;
    skos:scopeNote "An author signs copies. No reading."@en .
bt:kind-launch    a bs:EventKind ; skos:notation "LN" ; skos:prefLabel "Launch"@en ;
    skos:scopeNote "The first public event for a new work, at or near publication."@en .
bt:kind-workshop  a bs:EventKind ; skos:notation "WS" ; skos:prefLabel "Workshop"@en ;
    skos:scopeNote "Participants write or make something. Ticketed, usually."@en .
bt:kind-panel     a bs:EventKind ; skos:notation "PN" ; skos:prefLabel "Panel"@en ;
    skos:scopeNote "Several speakers in discussion, with a chair."@en .
bt:kind-book-club a bs:EventKind ; skos:notation "BC" ; skos:prefLabel "Book Club"@en ; skos:altLabel "Reading group"@en ;
    skos:scopeNote "A recurring meeting to discuss one work. The author is not usually present."@en .
bt:kind-lecture   a bs:EventKind ; skos:notation "LC" ; skos:prefLabel "Lecture"@en ;  skos:altLabel "Talk"@en ;
    skos:scopeNote "One speaker on a subject, not necessarily an author of a work in stock."@en .

# Three events, migrated.
bt:event-1  a bs:Event ; bs:eventKind bt:kind-reading .
bt:event-2  a bs:Event ; bs:eventKind bt:kind-reading .
bt:event-3  a bs:Event ; bs:eventKind bt:kind-lecture .
bs:Event    a owl:Class .
""",
    queries=[Query("Events by kind, by preferred label", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?kind (COUNT(?event) AS ?events) WHERE {
  ?k a bs:EventKind ; skos:prefLabel ?kind .
  OPTIONAL { ?event bs:eventKind ?k }
} GROUP BY ?kind ORDER BY DESC(?events)""", rows=7)],
    check=dict(profile=True),
    expect=dict(dl=True, individuals=10),
)
specs.register("o25", "niso", "skosNotes")

o(
    oid="o26", module=M,
    title="Borrow the term, or borrow the definition",
    decides="A term is reused by IRI only when its published meaning is the meaning wanted; otherwise the Trail mints its own and cites the source; and every borrowed term is declared.",
    corner="symbol and thought",
    why="Reuse is a principle in every guide. OBO FP-007 requires existing "
        "relations to be reused rather than reinvented; gist exists so that "
        "'person', 'organisation' and 'agreement' need not be defined "
        "again. The reason is the triangle: two ontologies that share an "
        "IRI share a referent, and their data joins without a mapping. Two "
        "that each mint a Person need a mapping, and a mapping is a place "
        "for an argument.\n\n"
        "But reusing an IRI means reusing its definition and its semantics, "
        "all of them. dct:title is safe; it is an annotation and says "
        "nothing a reasoner acts on. schema:Book comes with a hierarchy "
        "under schema:CreativeWork and a loose contract about what a Book "
        "is. dct:isPartOf is defined in RDFS only, which is why the Trail "
        "declares it an annotation property to stay in OWL 2 DL. So the "
        "rule has three branches. Borrow the IRI when the published "
        "definition is the one you want, and declare it in your own file so "
        "the profile checker knows what it is. Borrow the definition, "
        "citing it with dct:source, when the words are right but the "
        "semantics are not. Mint your own when neither fits, and say what "
        "you looked at first.\n\n"
        "The Trail borrows skos:, geo:, wgs84:, prov: and dct: terms by IRI, "
        "and declares every one, which is what lets a file of its own "
        "stand as OWL 2 DL without importing anything. It mints bs:Person "
        "rather than reuse gist:Person or foaf:Person, and module 09 "
        "shows the bridge that costs.",
    diagram="""
   want                                     do                              example

   the published meaning, exactly           reuse the IRI, declare it       skos:prefLabel, geo:hasGeometry
   the words, not the semantics             mint, cite with dct:source      bs:Person (source: gist:Person)
   neither                                  mint, say what you looked at    bs:TrailSegment

   a shared IRI is a shared referent: data joins with no mapping
   a borrowed IRI brings its whole definition, and its hierarchy, and its profile
""",
    learn=[
        "Reuse an IRI when you mean exactly what its owner means. Then declare it in your file, so the checker knows its type.",
        "Borrow a definition and cite it when the words fit and the semantics do not.",
        "Mint your own when neither fits, and record what you considered. The note is cheaper than the second argument.",
    ],
    body=DECL + """
# Borrowed by IRI, and declared: the published meaning is the meaning wanted.
skos:Concept       a owl:Class ;          rdfs:isDefinedBy <http://www.w3.org/2004/02/skos/core> .
geo:Feature        a owl:Class ;          rdfs:isDefinedBy <http://www.opengis.net/ont/geosparql> .
geo:hasGeometry    a owl:ObjectProperty ; rdfs:isDefinedBy <http://www.opengis.net/ont/geosparql> .
wgs84:lat          a owl:DatatypeProperty ; rdfs:range xsd:decimal ; rdfs:isDefinedBy <http://www.w3.org/2003/01/geo/wgs84_pos> .
dct:title          a owl:AnnotationProperty .
dct:isPartOf       a owl:AnnotationProperty ;
    skos:editorialNote "Defined only in RDFS by DCMI, so declared here as an annotation property to stay in OWL 2 DL."@en .
rdfs:isDefinedBy   a owl:AnnotationProperty .

# Minted, with the definition borrowed and cited.
bs:Person  a owl:Class ; skos:prefLabel "Person"@en ;
    skos:definition "A human being who was or is alive."@en ;
    dct:source      gist:Person ;
    skos:editorialNote "Definition after gist:Person. Minted rather than reused so that the Trail's files stand alone; module 09 adds the bridge."@en .

# Minted, with the search recorded.
bs:TrailSegment  a owl:Class ; skos:prefLabel "Trail Segment"@en ;
    skos:definition "A walking route between two bookshops, with a length."@en ;
    skos:editorialNote "Considered gist:GeoRoute (an ordered set of points; ours has two ends and a length) and gist:NetworkLink. Neither said 'walkable'. Minted."@en .
""",
    check=dict(profile=True),
    expect=dict(dl=True),
)
specs.register("o26", "oboRelations", "syntaxDeclarations")

o(
    oid="o27", module=M,
    title="Once published, a term means what it meant",
    decides="A definition may be clarified but never changed to denote different things; when the meaning must change, a new term is minted and the old one deprecated with a pointer.",
    corner="thought",
    why="OBO Foundry principle FP-019 is the shortest in the list and the "
        "one most often broken: the definition of a term must always denote "
        "the same things. Clarify the wording, correct a typo, add an "
        "example, and it is still the same term. Widen it to cover something "
        "it did not, or narrow it, and every dataset that used the old "
        "meaning is now silently wrong, with no error anywhere.\n\n"
        "The Trail's case is bs:Work, which o10 recorded as a work and an "
        "edition in one. The day a second edition appears, the class must "
        "split. The wrong move is to redefine bs:Work as 'a work, "
        "independent of edition' and start typing editions differently: "
        "every existing bs:Work assertion was made under the old meaning. "
        "The right move is a new term for the new meaning, bs:Edition say, "
        "and a deprecation on anything whose meaning has moved, with a "
        "pointer to what replaces it. gist's deprecation policy, "
        "module 11, is the mechanics; this is the principle.\n\n"
        "skos:historyNote and skos:changeNote are where the story goes. "
        "gist uses them rarely because git holds the history, and that is "
        "fair for an ontology whose users read the repository. For one "
        "whose users read the terms, a sentence on the term is worth more.",
    diagram="""
   allowed: same referents, better words          not allowed: new referents, same IRI

   "A book."                                       "A book."   ->   "A work, independent of edition."
     -> "A book: what an author wrote,               every bs:Work assertion made under the
         in a particular published form."            old meaning is now silently wrong

   the move: mint bs:Edition, deprecate what changed, point from old to new
   owl:deprecated true ; dct:isReplacedBy bs:Edition ; skos:changeNote "..."
""",
    learn=[
        "Clarify freely; never change what a term denotes. FP-019, and every guide agrees.",
        "When the meaning must move, mint a new IRI and deprecate the old one with a pointer. The data made under the old meaning stays true.",
        "A change note on the term is worth more to a user than a commit message they will never read.",
    ],
    body=DECL + """
owl:deprecated  a owl:AnnotationProperty .

bs:Work
    a                 owl:Class ;
    skos:prefLabel    "Work"@en ;
    skos:definition   "A book: what an author wrote, in a particular published form."@en ;
    skos:historyNote  "Defined 2025 as 'A book. Translations are Works in their own right.' Reworded 2026 without change of meaning."@en .

# What the split would look like the day a second edition appears. The old
# term keeps its meaning and its data; the new term carries the new meaning.
bs:PublishedWork
    a                 owl:Class ;
    owl:deprecated    true ;
    skos:prefLabel    "Published Work"@en ;
    skos:definition   "A book with an ISBN, as first modelled."@en ;
    skos:changeNote   "Deprecated 2026: the meaning moved to bs:Edition when works acquired more than one edition. Not deleted; assertions made under it remain true."@en ;
    dct:isReplacedBy  bs:Edition .

bs:Edition
    a                 owl:Class ;
    skos:prefLabel    "Edition"@en ;
    skos:definition   "A printing of a Work by a publisher, with an ISBN if made after 1970."@en .
""",
    queries=[Query("Deprecated terms and what replaces them", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?old ?new WHERE { ?old owl:deprecated true ; dct:isReplacedBy ?new }""", rows=1)],
    check=dict(profile=True, oqs="checks"),
    expect=dict(dl=True),
)
specs.register("o27", "oboStability", "gistDeprecation")
