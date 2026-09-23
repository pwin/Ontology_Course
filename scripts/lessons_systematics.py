# -*- coding: utf-8 -*-
"""Module 02 -- Systematics: OntoClean, roles and phases, the backbone."""
from ontocat import o, Query
import specs

M = "02-systematics"

# The four meta-properties are recorded as annotations in a small namespace
# of the course's own, so that the taxonomy can be queried against the
# OntoClean constraints. gUFO's types are the published equivalent, and o13
# maps to them.
OC = """
# Borrowed annotation properties, declared so the file is OWL 2 DL on its own.
skos:editorialNote  a owl:AnnotationProperty .
rdfs:isDefinedBy    a owl:AnnotationProperty .

oc:rigidity    a owl:AnnotationProperty ; rdfs:label "rigidity"@en ;
    rdfs:comment "+R rigid: no instance can stop being one. ~R anti-rigid: every instance could stop. -R neither."@en .
oc:identity    a owl:AnnotationProperty ; rdfs:label "identity"@en ;
    rdfs:comment "+I carries a criterion of identity; +O supplies its own; -I carries none."@en .
oc:unity       a owl:AnnotationProperty ; rdfs:label "unity"@en ;
    rdfs:comment "+U every instance is a whole under one relation; ~U no instance is; -U neither."@en .
oc:dependence  a owl:AnnotationProperty ; rdfs:label "dependence"@en ;
    rdfs:comment "+D an instance exists only if some other thing does; -D it does not."@en .
"""

o(
    oid="o08", module=M,
    title="A concrete kind and a role: Person and Author",
    decides="Person is a rigid kind and Author is a role a person plays, so Author is placed under Person and never the other way round.",
    corner="referent",
    why="Ask of any class whether one of its instances could stop being one "
        "and still exist. Rhona Blackwood cannot stop being a person, "
        "because if she is not a person she is not anything, and so Person "
        "is rigid, which OntoClean writes +R. She could easily have stopped "
        "being an author, by never writing the second book or never the "
        "first, and she would still have been Rhona Blackwood, so Author is "
        "anti-rigid, written ~R, meaning that every instance of it could in "
        "principle fail to be one. Guarino and Welty call the first kind of "
        "class a type and the second a role, and of everything OntoClean "
        "offers this distinction is the one I find myself using most.\n\n"
        "A role carries two marks rather than one, since as well as being "
        "anti-rigid it is dependent, written +D: nobody is an author except "
        "by way of a work, so Author exists only in relation to Work, in "
        "the way that Customer exists only in relation to a sale and "
        "Employee only in relation to an employer. The Trail's own "
        "definition says as much, calling an author someone who wrote at "
        "least one work in this dataset.\n\n"
        "What follows for the hierarchy is a rule rather than a preference. "
        "An anti-rigid class may sit under a rigid one, because a role is "
        "always played by things of some kind, and Author under Person is "
        "therefore unobjectionable; but a rigid class may never sit under "
        "an anti-rigid one, because every person would then be an author by "
        "necessity, which is exactly what makes a role a role. o09 shows "
        "what that looks like when it goes wrong. The set picture says the "
        "same thing: the set of authors is a subset of the set of persons, "
        "and which subset it is changes as books get written, while the set "
        "of persons does not change at all on that account.",
    diagram="""
                     bs:Person   +R   rigid: an instance cannot stop being one
                        |             (Rhona is a person in every circumstance)
                        |  rdfs:subClassOf   allowed: anti-rigid under rigid
                        |
                     bs:Author   ~R   anti-rigid: every instance could stop
                                  +D   dependent: on some Work

   the set of authors is a subset of the set of persons, and
   which subset it is depends on what has been written. The set
   of persons does not depend on the books.
""",
    learn=[
        "Rigidity is the first question to ask of a class, and it is simply whether an instance could stop being one and still exist: +R if never, ~R if always possible.",
        "A role is both anti-rigid and dependent, and Author, Customer, Employee, Patient and Member are all of them things of some kind, in a relation, for a while.",
        "A role goes under the kind that plays it, and a kind never goes under a role.",
    ],
    body=OC + """
bs:Person
    a              owl:Class ;
    rdfs:label     "Person"@en ;
    rdfs:comment   "A human being."@en ;
    oc:rigidity    "+R" ;
    oc:identity    "+O" ;
    oc:dependence  "-D" .

bs:Author
    a                owl:Class ;
    rdfs:subClassOf  bs:Person ;
    rdfs:label       "Author"@en ;
    rdfs:comment     "Someone who wrote at least one work. A role: played by a person, for as long as the works exist."@en ;
    oc:rigidity      "~R" ;
    oc:identity      "+I" ;
    oc:dependence    "+D" .

bs:Work
    a              owl:Class ;
    rdfs:label     "Work"@en ;
    oc:rigidity    "+R" ;
    oc:identity    "+O" .

bt:author-rhona-blackwood
    a           bs:Author, bs:Person ;
    rdfs:label  "Rhona Blackwood"@en .
""",
    queries=[Query("The rigidity of every class", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class ?rigidity ?under WHERE {
  ?class oc:rigidity ?rigidity .
  OPTIONAL { ?class rdfs:subClassOf ?under }
} ORDER BY ?class""", rows=3)],
    check=dict(profile=True, reason=True),
    expect=dict(dl=True, consistent=True, classes=3),
)
specs.register("o08", "ontocleanCacm", "ontocleanWp")

o(
    oid="o09", module=M,
    title="The subsumption that will not bear weight",
    decides="'Every bookshop is a trail member' is read as a role, not a subclass, and the draft that put Bookshop under TrailMember is reversed.",
    corner="referent",
    why="The committee's first draft said that a bookshop is a trail "
        "member, and somebody wrote it down as Bookshop rdfs:subClassOf "
        "TrailMember, which reads naturally enough and is nonetheless "
        "wrong. OntoClean says why in a single line: an anti-rigid class "
        "cannot subsume a rigid one. Being on the trail is something a shop "
        "is for now, since the brief tells us that shops have left and one "
        "has joined twice, so TrailMember is ~R, while Bookshop is +R, "
        "because a shop that leaves the trail is still perfectly well a "
        "bookshop. Put the rigid class under the anti-rigid one and every "
        "bookshop becomes a member by necessity, which is precisely what "
        "the brief denies.\n\n"
        "The right way round is TrailMember under Bookshop, so that a "
        "member is a bookshop, for a while, in a relation to the trail; "
        "then a shop can leave and the model has no opinion about whether "
        "it stops being a shop.\n\n"
        "The English 'is a' is the trap here, because 'a bookshop is a "
        "trail member' and 'a translation is a work' use the same two words "
        "for quite different claims, the first about a role that every "
        "current member happens to play and the second about what a "
        "translation is in every circumstance. Rigidity is how you tell "
        "them apart when the grammar will not. This file keeps the wrong "
        "draft in place so that the query at the end has something to find, "
        "and o12 shows the corrected version.",
    diagram="""
   the draft                                the rule

   bs:TrailMember   ~R  (for now)           an anti-rigid class (~R)
        ^                                    may not subsume
        |  rdfs:subClassOf    <- wrong       a rigid class (+R)
        |
   bs:Bookshop      +R  (always)

   'every bookshop is a member by necessity': what the model says,
   and what the brief denies. Reversed, it says what was meant:
   a member is a bookshop, in a relation to the trail, for a while.
""",
    learn=[
        "'Is a' in English covers both essence and role, and rigidity is what tells the two apart.",
        "An anti-rigid class over a rigid one is forbidden, it is the commonest error in a first draft, and a query over the annotations will find it.",
        "Membership of a trail, a scheme or a club is a role, so model it under the kind that plays it, or as a relation.",
    ],
    body=OC + """
bs:Bookshop
    a              owl:Class ;
    rdfs:label     "Bookshop"@en ;
    rdfs:comment   "A business that sells books from premises."@en ;
    oc:rigidity    "+R" ;
    oc:identity    "+O" .

bs:TrailMember
    a              owl:Class ;
    rdfs:label     "Trail member"@en ;
    rdfs:comment   "A bookshop that is currently on the trail. Shops join and leave."@en ;
    oc:rigidity    "~R" ;
    oc:identity    "+I" ;
    oc:dependence  "+D" .

# The draft, kept so the query below can find it: rigid under anti-rigid.
bs:Bookshop
    rdfs:subClassOf  bs:TrailMember .
""",
    queries=[Query("Rigid classes placed under anti-rigid ones", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?sub ?super WHERE {
  ?sub rdfs:subClassOf ?super .
  ?sub oc:rigidity "+R" .
  ?super oc:rigidity "~R" .
}""", rows=1)],
    check=dict(profile=True),
    expect=dict(dl=True, classes=2),
)
specs.register("o09", "ontocleanCacm", "ontocleanHb")

o(
    oid="o10", module=M,
    title="Identity: what makes two of them the same",
    decides="Work, Edition and Copy carry different criteria of identity, so they are three classes and disjoint; Work is what the Trail keeps, with the compromise written on it.",
    corner="referent",
    why="A class carries a criterion of identity when there is a way to "
        "tell whether two of its instances are one thing or two. Two works "
        "are the same if they have the same author and the same text, "
        "whatever printing you happen to hold; two editions are the same if "
        "they share an ISBN, whatever copy you hold; and two copies are the "
        "same only if they are the same object on the same shelf. That is "
        "one word, three tests, and a thing that passes one can fail "
        "another, since two copies of one edition are the same edition and "
        "different copies.\n\n"
        "OntoClean's rule follows from that. Classes with incompatible "
        "criteria of identity are disjoint, and a class that carries a "
        "criterion, +I, may not sit above one that carries none, -I, "
        "because the criterion is inherited downward. The practical use "
        "runs in the other direction, though: when a draft has one class "
        "doing two jobs, the criterion of identity is how you notice, and "
        "it is how you decide how many classes there really ought to be.\n\n"
        "The Trail's bs:Work is a work and an edition in one class, since "
        "it has an author and a text and it also has an ISBN, pages and a "
        "price. That is a compromise, made because the dataset never needs "
        "to say that two editions are one work, and it is written on the "
        "class as an editorial note, which is all the difference between a "
        "compromise and a mistake. The set picture makes it plain enough: a "
        "set needs a rule for when two members are one member, and 'same "
        "ISBN' and 'same text' are not the same rule.",
    diagram="""
   class            two of them are the same if       identity   unity

   Work             same author and text               +O         +U  (a whole under 'is a text')
   Edition          same ISBN                          +O         +U
   Copy             same physical object               +O         +U
   StockLine        same shop and same edition         +O         -U  (a count, not a whole)

   incompatible criteria  =>  disjoint classes
   bs:Work in the Trail = Work + Edition, by a recorded decision
""",
    learn=[
        "A criterion of identity is the test for one or two, a class that has one is a sortal, and different tests mean different classes.",
        "Book is three sortals, work and edition and copy, and deciding how many of them you need is a scope decision that belongs on the class in writing.",
        "Unity asks whether each instance is a whole, so that a stock line, being a count of copies, is ~U where a work is +U.",
    ],
    body=OC + """
bs:Work
    a                   owl:Class ;
    rdfs:label          "Work"@en ;
    rdfs:comment        "A book: what an author wrote, in a particular published form."@en ;
    skos:editorialNote  "Work and Edition in one class, by decision: the Trail never needs two editions of one work. The ISBN, pages and price are an edition's; the author and title are a work's. Split the class the day a second edition appears."@en ;
    oc:rigidity         "+R" ;
    oc:identity         "+O" ;
    oc:unity            "+U" .

bs:Copy
    a                   owl:Class ;
    rdfs:label          "Copy"@en ;
    rdfs:comment        "A physical copy of a work, on a shelf. Not modelled individually in the Trail; counted in bs:StockRecord."@en ;
    oc:rigidity         "+R" ;
    oc:identity         "+O" ;
    oc:unity            "+U" .

bs:StockRecord
    a                   owl:Class ;
    rdfs:label          "Stock record"@en ;
    rdfs:comment        "How many copies of a work one shop holds, at what price. A count, not a whole."@en ;
    oc:rigidity         "+R" ;
    oc:identity         "+O" ;
    oc:unity            "-U" .

[] a owl:AllDisjointClasses ;
   owl:members ( bs:Work bs:Copy bs:StockRecord ) .
""",
    check=dict(profile=True, reason=True),
    expect=dict(dl=True, consistent=True, classes=3),
)
specs.register("o10", "ontocleanHb", "ontocleanWp")

o(
    oid="o11", module=M,
    title="Phases: the same thing, for a while",
    decides="Living and dead authors, and past and scheduled events, are phases of one kind, not kinds of their own; gist's ContemporaryEvent and HistoricalEvent are the published example.",
    corner="referent",
    why="A role is anti-rigid because of a relation to something else, an "
        "author because of a work and a member because of a trail, whereas "
        "a phase is anti-rigid because of a condition inside the thing "
        "itself, as with a living person, a scheduled event or a child, and "
        "the instance simply passes through it. Both are ~R, a phase is -D "
        "and a role is +D, and that is the whole of the difference. "
        "Guizzardi's UFO keeps the two apart as Phase and Role, and gUFO "
        "carries them as gufo:Phase and gufo:Role.\n\n"
        "gist has two phases in plain sight, since gist:ContemporaryEvent "
        "is an event that has started and not ended while "
        "gist:HistoricalEvent is one that has ended, and the scope note on "
        "the first says it exactly: when the event actually ends, it will "
        "cease being contemporary. The same event passes from the one to "
        "the other and stays a gist:Event throughout, and gistUFO types "
        "gist:Offer and gist:ContingentObligation as phases of a commitment "
        "for the same reason.\n\n"
        "The Trail records death as the absence of bs:died and an event's "
        "pastness by its date, so neither is a class, and that is the usual "
        "and I think the right choice, because a phase is often better "
        "carried by a property than by a subclass: the property changes, "
        "and a class assertion should not have to. Model a phase as a class "
        "when you need to say things about the members of the phase as a "
        "set, and leave it as a property when all you will do is ask.",
    diagram="""
   anti-rigid, two ways

   ROLE    ~R  +D    by a relation to something else
           Author (to a Work)   TrailMember (to the trail)   Publisher (to works published)

   PHASE   ~R  -D    by a condition in the thing itself
           LivingPerson (no bs:died)     ScheduledEvent (a planned start, no actual one)
           gist:ContemporaryEvent -> gist:HistoricalEvent, one event, two phases

   In the Trail, both phases here are properties, not classes:
   ask 'FILTER NOT EXISTS { ?p bs:died ?y }' rather than type a class.
""",
    learn=[
        "A phase is anti-rigid from the inside and a role is anti-rigid from a relation, and both go under the kind rather than above it.",
        "gist models the two phases of an event as classes because it wants to say things about all current events; the Trail does not, so it uses a property instead.",
        "A class is for saying something about a set of members, so if all you will do is ask, a property and a query are cheaper and change more gracefully.",
    ],
    body=OC + """
bs:Event
    a             owl:Class ;
    rdfs:label    "Event"@en ;
    rdfs:comment  "Something that happened, or will happen, at a bookshop on a given day."@en ;
    oc:rigidity   "+R" ;
    oc:identity   "+O" .

# Two phases of an event, as gist has them. Shown here as classes so the
# distinction is visible; the Trail carries the same information as dates.
bs:ScheduledEvent
    a                owl:Class ;
    rdfs:subClassOf  bs:Event ;
    rdfs:label       "Scheduled event"@en ;
    rdfs:comment     "An event with a planned date that has not yet happened. A phase: the same event becomes a past event."@en ;
    oc:rigidity      "~R" ;
    oc:dependence    "-D" .

bs:PastEvent
    a                owl:Class ;
    rdfs:subClassOf  bs:Event ;
    rdfs:label       "Past event"@en ;
    rdfs:comment     "An event that has taken place. A phase."@en ;
    oc:rigidity      "~R" ;
    oc:dependence    "-D" .

# The same distinction as a property and a query, which is what the Trail does.
bs:eventDate  a owl:DatatypeProperty ; rdfs:label "event date"@en .

bt:event-inkwell-2025-03-08
    a             bs:Event ;
    rdfs:label    "Reading with Rab Fingal"@en ;
    bs:eventDate  "2025-03-08T19:00:00"^^xsd:dateTime .
""",
    notes="The Trail's data types event dates as xsd:date, which is not in the OWL 2 datatype map, so a file "
          "that used one would fall out of OWL 2 DL. This file uses xsd:dateTime, which is in the map. o50 is about that trap, and the SPARQL course's README has the full story.",
    queries=[Query("Anti-rigid classes, and whether each is a role or a phase", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
SELECT ?class (IF(?d = "+D", "role", "phase") AS ?kind) WHERE {
  ?class oc:rigidity "~R" ; oc:dependence ?d .
}""", rows=2)],
    check=dict(profile=True),
    expect=dict(dl=True, classes=3),
)
specs.register("o11", "gufo", "gistUfo")

o(
    oid="o12", module=M,
    title="The backbone",
    decides="The rigid classes of the Trail form its backbone taxonomy; roles and phases hang off it and never form part of it.",
    corner="referent",
    why="Strip a taxonomy down to its rigid classes and what is left is the "
        "backbone, the kinds every instance necessarily belongs to, "
        "arranged by subsumption. Guarino and Welty give the backbone its "
        "name and its test, which is that every instance in the domain "
        "falls under some backbone class and stays under it, the backbone "
        "being made only of classes that nothing can leave; the roles and "
        "phases are then attached beneath whichever backbone class plays "
        "them. A taxonomy built this way can be extended without "
        "collapsing, because the part that carries identity never depends "
        "on the part that changes.\n\n"
        "The Trail's backbone has ten kinds at the top, which are Place, "
        "Bookshop, Person, Publisher, Work, Series, Event, TrailSegment, "
        "StockRecord and Source, with four subkinds under Place and one "
        "under Work. Author is the one role in the shipped vocabulary, and "
        "Translation is not a role, because a translation is a translation "
        "in every circumstance and is therefore a subkind. Publisher is a "
        "fair argument either way: the Trail makes it a kind, gist would "
        "call it a role of an organisation, and the argument is recorded "
        "here rather than settled, with o14 giving the vocabulary to record "
        "it in.\n\n"
        "In set terms the backbone is the family of sets that nothing "
        "leaves, and the roles are subsets of them that things enter and "
        "leave.",
    diagram="""
   the backbone (all +R)                          hanging off it (~R)

   Place
     Settlement  CouncilArea  Region  Country
   Bookshop  . . . . . . . . . . . . . . . . . . . TrailMember (role)
   Person  . . . . . . . . . . . . . . . . . . . . Author (role)
   Publisher  (a kind here; a role of Organization in gist)
   Work
     Translation  (a subkind: a translation in every circumstance)
   Series   Event   TrailSegment   StockRecord   Source

   every particular falls under a backbone class, and stays there
""",
    learn=[
        "The backbone is the rigid part of the taxonomy, so build it first and let the roles hang off it.",
        "A subkind is rigid and inherits its identity criterion, as Translation does from Work and Settlement from Place, whereas a role is not a subkind at all.",
        "Where a class could be either, say which you chose and why; Publisher is the Trail's example of that.",
    ],
    body=OC + """
bs:Place        a owl:Class ; rdfs:label "Place"@en ;       oc:rigidity "+R" ; oc:identity "+O" .
bs:Settlement   a owl:Class ; rdfs:subClassOf bs:Place ; rdfs:label "Settlement"@en ;   oc:rigidity "+R" ; oc:identity "+I" .
bs:CouncilArea  a owl:Class ; rdfs:subClassOf bs:Place ; rdfs:label "Council area"@en ; oc:rigidity "+R" ; oc:identity "+I" .
bs:Region       a owl:Class ; rdfs:subClassOf bs:Place ; rdfs:label "Region"@en ;       oc:rigidity "+R" ; oc:identity "+I" .
bs:Country      a owl:Class ; rdfs:subClassOf bs:Place ; rdfs:label "Country"@en ;      oc:rigidity "+R" ; oc:identity "+I" .
bs:Bookshop     a owl:Class ; rdfs:label "Bookshop"@en ;    oc:rigidity "+R" ; oc:identity "+O" .
bs:Person       a owl:Class ; rdfs:label "Person"@en ;      oc:rigidity "+R" ; oc:identity "+O" .
bs:Publisher    a owl:Class ; rdfs:label "Publisher"@en ;   oc:rigidity "+R" ; oc:identity "+O" ;
    skos:editorialNote "Treated as a kind here. gist would make it a role of an Organization; the Trail has no organisations that are not publishers or shops, so the role has nothing to be a role of."@en .
bs:Work         a owl:Class ; rdfs:label "Work"@en ;        oc:rigidity "+R" ; oc:identity "+O" .
bs:Translation  a owl:Class ; rdfs:subClassOf bs:Work ; rdfs:label "Translation"@en ; oc:rigidity "+R" ; oc:identity "+I" .
bs:Series       a owl:Class ; rdfs:label "Series"@en ;      oc:rigidity "+R" ; oc:identity "+O" .
bs:Event        a owl:Class ; rdfs:label "Event"@en ;       oc:rigidity "+R" ; oc:identity "+O" .
bs:TrailSegment a owl:Class ; rdfs:label "Trail segment"@en ; oc:rigidity "+R" ; oc:identity "+O" .
bs:StockRecord  a owl:Class ; rdfs:label "Stock record"@en ; oc:rigidity "+R" ; oc:identity "+O" .
bs:Source       a owl:Class ; rdfs:label "Source"@en ;      oc:rigidity "+R" ; oc:identity "+O" .

# The roles, hanging off the backbone.
bs:Author       a owl:Class ; rdfs:subClassOf bs:Person ;   rdfs:label "Author"@en ;       oc:rigidity "~R" ; oc:dependence "+D" .
bs:TrailMember  a owl:Class ; rdfs:subClassOf bs:Bookshop ; rdfs:label "Trail member"@en ; oc:rigidity "~R" ; oc:dependence "+D" .
""",
    queries=[
        Query("The backbone: rigid classes and their rigid parents", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class ?parent WHERE {
  ?class oc:rigidity "+R" .
  OPTIONAL { ?class rdfs:subClassOf ?parent . ?parent oc:rigidity "+R" }
} ORDER BY ?parent ?class""", rows=15),
        Query("Roles, and the backbone class each hangs from", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?role ?kind WHERE { ?role oc:rigidity "~R" ; rdfs:subClassOf ?kind . ?kind oc:rigidity "+R" }""", rows=2),
    ],
    check=dict(profile=True, reason=True, metrics=True),
    expect=dict(dl=True, consistent=True, classes=17),
)
specs.register("o12", "ontocleanHb", "ontocleanCacm")

o(
    oid="o13", module=M,
    title="The taxonomy checks itself",
    decides="OntoClean's constraints are written as SPARQL queries over the annotations, so that a taxonomy can be checked in the editor before a reasoner ever sees it.",
    corner="referent",
    why="Each meta-property inherits downward in one direction, and each "
        "constraint is then the same sentence with a different letter in "
        "it, that a class marked one way may not subsume a class marked the "
        "other. Anti-rigid may not subsume rigid; a class with a criterion "
        "of identity may not subsume one without; unity may not subsume "
        "non-unity, and anti-unity may not subsume unity; dependent may not "
        "subsume independent; and two classes with incompatible criteria of "
        "identity must be disjoint.\n\n"
        "Because the marks are annotations in the graph, each constraint is "
        "a SPARQL query, and a taxonomy can be checked in the editor's "
        "SPARQL panel with nothing installed at all. This file seeds two "
        "violations, the TrailMember draft from o09 and a dependent class "
        "over an independent one, and each of them breaks two constraints "
        "at once, so two of the queries come back with two rows. A clean "
        "run is an empty result, which is the very thing the SHACL course "
        "warns about, since an empty result also means the query matched "
        "nothing; keep the seeded file, then, to prove that the queries "
        "fire.\n\n"
        "Neither the Ontology Quality Suite nor OQuaRE has anything to say "
        "about OntoClean, and that is no oversight in either of them, "
        "because rigidity is not in the graph unless somebody writes it "
        "there. This is the cheapest way I know of writing it there.",
    diagram="""
   inherits downward     so the constraint is            query

   ~R                    ~R may not subsume +R            rigid under anti-rigid
   +I                    +I may not subsume -I            no-identity under identity
   +U, ~U                +U may not subsume -U            non-unity under unity
                         ~U may not subsume +U            unity under anti-unity
   +D                    +D may not subsume -D            independent under dependent
   (identity)            incompatible IC => disjoint      checked in o10

   seeded here: Bookshop (+R, -D) under TrailMember (~R, +D)
                Person   (+R, -D) under Author      (~R, +D)
   each link breaks the rigidity rule and the dependence rule at once
""",
    learn=[
        "Every OntoClean constraint has the form 'X may not subsume Y', and written as a query over the annotations each one is a single line.",
        "Keep a file with the violations in it, because a check that has never fired is indistinguishable from a check that cannot.",
        "No metric suite sees rigidity, so it has to be recorded, and once it is recorded it can be checked like anything else in the graph.",
    ],
    body=OC + """
bs:Bookshop     a owl:Class ; oc:rigidity "+R" ; oc:identity "+O" ; oc:unity "+U" ; oc:dependence "-D" .
bs:TrailMember  a owl:Class ; oc:rigidity "~R" ; oc:identity "+I" ; oc:unity "+U" ; oc:dependence "+D" .
bs:Person       a owl:Class ; oc:rigidity "+R" ; oc:identity "+O" ; oc:unity "+U" ; oc:dependence "-D" .
bs:Author       a owl:Class ; oc:rigidity "~R" ; oc:identity "+I" ; oc:unity "+U" ; oc:dependence "+D" .
bs:Place        a owl:Class ; oc:rigidity "+R" ; oc:identity "+O" ; oc:unity "-U" ; oc:dependence "-D" .
bs:Settlement   a owl:Class ; oc:rigidity "+R" ; oc:identity "+I" ; oc:unity "+U" ; oc:dependence "-D" .

# Two seeded violations, so that the queries can be seen to fire.
bs:Bookshop  rdfs:subClassOf  bs:TrailMember .     # rigid under anti-rigid
bs:Person    rdfs:subClassOf  bs:Author .          # independent under dependent

# Two sound links, for contrast.
bs:Settlement  rdfs:subClassOf  bs:Place .
bs:Author      rdfs:subClassOf  bs:Person .
""",
    queries=[
        Query("Rigid under anti-rigid", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?sub ?super WHERE { ?sub rdfs:subClassOf ?super ; oc:rigidity "+R" . ?super oc:rigidity "~R" }""", rows=2),
        Query("Independent under dependent", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?sub ?super WHERE { ?sub rdfs:subClassOf ?super ; oc:dependence "-D" . ?super oc:dependence "+D" }""", rows=2),
        Query("No identity under identity", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?sub ?super WHERE { ?sub rdfs:subClassOf ?super ; oc:identity "-I" . ?super oc:identity ?i . FILTER(?i IN ("+I", "+O")) }""", rows=0),
        Query("Non-unity under unity", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?sub ?super WHERE { ?sub rdfs:subClassOf ?super ; oc:unity "-U" . ?super oc:unity "+U" }""", rows=0),
    ],
    check=dict(profile=True),
    expect=dict(dl=True),
)
specs.register("o13", "ontocleanHb", "semopsTestGate")

o(
    oid="o14", module=M,
    title="Reading gist through OntoClean",
    decides="The Trail's classes are typed with gUFO's Kind, SubKind, Role and Phase, the way gistUFO types gist's, and the typing is checked to agree with the annotations.",
    corner="referent",
    why="gistUFO is a small published file that types every gist class with "
        "one of gUFO's kinds of class, so that gist:Person is a gufo:Kind, "
        "gist:Contract a gufo:SubKind, gist:ContractTerm a gufo:Role, "
        "gist:Offer a gufo:Phase and gist:Category a "
        "gufo:AbstractIndividualType. Those are OntoClean's distinctions "
        "under names: a Kind is rigid and supplies identity, a SubKind is "
        "rigid and inherits it, a Role is anti-rigid and relational, and a "
        "Phase is anti-rigid and intrinsic. Reading that file is the "
        "quickest way I know to see the theory applied to a real ontology "
        "by people who then had to live with the result.\n\n"
        "The typing is done by punning, since gist:Person is an owl:Class "
        "and is also an individual of the class gufo:Kind; OWL 2 DL allows "
        "one IRI to be both and the reasoner keeps the two readings apart, "
        "as module 07 explains, and here it is enough that the profile "
        "checker agrees.\n\n"
        "This file types the Trail's classes the same way and adds one "
        "query, which asks that a class typed gufo:Role carry ~R and +D in "
        "the annotations and that a gufo:Kind carry +R. Where the two "
        "disagree one of them is wrong, and the disagreement is worth more "
        "than either record on its own. gist's own rule for naming "
        "instances, that the infix is the most specific rigid class, is the "
        "same theory put to a practical end: never name an instance after a "
        "role, because the role may end and the name should not.",
    diagram="""
   gUFO type          OntoClean marks        gist example (from gistUFO)    Trail

   gufo:Kind          +R, +O                 gist:Person, gist:Agreement    bs:Person, bs:Bookshop, bs:Work
   gufo:SubKind       +R, +I (inherited)     gist:Contract, gist:Account    bs:Settlement, bs:Translation
   gufo:Role          ~R, +D                 gist:ContractTerm, gist:Message bs:Author, bs:TrailMember
   gufo:Phase         ~R, -D                 gist:Offer, gist:ContingentObligation  (bs:PastEvent, o11)
   gufo:Category      +R, -I (a mixin)       gist:Content, gist:Composite   --

   one IRI, two readings:  bs:Author a owl:Class .   bs:Author a gufo:Role .
""",
    learn=[
        "gUFO's Kind, SubKind, Role, Phase and Category are OntoClean's distinctions as a vocabulary you can assert, and gistUFO applies them across the whole of gist.",
        "Typing a class with a metaclass is punning, and it stays within OWL 2 DL, as the profile checker confirms.",
        "Two records of the same decision, checked against each other, catch more than either alone, and here the gUFO type and the OntoClean marks have to agree.",
    ],
    body=OC + """
# gUFO's types, declared so this file stands on its own in OWL 2 DL.
gufo:Kind     a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .
gufo:SubKind  a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .
gufo:Role     a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .
gufo:Phase    a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .

bs:Person       a owl:Class, gufo:Kind ;    oc:rigidity "+R" ; oc:dependence "-D" .
bs:Bookshop     a owl:Class, gufo:Kind ;    oc:rigidity "+R" ; oc:dependence "-D" .
bs:Work         a owl:Class, gufo:Kind ;    oc:rigidity "+R" ; oc:dependence "-D" .
bs:Place        a owl:Class, gufo:Kind ;    oc:rigidity "+R" ; oc:dependence "-D" .
bs:Settlement   a owl:Class, gufo:SubKind ; oc:rigidity "+R" ; oc:dependence "-D" ; rdfs:subClassOf bs:Place .
bs:Translation  a owl:Class, gufo:SubKind ; oc:rigidity "+R" ; oc:dependence "-D" ; rdfs:subClassOf bs:Work .
bs:Author       a owl:Class, gufo:Role ;    oc:rigidity "~R" ; oc:dependence "+D" ; rdfs:subClassOf bs:Person .
bs:TrailMember  a owl:Class, gufo:Role ;    oc:rigidity "~R" ; oc:dependence "+D" ; rdfs:subClassOf bs:Bookshop .
bs:PastEvent    a owl:Class, gufo:Phase ;   oc:rigidity "~R" ; oc:dependence "-D" .

# A deliberate disagreement, for the query to find: typed a Kind, marked a role.
bs:Publisher    a owl:Class, gufo:Kind ;    oc:rigidity "~R" ; oc:dependence "+D" .
""",
    queries=[
        Query("Where the gUFO type and the OntoClean marks disagree", """
PREFIX oc: <https://example.org/bookshop-trail/ontoclean#>
PREFIX gufo: <http://purl.org/nemo/gufo#>
SELECT ?class ?type ?rigidity ?dependence WHERE {
  ?class a ?type ; oc:rigidity ?rigidity ; oc:dependence ?dependence .
  FILTER(?type IN (gufo:Kind, gufo:SubKind, gufo:Role, gufo:Phase))
  FILTER( (?type IN (gufo:Kind, gufo:SubKind) && ?rigidity != "+R")
       || (?type = gufo:Role  && !(?rigidity = "~R" && ?dependence = "+D"))
       || (?type = gufo:Phase && !(?rigidity = "~R" && ?dependence = "-D")) )
}""", rows=1),
    ],
    check=dict(profile=True, reason=True),
    expect=dict(dl=True, consistent=True),
)
specs.register("o14", "gistUfo", "gufo")
