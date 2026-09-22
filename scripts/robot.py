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

import rdflib

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
        before = rdflib.Graph().parse(str(path), format="turtle")
        after = rdflib.Graph().parse(str(out_path))
        new = []
        for s, p, o in after:
            if (s, p, o) in before:
                continue
            if any(isinstance(x, rdflib.BNode) for x in (s, p, o)):
                continue
            if o in (rdflib.OWL.NamedIndividual, rdflib.OWL.Thing) or s == rdflib.OWL.Thing:
                continue
            if p in (rdflib.RDF.type,) and o in (rdflib.OWL.Class, rdflib.OWL.ObjectProperty,
                                                 rdflib.OWL.DatatypeProperty, rdflib.OWL.AnnotationProperty,
                                                 rdflib.OWL.Ontology):
                continue
            new.append((s, p, o))
        result["inferred"] = new
        return result


def explain(path: Path, axiom: str, prefixes: dict, mode: str = "entailment", reasoner: str = "HermiT") -> str:
    """The minimal axiom set behind an entailment, or behind an inconsistency
    (mode="inconsistency"), as ROBOT's Markdown."""
    with tempfile.TemporaryDirectory() as tmp:
        md = Path(tmp) / "explanation.md"
        args = ["explain", "--input", str(path), "--reasoner", reasoner, "--mode", mode, "--explanation", str(md)]
        for p, u in prefixes.items():
            args += ["--prefix", f"{p}: {u}"]
        if mode == "entailment":
            args += ["--axiom", axiom]
        code, out = _run(args)
        if md.exists():
            return md.read_text(encoding="utf-8")
        return out[:1500]
