# Module 12 · Putting it together

The whole Trail vocabulary, rebuilt and compared with the shipped one decision by decision; the genre scheme with its integrity checked; the competency questions the SPARQL course answers and the constraints the SHACL course enforces, as the test suite this ontology exists to pass; and a challenge.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m12).

**Sources.** What this module is defined by, or argued from:

- [The SPARQL course: the questions this ontology exists to answer](https://www.semantechs.co.uk/SPARQL_Course/)
- [The SHACL course: the constraints OWL cannot express](https://www.semantechs.co.uk/SHACL_Course/)
- [SemOps Manual 8.1 Competency questions as tests](https://github.com/pwin/SemOpsManual/blob/main/docs/08-model-and-validate.md#competency-questions-as-tests)
- [SemOps Manual 12.5 The taxonomy layer: pattern-consistency](https://github.com/pwin/SemOpsManual/blob/main/docs/12-release-and-change.md#125-the-taxonomy-layer-pattern-consistency)

| Lesson | Decides | Corner |
|---|---|---|
| [o73 The whole vocabulary, decision by decision](o73-the-whole-vocabulary-decision-by-decision.ttl) | The shipped vocabulary is read as the sum of the course's decisions, each traced to the lesson that made it, and put through every instrument the course has: profile, reasoner, metrics, checks, audits. | all three |
| [o74 The genre scheme, complete](o74-the-genre-scheme-complete.ttl) | The shipped genre scheme, thirty-one concepts two to four levels deep, passes the SKOS integrity shapes of o39 and the cycle and depth queries, and is kept a concept scheme rather than promoted. | all three |
| [o75 The questions answered, and the rules kept elsewhere](o75-the-questions-answered-and-the-rules-kept-elsewhere.ttl) | The brief's ten questions are run against the whole dataset as the acceptance test of the vocabulary, and the constraints the ontology declined to express are found in the SHACL course, where they belong. | all three |
| [o76 Challenge: the day a second edition appears](o76-challenge-the-day-a-second-edition-appears.ttl) | Split bs:Work into Work and Edition so that the compromise of o10 is retired, every assertion made under the old meaning stays true, the competency questions still answer, and the reasoner agrees; an answer is beside the lesson, to be read after yours. | all three |
