# Module 09 · Standing on gist

An upper ontology is a vocabulary in common, so this module hooks the Trail's classes onto gist, decides which of gist's patterns are worth adopting, and reads two published alignments, gistBFO and gistUFO, as worked examples of how a class comes to be placed under a foundational one and why. Two of the placements disagree with one another, which is instructive in itself.

Each `.ttl` file carries its own explanation: what it decides, why, a diagram of the idea, and what to take away. Read the header, then follow the Open in the editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL panel can query it. Where a lesson has been reasoned over or measured, the MEASURED line says what the tools found.

The same lessons, with their measurements laid out in full, are in the [course document](https://www.semantechs.co.uk/Ontology_Course/#m09).

**Sources.** What this module is defined by, or argued from:

- [gist: a minimalist upper ontology](https://github.com/semanticarts/gist)
- [Winstanley, Is an upper ontology useful? ISKO UK 2023, CEUR-WS Vol. 3661](https://ceur-ws.org/Vol-3661/10-SHORT-PWinstanley-ISKOUK2023.pdf)
- [gistBFO: gist mapped to the Basic Formal Ontology](https://github.com/semanticarts/gistBFO)
- [BFO 2020](https://github.com/BFO-ontology/BFO-2020)
- [gistUFO: gist aligned with gUFO](https://github.com/semanticarts/gistUFO)
- [gUFO: a lightweight implementation of the Unified Foundational Ontology](https://nemo-ufes.github.io/gufo/)
- [OBO Foundry principle FP-007, relations: reuse existing ones](https://obofoundry.org/principles/fp-007-relations.html)

| Lesson | Decides | Corner |
|---|---|---|
| [o58 What an upper ontology is for](o58-what-an-upper-ontology-is-for.ttl) | The Trail stands on gist rather than defining person, organisation, event and place again, because an upper ontology is a vocabulary in common, and gist is the smallest one that covers a business. | thought |
| [o59 Hooking the Trail onto gist](o59-hooking-the-trail-onto-gist.ttl) | Each Trail kind is placed under its most specific gist class with a note saying why, two are left unplaced because nothing fits, and the whole is reasoned over with gist imported to see what gist's own axioms make of it. | referent |
| [o60 gist's patterns, and when to keep your own](o60-gist-s-patterns-and-when-to-keep-your-own.ttl) | Floor area is modelled gist's way, as a Magnitude with an Aspect and a Unit, beside the Trail's way, a datatype property with the unit in its name; the Trail keeps the simple form and records what it gives up. | referent |
| [o61 gistBFO: the same classes under a foundational ontology](o61-gistbfo-the-same-classes-under-a-foundational-ontology.ttl) | The Trail reaches BFO through gist's published bridge, reads each mapping note as a worked example of alignment reasoning, and reasons over the three ontologies together. | referent |
| [o62 Two alignments, one ontology: gistUFO beside gistBFO](o62-two-alignments-one-ontology-gistufo-beside-gistbfo.ttl) | The Trail's classes are typed the gUFO way, as gistUFO types gist's, and set beside their BFO placements; where the two published alignments disagree about gist:Event, the disagreement is kept as instruction. | referent |
