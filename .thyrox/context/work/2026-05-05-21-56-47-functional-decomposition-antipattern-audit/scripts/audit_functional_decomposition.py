#!/usr/bin/env python3
"""
Functional Decomposition Antipattern Audit (William Brown 1998).

Audits source/arquitectura-tecnica/domain-model/*.rst against criteria
C-1..C-5 documented in wp-state.md.

Usage:
    python3 audit_functional_decomposition.py \\
        --root <repo-root> \\
        --out <output-json>

Output: JSON with one finding per file:
    {
      "findings": [
        {
          "file": "...", "name": "...", "pascal": "...",
          "evidence": {...},
          "verdicts": {"C-1": "PASS|FAIL|N/A", ...},
          "vereditcto_global": "OK|REVISION|ANTIPATRON"
        },
        ...
      ]
    }
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# C-1: verbos prohibidos como prefijo (lowercase comparison)
FORBIDDEN_VERB_PREFIXES = (
    "calcular", "procesar", "validar", "ejecutar", "generar",
    "realizar", "crear", "obtener", "computar",
    "calculate", "process", "validate", "execute", "generate",
    "compute", "get", "make", "do", "run", "handle",
)

# Sufijos de pattern legitimos (no penalizar C-1)
PATTERN_SUFFIXES = (
    "Repository", "Repo", "Strategy", "Policy", "Specification",
    "Aggregator", "Generator", "Validator", "Guard", "Resolver",
    "Calculator", "Service", "Factory", "Builder", "Adapter",
)

# C-2: metodos "funcion-like" sospechosos cuando son unicos
SUSPECT_SINGLE_METHODS = {
    "execute", "process", "run", "handle", "apply",
    "ejecutar", "procesar", "correr", "compute", "calculate",
}

# C-5: declaraciones explicitas de pattern (regex case-insensitive)
PATTERN_DECLARATIONS = [
    (re.compile(r"\brepository\s+pattern\b", re.I), "Repository pattern"),
    (re.compile(r"\bstrategy\s+pattern\b", re.I), "Strategy pattern"),
    (re.compile(r"\bspecification\s+pattern\b", re.I), "Specification pattern"),
    (re.compile(r"\bdomain\s+service\b", re.I), "Domain Service"),
    (re.compile(r"\bvalue\s+object\b", re.I), "Value Object"),
    (re.compile(r"\baggregate\s+root\b", re.I), "Aggregate Root"),
    (re.compile(r"\bfactory\s+pattern\b", re.I), "Factory pattern"),
    (re.compile(r"\bpolicy\s+pattern\b", re.I), "Policy pattern"),
    (re.compile(r"\bguard\s+pattern\b", re.I), "Guard pattern"),
    (re.compile(r"\bpure\s+function\b", re.I), "Pure Function"),
    (re.compile(r"\bstateless\b.*\bstrategy\b", re.I), "Stateless Strategy"),
]


def kebab_to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("-"))


def extract_plantuml_blocks(text: str) -> list[str]:
    """Extract @startuml..@enduml blocks."""
    return re.findall(r"@startuml(.*?)@enduml", text, re.S)


def parse_class_block(uml: str) -> dict:
    """Parse first `class Name { ... }` block found.

    Returns dict with: class_name, methods (list[str]), attrs (list[str]),
    static_methods (list[str]), has_inheritance, has_relations, class_count.
    """
    classes = re.findall(
        r"class\s+(\w+)\s*(?:<<[^>]+>>\s*)?\{([^}]*)\}", uml, re.S
    )
    has_inheritance = bool(re.search(r"<\|--", uml))
    has_relations = bool(re.search(r"(o-->|\*-->|-->|\.\.>|--)", uml))
    if not classes:
        return {
            "class_name": None, "methods": [], "attrs": [],
            "static_methods": [], "has_inheritance": has_inheritance,
            "has_relations": has_relations, "class_count": 0,
        }
    class_name, body = classes[0]
    methods, attrs, static_methods = [], [], []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith(("--", "==", "..")):
            continue
        # eliminar prefijos de visibilidad
        m = re.match(r"^[+\-#~]\s*(\{static\}\s*)?(.+)$", line)
        if not m:
            continue
        is_static = bool(m.group(1))
        rest = m.group(2).strip()
        if "(" in rest:  # method
            name = rest.split("(", 1)[0].strip()
            methods.append(name)
            if is_static:
                static_methods.append(name)
        else:  # attribute
            name = rest.split(":", 1)[0].strip()
            attrs.append(name)
    return {
        "class_name": class_name, "methods": methods, "attrs": attrs,
        "static_methods": static_methods,
        "has_inheritance": has_inheritance,
        "has_relations": has_relations,
        "class_count": len(classes),
    }


def detect_pattern_declaration(text: str) -> str | None:
    for regex, label in PATTERN_DECLARATIONS:
        if regex.search(text):
            return label
    return None


def detect_pattern_suffix(class_name: str | None) -> str | None:
    if not class_name:
        return None
    for suf in PATTERN_SUFFIXES:
        if class_name.endswith(suf):
            return suf
    return None


def evaluate_c1(class_name: str | None, pattern_suffix: str | None) -> str:
    if not class_name:
        return "N/A"
    lower = class_name.lower()
    for verb in FORBIDDEN_VERB_PREFIXES:
        if lower.startswith(verb):
            # excepcion: si tambien tiene sufijo de pattern, REVISION
            return "REVISION" if pattern_suffix else "FAIL"
    return "PASS"


def evaluate_c2(parsed: dict) -> tuple[str, str]:
    methods, attrs = parsed["methods"], parsed["attrs"]
    if len(methods) >= 2:
        return "PASS", f"{len(methods)} metodos"
    if len(methods) == 1 and len(attrs) >= 3:
        return "PASS", f"1 metodo + {len(attrs)} atributos (entity con state)"
    if len(methods) == 1 and methods[0].lower() in SUSPECT_SINGLE_METHODS \
            and len(attrs) == 0:
        return "REVISION", f"1 metodo sospechoso ({methods[0]}) sin state"
    if len(methods) == 1:
        return "REVISION", f"1 metodo ({methods[0]}), {len(attrs)} atributos"
    if len(methods) == 0 and len(attrs) >= 1:
        return "PASS", "Sin metodos (entity con solo atributos)"
    return "REVISION", "Sin metodos ni atributos significativos"


def evaluate_c3(parsed: dict, pattern_decl: str | None) -> tuple[str, str]:
    if len(parsed["attrs"]) >= 1:
        return "PASS", f"{len(parsed['attrs'])} atributos"
    if pattern_decl and ("Strategy" in pattern_decl
                         or "Pure Function" in pattern_decl):
        return "PASS", f"Stateless legitimo ({pattern_decl})"
    return "REVISION", "Stateless sin declaracion de Strategy/Pure"


def evaluate_c4(parsed: dict) -> tuple[str, str]:
    if parsed["has_inheritance"] or parsed["has_relations"]:
        return "PASS", "Usa relaciones OOP"
    return "N/A", "No aplica (entity simple)"


def evaluate_c5(pattern_suffix: str | None,
                pattern_decl: str | None) -> tuple[str, str]:
    if pattern_suffix and pattern_decl:
        return "PASS", f"Declara pattern: {pattern_decl}"
    if pattern_suffix and not pattern_decl:
        return "REVISION", \
            f"Sufijo {pattern_suffix} sin declaracion explicita de pattern"
    if not pattern_suffix and pattern_decl:
        return "PASS", f"Declara pattern: {pattern_decl}"
    return "N/A", "Sin sufijo de pattern"


def aggregate_verdict(verdicts: dict[str, str]) -> str:
    values = list(verdicts.values())
    if any(v == "FAIL" for v in values):
        return "ANTIPATRON"
    if any(v == "REVISION" for v in values):
        return "REVISION"
    return "OK"


def audit_file(path: Path, repo_root: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    blocks = extract_plantuml_blocks(text)
    uml = "\n".join(blocks) if blocks else ""
    parsed = parse_class_block(uml)
    name = path.stem
    pascal = parsed["class_name"] or kebab_to_pascal(name)

    pattern_suffix = detect_pattern_suffix(pascal)
    pattern_decl = detect_pattern_declaration(text)

    c1 = evaluate_c1(pascal, pattern_suffix)
    c2, c2_evi = evaluate_c2(parsed)
    c3, c3_evi = evaluate_c3(parsed, pattern_decl)
    c4, c4_evi = evaluate_c4(parsed)
    c5, c5_evi = evaluate_c5(pattern_suffix, pattern_decl)

    verdicts = {"C-1": c1, "C-2": c2, "C-3": c3, "C-4": c4, "C-5": c5}
    return {
        "file": str(path.relative_to(repo_root)),
        "name": name,
        "pascal": pascal,
        "evidence": {
            "class_count": parsed["class_count"],
            "method_count": len(parsed["methods"]),
            "methods_sample": parsed["methods"][:6],
            "attr_count": len(parsed["attrs"]),
            "attrs_sample": parsed["attrs"][:6],
            "has_inheritance": parsed["has_inheritance"],
            "has_relations": parsed["has_relations"],
            "pattern_suffix": pattern_suffix,
            "C-2": c2_evi, "C-3": c3_evi,
            "C-4": c4_evi, "C-5": c5_evi,
        },
        "verdicts": verdicts,
        "vereditcto_global": aggregate_verdict(verdicts),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument(
        "--glob", default="source/arquitectura-tecnica/domain-model/*.rst",
    )
    args = ap.parse_args()

    files = sorted(args.root.glob(args.glob))
    skip = {"index.rst", "overview.rst"}
    files = [f for f in files if f.name not in skip]

    findings = [audit_file(f, args.root) for f in files]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"findings": findings}, indent=2, sort_keys=True,
                   ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    counts = {"OK": 0, "REVISION": 0, "ANTIPATRON": 0}
    for f in findings:
        counts[f["vereditcto_global"]] += 1
    print(f"Total: {len(findings)}  "
          f"OK: {counts['OK']}  "
          f"REVISION: {counts['REVISION']}  "
          f"ANTIPATRON: {counts['ANTIPATRON']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
