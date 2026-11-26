# -*- coding: utf-8 -*-
"""A thin wrapper round ROBOT, which wraps the OWL API, HermiT and the OWL 2
profile checker. The course uses it as the reference: when a lesson says an
ontology is in OWL 2 DL, or consistent, or that a reasoner infers a triple,
this is what said so.

ROBOT is one jar. scripts/setup-tools.ps1 fetches it, or:

    curl -L -o lib/owl/robot.jar \\
      https://github.com/ontodev/robot/releases/latest/download/robot.jar
"""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from semops_graph import OWL, RDF, Graph, is_blank, value

ROOT = Path(__file__).resolve().parent.parent
JAR = ROOT / "lib" / "owl" / "robot.jar"

_NOISE = re.compile(r"WARNING: (A terminally deprecated|sun\.misc\.Unsafe|Please consider|Use --sun-misc)")


def available() -> bool:
    return JAR.exists()


def _run(args: list[str], timeout: int = 300) -> tuple[int, str]:
    p = subprocess.run(["java", "-jar", str(JAR)] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    out = "\n".join(line for line in ((p.stdout or "") + "\n" + (p.stderr or "")).splitlines()
                    if line.strip() and not _NOISE.search(line))
    return p.returncode, out


def profile(path: Path, name: str = "DL") -> tuple[bool, str]:
    """Is the ontology (with its imports closure) in the named profile? Returns
    the verdict and the first violation the checker lists."""
    code, out = _run(["validate-profile", "--profile", name, "--input", str(path)])
    ok = "in profile]" in out and "NOT in profile" not in out
    first = ""
    for line in out.splitlines():
        s = line.strip()
        if s.startswith(("Use of", "Axiom type", "Illegal", "Not enough", "Cannot", "Datatype", "Undeclared")):
            first = s
            break
    return ok, first


def reason(path: Path, reasoner: str = "HermiT", generators: str = "SubClass ClassAssertion PropertyAssertion") -> dict:
    """Run the reasoner. Returns consistency, the unsatisfiable classes, and the
    triples the reasoned ontology has that the input did not."""
    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "reasoned.ttl"
        code, out = _run(["reason", "--reasoner", reasoner, "--input", str(path),
                          "--axiom-generators", generators, "--include-indirect", "true",
                          "--output", str(out_path)])
        result = {"consistent": True, "unsatisfiable": [], "inferred": [], "log": out[:2000]}
        if "The ontology is inconsistent" in out:
            result["consistent"] = False
            return result
        unsat = re.findall(r"unsatisfiable:\s+(\S+)", out)
        if unsat:
            result["unsatisfiable"] = unsat
            return result
        if not out_path.exists():
            result["error"] = out[:800]
            return result
        # Both graphs in HOLOS, compared as N-Triples. Blank nodes are left out,
        # since their labels do not survive a round trip through the OWL API.
        before = Graph.from_file(path, "turtle").triples()
        after = Graph.from_file(out_path, "turtle").triples()
        thing, individual = f"<{OWL}Thing>", f"<{OWL}NamedIndividual>"
        declarations = {f"<{OWL}{k}>" for k in ("Class", "ObjectProperty", "DatatypeProperty",
                                                  "AnnotationProperty", "Ontology")}
        new = []
        for s, p, o in after - before:
            if any(is_blank(x) for x in (s, p, o)):
                continue
            if o in (individual, thing) or s == thing:
                continue
            if p == f"<{RDF}type>" and o in declarations:
                continue
            new.append((s, p, o))
        # Sorted on the terms' plain text, so the first few the course document
        # shows are the same on every run.
        new.sort(key=lambda t: tuple(map(value, t)))
        result["inferred"] = new
        return result


def explain(path: Path, axiom: str, prefixes: dict, mode: str = "entailment", reasoner: str = "HermiT",
            most: int = 1) -> str:
    """The minimal axiom sets behind an entailment, or behind an inconsistency
    (mode="inconsistency"), as ROBOT's Markdown, up to `most` of them. Which
    one comes back when `most` is smaller than the number there are depends
    on the reasoner's search order, so ask for all of them where a measured
    line depends on it."""
    with tempfile.TemporaryDirectory() as tmp:
        md = Path(tmp) / "explanation.md"
        args = ["explain", "--input", str(path), "--reasoner", reasoner, "--mode", mode, "--max", str(most), "--explanation", str(md)]
        for p, u in prefixes.items():
            args += ["--prefix", f"{p}: {u}"]
        if mode == "entailment":
            args += ["--axiom", axiom]
        code, out = _run(args)
        if md.exists():
            return md.read_text(encoding="utf-8")
        return out[:1500]
