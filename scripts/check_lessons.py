# -*- coding: utf-8 -*-
"""Parse, reason over and measure every lesson, and compare with what it says.

    python scripts/check_lessons.py              # every lesson
    python scripts/check_lessons.py o07 o08      # just these
    python scripts/check_lessons.py --module 07-owl
    python scripts/check_lessons.py --show o44   # print the inferred triples and rows

Each lesson's model is written to build/models/, parsed with rdflib, and then
put through whatever its `check` asks for: the OWL 2 profile checker and
HermiT (through ROBOT), an OWL 2 RL closure (owlrl, the same profile the
editor's reasoner implements), the Ontology Quality Suite, the `shacl`
engine (the same one the editor runs, through its Python bindings), the
OQuaRE metrics, a naming audit, a definition audit, and its own SPARQL
queries. What comes back is compared with the lesson's `expect`, and the run
fails on any expectation that does not hold.

Two files come out of it:

    build/results/<oid>.json     everything measured, for the course document
    build/measured.json          the one-line MEASURED summary per lesson,
                                 which build_lessons.py writes into each header
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import rdflib
from rdflib.namespace import OWL, RDF, RDFS, SKOS

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import catalogue  # noqa: E402,F401
import metrics  # noqa: E402
import robot  # noqa: E402
from ontocat import CATALOGUE, DATA, LIB, PREFIX_URI  # noqa: E402

BUILD = ROOT / "build"
MODELS = BUILD / "models"
RESULTS = BUILD / "results"

NS = {p: rdflib.Namespace(u) for p, u in PREFIX_URI.items()}


def pname(term) -> str:
    """A prefixed name for a term, or the IRI in angle brackets."""
    if isinstance(term, rdflib.Literal):
        return f'"{term}"'
    if isinstance(term, rdflib.BNode):
        return "_:" + str(term)[:6]
    s = str(term)
    for p, u in sorted(PREFIX_URI.items(), key=lambda x: -len(x[1])):
        if s.startswith(u):
            return f"{p}:{s[len(u):]}"
    return f"<{s}>"


def parse_pname(text: str):
    if text.startswith("<"):
        return rdflib.URIRef(text.strip("<>"))
    if text.startswith('"'):
        return rdflib.Literal(text.strip('"'))
    p, _, local = text.partition(":")
    return NS[p][local]


def triple_from(text: str):
    s, p, o = text.split(None, 2)
    return parse_pname(s), parse_pname(p), parse_pname(o)


_DIR_TAG = re.compile(r'@([A-Za-z][A-Za-z0-9-]*?)--(?:rtl|ltr)\b')


def load_data(name: str, into: rdflib.Graph) -> None:
    """Parse a data file into a graph. The Trail's data carries RDF 1.2
    directional language tags (@ar--rtl), which rdflib does not read; the
    direction is dropped, as the SHACL course does before a tool that cannot read them."""
    text = (DATA / name).read_text(encoding="utf-8")
    into.parse(data=_DIR_TAG.sub(r"@\1", text), format="turtle")


# ---------------------------------------------------------------- audits

CLASS_NAME = re.compile(r"^[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*$")
PROP_NAME = re.compile(r"^[a-z][a-z0-9]+(?:[A-Z][a-z0-9]+)*$")
BS = "https://example.org/bookshop-trail/schema#"


def audit_names(g: rdflib.Graph) -> list[str]:
    """Local names in the schema namespace that break the conventions of
    module 03: UpperCamelCase classes, lowerCamelCase properties, letters and
    digits only, acronyms camel-cased."""
    bad = []
    for c in set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, RDFS.Class)):
        if isinstance(c, rdflib.URIRef) and str(c).startswith(BS):
            local = str(c)[len(BS):]
            if not CLASS_NAME.match(local):
                bad.append("bs:" + local)
    for kind in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty, RDF.Property):
        for p in g.subjects(RDF.type, kind):
            if isinstance(p, rdflib.URIRef) and str(p).startswith(BS):
                local = str(p)[len(BS):]
                if not PROP_NAME.match(local) and "bs:" + local not in bad:
                    bad.append("bs:" + local)
    return sorted(bad)


def audit_definitions(g: rdflib.Graph) -> list[str]:
    """Terms whose definition repeats the term's own name: a rough test for
    circularity, and rough on purpose -- it also catches 'a publisher is an
    organisation that publishes', which is the case worth catching."""
    circular = []
    for term in set(g.subjects(SKOS.definition, None)) | set(g.subjects(RDFS.comment, None)):
        if not isinstance(term, rdflib.URIRef):
            continue
        local = str(term).split("#")[-1].split("/")[-1]
        words = re.findall(r"[A-Z]?[a-z]+", local)
        if not words:
            continue
        stems = {w.lower()[:max(4, len(w) - 2)] for w in words if len(w) > 3}
        for text in list(g.objects(term, SKOS.definition)) + list(g.objects(term, RDFS.comment)):
            first = str(text).split(".")[0].lower()
            if any(re.search(r"\b" + re.escape(st), first) for st in stems):
                circular.append(pname(term))
                break
    return sorted(set(circular))


def rl_closure(g: rdflib.Graph) -> tuple[rdflib.Graph, list]:
    """The OWL 2 RL closure, and the triples it added about the Trail's own
    terms. owlrl also adds its axiomatic triples (every XSD datatype, owl:Nothing
    under every class); those are left out of the list and the count."""
    import owlrl
    before = rdflib.Graph()
    for t in g:
        before.add(t)
    closed = rdflib.Graph()
    for t in g:
        closed.add(t)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(closed)
    w3c = (str(RDF), str(RDFS), str(OWL), "http://www.w3.org/2001/XMLSchema#")
    new = []
    for s, p, o in closed:
        if (s, p, o) in before:
            continue
        if any(isinstance(x, rdflib.BNode) for x in (s, p, o)) or isinstance(s, rdflib.Literal):
            continue
        if str(s).startswith(w3c) or o in (OWL.Thing, RDFS.Resource, OWL.NamedIndividual, OWL.Nothing) or s == o:
            continue
        if str(p).startswith(str(RDFS)) and p not in (RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range):
            continue
        new.append((s, p, o))
    return closed, new


def run_oqs(path: Path, stage: str, out_dir: Path, own: str | None) -> dict:
    """Run the Ontology Quality Suite and collect the check ids it reports."""
    args = [sys.executable, "-m", "ontology_suite", stage, "--ontology", str(path),
            "--out-dir", str(out_dir), "--fail-on", "never"]
    if stage == "checks":
        args += ["--engine", "sparql"]
        if own:
            args += ["--own-namespace", own]
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    found: dict[str, int] = {}
    messages: dict[str, str] = {}
    csv_path = out_dir / "full_results.csv"
    if csv_path.exists():
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                cid = row.get("check_id", "")
                found[cid] = found.get(cid, 0) + 1
                messages.setdefault(cid, (row.get("message") or "")[:200])
    return {"ids": dict(sorted(found.items())), "messages": messages, "rc": p.returncode,
            "tail": (p.stdout or "")[-600:]}


def run_version_diff(l, old_name: str, new_name: str) -> dict:
    """Two companion files through the Quality Suite's version-diff: the
    suggested bump and the change lines."""
    folder = MODELS / l.oid
    folder.mkdir(parents=True, exist_ok=True)
    old = folder / old_name
    new = folder / new_name
    old.write_text(l.companions[old_name].strip() + "\n", encoding="utf-8", newline="\n")
    new.write_text(l.companions[new_name].strip() + "\n", encoding="utf-8", newline="\n")
    p = subprocess.run([sys.executable, "-m", "ontology_suite", "version-diff", str(old), str(new),
                        "--exclude-imports", "--out-dir", str(folder / "diff")],
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
        return pname(rdflib.URIRef(text[1:-1]))
    return text


def run_shacl(data_text: str, shapes_text: str, inference: str = "none") -> dict:
    """Validate with the engine the Turtle Editor Viewer runs: `shacl`, the
    Rust engine whose WebAssembly build is in the editor and whose Python
    bindings are on PyPI. Same engine, same answers as the browser."""
    import shacl as engine
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
    return {"conforms": bool(report.conforms), "counts": counts, "rows": rows,
            "shapes": len(shapes), "inference": inference}


def run_rules(data_text: str, shapes_text: str) -> dict:
    """A validator's only output is its report, so a rule's effect is measured
    the way the SHACL course measures it and the way the editor's Inference
    dropdown shows it: a shape at Info severity reports one result per derived
    triple, and the count is taken at each inference mode."""
    import shacl as engine
    shapes = engine.Shapes.from_text(shapes_text)
    out = {}
    for mode in ("none", "rules", "rules-iterated"):
        report = shapes.validate_text(data_text, inference=mode)
        out[mode] = sum(1 for r in report.results if r.severity == "Info")
    return out


# ---------------------------------------------------------------- one lesson

def measure_local(l) -> tuple[dict, rdflib.Graph | None, Path]:
    """Everything that runs in-process: parse, count, audit, closure, shapes,
    queries. rdflib's SPARQL parser is not thread-safe, so this runs on the
    main thread."""
    r: dict = {"oid": l.oid, "ok": True}
    chk = l.check
    path = MODELS / f"{l.oid}.ttl"
    path.write_text(l.model_text, encoding="utf-8", newline="\n")
    try:
        g = rdflib.Graph().parse(str(path), format="turtle")
    except Exception as e:  # noqa: BLE001
        r["ok"] = False
        r["error"] = f"does not parse: {str(e)[:300]}"
        return r, None, path
    r["triples"] = len(g)
    r["classes"] = len({c for c in g.subjects(RDF.type, OWL.Class) if isinstance(c, rdflib.URIRef)}
                       | {c for c in g.subjects(RDF.type, RDFS.Class) if isinstance(c, rdflib.URIRef)})
    r["object_properties"] = len(set(g.subjects(RDF.type, OWL.ObjectProperty)))
    r["datatype_properties"] = len(set(g.subjects(RDF.type, OWL.DatatypeProperty)))
    r["annotation_properties"] = len(set(g.subjects(RDF.type, OWL.AnnotationProperty)))
    r["rdf_properties"] = len(set(g.subjects(RDF.type, RDF.Property)))
    r["concepts"] = len(set(g.subjects(RDF.type, SKOS.Concept)))
    meta = {OWL.Class, RDFS.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty, RDF.Property,
            OWL.Ontology, OWL.NamedIndividual, RDFS.Datatype, OWL.Restriction, OWL.AllDisjointClasses,
            OWL.TransitiveProperty, OWL.SymmetricProperty, OWL.FunctionalProperty, OWL.InverseFunctionalProperty,
            OWL.AsymmetricProperty, OWL.IrreflexiveProperty, OWL.ReflexiveProperty, SKOS.ConceptScheme}
    r["individuals"] = len({s for s, t in g.subject_objects(RDF.type)
                            if isinstance(s, rdflib.URIRef) and t not in meta and not str(t).startswith(str(OWL))
                            and (s, RDF.type, OWL.Class) not in g and (s, RDF.type, RDFS.Class) not in g})

    full = g
    full_path = path
    if chk.get("with_data") or chk.get("imports"):
        full = rdflib.Graph()
        for t in g:
            full.add(t)
        names = chk.get("with_data") or []
        for name in ([names] if isinstance(names, str) else names):
            load_data(name, full)
        for name in chk.get("imports") or []:
            imported = rdflib.Graph().parse(str(LIB / name), format="turtle")
            # One ontology header only: the OWL API refuses a document with
            # several, so the imported ontologies' own headers are dropped.
            for header in list(imported.subjects(RDF.type, OWL.Ontology)):
                imported.remove((header, None, None))
            imported.remove((None, OWL.imports, None))
            for t in imported:
                full.add(t)
        full_path = MODELS / f"{l.oid}.full.ttl"
        full.serialize(destination=str(full_path), format="turtle")
        r["full_triples"] = len(full)

    if chk.get("names"):
        r["names_bad"] = audit_names(g)
    if chk.get("definitions"):
        r["circular"] = audit_definitions(g)
    if chk.get("rl"):
        closed, new = rl_closure(full)
        r["rl"] = {"added": len(new),
                   "named": [" ".join(pname(x) for x in t) for t in new],
                   "sameas": [list(x) for x in sorted({tuple(sorted((pname(s), pname(o))))
                                                       for s, p, o in new if p == OWL.sameAs})]}
    if chk.get("shacl"):
        r["shacl"] = run_shacl(full.serialize(format="turtle"), chk["shacl"], chk.get("shacl_inference", "none"))
    if chk.get("rules"):
        r["rules"] = run_rules(full.serialize(format="turtle"), chk["rules"])
    if chk.get("metrics"):
        r["metrics"] = metrics.compute(full, chk.get("metrics_namespace", BS if chk["metrics"] is True else None))
    if l.queries:
        r["queries"] = []
        for q in l.queries:
            target = full
            if q.on == "reasoned":
                target, _ = rl_closure(full)
            try:
                res = target.query(q.text)
                if res.type == "SELECT":
                    rows = [[pname(x) if x is not None else "" for x in row] for row in res]
                    r["queries"].append({"title": q.title, "rows": len(rows), "sample": rows[:8], "expected": q.rows})
                else:
                    r["queries"].append({"title": q.title, "rows": int(bool(res.askAnswer)), "sample": [], "expected": q.rows})
            except Exception as e:  # noqa: BLE001
                r["queries"].append({"title": q.title, "error": str(e)[:200], "expected": q.rows})
    return r, full, full_path


def measure_external(l, r: dict, full_path: Path) -> dict:
    """The subprocess work: ROBOT's profile checker and HermiT, and the
    Ontology Quality Suite. Safe to run in a thread pool. The profile is
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
        r["explanation"] = robot.explain(full_path, chk.get("explain_axiom", ""), prefixes, mode=chk["explain"])
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
        out_dir = BUILD / "oqs" / l.oid
        out_dir.mkdir(parents=True, exist_ok=True)
        r["oqs"] = run_oqs(full_path, chk["oqs"], out_dir, chk.get("own_namespace", BS))
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
            problems.append(f"OQS did not report {cid}")
    for cid in e.get("oqs_not", []):
        if cid in oqs:
            problems.append(f"OQS reported {cid}, but should not have")
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


def summary_line(r: dict) -> str:
    if not r.get("ok"):
        return "does not parse -- " + r.get("error", "")[:100]
    parts = [f"parses, {r['triples']} triples"]
    counts = []
    if r["classes"]:
        counts.append(f"{r['classes']} class{'es' if r['classes'] != 1 else ''}")
    if r["object_properties"]:
        counts.append(f"{r['object_properties']} object propert{'ies' if r['object_properties'] != 1 else 'y'}")
    if r["datatype_properties"]:
        counts.append(f"{r['datatype_properties']} datatype propert{'ies' if r['datatype_properties'] != 1 else 'y'}")
    if r["concepts"]:
        counts.append(f"{r['concepts']} concepts")
    if r["individuals"]:
        counts.append(f"{r['individuals']} individuals")
    if counts:
        parts.append(", ".join(counts))
    if "names_bad" in r:
        parts.append(f"{len(r['names_bad'])} local names break the conventions")
    if "circular" in r:
        parts.append(f"{len(r['circular'])} circular definitions")
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
            parts.append(f"HermiT: {len(h['unsatisfiable'])} unsatisfiable class{'es' if len(h['unsatisfiable']) != 1 else ''}")
        else:
            n = len(h["inferred"])
            parts.append(f"HermiT: consistent, {n} inferred" if n else "HermiT: consistent, nothing new")
    rl = r.get("rl", {})
    if rl:
        parts.append(f"RL closure +{rl['added']}")
    if r.get("rules"):
        parts.append("rule reports " + " -> ".join(f"{m} {n}" for m, n in r["rules"].items()))
    if r.get("explanation"):
        n = sum(1 for line in r["explanation"].splitlines() if line.startswith("  - "))
        parts.append(f"explained by {n} axioms" if n else "explanation returned")
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
        parts.append("OQS: " + (", ".join(ids) if ids else "no findings"))
    sh = r.get("shacl", {})
    if sh:
        c = sh["counts"]
        parts.append(("conforms" if sh["conforms"] else "does not conform") +
                     f" ({c['Violation']} violations, {c['Warning']} warnings, {c['Info']} info)")
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
                print(f"        OQS {cid}: {msg[:110]}")
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
