# -*- coding: utf-8 -*-
"""The course's RDF on SemOps System: a HOLOS store from `semops-system`.

HOLOS is the store and SPARQL 1.2 engine the Turtle Editor Viewer runs in the browser,
so a lesson query measured here gives the rows a reader sees. This module is the little
the checker needs on top of it: load files and text, count, query, update and write out.

Terms are N-Triples strings throughout: `<http://...>`, `_:label`, `"text"@en`,
`"7"^^<http://www.w3.org/2001/XMLSchema#integer>`. That is what the store hands back
from `QuerySolution.term`, and it keeps a language tag, a datatype and a blank node
distinct where the store's Python values would not. `value()` gives the plain form: the
IRI, the label or the lexical text.

    pip install semops-system
"""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

import semops_system as so

RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
OWL = "http://www.w3.org/2002/07/owl#"
SKOS = "http://www.w3.org/2004/02/skos/core#"
XSD = "http://www.w3.org/2001/XMLSchema#"

# For the checker's own queries. Lesson queries carry their own prologue.
PREFIXES = (f"PREFIX rdf: <{RDF}>\nPREFIX rdfs: <{RDFS}>\nPREFIX owl: <{OWL}>\n"
            f"PREFIX skos: <{SKOS}>\nPREFIX xsd: <{XSD}>\n")

_FORMAT_BY_SUFFIX = {".ttl": "turtle", ".nt": "ntriples", ".owl": "rdfxml", ".rdf": "rdfxml",
                     ".xml": "rdfxml", ".trig": "trig", ".nq": "nquads"}


# ---------------------------------------------------------------- terms

def is_iri(t: str | None) -> bool:
    return bool(t) and t.startswith("<")


def is_blank(t: str | None) -> bool:
    return bool(t) and t.startswith("_:")


def is_literal(t: str | None) -> bool:
    return bool(t) and t.startswith('"')


_ESCAPE = re.compile(r'\\(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|.)')
_SIMPLE = {"t": "\t", "b": "\b", "n": "\n", "r": "\r", "f": "\f", '"': '"', "'": "'", "\\": "\\"}


def _unescape(text: str) -> str:
    def one(m: re.Match) -> str:
        e = m.group(1)
        if e[0] in "uU" and len(e) > 1:
            return chr(int(e[1:], 16))
        return _SIMPLE.get(e, e)
    return _ESCAPE.sub(one, text)


def lexical(t: str) -> str:
    """A literal's lexical form, unescaped."""
    end = len(t) - 1
    while end > 0:
        if t[end] == '"':
            backslashes = 0
            i = end - 1
            while i >= 0 and t[i] == "\\":
                backslashes += 1
                i -= 1
            if backslashes % 2 == 0:
                break
        end -= 1
    return _unescape(t[1:end])


def value(t: str | None) -> str:
    """The plain form of a term: what rdflib's str() gave, so that sort orders and
    the text the course document shows do not change with the engine."""
    if not t:
        return ""
    if is_iri(t):
        return t[1:-1]
    if is_blank(t):
        return t[2:]
    if is_literal(t):
        return lexical(t)
    return t


def iri(text: str) -> str:
    """An IRI as an N-Triples term."""
    return f"<{text}>"


def escape_literal(text: str) -> str:
    return (text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r"))


# ---------------------------------------------------------------- the store

def _format_for(path: Path, fmt: str | None) -> str:
    return fmt or _FORMAT_BY_SUFFIX.get(path.suffix.lower(), "turtle")


class Graph:
    """One in-memory HOLOS store, as a graph."""

    def __init__(self) -> None:
        self._store = so.holos.Store()

    @classmethod
    def from_file(cls, path: Path | str, fmt: str | None = None) -> Graph:
        g = cls()
        g.load_file(path, fmt)
        return g

    @classmethod
    def from_text(cls, text: str, fmt: str = "turtle") -> Graph:
        g = cls()
        g.load_text(text, fmt)
        return g

    def load_file(self, path: Path | str, fmt: str | None = None) -> int:
        path = Path(path)
        return self._store.load(str(path), format=_format_for(path, fmt))

    def load_text(self, text: str, fmt: str = "turtle") -> int:
        # The store reads files; text goes through one.
        suffix = {"turtle": ".ttl", "ntriples": ".nt", "rdfxml": ".rdf"}.get(fmt, ".ttl")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f"text{suffix}"
            path.write_text(text, encoding="utf-8", newline="\n")
            return self._store.load(str(path), format=fmt)

    def __len__(self) -> int:
        return len(self._store)

    def copy(self) -> Graph:
        return Graph.from_text(self.serialize("ntriples"), "ntriples")

    # -------------------------------------------------------- queries

    def select(self, query: str) -> list[dict[str, str | None]]:
        """Each row as {variable: N-Triples term or None}, in the engine's order."""
        return [{v: row.term(v) for v in row.variables} for row in self._store.query(query)]

    def ask(self, query: str) -> bool:
        return bool(self._store.query(query))

    def update(self, update: str) -> dict:
        return self._store.update(update)

    def column(self, query: str, var: str) -> set[str]:
        """The distinct values of one variable."""
        return {row[var] for row in self.select(query) if row.get(var)}

    def count(self, query: str, var: str = "n") -> int:
        rows = self.select(query)
        return int(value(rows[0][var])) if rows and rows[0].get(var) else 0

    def triples(self) -> set[tuple[str, str, str]]:
        return {(r["s"], r["p"], r["o"]) for r in self.select("SELECT ?s ?p ?o WHERE { ?s ?p ?o }")}

    # -------------------------------------------------------- writing out

    def dump(self, path: Path | str, fmt: str = "turtle") -> None:
        self._store.dump(str(path), format=fmt)

    def serialize(self, fmt: str = "turtle") -> str:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out"
            self.dump(path, fmt)
            return path.read_text(encoding="utf-8")


_FORM = re.compile(r"\b(SELECT|ASK|CONSTRUCT|DESCRIBE)\b", re.I)
# A comment starts a line or follows white space; a # inside an IRI does neither.
_COMMENT = re.compile(r"(?m)(^|\s)#[^\n]*")


def query_form(query: str) -> str:
    """SELECT, ASK, CONSTRUCT or DESCRIBE: the first of them after the prologue."""
    m = _FORM.search(_COMMENT.sub("", query))
    return m.group(1).upper() if m else "SELECT"
