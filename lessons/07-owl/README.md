# Module 07 · The ladder: OWL 2

The top rungs. OWL 2 lets an ontology say enough that a reasoner can contradict it, which is the first time the model can be wrong rather than incomplete. Each lesson takes one construct, states what it commits you to, and shows what the reasoner does with it. The surprises are the point: a maximum cardinality that merges two towns instead of flagging an error, a universal restriction that infers nothing, a transitive property that cannot also be functional.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m07).

**Sources.** What this module is defined by, or argued from:

- [OWL 2 Primer 4.1 Classes, Properties and Individuals](https://www.w3.org/TR/owl2-primer/#Classes.2C_Properties.2C_and_Individuals_.E2.80.93_And_Basic_Modeling_With_Them)
- [OWL 2 Primer 4.3 Class Disjointness](https://www.w3.org/TR/owl2-primer/#Class_Disjointness)
- [OWL 2 Primer 5.2 Property Restrictions](https://www.w3.org/TR/owl2-primer/#Property_Restrictions)
- [OWL 2 Primer 5.2 Property Restrictions: existential quantification](https://www.w3.org/TR/owl2-primer/#Property_Restrictions)
- [OWL 2 Primer 5.2 Property Restrictions: universal quantification](https://www.w3.org/TR/owl2-primer/#Property_Restrictions)
- [OWL 2 Primer 5.2.3 Property Cardinality Restrictions](https://www.w3.org/TR/owl2-primer/#Property_Cardinality_Restrictions)
- [OWL 2 Primer 5.1 Complex Classes](https://www.w3.org/TR/owl2-primer/#Complex_Classes)
- [OWL 2 Primer 5.3 Enumeration of Individuals](https://www.w3.org/TR/owl2-primer/#Enumeration_of_Individuals)
- [OWL 2 Primer 6 Advanced Use of Properties](https://www.w3.org/TR/owl2-primer/#Advanced_Use_of_Properties)
- [OWL 2 Primer 6 Advanced Use of Properties: inverse properties](https://www.w3.org/TR/owl2-primer/#Advanced_Use_of_Properties)
- [OWL 2 Primer 6.4 Property Chains](https://www.w3.org/TR/owl2-primer/#Property_Chains)
- [OWL 2 Primer 6.5 Keys](https://www.w3.org/TR/owl2-primer/#Keys)
- [OWL 2 Primer 4.6 Domain and Range Restrictions](https://www.w3.org/TR/owl2-primer/#Domain_and_Range_Restrictions)
- [OWL 2 Primer 4.7 Equality and Inequality of Individuals](https://www.w3.org/TR/owl2-primer/#Equality_and_Inequality_of_Individuals)
- [OWL 2 Primer 4.8 Datatypes](https://www.w3.org/TR/owl2-primer/#Datatypes)
- [OWL 2 Primer 8.1 Punning](https://www.w3.org/TR/owl2-primer/#a_Punning)
- [OWL 2 Primer 8.2 Document Information and Annotations](https://www.w3.org/TR/owl2-primer/#Document_Information_and_Annotations)
- [OWL 2 Primer 10.1 OWL 2 DL and OWL 2 Full](https://www.w3.org/TR/owl2-primer/#OWL_2_DL_and_OWL_2_Full)
- [OWL 2 Primer 10.2 OWL 2 Profiles](https://www.w3.org/TR/owl2-primer/#OWL_2_Profiles)
- [OWL 2 Primer 2.2 Modeling Knowledge: Basic Notions (the open world, no unique names)](https://www.w3.org/TR/owl2-primer/#Modeling_Knowledge:_Basic_Notions)
- [OWL 2 Structural Specification 11 Global Restrictions on Axioms in OWL 2 DL](https://www.w3.org/TR/owl2-syntax/#Global_Restrictions_on_Axioms_in_OWL_2_DL)
- [OWL 2 Structural Specification 4 Datatype Maps](https://www.w3.org/TR/owl2-syntax/#Datatype_Maps)
- [OWL 2 Structural Specification 5.8.1 Typing Constraints of OWL 2 DL](https://www.w3.org/TR/owl2-syntax/#Typing_Constraints_of_OWL_2_DL)
- [OWL 2 Structural Specification 5.8 Entity Declarations and Typing](https://www.w3.org/TR/owl2-syntax/#Entity_Declarations_and_Typing)
- [OWL 2 Profiles 2 OWL 2 EL](https://www.w3.org/TR/owl2-profiles/#OWL_2_EL)
- [OWL 2 Profiles 3 OWL 2 QL](https://www.w3.org/TR/owl2-profiles/#OWL_2_QL)
- [OWL 2 Profiles 4 OWL 2 RL](https://www.w3.org/TR/owl2-profiles/#OWL_2_RL)
- [gist Style Guide: OWL restrictions, the eleven rules](https://github.com/semanticarts/gist/blob/develop/docs/gistStyleGuide.md#owl-restrictions)
- [SHACL: constraints on data, which OWL axioms are not](https://www.w3.org/TR/shacl/)

| Lesson | Decides | Corner |
|---|---|---|
| [o42 owl:Class, owl:Ontology, and the rule that everything is declared](o42-owl-class-owl-ontology-and-the-rule-that-everything-is-declared.ttl) | The vocabulary becomes an OWL 2 DL ontology: an owl:Ontology node, every class an owl:Class, every property exactly one of object, datatype or annotation, every borrowed term declared, and the profile checker as referee. | referent |
| [o43 Disjointness: now you can be wrong](o43-disjointness-now-you-can-be-wrong.ttl) | The top-level kinds are declared pairwise disjoint, so that one thing typed as two of them is a contradiction a reasoner reports, and a query finds in the browser. | referent |
| [o44 Existential restrictions: a necessary condition, and the open world](o44-existential-restrictions-a-necessary-condition-and-the-open-world.ttl) | 'Every bookshop is located in some settlement' is written as a subclass axiom with owl:someValuesFrom, which constrains the set without producing a triple, and a shop with no recorded town is not an error. | referent |
| [o45 Universal restrictions: types the values, and is true of nothing](o45-universal-restrictions-types-the-values-and-is-true-of-nothing.ttl) | 'A bookshop stocks only works' is written with owl:allValuesFrom, which types every value of bs:stocks on a bookshop as a Work and is trivially satisfied by a shop that stocks nothing. | referent |
| [o46 Defined classes: the reasoner decides membership](o46-defined-classes-the-reasoner-decides-membership.ttl) | Author is defined rather than declared: equivalent to a Person who wrote some Work, so that the reasoner types every such person an Author without being told, and the role from module 02 has its formal definition. | referent |
| [o47 Cardinality: the reasoner merges before it complains](o47-cardinality-the-reasoner-merges-before-it-complains.ttl) | Cardinality restrictions are written for meaning and never for validation, because two values under a maximum of one make the reasoner conclude they are the same thing, not that the data is wrong. | referent |
| [o48 Property characteristics, and the property that cannot be two things](o48-property-characteristics-and-the-property-that-cannot-be-two-things.ttl) | bs:within is transitive, bs:connectsTo symmetric, bs:imprintOf asymmetric and irreflexive; and because a transitive property is non-simple, bs:within may not also be functional, which the profile checker enforces. | referent |
| [o49 Inverses, chains and keys](o49-inverses-chains-and-keys.ttl) | bs:wrote is declared the inverse of bs:author so that one assertion yields both directions; a property chain gives an event its town; and a key on ISBN says what identifies a work, without leaving OWL 2 DL. | referent |
| [o50 Datatypes and profiles: where the language draws its lines](o50-datatypes-and-profiles-where-the-language-draws-its-lines.ttl) | Values are typed only with datatypes in the OWL 2 map, which excludes xsd:gYear and xsd:date; the year properties are left without a range for that reason; and the profile a consumer needs is checked, not assumed. | referent |
