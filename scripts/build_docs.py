# -*- coding: utf-8 -*-
"""docs/index.html: the whole course as one document.

    python scripts/check_lessons.py     # first, so the measurements are current
    python scripts/build_docs.py

Every lesson appears with its model, its explanation, what the tools measured
for it, and buttons that open the lesson in the editor or copy the model. The
reference sections at the end are generated from the same tables the READMEs
use. Lesson ids in the prose become links: o07 to this document, q28 to the
SPARQL course, s20 to the SHACL course, all three at their hosted addresses.
"""
from __future__ import annotations

import base64
import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import catalogue  # noqa: E402,F401
import features  # noqa: E402
import metrics  # noqa: E402
import specs  # noqa: E402
from ontocat import (CATALOGUE, MODULE_INFO, REPO, SPARQL_REPO, SHACL_REPO, SITE, SPARQL_SITE,  # noqa: E402
                     SHACL_SITE, SEMOPS, EDITOR_BASE)

BUILD = ROOT / "build"
DOCS = ROOT / "docs"
MAX_ROWS = 10

E = html.escape

# ---------------------------------------------------------------- highlighting

SPARQL_KW = re.compile(r"\b(SELECT|CONSTRUCT|ASK|WHERE|FILTER|BIND|AS|NOT|EXISTS|UNION|OPTIONAL|GROUP BY|HAVING|"
                       r"ORDER BY|DESC|ASC|LIMIT|PREFIX|GRAPH|MINUS|VALUES|DISTINCT|COUNT|SUM|STR|SUBSTR|"
                       r"REGEX|BOUND|COALESCE|LANG|IN|IF|CONTAINS|STRSTARTS|isIRI|isNumeric)\b")
SPARQL_VAR = re.compile(r"(\$this|\$[A-Za-z][A-Za-z0-9]*|\?[A-Za-z][A-Za-z0-9]*)")

TOKEN = re.compile(r"""
    (?P<comment>\#[^\n]*)
  | (?P<lstring>"{3}[\s\S]*?"{3})
  | (?P<string>"(?:[^"\\\n]|\\.)*"(?:@[A-Za-z0-9-]+|\^\^[A-Za-z]+:[A-Za-z0-9_]+)?)
  | (?P<iri><[^>\s]*>)
  | (?P<annot>@prefix)
  | (?P<kwterm>(?<![A-Za-z0-9])(?:owl|rdfs|rdf|skos|sh):[A-Za-z][A-Za-z0-9]*)
  | (?P<pname>(?<![A-Za-z0-9])[A-Za-z][A-Za-z0-9_-]*:[A-Za-z0-9_.-]*)
  | (?P<num>(?<![A-Za-z0-9_.-])-?\d+(?:\.\d+)?(?![A-Za-z0-9_-]))
  | (?P<kw>(?<![A-Za-z0-9_])(?:a|true|false)(?![A-Za-z0-9_]))
""", re.X)


def highlight_sparql(text: str) -> str:
    out, pos = [], 0
    for m in SPARQL_VAR.finditer(text):
        out.append(SPARQL_KW.sub(lambda k: f'<b>{k.group(0)}</b>', E(text[pos:m.start()])))
        out.append(f'<span class="t-var">{E(m.group(0))}</span>')
        pos = m.end()
    out.append(SPARQL_KW.sub(lambda k: f'<b>{k.group(0)}</b>', E(text[pos:])))
    return "".join(out)


def highlight(turtle: str) -> str:
    out, pos = [], 0
    for m in TOKEN.finditer(turtle):
        out.append(E(turtle[pos:m.start()]))
        kind, tok = m.lastgroup, m.group(0)
        cls = {"comment": "t-comment", "lstring": "t-string", "string": "t-string", "iri": "t-iri", "annot": "t-annot",
               "kwterm": "t-kw", "pname": "t-pname", "num": "t-num", "kw": "t-fn"}[kind]
        inner = highlight_sparql(tok) if kind == "lstring" else E(tok)
        out.append(f'<span class="{cls}">{inner}</span>')
        pos = m.end()
    out.append(E(turtle[pos:]))
    return "".join(out)


# ---------------------------------------------------------------- pieces

def prose(text: str) -> str:
    """Paragraphs from a why/notes string; code-ish tokens in <code>; lesson
    ids linked, in this document and in the other two courses."""
    paras = [" ".join(p.split()) for p in text.split(chr(10) + chr(10)) if p.strip()]

    def fmt(p):
        p = E(p)
        p = re.sub(r"(?<![\w/#])((?:bs|bt|oc|rdf|rdfs|owl|xsd|skos|dct|vann|sh|geo|gist|gistd|gufo|obo|wgs84):[A-Za-z_][\w.-]*)",
                   r"<code>\1</code>", p)
        p = re.sub(r"(?<![\w-])(o\d\d)\b", r'<a href="#\1">\1</a>', p)
        p = re.sub(r"(?<![\w-])(q\d{2,3})\b", r'<a href="%s#\1">\1</a>' % SPARQL_SITE, p)
        p = re.sub(r"(?<![\w-])(s\d\d)\b", r'<a href="%s#\1">\1</a>' % SHACL_SITE, p)
        p = re.sub(r"\b((?:LOG|STR|QUA|STY|REA|EFF|DAT|CNF|VOC|TQL)-\d{3})\b", r"<code>\1</code>", p)
        p = re.sub(r"\b(FP-\d{3})\b", r"<code>\1</code>", p)
        return f"<p>{p}</p>"
    return "".join(fmt(p) for p in paras)


def button_bar(l) -> str:
    return (f'<div class="btns">'
            f'<a class="btn primary" href="{E(l.editor_url)}" target="_blank" rel="noopener">Open in the editor</a>'
            f'<button class="btn" data-copy="{l.oid}">Copy model</button>'
            f'<a class="btn" href="{REPO}/blob/main/lessons/{l.module}/{E(l.filename)}" target="_blank" rel="noopener">The file</a>'
            + "".join(f'<a class="btn" href="{REPO}/blob/main/lessons/{l.module}/{E(name)}" target="_blank" rel="noopener">{E(name)}</a>'
                      for name in l.companions)
            + '</div>')


def n_of(n, one: str, many: str | None = None) -> str:
    """`n` with its noun agreeing: 1 violation, 2 violations."""
    return f"{n} {one if n == 1 else (many or one + 's')}"


def measured_block(l, r: dict | None) -> str:
    if not r:
        return ""
    if not r.get("ok"):
        return f'<div class="report err"><h4>Measured</h4><p class="results-note">{E(r.get("error", ""))}</p></div>'
    rows = []

    def row(label, value):
        rows.append(f"<tr><th>{E(label)}</th><td>{value}</td></tr>")

    counts = [n_of(r["triples"], "triple")]
    for key, one, many in (("classes", "class", "classes"), ("object_properties", "object property", "object properties"),
                           ("datatype_properties", "datatype property", "datatype properties"),
                           ("annotation_properties", "annotation property", "annotation properties"),
                           ("concepts", "concept", "concepts"), ("individuals", "individual", "individuals")):
        n = r.get(key, 0)
        if n:
            counts.append(n_of(n, one, many))
    row("Parses", E("; ".join(counts)) + (f' (with the data: {n_of(r["full_triples"], "triple")})' if r.get("full_triples") else ""))
    if "names_bad" in r:
        row("Naming audit", E(", ".join(r["names_bad"]) if r["names_bad"] else "every local name conforms"))
    if "circular" in r:
        row("Definition audit", E(", ".join(r["circular"]) + " repeat the term's own name" if r["circular"] else "no circular definition"))
    prof = r.get("profile", {})
    if prof and "skipped" not in prof:
        parts = []
        for nm in ("DL", "EL", "QL", "RL"):
            if nm in prof:
                parts.append(f'<span class="{"ok" if prof[nm]["ok"] else "no"}">OWL 2 {nm}: {"in profile" if prof[nm]["ok"] else "not in profile"}</span>'
                             + (f' <span class="why">{E(prof[nm]["first"][:140])}</span>' if not prof[nm]["ok"] and prof[nm]["first"] else ""))
        row("Profile (ROBOT)", "<br>".join(parts))
    h = r.get("hermit", {})
    if h and "skipped" not in h:
        if not h["consistent"]:
            v = '<span class="no">inconsistent</span>'
        elif h["unsatisfiable"]:
            v = '<span class="no">consistent; unsatisfiable: ' + E(", ".join(u.split("#")[-1] for u in h["unsatisfiable"])) + "</span>"
        else:
            v = '<span class="ok">consistent</span>'
            if h["inferred"]:
                shown = h["inferred"][:MAX_ROWS]
                v += f"; {len(h['inferred'])} inferred" + "<ul class='trip'>" + "".join(f"<li><code>{E(t)}</code></li>" for t in shown) + "</ul>"
                if len(h["inferred"]) > MAX_ROWS:
                    v += f'<span class="results-note">and {len(h["inferred"]) - MAX_ROWS} more</span>'
            else:
                v += "; nothing new"
        row("HermiT", v)
    if r.get("explanation"):
        lines = [x[4:] for x in r["explanation"].splitlines() if x.startswith("  - ")]
        if lines:
            row("Explanation (ROBOT)", "<ul class='trip'>" + "".join(f"<li>{E(re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\\1', x))}</li>" for x in lines[:8]) + "</ul>")
    rl = r.get("rl", {})
    if rl:
        v = f"+{rl['added']} triples about the Trail's terms"
        if rl["named"]:
            v += "<ul class='trip'>" + "".join(f"<li><code>{E(t)}</code></li>" for t in rl["named"][:MAX_ROWS]) + "</ul>"
            if len(rl["named"]) > MAX_ROWS:
                v += f'<span class="results-note">and {len(rl["named"]) - MAX_ROWS} more</span>'
        row("OWL 2 RL closure (owlrl; what Show Facts computes)", v)
    if r.get("rules"):
        labels = {"none": "asserted only", "rules": "rules, one pass", "rules-iterated": "rules, iterated to a fixpoint"}
        trs = "".join(f"<tr><td>{E(labels[m])}</td><td>{n} reported</td></tr>" for m, n in r["rules"].items())
        row("SHACL-AF rule (the editor's Inference dropdown)",
            "One Info result per derived triple, counted at each mode:"
            f'<div class="tablewrap small"><table><tbody>{trs}</tbody></table></div>')
    if r.get("version_diff"):
        vd = r["version_diff"]
        v = f"<b>Suggested version bump: {E(vd['bump'] or 'none')}</b>"
        if vd["lines"]:
            v += "<ul class='trip'>" + "".join(f"<li>{E(x)}</li>" for x in vd["lines"][:12]) + "</ul>"
        row("version-diff (Ontology Quality Suite)", v)
    if r.get("answer"):
        a = r["answer"]
        v = ("OWL 2 DL" if a["dl"] else "not DL") + "; " + ("consistent" if a["consistent"] and not a["unsatisfiable"] else "not consistent")
        if a["inferred"]:
            v += "<ul class='trip'>" + "".join(f"<li><code>{E(t)}</code></li>" for t in a["inferred"][:8]) + "</ul>"
        row("answer.ttl", v)
    oqs = r.get("oqs", {})
    if oqs:
        ids = oqs.get("ids", {})
        if ids:
            v = "<ul class='trip'>" + "".join(f"<li><code>{E(cid)}</code> &times;{n}: {E(oqs['messages'].get(cid, '')[:150])}</li>" for cid, n in ids.items()) + "</ul>"
        else:
            v = "no findings"
        row("Ontology Quality Suite", v)
    sh = r.get("shacl", {})
    if sh:
        c = sh["counts"]
        v = (f'<span class="{"ok" if sh["conforms"] else "no"}">{"conforms" if sh["conforms"] else "does not conform"}</span>'
             f' &middot; {n_of(c["Violation"], "violation")}, {n_of(c["Warning"], "warning")}, {c["Info"]} info')
        if sh["rows"]:
            trs = "".join(f'<tr class="sev-{x["severity"].lower()}"><td>{x["severity"]}</td><td><code>{E(x["focus"])}</code></td>'
                          f'<td><code>{E(x["path"])}</code></td><td>{E(x["message"])}</td></tr>' for x in sh["rows"][:MAX_ROWS])
            v += f'<div class="tablewrap small"><table><thead><tr><th>Severity</th><th>Focus node</th><th>Path</th><th>Message</th></tr></thead><tbody>{trs}</tbody></table></div>'
            if len(sh["rows"]) > MAX_ROWS:
                v += f'<span class="results-note">and {len(sh["rows"]) - MAX_ROWS} more</span>'
        row(f"SHACL ({n_of(sh['shapes'], 'shape')} compiled" + (f", inference <em>{E(sh['inference'])}</em>" if sh.get("inference", "none") != "none" else "") + ")", v)
    m = r.get("metrics", {})
    if m:
        trs = "".join(f"<tr><td><code>{k}</code></td><td>{(f'{v*100:.0f}%' if k in metrics.RELATIVE else f'{v:g}')}</td><td>{m['scores'][k]}</td></tr>"
                      for k, v in m["metrics"].items())
        v = (f"{n_of(m['counts']['classes'], 'class', 'classes')}, "
             f"{n_of(m['counts']['object_properties'], 'object property', 'object properties')}, "
             f"{n_of(m['counts']['datatype_properties'], 'datatype property', 'datatype properties')}, "
             f"{n_of(m['counts']['roots'], 'root')}, {n_of(m['counts']['leaves'], 'leaf', 'leaves')}"
             f'<div class="tablewrap small"><table><thead><tr><th>Metric</th><th>Value</th><th>Score 1 to 5</th></tr></thead><tbody>{trs}</tbody></table></div>')
        row("OQuaRE (scripts/metrics.py)", v)
    for q in r.get("queries", []):
        if "error" in q:
            row(f"Query: {q['title']}", f'<span class="no">{E(q["error"])}</span>')
        else:
            v = f"{q['rows']} row{'' if q['rows'] == 1 else 's'}"
            if q["sample"]:
                v += "<ul class='trip'>" + "".join("<li>" + "  ".join(f"<code>{E(x)}</code>" for x in rowv) + "</li>" for rowv in q["sample"][:8]) + "</ul>"
            row(f"Query: {q['title']}", v)
    return f'<div class="report"><h4>Measured</h4><table class="measured"><tbody>{"".join(rows)}</tbody></table></div>'


def lesson_html(l, results: dict) -> str:
    specs_html = "".join(f'<li><a href="{E(u)}">{E(t)}</a></li>' for t, u in specs.for_lesson(l.oid, l.module, limit=2))
    learn = "".join(f"<li>{prose(x)[3:-4]}</li>" for x in l.learn)
    notes = f'<h4>Note</h4>{prose(l.notes)}' if l.notes else ""
    tryit = f'<h4>Try it</h4>{prose(l.tryit)}' if l.tryit else ""
    queries = ""
    if l.queries:
        items = []
        for i, q in enumerate(l.queries):
            qid = f"{l.oid}-q{i}"
            items.append(f'<div class="query"><div class="qh"><span>{E(q.title)} <em>(on the {E(q.on)})</em></span>'
                         f'<button class="btn small" data-copy="{qid}">Copy query</button></div>'
                         f'<div class="code-wrap"><pre class="code" id="code-{qid}">{highlight_sparql(q.text.strip())}</pre></div></div>')
        queries = f'<h4>Afterwards, in the SPARQL panel</h4>{"".join(items)}'
    meta = []
    if l.corner:
        meta.append(f"Corner: <em>{E(l.corner)}</em>")
    if l.data:
        meta.append(f"Data: <code>{E(l.data)}</code>")
    meta.append("Runs in the browser" + (f"; {E(l.local)}" if l.local else ""))
    return f"""
<article class="lesson" id="{l.oid}">
  <div class="lhead"><span class="lid">{l.oid.upper()}</span><h3>{E(l.title)}</h3></div>
  <p class="asks">{E(l.decides)}</p>
  <p class="dataline">{" &middot; ".join(meta)}</p>
  {button_bar(l)}
  <div class="code-wrap"><pre class="code" id="code-{l.oid}">{highlight(l.model_text.strip())}</pre></div>
  <div class="mech">
    <div class="mech-prose"><h4>Why</h4>{prose(l.why)}</div>
    <div class="mech-diagram"><h4>Diagram</h4><pre class="diagram">{E(l.diagram.strip(chr(10)))}</pre></div>
  </div>
  <div class="learn"><h4>What to take away</h4><ul>{learn}</ul>{notes}{tryit}</div>
  {measured_block(l, results.get(l.oid))}
  {queries}
  <p class="specline">Sources <ul class="specs">{specs_html}</ul></p>
</article>"""


def module_html(module: str, lessons: list, results: dict) -> str:
    title, blurb = MODULE_INFO[module]
    num = module.split("-")[0]
    spec_links = "".join(f'<li><a href="{E(u)}">{E(t)}</a></li>' for t, u in specs.for_module(module))
    body = "".join(lesson_html(l, results) for l in lessons)
    return f"""
<section class="module" id="m{num}">
  <div class="module-head"><div class="module-num">Module {num}</div><h2>{E(title)}</h2>
  <p class="module-blurb">{E(blurb)}</p>
  <details class="standards"><summary>Sources</summary><ul>{spec_links}</ul></details></div>
  {body}
</section>"""


def lab_html() -> str:
    return f"""
<section class="module" id="m00">
  <div class="module-head"><div class="module-num">Module 00</div><h2>The lab</h2>
  <p class="module-blurb">Twenty minutes on the tool before the first lesson. Everything runs in the Turtle Editor Viewer at
  <a href="{EDITOR_BASE}">semantechs.co.uk/turtle-editor-viewer</a>: the parser, the graph view, the SPARQL engine, the OWL 2 RL
  reasoner behind <b>Show Facts</b>, and the SHACL engine with its Inference dropdown, all inside the page. The full text is
  <a href="{REPO}/tree/main/lessons/00-the-lab">lessons/00-the-lab/README.md</a>.</p></div>

  <div class="grid2">
    <div class="panel"><h3>One file, one tab</h3>
      <p>Every lesson is a Turtle file with a header that carries the whole lesson. <b>Open in the editor</b> loads it; the
      graph view draws it; <b>Add Prefixes</b> then the SPARQL panel runs the queries at the end of the file.</p>
      <p>Press <b>Get All</b> after any edit, or the SPARQL panel answers about the file as it was.</p>
      <p><b>Show labels</b>, <b>Node Labels</b> and <b>Property Labels</b> are ticked when the editor opens, and put
      labels where the IRIs would be. Untick all three to see the IRIs; module 03 needs them.</p></div>
    <div class="panel"><h3>Show Facts</h3>
      <p>The editor's reasoner is an OWL 2 RL engine. It types individuals, closes transitive and symmetric properties, follows
      inverses and chains, merges under functional properties, and never reports a contradiction. The <b>Measured</b> block
      under each lesson says what an OWL 2 RL closure added, which is what Show Facts shows.</p></div>
    <div class="panel"><h3>Shapes and the Inference dropdown</h3>
      <p>Some lessons carry a companion shapes file; the button opens it in a second tab already selected. <b>Validate</b>
      runs it. The rule lesson in module 08 also sets <b>Inference</b> to <em>rules, iterated</em>, which the dropdown beside Shapes changes.</p></div>
    <div class="panel"><h3>What needs a terminal</h3>
      <p>Unsatisfiable classes, the inferred hierarchy, explanations and profile verdicts come from a description-logic
      reasoner, HermiT through ROBOT; the check identifiers from the Ontology Quality Suite. The SHACL numbers do not:
      they come from <code>shacl</code>, the same engine the editor runs, through its Python bindings. Each lesson's
      <em>Runs in</em> line says which, and the Measured block already has the result.</p></div>
  </div>

  <h4 class="subhead">The same measurements, from the command line</h4>
  <div class="code-wrap"><pre class="code">./scripts/setup-tools.ps1                  # fetches ROBOT, gist, gistBFO, gUFO and BFO into lib/
pip install -r scripts/requirements.txt     # rdflib, owlrl, shacl, ontology-quality-suite
python scripts/check_lessons.py             # every lesson, every instrument; about two minutes
python scripts/check_lessons.py o47 --show  # one lesson, with the inferred triples printed</pre></div>
</section>"""


def courses_html() -> str:
    return f"""
<section class="module ref" id="courses">
  <div class="module-head"><div class="module-num">Reference</div><h2>The three courses</h2>
  <p class="module-blurb">One dataset, one vocabulary, one editor, three courses. This one says what the terms mean; the
  <a href="{SPARQL_SITE}">SPARQL course</a> asks the questions; the <a href="{SHACL_SITE}">SHACL course</a> checks the data.
  Lesson ids link across: <a href="#o52">o52</a> reaches the same 186 pairs as the SPARQL course's
  <a href="{SPARQL_SITE}#m18">module 18</a> and the SHACL course's <a href="{SHACL_SITE}#s51">s51</a>.</p></div>
  <div class="tablewrap"><table><thead><tr><th>This course</th><th>The SPARQL course</th><th>The SHACL course</th></tr></thead><tbody>
  <tr><td><a href="#o29">o29</a> bs:founded left non-functional</td><td><a href="{SPARQL_SITE}#q61">q61</a> to q63, the disputed dates</td><td><a href="{SHACL_SITE}#s04">s04</a> exactly one founding year, as a shape</td></tr>
  <tr><td><a href="#o36">o36</a> the uneven genre tree</td><td><a href="{SPARQL_SITE}#q33">q33</a> every book of fiction however narrow the genre; <a href="{SPARQL_SITE}#q28">q28</a> the same lesson on the place hierarchy</td><td><a href="{SHACL_SITE}#s20">s20</a> the same chain in a shape, on places</td></tr>
  <tr><td><a href="#o38">o38</a> domain as an inference rule</td><td><a href="{SPARQL_SITE}#q143">q143</a> the inference nobody wanted</td><td><a href="{SHACL_SITE}#s59">s59</a> the inference that hides an error</td></tr>
  <tr><td><a href="#o43">o43</a> disjointness, as a query in the browser</td><td>module 13, debugging</td><td><a href="{SHACL_SITE}#s25">s25</a> sh:not</td></tr>
  <tr><td><a href="#o47">o47</a> cardinality merges before it complains</td><td><a href="{SPARQL_SITE}#q03">q03</a> which town is each shop in</td><td><a href="{SHACL_SITE}#s04">s04</a> the shape that was meant</td></tr>
  <tr><td><a href="#o48">o48</a> bs:within transitive</td><td>module 18, the 186 pairs from a reasoner</td><td><a href="{SHACL_SITE}#s50">s50</a>, <a href="{SHACL_SITE}#s51">s51</a> the same by a rule</td></tr>
  <tr><td><a href="#o49">o49</a> the ISBN as a key</td><td><a href="{SPARQL_SITE}#q15">q15</a> works with no ISBN</td><td><a href="{SHACL_SITE}#s39">s39</a> the check digit</td></tr>
  <tr><td><a href="#o52">o52</a> three routes to one inference</td><td>module 00 &sect;3, the reasoner and the path</td><td><a href="{SHACL_SITE}#s51">s51</a> to a fixpoint</td></tr>
  <tr><td><a href="#o67">o67</a> style shapes on the vocabulary</td><td>&mdash;</td><td><a href="{SHACL_SITE}#s16">s16</a> sh:uniqueLang, <a href="{SHACL_SITE}#s15">s15</a> sh:pattern</td></tr>
  <tr><td><a href="#o75">o75</a> the ten questions as the acceptance test</td><td>the whole course</td><td><a href="{SHACL_SITE}#s64">s64</a> the whole trail in one shapes graph</td></tr>
  </tbody></table></div>
  <p class="module-blurb">The <a href="{SEMOPS}">SemOps Manual</a> is the fourth text this course leans on: chapter 2 on definitions as territory,
  8 on the inner loop, 9 on the gate, 12 on evidence-based versions.</p>
</section>"""


def features_html() -> str:
    where = {}
    for l in CATALOGUE:
        for t in features.terms_in(l):
            where.setdefault(t, []).append(l)
    groups = []
    for group, items in features.TERMS:
        trs = []
        for term, key in items:
            label, url = specs.SECTIONS[key]
            refs = " ".join(f'<a href="#{l.oid}">{l.oid}</a>' for l in where.get(term, []))
            trs.append(f'<tr><td><code>{E(term)}</code></td><td><a href="{E(url)}">{E(label)}</a></td><td>{refs}</td></tr>')
        groups.append(f'<h4 class="subhead">{E(group)}</h4><div class="tablewrap"><table><thead><tr><th>Term</th><th>Defined in</th>'
                      f'<th>Lessons</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    return f"""
<section class="module ref" id="features">
  <div class="module-head"><div class="module-num">Reference</div><h2>Every term, and where it is shown</h2>
  <p class="module-blurb">Generated from the lesson models themselves, so it cannot disagree with them. The same index is
  <a href="{REPO}/blob/main/FEATURES.md">FEATURES.md</a> in the repository.</p></div>
  {"".join(groups)}
</section>"""


def standards_html() -> str:
    parts = []
    for heading, items in specs.READING_LIST:
        lis = "".join(f'<li><a href="{E(u)}">{E(t)}</a>. {E(d)}</li>' for u, t, d in items)
        parts.append(f'<h4 class="subhead">{E(heading)}</h4><ul class="reading">{lis}</ul>')
    return f"""
<section class="module ref" id="standards">
  <div class="module-head"><div class="module-num">Reference</div><h2>The sources</h2>
  <p class="module-blurb">Everything this course teaches is defined or argued somewhere, and each lesson's header names the two
  places that matter most for it. <code>python scripts/check_links.py</code> fetches every document and confirms each anchor
  still lands.</p></div>
  {"".join(parts)}
</section>"""


# ---------------------------------------------------------------- page

CSS = """
:root {
  --paper:#fbfaf7; --paper-2:#f2f1ec; --paper-3:#e7e6df; --ink:#191d24; --ink-2:#454c58; --ink-3:#6f7784;
  --rule:#d8d7cf; --route:#1f5f8b; --route-soft:#e4eef6; --bracken:#4a6b3d; --bracken-soft:#eaf0e6;
  --amber:#9a6b00; --amber-soft:#fbf1dc; --code-bg:#f4f3ee; --code-edge:#e2e1d8;
  --t-kw:#6b2f8a; --t-fn:#1d5c73; --t-var:#245a2a; --t-str:#8a4b1a; --t-iri:#4a5160; --t-pname:#2f4858; --t-com:#8b8f86; --t-num:#8a4b1a; --t-annot:#1f5f8b;
  --sans:"Atkinson Hyperlegible",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  --serif:"Newsreader",Georgia,"Times New Roman",serif;
  --mono:"JetBrains Mono",ui-monospace,"Cascadia Mono",Consolas,monospace;
  --maxw:74ch; color-scheme:light;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper:#14161a; --paper-2:#1b1e23; --paper-3:#24282e; --ink:#e8e6e0; --ink-2:#b9bcc2; --ink-3:#8b9099; --rule:#2f343b;
  --route:#6fb0e0; --route-soft:#15283a; --bracken:#8fbe79; --bracken-soft:#18241a; --amber:#d9a441; --amber-soft:#2a2113;
  --code-bg:#191c21; --code-edge:#2b3037;
  --t-kw:#c9a0e0; --t-fn:#7fc8e0; --t-var:#9ed5a3; --t-str:#e0b083; --t-iri:#9aa3b0; --t-pname:#a8c4d4; --t-com:#71776f; --t-num:#e0b083; --t-annot:#6fb0e0;
  color-scheme:dark; } }
:root[data-theme="dark"] {
  --paper:#14161a; --paper-2:#1b1e23; --paper-3:#24282e; --ink:#e8e6e0; --ink-2:#b9bcc2; --ink-3:#8b9099; --rule:#2f343b;
  --route:#6fb0e0; --route-soft:#15283a; --bracken:#8fbe79; --bracken-soft:#18241a; --amber:#d9a441; --amber-soft:#2a2113;
  --code-bg:#191c21; --code-edge:#2b3037;
  --t-kw:#c9a0e0; --t-fn:#7fc8e0; --t-var:#9ed5a3; --t-str:#e0b083; --t-iri:#9aa3b0; --t-pname:#a8c4d4; --t-com:#71776f; --t-num:#e0b083; --t-annot:#6fb0e0;
  color-scheme:dark; }
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:var(--sans); font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased; }
a { color:var(--route); text-decoration-thickness:1px; text-underline-offset:2px; }
code { font-family:var(--mono); font-size:.86em; }
.shell { display:grid; grid-template-columns:250px minmax(0,1fr); }
.rail { position:sticky; top:0; align-self:start; height:100vh; overflow-y:auto; padding:28px 20px 40px; border-right:1px solid var(--rule); background:var(--paper-2); }
.rail .brand { font-family:var(--serif); font-size:1.15rem; line-height:1.25; margin:0 0 4px; }
.rail .brand em { font-style:italic; color:var(--route); }
.rail .tagline { font-size:.78rem; color:var(--ink-3); margin:0 0 20px; }
.rail ol { list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:1px; }
.rail ol a { display:grid; grid-template-columns:26px 1fr auto; align-items:baseline; gap:6px; padding:6px 8px; border-radius:2px; color:var(--ink-2); text-decoration:none; font-size:.82rem; line-height:1.3; }
.rail ol a:hover { background:var(--paper-3); color:var(--ink); }
.rail .n { font-family:var(--mono); font-size:.72rem; color:var(--route); }
.rail .c { font-family:var(--mono); font-size:.68rem; color:var(--ink-3); }
.rail .railnote { font-size:.74rem; color:var(--ink-3); margin-top:22px; padding-top:14px; border-top:1px solid var(--rule); }
main { padding:0 0 100px; min-width:0; }
.hero { padding:44px 40px 34px; border-bottom:1px solid var(--rule); }
.hero .logo { width:64px; height:64px; display:block; margin:0 0 18px; }
.eyebrow { font-family:var(--mono); font-size:.7rem; letter-spacing:.14em; text-transform:uppercase; color:var(--route); margin:0 0 14px; }
h1 { font-family:var(--serif); font-weight:600; font-size:clamp(2.1rem,4.4vw,3.1rem); line-height:1.05; margin:0 0 16px; letter-spacing:-.015em; max-width:22ch; }
h1 small { display:block; font-size:.5em; color:var(--ink-3); font-weight:400; margin-top:6px; }
.standfirst { font-size:1.06rem; color:var(--ink-2); max-width:var(--maxw); margin:0 0 26px; }
.standfirst strong { color:var(--ink); font-weight:400; border-bottom:2px solid var(--route-soft); }
.facts { display:flex; flex-wrap:wrap; margin-top:8px; border-top:1px solid var(--rule); }
.fact { padding:14px 26px 12px 0; margin-right:26px; }
.fact b { display:block; font-family:var(--mono); font-size:1.45rem; font-weight:700; line-height:1; color:var(--ink); }
.fact span { font-size:.76rem; color:var(--ink-3); }
.intro { padding:34px 40px 10px; }
.intro h2, .subhead { font-family:var(--serif); font-weight:600; font-size:1.5rem; margin:34px 0 10px; letter-spacing:-.01em; }
h4.subhead { font-size:1.15rem; margin:30px 0 8px; }
.intro p { max-width:var(--maxw); color:var(--ink-2); }
.intro p strong { color:var(--ink); }
.grid2 { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:22px; margin:22px 0; }
.panel { border:1px solid var(--rule); border-radius:3px; padding:16px 18px; background:var(--paper-2); }
.panel h3 { font-family:var(--sans); font-size:.8rem; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-3); margin:0 0 10px; }
.panel p { margin:0 0 8px; font-size:.92rem; }
.tablewrap { overflow-x:auto; margin:14px 0 20px; border:1px solid var(--rule); border-radius:3px; }
.tablewrap.small { margin:8px 0 4px; }
table { border-collapse:collapse; width:100%; font-size:.86rem; }
th, td { text-align:left; padding:8px 12px; border-bottom:1px solid var(--rule); vertical-align:top; }
th { font-size:.7rem; letter-spacing:.08em; text-transform:uppercase; color:var(--ink-3); background:var(--paper-2); font-weight:700; }
tr:last-child td { border-bottom:none; }
table.measured th { width:18ch; text-transform:none; letter-spacing:0; font-size:.8rem; color:var(--ink-2); background:transparent; }
table.measured td { font-size:.86rem; color:var(--ink-2); }
ul.trip { margin:4px 0 0; padding-left:18px; }
ul.trip li { margin:0 0 2px; font-size:.82rem; }
.ok { color:var(--bracken); font-weight:700; } .no { color:#b3261e; font-weight:700; } .why { color:var(--ink-3); font-family:var(--mono); font-size:.74rem; }
.module { padding:0 40px; scroll-margin-top:12px; }
.module-head { padding:52px 0 8px; margin-top:34px; border-top:2px solid var(--ink); }
.module-num { font-family:var(--mono); font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; color:var(--route); }
.module-head h2 { font-family:var(--serif); font-weight:600; font-size:clamp(1.6rem,3vw,2.1rem); margin:6px 0 10px; letter-spacing:-.015em; }
.module-blurb { max-width:var(--maxw); color:var(--ink-2); margin:0 0 8px; }
details.standards { max-width:var(--maxw); font-size:.88rem; color:var(--ink-2); margin:8px 0 0; }
details.standards summary { cursor:pointer; color:var(--ink-3); }
details.standards ul { margin:6px 0 0; padding-left:18px; }
.lesson { padding:30px 0 26px; border-bottom:1px solid var(--rule); scroll-margin-top:12px; }
.lhead { display:flex; align-items:baseline; gap:12px; }
.lid { font-family:var(--mono); font-size:.78rem; font-weight:700; color:var(--paper); background:var(--route); padding:2px 7px; border-radius:2px; letter-spacing:.04em; }
.lhead h3 { font-family:var(--serif); font-weight:600; font-size:1.35rem; margin:0; letter-spacing:-.01em; }
.asks { max-width:var(--maxw); color:var(--ink-2); margin:8px 0 6px; font-size:1.02rem; }
.dataline { font-size:.82rem; color:var(--ink-3); margin:0 0 12px; }
.btns { display:flex; flex-wrap:wrap; gap:8px; margin:0 0 12px; }
.btn { font:inherit; font-size:.8rem; padding:6px 12px; border:1px solid var(--rule); border-radius:3px; background:var(--paper-2); color:var(--ink); cursor:pointer; text-decoration:none; }
.btn:hover { background:var(--paper-3); }
.btn.primary { background:var(--route); border-color:var(--route); color:#fff; }
.btn.primary:hover { filter:brightness(1.08); }
.btn.small { padding:3px 9px; font-size:.74rem; }
.btn.done { border-color:var(--bracken); color:var(--bracken); }
.code-wrap { overflow-x:auto; background:var(--code-bg); border:1px solid var(--code-edge); border-radius:3px; }
pre.code { margin:0; padding:15px 18px; font-family:var(--mono); font-size:.82rem; line-height:1.55; }
pre.code b { color:var(--t-kw); font-weight:700; }
.t-kw { color:var(--t-kw); font-weight:700; } .t-fn { color:var(--t-fn); } .t-var { color:var(--t-var); } .t-string { color:var(--t-str); }
.t-iri { color:var(--t-iri); } .t-pname { color:var(--t-pname); } .t-comment { color:var(--t-com); font-style:italic; } .t-num { color:var(--t-num); } .t-annot { color:var(--t-annot); font-weight:700; }
.mech { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1.15fr); gap:26px; margin-top:20px; align-items:start; }
.mech h4, .learn h4, .report h4, h4.q { font-family:var(--sans); font-size:.74rem; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-3); margin:0 0 8px; }
.mech-prose p { margin:0 0 10px; color:var(--ink-2); font-size:.95rem; }
pre.diagram { margin:0; padding:14px 16px; max-width:100%; background:var(--paper-2); border:1px solid var(--rule); border-radius:3px; font-family:var(--mono); font-size:.76rem; line-height:1.45; overflow-x:auto; color:var(--ink-2); }
.learn { margin-top:18px; max-width:var(--maxw); }
.learn ul { margin:0; padding-left:20px; color:var(--ink-2); font-size:.95rem; }
.learn li { margin-bottom:6px; }
.learn h4 { margin-top:14px; }
.learn p { color:var(--ink-2); font-size:.95rem; margin:0 0 8px; }
.report { margin-top:18px; }
.results-note { font-size:.82rem; color:var(--ink-3); margin:4px 0; display:block; }
tr.sev-violation td:first-child { color:#b3261e; font-weight:700; }
tr.sev-warning td:first-child { color:var(--amber); font-weight:700; }
tr.sev-info td:first-child { color:var(--bracken); font-weight:700; }
.report.err .results-note { color:#b3261e; font-family:var(--mono); }
.query { margin:10px 0; }
.qh { display:flex; justify-content:space-between; align-items:center; font-size:.86rem; color:var(--ink-2); margin:0 0 6px; }
.qh em { color:var(--ink-3); }
.specline { font-size:.78rem; color:var(--ink-3); margin:16px 0 0; }
ul.specs { display:inline; padding:0; margin:0; }
ul.specs li { display:inline; } ul.specs li + li::before { content:" · "; }
.ref .module-head { border-top-color:var(--ink-3); }
ul.reading { max-width:var(--maxw); color:var(--ink-2); font-size:.92rem; }
ul.reading li { margin-bottom:8px; }
footer { padding:40px; color:var(--ink-3); font-size:.8rem; border-top:1px solid var(--rule); margin-top:40px; }
@media (max-width: 900px) { .shell { grid-template-columns:1fr; } .rail { position:static; height:auto; border-right:none; border-bottom:1px solid var(--rule); }
  .mech { grid-template-columns:1fr; } .hero, .intro, .module, footer { padding-left:16px; padding-right:16px; } }
"""

JS = """
document.addEventListener('click', function (ev) {
  var b = ev.target.closest('button[data-copy]'); if (!b) return;
  var pre = document.getElementById('code-' + b.getAttribute('data-copy')); if (!pre) return;
  var head = pre.getAttribute('data-head') || '';
  var text = head + pre.textContent;
  function done() { var old = b.textContent; b.textContent = 'Copied'; b.classList.add('done'); setTimeout(function () { b.textContent = old; b.classList.remove('done'); }, 1400); }
  if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done); }
  else { var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); done(); } catch (e) {} document.body.removeChild(ta); }
});
"""


def main() -> None:
    results = {}
    for p in (BUILD / "results").glob("o*.json"):
        results[p.stem] = json.loads(p.read_text(encoding="utf-8"))
    by_module: dict[str, list] = {}
    for l in CATALOGUE:
        by_module.setdefault(l.module, []).append(l)
    for lessons in by_module.values():
        lessons.sort(key=lambda l: l.sort_key)
    n_terms = sum(len(items) for _, items in features.TERMS)
    n_measured = sum(1 for r in results.values() if r.get("hermit") or r.get("profile") or r.get("rl") or r.get("oqs") or r.get("shacl"))

    rail = ['<a href="#m00"><span class="n">00</span><span>The lab</span><span class="c"></span></a>']
    for module, lessons in by_module.items():
        num = module.split("-")[0]
        rail.append(f'<a href="#m{num}"><span class="n">{num}</span><span>{E(MODULE_INFO[module][0])}</span><span class="c">{lessons[0].oid}–{lessons[-1].oid}</span></a>')
    for anchor, label in (("courses", "The three courses"), ("features", "Every term"), ("standards", "The sources")):
        rail.append(f'<a href="#{anchor}"><span class="n">—</span><span>{label}</span><span class="c"></span></a>')

    modules = "".join(module_html(m, ls, results) for m, ls in by_module.items())
    heads = "".join(f'<script type="application/json" id="head-{l.oid}">{json.dumps(l.copy_text[:l.copy_text.index(chr(10)+chr(10))+2])}</script>' for l in CATALOGUE)

    logo = ""
    logo_path = ROOT / "assets" / "semantechs-logo.png"
    if logo_path.exists():
        logo = f'<img class="logo" alt="Semantechs" src="data:image/png;base64,{base64.b64encode(logo_path.read_bytes()).decode()}">'

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Bookshop Trail — Ontology</title>
<meta name="description" content="An ontology course on the Bookshop Trail: meaning, systematics, naming, definitions, design principles, and RDFS, SKOS and OWL 2 as one idea; every lesson measured.">
<link rel="icon" href="favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=Atkinson+Hyperlegible:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="shell">
<nav class="rail">
  <p class="brand">The Bookshop Trail <em>Ontology</em></p>
  <p class="tagline">A Semantechs teaching resource</p>
  <ol>{"".join(f"<li>{a}</li>" for a in rail)}</ol>
  <p class="railnote">The third of three: the <a href="{SPARQL_SITE}">SPARQL course</a> asks the Bookshop Trail questions, the
  <a href="{SHACL_SITE}">SHACL course</a> checks its data, and this one says what the terms mean.</p>
</nav>
<main>
<header class="hero">
  {logo}
  <p class="eyebrow">A Semantechs teaching resource</p>
  <h1>The Bookshop Trail <small>an ontology course</small></h1>
  <p class="standfirst">Seventy-six lessons that start with a word, a thing and the idea in between, and end with an OWL 2 DL
  vocabulary a reasoner has agreed with. <strong>Meaning, systematics, naming, definitions and design principles</strong> take
  half the course; RDFS, SKOS and OWL 2 take a quarter, as one idea at rising commitment; standing on gist, measuring quality,
  and living with change take the rest. Every lesson opens in the browser editor, and every claim a tool could check has been
  checked.</p>
  <div class="facts">
    <div class="fact"><b>{len(CATALOGUE)}</b><span>lessons</span></div>
    <div class="fact"><b>{len(by_module)}</b><span>modules</span></div>
    <div class="fact"><b>{n_measured}</b><span>measured by a reasoner, a checker or a validator</span></div>
    <div class="fact"><b>{n_terms}</b><span>terms shown</span></div>
    <div class="fact"><b>1</b><span>editor, in the browser</span></div>
  </div>
</header>

<section class="intro">
  <h2>Start here</h2>
  <p>Read <a href="{REPO}/blob/main/data/the-brief.md">the brief</a>: a page from the Trail's committee, written loosely on
  purpose. Then press <strong>Open in the editor</strong> on <a href="#o01">o01</a>. The file arrives in the editor at
  <a href="{EDITOR_BASE}">semantechs.co.uk/turtle-editor-viewer</a>, the graph view draws it, and the header in the file is the
  lesson. Read the header before you look at the graph.</p>
  <p>Each lesson decides one thing about the Bookshop Trail's vocabulary and says why. The <strong>Measured</strong> block under
  it is what the tools found when the file was put through them: the OWL 2 profile checker, HermiT, an OWL 2 RL closure like the
  editor's own reasoner, the editor's own SHACL engine, the Ontology Quality Suite, the OQuaRE metrics, and the lesson's own queries. Where a lesson
  seeds a fault, the block shows the tool finding it.</p>
  <p>The triangle from <a href="#o01">o01</a> runs through the whole course. Each lesson names the corner it works on: the
  <em>symbol</em> (naming), the <em>thought</em> (definitions, scope, agreement) or the <em>referent</em> (kinds, roles, sets,
  axioms). RDFS, SKOS and OWL 2 arrive in modules 06 and 07 as one idea at rising commitment, and the lessons before them are
  what makes the commitment worth making.</p>
  <h2>A suggested order</h2>
  <p>00 → 01 → <strong>02 in full</strong> → 03 (o15, o17, o19) → <strong>04 in full</strong> → <strong>05 in full</strong> →
  06 (o35, o36, o38, o40) → 07 (o43, o46, o47, o48) → 08 (o52, o56) → 09 (o59, o61) → 10 (o66, o68) → 11 (o70, o71) → 12.
  Modules 02, 04 and 05 are where the thinking is; the rest is what the thinking looks like written down.</p>
</section>

{lab_html()}
{modules}
{courses_html()}
{features_html()}
{standards_html()}

<footer>
  <p>The Bookshop Trail, an ontology course. MIT licence; copyright © 2026 Peter Winstanley. The Semantechs name and mark are
  excluded from the licence. Everything except the geography is fiction. Source and files: <a href="{REPO}">{REPO}</a>.
  gist, gistBFO and gistUFO are Semantic Arts', CC-BY-4.0; gUFO is NEMO's, CC-BY-4.0; BFO 2020 is the BFO Consortium's.</p>
</footer>
</main>
</div>
{heads}
<script>
(function () {{
  document.querySelectorAll('script[id^="head-"]').forEach(function (s) {{
    var pre = document.getElementById('code-' + s.id.slice(5)); if (pre) pre.setAttribute('data-head', JSON.parse(s.textContent));
  }});
}})();
{JS}
</script>
</body>
</html>"""
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote docs/index.html ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
