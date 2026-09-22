# Module 05 · Design principles

What a well-made ontology has in common, drawn from three places that agree more than they differ: the gist style guide, the OBO Foundry principles, and the SemOps Manual. Minimal, reused before invented, disjoint at the top, sparse in its domains and ranges, meaning rather than integrity, and built with the people who will have to read it.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m05).

**Sources.** What this module is defined by, or argued from:

- [gist: a minimalist upper ontology](https://github.com/semanticarts/gist)
- [gist Style Guide: inverses, and why gist has none](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#inverses)
- [gist Style Guide: OWL restrictions, the eleven rules](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#owl-restrictions)
- [OBO Foundry principle FP-001, open](https://obofoundry.org/principles/fp-001-open.html)
- [OBO Foundry principle FP-007, relations: reuse existing ones](https://obofoundry.org/principles/fp-007-relations.html)
- [OBO Foundry principle FP-010, commitment to collaboration](https://obofoundry.org/principles/fp-010-collaboration.html)
- [OBO Foundry principle FP-009, documented plurality of users](https://obofoundry.org/principles/fp-009-users.html)
- [SemOps Manual 2.2 The priesthood problem](https://github.com/pwin/SemOpsManual/blob/main/docs/02-people-and-cognition.md#22-the-priesthood-problem)
- [SemOps Manual 2.4 Cognitive capacity is a hard budget](https://github.com/pwin/SemOpsManual/blob/main/docs/02-people-and-cognition.md#24-cognitive-capacity-is-a-hard-budget)
- [SemOps Manual 2.5 The workshop is a social event with a technical output](https://github.com/pwin/SemOpsManual/blob/main/docs/02-people-and-cognition.md#25-the-workshop-is-a-social-event-with-a-technical-output)
- [SemOps Manual 8.1 The inner loop belongs in the editor](https://github.com/pwin/SemOpsManual/blob/main/docs/08-model-and-validate.md#81-the-inner-loop-belongs-in-the-editor)
- [SemOps Manual 8.4 Your own rules, without forking anything](https://github.com/pwin/SemOpsManual/blob/main/docs/08-model-and-validate.md#84-your-own-rules-without-forking-anything)
- [SemOps Manual 6.3 The five maturity levels](https://github.com/pwin/SemOpsManual/blob/main/docs/06-stages-and-stories.md#63-the-five-maturity-levels)
- [Winstanley, Team building: the importance of an ontology (2025)](https://www.semanticarts.com/team-building-the-importance-of-an-ontology/)
- [Winstanley, Is an upper ontology useful? ISKO UK 2023, CEUR-WS Vol. 3661](https://ceur-ws.org/Vol-3661/10-SHORT-PWinstanley-ISKOUK2023.pdf)

| Lesson | Decides | Corner |
|---|---|---|
| [o28 Minimal: as few terms as will answer the questions](o28-minimal-as-few-terms-as-will-answer-the-questions.ttl) | The Trail has twenty-five classes because ten questions need them; a class that no question needs is not added, and gist's ninety-six for a whole enterprise is the standard to be measured against. | thought |
| [o29 Meaning in the ontology, rules in the shapes](o29-meaning-in-the-ontology-rules-in-the-shapes.ttl) | An axiom is written only when it is true of every dataset the ontology could describe; anything that is a rule about this dataset, for this purpose, is a SHACL shape, and bs:founded stays non-functional for exactly that reason. | referent |
| [o30 Pragmatism and purity](o30-pragmatism-and-purity.ttl) | A departure from a principle is allowed when it changes only a name or a convenience, refused when it changes an inference or a query, and written on the term either way. | thought |
| [o31 Disjoint at the top, sparse in the middle, no inverses](o31-disjoint-at-the-top-sparse-in-the-middle-no-inverses.ttl) | The top-level kinds are declared pairwise disjoint, domains and ranges are declared only where every use will agree, and inverses are not declared unless a lesson needs one. | referent |
| [o32 One parent, mostly](o32-one-parent-mostly.ttl) | Every backbone class has one parent; a second parent is allowed only for a rigid subkind that is both things in every circumstance, and the tangledness is measured rather than assumed. | referent |
| [o33 Built with the people who will read it](o33-built-with-the-people-who-will-read-it.ttl) | Every definition records who agreed it and when, the domain experts review the model in a form they can read, and a disagreement about territory is modelled rather than adjudicated by the modeller. | thought |
| [o34 Ontologies like code: the loop and the gate](o34-ontologies-like-code-the-loop-and-the-gate.ttl) | The vocabulary lives in version control, is checked in the editor as it is written and at the gate before it merges, and the checks are asserted by identifier and scoped to the Trail's own namespace. | thought |
