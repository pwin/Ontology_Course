# -*- coding: utf-8 -*-
"""Write lessons/**/*.ttl and the module READMEs from the catalogue.

    python scripts/build_lessons.py

Run check_lessons.py first if you want the MEASURED line in each header to be
current: it is read from build/measured.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import catalogue  # noqa: E402,F401
import specs  # noqa: E402
from ontocat import CATALOGUE, MODULE_INFO, LESSONS, SITE, SPARQL_SITE, SHACL_SITE  # noqa: E402

BUILD = ROOT / "build"


def module_readme(module: str, lessons: list) -> str:
    title, blurb = MODULE_INFO[module]
    num = module.split("-")[0]
    lines = [f"# Module {num} · {title}", "", blurb, ""]
    lines.append("Each `.ttl` file carries its own explanation: what it decides, why, a diagram "
                 "of the idea, and what to take away. Read the header, then follow the Open in the "
                 "editor link at its foot, which puts the file in the editor; the graph view draws it and the SPARQL "
                 "panel can query it. Where a lesson has been reasoned over or measured, the "
                 "MEASURED line says what the tools found.")
    lines.append("")
    lines.append(f"The same lessons, with their measurements laid out in full, are in the "
                 f"[course document]({SITE}#m{num}).")
    lines.append("")
    lines.append("**Sources.** What this module is defined by, or argued from:")
    lines.append("")
    for label, url in specs.for_module(module):
        lines.append(f"- [{label}]({url})")
    lines.append("")
    lines.append("| Lesson | Decides | Corner |")
    lines.append("|---|---|---|")
    for l in lessons:
        lines.append(f"| [{l.oid} {l.title}]({l.filename}) | {l.decides} | {l.corner or ''} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    measured_path = BUILD / "measured.json"
    measured = json.loads(measured_path.read_text(encoding="utf-8")) if measured_path.exists() else {}
    for l in CATALOGUE:
        l.measured = measured.get(l.oid, "")

    for folder in LESSONS.iterdir() if LESSONS.exists() else []:
        if folder.is_dir():
            for f in folder.glob("*.ttl"):
                f.unlink()

    by_module: dict[str, list] = {}
    for l in CATALOGUE:
        by_module.setdefault(l.module, []).append(l)
    count = companions = 0
    for module, lessons in by_module.items():
        lessons.sort(key=lambda l: l.sort_key)
        folder = LESSONS / module
        folder.mkdir(parents=True, exist_ok=True)
        for l in lessons:
            l.path.write_text(l.text(), encoding="utf-8", newline="\n")
            for name, text in l.companions.items():
                (folder / name).write_text(text.strip() + "\n", encoding="utf-8", newline="\n")
                companions += 1
            count += 1
        (folder / "README.md").write_text(module_readme(module, lessons), encoding="utf-8", newline="\n")
    print(f"wrote {count} lessons and {companions} companion files in {len(by_module)} modules")


if __name__ == "__main__":
    main()
