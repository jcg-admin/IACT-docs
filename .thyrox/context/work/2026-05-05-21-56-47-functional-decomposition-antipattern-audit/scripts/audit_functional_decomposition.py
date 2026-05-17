#!/usr/bin/env python3
"""Functional Decomposition (Brown 1998) audit — config-driven.

The script contains NO hardcoded vocabulary. All heuristics
(forbidden prefixes, pattern suffixes, regexes, thresholds, target
glob, exclusions) are loaded from a YAML config file.

Usage:
    python3 audit_functional_decomposition.py \\
        --root <repo-root> \\
        --out <output-json> \\
        --config <config-yml> \\
        [--glob <override-glob>]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "PyYAML is required: pip install pyyaml\n"
    )
    sys.exit(2)


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def extract_plantuml_blocks(text: str) -> list[str]:
    return re.findall(r"@startuml(.*?)@enduml", text, re.S)


def parse_class_block(uml: str) -> dict[str, Any]:
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
        m = re.match(r"^[+\-#~]\s*(\{static\}\s*)?(.+)$", line)
        if not m:
            continue
        is_static = bool(m.group(1))
        rest = m.group(2).strip()
        if "(" in rest:
            name = rest.split("(", 1)[0].strip()
            methods.append(name)
            if is_static:
                static_methods.append(name)
        else:
            name = rest.split(":", 1)[0].strip()
            attrs.append(name)
    return {
        "class_name": class_name, "methods": methods, "attrs": attrs,
        "static_methods": static_methods,
        "has_inheritance": has_inheritance,
        "has_relations": has_relations,
        "class_count": len(classes),
    }


def kebab_to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("-"))


def detect_pattern_declaration(text: str, decls: list[dict]) -> str | None:
    for entry in decls:
        if re.search(entry["regex"], text, re.I):
            return entry["label"]
    return None


def detect_pattern_suffix(class_name: str | None,
                          suffixes: list[str]) -> str | None:
    if not class_name:
        return None
    for suf in suffixes:
        if class_name.endswith(suf):
            return suf
    return None


def evaluate_c1(class_name: str | None,
                pattern_suffix: str | None,
                forbidden: list[str]) -> str:
    if not class_name:
        return "N/A"
    lower = class_name.lower()
    for verb in forbidden:
        if lower.startswith(verb.lower()):
            return "REVIEW" if pattern_suffix else "FAIL"
    return "PASS"


def evaluate_c2(parsed: dict, suspect: list[str],
                thresholds: dict) -> tuple[str, str]:
    methods, attrs = parsed["methods"], parsed["attrs"]
    if len(methods) >= thresholds["min_methods_for_pass"]:
        return "PASS", f"{len(methods)} metodos"
    if (len(methods) == 1
            and len(attrs) >= thresholds["min_attrs_when_one_method"]):
        return "PASS", (
            f"1 metodo + {len(attrs)} atributos (entity con state)"
        )
    suspect_lower = {s.lower() for s in suspect}
    if (len(methods) == 1 and methods[0].lower() in suspect_lower
            and len(attrs) == 0):
        return "REVIEW", f"1 metodo sospechoso ({methods[0]}) sin state"
    if len(methods) == 1:
        return "REVIEW", (
            f"Solo 1 metodo: '{methods[0]}'"
        )
    if (len(methods) == 0
            and len(attrs) >= thresholds["min_attrs_when_zero_methods"]):
        return "PASS", "Sin metodos (entity con solo atributos)"
    return "REVIEW", "Sin metodos ni atributos significativos"


def evaluate_c3(parsed: dict, pattern_decl: str | None) -> tuple[str, str]:
    if len(parsed["attrs"]) >= 1:
        return "PASS", f"{len(parsed['attrs'])} atributos"
    if pattern_decl and (
        "Strategy" in pattern_decl or "Pure Function" in pattern_decl
    ):
        return "PASS", f"Stateless legitimo ({pattern_decl})"
    if len(parsed["methods"]) >= 1:
        return "REVIEW", "Sin atributos pero con metodos (stateless)"
    return "REVIEW", "Stateless sin declaracion de Strategy/Pure"


def evaluate_c4(parsed: dict) -> tuple[str, str]:
    if parsed["has_inheritance"] or parsed["has_relations"]:
        return "PASS", "Usa relaciones OOP"
    return "N/A", "No aplica (entity simple)"


def evaluate_c5(pattern_suffix: str | None,
                pattern_decl: str | None) -> tuple[str, str]:
    if pattern_suffix and pattern_decl:
        return "PASS", f"Declara pattern: {pattern_decl}"
    if pattern_suffix and not pattern_decl:
        return "REVIEW", (
            f"Sufijo {pattern_suffix} sin declaracion explicita de pattern"
        )
    if not pattern_suffix and pattern_decl:
        return "PASS", f"Declara pattern: {pattern_decl}"
    return "N/A", "Sin sufijo de pattern"


def aggregate_verdict(verdicts: dict[str, str]) -> str:
    values = list(verdicts.values())
    if any(v == "FAIL" for v in values):
        return "ANTIPATRON"
    if any(v == "REVIEW" for v in values):
        return "REVISION"
    return "OK"


def audit_file(path: Path, repo_root: Path,
               cfg: dict[str, Any]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    blocks = extract_plantuml_blocks(text)
    uml = "\n".join(blocks) if blocks else ""
    parsed = parse_class_block(uml)
    name = path.stem
    pascal = parsed["class_name"] or kebab_to_pascal(name)

    pattern_suffix = detect_pattern_suffix(pascal, cfg["pattern_suffixes"])
    pattern_decl = detect_pattern_declaration(
        text, cfg["c5_pattern_declarations"]
    )

    c1 = evaluate_c1(pascal, pattern_suffix, cfg["c1_forbidden_verb_prefixes"])
    c2, c2_evi = evaluate_c2(
        parsed, cfg["c2_suspect_single_methods"], cfg["c2_thresholds"]
    )
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
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument(
        "--glob", default=None,
        help="override target.glob from config",
    )
    args = ap.parse_args()

    cfg = load_config(args.config)
    glob = args.glob or cfg["target"]["glob"]
    skip = set(cfg["target"].get("exclude_basenames", []))

    files = sorted(args.root.glob(glob))
    files = [f for f in files if f.name not in skip]

    findings = [audit_file(f, args.root, cfg) for f in files]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"findings": findings}, indent=2, sort_keys=True,
                   ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    counts = {"OK": 0, "REVISION": 0, "ANTIPATRON": 0}
    for f in findings:
        counts[f["vereditcto_global"]] += 1
    print(
        f"Total: {len(findings)}  "
        f"OK: {counts['OK']}  "
        f"REVISION: {counts['REVISION']}  "
        f"ANTIPATRON: {counts['ANTIPATRON']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
