# -*- coding: utf-8 -*-
"""Module 12 -- Putting it together: the vocabulary, the scheme, the questions, a challenge."""
from ontocat import o, Query, DVOCAB, DGENRES, D11
import specs

M = "12-putting-it-together"

DECL = """
skos:prefLabel      a owl:AnnotationProperty .
skos:definition     a owl:AnnotationProperty .
skos:editorialNote  a owl:AnnotationProperty .
"""

o(
    oid="o73", module=M,
    title="The whole vocabulary, decision by decision",
    decides="The shipped vocabulary is read as the sum of the course's decisions, each traced to the lesson that made it, and put through every instrument the course has: profile, reasoner, metrics, checks, audits.",
    corner="all three",
    why="data/01-vocabulary.ttl is the Bookshop Trail's schema as the "
        "SPARQL and SHACL courses use it, and every choice in it has a "
        "lesson behind it now. Its classes are the backbone of o12 with "
        "one role hanging off it. Its properties are named as o18 said, "
        "with the four departures recorded. Its comments carry "
        "definitions in the form o21 asked for and usage notes beside "
        "them, in one property, which o23 called a compromise. bs:within "
        "is transitive and not functional, o48. bs:founded is not "
        "functional, o29. The domain of bs:locatedIn is a union, o38. The "
        "year properties have no range, o50. The genres are a concept "
        "scheme, o24 and o36. The borrowed terms are declared, o26 and "
        "o42. bs:disputes is an annotation property because it points at "
        "an RDF 1.2 triple term, which is where OWL 2 stops.\n\n"
        "The measured line puts it through everything at once: OWL 2 DL and not in EL, QL or RL, since EL and QL refuse a functional object property and RL the union domain of bs:locatedIn; consistent, with nothing unsatisfiable; "
        "seventeen classes of its own and twenty-five with the borrowed "
        "ones; every local name conforming; no circular definition; the "
        "OQuaRE scores of module 10; and the Quality Suite's findings "
        "scoped to bs:, which are the SKOS policy question and the "
        "open domains left open on purpose.\n\n"
        "What it does not have is the two things the course added and "
        "the shipped file did not adopt: OntoClean annotations on the "
        "classes, and SKOS annotations in place of rdfs:label and "
        "rdfs:comment. Both are one pass of work and both are recorded "
        "here as decisions to take, which is the right state for a "
        "vocabulary to be in between releases.",
    diagram="""
   in the shipped file                          decided in
   ten top-level kinds, one role                o12, o08
   Author under Person, never the reverse       o08, o09
   Work = work + edition, noted                 o10, o30
   author, locatedIn, publishedBy, genre        o18 (departures recorded)
   rdfs:label + rdfs:comment                    o23 (a compromise; SKOS annotations to adopt)
   bs:within transitive, not functional         o48
   bs:founded not functional                    o29
   locatedIn domain: a union                    o38, o31
   gYear properties: no range                   o50
   genres: skos:Concept, not classes            o24, o36
   borrowed terms declared                      o26, o42
   bs:disputes an annotation property           o42

   measured: DL; not EL/QL/RL; consistent; 17 own classes; names clean; definitions clean
""",
    learn=[
        "A vocabulary is the sum of its decisions. Trace each to its reason, and the file becomes readable as an argument.",
        "Put it through every instrument at once before a release. The measured line is what that looks like.",
        "The decisions not yet taken are recorded too. That is the state a vocabulary should be in between releases.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Decisions to take at the next release: OntoClean annotations on every class (o13); SKOS annotations in place of rdfs:label and rdfs:comment (o23); gist:isCategorizedBy for the event kinds (o60)."@en .
""",
    data=DVOCAB,
    queries=[Query("The vocabulary's own account of its properties without a range", """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?property ?comment WHERE {
  ?property a owl:DatatypeProperty ; rdfs:comment ?comment .
  FILTER NOT EXISTS { ?property rdfs:range ?r }
  FILTER(STRSTARTS(STR(?property), "https://example.org/bookshop-trail/schema#"))
} ORDER BY ?property""", on="data")],
    check=dict(profiles=True, profile_on="full", with_data=DVOCAB, reason=True, metrics=True, names=True, definitions=True, oqs="checks"),
    expect=dict(dl=True, el=False, ql=False, rl=False, consistent=True, unsat=[], names_bad=0),
    local="the profile verdicts and HermiT are ROBOT; the findings are the Quality Suite; the metrics and audits are the course's scripts",
)
specs.register("o73", "sparqlCourse", "shaclCourse")

o(
    oid="o74", module=M,
    title="The genre scheme, complete",
    decides="The shipped genre scheme, thirty-one concepts two to four levels deep, passes the SKOS integrity shapes of o39 and the cycle and depth queries, and is kept a concept scheme rather than promoted.",
    corner="all three",
    why="data/02-genres.ttl is the shelf plan: one concept scheme, one top "
        "concept, thirty-one concepts, preferred labels in English with "
        "Welsh and Gaelic where they exist, alternative labels for the "
        "American spellings and the trade names, scope notes, and a tree "
        "that is two levels deep under Poetry and four under Science "
        "Fiction, because that is how the shops shelve them. o36 said "
        "why the depth is uneven and why that is right; o24 said why the "
        "genres are particulars; o39 gave the integrity conditions.\n\n"
        "The measured line runs the o39 shapes on the whole scheme: one "
        "preferred label per language, every concept in the scheme, "
        "related disjoint from broader, no concept its own ancestor. It "
        "conforms. The queries count the concepts, find the deepest, and "
        "confirm that skos:broader+ from the top concept reaches all "
        "thirty. That last one is the test that matters for question 4 in the brief, which the SPARQL course's q33 answers with skos:broader+, and which a fixed chain of two hops gets wrong, as q28 shows on the place hierarchy.\n\n"
        "The scheme stays a scheme. No question in the brief needs an "
        "axiom about the members of a genre, so o40's promotion is not "
        "taken, and the shelf plan can be rearranged by the shops without "
        "a reasoner retyping a single work.",
    diagram="""
   bt:genre-scheme  a skos:ConceptScheme ; skos:hasTopConcept bt:genre-literature
     Literature
       Fiction: Crime (Cosy, Tartan Noir, Police Procedural), Speculative (SF: Hard, Space Opera, Climate; Fantasy: Folk, Portal), ...
       Non-fiction: Nature Writing, History (Maritime, Industrial), Travel, Biography, ...
       Poetry

   31 concepts, depth 2 to 4, one preferred label per language, alt labels, scope notes
   integrity shapes: conforms.  broader+ from the top: reaches every concept.
""",
    learn=[
        "A concept scheme is finished when its integrity conditions pass and its questions are answered by paths. Neither needs a reasoner.",
        "Uneven depth is a fact about the domain. The queries that walk it must not assume otherwise.",
        "Not promoting is a decision. Record it, and revisit it the day an axiom about members is needed.",
    ],
    body=DECL + """
skos:ConceptScheme  a owl:Class .
skos:hasTopConcept  a owl:ObjectProperty .

bt:genre-scheme
    a                   skos:ConceptScheme ;
    skos:prefLabel      "Bookshop Trail genre scheme"@en ;
    skos:hasTopConcept  bt:genre-literature ;
    skos:editorialNote  "Kept as a concept scheme: no competency question needs an axiom about the members of a genre. Promote (o40) only if one does."@en .
""",
    data=DGENRES,
    companions={"skos-shapes.ttl": __import__("lessons_ladder").SKOS_SHAPES},
    shapes="skos-shapes.ttl",
    queries=[
        Query("How many concepts, and how many the top concept reaches", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT (COUNT(DISTINCT ?c) AS ?concepts) (COUNT(DISTINCT ?reached) AS ?reachedFromTop) WHERE {
  ?c a skos:Concept .
  OPTIONAL { ?reached skos:broader+ bt:genre-literature . FILTER(?reached = ?c) }
}""", on="data", rows=1),
        Query("The deepest concepts", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?leaf (COUNT(?up) AS ?depth) WHERE { ?leaf a skos:Concept ; skos:broader+ ?up }
GROUP BY ?leaf ORDER BY DESC(?depth) LIMIT 5""", on="data", rows=5),
        Query("Concepts that are their own ancestor (none)", """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?c WHERE { ?c skos:broader+ ?c }""", on="data", rows=0),
    ],
    check=dict(with_data=DGENRES, shacl=__import__("lessons_ladder").SKOS_SHAPES),
    expect=dict(shacl_conforms=True),
    notes="Open in the editor opens this lesson with the shapes; to validate the whole scheme, load data/02-genres.ttl in the first tab, "
          "keep the shapes tab, and press Validate. The AFTERWARDS queries run on the scheme.",
)
specs.register("o74", "skosSchemes", "sparqlCourse")

o(
    oid="o75", module=M,
    title="The questions answered, and the rules kept elsewhere",
    decides="The brief's ten questions are run against the whole dataset as the acceptance test of the vocabulary, and the constraints the ontology declined to express are found in the SHACL course, where they belong.",
    corner="all three",
    why="An ontology exists to answer questions, o07 said, and the SPARQL "
        "course is the Trail's questions written down: 145 of them, run on "
        "three engines and compared value by value. This lesson runs the "
        "brief's ten as the acceptance test, on the shipped vocabulary and "
        "data, in the editor's SPARQL panel or in the checker. Each is a "
        "row count on the measured line: four towns with no bookshop, "
        "four shops in Wales, the shops reachable on foot from The "
        "Inkwell, the imprints that belong ultimately to the Lodestone "
        "Group, the works with no ISBN, the two founding claims for Ex "
        "Libris. Where the SPARQL course has the question, its number is "
        "given.\n\n"
        "The other half of the package is the SHACL course, and it holds "
        "the rules this course refused to put in the ontology. Exactly "
        "one town per shop is s04; one founding year is s04 as well, as a "
        "finding rather than a contradiction, o29; a valid ISBN check "
        "digit is s39; a segment's ends are two different shops, s36; "
        "nothing is within itself, s30. Each is a rule about the "
        "dataset, with a severity somebody chose, and each is exactly the "
        "kind of thing gist's tenth rule sends to SHACL.\n\n"
        "Three courses, one data set, one vocabulary. The ontology says "
        "what the terms mean; the queries ask; the shapes check. A "
        "question that cannot be asked, or a rule that cannot be "
        "checked, is a gap in the vocabulary, and this is how it would be "
        "found.",
    diagram="""
   question (the brief)                                 answered by          SPARQL course   rule kept in SHACL course
   1  shops in Wales / an area                          bs:within+           q28             --
   2  towns with no bookshop                            NOT EXISTS           q16             s21 (as a warning)
   3  walkable from The Inkwell, and how far            (connectsTo|^)+      q31, q32        s36
   4  crime fiction shops, including its kinds          skos:broader*        q33, q28        --
   5  events in York, and the cost                      heldAt/locatedIn     q20s            --
   6  works with no ISBN                                NOT EXISTS           q15             s39 (check digit)
   7  influenced at any remove by Rhona Blackwood       influencedBy+        q34             s30 (no cycles)
   8  imprints ultimately of the Lodestone Group        imprintOf+           q44             --
   9  when Ex Libris opened, and who says so            RDF 1.2 layer        q61 to q63      s53 to s55
   10 who stocks a book, cheapest                       StockRecord          q21             s47
""",
    learn=[
        "The competency questions are the acceptance test. Run them on the whole dataset before every release.",
        "The rules the ontology refused are not lost. They are shapes, in the SHACL course, with severities somebody chose.",
        "Three courses, one package: meaning, questions, checks. A gap in one shows up in another.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema"@en ;
    skos:editorialNote  "Acceptance test: the brief's ten questions as queries, run on bookshop-trail-1.1.ttl. The SPARQL course holds the full suite; the SHACL course holds the rules."@en .
""",
    data=D11,
    queries=[
        Query("Q3: shops reachable on foot from The Inkwell", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT (COUNT(DISTINCT ?shop) AS ?reachable) WHERE { bt:shop-inkwell (bs:connectsTo|^bs:connectsTo)+ ?shop . FILTER(?shop != bt:shop-inkwell) }""", on="data", rows=1),
        Query("Q4: shops specialising in crime fiction, including its kinds", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX bt: <https://example.org/bookshop-trail/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?shop ?genre WHERE { ?shop bs:specialises ?g . ?g skos:broader* bt:genre-crime-fiction ; skos:prefLabel ?genre . FILTER(LANG(?genre) = "en") } ORDER BY ?shop""", on="data", rows=4),
        Query("Q6: works with no ISBN", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
SELECT (COUNT(?w) AS ?withoutIsbn) WHERE { ?w a bs:Work . FILTER NOT EXISTS { ?w bs:isbn ?i } }""", on="data", rows=1),
        Query("Q8: imprints that belong, ultimately, to the Lodestone Group", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?imprint WHERE { ?imprint bs:imprintOf+ bt:pub-lodestone-group } ORDER BY ?imprint""", on="data"),
        Query("Q10: who stocks The Book Town, cheapest first", """
PREFIX bs: <https://example.org/bookshop-trail/schema#>
PREFIX bt: <https://example.org/bookshop-trail/>
SELECT ?shop ?price WHERE { ?rec bs:ofWork bt:book-the-book-town ; bs:atShop ?shop ; bs:shelfPrice ?price } ORDER BY ?price""", on="data"),
    ],
    check=dict(with_data=D11),
    expect=dict(),
)
specs.register("o75", "sparqlCourse", "shaclCourse")

ANSWER = """
@prefix bt:   <https://example.org/bookshop-trail/> .
@prefix bs:   <https://example.org/bookshop-trail/schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dct:  <http://purl.org/dc/terms/> .

# One answer to the challenge: Work split from Edition, with the data kept
# true. Compare it with your own before reading it through.

skos:prefLabel a owl:AnnotationProperty . skos:definition a owl:AnnotationProperty .
skos:editorialNote a owl:AnnotationProperty . skos:changeNote a owl:AnnotationProperty .
dct:isReplacedBy a owl:AnnotationProperty . owl:deprecated a owl:AnnotationProperty .

bs:Work  a owl:Class ; skos:prefLabel "Work"@en ;
    skos:definition "What an author wrote, independent of any printing."@en ;
    skos:changeNote "3.0.0: the edition properties moved to bs:Edition. Assertions of bs:isbn on a Work made under 2.x remain true of the work's first edition, minted below."@en .
bs:Edition  a owl:Class ; skos:prefLabel "Edition"@en ;
    skos:definition "A printing of a Work by a publisher, with an ISBN if made after 1970."@en ;
    rdfs:subClassOf [ a owl:Restriction ; owl:onProperty bs:editionOf ; owl:someValuesFrom bs:Work ] .
bs:Translation  a owl:Class ; rdfs:subClassOf bs:Work ; skos:prefLabel "Translation"@en .
bs:Publisher  a owl:Class .
bs:Author     a owl:Class .

[] a owl:AllDisjointClasses ; owl:members ( bs:Work bs:Edition bs:Publisher bs:Author ) .

bs:editionOf    a owl:ObjectProperty, owl:FunctionalProperty ; rdfs:domain bs:Edition ; rdfs:range bs:Work ; skos:prefLabel "edition of"@en .
bs:author       a owl:ObjectProperty ; rdfs:domain bs:Work ;    rdfs:range bs:Author .
bs:publishedBy  a owl:ObjectProperty ; rdfs:domain bs:Edition ; rdfs:range bs:Publisher ;
    skos:changeNote "3.0.0: domain moved from Work to Edition."@en .
bs:isbn         a owl:DatatypeProperty, owl:FunctionalProperty ; rdfs:domain bs:Edition ; rdfs:range xsd:string .
bs:pages        a owl:DatatypeProperty ; rdfs:domain bs:Edition ; rdfs:range xsd:integer .
bs:Edition      owl:hasKey ( bs:isbn ) .

# The migration for one work: the 2.x assertions stay on the work where they
# are the work's, and move to a minted first edition where they are the edition's.
bt:book-the-book-town  a bs:Work ; skos:prefLabel "The Book Town"@en ; bs:author bt:author-rab-fingal .
bt:edition-the-book-town-1  a bs:Edition ; bs:editionOf bt:book-the-book-town ;
    bs:publishedBy bt:pub-bell-rock ; bs:isbn "9787063088596" ; bs:pages 544 .
bt:author-rab-fingal  a bs:Author .
bt:pub-bell-rock      a bs:Publisher .
"""

o(
    oid="o76", module=M,
    title="Challenge: the day a second edition appears",
    decides="Split bs:Work into Work and Edition so that the compromise of o10 is retired, every assertion made under the old meaning stays true, the competency questions still answer, and the reasoner agrees; an answer is beside the lesson, to be read after yours.",
    corner="all three",
    why="The brief that arrives after the site launches: Bell Rock has "
        "issued a second edition of The Book Town, with a new ISBN and a "
        "different page count, and the committee wants both stocked and "
        "told apart. Under the shipped vocabulary a work has one ISBN, "
        "functionally, so there is no way to say it. o10 recorded the "
        "compromise and o27 said what the fix must respect: the meaning of "
        "bs:Work must not move under the data already written.\n\n"
        "The task, then. Introduce bs:Edition with an identity criterion "
        "of its own, the ISBN, as a key. Decide which of bs:Work's "
        "properties are the work's (author, title, genre, original "
        "language) and which are the edition's (publisher, ISBN, pages, "
        "price, publication year), and move only the second group, with "
        "a change note on each. Decide how existing bs:Work assertions "
        "carrying an ISBN are migrated: a first edition minted per work is "
        "one answer. Keep Work and Edition disjoint, since their criteria "
        "of identity differ. Decide the version number by the diff (o71). "
        "Then check: OWL 2 DL; consistent with the data; the stock "
        "records now point at editions, and question 10 in the brief "
        "still answers; and a query for 'the editions of The Book Town' "
        "returns two.\n\n"
        "answer.ttl beside this lesson is one way to do it, measured: DL, "
        "consistent, with the migration of one work shown. It is not the "
        "only way. A version that keeps bs:Work for editions and mints a "
        "new bs:AbstractWork above it is defensible, and the argument "
        "about which is better is the argument this course was about.",
    diagram="""
   before                                   after
   bs:Work  isbn, pages, publishedBy,       bs:Work      author, title, genre, originalLanguage
            author, title, genre            bs:Edition   editionOf (functional), isbn (key), pages, publishedBy, rrp, publicationYear
                                            Work and Edition disjoint: different criteria of identity

   acceptance
   - OWL 2 DL; consistent with the data
   - every 2.x assertion still true of something (the work, or its first edition)
   - question 10 still answers; 'editions of The Book Town' returns two
   - version-diff says MAJOR, and the change notes say why
""",
    learn=[
        "The day the identity criterion changes is the day a class splits. The split is a new term, not a new meaning for the old one.",
        "Sort the properties by which referent they belong to. The design work is that sorting; the axioms follow.",
        "Acceptance is measured: profile, reasoner, competency questions, diff. Read the answer only after yours passes them.",
    ],
    body=DECL + """
<https://example.org/bookshop-trail/schema>
    a                   owl:Ontology ;
    skos:prefLabel      "The Bookshop Trail schema, 3.0.0 (the challenge)"@en ;
    skos:editorialNote  "Your answer goes here. answer.ttl beside this lesson is one answer, measured."@en .
""",
    companions={"answer.ttl": ANSWER},
    check=dict(profile=True, answer="answer.ttl"),
    expect=dict(dl=True, answer_dl=True, answer_consistent=True),
    notes="The checker measures answer.ttl as well: python scripts/check_lessons.py o76 --show prints what HermiT and the profile checker "
          "made of it. To measure your own, put it in place of answer.ttl and run the same command.",
)
specs.register("o76", "oboStability", "semopsSemver")
