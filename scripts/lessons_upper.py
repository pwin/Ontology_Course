# -*- coding: utf-8 -*-
"""Module 09 -- Standing on gist: reuse, alignment, and two published bridges."""
from ontocat import o, Query
import specs

M = "09-upper-ontologies"

DECL = """
skos:prefLabel      a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
rdfs:isDefinedBy    a owl:AnnotationProperty .
"""

# gist terms the lessons use, declared locally so each file is OWL 2 DL on
# its own. The checker imports the real gistCore before reasoning.
GIST_DECL = """
gist:Organization        a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:Person              a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:Content             a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:Event               a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:GeoRegion           a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:GovernedGeoRegion   a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:OrderedCollection   a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:GeoRoute            a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:Category            a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:Magnitude           a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:Aspect              a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:UnitOfMeasure       a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:Building            a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:isCategorizedBy     a owl:ObjectProperty .
gist:hasMagnitude        a owl:ObjectProperty .
gist:hasAspect           a owl:ObjectProperty .
gist:hasUnitOfMeasure    a owl:ObjectProperty .
gist:numericValue        a owl:DatatypeProperty .
"""

o(
    oid="o58", module=M,
    title="What an upper ontology is for",
    decides="The Trail stands on gist rather than defining person, organisation, event and place again, because an upper ontology is a vocabulary in common, and gist is the smallest one that covers a business.",
    corner="thought",
    why="An upper ontology is a set of classes general enough that every "
        "domain ontology needs them and few define them well, among them "
        "person, organisation, event, place, agreement, content, and a "
        "quantity with a unit. Its value is the one o26 gave for reuse, at "
        "the level where reuse pays best: two ontologies that both put "
        "their people under gist:Person can be joined without a mapping, "
        "and two teams that have both learned gist's hundred classes share "
        "a vocabulary before they ever meet.\n\n"
        "An upper ontology is for that, and the paper this lesson cites, Is "
        "an upper ontology useful?, sets out the whole list: a starter "
        "palette of classes and properties, commonality between domain "
        "ontologies, logical consistency done once at the top, a common "
        "vocabulary, a tool for thought, integrated data, and data that can "
        "be partitioned again afterwards. Its answer to its own title is "
        "yes, and the point about a common vocabulary is the one this "
        "course keeps coming back to, that the ontology is part of the "
        "vocabulary of the organisation, so you should choose one whose "
        "class names can enter everyday speech; continuant fiat boundary, "
        "as the paper observes, might not be for everyone.\n\n"
        "gist is built to be that vocabulary for enterprises, and its "
        "design choices are all in the service of being learnable: about a "
        "hundred classes, everyday names, sparse domains and ranges, no "
        "inverses, disjointness at the top, everything defined in SKOS "
        "annotations, a CC-BY licence, and a release with a version number "
        "and a migration guide. The paper puts the Goldilocks level of "
        "abstraction at a human scale, about as many classes as there were "
        "people in your year at school, and the measured line has version "
        "14's counts, taken from the file itself; BFO, at the other end of "
        "the spectrum, has thirty-six classes and a philosophy, and this "
        "module reads both.\n\n"
        "What standing on an upper ontology costs is that its commitments "
        "come along too. Put bs:Bookshop under gist:Organization and gist's "
        "disjointness axioms now apply to bookshops, so that a bookshop "
        "cannot also be a gist:Building, however much it may be a shop with "
        "a door; which is the right consequence, and o59 finds it.",
    diagram="""
   domain ontologies                        the upper ontology

   the Trail       bs:Person   bs:Bookshop  \\
   a supplier      sup:Staff   sup:Supplier   +---->  gist:Person   gist:Organization   gist:Event ...
   a library       lib:Reader  lib:Branch   /        one vocabulary in common; joins with no mapping

   gist 14, measured from the file:  about a hundred classes, sixty-odd object properties,
   fifty datatype properties, everyday names, no inverses, CC-BY
""",
    learn=[
        "An upper ontology is a vocabulary in common, and its value is that two teams, or two datasets, meet already agreed on what a person, an organisation or an event is.",
        "gist is built to be learned, with a hundred classes under ordinary names, and every design choice in module 05 comes from it.",
        "Standing on an upper ontology imports its commitments, which is the point of it and also the cost.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Stands on gist 14.1.0 (https://w3id.org/semanticarts/ontology/gistCore), CC-BY-4.0, Semantic Arts. The bridge axioms are in o59."@en .

gist:Person        a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
gist:Organization  a owl:Class ; rdfs:isDefinedBy <https://w3id.org/semanticarts/ontology/gistCore> .
""",
    check=dict(profile=True, imports=["gist/gistCore.ttl"], metrics=True, metrics_namespace="https://w3id.org/semanticarts/ns/ontology/gist/"),
    expect=dict(dl=True),
    local="the counts on the MEASURED line are computed from gistCore.ttl, fetched by scripts/setup-tools.ps1",
)
specs.register("o58", "blogUpper", "gistReadme")

o(
    oid="o59", module=M,
    title="Hooking the Trail onto gist",
    decides="Each Trail kind is placed under its most specific gist class with a note saying why, two are left unplaced because nothing fits, and the whole is reasoned over with gist imported to see what gist's own axioms make of it.",
    corner="referent",
    why="Alignment is placing each of your classes under the most specific "
        "class of the upper ontology that is true of every instance, and "
        "then writing down the argument. gistBFO's README states the "
        "standard well: a mapping that puts everything under the top class "
        "is not an interesting mapping, so aim low and be able to say why. "
        "The bridge for the Trail comes to seven subclass axioms, one "
        "typing, and two refusals.\n\n"
        "Most of them are easy enough. bs:Person goes under gist:Person, "
        "whose definition, a human being who was or is alive, is the "
        "Trail's own; bs:Publisher and bs:Bookshop go under "
        "gist:Organization, a structured entity formed to achieve goals; "
        "bs:Event under gist:Event and bs:Series under "
        "gist:OrderedCollection; and the genres, being particulars, are "
        "gist:Category, which gist defines as a concept used to categorise "
        "without formal semantics, which is the very call o24 made. Some of "
        "them take an argument, though. bs:Bookshop is the business rather "
        "than the premises, so it goes under Organization and not Building, "
        "the identity criterion from o10 deciding it, and gist's "
        "disjointness would object if it went under both; bs:Work is a work "
        "and an edition at once, and gist's own example for Content is "
        "Huckleberry Finn independent of any edition, so bs:Work goes under "
        "gist:Content with the compromise noted; and places go under "
        "gist:GovernedGeoRegion, since every one of them is governed by "
        "exactly the council or country it lies within.\n\n"
        "Two are refused outright. bs:StockRecord, being a count of copies "
        "at a price, is not a Magnitude, an Offer or a Collection in gist's "
        "sense, and a forced placement would be worse than none at all; and "
        "bs:TrailSegment comes close to gist:GeoRoute without quite "
        "fitting, a route being an ordered set of points where a segment is "
        "a pair of shops with a length. Both refusals are noted, in the way "
        "the SemOps ledger marks a gap grey rather than painting it green, "
        "and HermiT, with gistCore imported, finds the bridge consistent.",
    diagram="""
   Trail                    gist                          why
   bs:Person                gist:Person                   same definition
   bs:Bookshop              gist:Organization             the business, not the building (identity, o10)
   bs:Publisher             gist:Organization
   bs:Work                  gist:Content                  gist's own example: a literary work, independent of edition
   bs:Event                 gist:Event
   bs:Series                gist:OrderedCollection
   bs:Place                 gist:GovernedGeoRegion        each is governed by the area or country it is within
   bt:genre-*               gist:Category  (individuals)  a concept used to categorise, no formal semantics
   bs:StockRecord           --                            nothing fits; noted, not forced
   bs:TrailSegment          --                            GeoRoute is an ordered set of points; noted

   measured: consistent, with gistCore imported
""",
    learn=[
        "Place each class under the most specific upper class that is true of every instance, and write the argument on the axiom itself.",
        "Identity decides the hard ones, since a bookshop is the business and the building is a different referent altogether.",
        "Refuse a placement rather than force one, because a gap written down is a decision where a wrong placement is a contradiction waiting for data.",
    ],
    body=DECL + GIST_DECL + """
bs:Person        a owl:Class ; rdfs:subClassOf gist:Person .
bs:Bookshop      a owl:Class ; rdfs:subClassOf gist:Organization ;
    skos:editorialNote "Under Organization, not Building: the shop is the business. gist declares the two disjoint, so a shop that is both would be a contradiction."@en .
bs:Publisher     a owl:Class ; rdfs:subClassOf gist:Organization .
bs:Work          a owl:Class ; rdfs:subClassOf gist:Content ;
    skos:editorialNote "gist:Content's example is a literary work independent of edition. bs:Work is also an edition (o10); the compromise stands."@en .
bs:Event         a owl:Class ; rdfs:subClassOf gist:Event .
bs:Series        a owl:Class ; rdfs:subClassOf gist:OrderedCollection .
bs:Place         a owl:Class ; rdfs:subClassOf gist:GovernedGeoRegion ;
    skos:editorialNote "Every Trail place is governed by the council area or country it is within."@en .
bs:StockRecord   a owl:Class ;
    skos:editorialNote "Not placed. Neither gist:Magnitude, gist:Offer nor gist:Collection is true of every stock record."@en .
bs:TrailSegment  a owl:Class ;
    skos:editorialNote "Not placed. gist:GeoRoute is an ordered set of points; a segment is two shops and a length."@en .

skos:Concept  a owl:Class .
bt:genre-crime-fiction  a skos:Concept, gist:Category ; skos:prefLabel "Crime Fiction"@en .

bt:shop-inkwell  a bs:Bookshop ; skos:prefLabel "The Inkwell"@en .
""",
    queries=[Query("The bridge, and what each placement says", """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?trail ?upper ?why WHERE {
  ?trail rdfs:subClassOf ?upper .
  FILTER(STRSTARTS(STR(?trail), "https://example.org/bookshop-trail/schema#") && STRSTARTS(STR(?upper), "https://w3id.org/semanticarts/"))
  OPTIONAL { ?trail skos:editorialNote ?why }
} ORDER BY ?trail""", rows=7)],
    check=dict(profile=True, reason=True, imports=["gist/gistCore.ttl"]),
    expect=dict(dl=True, consistent=True, inferred=["bt:shop-inkwell rdf:type gist:Organization"]),
    tryit="Add 'bs:Bookshop rdfs:subClassOf gist:Building .' and run the checker: gist declares Organization and Building disjoint, so "
          "bs:Bookshop becomes unsatisfiable, and The Inkwell makes the whole graph inconsistent. Identity, enforced by someone else's axiom.",
    local="consistency with gist imported is HermiT through ROBOT; gistCore.ttl is fetched by scripts/setup-tools.ps1",
)
specs.register("o59", "gistReadme", "oboRelations")

o(
    oid="o60", module=M,
    title="gist's patterns, and when to keep your own",
    decides="Floor area is modelled gist's way, as a Magnitude with an Aspect and a Unit, beside the Trail's way, a datatype property with the unit in its name; the Trail keeps the simple form and records what it gives up.",
    corner="referent",
    why="gist has a pattern for measured quantities that is worth "
        "understanding even where you do not adopt it. A gist:Magnitude is "
        "a node with a numeric value, a gist:Aspect saying what was "
        "measured, area in this case, and a gist:UnitOfMeasure saying in "
        "what, square metres, so that every shop's floor area becomes four "
        "triples where it was one. In return the unit is data rather than a "
        "hint buried in a property name, a query can convert between units, "
        "and a floor area and a plot area become the same aspect measured "
        "on different things; gist uses the same pattern for money, "
        "durations and probabilities, and defines several classes by it, "
        "since a GeoRegion is a location with a magnitude whose aspect is "
        "area.\n\n"
        "The Trail says bs:floorArea 140.0 and puts 'square metres' in the "
        "definition, which is the pragmatic form: one triple, a column in "
        "the spreadsheet, and a number a query can compare. It gives up the "
        "unit as data and the possibility of a second unit, and o30's rule "
        "applies, that a departure changing only convenience is allowed so "
        "long as the note says what was traded away. On the day the website "
        "needs square feet, that note is the migration plan.\n\n"
        "gist:isCategorizedBy is the other pattern the Trail could borrow, "
        "since the event kinds of o25 are gist:Category instances and an "
        "event isCategorizedBy one of them. That costs nothing at all and "
        "gains a shared property, and the shipped vocabulary should "
        "probably adopt it.",
    diagram="""
   the Trail's way                        gist's way

   bt:shop-inkwell bs:floorArea 140.0     bt:shop-inkwell gist:hasMagnitude bt:mag-inkwell-area .
   (unit: in the definition)              bt:mag-inkwell-area a gist:Magnitude ;
                                              gist:numericValue 140.0 ;
                                              gist:hasAspect gistd:_Aspect_area ;
                                              gist:hasUnitOfMeasure bt:unit-square-metre .

   one triple, unit as a hint             four triples, unit as data, convertible, shareable
   the note records the trade
""",
    learn=[
        "gist's Magnitude pattern makes the unit into data, at a cost of three triples a value, and it pays whenever units vary or values are shared.",
        "A datatype property with the unit in its definition is the pragmatic form, so record what it gives up.",
        "Borrow the cheap patterns wholesale, since gist:isCategorizedBy for a controlled list costs nothing.",
    ],
    body=DECL + GIST_DECL + """
bs:Bookshop  a owl:Class ; rdfs:subClassOf gist:Organization .

# The Trail's way.
bs:floorArea  a owl:DatatypeProperty ; rdfs:domain bs:Bookshop ; rdfs:range xsd:decimal ;
    skos:definition "Selling floor in square metres."@en ;
    skos:editorialNote "Compromise: the unit is in the definition, not in the data. gist's Magnitude pattern is the alternative; adopt it if a second unit is ever needed."@en .
bt:shop-inkwell  a bs:Bookshop ; bs:floorArea 140.0 .

# gist's way, for the same fact.
gistd:_Aspect_area     a gist:Aspect ;        skos:prefLabel "area"@en .
bt:unit-square-metre   a gist:UnitOfMeasure ; skos:prefLabel "square metre"@en .
bt:mag-inkwell-area    a gist:Magnitude ;
    gist:numericValue      140.0 ;
    gist:hasAspect         gistd:_Aspect_area ;
    gist:hasUnitOfMeasure  bt:unit-square-metre .
bt:shop-inkwell  gist:hasMagnitude bt:mag-inkwell-area .

# The cheap pattern: a controlled list as categories.
bs:Event  a owl:Class ; rdfs:subClassOf gist:Event .
bt:kind-reading  a gist:Category ; skos:prefLabel "Reading"@en .
bt:event-1       a bs:Event ; gist:isCategorizedBy bt:kind-reading .
""",
    check=dict(profile=True, reason=True, imports=["gist/gistCore.ttl"]),
    expect=dict(dl=True, consistent=True),
)
specs.register("o60", "gistReadme", "gistRestrictions")

BFO_DECL = """
obo:BFO_0000001  a owl:Class ; skos:prefLabel "entity"@en .
obo:BFO_0000002  a owl:Class ; skos:prefLabel "continuant"@en .
obo:BFO_0000003  a owl:Class ; skos:prefLabel "occurrent"@en .
obo:BFO_0000015  a owl:Class ; skos:prefLabel "process"@en .
obo:BFO_0000027  a owl:Class ; skos:prefLabel "object aggregate"@en .
obo:BFO_0000030  a owl:Class ; skos:prefLabel "object"@en .
obo:BFO_0000031  a owl:Class ; skos:prefLabel "generically dependent continuant"@en .
obo:BFO_0000040  a owl:Class ; skos:prefLabel "material entity"@en .
"""

o(
    oid="o61", module=M,
    title="gistBFO: the same classes under a foundational ontology",
    decides="The Trail reaches BFO through gist's published bridge, reads each mapping note as a worked example of alignment reasoning, and reasons over the three ontologies together.",
    corner="referent",
    why="BFO is a foundational ontology of quite a different temperament: "
        "thirty-six classes, every IRI a number, and a philosophy, in which "
        "everything is either a continuant, which persists through time, or "
        "an occurrent, which unfolds in it, and a continuant is either "
        "independent, a material object say, or dependent on one, being a "
        "quality or a piece of information. The OBO Foundry builds its "
        "biomedical ontologies on it and a great deal of careful thought "
        "has gone into it. gist chose everyday names and no philosophy at "
        "all, and gistBFO is the published bridge between the two, about "
        "forty subclass axioms from gist classes into their most specific "
        "BFO superclass, each with a note saying why.\n\n"
        "The notes are the useful part, because they show the reasoning "
        "that an alignment needs. gist:Organization goes under object "
        "aggregate, partly in order to agree with the Common Core "
        "Ontologies; gist:Content goes under generically dependent "
        "continuant, since a work is information that any copy can carry; "
        "gist:Category goes under the same, with a note explaining why not "
        "a quality, a category being a bucket that things fall into rather "
        "than a redness that a car has. And then there is gist:Event, which "
        "BFO splits, since a scheduled event is a plan, a generically "
        "dependent continuant, while one that has happened is a process, so "
        "gist:Event goes under the union of the two, which is a mapping "
        "that admits to being two things.\n\n"
        "The Trail inherits the whole bridge, so that bs:Bookshop under "
        "gist:Organization is under object aggregate, bs:Work under "
        "gist:Content is a generically dependent continuant, and bs:Event "
        "is whatever gist:Event is. HermiT, given the Trail's bridge with "
        "gistCore, gistBFO and BFO 2020 core together, reports the four of "
        "them consistent in a few seconds, which is the measured line. "
        "Whether the Trail wants BFO's commitments is a separate question, "
        "and the plain answer is that a bookshop website does not; the "
        "value here lies in seeing an alignment done well.",
    diagram="""
   Trail             gist                  BFO (gistBFO)                                   note
   bs:Bookshop  ->   gist:Organization ->  obo:BFO_0000027  object aggregate               partly to agree with CCO
   bs:Work      ->   gist:Content      ->  obo:BFO_0000031  generically dependent continuant  carried by any copy
   bt:genre-*   ->   gist:Category     ->  obo:BFO_0000031                                 a bucket, not a quality
   bs:Event     ->   gist:Event        ->  GDC or process                                  a plan, or a happening
   bs:Person    ->   gist:Person       ->  (via LivingThing) material entity

   measured: the Trail + gistCore + gistBFO + BFO 2020 core, consistent under HermiT
""",
    learn=[
        "A foundational ontology brings a philosophy with it, so read the bridge's notes to see what each placement commits you to.",
        "The hard mappings are the candid ones, like gist:Event under a union, because in BFO's terms it really is two kinds of thing.",
        "Inheriting a bridge is cheap and reasoning over it is quick, and deciding whether you want its commitments is the real work.",
    ],
    body=DECL + GIST_DECL + BFO_DECL + """
bs:Bookshop  a owl:Class ; rdfs:subClassOf gist:Organization .
bs:Work      a owl:Class ; rdfs:subClassOf gist:Content .
bs:Event     a owl:Class ; rdfs:subClassOf gist:Event .
bs:Person    a owl:Class ; rdfs:subClassOf gist:Person .

# The gistBFO axioms these inherit, restated here with labels so the file
# reads on its own; the checker imports the real gistBFO and BFO.
gist:Organization  rdfs:subClassOf obo:BFO_0000027 .
gist:Content       rdfs:subClassOf obo:BFO_0000031 .
gist:Category      rdfs:subClassOf obo:BFO_0000031 .
gist:Event         rdfs:subClassOf [ a owl:Class ; owl:unionOf ( obo:BFO_0000031 obo:BFO_0000015 ) ] .

bt:shop-inkwell  a bs:Bookshop .
""",
    queries=[Query("What The Inkwell is, all the way up", """
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?type WHERE { bt:shop-inkwell a ?type }""", on="reasoned")],
    check=dict(profile=True, reason=True, rl=True, imports=["gist/gistCore.ttl", "gist/gistBFO.ttl", "bfo/bfo-core.ttl"]),
    expect=dict(dl=True, consistent=True, inferred=["bt:shop-inkwell rdf:type obo:BFO_0000027"]),
    local="the four-ontology consistency check is HermiT through ROBOT; gistBFO and BFO are fetched by scripts/setup-tools.ps1",
)
specs.register("o61", "gistBfo", "bfo")

o(
    oid="o62", module=M,
    title="Two alignments, one ontology: gistUFO beside gistBFO",
    decides="The Trail's classes are typed the gUFO way, as gistUFO types gist's, and set beside their BFO placements; where the two published alignments disagree about gist:Event, the disagreement is kept as instruction.",
    corner="referent",
    why="gistUFO is the second published alignment of gist, this time to "
        "gUFO, and it works rather differently from gistBFO, in that it "
        "does not put gist classes under gUFO classes so much as type them: "
        "gist:Person is a gufo:Kind, gist:Offer a gufo:Phase, "
        "gist:ContractTerm a gufo:Role, and gist:Category a "
        "gufo:AbstractIndividualType. That is module 02's analysis applied "
        "by other people to a real ontology and published for the rest of "
        "us, and o14 used it. A second file then places gist classes under "
        "gUFO's individuals hierarchy, with gist:Person under "
        "gufo:FunctionalComplex, gist:Agreement under gufo:Relator and "
        "gist:Event under gufo:Event.\n\n"
        "Set the two alignments side by side and they agree on most things "
        "and disagree on one, instructively. gistBFO says that a gist:Event "
        "is a generically dependent continuant or a process, because a "
        "scheduled event is a plan; gistUFO says that a gist:Event is a "
        "gufo:Event, a perdurant, something that happens, and types "
        "gist:ScheduledEvent as an intrinsic mode of whatever is doing the "
        "planning. Neither of them is wrong, and they draw the line between "
        "the plan and the happening in different places, so that an "
        "ontology importing both would have to choose. An alignment is "
        "exactly that, a set of decisions each with a note attached, and "
        "two sets of decisions made by careful people will not always "
        "coincide.\n\n"
        "The Trail types its classes the gUFO way here, with gUFO imported, "
        "and the profile checker and HermiT both accept the punning; the "
        "query at the end lists every class with its gUFO type and, through "
        "gist, its BFO superclass, which is about as much foundational "
        "commitment as a bookshop trail could want.",
    diagram="""
   class            gUFO (gistUFO)                     BFO (gistBFO)                          agree?
   gist:Person      Kind; FunctionalComplex            material entity, via LivingThing       yes
   gist:Organization Kind; FunctionalComplex           object aggregate                       yes
   gist:Content     Category; Object                   generically dependent continuant       roughly
   gist:Category    AbstractIndividualType; QualityValue  generically dependent continuant    roughly
   gist:Event       EventType; gufo:Event (a perdurant) GDC or process                        no: the plan vs the happening
   gist:Offer       Phase (of a Commitment)            (a commitment: relational quality)     different questions

   an alignment is a set of decisions with notes; two careful sets will not always coincide
""",
    learn=[
        "gistUFO types classes by what kind of class they are and gistBFO places them under what kind of thing they are, and both of those are alignment.",
        "Two published alignments of one ontology disagree about events, so keep the disagreement, because it shows where the line between plan and happening has been drawn.",
        "The Trail can carry both typings and the checker accepts it, though whether to adopt either is a scope decision.",
    ],
    body=DECL + """
# gUFO's types, declared so the file stands alone; the checker imports gUFO.
gufo:Kind     a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .
gufo:SubKind  a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .
gufo:Role     a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .
gufo:EventType a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .
gufo:AbstractIndividualType a owl:Class ; rdfs:isDefinedBy <http://purl.org/nemo/gufo> .
gist:Organization  a owl:Class .  gist:Person a owl:Class .  gist:Event a owl:Class .  gist:Category a owl:Class .

bs:Person       a owl:Class, gufo:Kind ;      rdfs:subClassOf gist:Person .
bs:Bookshop     a owl:Class, gufo:Kind ;      rdfs:subClassOf gist:Organization .
bs:Settlement   a owl:Class, gufo:SubKind ;   rdfs:subClassOf bs:Place .
bs:Place        a owl:Class, gufo:Kind .
bs:Author       a owl:Class, gufo:Role ;      rdfs:subClassOf bs:Person .
bs:Event        a owl:Class, gufo:EventType ; rdfs:subClassOf gist:Event .
bt:genre-crime-fiction  a gist:Category ;
    skos:editorialNote "gistUFO types gist:Category as a gufo:AbstractIndividualType, and gistBFO places it under a generically dependent continuant."@en .
""",
    queries=[Query("Every class, its gUFO type, and its gist parent", """
PREFIX gufo: <http://purl.org/nemo/gufo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class ?gufoType ?gistParent WHERE {
  ?class a ?gufoType . FILTER(STRSTARTS(STR(?gufoType), STR(gufo:)))
  OPTIONAL { ?class rdfs:subClassOf ?gistParent . FILTER(STRSTARTS(STR(?gistParent), "https://w3id.org/semanticarts/")) }
} ORDER BY ?class""", rows=6)],
    check=dict(profile=True, reason=True, imports=["gufo/gufo.ttl", "gist/gistCore.ttl"]),
    expect=dict(dl=True, consistent=True),
    local="consistency with gUFO and gist imported is HermiT through ROBOT",
)
specs.register("o62", "gistUfo", "gufo")
