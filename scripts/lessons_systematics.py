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
    why="Ask of a class: could one of its instances stop being one and still "
        "exist? Rhona Blackwood cannot stop being a person; if she is not a "
        "person she is not anything. Person is rigid, written +R. She could "
        "have stopped being an author, by never writing the second book, or "
        "never the first; she would still be Rhona Blackwood. Author is "
        "anti-rigid, written ~R: every instance of it could, in principle, "
        "fail to be one. Guarino and Welty call the first kind of class a "
        "type and the second a role, and the distinction is the most useful "
        "single thing OntoClean offers.\n\n"
        "A role has two more marks. It is anti-rigid, and it is dependent, "
        "written +D: nobody is an author except by way of a work. Author "
        "exists only in relation to Work, in the way that Customer exists "
        "only in relation to a sale and Employee only in relation to an "
        "employer. The Trail's own definition says so: 'someone who wrote at "
        "least one work in this dataset'.\n\n"
        "The consequence for the hierarchy is a rule, not a preference. An "
        "anti-rigid class may sit under a rigid one, because a role is "
        "played by things of some kind: Author under Person is fine. A rigid "
        "class may never sit under an anti-rigid one, because every person "
        "would then be an author by necessity, which contradicts the role "
        "being optional. o09 shows what that looks like when it goes wrong. "
        "The set picture is the same: the set of authors is a subset of the "
        "set of persons, and which subset it is changes as books are "
        "written; the set of persons does not change because of it.",
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
        "Rigidity is the first question to ask of a class: could an instance stop being one and still exist? +R if never, ~R if always possible.",
        "A role is anti-rigid and dependent. Author, Customer, Employee, Patient, Member: things of some kind, in a relation, for a while.",
        "A role goes under the kind that plays it. Never put a kind under a role.",
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
    why="The committee's first draft said 'a bookshop is a trail member', "
        "and someone wrote it down as Bookshop rdfs:subClassOf TrailMember. "
        "It reads naturally. It is wrong, and OntoClean says why in one "
        "line: an anti-rigid class cannot subsume a rigid one. Being on the "
        "trail is something a shop is for now; the brief says shops have "
        "left and one has joined twice. TrailMember is ~R. Bookshop is +R, "
        "because a shop that leaves the trail is still a bookshop. Put the "
        "rigid class under the anti-rigid one and every bookshop is a member "
        "by necessity, which is precisely what the brief denies.\n\n"
        "The right way round is TrailMember under Bookshop: a member is a "
        "bookshop, for a while, in a relation to the trail. Then a shop can "
        "leave, and the model has no opinion about whether it stops being a "
        "shop.\n\n"
        "The English 'is a' is the trap. 'A bookshop is a trail member' and "
        "'a translation is a work' use the same two words for different "
        "claims: the first is about a role every current member happens to "
        "play, the second is about what a translation is in every circumstance. "
        "Rigidity is how you tell them apart when the grammar will not. This "
        "file keeps the wrong draft in place so the query at the end can "
        "find it; o12 shows the corrected version.",
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
        "'Is a' in English covers both essence and role. Rigidity tells them apart.",
        "~R over +R is forbidden. It is the commonest error in a first draft, and a query over the annotations finds it.",
        "Membership of a trail, a scheme, a club is a role. Model it under the kind that plays it, or as a relation.",
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
    why="A class carries a criterion of identity if there is a way to tell "
        "whether two of its instances are one thing or two. Two works are the "
        "same if they have the same author and the same text, whatever "
        "printing you hold. Two editions are the same if they have the same "
        "ISBN, whatever copy you hold. Two copies are the same only if they "
        "are the same object, on the same shelf. Same word, three tests, and "
        "a thing that passes one can fail another: two copies of one "
        "edition are the same edition and different copies.\n\n"
        "OntoClean's rule follows: classes with incompatible criteria of "
        "identity are disjoint, and a class that carries a criterion (+I) "
        "may not sit above one that carries none (-I), because the criterion "
        "is inherited downward. The practical use is in the other direction. "
        "When a draft has one class doing two jobs, the criterion of identity "
        "is how you notice, and it is how you decide how many classes there "
        "really are.\n\n"
        "The Trail's bs:Work is a work and an edition in one class: it has an "
        "author and a text, and it also has an ISBN, pages and a price. That "
        "is a compromise, made because the dataset never needs to say that "
        "two editions are one work. It is written on the class as an "
        "editorial note, which is the difference between a compromise and a "
        "mistake. The set picture makes it plain: a set needs a rule for "
        "when two members are one member, and 'same ISBN' and 'same text' "
        "are different rules.",
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
        "A criterion of identity is the test for 'one or two'. A class that has one is a sortal; different tests mean different classes.",
        "Book is three sortals: work, edition, copy. Deciding how many you need is a scope decision, and it should be written on the class.",
        "Unity asks whether each instance is a whole. A stock line is a count of copies; a work is one thing. Mereological sums are ~U.",
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
    why="A role is anti-rigid because of a relation to something else: an "
        "author because of a work, a member because of a trail. A phase is "
        "anti-rigid because of a condition inside the thing itself: a living "
        "person, a scheduled event, a child. The instance passes through it. "
        "Both are ~R; a phase is -D, a role is +D, and that is the whole "
        "difference. Guizzardi's UFO keeps the two apart as Phase and Role, "
        "and gUFO carries them as gufo:Phase and gufo:Role.\n\n"
        "gist has two phases in plain sight. gist:ContemporaryEvent is an "
        "event that has started and not ended; gist:HistoricalEvent is one "
        "that has ended. The scope note on the first says it exactly: 'when "
        "the event actually ends, it will cease being contemporary'. The "
        "same event passes from one to the other, and it stays a gist:Event "
        "throughout. gistUFO types gist:Offer and gist:ContingentObligation "
        "as phases of a commitment for the same reason.\n\n"
        "The Trail records death as the absence of bs:died, and an event's "
        "pastness by its date. Neither is a class. That is the usual and "
        "right choice: a phase is often better carried by a property than by "
        "a subclass, because the property changes and a class assertion "
        "should not have to. Model a phase as a class when you need to say "
        "things about the members of the phase as a set; leave it as a "
        "property when you only need to ask.",
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
        "A phase is anti-rigid from the inside; a role is anti-rigid from a relation. Both go under the kind, never above it.",
        "gist models the two phases of an event as classes because it wants to say things about all current events. The Trail does not, so it uses a property.",
        "A class is for saying something about a set of members. If all you will do is ask, a property and a query are cheaper and change more gracefully.",
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
          "that used one would fall out of OWL 2 DL. This file uses xsd:dateTime, which is in the map. o57 is "
          "about that trap, and the SPARQL course's README has the full story.",
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
        "backbone: the kinds every instance necessarily belongs to, arranged "
        "by subsumption. Guarino and Welty give the backbone its name and its "
        "test: every instance of a backbone class is an instance of exactly "
        "one lowest backbone class, and stays so. The roles and phases are "
        "then attached beneath the backbone class that plays them. A "
        "taxonomy built this way can be extended without collapsing, because "
        "the part that carries identity never depends on the part that "
        "changes.\n\n"
        "The Trail's backbone has ten kinds at the top: Place, Bookshop, "
        "Person, Publisher, Work, Series, Event, TrailSegment, StockRecord "
        "and Source. Place has four subkinds, Work has one. Author is the one "
        "role in the shipped vocabulary; Translation is not a role, because a translation is a translation in every circumstance, so it is a subkind. "
        "Publisher is a fair argument: the Trail makes it a kind, and gist "
        "would call it a role of an organisation. That argument is recorded "
        "here rather than settled, and o13 gives the vocabulary to record it "
        "in.\n\n"
        "The set picture: the backbone partitions the domain. Every "
        "particular is in exactly one leaf set of the backbone, and the "
        "roles are subsets that cut across time.",
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

   backbone classes partition the domain; each particular has exactly one leaf
""",
    learn=[
        "The backbone is the rigid part of the taxonomy. Build it first, and let the roles hang off it.",
        "A subkind is rigid and inherits its identity criterion: Translation under Work, Settlement under Place. A role is not a subkind.",
        "Where a class could be either, say which you chose and why. Publisher is the Trail's example.",
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
        "constraint is the same sentence with a different letter: a class "
        "marked one way may not subsume a class marked the other. Anti-rigid "
        "may not subsume rigid. A class with a criterion of identity may not "
        "subsume one without. Unity may not subsume non-unity, and anti-unity "
        "may not subsume unity. Dependent may not subsume independent. And "
        "two classes with incompatible criteria of identity must be "
        "disjoint.\n\n"
        "Because the marks are annotations in the graph, each constraint is "
        "a SPARQL query, and a taxonomy can be checked in the editor's "
        "SPARQL panel with nothing installed. This file seeds two "
        "violations, the TrailMember draft from o09 and a dependent class "
        "over an independent one, and the queries find both. A clean run is "
        "an empty result, which is the same thing the SHACL course warns "
        "about: an empty result also means the query matched nothing, so "
        "keep the seeded file to prove the queries fire.\n\n"
        "The Ontology Quality Suite has no OntoClean check and OQuaRE has no "
        "OntoClean metric. That is not an oversight in either; rigidity is "
        "not in the graph unless someone writes it there. This is the "
        "cheapest way to write it there.",
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
        "Every OntoClean constraint has the form 'X may not subsume Y'. Written as a query over the annotations, each is a one-line check.",
        "Keep a file with the violations in it. A check that has never fired is indistinguishable from a check that cannot.",
        "No metric suite sees rigidity. It has to be recorded, and once recorded it can be checked like anything else.",
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
        "one of gUFO's kinds of class: gist:Person is a gufo:Kind, "
        "gist:Contract a gufo:SubKind, gist:ContractTerm a gufo:Role, "
        "gist:Offer a gufo:Phase, gist:Category a gufo:AbstractIndividualType. "
        "Those are OntoClean's distinctions with names: a Kind is rigid and "
        "supplies identity, a SubKind is rigid and inherits it, a Role is "
        "anti-rigid and relational, a Phase is anti-rigid and intrinsic. "
        "Reading the file is the fastest way to see the theory applied to a "
        "real ontology by people who had to live with the result.\n\n"
        "The typing is done by punning: gist:Person is an owl:Class, and it "
        "is also an individual of the class gufo:Kind. OWL 2 DL allows one "
        "IRI to be both, and the reasoner keeps the two readings apart. "
        "Module 07 says more; here it is enough that the profile checker "
        "agrees.\n\n"
        "This file types the Trail's classes the same way and adds one "
        "query: a class typed gufo:Role must carry ~R and +D in the "
        "annotations, and a gufo:Kind must carry +R. If the two disagree, "
        "one of them is wrong, and the disagreement is worth more than "
        "either alone. gist's own naming rule for instances, 'the most "
        "specific rigid class', is the same theory used for a practical end: "
        "never name an instance after a role, because the role may end and "
        "the name should not.",
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
        "gUFO's Kind, SubKind, Role, Phase and Category are OntoClean's distinctions as a vocabulary you can assert. gistUFO applies them to all of gist.",
        "Typing a class with a metaclass is punning, and it is OWL 2 DL. The profile checker confirms it.",
        "Two records of the same decision, checked against each other, catch more than either. Here the gUFO type and the OntoClean marks must agree.",
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
