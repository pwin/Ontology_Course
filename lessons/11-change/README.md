# Module 11 · Release and change

An ontology is for life. The header that says what it is, the policy that retires a term without deleting it, the version number decided by evidence rather than opinion, and the one principle every source agrees on: once published, a term must always mean the same thing.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m11).

**Sources.** What this module is defined by, or argued from:

- [OWL 2 Structural Specification 3.1 Ontology IRI and Version IRI](https://www.w3.org/TR/owl2-syntax/#Ontology_IRI_and_Version_IRI)
- [OWL 2 Structural Specification 3.4 Imports](https://www.w3.org/TR/owl2-syntax/#Imports)
- [OWL 2 Primer 9 Ontology Management](https://www.w3.org/TR/owl2-primer/#Ontology_Management)
- [gist: deprecation and deletion policy](https://github.com/semanticarts/gist/blob/develop/docs/DeprecationAndDeletionPolicy.md)
- [OBO Foundry principle FP-004, versioning](https://obofoundry.org/principles/fp-004-versioning.html)
- [OBO Foundry principle FP-011, locus of authority](https://obofoundry.org/principles/fp-011-locus-of-authority.html)
- [OBO Foundry principle FP-013, notification of changes](https://obofoundry.org/principles/fp-013-notification.html)
- [OBO Foundry principle FP-016, maintenance](https://obofoundry.org/principles/fp-016-maintenance.html)
- [OBO Foundry principle FP-019, stability of term meaning](https://obofoundry.org/principles/fp-019-term-stability.html)
- [SemOps Manual 12.1 Evidence-based semver: version-diff](https://github.com/pwin/SemOpsManual/blob/main/docs/12-release-and-change.md#121-evidence-based-semver-version-diff)
- [SemOps Manual 12.3 The migration annotation, and its direction](https://github.com/pwin/SemOpsManual/blob/main/docs/12-release-and-change.md#123-the-migration-annotation-and-its-direction)
- [SemOps Manual 13.2 Documentation as a product](https://github.com/pwin/SemOpsManual/blob/main/docs/13-operate-and-consume.md#132-documentation-as-a-product-docgen)
- [Best Practice Recipes for Publishing RDF Vocabularies](https://www.w3.org/TR/swbp-vocab-pub/)

| Lesson | Decides | Corner |
|---|---|---|
| [o69 The header: what an ontology says about itself](o69-the-header-what-an-ontology-says-about-itself.ttl) | The ontology node carries a version IRI, a version number, its prior version, a title, a description, a creator, dates, a licence, its preferred prefix and namespace, and a named point of contact; the Quality Suite's metadata checks confirm nothing is missing. | symbol and thought |
| [o70 Deprecate; do not delete](o70-deprecate-do-not-delete.ttl) | A term whose meaning has moved is marked deprecated, kept for a full major version, given a change note and a replacement, and the migration is asserted from the retiring IRI so that tooling can find it. | symbol |
| [o71 The version number decided by evidence](o71-the-version-number-decided-by-evidence.ttl) | A release's version number is derived from what happened to the axioms, by diffing the old and new files, rather than from what the author believed the change was; a removed class makes it major whatever else was added. | thought |
| [o72 Publishing the IRIs, and keeping them alive](o72-publishing-the-iris-and-keeping-them-alive.ttl) | The vocabulary is published where its IRIs resolve, with a persistent redirector in front, documentation generated from the file, a channel for requests, and notice of changes; and where the Trail cannot do that, it says so. | symbol |
