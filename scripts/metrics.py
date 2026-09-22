# -*- coding: utf-8 -*-
"""The OQuaRE metrics, computed from an RDF graph.

Duque-Ramos, Fernandez-Breis, Stevens and Aussenac-Gilles, "OQuaRE: a
SQuaRE-based approach for evaluating the quality of ontologies", JRPIT 43(2),
2011. The formulas are the paper's, with its notation: C the classes, RC the
relationships (object properties) of a class, PC its properties (datatype
properties), IC its individuals, SupC its direct superclasses, and Thing the
root. Where the paper is silent on a detail -- which class a property "belongs
to" when its domain is a union, whether an equivalentClass counts as a
parent -- the choice made here is stated in a comment, because a metric is
only as reproducible as its small print.

    python scripts/metrics.py data/01-vocabulary.ttl lib/gist/gistCore.ttl
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import rdflib
from rdflib.namespace import OWL, RDF, RDFS, SKOS

# The paper's table 3: the value ranges that score 1 to 5. Absolute metrics
# score low when large; the relative ones score by twenty-percent bands.
THRESHOLDS = {
    "LCOMOnto": [(8, None), (6, 8), (4, 6), (2, 4), (None, 2)],
    "WMCOnto":  [(15, None), (11, 15), (8, 11), (5, 8), (None, 5)],
    "DITOnto":  [(8, None), (6, 8), (4, 6), (2, 4), (None, 2)],
    "NACOnto":  [(8, None), (6, 8), (4, 6), (2, 4), (None, 2)],
    "NOCOnto":  [(12, None), (8, 12), (6, 8), (3, 6), (None, 3)],
    "CBOOnto":  [(8, None), (6, 8), (4, 6), (2, 4), (None, 2)],
    "RFCOnto":  [(12, None), (8, 12), (6, 8), (3, 6), (None, 3)],
    "NOMOnto":  [(8, None), (6, 8), (4, 6), (2, 4), (None, 2)],
    "TMOnto":   [(8, None), (6, 8), (4, 6), (2, 4), (None, 2)],
}
RELATIVE = {"RROnto", "AROnto", "INROnto", "CROnto", "ANOnto"}

ANNOTATION_PROPS = {RDFS.label, RDFS.comment, SKOS.prefLabel, SKOS.altLabel, SKOS.definition,
                    SKOS.scopeNote, SKOS.example, SKOS.editorialNote, SKOS.note, RDFS.seeAlso,
                    RDFS.isDefinedBy}


def score(metric: str, value: float) -> int:
    """The paper's 1 to 5 score for a metric value."""
    if metric in RELATIVE:
        pct = value * 100
        return 5 if pct > 80 else 4 if pct > 60 else 3 if pct > 40 else 2 if pct > 20 else 1
    bands = THRESHOLDS[metric]
    for i, (lo, hi) in enumerate(bands):
        if lo is None and value <= hi:
            return i + 1
        if hi is None and value > lo:
            return i + 1
        if lo is not None and hi is not None and lo < value <= hi:
            return i + 1
    return 1


def compute(g: rdflib.Graph, namespace: str | None = None) -> dict:
    """Every OQuaRE metric this course reports, plus the counts behind them.
    `namespace` restricts the classes and properties counted to those whose
    IRI starts with it, so that borrowed terms do not inflate a score."""
    def own(x):
        return isinstance(x, rdflib.URIRef) and (namespace is None or str(x).startswith(namespace))

    classes = {c for c in g.subjects(RDF.type, OWL.Class) if own(c)}
    classes |= {c for c in g.subjects(RDF.type, RDFS.Class) if own(c)}
    obj_props = {p for p in g.subjects(RDF.type, OWL.ObjectProperty) if own(p)}
    data_props = {p for p in g.subjects(RDF.type, OWL.DatatypeProperty) if own(p)}
    if not obj_props and not data_props:
        # An RDFS-only graph: every rdf:Property counts as a relationship
        obj_props = {p for p in g.subjects(RDF.type, RDF.Property) if own(p)}

    # Direct named superclasses, restricted to the counted classes.
    sup = defaultdict(set)
    for c in classes:
        for s in g.objects(c, RDFS.subClassOf):
            if s in classes and s != c:
                sup[c].add(s)
    children = defaultdict(set)
    for c, ss in sup.items():
        for s in ss:
            children[s].add(c)

    # Which classes a property belongs to: its rdfs:domain, or every class in
    # a union domain. A property with no domain belongs to no class.
    def domain_classes(p):
        out = set()
        for d in g.objects(p, RDFS.domain):
            if d in classes:
                out.add(d)
            else:
                lst = g.value(d, OWL.unionOf)
                if lst is not None:
                    for m in rdflib.collection.Collection(g, lst):
                        if m in classes:
                            out.add(m)
        return out

    rel_of = defaultdict(set)   # RC: object properties per class
    prop_of = defaultdict(set)  # PC: datatype properties per class
    for p in obj_props:
        for c in domain_classes(p):
            rel_of[c].add(p)
    for p in data_props:
        for c in domain_classes(p):
            prop_of[c].add(p)

    # Individuals per class, counting only the counted classes' direct types.
    inst_of = defaultdict(set)
    for s, c in g.subject_objects(RDF.type):
        if c in classes and isinstance(s, rdflib.URIRef):
            inst_of[c].add(s)

    ann_of = defaultdict(int)
    for c in classes:
        for p in g.predicates(c, None):
            if p in ANNOTATION_PROPS:
                ann_of[c] += 1

    n = len(classes) or 1
    roots = [c for c in classes if not sup[c]]
    leaves = [c for c in classes if not children[c]]

    def depth(c, seen=()):
        if not sup[c] or c in seen:
            return 1
        return 1 + max(depth(s, seen + (c,)) for s in sup[c])

    def ancestors(c, seen=None):
        seen = seen or set()
        for s in sup[c]:
            if s not in seen:
                seen.add(s)
                ancestors(s, seen)
        return seen

    depths = {c: depth(c) for c in classes}
    m = {}
    # LCOMOnto: mean path length from each leaf to the root
    m["LCOMOnto"] = (sum(depths[c] for c in leaves) / len(leaves)) if leaves else 0.0
    # WMCOnto: mean number of properties and relationships per class
    m["WMCOnto"] = (sum(len(prop_of[c]) for c in classes) + sum(len(rel_of[c]) for c in classes)) / n
    # DITOnto: the longest path from Thing to a leaf
    m["DITOnto"] = max(depths.values()) if depths else 0
    # NACOnto: mean number of ancestors per leaf class
    m["NACOnto"] = (sum(len(ancestors(c)) for c in leaves) / len(leaves)) if leaves else 0.0
    # NOCOnto: mean number of direct subclasses, over classes that are not roots
    non_root = n - len(roots) or 1
    m["NOCOnto"] = sum(len(children[c]) for c in classes) / non_root
    # CBOOnto: mean number of direct superclasses, over classes that are not roots
    m["CBOOnto"] = sum(len(sup[c]) for c in classes) / non_root
    # RFCOnto: properties plus superclasses, over classes that are not roots
    m["RFCOnto"] = (sum(len(prop_of[c]) for c in classes) + sum(len(sup[c]) for c in classes)) / non_root
    # NOMOnto: datatype properties per class
    m["NOMOnto"] = sum(len(prop_of[c]) for c in classes) / n
    # RROnto: properties over relationships plus classes
    denom = sum(len(rel_of[c]) for c in classes) + n
    m["RROnto"] = sum(len(prop_of[c]) for c in classes) / denom if denom else 0.0
    # AROnto: attributes (datatype properties) per class, read as a ratio
    m["AROnto"] = sum(len(prop_of[c]) for c in classes) / n
    # INROnto: relationships per class
    m["INROnto"] = sum(len(rel_of[c]) for c in classes) / n
    # CROnto: individuals per class
    m["CROnto"] = sum(len(inst_of[c]) for c in classes) / n
    # ANOnto: annotations per class
    m["ANOnto"] = sum(ann_of[c] for c in classes) / n
    # TMOnto: parents per class, over classes with a parent (the paper's
    # denominator subtracts the classes with no parent)
    with_parent = [c for c in classes if sup[c]]
    m["TMOnto"] = (sum(len(sup[c]) for c in with_parent) / len(with_parent)) if with_parent else 0.0

    scores = {k: score(k, v) for k, v in m.items()}
    return {
        "counts": {"classes": n if classes else 0, "object_properties": len(obj_props),
                   "datatype_properties": len(data_props), "roots": len(roots), "leaves": len(leaves),
                   "individuals": sum(len(v) for v in inst_of.values())},
        "metrics": {k: round(v, 3) for k, v in m.items()},
        "scores": scores,
        "tangled": sorted(str(c) for c in classes if len(sup[c]) > 1),
    }


def table(result: dict) -> str:
    rows = ["| Metric | Value | Score |", "|---|---|---|"]
    for k, v in result["metrics"].items():
        val = f"{v * 100:.0f}%" if k in RELATIVE else f"{v:g}"
        rows.append(f"| {k} | {val} | {result['scores'][k]} |")
    return "\n".join(rows)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        g = rdflib.Graph().parse(arg)
        r = compute(g)
        print(f"== {arg}: {r['counts']}")
        print(table(r))
        if r["tangled"]:
            print("tangled:", ", ".join(r["tangled"][:10]))
