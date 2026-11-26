# -*- coding: utf-8 -*-
"""Parse, reason over and measure every lesson, and compare with what it says.

    python scripts/check_lessons.py              # every lesson
    python scripts/check_lessons.py o07 o08      # just these
    python scripts/check_lessons.py --module 07-owl
    python scripts/check_lessons.py --show o44   # print the inferred triples and rows

Each lesson's model is written to build/models/, loaded into HOLOS, and then
put through whatever its `check` asks for: the OWL 2 profile checker and
HermiT (through ROBOT), an OWL 2 RL closure (owlrl, the same profile the
editor's reasoner implements), the quality checks (`semops check`), the
SHACL engine, the OQuaRE metrics, a naming audit, a definition audit, and its
own SPARQL queries. What comes back is compared with the lesson's `expect`,
and the run fails on any expectation that does not hold.

HOLOS, the SHACL engine and the checks are SemOps System's, from
`pip install semops-system`: the engine the Turtle Editor Viewer runs in the
browser, so a query's rows here are the rows a reader sees there. owlrl is the
one exception, because SemOps has no OWL 2 RL reasoner yet; it works on rdflib
graphs, so rdflib is used for that and nothing else.

Two files come out of it:

    build/results/<oid>.json     everything measured, for the course document
    build/measured.json          the one-line MEASURED summary per lesson,
                                 which build_lessons.py writes into each header
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import catalogue  # noqa: E402,F401
import metrics  # noqa: E402
import robot  # noqa: E402
from ontocat import CATALOGUE, DATA, LIB, PREFIX_URI  # noqa: E402
from semops_graph import (OWL, PREFIXES, RDF, RDFS, Graph, escape_literal, is_blank, is_iri,  # noqa: E402
                          is_literal, lexical, query_form, value)

BUILD = ROOT / "build"
MODELS = BUILD / "models"
RESULTS = BUILD / "results"

_BY_LENGTH = sorted(PREFIX_URI.items(), key=lambda x: -len(x[1]))


def pname(term: str | None) -> str:
    """A prefixed name for an N-Triples term, or the IRI in angle brackets. A
    literal shows its text in quotes and a blank node the start of its label."""
    if not term:
        return ""
    if is_literal(term):
        return f'"{lexical(term)}"'
    if is_blank(term):
        return "_:" + term[2:8]
    s = value(term)
    for p, u in _BY_LENGTH:
        if s.startswith(u):
            return f"{p}:{s[len(u):]}"
    return f"<{s}>"


_DIR_TAG = re.compile(r'@([A-Za-z][A-Za-z0-9-]*?)--(?:rtl|ltr)\b')


def load_data(name: str, into: Graph) -> None:
    """Load a data file into a graph. The Trail's data carries RDF 1.2
    directional language tags (@ar--rtl). HOLOS reads them, but the full graph
    goes on to ROBOT, whose OWL API does not, so the direction is dropped, as
    the SHACL course does before a tool that cannot read them."""
    text = (DATA / name).read_text(encoding="utf-8")
    into.load_text(_DIR_TAG.sub(r"@\1", text), "turtle")


# ---------------------------------------------------------------- audits

CLASS_NAME = re.compile(r"^[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*$")
PROP_NAME = re.compile(r"^[a-z][a-z0-9]+(?:[A-Z][a-z0-9]+)*$")
BS = "https://example.org/bookshop-trail/schema#"


def _iris_typed(g: Graph, *types: str) -> set[str]:
    """The IRIs with any of these rdf:types."""
    values = " ".join(types)
    return g.column(PREFIXES + f"SELECT DISTINCT ?x WHERE {{ VALUES ?t {{ {values} }} ?x a ?t FILTER isIRI(?x) }}", "x")


def audit_names(g: Graph) -> list[str]:
    """Local names in the schema namespace that break the conventions of
    module 03: UpperCamelCase classes, lowerCamelCase properties, letters and
    digits only, acronyms camel-cased."""
    bad = []
    for c in sorted(_iris_typed(g, "owl:Class", "rdfs:Class")):
        if value(c).startswith(BS):
            local = value(c)[len(BS):]
            if not CLASS_NAME.match(local):
                bad.append("bs:" + local)
    for kind in ("owl:ObjectProperty", "owl:DatatypeProperty", "owl:AnnotationProperty", "rdf:Property"):
        for p in sorted(_iris_typed(g, kind)):
            if value(p).startswith(BS):
                local = value(p)[len(BS):]
                if not PROP_NAME.match(local) and "bs:" + local not in bad:
                    bad.append("bs:" + local)
    return sorted(bad)


def audit_definitions(g: Graph) -> list[str]:
    """Terms whose definition repeats the term's own name: a rough test for
    circularity, and rough on purpose -- it also catches 'a publisher is an
    organisation that publishes', which is the case worth catching."""
    texts: dict[str, list[str]] = {}
    for row in g.select(PREFIXES + "SELECT ?term ?text WHERE { VALUES ?p { skos:definition rdfs:comment } "
                                   "?term ?p ?text FILTER isIRI(?term) }"):
        texts.setdefault(row["term"], []).append(value(row["text"]))
    circular = []
    for term, said in texts.items():
        local = value(term).split("#")[-1].split("/")[-1]
        words = re.findall(r"[A-Z]?[a-z]+", local)
        if not words:
            continue
        stems = {w.lower()[:max(4, len(w) - 2)] for w in words if len(w) > 3}
        for text in said:
            first = text.split(".")[0].lower()
            if any(re.search(r"\b" + re.escape(st), first) for st in stems):
                circular.append(pname(term))
                break
    return sorted(set(circular))


def _nt(t) -> str:
    """An rdflib term as N-Triples, the form the rest of the checker uses."""
    import rdflib
    if isinstance(t, rdflib.URIRef):
        return f"<{t}>"
    if isinstance(t, rdflib.BNode):
        return f"_:{t}"
    if isinstance(t, rdflib.Literal):
        text = f'"{escape_literal(str(t))}"'
        if t.language:
            return f"{text}@{t.language}"
        if t.datatype and str(t.datatype) != "http://www.w3.org/2001/XMLSchema#string":
            return f"{text}^^<{t.datatype}>"
        return text
    return str(t)


def rl_closure(g: Graph) -> tuple[Graph, list[tuple[str, str, str]]]:
    """The OWL 2 RL closure, and the triples it added about the Trail's own
    terms. owlrl also adds its axiomatic triples (every XSD datatype, owl:Nothing
    under every class); those are left out of the list and the count.

    The one place rdflib is used: SemOps has no OWL 2 RL reasoner yet, and owlrl
    works on rdflib graphs. The graph goes in as N-Triples and the closure comes
    back the same way. owlrl's closure is generalised RDF, where a literal can be a
    subject; those triples cannot be written as RDF, and are dropped on the way back,
    as nothing measured here sits on one."""
    import owlrl
    import rdflib
    from rdflib.namespace import OWL as O, RDFS as RS
    before = rdflib.Graph().parse(data=g.serialize("ntriples"), format="nt")
    closed = rdflib.Graph()
    for t in before:
        closed.add(t)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(closed)
    w3c = (RDF, RDFS, OWL, "http://www.w3.org/2001/XMLSchema#")
    new = []
    for s, p, o in closed:
        if (s, p, o) in before:
            continue
        if any(isinstance(x, rdflib.BNode) for x in (s, p, o)) or isinstance(s, rdflib.Literal):
            continue
        if str(s).startswith(w3c) or o in (O.Thing, RS.Resource, O.NamedIndividual, O.Nothing) or s == o:
            continue
        if str(p).startswith(RDFS) and p not in (RS.subClassOf, RS.subPropertyOf, RS.domain, RS.range):
            continue
        new.append((s, p, o))
    # A graph iterates in hash order, which changes with every run, and the
    # course document shows the first few; sorted, it shows the same ones.
    new.sort(key=lambda t: tuple(map(str, t)))
    lines = [f"{_nt(s)} {_nt(p)} {_nt(o)} ." for s, p, o in closed
             if not isinstance(s, rdflib.Literal) and isinstance(p, rdflib.URIRef)]
    return Graph.from_text("\n".join(lines) + "\n", "ntriples"), [tuple(_nt(x) for x in t) for t in new]


# Where the checks report a finding about the graph as a whole, such as QUA-005's
# missing owl:Ontology: a node of the registry's own, outside any namespace.
GRAPH_NODE = "https://semantechs.co.uk/ontology-quality/Graph"


def run_checks(path: Path, stage: str, hermit: dict | None, own: str) -> dict:
    """The quality checks, as `semops check --engine sparql` runs them, and the
    check ids they report, measured as the Ontology Quality Suite measured them.

    Stage "checks" is scoped to the lesson's own namespace, as the suite's
    --own-namespace scoped it: the findings about terms in that namespace, and the
    findings about the graph as a whole. `semops check` has no such option, so the
    scope is applied here, to its findings. Stage "ontology" was the suite's other
    command, which ran the logical and reasoning checks over everything; it keeps
    those two categories, unscoped.

    REA-020 and REA-021 need an external DL reasoner, which `semops check` does not
    run: it runs the checks that have a SHACL shape or a SPARQL query. For stage
    "ontology" they come from the HermiT run the lesson already makes through ROBOT
    -- the reasoner the suite took them from, through owlready2."""
    import semops_system as so
    run = so.check(str(path), engine="sparql")
    if stage == "ontology":
        def keep(f: dict) -> bool:
            return f.get("category") in ("logical", "reasoning")
    else:
        def keep(f: dict) -> bool:
            focus = (f.get("focus_node") or "").strip("<>")
            return focus.startswith(own) or focus == GRAPH_NODE
    found: dict[str, int] = {}
    messages: dict[str, str] = {}
    for f in filter(keep, run["findings"]):
        cid = f["check_id"]
        found[cid] = found.get(cid, 0) + 1
        # The smallest that says something: the findings' order is not a contract.
        m = (f.get("message") or "")[:200]
        if cid not in messages or (m and (not messages[cid] or m < messages[cid])):
            messages[cid] = m
    if stage == "ontology" and hermit and "skipped" not in hermit:
        # Worded as the suite worded them, naming the reasoner that said so.
        if not hermit.get("consistent", True):
            found["REA-020"] = 1
            messages["REA-020"] = "The ontology is inconsistent according to HermiT, through ROBOT."
        elif hermit.get("unsatisfiable"):
            found["REA-021"] = len(hermit["unsatisfiable"])
            messages["REA-021"] = min(f"{u.strip('<>')} is unsatisfiable (equivalent to owl:Nothing) according to "
                                      "HermiT, through ROBOT." for u in hermit["unsatisfiable"])
    return {"ids": dict(sorted(found.items())), "messages": messages, "complete": run["complete"],
            "failed": sorted(f.get("check_id", "") for f in run["failed"])}


def run_version_diff(l, old_name: str, new_name: str) -> dict:
    """Two companion files through `semops diff`, which reports as the Ontology
    Quality Suite's version-diff did: the suggested bump and the change lines.
    Imports are not followed: each file is compared as it stands."""
    folder = MODELS / l.oid
    folder.mkdir(parents=True, exist_ok=True)
    old = folder / old_name
    new = folder / new_name
    old.write_text(l.companions[old_name].strip() + "\n", encoding="utf-8", newline="\n")
    new.write_text(l.companions[new_name].strip() + "\n", encoding="utf-8", newline="\n")
    p = subprocess.run([sys.executable, "-m", "semops_system", "diff", str(old), str(new)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    out = (p.stdout or "") + (p.stderr or "")
    bump = ""
    lines = []
    for line in out.splitlines():
        if "Suggested version bump" in line:
            bump = line.split(":", 1)[1].strip()
        elif line.strip().startswith("- ") or line.rstrip().endswith("]:"):
            lines.append(line.strip())
    return {"bump": bump, "lines": lines[:20], "rc": p.returncode}


def _shacl_term(text: str | None) -> str:
    """An N-Triples term from the engine, as a prefixed name where one fits."""
    if not text:
        return ""
    if text.startswith("<") and text.endswith(">"):
        return pname(text)
    return text


def explanation_sizes(md: str) -> list[int]:
    """The number of axioms in each set of ROBOT's explanation Markdown,
    smallest first, so that the line does not depend on the order found."""
    sizes: list[int] = []
    for line in md.split("# Axiom Impact")[0].splitlines():
        if line.startswith("## "):
            sizes.append(0)
        elif line.startswith("  - ") and sizes:
            sizes[-1] += 1
    return sorted(sizes)


def run_shacl(data_text: str, shapes_text: str, inference: str = "none") -> dict:
    """Validate with the engine the Turtle Editor Viewer runs: SemOps System's
    SHACL engine, whose WebAssembly build is in the editor and whose Python
    bindings are `semops-system`'s `shacl` module. Same engine, same answers as
    the browser."""
    from semops_system import shacl as engine
    shapes = engine.Shapes.from_text(shapes_text)
    report = shapes.validate_text(data_text, inference=inference)
    counts = {"Violation": 0, "Warning": 0, "Info": 0}
    rows = []
    for r in report.results:
        counts[r.severity] = counts.get(r.severity, 0) + 1
        rows.append({"severity": r.severity, "focus": _shacl_term(r.focus_node),
                     "path": _shacl_term(r.path), "value": _shacl_term(r.value),
                     "shape": _shacl_term(r.root_shape), "component": r.component,
                     "message": (r.message or "")[:160]})
    # The engine reports in the order it meets the data, which follows how the graph
    # was written out; sorted, the rows the document shows are the same every run.
    rows.sort(key=lambda x: (x["focus"], x["path"], x["component"], x["value"], x["message"]))
    return {"conforms": bool(report.conforms), "counts": counts, "rows": rows,
            "shapes": len(shapes), "inference": inference}


def run_rules(data_text: str, shapes_text: str) -> dict:
    """A validator's only output is its report, so a rule's effect is measured
    the way the SHACL course measures it and the way the editor's Inference
    dropdown shows it: a shape at Info severity reports one result per derived
    triple, and the count is taken at each inference mode."""
    from semops_system import shacl as engine
    shapes = engine.Shapes.from_text(shapes_text)
    out = {}
    for mode in ("none", "rules", "rules-iterated"):
        report = shapes.validate_text(data_text, inference=mode)
        out[mode] = sum(1 for r in report.results if r.severity == "Info")
    return out


# ---------------------------------------------------------------- one lesson

def measure_local(l) -> tuple[dict, Graph | None, Path]:
    """Everything that runs in-process: parse, count, audit, closure, shapes,
    queries. Runs on the main thread, one lesson at a time."""
    r: dict = {"oid": l.oid, "ok": True}
    chk = l.check
    path = MODELS / f"{l.oid}.ttl"
    path.write_text(l.model_text, encoding="utf-8", newline="\n")
    try:
        g = Graph.from_file(path, "turtle")
    except Exception as e:  # noqa: BLE001
        r["ok"] = False
        r["error"] = f"does not parse: {str(e)[:300]}"
        return r, None, path
    r["triples"] = len(g)
    r["classes"] = len(_iris_typed(g, "owl:Class", "rdfs:Class"))

    def typed(t: str) -> int:
        # Blank nodes count here, as they always have: an anonymous property is still one.
        return g.count(PREFIXES + f"SELECT (COUNT(DISTINCT ?x) AS ?n) WHERE {{ ?x a {t} }}")
    r["object_properties"] = typed("owl:ObjectProperty")
    r["datatype_properties"] = typed("owl:DatatypeProperty")
    r["annotation_properties"] = typed("owl:AnnotationProperty")
    r["rdf_properties"] = typed("rdf:Property")
    r["concepts"] = typed("skos:Concept")
    meta = ("owl:Class rdfs:Class owl:ObjectProperty owl:DatatypeProperty owl:AnnotationProperty rdf:Property "
            "owl:Ontology owl:NamedIndividual rdfs:Datatype owl:Restriction owl:AllDisjointClasses "
            "owl:TransitiveProperty owl:SymmetricProperty owl:FunctionalProperty owl:InverseFunctionalProperty "
            "owl:AsymmetricProperty owl:IrreflexiveProperty owl:ReflexiveProperty skos:ConceptScheme")
    # An individual: an IRI typed with something that is neither one of the
    # metamodel's types nor anything else in the OWL namespace, and that is not
    # itself a class. A blank-node type (a restriction used as a type) counts.
    r["individuals"] = g.count(PREFIXES + f"""
        SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE {{
          ?s a ?t
          FILTER(isIRI(?s))
          FILTER(?t NOT IN ({", ".join(meta.split())}))
          FILTER(isBlank(?t) || !STRSTARTS(STR(?t), STR(owl:)))
          FILTER NOT EXISTS {{ ?s a owl:Class }}
          FILTER NOT EXISTS {{ ?s a rdfs:Class }}
        }}""")

    full = g
    full_path = path
    if chk.get("with_data") or chk.get("imports"):
        full = Graph.from_file(path, "turtle")
        names = chk.get("with_data") or []
        for name in ([names] if isinstance(names, str) else names):
            load_data(name, full)
        for name in chk.get("imports") or []:
            imported = Graph.from_file(LIB / name, "turtle")
            # One ontology header only: the OWL API refuses a document with
            # several, so the imported ontologies' own headers are dropped.
            imported.update(PREFIXES + "DELETE { ?h ?p ?o } WHERE { ?h a owl:Ontology ; ?p ?o }")
            imported.update(PREFIXES + "DELETE WHERE { ?s owl:imports ?o }")
            full.load_text(imported.serialize("ntriples"), "ntriples")
        full_path = MODELS / f"{l.oid}.full.ttl"
        full.dump(full_path, "turtle")
        r["full_triples"] = len(full)

    if chk.get("names"):
        r["names_bad"] = audit_names(g)
    if chk.get("definitions"):
        r["circular"] = audit_definitions(g)
    if chk.get("rl"):
        closed, new = rl_closure(full)
        same_as = f"<{OWL}sameAs>"
        r["rl"] = {"added": len(new),
                   "named": [" ".join(pname(x) for x in t) for t in new],
                   "sameas": [list(x) for x in sorted({tuple(sorted((pname(s), pname(o))))
                                                       for s, p, o in new if p == same_as})]}
    if chk.get("shacl"):
        r["shacl"] = run_shacl(full.serialize("turtle"), chk["shacl"], chk.get("shacl_inference", "none"))
    if chk.get("rules"):
        r["rules"] = run_rules(full.serialize("turtle"), chk["rules"])
    if chk.get("metrics"):
        r["metrics"] = metrics.compute(full, chk.get("metrics_namespace", BS if chk["metrics"] is True else None))
    if l.queries:
        r["queries"] = []
        closure = None
        for q in l.queries:
            target = full
            if q.on == "reasoned":
                if closure is None:
                    closure, _ = rl_closure(full)
                target = closure
            try:
                if query_form(q.text) == "ASK":
                    r["queries"].append({"title": q.title, "rows": int(target.ask(q.text)), "sample": [],
                                         "expected": q.rows})
                else:
                    rows = [[pname(t) for t in row.values()] for row in target.select(q.text)]
                    # Without ORDER BY the order is the engine's; sorted, the
                    # sample the document shows is the same every time.
                    if not re.search(r"\bORDER\s+BY\b", q.text, re.I):
                        rows.sort()
                    r["queries"].append({"title": q.title, "rows": len(rows), "sample": rows[:8], "expected": q.rows})
            except Exception as e:  # noqa: BLE001
                r["queries"].append({"title": q.title, "error": str(e)[:200], "expected": q.rows})
    return r, full, full_path


def measure_external(l, r: dict, full_path: Path) -> dict:
    """The subprocess work: ROBOT's profile checker and HermiT, and the
    quality checks. Safe to run in a thread pool. The profile is
    checked on the lesson's own model unless the lesson says profile_on="full";
    reasoning always sees the full graph, data and imports included."""
    chk = l.check
    if not r.get("ok"):
        return r
    if chk.get("profile") or chk.get("profiles"):
        if robot.available():
            names = ["DL", "EL", "QL", "RL"] if chk.get("profiles") else ["DL"]
            target = full_path if chk.get("profile_on") == "full" else MODELS / f"{l.oid}.ttl"
            r["profile"] = {}
            for nm in names:
                ok, first = robot.profile(target, nm)
                r["profile"][nm] = {"ok": ok, "first": first}
        else:
            r["profile"] = {"skipped": "ROBOT not installed"}
    if chk.get("reason"):
        if robot.available():
            r["hermit"] = robot.reason(full_path)
            r["hermit"]["inferred"] = [" ".join(pname(x) for x in t) for t in r["hermit"]["inferred"]]
        else:
            r["hermit"] = {"skipped": "ROBOT not installed"}
    if chk.get("explain") and robot.available():
        prefixes = {k: v for k, v in PREFIX_URI.items() if k in ("bt", "bs", "owl", "rdfs", "xsd", "skos")}
        r["explanation"] = robot.explain(full_path, chk.get("explain_axiom", ""), prefixes, mode=chk["explain"],
                                         most=chk.get("explain_most", 1))
    if chk.get("version_diff"):
        old_name, new_name = chk["version_diff"]
        r["version_diff"] = run_version_diff(l, old_name, new_name)
    if chk.get("answer") and robot.available():
        folder = MODELS / l.oid
        folder.mkdir(parents=True, exist_ok=True)
        answer = folder / chk["answer"]
        answer.write_text(l.companions[chk["answer"]].strip() + "\n", encoding="utf-8", newline="\n")
        ok, first = robot.profile(answer, "DL")
        h = robot.reason(answer)
        r["answer"] = {"dl": ok, "first": first, "consistent": h["consistent"], "unsatisfiable": h["unsatisfiable"],
                       "inferred": [" ".join(pname(x) for x in t) for t in h["inferred"]]}
    if chk.get("oqs"):
        r["oqs"] = run_checks(full_path, chk["oqs"], r.get("hermit"), chk.get("own_namespace", BS))
    return r


def check_expectation(l, r: dict) -> list[str]:
    e = l.expect
    problems = []
    if not r.get("ok"):
        return [r.get("error", "failed")]
    for key in ("classes", "object_properties", "datatype_properties", "annotation_properties", "individuals", "concepts"):
        if key in e and r.get(key) != e[key]:
            problems.append(f"{key}: expected {e[key]}, got {r.get(key)}")
    if "min_triples" in e and r["triples"] < e["min_triples"]:
        problems.append(f"triples: expected at least {e['min_triples']}, got {r['triples']}")
    if "names_bad" in e and len(r.get("names_bad", [])) != e["names_bad"]:
        problems.append(f"names_bad: expected {e['names_bad']}, got {r.get('names_bad')}")
    if "circular" in e and len(r.get("circular", [])) != e["circular"]:
        problems.append(f"circular: expected {e['circular']}, got {r.get('circular')}")
    prof = r.get("profile", {})
    for nm in ("DL", "EL", "QL", "RL"):
        key = nm.lower()
        if key in e and nm in prof and prof[nm]["ok"] != e[key]:
            problems.append(f"OWL 2 {nm}: expected {'in' if e[key] else 'out of'} profile; {prof[nm]['first'][:120]}")
    h = r.get("hermit", {})
    if "explanations" in e and len(explanation_sizes(r.get("explanation", ""))) != e["explanations"]:
        problems.append(f"explanations: expected {e['explanations']} sets, got "
                        f"{len(explanation_sizes(r.get('explanation', '')))}")
    if "consistent" in e and "consistent" in h and h["consistent"] != e["consistent"]:
        problems.append(f"consistent: expected {e['consistent']}, got {h['consistent']}")
    if "unsat" in e and "unsatisfiable" in h:
        got = {u.split("#")[-1].split("/")[-1] for u in h["unsatisfiable"]}
        if got != set(e["unsat"]):
            problems.append(f"unsatisfiable: expected {sorted(e['unsat'])}, got {sorted(got)}")
    for t in e.get("inferred", []):
        if t not in h.get("inferred", []):
            problems.append(f"not inferred by HermiT: {t}")
    for t in e.get("not_inferred", []):
        if t in h.get("inferred", []):
            problems.append(f"inferred by HermiT, but should not be: {t}")
    rl = r.get("rl", {})
    for t in e.get("rl_inferred", []):
        if t not in rl.get("named", []):
            problems.append(f"not in the RL closure: {t}")
    for t in e.get("rl_not_inferred", []):
        if t in rl.get("named", []):
            problems.append(f"in the RL closure, but should not be: {t}")
    for pair in e.get("rl_sameas", []):
        if sorted(pair) not in rl.get("sameas", []):
            problems.append(f"RL closure did not derive sameAs {pair}")
    if "rl_min_added" in e and rl.get("added", 0) < e["rl_min_added"]:
        problems.append(f"RL closure added {rl.get('added')}, expected at least {e['rl_min_added']}")
    if "answer_dl" in e and "answer" in r and r["answer"]["dl"] != e["answer_dl"]:
        problems.append(f"answer.ttl DL: expected {e['answer_dl']}; {r['answer']['first'][:120]}")
    if "answer_consistent" in e and "answer" in r and r["answer"]["consistent"] != e["answer_consistent"]:
        problems.append(f"answer.ttl consistent: expected {e['answer_consistent']}")
    if "bump" in e and r.get("version_diff", {}).get("bump", "").upper() != e["bump"].upper():
        problems.append(f"version-diff suggested {r.get('version_diff', {}).get('bump')!r}, expected {e['bump']!r}")
    oqs = r.get("oqs", {}).get("ids", {})
    for cid in e.get("oqs", []):
        if cid not in oqs:
            problems.append(f"semops check did not report {cid}")
    for cid in e.get("oqs_not", []):
        if cid in oqs:
            problems.append(f"semops check reported {cid}, but should not have")
    sh = r.get("shacl", {})
    if "shacl_conforms" in e and sh and sh["conforms"] != e["shacl_conforms"]:
        problems.append(f"SHACL conforms: expected {e['shacl_conforms']}, got {sh['conforms']}")
    if "shacl_violations" in e and sh and sh["counts"]["Violation"] != e["shacl_violations"]:
        problems.append(f"SHACL violations: expected {e['shacl_violations']}, got {sh['counts']['Violation']}")
    for mode, want in (e.get("rules") or {}).items():
        got = (r.get("rules") or {}).get(mode)
        if got != want:
            problems.append(f"rules at inference {mode!r}: expected {want} reported triples, got {got}")
    if "shacl_shapes" in e and r.get("shacl", {}).get("shapes") != e["shacl_shapes"]:
        problems.append(f"shapes compiled: expected {e['shacl_shapes']}, got {r.get('shacl', {}).get('shapes')}")
    for q in r.get("queries", []):
        if "error" in q:
            problems.append(f"query '{q['title']}' failed: {q['error']}")
        elif q["expected"] is not None and q["rows"] != q["expected"]:
            problems.append(f"query '{q['title']}': expected {q['expected']} rows, got {q['rows']}")
    return problems


def plural(n: int, one: str, many: str | None = None) -> str:
    """`n` with its noun agreeing: 1 individual, 2 individuals."""
    return f"{n} {one if n == 1 else (many or one + 's')}"


def summary_line(r: dict) -> str:
    if not r.get("ok"):
        return "does not parse -- " + r.get("error", "")[:100]
    parts = ["parses, " + plural(r["triples"], "triple")]
    counts = []
    if r["classes"]:
        counts.append(plural(r["classes"], "class", "classes"))
    if r["object_properties"]:
        counts.append(plural(r["object_properties"], "object property", "object properties"))
    if r["datatype_properties"]:
        counts.append(plural(r["datatype_properties"], "datatype property", "datatype properties"))
    if r["concepts"]:
        counts.append(plural(r["concepts"], "concept"))
    if r["individuals"]:
        counts.append(plural(r["individuals"], "individual"))
    if counts:
        parts.append(", ".join(counts))
    if "names_bad" in r:
        parts.append(plural(len(r["names_bad"]), "local name") +
                     (" breaks" if len(r["names_bad"]) == 1 else " break") + " the conventions")
    if "circular" in r:
        parts.append(plural(len(r["circular"]), "circular definition"))
    prof = r.get("profile", {})
    if prof and "skipped" not in prof:
        ins = [nm for nm in ("DL", "EL", "QL", "RL") if nm in prof and prof[nm]["ok"]]
        outs = [nm for nm in ("DL", "EL", "QL", "RL") if nm in prof and not prof[nm]["ok"]]
        if ins:
            parts.append("OWL 2 " + "/".join(ins) + (" in profile" if len(ins) == 1 else ""))
        if outs:
            parts.append("not " + "/".join(outs))
    h = r.get("hermit", {})
    if h and "skipped" not in h:
        if not h["consistent"]:
            parts.append("HermiT: INCONSISTENT")
        elif h["unsatisfiable"]:
            parts.append("HermiT: " + plural(len(h["unsatisfiable"]), "unsatisfiable class", "unsatisfiable classes"))
        else:
            n = len(h["inferred"])
            parts.append(f"HermiT: consistent, {n} inferred" if n else "HermiT: consistent, nothing new")
    rl = r.get("rl", {})
    if rl:
        parts.append(f"RL closure +{rl['added']}")
    if r.get("rules"):
        parts.append("rule reports " + " -> ".join(f"{m} {n}" for m, n in r["rules"].items()))
    if r.get("explanation"):
        sizes = explanation_sizes(r["explanation"])
        if len(sizes) > 1:
            parts.append(f"explained by {len(sizes)} sets, of " + ", ".join(map(str, sizes[:-1]))
                         + f" and {sizes[-1]} axioms")
        else:
            parts.append("explained by " + plural(sizes[0], "axiom") if sizes else "explanation returned")
    if r.get("version_diff"):
        parts.append("version-diff: " + (r["version_diff"]["bump"] or "no verdict"))
    if r.get("answer"):
        a = r["answer"]
        parts.append("answer.ttl: " + ("OWL 2 DL" if a["dl"] else "not DL") + ", " +
                     ("consistent" if a["consistent"] and not a["unsatisfiable"] else "not consistent") +
                     (f", {len(a['inferred'])} inferred" if a["inferred"] else ""))
    oqs = r.get("oqs", {})
    if oqs:
        ids = oqs.get("ids", {})
        parts.append("checks: " + (", ".join(ids) if ids else "no findings"))
    sh = r.get("shacl", {})
    if sh:
        c = sh["counts"]
        parts.append(("conforms" if sh["conforms"] else "does not conform") +
                     f" ({plural(c['Violation'], 'violation')}, "
                     f"{plural(c['Warning'], 'warning')}, {c['Info']} info)")
    m = r.get("metrics", {})
    if m:
        s = m["scores"]
        parts.append("OQuaRE DIT " + str(m["metrics"]["DITOnto"]) + f" ({s['DITOnto']}), ANOnto {m['metrics']['ANOnto']:.2f} ({s['ANOnto']})")
    for q in r.get("queries", []):
        if "rows" in q:
            parts.append(f"'{q['title'][:28]}' {q['rows']} row{'s' if q['rows'] != 1 else ''}")
    return "; ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--module")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    lessons = list(CATALOGUE)
    if args.ids:
        wanted = {i.lower() for i in args.ids}
        lessons = [l for l in lessons if l.oid in wanted]
    if args.module:
        lessons = [l for l in lessons if l.module == args.module]
    if not lessons:
        print("no lessons matched")
        return 2

    MODELS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    if not robot.available():
        print("note: lib/owl/robot.jar not found; profile and HermiT checks are skipped "
              "(run scripts/setup-tools.ps1)")

    local = [measure_local(l) for l in lessons]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda x: measure_external(x[0], x[1][0], x[1][2]), zip(lessons, local)))

    measured_path = BUILD / "measured.json"
    measured = json.loads(measured_path.read_text(encoding="utf-8")) if measured_path.exists() else {}
    failed = 0
    for l, r in zip(lessons, results):
        problems = check_expectation(l, r)
        line = summary_line(r)
        measured[l.oid] = line
        (RESULTS / f"{l.oid}.json").write_text(json.dumps(r, indent=1, default=str), encoding="utf-8")
        mark = "FAIL" if problems else "ok  "
        failed += bool(problems)
        print(f"{mark} {l.oid} {l.title[:44]:44} {line}")
        for p in problems:
            print(f"        ! {p}")
        if args.show:
            for t in r.get("hermit", {}).get("inferred", [])[:30]:
                print(f"        HermiT + {t}")
            for t in r.get("rl", {}).get("named", [])[:30]:
                print(f"        RL     + {t}")
            for cid, msg in r.get("oqs", {}).get("messages", {}).items():
                print(f"        check {cid}: {msg[:110]}")
            for row in r.get("shacl", {}).get("rows", [])[:12]:
                print(f"        SHACL {row['severity'][:4]} {row['focus']:28} {row['path']:22} {row['message'][:60]}   [{row['shape']}]")
            for q in r.get("queries", []):
                print(f"        query '{q['title']}': {q.get('rows', q.get('error'))} rows")
                for row in q.get("sample", [])[:8]:
                    print("            " + "  ".join(row))
            if r.get("names_bad"):
                print("        names: " + ", ".join(r["names_bad"]))
            if r.get("circular"):
                print("        circular: " + ", ".join(r["circular"]))
    measured_path.write_text(json.dumps(measured, indent=1, sort_keys=True), encoding="utf-8")
    print(f"\n{len(lessons) - failed} of {len(lessons)} lessons as expected")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
