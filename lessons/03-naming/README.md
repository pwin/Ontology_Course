# Module 03 · Naming

This is the symbol corner. An IRI identifies, a label names, and a definition says what is meant, and keeping the three of them apart is what lets a shop be renamed without becoming a different shop, and lets two organisations use the same word for different things without colliding. The module sets out the conventions the Trail follows beside the ones gist follows, and audits the one against the other.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m03).

**Sources.** What this module is defined by, or argued from:

- [gist Style Guide: orthographic conventions for local names](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#orthographic-conventions-for-class-and-property-local-names)
- [gist Style Guide: textual standards for property local names](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#textual-standards-for-property-local-names)
- [gist Style Guide: labels](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#labels)
- [gist Style Guide: definition of title case](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#gist-definition-of-title-case)
- [gist Style Guide: namespaces](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#namespaces)
- [gist: the namespace document](https://github.com/semanticarts/gist/blob/develop/docs/Namespace.md)
- [gist Style Guide: instance local names, and the most specific rigid class](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#instance-local-names)
- [OBO Foundry principle FP-003, URI/identifier space](https://obofoundry.org/principles/fp-003-uris.html)
- [OBO Foundry principle FP-012, naming conventions](https://obofoundry.org/principles/fp-012-naming-conventions.html)
- [Cool URIs for the Semantic Web 3 URIs for Real-World Objects](https://www.w3.org/TR/cooluris/#semweb)
- [Cool URIs for the Semantic Web 4.1 Hash URIs](https://www.w3.org/TR/cooluris/#hashuri)
- [Cool URIs for the Semantic Web 4.2 303 URIs](https://www.w3.org/TR/cooluris/#r303gendocument)
- [Cool URIs for the Semantic Web 4.4 Choosing between 303 and Hash](https://www.w3.org/TR/cooluris/#choosing)
- [Architecture of the World Wide Web 2.5 URI Opacity](https://www.w3.org/TR/webarch/#uri-opacity)
- [RDF Schema 3.5 rdfs:label](https://www.w3.org/TR/rdf12-schema/#ch_label)
- [BCP 47 Tags for Identifying Languages](https://www.rfc-editor.org/info/bcp47)
- [SKOS Reference 5 Lexical Labels](https://www.w3.org/TR/skos-reference/#labels)
- [SKOS Reference 5.3 integrity condition S14, one preferred label per language](https://www.w3.org/TR/skos-reference/#L1541)

| Lesson | Decides | Corner |
|---|---|---|
| [o15 An IRI is not a name](o15-an-iri-is-not-a-name.ttl) | The IRI identifies and the label names; a shop can be renamed without becoming a different shop, and an IRI may be readable or opaque as long as nothing depends on reading it. | symbol |
| [o16 Namespaces: one for the vocabulary, one for the data](o16-namespaces-one-for-the-vocabulary-one-for-the-data.ttl) | The schema lives in a hash namespace and the data in a slash namespace, the ontology IRI is not the namespace IRI, and both are declared on the ontology node. | symbol |
| [o17 Local names](o17-local-names.ttl) | Classes are UpperCamelCase, properties lowerCamelCase, letters and digits only, acronyms camel-cased, no home-made abbreviations; a draft that breaks each rule is corrected. | symbol |
| [o18 Naming a property so that it reads](o18-naming-a-property-so-that-it-reads.ttl) | Object properties are verb-initial and read as a sentence, datatype properties are nouns, direction is unambiguous and runs up the tree; the Trail's departures from that are listed rather than hidden. | symbol |
| [o19 Labels: one per language, in the right case](o19-labels-one-per-language-in-the-right-case.ttl) | Every term has exactly one skos:prefLabel per language, classes in title case and properties in lower case, alternatives in skos:altLabel; the rules are shapes, and they run in the editor. | symbol |
| [o20 Naming the particulars](o20-naming-the-particulars.ttl) | Instance IRIs carry a type infix and a slug, never a role, and are minted once; the Trail's shop-inkwell and gist's _Bookshop_The_Inkwell are the same rule in two spellings. | symbol |
