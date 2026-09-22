# Module 01 · Meaning

Before a class or a property, there is a word, the thing it stands for, and the idea in between. The triangle of reference is the oldest picture of that, and it is the picture this whole course is drawn on. This module puts the Bookshop Trail's nouns on it, shows the two ways a word fails, and introduces the one kind of symbol that is globally unique and that a machine can compare: the IRI. Strings to things.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then open the LOAD IT link, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m01).

**Sources.** What this module is defined by, or argued from:

- [Ogden and Richards, the triangle of reference (1923)](https://en.wikipedia.org/wiki/Triangle_of_reference)
- [Peirce's theory of signs, Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/peirce-semiotics/)
- [Google, 'things, not strings' (2012)](https://blog.google/products/search/introducing-knowledge-graph-things-not/)
- [RDF 1.2 Concepts 1.2 Resources and Statements](https://www.w3.org/TR/rdf12-concepts/#resources-and-statements)
- [RDF 1.2 Concepts 1.3 The Referent of an IRI](https://www.w3.org/TR/rdf12-concepts/#referents)
- [RDF 1.2 Concepts 3.2 IRIs](https://www.w3.org/TR/rdf12-concepts/#section-IRIs)
- [Architecture of the World Wide Web 2 Identification](https://www.w3.org/TR/webarch/#identification)
- [Architecture of the World Wide Web 2.2.2.1 URI Ownership](https://www.w3.org/TR/webarch/#uri-ownership)
- [Architecture of the World Wide Web 2.5 URI Opacity](https://www.w3.org/TR/webarch/#uri-opacity)
- [Berners-Lee, Linked Data (2006): the four rules](https://www.w3.org/DesignIssues/LinkedData.html)
- [RFC 3987 Internationalized Resource Identifiers](https://www.rfc-editor.org/rfc/rfc3987)
- [SemOps Manual 2.1 Definitions are territory](https://github.com/pwin/SemOpsManual/blob/main/docs/02-people-and-cognition.md#21-definitions-are-territory)
- [Winstanley, Team building: the importance of an ontology (2025)](https://www.semanticarts.com/team-building-the-importance-of-an-ontology/)
- [OBO Foundry principle FP-005, scope](https://obofoundry.org/principles/fp-005-delineated-content.html)

| Lesson | Decides | Corner |
|---|---|---|
| [o01 A word, a thing, and the idea in between](o01-a-word-a-thing-and-the-idea-in-between.ttl) | Every term in the brief is a symbol standing for a referent by way of a thought, and the three are kept apart from the first line. | all three, introduced |
| [o02 One word, many things; many words, one thing](o02-one-word-many-things;-many-words-one-thing.ttl) | 'Book' is split into three referents and 'shop', 'bookshop' and 'store' are merged into one, because identity follows the referent and not the word. | symbol and referent |
| [o03 Shared meaning is an agreement](o03-shared-meaning-is-an-agreement.ttl) | A definition is treated as the record of an agreement, with who made it and when, and a disagreement is modelled rather than settled by the modeller. | thought |
| [o04 A symbol that is globally unique, and that a machine can read](o04-a-symbol-that-is-globally-unique-and-that-a-machine-can-read.ttl) | Every referent gets an IRI, because an IRI is the one kind of symbol that cannot collide with anyone else's and that a machine can compare, join on and look up. | symbol |
| [o05 A particular or a kind](o05-a-particular-or-a-kind.ttl) | Wigtown, The Inkwell and Rhona Blackwood are particulars; Settlement, Bookshop and Person are kinds; rdf:type is the link, and a kind is a referent with an IRI like any other. | referent |
| [o06 A relationship is a thing too](o06-a-relationship-is-a-thing-too.ttl) | The brief's verbs become properties with IRIs of their own: locatedIn, wrote, stocks, heldAt; its measurements become datatype properties; and a property is defined like any other term. | referent |
| [o07 Scope, and the questions that fix it](o07-scope-and-the-questions-that-fix-it.ttl) | The ontology covers what the brief's ten questions need and nothing the brief only mentions; the questions are written into the ontology as its statement of scope. | thought |
