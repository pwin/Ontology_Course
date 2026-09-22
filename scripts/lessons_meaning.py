# -*- coding: utf-8 -*-
"""Module 01 -- Meaning: the triangle, the two ways a word fails, and the IRI."""
from ontocat import o, Query
import specs

M = "01-meaning"

o(
    oid="o01", module=M,
    title="A word, a thing, and the idea in between",
    decides="Every term in the brief is a symbol standing for a referent by way of a thought, and the three are kept apart from the first line.",
    corner="all three, introduced",
    why="Ogden and Richards drew it in 1923 and nobody has improved on it. At "
        "one corner is the symbol: the word 'Wigtown', the string in the "
        "spreadsheet. At another is the referent: the town itself, on the "
        "Solway coast, which does not care what it is called. At the third is "
        "the thought, the idea of the town in somebody's head, and it is the "
        "thought that connects the other two. The symbol does not refer to the "
        "town directly; it refers by way of someone's understanding of it, "
        "which is why the base of the triangle is drawn as a dotted line.\n\n"
        "That dotted line is where every data integration problem lives. Two "
        "people share the symbol 'area' and hold different thoughts under it, "
        "one of square metres and one of council boundaries, and nothing in "
        "the spreadsheet says which. An ontology is a way of fixing the "
        "thought corner in writing, so that a shared symbol carries a shared "
        "meaning.\n\n"
        "This file is the smallest possible start. Each candidate term from "
        "the brief becomes a node with a label (the symbol) and a comment "
        "(the thought, written down). The referent stays where it is; the "
        "node points at it. Nothing here is a class or a property yet. That "
        "comes later, and it comes more easily once the three corners are "
        "habit.",
    diagram="""
                      THOUGHT
                 (the idea of the town)
                     /          \\
        symbolises  /            \\  refers to
                   /              \\
             SYMBOL  . . . . . . . REFERENT
            "Wigtown"               the town
             a string           on the Solway coast

   The dotted base: a symbol stands for a referent only through
   a thought. Share the symbol, and you have not yet shared the
   thought. Writing the thought down is what an ontology is for.
""",
    learn=[
        "Symbol, thought, referent. Keep the three apart and most confusions about naming, defining and identity become easy to state.",
        "A label is a symbol for people. A definition is the thought written down. Neither is the thing.",
        "The brief is a pile of symbols. The first job is to find out how many referents are behind them, and it is rarely one per word.",
    ],
    tryit="Open the LOAD IT link. The graph view draws each candidate as a node with its label and comment. Pick 'Subjects' and choose one; then ask "
          "yourself which corner of the triangle each of the three things on screen is: the IRI, the label, the comment.",
    body="""
# The candidate terms from the brief, as symbols with the thought written
# beside them. No classes, no properties: nodes, labels, comments.

bt:candidate-wigtown
    rdfs:label    "Wigtown"@en ;
    rdfs:comment  "The town in Dumfries and Galloway, Scotland's book town. Not the festival, the ward or the bay."@en .

bt:candidate-area
    rdfs:label    "area"@en ;
    rdfs:comment  "Used in the brief for two things: a shop's floor area in square metres, and a council area. Two thoughts under one symbol; see o02."@en .

bt:candidate-book
    rdfs:label    "book"@en ;
    rdfs:comment  "Used in the brief for a title, an edition and a copy on a shelf. Three thoughts under one symbol; see o02."@en .

bt:candidate-author
    rdfs:label    "author"@en ;
    rdfs:comment  "Someone who wrote a book. Also used for whoever appears at an event, who may be a translator."@en .

bt:candidate-shop
    rdfs:label    "shop"@en ;
    rdfs:comment  "One symbol of three: shop, bookshop, store. One thought; see o02."@en .

bt:candidate-founded
    rdfs:label    "founded"@en ;
    rdfs:comment  "The year a shop opened. The guidebooks disagree for four shops, and the brief asks that both dates be kept with their source."@en .
""",
    expect=dict(min_triples=12),
)
specs.register("o01", "triangle", "peirce")

o(
    oid="o02", module=M,
    title="One word, many things; many words, one thing",
    decides="'Book' is split into three referents and 'shop', 'bookshop' and 'store' are merged into one, because identity follows the referent and not the word.",
    corner="symbol and referent",
    why="A word fails in two directions. Homonymy is one symbol over several "
        "referents: 'book' in the brief means the title someone wrote, the "
        "edition with an ISBN, and the copy on the shelf at a price. Ask "
        "'do you have the book?' and three different answers are correct. "
        "Synonymy is several symbols over one referent: shop, bookshop, store "
        "are one thing three ways, and a search that matches on the string "
        "will find a third of them.\n\n"
        "Both failures have the same cure. Decide how many referents there "
        "are, give each its own identifier, and hang the words off the "
        "identifiers as labels. The identifier decides identity; the words "
        "are free to vary. Google called this 'things, not strings' in 2012 "
        "and the phrase has stuck because it is exactly right.\n\n"
        "The Trail keeps 'book' as one class, bs:Work, and gives it an ISBN, "
        "which is honestly an edition's property. That is a recorded "
        "compromise (o09 comes back to it), and it is a better state than the "
        "brief's, where the compromise was invisible.",
    diagram="""
   HOMONYMY: one symbol, three referents           SYNONYMY: three symbols, one referent

        "book" ---.---> the title (a work)              "shop"     --.
                  |---> the edition (an ISBN)            "bookshop" --+--> bt:shop-inkwell
                  '---> the copy (a shelf price)         "store"    --'

   cure: one identifier per referent               cure: one identifier, three labels
""",
    learn=[
        "Count referents, not words. A symbol with two referents needs two identifiers; two symbols with one referent need one.",
        "Labels are cheap and plural. Identifiers are the thing that must be unique.",
        "The Trail's bs:Work is a title and an edition in one class. Written down, that is a decision; unwritten, it is a trap.",
    ],
    body="""
# 'book', split by referent. Three things, three identifiers; the word is a
# label on all of them.

bt:candidate-work
    rdfs:label    "book"@en, "work"@en, "title"@en ;
    rdfs:comment  "What an author wrote, independent of any printing. Translated, it becomes another work."@en .

bt:candidate-edition
    rdfs:label    "book"@en, "edition"@en ;
    rdfs:comment  "A printing of a work by a publisher, with an ISBN if made after 1970."@en .

bt:candidate-copy
    rdfs:label    "book"@en, "copy"@en ;
    rdfs:comment  "A physical copy of an edition, on a shelf in one shop at one price. The Trail counts these in bs:StockRecord rather than naming each."@en .

# 'shop', merged by referent. One thing, three labels.

bt:candidate-bookshop
    rdfs:label    "bookshop"@en, "shop"@en, "store"@en ;
    rdfs:comment  "A business that sells books from premises. The building it trades from is a different referent; o05 and o09."@en .
""",
    queries=[Query("Every symbol with more than one node behind it", """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?label (COUNT(?node) AS ?referents)
WHERE { ?node rdfs:label ?label }
GROUP BY ?label
HAVING (COUNT(?node) > 1)
ORDER BY DESC(?referents)""", rows=1)],
    expect=dict(min_triples=12),
)
specs.register("o02", "thingsNotStrings", "rdfReferents")

o(
    oid="o03", module=M,
    title="Shared meaning is an agreement",
    decides="A definition is treated as the record of an agreement, with who made it and when, and a disagreement is modelled rather than settled by the modeller.",
    corner="thought",
    why="Two people looking at the same referent hold two thoughts, and the "
        "triangle has no mechanism for making them one. What makes a meaning "
        "shared is an agreement: this symbol, from now on, means this, and "
        "here is the sentence we all signed up to. The sentence is the "
        "definition. It is a social artefact before it is a technical one, "
        "and the process of arriving at it is where a team finds out what it "
        "actually thinks.\n\n"
        "Some disagreements are not misunderstandings. The SemOps Manual's "
        "example is 'active customer', where finance and product each need a "
        "different definition for reasons that are load-bearing for them. The "
        "right move is to model both, well labelled, and let someone with the "
        "authority decide which goes in the board pack; the modeller's job is "
        "to make the difference visible, not to adjudicate it. The wrong move "
        "is the one that happens by default: the modeller picks one, ships "
        "it, and half the business ignores the model from then on.\n\n"
        "The Trail has a small version. 'Founded' and 'opened' are agreed to "
        "mean the same; the committee said so. The founding year of Ex Libris "
        "is not agreed, and the brief asks for both claims to be kept with "
        "their source. That is a disagreement about a fact, not about a "
        "meaning, and the RDF 1.2 layer of the data records it as such. What "
        "this lesson adds is the record of the agreement itself: who decided "
        "that founded means opened, and when.",
    diagram="""
   your thought          my thought
       |                      |
       '------> agreement <---'
                   |
            written down as
                   |
              a definition       + who decided, and when
                   |
             carried by the symbol, from now on

   A disagreement that will not close is modelled as two terms,
   each defined, and the choice between them is somebody's decision.
""",
    learn=[
        "A definition is an agreement in writing. It is the thing that makes a shared symbol carry a shared thought.",
        "Record who agreed it and when. Definitions get argued over again, and the trail of the decision is what stops the argument repeating.",
        "Do not resolve a disagreement that is really about territory. Model both meanings with clear labels and hand the choice to someone with the authority to make it.",
        "Building the vocabulary is a social process, and often the most useful part of it. People find out what they mean.",
    ],
    body="""
# The agreement that 'founded' and 'opened' are one term, with the record of
# who agreed it. dct:source and skos:editorialNote carry the trail.

bt:candidate-founded
    rdfs:label          "founded"@en, "opened"@en ;
    rdfs:comment        "The year a shop or publisher began trading."@en ;
    skos:editorialNote  "Agreed at the committee of 12 March 2025 that 'founded' and 'opened' are the same term. Where sources disagree about the year, keep every claim with its source; do not choose."@en ;
    dct:source          bt:committee-2025-03-12 .

bt:committee-2025-03-12
    rdfs:label    "Trail committee, 12 March 2025"@en ;
    rdfs:comment  "The meeting that agreed the first list of terms."@en .

# A disagreement that stays open: two claims about one fact, each with a
# source. This is what the brief asked for, and it is data, not vocabulary.

bt:claim-ex-libris-1921
    rdfs:label    "Ex Libris founded in 1921, per the national register"@en ;
    dct:source    bt:source-national-register .

bt:claim-ex-libris-1923
    rdfs:label    "Ex Libris founded in 1923, per the trail guide"@en ;
    dct:source    bt:source-trail-guide-2024 .
""",
    expect=dict(min_triples=10),
)
specs.register("o03", "semopsTerritory", "blogTeam")

o(
    oid="o04", module=M,
    title="A symbol that is globally unique, and that a machine can read",
    decides="Every referent gets an IRI, because an IRI is the one kind of symbol that cannot collide with anyone else's and that a machine can compare, join on and look up.",
    corner="symbol",
    why="A label is a symbol for people. 'Wigtown' works in a conversation "
        "and fails in a database, where the festival and the town both answer "
        "to it and no machine can tell them apart. A code works inside one "
        "system: EVT-001, row 14, the shop id. It fails the moment two "
        "systems meet, because both of them have an EVT-001.\n\n"
        "An IRI is a symbol built to survive that meeting. It is globally "
        "unique by construction: the http scheme delegates the right to mint "
        "names under a domain to whoever holds the domain, so "
        "example.org/bookshop-trail/place-wigtown can only have been coined "
        "by one party, and nobody else's place-wigtown can be confused with "
        "it. The Web Architecture document calls this URI ownership.\n\n"
        "It is machine-readable in a precise and modest sense. A machine "
        "cannot understand it, but it can test two of them for equality by "
        "comparing strings, join two graphs wherever the same IRI appears in "
        "both, and, because it is an http IRI, fetch it and get back the "
        "definition. Nothing more is claimed and nothing more is needed. The "
        "same document also asks for opacity: a machine should read nothing "
        "into the spelling of an IRI, which is why gist and BFO can both be "
        "right about naming, one readable and one numeric, as o15 discusses.\n\n"
        "The IRI is still not the referent. It is a third kind of symbol, "
        "sitting on the symbol corner beside the label, and RDF Concepts "
        "section 1.3 says in as many words that what it refers to is fixed by "
        "convention and definition, not by the IRI itself. owl:sameAs is the "
        "statement that two IRIs share a referent; the Trail uses it to say "
        "that its Wigtown is DBpedia's.",
    diagram="""
   symbols on the symbol corner            what a machine can do with each

   label   "Wigtown"@en                    match a string; collide with the festival
   code    WGT-04                          match inside one system; collide outside it
   IRI     bt:place-wigtown                compare for identity anywhere
           = https://example.org/          join two graphs on it
             bookshop-trail/place-wigtown  fetch it and read the definition
                                           cannot be minted by anyone but the owner of example.org

   bt:place-wigtown  owl:sameAs  <http://dbpedia.org/resource/Wigtown>
   "these two symbols, minted by two owners, share one referent"
""",
    learn=[
        "Globally unique comes from ownership: only the holder of a domain can mint IRIs under it. That is the whole trick, and it is enough.",
        "Machine-readable means comparable, joinable and fetchable. It does not mean understood.",
        "An IRI is opaque to a machine. Its spelling is for people, and the definition it resolves to is what fixes the referent.",
        "owl:sameAs joins two owners' symbols at the referent. Use it when you mean identity, not resemblance.",
    ],
    tryit="In the SPARQL panel, count how many distinct subjects have the label 'Wigtown'. Then count distinct IRIs. The first number is what a string "
          "search sees; the second is what a graph sees.",
    body="""
bt:place-wigtown
    rdfs:label    "Wigtown"@en, "Baile na h-Uige"@gd ;
    rdfs:comment  "The town. The IRI is the Trail's own; the labels are anyone's."@en ;
    owl:sameAs    <http://dbpedia.org/resource/Wigtown> .

bt:festival-wigtown
    rdfs:label    "Wigtown Book Festival"@en, "Wigtown"@en ;
    rdfs:comment  "The festival, which people also call Wigtown. A different referent, so a different IRI."@en .

# A local code, kept for the spreadsheet's sake. It identifies inside the
# Trail's own systems and nowhere else, so it is a label here, not a name.
bt:place-wigtown
    skos:notation  "WGT-04" .
""",
    queries=[
        Query("Symbols that name more than one thing", """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?label (COUNT(DISTINCT ?thing) AS ?things)
WHERE { ?thing rdfs:label ?label }
GROUP BY ?label
HAVING (COUNT(DISTINCT ?thing) > 1)""", rows=1),
        Query("What the Trail's Wigtown is the same as", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?ours ?theirs WHERE { ?ours owl:sameAs ?theirs }""", rows=1),
    ],
    expect=dict(min_triples=8),
)
specs.register("o04", "webarchOwner", "rdfReferents")

o(
    oid="o05", module=M,
    title="A particular or a kind",
    decides="Wigtown, The Inkwell and Rhona Blackwood are particulars; Settlement, Bookshop and Person are kinds; rdf:type is the link, and a kind is a referent with an IRI like any other.",
    corner="referent",
    why="Some symbols in the brief pick out one thing: Wigtown, The Inkwell, "
        "Rhona Blackwood, the Lodestone Group. Others pick out a kind of "
        "thing: town, shop, author, publisher. The first are particulars, "
        "called individuals in OWL; the second are kinds, called classes. The "
        "relation between them is rdf:type, and it is the first relation "
        "worth writing down, because most of the brief's questions are "
        "questions about kinds: which shops, which towns, which events.\n\n"
        "A kind is a referent too. bs:Settlement refers to the kind, town, "
        "in the same way bt:place-wigtown refers to the town, and it gets an IRI on the same terms. The IRI is what lets you say things about the kind itself: what it is called in Welsh, what its definition is, "
        "which other kinds it falls under. The class hierarchy of module 02 "
        "is just statements about kinds.\n\n"
        "The line between particular and kind is not always where the brief "
        "puts it. 'Crime fiction' looks like a kind of book, and a class of works is one fair reading. It is also a thing a shop specialises "
        "in, and a shop is not a member of a class of books. The Trail treats "
        "genres as particulars, concepts in a scheme, so that both a work and "
        "a shop can point at the same one. o24 returns to that choice; it is "
        "the most consequential one in the course.",
    diagram="""
   particulars (individuals)          rdf:type        kinds (classes)

   bt:place-wigtown        ------------------------>  bs:Settlement
   bt:shop-inkwell         ------------------------>  bs:Bookshop
   bt:author-rhona-blackwood --------------------->  bs:Person
   bt:genre-crime-fiction  ------------------------>  skos:Concept   <- a particular, on purpose

   Both columns are referents with IRIs. The right-hand ones can be
   labelled, defined and arranged under each other, like anything else.
""",
    learn=[
        "rdf:type says which kind a particular belongs to. It is the first structural statement, and the one every question about 'which shops' depends on.",
        "A class is a referent, with an IRI, a label and a definition. Saying things about kinds is what a taxonomy is.",
        "Whether something is a particular or a kind is a decision, and genre is the case where the obvious answer is not the best one.",
    ],
    body="""
bs:Settlement
    a             rdfs:Class ;
    rdfs:label    "Settlement"@en ;
    rdfs:comment  "A town or city."@en .

bs:Bookshop
    a             rdfs:Class ;
    rdfs:label    "Bookshop"@en ;
    rdfs:comment  "A business that sells books from premises."@en .

bs:Person
    a             rdfs:Class ;
    rdfs:label    "Person"@en ;
    rdfs:comment  "A human being."@en .

bt:place-wigtown
    a           bs:Settlement ;
    rdfs:label  "Wigtown"@en .

bt:shop-inkwell
    a           bs:Bookshop ;
    rdfs:label  "The Inkwell"@en .

bt:author-rhona-blackwood
    a           bs:Person ;
    rdfs:label  "Rhona Blackwood"@en .

# A genre is a particular here, not a class: something a shop specialises in
# and a work belongs to. Module 04 and module 06 make the case in full.
bt:genre-crime-fiction
    a           skos:Concept ;
    rdfs:label  "Crime Fiction"@en .
""",
    queries=[Query("Every particular and its kind", """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?thing ?kind WHERE { ?thing a ?kind . FILTER(?kind != rdfs:Class) } ORDER BY ?kind""", rows=4)],
    expect=dict(classes=3, min_triples=14),
)
specs.register("o05", "rdfsType", "rdfsClass")

o(
    oid="o06", module=M,
    title="A relationship is a thing too",
    decides="The brief's verbs become properties with IRIs of their own: locatedIn, wrote, stocks, heldAt; its measurements become datatype properties; and a property is defined like any other term.",
    corner="referent",
    why="Nouns give kinds and particulars. The verbs and the 'has' phrases "
        "give relationships: a shop is in a town, an author wrote a work, a "
        "shop stocks a work, an event was held at a shop. Each of these is a "
        "referent in its own right, a kind of connection that can hold "
        "between many pairs, and it gets an IRI, a label and a definition on "
        "the same terms as a class. The triangle applies to it unchanged.\n\n"
        "Some relationships end in a value rather than a thing: the year "
        "opened, the floor area, the number of staff, whether there is a "
        "cafe. These are datatype properties. The distinction matters later "
        "because OWL requires every property to be one or the other and not "
        "both, but it is worth making now for a simpler reason: a value has "
        "no identity of its own. 140 square metres is not a thing with an "
        "IRI; it is a measurement of one.\n\n"
        "Two relationships from the brief are worth pausing on. 'Specialises "
        "in' points a shop at a genre, and 'in one or more genres' points a "
        "work at the same genres, which is the argument for genres being "
        "particulars (o05). And 'influenced by' runs author to author, at "
        "several removes, which the brief's question 7 wants followed; that "
        "is a property with a shape the reasoner will have views on in "
        "module 07.",
    diagram="""
   noun phrase in the brief          what it becomes

   "a shop is in a town"             bs:locatedIn      object property   Bookshop -> Settlement
   "the author wrote it"             bs:wrote          object property   Person   -> Work
   "the shop stocks it"              bs:stocks         object property   Bookshop -> Work
   "held at the shop"                bs:heldAt         object property   Event    -> Bookshop
   "who influenced them"             bs:influencedBy   object property   Person   -> Person

   "year opened"                     bs:founded        datatype property Bookshop -> a year
   "area (square metres)"            bs:floorArea      datatype property Bookshop -> a number
   "whether there is a cafe"         bs:hasCafe        datatype property Bookshop -> true/false

   A property is a referent: it has an IRI, a label, a definition.
""",
    learn=[
        "Verbs become object properties, measurements become datatype properties, and both are terms with IRIs and definitions.",
        "A value has no identity. That is the line between an object property and a datatype property, and OWL will hold you to it.",
        "The brief's 'at several removes' is a property that will need transitivity, a path, or a rule. Notice it now; module 08 answers it three ways.",
    ],
    body="""
bs:locatedIn
    a             rdf:Property ;
    rdfs:label    "located in"@en ;
    rdfs:comment  "The settlement a shop or publisher trades in."@en .

bs:wrote
    a             rdf:Property ;
    rdfs:label    "wrote"@en ;
    rdfs:comment  "The person wrote the work. Translating is a different relationship."@en .

bs:stocks
    a             rdf:Property ;
    rdfs:label    "stocks"@en ;
    rdfs:comment  "The shop has copies of the work on its shelves."@en .

bs:heldAt
    a             rdf:Property ;
    rdfs:label    "held at"@en ;
    rdfs:comment  "The shop where an event took place."@en .

bs:influencedBy
    a             rdf:Property ;
    rdfs:label    "influenced by"@en ;
    rdfs:comment  "Whom this author read first. Direct influence only; several removes is a question for a path."@en .

bs:founded
    a             rdf:Property ;
    rdfs:label    "founded"@en ;
    rdfs:comment  "The year a shop or publisher began trading. A value, not a thing."@en .

bs:floorArea
    a             rdf:Property ;
    rdfs:label    "floor area"@en ;
    rdfs:comment  "Selling floor in square metres."@en .

bt:shop-inkwell
    bs:locatedIn  bt:place-wigtown ;
    bs:founded    "1979" ;
    bs:floorArea  "140.0" .
""",
    expect=dict(min_triples=20),
)
specs.register("o06", "rdfsProperty", "rdfIris")

o(
    oid="o07", module=M,
    title="Scope, and the questions that fix it",
    decides="The ontology covers what the brief's ten questions need and nothing the brief only mentions; the questions are written into the ontology as its statement of scope.",
    corner="thought",
    why="The brief mentions a bay, a festival, a council ward, the weather "
        "that cancels a reading, the till. None of them is in scope, and "
        "the way to know is the list of questions at the end of it. An "
        "ontology exists to answer questions; a term that no question needs "
        "is a term that will be defined badly, because nobody will use it "
        "enough to notice.\n\n"
        "Competency questions are the oldest tool in ontology engineering and "
        "still the best test of scope. Written as prose they are a "
        "requirement. Written as SPARQL they are a test, and the SemOps "
        "Manual makes the point that a question captured once and run "
        "forever is the cheapest way to survive maintenance. The Bookshop "
        "Trail already has its questions written as SPARQL: the SPARQL "
        "course is 145 of them, and module 12 runs a selection against the "
        "ontology this course builds.\n\n"
        "The OBO Foundry lists scope as a founding principle, FP-005: the "
        "ontology must have a clearly specified scope and content. The Trail "
        "states its scope in two sentences on the ontology node, and lists "
        "the ten questions beside it. That is enough. It is also more than "
        "most ontologies carry.",
    diagram="""
   in the brief                 in scope?     why

   shops, towns, books, ...       yes         questions 1 to 10 need them
   the walking trail              yes         question 3
   who influenced whom            yes         question 7
   the festival                   no          no question asks about it
   the council ward, the bay      no          named only to say what Wigtown is not
   the weather, the till          no          not mentioned in any question

   A term nobody asks about is a term nobody will keep right.
""",
    learn=[
        "Scope is fixed by the questions. Write them down, keep them with the ontology, and refuse terms no question needs.",
        "A competency question in SPARQL is a test. The SPARQL course is this ontology's test suite, and module 12 uses it that way.",
        "State the scope on the ontology itself, in two sentences. OBO FP-005 asks for exactly this and few ontologies do it.",
    ],
    body="""
<https://example.org/bookshop-trail/schema>
    a             owl:Ontology ;
    rdfs:label    "The Bookshop Trail schema"@en ;
    rdfs:comment  "A vocabulary for a network of independent bookshops in real British towns: the shops, the towns and areas they are in, the books they stock, the people who wrote them, the events they hold, and the walking routes between them. Out of scope: festivals, wards, weather, tills, and anything the ten questions below do not need."@en ;
    skos:scopeNote "Competency questions, from the committee's brief: (1) which shops are in Wales, the south west, or a given council area; (2) which towns have no bookshop; (3) what can be walked to from a shop, and how far; (4) which shops specialise in crime fiction including its kinds; (5) who appeared at events in York and what it cost; (6) which books have no ISBN; (7) which authors were influenced, at any remove, by Rhona Blackwood; (8) which imprints belong ultimately to the Lodestone Group; (9) when Ex Libris opened and who says so; (10) which shops stock a book and the cheapest copy."@en ;
    dct:source    <https://github.com/pwin/Ontology_Course/blob/main/data/the-brief.md> .
""",
    expect=dict(min_triples=5),
)
specs.register("o07", "oboScope", "semopsCq")
