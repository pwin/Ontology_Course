# Module 02 · Systematics

A taxonomy is a set of claims about what things are, and some of those claims are wrong in ways that do not show until the ontology is used. OntoClean gives four questions to ask of every class: could an instance stop being one, what makes two of them the same, is each one a whole, and does it exist only in relation to something else. The answers decide which subclass links will bear weight. The module ends with the checks written as queries, and with gist read through them.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m02).

**Sources.** What this module is defined by, or argued from:

- [Guarino and Welty, Evaluating ontological decisions with OntoClean, CACM 45(2), 2002](https://doi.org/10.1145/503124.503150)
- [Guarino and Welty, An overview of OntoClean, Handbook on Ontologies, 2009](https://doi.org/10.1007/978-3-540-92673-3_9)
- [OntoClean: the four meta-properties](https://en.wikipedia.org/wiki/OntoClean)
- [gUFO: a lightweight implementation of the Unified Foundational Ontology](https://nemo-ufes.github.io/gufo/)
- [gistUFO: gist aligned with gUFO](https://github.com/semanticarts/gistUFO)
- [gist Style Guide: instance local names, and the most specific rigid class](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#instance-local-names)
- [SemOps Manual 2.3 Cognitive styles](https://github.com/pwin/SemOpsManual/blob/main/docs/02-people-and-cognition.md#23-cognitive-styles-people-do-not-categorise-the-same-way)

| Lesson | Decides | Corner |
|---|---|---|
| [o08 A concrete kind and a role: Person and Author](o08-a-concrete-kind-and-a-role-person-and-author.ttl) | Person is a rigid kind and Author is a role a person plays, so Author is placed under Person and never the other way round. | referent |
| [o09 The subsumption that will not bear weight](o09-the-subsumption-that-will-not-bear-weight.ttl) | 'Every bookshop is a trail member' is read as a role, not a subclass, and the draft that put Bookshop under TrailMember is reversed. | referent |
| [o10 Identity: what makes two of them the same](o10-identity-what-makes-two-of-them-the-same.ttl) | Work, Edition and Copy carry different criteria of identity, so they are three classes and disjoint; Work is what the Trail keeps, with the compromise written on it. | referent |
| [o11 Phases: the same thing, for a while](o11-phases-the-same-thing-for-a-while.ttl) | Living and dead authors, and past and scheduled events, are phases of one kind, not kinds of their own; gist's ContemporaryEvent and HistoricalEvent are the published example. | referent |
| [o12 The backbone](o12-the-backbone.ttl) | The rigid classes of the Trail form its backbone taxonomy; roles and phases hang off it and never form part of it. | referent |
| [o13 The taxonomy checks itself](o13-the-taxonomy-checks-itself.ttl) | OntoClean's constraints are written as SPARQL queries over the annotations, so that a taxonomy can be checked in the editor before a reasoner ever sees it. | referent |
| [o14 Reading gist through OntoClean](o14-reading-gist-through-ontoclean.ttl) | The Trail's classes are typed with gUFO's Kind, SubKind, Role and Phase, the way gistUFO types gist's, and the typing is checked to agree with the annotations. | referent |
