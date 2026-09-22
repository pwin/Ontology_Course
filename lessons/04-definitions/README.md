# Module 04 · Definitions and controlled vocabularies

The thought corner, written down. A definition is the agreement that makes a shared symbol carry a shared meaning, and a controlled vocabulary is a list of terms whose definitions someone has agreed to look after. This module covers the form of a good definition, the ways one fails, the set of annotations that carry it, and the decision that comes before any taxonomy: is this a class, or a category.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then open the LOAD IT link, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m04).

**Sources.** What this module is defined by, or argued from:

- [OBO Foundry principle FP-006, textual definitions](https://obofoundry.org/principles/fp-006-textual-definitions.html)
- [gist Style Guide: conventions for annotation use](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#conventions-for-annotation-use)
- [gist Style Guide: formatting conventions for annotations](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#formatting-conventions-for-annotations)
- [gist Style Guide: annotation cardinality](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#annotation-cardinality)
- [ANSI/NISO Z39.19, Guidelines for the construction of monolingual controlled vocabularies](https://groups.niso.org/higherlogic/ws/public/download/12591/z39-19-2005r2010.pdf)
- [SKOS Reference 7 Documentation Properties](https://www.w3.org/TR/skos-reference/#notes)
- [RDF Schema 3.6 rdfs:comment](https://www.w3.org/TR/rdf12-schema/#ch_comment)
- [OBO Foundry principle FP-019, stability of term meaning](https://obofoundry.org/principles/fp-019-term-stability.html)
- [OBO Foundry principle FP-008, documentation](https://obofoundry.org/principles/fp-008-documented.html)
- [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- [SemOps Manual 2.1 Definitions are territory](https://github.com/pwin/SemOpsManual/blob/main/docs/02-people-and-cognition.md#21-definitions-are-territory)

| Lesson | Decides | Corner |
|---|---|---|
| [o21 A definition is not a label](o21-a-definition-is-not-a-label.ttl) | Every class and property gets a definition in the form 'a genus that differs thus', one sentence, and anything else that was in the comment moves to a scope note. | thought |
| [o22 How a definition fails](o22-how-a-definition-fails.ttl) | Five failing definitions from the draft are named for what they are, circular, too broad, by example, negative and by IRI, and each is rewritten. | thought |
| [o23 The annotation set](o23-the-annotation-set.ttl) | Each term carries prefLabel and definition exactly once, scopeNote and example where they help, editorialNote for the maintainers, and never rdfs:comment as a dumping ground. | thought |
| [o24 Class or category: when a concept becomes a class](o24-class-or-category-when-a-concept-becomes-a-class.ttl) | A genre stays a concept, a particular that a work belongs to and a shop specialises in, and is promoted to a class only when something must be said about its members as a set. | referent |
| [o25 A controlled vocabulary before a taxonomy](o25-a-controlled-vocabulary-before-a-taxonomy.ttl) | The event kinds stop being strings in the data and become a controlled list of seven terms with one preferred label each, synonyms, a scope note and a maintainer. | thought |
| [o26 Borrow the term, or borrow the definition](o26-borrow-the-term-or-borrow-the-definition.ttl) | A term is reused by IRI only when its published meaning is the meaning wanted; otherwise the Trail mints its own and cites the source; and every borrowed term is declared. | symbol and thought |
| [o27 Once published, a term means what it meant](o27-once-published-a-term-means-what-it-meant.ttl) | A definition may be clarified but never changed to denote different things; when the meaning must change, a new term is minted and the old one deprecated with a pointer. | thought |
