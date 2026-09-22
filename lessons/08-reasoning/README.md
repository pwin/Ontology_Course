# Module 08 · Reasoning

What follows from what you said. Consistency, unsatisfiable classes, the inferred hierarchy, an explanation traced back to the axioms that caused it, and the difference between an OWL 2 RL closure like the editor's and a description-logic reasoner like HermiT. The module ends by reasoning over the whole Trail, and finds the reason one property was left non-functional.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m08).

**Sources.** What this module is defined by, or argued from:

- [OWL 2 Direct Semantics 2.2 Interpretations](https://www.w3.org/TR/owl2-direct-semantics/#Interpretations)
- [OWL 2 Primer 2.2 Modeling Knowledge: Basic Notions (the open world, no unique names)](https://www.w3.org/TR/owl2-primer/#Modeling_Knowledge:_Basic_Notions)
- [OWL 2 Primer 10.1 OWL 2 DL and OWL 2 Full](https://www.w3.org/TR/owl2-primer/#OWL_2_DL_and_OWL_2_Full)
- [OWL 2 Profiles 4 OWL 2 RL](https://www.w3.org/TR/owl2-profiles/#OWL_2_RL)
- [The SPARQL course, module 18: inference](https://www.semantechs.co.uk/SPARQL_Course/#m18)
- [The SHACL course, module 09: validating with inference](https://www.semantechs.co.uk/SHACL_Course/#m09)
- [SemOps Manual 11.2 Three ways to derive a triple](https://github.com/pwin/SemOpsManual/blob/main/docs/11-rules-and-inference.md#112-three-ways-to-derive-a-triple)

| Lesson | Decides | Corner |
|---|---|---|
| [o51 What follows from what you said](o51-what-follows-from-what-you-said.ttl) | An inference is a statement true in every interpretation that satisfies the ontology; a reasoner finds them; adding axioms never removes one; and 'not said' is not 'false'. | referent |
| [o52 Three routes to one inference](o52-three-routes-to-one-inference.ttl) | The transitive closure of bs:within, sixty-three pairs becoming a hundred and eighty-six, is reached by an OWL reasoner, by a SPARQL property path, and by a SHACL rule iterated to a fixpoint; each is measured, and the choice between them is a matter of when and where the work is done. | referent |
| [o53 Inconsistency: the three usual causes](o53-inconsistency-the-three-usual-causes.ttl) | A contradiction is traced to one of three habits: a thing typed with two disjoint kinds, a functional property with two values declared different, or a value that its datatype cannot hold; each is seeded, and the reasoner names the axioms responsible. | referent |
| [o54 Unsatisfiable classes: consistent, and dead](o54-unsatisfiable-classes-consistent-and-dead.ttl) | A class that can have no instances is found by the reasoner before any data arrives; the ontology stays consistent, and the class is fixed rather than shipped. | referent |
| [o55 Classification: the hierarchy the reasoner infers](o55-classification-the-hierarchy-the-reasoner-infers.ttl) | Subclass relations that follow from definitions are left for the reasoner to infer rather than asserted, and the inferred hierarchy is compared with the asserted one as a check on both. | referent |
| [o56 Two reasoners: the rule engine and the description logic](o56-two-reasoners-the-rule-engine-and-the-description-logic.ttl) | The editor's OWL 2 RL closure is used for what it does well, typing individuals and closing properties, and a description-logic reasoner for what only it does, which is to classify, to find the dead classes, and to explain. | referent |
| [o57 Reasoning over the whole Trail](o57-reasoning-over-the-whole-trail.ttl) | The shipped vocabulary and the whole dataset go through a description-logic reasoner together: consistent, one hundred and eighty-six within pairs, the reversed segments and inverses materialised, and not one new type, because the data types everything already. | referent |
