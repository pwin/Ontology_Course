# -*- coding: utf-8 -*-
"""FEATURES.md: every RDFS, SKOS and OWL 2 term the course demonstrates, and where.

    python scripts/features.py          # writes FEATURES.md, prints the gaps

The index is built by scanning the model of every lesson for prefixed terms,
so it cannot disagree with them. TERMS lists the vocabulary the course means
to cover, grouped as the specifications group it; a term in TERMS with no
lesson is printed as a gap, and a term in the models that TERMS does not know
is printed too, so the list stays complete in both directions.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import catalogue  # noqa: E402,F401
import specs  # noqa: E402
from ontocat import CATALOGUE, SITE  # noqa: E402

# group -> [(term, spec key or None)]
TERMS = [
    ("RDF and RDF Schema", [
        ("rdf:type", "rdfsType"), ("rdf:Property", "rdfsProperty"), ("rdfs:Class", "rdfsClass"),
        ("rdfs:subClassOf", "rdfsSubClassOf"), ("rdfs:subPropertyOf", "rdfsSubPropertyOf"),
        ("rdfs:domain", "rdfsDomain"), ("rdfs:range", "rdfsRange"), ("rdfs:label", "rdfsLabel"),
        ("rdfs:comment", "rdfsComment"), ("rdfs:seeAlso", "rdfsSeeAlso"), ("rdfs:isDefinedBy", "rdfsIsDefinedBy"),
        ("rdfs:Datatype", "syntaxDatatypeMap"),
    ]),
    ("SKOS", [
        ("skos:Concept", "skosConcepts"), ("skos:ConceptScheme", "skosSchemes"), ("skos:inScheme", "skosSchemes"),
        ("skos:hasTopConcept", "skosSchemes"), ("skos:prefLabel", "skosLabels"), ("skos:altLabel", "skosLabels"),
        ("skos:hiddenLabel", "skosLabels"), ("skos:notation", "skosLabels"),
        ("skos:definition", "skosNotes"), ("skos:scopeNote", "skosNotes"), ("skos:example", "skosNotes"),
        ("skos:editorialNote", "skosNotes"), ("skos:historyNote", "skosNotes"), ("skos:changeNote", "skosNotes"),
        ("skos:broader", "skosSemantic"), ("skos:narrower", "skosSemantic"), ("skos:related", "skosSemantic"),
        ("skos:Collection", "skosCollections"), ("skos:member", "skosCollections"),
        ("skos:closeMatch", "skosMapping"),
    ]),
    ("OWL 2: classes", [
        ("owl:Class", "primerClasses"), ("owl:Thing", "primerClasses"), ("owl:Nothing", "primerClasses"),
        ("owl:equivalentClass", "primerComplex"), ("owl:disjointWith", "primerDisjoint"),
        ("owl:AllDisjointClasses", "primerDisjoint"), ("owl:members", "primerDisjoint"),
        ("owl:intersectionOf", "primerComplex"), ("owl:unionOf", "primerComplex"), ("owl:complementOf", "primerComplex"),
        ("owl:oneOf", "primerEnumeration"),
        ("owl:Restriction", "primerRestrictions"), ("owl:onProperty", "primerRestrictions"),
        ("owl:someValuesFrom", "primerExistential"), ("owl:allValuesFrom", "primerUniversal"),
        ("owl:hasValue", "primerRestrictions"), ("owl:cardinality", "primerCardinality"),
        ("owl:minCardinality", "primerCardinality"), ("owl:maxCardinality", "primerCardinality"),
        ("owl:qualifiedCardinality", "primerCardinality"), ("owl:onClass", "primerCardinality"),
    ]),
    ("OWL 2: properties", [
        ("owl:ObjectProperty", "primerObjectProps"), ("owl:DatatypeProperty", "primerDatatypes"),
        ("owl:AnnotationProperty", "primerAnnotations"), ("owl:inverseOf", "primerInverse"),
        ("owl:propertyChainAxiom", "primerChains"), ("owl:hasKey", "primerKeys"),
        ("owl:FunctionalProperty", "primerCharacteristics"), ("owl:InverseFunctionalProperty", "primerCharacteristics"),
        ("owl:TransitiveProperty", "primerCharacteristics"), ("owl:SymmetricProperty", "primerCharacteristics"),
        ("owl:AsymmetricProperty", "primerCharacteristics"), ("owl:IrreflexiveProperty", "primerCharacteristics"),
    ]),
    ("OWL 2: individuals, datatypes, the ontology", [
        ("owl:NamedIndividual", "primerClasses"), ("owl:sameAs", "primerEquality"), ("owl:differentFrom", "primerEquality"),
        ("owl:AllDifferent", "primerEquality"), ("owl:onDatatype", "primerAdvancedDatatypes"),
        ("owl:withRestrictions", "primerAdvancedDatatypes"),
        ("owl:Ontology", "syntaxOntologyIri"), ("owl:versionIRI", "syntaxOntologyIri"), ("owl:versionInfo", "primerManagement"),
        ("owl:priorVersion", "primerManagement"), ("owl:imports", "syntaxImports"), ("owl:deprecated", "gistDeprecation"),
    ]),
    ("Metadata: Dublin Core and vann", [
        ("dct:title", "dctTerms"), ("dct:description", "dctTerms"), ("dct:creator", "dctTerms"),
        ("dct:contributor", "dctTerms"), ("dct:created", "dctTerms"), ("dct:modified", "dctTerms"),
        ("dct:license", "dctTerms"), ("dct:source", "dctTerms"), ("dct:isReplacedBy", "dctTerms"), ("dct:isPartOf", "dctTerms"),
        ("vann:preferredNamespacePrefix", "vocabPub"), ("vann:preferredNamespaceUri", "vocabPub"),
    ]),
    ("OntoClean marks (the course's own annotations)", [
        ("oc:rigidity", "ontocleanCacm"), ("oc:identity", "ontocleanCacm"), ("oc:unity", "ontocleanCacm"),
        ("oc:dependence", "ontocleanCacm"),
    ]),
    ("gUFO types", [
        ("gufo:Kind", "gufo"), ("gufo:SubKind", "gufo"), ("gufo:Role", "gufo"), ("gufo:Phase", "gufo"),
        ("gufo:EventType", "gufo"), ("gufo:AbstractIndividualType", "gufo"),
    ]),
    ("gist classes and patterns", [
        ("gist:Person", "gistReadme"), ("gist:Organization", "gistReadme"), ("gist:Content", "gistReadme"),
        ("gist:Event", "gistReadme"), ("gist:Category", "gistReadme"), ("gist:GovernedGeoRegion", "gistReadme"),
        ("gist:GeoRegion", "gistReadme"), ("gist:GeoRoute", "gistReadme"), ("gist:Building", "gistReadme"),
        ("gist:OrderedCollection", "gistReadme"), ("gist:Magnitude", "gistReadme"), ("gist:Aspect", "gistReadme"),
        ("gist:UnitOfMeasure", "gistReadme"), ("gist:isCategorizedBy", "gistReadme"), ("gist:hasMagnitude", "gistReadme"),
        ("gist:hasAspect", "gistReadme"), ("gist:hasUnitOfMeasure", "gistReadme"), ("gist:numericValue", "gistReadme"),
    ]),
    ("BFO classes (through gistBFO)", [
        ("obo:BFO_0000001", "bfo"), ("obo:BFO_0000002", "bfo"), ("obo:BFO_0000003", "bfo"),
        ("obo:BFO_0000027", "gistBfo"), ("obo:BFO_0000030", "gistBfo"), ("obo:BFO_0000031", "gistBfo"),
        ("obo:BFO_0000015", "gistBfo"), ("obo:BFO_0000040", "gistBfo"),
    ]),
    ("SHACL, in the companion shapes", [
        ("sh:NodeShape", "shaclSpec"), ("sh:targetClass", "shaclSpec"), ("sh:property", "shaclSpec"),
        ("sh:uniqueLang", "shaclSpec"), ("sh:pattern", "shaclSpec"), ("sh:disjoint", "shaclSpec"),
        ("sh:sparql", "shaclSpec"), ("sh:rule", "shaclSpec"), ("sh:SPARQLRule", "shaclSpec"),
        ("sh:SPARQLTarget", "shaclSpec"), ("sh:targetObjectsOf", "shaclSpec"), ("sh:severity", "shaclSpec"),
    ]),
]

_TERM = re.compile(r"(?<![A-Za-z0-9_])(?:rdf|rdfs|owl|skos|dct|vann|oc|gufo|gist|obo|sh):[A-Za-z][A-Za-z0-9_]*")
_STR = re.compile(r"\"\"\".*?\"\"\"|\"(?:[^\"\\]|\\.)*\"", re.S)
_COMMENT = re.compile("#[^" + chr(10) + "]*")
_IRI = re.compile(r"<[^>\s]*>")

# Terms that appear as vocabulary in passing rather than being taught.
IGNORE = {"rdf:first", "rdf:rest", "rdf:nil", "owl:backwardCompatibleWith", "owl:incompatibleWith",
          "sh:path", "sh:message", "sh:minCount", "sh:maxCount", "sh:select", "sh:construct", "sh:prefixes",
          "sh:declare", "sh:prefix", "sh:namespace", "sh:or", "sh:in", "sh:class", "sh:target", "sh:hasValue",
          "sh:Warning", "sh:Violation", "sh:Info", "sh:SPARQLConstraint", "sh:zeroOrOnePath",
          "sh:oneOrMorePath", "sh:PropertyShape", "sh:name"}


def terms_in(lesson) -> set:
    text = lesson.body
    for name, comp in lesson.companions.items():
        text += chr(10) + comp
    found = set(_TERM.findall(_COMMENT.sub(" ", _STR.sub(" ", _IRI.sub(" ", text)))))
    return {t for t in found if t not in IGNORE}


def main() -> None:
    where: dict[str, list] = {}
    for l in CATALOGUE:
        for t in terms_in(l):
            where.setdefault(t, []).append(l)
    known = {t for _, items in TERMS for t, _ in items}
    lines = ["# Features", "",
             "Every term the course demonstrates, and the lessons that demonstrate it. "
             "Generated by `python scripts/features.py` from the lesson models themselves, so it cannot "
             "disagree with them. Each term links to the section of the standard, style guide or paper that "
             "defines it, and each lesson to its file. The same index is in the "
             f"[course document]({SITE}#features).", ""]
    total = 0
    for group, items in TERMS:
        lines.append(f"## {group}")
        lines.append("")
        lines.append("| Term | Defined in | Lessons |")
        lines.append("|---|---|---|")
        for term, key in items:
            lessons = where.get(term, [])
            total += bool(lessons)
            label, url = specs.SECTIONS[key] if key else ("", "")
            spec = f"[{label}]({url})" if key else ""
            refs = ", ".join(f"[{l.oid}](lessons/{l.module}/{l.filename})" for l in lessons) or "*(no lesson yet)*"
            lines.append(f"| `{term}` | {spec} | {refs} |")
        lines.append("")
    extra = sorted(t for t in where if t not in known and not t.startswith(("bs:", "bt:")))
    if extra:
        lines.append("## Also used")
        lines.append("")
        lines.append("Terms the models use that the table above does not list.")
        lines.append("")
        for t in extra:
            refs = ", ".join(f"[{l.oid}](lessons/{l.module}/{l.filename})" for l in where[t])
            lines.append(f"- `{t}`: {refs}")
        lines.append("")
    (ROOT / "FEATURES.md").write_text(chr(10).join(lines), encoding="utf-8", newline=chr(10))
    gaps = [t for _, items in TERMS for t, _ in items if t not in where]
    print(f"FEATURES.md: {total} of {len(known)} terms demonstrated")
    if gaps:
        print("no lesson for: " + ", ".join(gaps))
    if extra:
        print("used but not catalogued: " + ", ".join(extra))


if __name__ == "__main__":
    main()
