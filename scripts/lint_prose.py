# -*- coding: utf-8 -*-
"""Flag wording in the lesson texts that does not belong in this course.

    python scripts/lint_prose.py            # every lesson, and the module blurbs
    python scripts/lint_prose.py o20 o44    # just these
    python scripts/lint_prose.py --md       # the README and the lab as well

The course's prose is meant to read like the SPARQL and SHACL courses': short
declarative sentences, concrete nouns, few adverbs, no em dashes in file text,
no rhetorical closers, no triplets for rhythm. This lists the words and turns
of phrase that drift from that, with the lesson and field they occur in, so
they can be rewritten. It is advisory; nothing here fails a build.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import catalogue  # noqa: E402,F401
from ontocat import CATALOGUE, MODULE_INFO  # noqa: E402

WORDS = [
    "honest", "genuinely", "plainly", "quietly", "crucially", "robust", "nuanced", "seamless", "seamlessly",
    "delve", "leverage", "elegant", "elegantly", "simply", "merely", "essentially", "arguably", "importantly",
    "interestingly", "notably", "of course", "needless to say", "it turns out", "the beauty of", "the point is",
    "not just", "not merely", "not only", "at its core", "in essence", "in other words", "in a nutshell",
    "let's", "we'll", "you'll", "it's worth", "worth noting", "worth knowing", "in earnest", "dangerous",
    "surprise", "confident", "the tell", "tell,", "a testament", "underscores", "underscore the", "highlights the",
    "navigate", "landscape", "realm", "tapestry", "multifaceted", "pivotal", "crucial", "vital", "key takeaway",
    "game-changer", "unlock", "empower", "streamline", "foster", "ensure that", "it is important to",
    "in today's", "ever-evolving", "cutting-edge", "state-of-the-art", "comprehensive", "holistic",
    "furthermore", "moreover", "additionally", "in conclusion", "to summarize", "to sum up", "overall,",
    "ultimately,", "at the end of the day", "that being said", "with that said", "as we have seen",
    "as mentioned", "aforementioned", "utilize", "utilise", "facilitate", "enhance", "harness",
]
PATTERNS = [
    (re.compile("—"), "em dash (use , or ; or -- in file text)"),
    (re.compile("– "), "spaced en dash"),
    (re.compile(r"\bThat is what\b"), "rhetorical closer"),
    (re.compile(r"\bThat is the\b [a-z]+ (of|about)\b"), "rhetorical closer"),
    (re.compile(r"\bnot an? \w+[,;.] (it|but) (is|a)\b", re.I), "'not X, it is Y' framing"),
    (re.compile(r"\bnot (just|only|merely) \w+ but\b", re.I), "'not only X but Y'"),
    (re.compile(r"\b(\w+), (\w+),? and (\w+)\b\.$"), "sentence-final triplet"),
    (re.compile(r"!\s"), "exclamation"),
    (re.compile(r"\bHere's\b|\bhere's the thing\b", re.I), "chatty opener"),
    (re.compile(r"\b(Firstly|Secondly|Thirdly|Lastly)\b"), "enumerating adverb"),
    (re.compile(r":\s*$", re.M), "colon at end of a paragraph"),
    (re.compile(r"\bIt'?s (also )?(worth|important)\b", re.I), "it is worth/important"),
    (re.compile(r"\bthis (is|was) (a|the) (key|central|critical) (point|insight|idea)\b", re.I), "signposting"),
]


def check(oid: str, field: str, text: str, out: list) -> None:
    low = text.lower()
    for w in WORDS:
        for m in re.finditer(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
            start = max(0, m.start() - 40)
            out.append((oid, field, w, text[start:m.end() + 40].replace(chr(10), " ")))
    for pat, label in PATTERNS:
        if field in ("diagram", "body") and label.startswith("colon"):
            continue
        for m in pat.finditer(text):
            start = max(0, m.start() - 40)
            out.append((oid, field, label, text[start:m.end() + 40].replace(chr(10), " ")))


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    wanted = {a.lower() for a in args}
    out: list = []
    for l in CATALOGUE:
        if wanted and l.oid not in wanted:
            continue
        check(l.oid, "title", l.title, out)
        check(l.oid, "decides", l.decides, out)
        check(l.oid, "why", l.why, out)
        check(l.oid, "diagram", l.diagram, out)
        check(l.oid, "notes", l.notes, out)
        check(l.oid, "tryit", l.tryit, out)
        for i, item in enumerate(l.learn):
            check(l.oid, f"learn[{i}]", item, out)
        check(l.oid, "body", l.body, out)
    if not wanted:
        for module, (title, blurb) in MODULE_INFO.items():
            check(module, "blurb", blurb, out)
    if "--md" in sys.argv:
        for name in ("README.md", "NOTICE.md", "lessons/00-the-lab/README.md", "data/the-brief.md"):
            p = ROOT / name
            if p.exists():
                check(name, "text", p.read_text(encoding="utf-8"), out)
    for oid, field, what, ctx in out:
        print(f"{oid:24} {field:9} {what:28} ...{ctx}...")
    print(f"\n{len(out)} flags")
    return 0


if __name__ == "__main__":
    main()
