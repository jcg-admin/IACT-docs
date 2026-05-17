#!/usr/bin/env python3
"""Generate aggregated markdown report from audit-data.json."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, type=Path)
    args = ap.parse_args()

    data = json.loads(args.data.read_text(encoding="utf-8"))
    findings = data["findings"]

    globals_count = Counter(f["vereditcto_global"] for f in findings)
    per_criterion: dict[str, Counter] = {
        c: Counter() for c in ("C-1", "C-2", "C-3", "C-4", "C-5")
    }
    for f in findings:
        for c, v in f["verdicts"].items():
            per_criterion[c][v] += 1

    pattern_counter = Counter(
        f["evidence"]["pattern_suffix"] or "(none)" for f in findings
    )

    print("# Audit Summary — auto-generated\n")
    print(f"Total auditados: **{len(findings)}**\n")
    print("## Veredictos globales\n")
    for k in ("OK", "REVISION", "ANTIPATRON"):
        print(f"- {k}: {globals_count.get(k, 0)}")
    print("\n## Por criterio\n")
    print("| Crit | PASS | REVISION | FAIL | N/A |")
    print("|---|---|---|---|---|")
    for c in ("C-1", "C-2", "C-3", "C-4", "C-5"):
        row = per_criterion[c]
        print(f"| {c} | {row['PASS']} | {row['REVISION']} | "
              f"{row['FAIL']} | {row['N/A']} |")

    print("\n## Distribucion por sufijo de pattern\n")
    for suf, n in pattern_counter.most_common():
        print(f"- {suf}: {n}")

    print("\n## Files no-OK\n")
    for f in findings:
        if f["vereditcto_global"] != "OK":
            print(f"- **{f['vereditcto_global']}** — `{f['file']}`")
            for c, v in f["verdicts"].items():
                if v not in ("PASS", "N/A"):
                    print(f"  - {c}: {v}  ({f['evidence'].get(c, '')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
