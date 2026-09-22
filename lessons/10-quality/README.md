# Module 10 · Quality

Measuring what was built, and knowing what the measurements cannot see. OQuaRE's metrics scored on the Trail and on gist; the Ontology Quality Suite's checks by identifier; style shapes like the ones gist runs on itself; competency questions as tests. Then the limits: a five-out-of-five ontology can still be wrong, and no metric sees rigidity.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then open the LOAD IT link, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m10).

**Sources.** What this module is defined by, or argued from:

- [Duque-Ramos, Fernandez-Breis, Stevens and Aussenac-Gilles, OQuaRE: a SQuaRE-based approach for evaluating the quality of ontologies, JRPIT 43(2), 2011](http://www.cs.man.ac.uk/~stevensr/papers/OQuareProof.pdf)
- [The Ontology Quality Suite](https://github.com/pwin/consolidated-ontology-quality-suite-python)
- [SemOps Manual 9.4 The right fix: --own-namespace](https://github.com/pwin/SemOpsManual/blob/main/docs/09-continuous-integration.md#94-the-right-fix---own-namespace)
- [SemOps Manual 9.8 Testing the gate itself](https://github.com/pwin/SemOpsManual/blob/main/docs/09-continuous-integration.md#98-testing-the-gate-itself)
- [SemOps Manual 8.1 Competency questions as tests](https://github.com/pwin/SemOpsManual/blob/main/docs/08-model-and-validate.md#competency-questions-as-tests)
- [gist: the shapes that enforce its own style](https://github.com/semanticarts/gist/blob/develop/validation/shapes/ontologyShapes.ttl)
- [SemOps Manual 8.4 Your own rules, without forking anything](https://github.com/pwin/SemOpsManual/blob/main/docs/08-model-and-validate.md#84-your-own-rules-without-forking-anything)

| Lesson | Decides | Corner |
|---|---|---|
| [o63 OQuaRE in a page](o63-oquare-in-a-page.ttl) | Quality is assessed with a published model rather than a feeling: OQuaRE's characteristics, sub-characteristics and metrics, each metric scored one to five against the paper's thresholds, and the scores read as a map of strengths rather than a mark. | thought |
| [o64 Structure: depth, breadth, tangledness, cohesion](o64-structure-depth-breadth-tangledness-cohesion.ttl) | The Trail's hierarchy is two deep, one wide on average, untangled and cohesive, which the structural metrics confirm; and gist, measured the same way, shows sixty-two roots because its structure lives in definitions the metrics do not read. | referent |
| [o65 Richness and coupling: what the metrics count, and what a style choice does to them](o65-richness-and-coupling-what-the-metrics-count-and-what-a-style-choice-does-to-them.ttl) | The richness metrics are read with their small print: they count properties by declared domain, so an ontology that keeps domains sparse on principle scores low on richness, and gist does. | referent |
| [o66 The checks, by identifier](o66-the-checks-by-identifier.ttl) | The shipped vocabulary goes through the Ontology Quality Suite scoped to its own namespace, and the findings are read by identifier: a check that fires on every term is a policy not adopted, not a hundred mistakes. | thought |
| [o67 Style shapes: the vocabulary validated like data](o67-style-shapes-the-vocabulary-validated-like-data.ttl) | The house style is written as SHACL shapes that target owl:Class and the property types, as gist does for itself, and the shipped vocabulary is validated against them in the editor. | symbol and thought |
| [o68 What the metrics cannot see](o68-what-the-metrics-cannot-see.ttl) | Metrics and checks are one part of a gate that also runs the reasoner, the OntoClean queries, the style shapes and the competency questions, because a five-out-of-five ontology can still be wrong and no metric sees rigidity or meaning. | thought |
