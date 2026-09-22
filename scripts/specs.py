# -*- coding: utf-8 -*-
"""Where each lesson is defined, or argued.

One table of sections keyed by a short name, and a map from lessons and
modules to the sections that define them. The module READMEs, the course
document and the .ttl headers all draw on this, and check_links.py fetches
every document and confirms each anchor still lands on a heading.

This course cites more than W3C Recommendations: a style guide, a set of
principles, two papers and a manual. They are held to the same rule -- a
link, and a check that the link still works.
"""
from __future__ import annotations

RDFS = "https://www.w3.org/TR/rdf12-schema/"
RDFC = "https://www.w3.org/TR/rdf12-concepts/"
RDFSEM = "https://www.w3.org/TR/rdf12-semantics/"
TURTLE = "https://www.w3.org/TR/rdf12-turtle/"
PRIMER = "https://www.w3.org/TR/owl2-primer/"
SYNTAX = "https://www.w3.org/TR/owl2-syntax/"
PROFILES = "https://www.w3.org/TR/owl2-profiles/"
DIRECT = "https://www.w3.org/TR/owl2-direct-semantics/"
SKOSREF = "https://www.w3.org/TR/skos-reference/"
SKOSPRIMER = "https://www.w3.org/TR/skos-primer/"
COOL = "https://www.w3.org/TR/cooluris/"
WEBARCH = "https://www.w3.org/TR/webarch/"
VOCABPUB = "https://www.w3.org/TR/swbp-vocab-pub/"
LINKED = "https://www.w3.org/DesignIssues/LinkedData.html"
RFC3987 = "https://www.rfc-editor.org/rfc/rfc3987"
BCP47 = "https://www.rfc-editor.org/info/bcp47"
SHACL = "https://www.w3.org/TR/shacl/"
DCT = "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/"
TRIANGLE = "https://en.wikipedia.org/wiki/Triangle_of_reference"
PEIRCE = "https://plato.stanford.edu/entries/peirce-semiotics/"
THINGS = "https://blog.google/products/search/introducing-knowledge-graph-things-not/"
ONTOCLEAN_WP = "https://en.wikipedia.org/wiki/OntoClean"
ONTOCLEAN_CACM = "https://doi.org/10.1145/503124.503150"
ONTOCLEAN_HB = "https://doi.org/10.1007/978-3-540-92673-3_9"
OQUARE = "http://www.cs.man.ac.uk/~stevensr/papers/OQuareProof.pdf"
GIST = "https://github.com/semanticarts/gist"
GISTSTYLE = "https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md"
GISTDEP = "https://github.com/semanticarts/gist/blob/develop/docs/DeprecationAndDeletionPolicy.md"
GISTNS = "https://github.com/semanticarts/gist/blob/develop/docs/Namespace.md"
GISTBFO = "https://github.com/semanticarts/gistBFO"
GISTUFO = "https://github.com/semanticarts/gistUFO"
GUFO = "https://nemo-ufes.github.io/gufo/"
BFO = "https://github.com/BFO-ontology/BFO-2020"
OBO = "https://obofoundry.org/principles/"
OBO_INDEX = OBO + "fp-000-summary.html"
NISO = "https://groups.niso.org/higherlogic/ws/public/download/12591/z39-19-2005r2010.pdf"
SEMOPS = "https://github.com/pwin/SemOpsManual/blob/main/docs/"
OQS = "https://github.com/pwin/consolidated-ontology-quality-suite-python"
BLOG_TEAM = "https://www.semanticarts.com/team-building-the-importance-of-an-ontology/"
UPPER = "https://ceur-ws.org/Vol-3661/10-SHORT-PWinstanley-ISKOUK2023.pdf"
SPARQL_COURSE = "https://www.semantechs.co.uk/SPARQL_Course/"
SHACL_COURSE = "https://www.semantechs.co.uk/SHACL_Course/"

# key -> (label, url)
SECTIONS = {
    # Meaning
    "triangle":       ("Ogden and Richards, the triangle of reference (1923)", TRIANGLE),
    "peirce":         ("Peirce's theory of signs, Stanford Encyclopedia of Philosophy", PEIRCE),
    "thingsNotStrings": ("Google, 'things, not strings' (2012)", THINGS),
    "rdfIris":        ("RDF 1.2 Concepts 1.2 Resources and Statements", RDFC + "#resources-and-statements"),
    "rdfReferents":   ("RDF 1.2 Concepts 1.3 The Referent of an IRI", RDFC + "#referents"),
    "rdfIriSection":  ("RDF 1.2 Concepts 3.2 IRIs", RDFC + "#section-IRIs"),
    "rdfGraph":       ("RDF 1.2 Concepts 3 RDF Graphs", RDFC + "#section-rdf-graph"),
    "rdfLiterals":    ("RDF 1.2 Concepts 3.3 Literals", RDFC + "#section-Graph-Literal"),
    "rdfVocab":       ("RDF 1.2 Concepts 1.4 RDF Vocabularies and Namespace IRIs", RDFC + "#vocabularies"),
    "webarchId":      ("Architecture of the World Wide Web 2 Identification", WEBARCH + "#identification"),
    "webarchOwner":   ("Architecture of the World Wide Web 2.2.2.1 URI Ownership", WEBARCH + "#uri-ownership"),
    "webarchOpacity": ("Architecture of the World Wide Web 2.5 URI Opacity", WEBARCH + "#uri-opacity"),
    "linkedData":     ("Berners-Lee, Linked Data (2006): the four rules", LINKED),
    "rfc3987":        ("RFC 3987 Internationalized Resource Identifiers", RFC3987),
    "coolHash":       ("Cool URIs for the Semantic Web 4.1 Hash URIs", COOL + "#hashuri"),
    "cool303":        ("Cool URIs for the Semantic Web 4.2 303 URIs", COOL + "#r303gendocument"),
    "coolChoosing":   ("Cool URIs for the Semantic Web 4.4 Choosing between 303 and Hash", COOL + "#choosing"),
    "coolCool":       ("Cool URIs for the Semantic Web 3 URIs for Real-World Objects", COOL + "#semweb"),
    "semopsTerritory": ("SemOps Manual 2.1 Definitions are territory", SEMOPS + "02-people-and-cognition.md#21-definitions-are-territory"),
    "semopsPriesthood": ("SemOps Manual 2.2 The priesthood problem", SEMOPS + "02-people-and-cognition.md#22-the-priesthood-problem"),
    "semopsStyles":   ("SemOps Manual 2.3 Cognitive styles", SEMOPS + "02-people-and-cognition.md#23-cognitive-styles-people-do-not-categorise-the-same-way"),
    "semopsBudget":   ("SemOps Manual 2.4 Cognitive capacity is a hard budget", SEMOPS + "02-people-and-cognition.md#24-cognitive-capacity-is-a-hard-budget"),
    "semopsWorkshop": ("SemOps Manual 2.5 The workshop is a social event with a technical output", SEMOPS + "02-people-and-cognition.md#25-the-workshop-is-a-social-event-with-a-technical-output"),
    "blogTeam":       ("Winstanley, Team building: the importance of an ontology (2025)", BLOG_TEAM),
    "blogUpper":      ("Winstanley, Is an upper ontology useful? ISKO UK 2023, CEUR-WS Vol. 3661", UPPER),
    # Systematics
    "ontocleanWp":    ("OntoClean: the four meta-properties", ONTOCLEAN_WP),
    "ontocleanCacm":  ("Guarino and Welty, Evaluating ontological decisions with OntoClean, CACM 45(2), 2002", ONTOCLEAN_CACM),
    "ontocleanHb":    ("Guarino and Welty, An overview of OntoClean, Handbook on Ontologies, 2009", ONTOCLEAN_HB),
    "gufo":           ("gUFO: a lightweight implementation of the Unified Foundational Ontology", GUFO),
    "gistUfo":        ("gistUFO: gist aligned with gUFO", GISTUFO),
    "gistInstanceNames": ("gist Style Guide: instance local names, and the most specific rigid class", GISTSTYLE + "#instance-local-names"),
    # Naming
    "gistLocalNames": ("gist Style Guide: orthographic conventions for local names", GISTSTYLE + "#orthographic-conventions-for-class-and-property-local-names"),
    "gistPropertyNames": ("gist Style Guide: textual standards for property local names", GISTSTYLE + "#textual-standards-for-property-local-names"),
    "gistLabels":     ("gist Style Guide: labels", GISTSTYLE + "#labels"),
    "gistTitleCase":  ("gist Style Guide: definition of title case", GISTSTYLE + "#gist-definition-of-title-case"),
    "gistNamespaces": ("gist Style Guide: namespaces", GISTSTYLE + "#namespaces"),
    "gistNsDoc":      ("gist: the namespace document", GISTNS),
    "oboUris":        ("OBO Foundry principle FP-003, URI/identifier space", OBO + "fp-003-uris.html"),
    "oboNaming":      ("OBO Foundry principle FP-012, naming conventions", OBO + "fp-012-naming-conventions.html"),
    "rdfsLabel":      ("RDF Schema 3.5 rdfs:label", RDFS + "#ch_label"),
    "bcp47":          ("BCP 47 Tags for Identifying Languages", BCP47),
    "skosLabels":     ("SKOS Reference 5 Lexical Labels", SKOSREF + "#labels"),
    "skosS14":        ("SKOS Reference 5.3 integrity condition S14, one preferred label per language", SKOSREF + "#L1541"),
    "vocabPub":       ("Best Practice Recipes for Publishing RDF Vocabularies", VOCABPUB),
    # Definitions and controlled vocabularies
    "gistAnnotations": ("gist Style Guide: conventions for annotation use", GISTSTYLE + "#conventions-for-annotation-use"),
    "gistAnnotationFormat": ("gist Style Guide: formatting conventions for annotations", GISTSTYLE + "#formatting-conventions-for-annotations"),
    "gistAnnotationCard": ("gist Style Guide: annotation cardinality", GISTSTYLE + "#annotation-cardinality"),
    "oboDefinitions": ("OBO Foundry principle FP-006, textual definitions", OBO + "fp-006-textual-definitions.html"),
    "oboStability":   ("OBO Foundry principle FP-019, stability of term meaning", OBO + "fp-019-term-stability.html"),
    "oboScope":       ("OBO Foundry principle FP-005, scope", OBO + "fp-005-delineated-content.html"),
    "oboDocumented":  ("OBO Foundry principle FP-008, documentation", OBO + "fp-008-documented.html"),
    "niso":           ("ANSI/NISO Z39.19, Guidelines for the construction of monolingual controlled vocabularies", NISO),
    "skosNotes":      ("SKOS Reference 7 Documentation Properties", SKOSREF + "#notes"),
    "skosConcepts":   ("SKOS Reference 3 The skos:Concept Class", SKOSREF + "#concepts"),
    "rdfsComment":    ("RDF Schema 3.6 rdfs:comment", RDFS + "#ch_comment"),
    "dctTerms":       ("DCMI Metadata Terms", DCT),
    # Design principles
    "gistInverses":   ("gist Style Guide: inverses, and why gist has none", GISTSTYLE + "#inverses"),
    "gistRestrictions": ("gist Style Guide: OWL restrictions, the eleven rules", GISTSTYLE + "#owl-restrictions"),
    "gistReadme":     ("gist: a minimalist upper ontology", GIST),
    "oboOpen":        ("OBO Foundry principle FP-001, open", OBO + "fp-001-open.html"),
    "oboRelations":   ("OBO Foundry principle FP-007, relations: reuse existing ones", OBO + "fp-007-relations.html"),
    "oboCollab":      ("OBO Foundry principle FP-010, commitment to collaboration", OBO + "fp-010-collaboration.html"),
    "oboUsers":       ("OBO Foundry principle FP-009, documented plurality of users", OBO + "fp-009-users.html"),
    "semopsInnerLoop": ("SemOps Manual 8.1 The inner loop belongs in the editor", SEMOPS + "08-model-and-validate.md#81-the-inner-loop-belongs-in-the-editor"),
    "semopsHouseRules": ("SemOps Manual 8.4 Your own rules, without forking anything", SEMOPS + "08-model-and-validate.md#84-your-own-rules-without-forking-anything"),
    "semopsMaturity": ("SemOps Manual 6.3 The five maturity levels", SEMOPS + "06-stages-and-stories.md#63-the-five-maturity-levels"),
    # The ladder
    "rdfsClass":      ("RDF Schema 2.2 rdfs:Class", RDFS + "#ch_class"),
    "rdfsType":       ("RDF Schema 3.3 rdf:type", RDFS + "#ch_type"),
    "rdfsSubClassOf": ("RDF Schema 3.4 rdfs:subClassOf", RDFS + "#ch_subclassof"),
    "rdfsProperty":   ("RDF Schema 2.5 rdf:Property", RDFS + "#ch_property"),
    "rdfsRange":      ("RDF Schema 3.1 rdfs:range", RDFS + "#ch_range"),
    "rdfsDomain":     ("RDF Schema 3.2 rdfs:domain", RDFS + "#ch_domain"),
    "rdfsSubPropertyOf": ("RDF Schema 3.5 rdfs:subPropertyOf", RDFS + "#ch_subpropertyof"),
    "rdfsEntailment": ("RDF 1.2 Semantics 9 RDFS Interpretations", RDFSEM + "#rdfs_interpretations"),
    "rdfsRules":      ("RDF 1.2 Semantics 9.2 RDFS Entailment", RDFSEM + "#rdfs_entailment"),
    "skosSchemes":    ("SKOS Reference 4 Concept Schemes", SKOSREF + "#schemes"),
    "skosSemantic":   ("SKOS Reference 8 Semantic Relations", SKOSREF + "#semantic-relations"),
    "skosCollections": ("SKOS Reference 9 Concept Collections", SKOSREF + "#collections"),
    "skosMapping":    ("SKOS Reference 10 Mapping Properties", SKOSREF + "#mapping"),
    "skosPrimerRel":  ("SKOS Primer 2.3 Semantic Relationships", SKOSPRIMER + "#secrel"),
    "skosPrimerScheme": ("SKOS Primer 2.4 Concept Schemes", SKOSPRIMER + "#secscheme"),
    "skosPrimerOwl":  ("SKOS Primer 4.6 Combining SKOS and OWL", SKOSPRIMER + "#secskosowl"),
    "skosS27":        ("SKOS Reference 8.6 integrity condition S27, related and broaderTransitive are disjoint", SKOSREF + "#L2422"),
    # OWL 2
    "primerClasses":  ("OWL 2 Primer 4.1 Classes, Properties and Individuals", PRIMER + "#Classes.2C_Properties.2C_and_Individuals_.E2.80.93_And_Basic_Modeling_With_Them"),
    "primerHierarchy": ("OWL 2 Primer 4.2 Class Hierarchies", PRIMER + "#Class_Hierarchies"),
    "primerDisjoint": ("OWL 2 Primer 4.3 Class Disjointness", PRIMER + "#Class_Disjointness"),
    "primerObjectProps": ("OWL 2 Primer 4.4 Object Properties", PRIMER + "#Object_Properties"),
    "primerPropHierarchy": ("OWL 2 Primer 4.5 Property Hierarchies", PRIMER + "#Property_Hierarchies"),
    "primerDomainRange": ("OWL 2 Primer 4.6 Domain and Range Restrictions", PRIMER + "#Domain_and_Range_Restrictions"),
    "primerEquality": ("OWL 2 Primer 4.7 Equality and Inequality of Individuals", PRIMER + "#Equality_and_Inequality_of_Individuals"),
    "primerDatatypes": ("OWL 2 Primer 4.8 Datatypes", PRIMER + "#Datatypes"),
    "primerComplex":  ("OWL 2 Primer 5.1 Complex Classes", PRIMER + "#Complex_Classes"),
    "primerRestrictions": ("OWL 2 Primer 5.2 Property Restrictions", PRIMER + "#Property_Restrictions"),
    "primerExistential": ("OWL 2 Primer 5.2 Property Restrictions: existential quantification", PRIMER + "#Property_Restrictions"),
    "primerUniversal": ("OWL 2 Primer 5.2 Property Restrictions: universal quantification", PRIMER + "#Property_Restrictions"),
    "primerCardinality": ("OWL 2 Primer 5.2.3 Property Cardinality Restrictions", PRIMER + "#Property_Cardinality_Restrictions"),
    "primerEnumeration": ("OWL 2 Primer 5.3 Enumeration of Individuals", PRIMER + "#Enumeration_of_Individuals"),
    "primerCharacteristics": ("OWL 2 Primer 6 Advanced Use of Properties", PRIMER + "#Advanced_Use_of_Properties"),
    "primerInverse":  ("OWL 2 Primer 6 Advanced Use of Properties: inverse properties", PRIMER + "#Advanced_Use_of_Properties"),
    "primerChains":   ("OWL 2 Primer 6.4 Property Chains", PRIMER + "#Property_Chains"),
    "primerKeys":     ("OWL 2 Primer 6.5 Keys", PRIMER + "#Keys"),
    "primerAdvancedDatatypes": ("OWL 2 Primer 7 Advanced Use of Datatypes", PRIMER + "#Advanced_Use_of_Datatypes"),
    "primerPunning":  ("OWL 2 Primer 8.1 Punning", PRIMER + "#a_Punning"),
    "primerAnnotations": ("OWL 2 Primer 8.2 Document Information and Annotations", PRIMER + "#Document_Information_and_Annotations"),
    "primerManagement": ("OWL 2 Primer 9 Ontology Management", PRIMER + "#Ontology_Management"),
    "primerDlFull":   ("OWL 2 Primer 10.1 OWL 2 DL and OWL 2 Full", PRIMER + "#OWL_2_DL_and_OWL_2_Full"),
    "primerProfiles": ("OWL 2 Primer 10.2 OWL 2 Profiles", PRIMER + "#OWL_2_Profiles"),
    "primerOpenWorld": ("OWL 2 Primer 2.2 Modeling Knowledge: Basic Notions (the open world, no unique names)", PRIMER + "#Modeling_Knowledge:_Basic_Notions"),
    "syntaxDatatypeMap": ("OWL 2 Structural Specification 4 Datatype Maps", SYNTAX + "#Datatype_Maps"),
    "syntaxGlobal":   ("OWL 2 Structural Specification 11 Global Restrictions on Axioms in OWL 2 DL", SYNTAX + "#Global_Restrictions_on_Axioms_in_OWL_2_DL"),
    "syntaxTyping":   ("OWL 2 Structural Specification 5.8.1 Typing Constraints of OWL 2 DL", SYNTAX + "#Typing_Constraints_of_OWL_2_DL"),
    "syntaxDeclarations": ("OWL 2 Structural Specification 5.8 Entity Declarations and Typing", SYNTAX + "#Entity_Declarations_and_Typing"),
    "syntaxOntologyIri": ("OWL 2 Structural Specification 3.1 Ontology IRI and Version IRI", SYNTAX + "#Ontology_IRI_and_Version_IRI"),
    "syntaxImports":  ("OWL 2 Structural Specification 3.4 Imports", SYNTAX + "#Imports"),
    "syntaxMetamodeling": ("OWL 2 Structural Specification 5.9 Metamodeling", SYNTAX + "#Metamodeling"),
    "syntaxAnnotationProps": ("OWL 2 Structural Specification 5.5 Annotation Properties", SYNTAX + "#Annotation_Properties"),
    "syntaxKeys":     ("OWL 2 Structural Specification 9.5 Keys", SYNTAX + "#Keys"),
    "profilesEL":     ("OWL 2 Profiles 2 OWL 2 EL", PROFILES + "#OWL_2_EL"),
    "profilesQL":     ("OWL 2 Profiles 3 OWL 2 QL", PROFILES + "#OWL_2_QL"),
    "profilesRL":     ("OWL 2 Profiles 4 OWL 2 RL", PROFILES + "#OWL_2_RL"),
    "directSemantics": ("OWL 2 Direct Semantics 2.2 Interpretations", DIRECT + "#Interpretations"),
    "shaclSpec":      ("SHACL: constraints on data, which OWL axioms are not", SHACL),
    # Reasoning
    "sparqlCourseInference": ("The SPARQL course, module 18: inference", SPARQL_COURSE + "#m18"),
    "shaclCourseInference": ("The SHACL course, module 09: validating with inference", SHACL_COURSE + "#m09"),
    "semopsRules":    ("SemOps Manual 11.2 Three ways to derive a triple", SEMOPS + "11-rules-and-inference.md#112-three-ways-to-derive-a-triple"),
    # Upper ontologies
    "gistBfo":        ("gistBFO: gist mapped to the Basic Formal Ontology", GISTBFO),
    "bfo":            ("BFO 2020", BFO),
    # Quality
    "oquare":         ("Duque-Ramos, Fernandez-Breis, Stevens and Aussenac-Gilles, OQuaRE: a SQuaRE-based approach for evaluating the quality of ontologies, JRPIT 43(2), 2011", OQUARE),
    "oqs":            ("The Ontology Quality Suite", OQS),
    "semopsGate":     ("SemOps Manual 9.4 The right fix: --own-namespace", SEMOPS + "09-continuous-integration.md#94-the-right-fix---own-namespace"),
    "semopsTestGate": ("SemOps Manual 9.8 Testing the gate itself", SEMOPS + "09-continuous-integration.md#98-testing-the-gate-itself"),
    "semopsCq":       ("SemOps Manual 8.1 Competency questions as tests", SEMOPS + "08-model-and-validate.md#competency-questions-as-tests"),
    "gistShapes":     ("gist: the shapes that enforce its own style", GIST + "/blob/develop/validation/shapes/ontologyShapes.ttl"),
    # Change
    "gistDeprecation": ("gist: deprecation and deletion policy", GISTDEP),
    "oboVersioning":  ("OBO Foundry principle FP-004, versioning", OBO + "fp-004-versioning.html"),
    "oboAuthority":   ("OBO Foundry principle FP-011, locus of authority", OBO + "fp-011-locus-of-authority.html"),
    "oboNotification": ("OBO Foundry principle FP-013, notification of changes", OBO + "fp-013-notification.html"),
    "oboMaintenance": ("OBO Foundry principle FP-016, maintenance", OBO + "fp-016-maintenance.html"),
    "semopsSemver":   ("SemOps Manual 12.1 Evidence-based semver: version-diff", SEMOPS + "12-release-and-change.md#121-evidence-based-semver-version-diff"),
    "semopsMigration": ("SemOps Manual 12.3 The migration annotation, and its direction", SEMOPS + "12-release-and-change.md#123-the-migration-annotation-and-its-direction"),
    "semopsTaxonomy": ("SemOps Manual 12.5 The taxonomy layer: pattern-consistency", SEMOPS + "12-release-and-change.md#125-the-taxonomy-layer-pattern-consistency"),
    "semopsDocgen":   ("SemOps Manual 13.2 Documentation as a product", SEMOPS + "13-operate-and-consume.md#132-documentation-as-a-product-docgen"),
    # Putting it together
    "sparqlCourse":   ("The SPARQL course: the questions this ontology exists to answer", SPARQL_COURSE),
    "shaclCourse":    ("The SHACL course: the constraints OWL cannot express", SHACL_COURSE),
}

# Which sections a module is defined by, in the order the README lists them.
MODULE_SPECS = {
    "00-the-lab": ["rdfGraph", "rdfsClass", "primerClasses", "skosConcepts"],
    "01-meaning": ["triangle", "peirce", "thingsNotStrings", "rdfIris", "rdfReferents", "rdfIriSection", "webarchId",
                   "webarchOwner", "webarchOpacity", "linkedData", "rfc3987", "semopsTerritory", "blogTeam", "oboScope"],
    "02-systematics": ["ontocleanCacm", "ontocleanHb", "ontocleanWp", "gufo", "gistUfo", "gistInstanceNames",
                       "semopsStyles"],
    "03-naming": ["gistLocalNames", "gistPropertyNames", "gistLabels", "gistTitleCase", "gistNamespaces", "gistNsDoc",
                  "gistInstanceNames", "oboUris", "oboNaming", "coolCool", "coolHash", "cool303", "coolChoosing",
                  "webarchOpacity", "rdfsLabel", "bcp47", "skosLabels", "skosS14"],
    "04-definitions": ["oboDefinitions", "gistAnnotations", "gistAnnotationFormat", "gistAnnotationCard", "niso",
                       "skosNotes", "rdfsComment", "oboStability", "oboDocumented", "dctTerms", "semopsTerritory"],
    "05-principles": ["gistReadme", "gistInverses", "gistRestrictions", "oboOpen", "oboRelations", "oboCollab",
                      "oboUsers", "semopsPriesthood", "semopsBudget", "semopsWorkshop", "semopsInnerLoop",
                      "semopsHouseRules", "semopsMaturity", "blogTeam", "blogUpper"],
    "06-the-ladder": ["rdfsClass", "rdfsType", "rdfsSubClassOf", "rdfsProperty", "rdfsDomain", "rdfsRange",
                      "rdfsSubPropertyOf", "rdfsEntailment", "rdfsRules", "skosConcepts", "skosSchemes", "skosLabels",
                      "skosSemantic", "skosCollections", "skosMapping", "skosPrimerRel", "skosPrimerOwl", "skosS27"],
    "07-owl": ["primerClasses", "primerDisjoint", "primerRestrictions", "primerExistential", "primerUniversal",
               "primerCardinality", "primerComplex", "primerEnumeration", "primerCharacteristics", "primerInverse",
               "primerChains", "primerKeys", "primerDomainRange", "primerEquality", "primerDatatypes", "primerPunning",
               "primerAnnotations", "primerDlFull", "primerProfiles", "primerOpenWorld", "syntaxGlobal",
               "syntaxDatatypeMap", "syntaxTyping", "syntaxDeclarations", "profilesEL", "profilesQL", "profilesRL",
               "gistRestrictions", "shaclSpec"],
    "08-reasoning": ["directSemantics", "primerOpenWorld", "primerDlFull", "profilesRL", "sparqlCourseInference",
                     "shaclCourseInference", "semopsRules"],
    "09-upper-ontologies": ["gistReadme", "blogUpper", "gistBfo", "bfo", "gistUfo", "gufo", "oboRelations"],
    "10-quality": ["oquare", "oqs", "semopsGate", "semopsTestGate", "semopsCq", "gistShapes", "semopsHouseRules"],
    "11-change": ["syntaxOntologyIri", "syntaxImports", "primerManagement", "gistDeprecation", "oboVersioning",
                  "oboAuthority", "oboNotification", "oboMaintenance", "oboStability", "semopsSemver",
                  "semopsMigration", "semopsDocgen", "vocabPub"],
    "12-putting-it-together": ["sparqlCourse", "shaclCourse", "semopsCq", "semopsTaxonomy"],
}

LESSON_SPECS: dict[str, list[str]] = {}


def register(oid: str, *keys: str) -> None:
    LESSON_SPECS[oid] = list(keys)


def for_lesson(oid: str, module: str, limit: int = 2) -> list[tuple[str, str]]:
    keys = LESSON_SPECS.get(oid) or MODULE_SPECS.get(module, [])
    return [SECTIONS[k] for k in keys[:limit]]


def for_module(module: str) -> list[tuple[str, str]]:
    seen, out = set(), []
    for k in MODULE_SPECS.get(module, []):
        if k not in seen:
            seen.add(k)
            out.append(SECTIONS[k])
    return out


# The reading list at the end of the README and the course document.
READING_LIST = [
    ("Meaning, and the identifiers that carry it", [
        (TRIANGLE, "The triangle of reference",
         "Ogden and Richards, 1923: symbol, thought, referent. The picture the course is drawn on."),
        (PEIRCE, "Peirce's theory of signs",
         "Where the word semiotic comes from. Sign, object and interpretant, a generation before Ogden and Richards."),
        (RDFC, "RDF 1.2 Concepts and Abstract Syntax",
         "Section 1.3, the referent of an IRI, is three paragraphs that settle most arguments about what an IRI means."),
        (WEBARCH, "Architecture of the World Wide Web, Volume One",
         "URI ownership and URI opacity: why an IRI is globally unique, and why a machine should not read anything into its spelling."),
        (COOL, "Cool URIs for the Semantic Web",
         "Hash or slash, and what a browser gets when it asks."),
        (LINKED, "Linked Data",
         "Four rules on one page. Use IRIs as names, make them HTTP, return something useful, link to others."),
    ]),
    ("Systematics and definitions", [
        (ONTOCLEAN_CACM, "Evaluating ontological decisions with OntoClean",
         "Guarino and Welty's short account: rigidity, identity, unity, dependence, and the subsumptions they forbid."),
        (ONTOCLEAN_HB, "An overview of OntoClean",
         "The longer treatment, in the Handbook on Ontologies. The backbone taxonomy is defined here."),
        (GUFO, "gUFO",
         "The Unified Foundational Ontology as a small OWL vocabulary: Kind, SubKind, Role, Phase, Category. Module 02 types the Trail's classes with it, as gistUFO types gist's."),
        (NISO, "ANSI/NISO Z39.19",
         "Monolingual controlled vocabularies: the rules for preferred terms, synonyms, scope notes and hierarchy that SKOS was built to carry."),
        (OBO_INDEX, "The OBO Foundry principles",
         "Sixteen principles, each on a page: open, textual definitions, stability of meaning, versioning, a named person responsible."),
    ]),
    ("Style guides and manuals", [
        (GISTSTYLE, "The gist Style Guide",
         "Local names, labels, the annotation set and its cardinalities, no inverses, and eleven rules for restrictions. The most concrete style guide in print."),
        (GIST, "gist",
         "Semantic Arts' minimalist upper ontology, CC-BY-4.0. Module 09 stands the Trail on it."),
        (GISTBFO, "gistBFO",
         "Forty subclass assertions from gist into BFO, each with a note saying why. Read as worked examples of alignment."),
        (GISTUFO, "gistUFO",
         "gist's classes typed as gUFO kinds, roles and phases. OntoClean applied to a real ontology."),
        (UPPER, "Is an upper ontology useful?",
         "Winstanley, ISKO UK 2023. A starter palette, a common vocabulary, a tool for thought, a hanger for data, and the Goldilocks level of abstraction. Module 09 opens with it."),
        (SEMOPS, "The SemOps Manual",
         "Running a semantic practice the way software is run. Chapters 2, 8, 9 and 12 are cited here: definitions are territory, the inner loop, the gate, and evidence-based versioning."),
        (OQUARE, "OQuaRE",
         "The quality model module 10 measures with: fourteen metrics, each scored one to five against published thresholds."),
        (OQS, "The Ontology Quality Suite",
         "The checks module 10 runs, by identifier. pip install ontology-quality-suite."),
    ]),
    ("The languages", [
        (RDFS, "RDF 1.2 Schema",
         "rdfs:Class, rdfs:subClassOf, rdfs:domain, rdfs:range, rdfs:label and rdfs:comment. The first rung of the ladder."),
        (SKOSREF, "SKOS Reference",
         "Concept schemes, labels, broader and narrower, notes, collections, mapping, and the integrity conditions."),
        (SKOSPRIMER, "SKOS Primer",
         "The readable one, including the section on combining SKOS with OWL."),
        (PRIMER, "OWL 2 Primer",
         "Start here for OWL. Every construct module 07 uses is introduced with an example."),
        (SYNTAX, "OWL 2 Structural Specification and Functional-Style Syntax",
         "The normative one: the datatype map, the global restrictions, and what OWL 2 DL requires of declarations."),
        (PROFILES, "OWL 2 Profiles",
         "EL, QL and RL: what each gives up and what it gets in return."),
        (SHACL, "SHACL",
         "For the constraints an ontology should not try to express. The SHACL course covers it in full."),
    ]),
]
