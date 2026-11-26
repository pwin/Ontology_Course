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

sys.path.insert(0, str(Path(__file__).resolve().parent))

from semops_graph import PREFIXES, RDFS, SKOS, Graph, is_iri, value  # noqa: E402

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

ANNOTATION_PROPS = {f"<{RDFS}{k}>" for k in ("label", "comment", "seeAlso", "isDefinedBy")} | {
    f"<{SKOS}{k}>" for k in ("prefLabel", "altLabel", "definition", "scopeNote", "example", "editorialNote", "note")}


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


def compute(g: Graph, namespace: str | None = None) -> dict:
    """Every OQuaRE metric this course reports, plus the counts behind them.
    `namespace` restricts the classes and properties counted to those whose
    IRI starts with it, so that borrowed terms do not inflate a score. The graph
    is read with SPARQL on HOLOS; the arithmetic is the paper's, in Python."""
    def own(x):
        return is_iri(x) and (namespace is None or value(x).startswith(namespace))

    def typed(*types: str) -> set[str]:
        return {x for x in g.column(PREFIXES + f"SELECT DISTINCT ?x WHERE {{ VALUES ?t {{ {' '.join(types)} }} ?x a ?t }}", "x")
                if own(x)}

    def pairs(where: str, a: str = "a", b: str = "b") -> list[tuple[str, str]]:
        return [(r[a], r[b]) for r in g.select(PREFIXES + f"SELECT ?{a} ?{b} WHERE {{ {where} }}") if r[a] and r[b]]

    classes = typed("owl:Class", "rdfs:Class")
    obj_props = typed("owl:ObjectProperty")
    data_props = typed("owl:DatatypeProperty")
    if not obj_props and not data_props:
        # An RDFS-only graph: every rdf:Property counts as a relationship
        obj_props = typed("rdf:Property")

    # Direct named superclasses, restricted to the counted classes.
    sup = defaultdict(set)
    for c, s in pairs("?a rdfs:subClassOf ?b"):
        if c in classes and s in classes and s != c:
            sup[c].add(s)
    children = defaultdict(set)
    for c, ss in sup.items():
        for s in ss:
            children[s].add(c)

    # Which classes a property belongs to: its rdfs:domain, or every class in
    # a union domain. A property with no domain belongs to no class.
    domains = defaultdict(set)
    for p, d in pairs("?a rdfs:domain ?b"):
        domains[p].add(d)
    union_members = defaultdict(set)
    for d, m in pairs("?a owl:unionOf/rdf:rest*/rdf:first ?b"):
        union_members[d].add(m)

    def domain_classes(p):
        out = set()
        for d in domains[p]:
            if d in classes:
                out.add(d)
            else:
                out |= {m for m in union_members[d] if m in classes}
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
    for s, c in pairs("?a a ?b"):
        if c in classes and is_iri(s):
            inst_of[c].add(s)

    # Annotations per class: one for every annotation triple about it.
    ann_of = defaultdict(int)
    for c, p in pairs("?a ?b ?o"):
        if c in classes and p in ANNOTATION_PROPS:
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
        "tangled": sorted(value(c) for c in classes if len(sup[c]) > 1),
    }


def table(result: dict) -> str:
    rows = ["| Metric | Value | Score |", "|---|---|---|"]
    for k, v in result["metrics"].items():
        val = f"{v * 100:.0f}%" if k in RELATIVE else f"{v:g}"
        rows.append(f"| {k} | {val} | {result['scores'][k]} |")
    return "\n".join(rows)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        g = Graph.from_file(arg)
        r = compute(g)
        print(f"== {arg}: {r['counts']}")
        print(table(r))
        if r["tangled"]:
            print("tangled:", ", ".join(r["tangled"][:10]))
