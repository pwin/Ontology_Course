# Module 06 · The ladder: RDFS and SKOS

RDFS, SKOS and OWL 2 are one idea at rising degrees of commitment. A list of labelled terms says almost nothing; a concept scheme says how the terms relate without saying what they are; a class hierarchy says that membership is inherited, and a reasoner starts to draw conclusions. This module climbs the first rungs with the genre scheme and the place hierarchy, and says at each rung what has been promised.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m06).

**Sources.** What this module is defined by, or argued from:

- [RDF Schema 2.2 rdfs:Class](https://www.w3.org/TR/rdf12-schema/#ch_class)
- [RDF Schema 3.3 rdf:type](https://www.w3.org/TR/rdf12-schema/#ch_type)
- [RDF Schema 3.4 rdfs:subClassOf](https://www.w3.org/TR/rdf12-schema/#ch_subclassof)
- [RDF Schema 2.5 rdf:Property](https://www.w3.org/TR/rdf12-schema/#ch_property)
- [RDF Schema 3.2 rdfs:domain](https://www.w3.org/TR/rdf12-schema/#ch_domain)
- [RDF Schema 3.1 rdfs:range](https://www.w3.org/TR/rdf12-schema/#ch_range)
- [RDF Schema 3.5 rdfs:subPropertyOf](https://www.w3.org/TR/rdf12-schema/#ch_subpropertyof)
- [RDF 1.2 Semantics 9 RDFS Interpretations](https://www.w3.org/TR/rdf12-semantics/#rdfs_interpretations)
- [RDF 1.2 Semantics 9.2 RDFS Entailment](https://www.w3.org/TR/rdf12-semantics/#rdfs_entailment)
- [SKOS Reference 3 The skos:Concept Class](https://www.w3.org/TR/skos-reference/#concepts)
- [SKOS Reference 4 Concept Schemes](https://www.w3.org/TR/skos-reference/#schemes)
- [SKOS Reference 5 Lexical Labels](https://www.w3.org/TR/skos-reference/#labels)
- [SKOS Reference 8 Semantic Relations](https://www.w3.org/TR/skos-reference/#semantic-relations)
- [SKOS Reference 9 Concept Collections](https://www.w3.org/TR/skos-reference/#collections)
- [SKOS Reference 10 Mapping Properties](https://www.w3.org/TR/skos-reference/#mapping)
- [SKOS Primer 2.3 Semantic Relationships](https://www.w3.org/TR/skos-primer/#secrel)
- [SKOS Primer 4.6 Combining SKOS and OWL](https://www.w3.org/TR/skos-primer/#secskosowl)
- [SKOS Reference 8.6 integrity condition S27, related and broaderTransitive are disjoint](https://www.w3.org/TR/skos-reference/#L2422)

| Lesson | Decides | Corner |
|---|---|---|
| [o35 A class is a set, in every model](o35-a-class-is-a-set-in-every-model.ttl) | Classes are read as sets and the vocabulary's structural words as set operations: rdf:type is membership, rdfs:subClassOf is subset, equivalence is equality, disjointness is an empty intersection. | referent |
| [o36 Rung one, a list; rung two, a concept scheme](o36-rung-one-a-list;-rung-two-a-concept-scheme.ttl) | The genres are a SKOS concept scheme: particulars with labels, arranged by broader and narrower, promising nothing about the works in them; and the scheme's uneven depth is kept because it is true. | symbol and thought |
| [o37 Rung three, a class hierarchy: membership is inherited](o37-rung-three-a-class-hierarchy-membership-is-inherited.ttl) | Places are a class hierarchy, not a concept scheme, because a query about Places must find every Settlement without being told; rdfs:subClassOf commits to that and a reasoner delivers it. | referent |
| [o38 Rung four, domain and range: inference rules, not constraints](o38-rung-four-domain-and-range-inference-rules-not-constraints.ttl) | A domain is declared only when everything that will ever have the property is of that class, because the reasoner will type whatever has it; the Trail's bs:locatedIn gets a union domain for that reason. | referent |
| [o39 SKOS in full: labels, notes, related, mapping, and the integrity conditions](o39-skos-in-full-labels-notes-related-mapping-and-the-integrity-conditions.ttl) | The genre scheme carries one preferred label per language, alternatives, scope notes, associative links kept apart from hierarchy, and mappings to outside schemes by match properties rather than owl:sameAs; and its integrity is checked by shapes. | all three |
| [o40 Climbing a rung: when a concept becomes a class](o40-climbing-a-rung-when-a-concept-becomes-a-class.ttl) | Where an axiom about members is needed, the concept is punned into a class as well, with rdfs:subClassOf running beside skos:broader, and the reasoner then types works by their genre's ancestors. | referent |
| [o41 What RDFS cannot say](o41-what-rdfs-cannot-say.ttl) | Disjointness, cardinality, inverses, defined classes and 'exactly one' are wanted and RDFS has none of them, so the list of what it cannot say becomes the agenda for the top of the ladder. | referent |
