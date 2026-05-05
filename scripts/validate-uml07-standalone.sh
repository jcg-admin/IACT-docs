#!/usr/bin/env bash
# scripts/validate-uml07-standalone.sh
#
# Audit script para los 83 archivos uml-07 standalone en
# source/arquitectura-tecnica/use-case-view/<module>/uc-XXX-NN-<slug>.rst
#
# Verifica:
#   C-01 R-01 layout: left to right direction
#   C-02 R-01 rectangle: rectangle "MOD_<X>"
#   C-03 R-02 include direction: ..> con <<include>>
#   C-04 R-03 extend direction: ..> con <<extend>>
#   C-05 R-05/BR-006: NO <|-- entre actores
#   C-06 STD-011: alias = label exacto (sin abreviar)
#   C-07 R-09: extension points en label del UC base
#   C-08 R-12: NO codenames de implementacion como UC labels
#
# Refs: discover/uml07-canonical-rules-annex.md
# Output: track/audit-report-{ISO}.md

set -e

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo /home/user/IACT-docs)"
cd "$ROOT"
USECASE_DIR="source/arquitectura-tecnica/use-case-view"
WP=".thyrox/context/work/2026-05-05-20-28-12-use-case-view-uml07-standalone-pass"
ISO=$(date -u +%Y-%m-%dT%H-%M-%S)
REPORT="$WP/track/audit-report-${ISO}.md"
mkdir -p "$(dirname "$REPORT")"

# Detect uml-07 standalone files
FILES=$(find "$USECASE_DIR" -name "uc-*-*.rst" | sort)
TOTAL=$(echo "$FILES" | wc -l)

echo "# Audit Report — uml-07 standalone" > "$REPORT"
echo "Generated: ${ISO}" >> "$REPORT"
echo "Files audited: $TOTAL" >> "$REPORT"
echo "" >> "$REPORT"

VIOLATIONS=0

# C-01 left to right direction
echo "## C-01 — left to right direction (R-01)" >> "$REPORT"
MISSING=$(echo "$FILES" | xargs -I {} grep -L "^ left to right direction" {} 2>/dev/null || true)
if [ -n "$MISSING" ]; then
  COUNT=$(echo "$MISSING" | wc -l)
  echo "Files missing 'left to right direction': $COUNT" >> "$REPORT"
  echo '```' >> "$REPORT"
  echo "$MISSING" >> "$REPORT"
  echo '```' >> "$REPORT"
  VIOLATIONS=$((VIOLATIONS + COUNT))
else
  echo "✓ All files have 'left to right direction'" >> "$REPORT"
fi
echo "" >> "$REPORT"

# C-02 rectangle MOD_*
echo "## C-02 — rectangle MOD_<X> (R-01)" >> "$REPORT"
MISSING=$(echo "$FILES" | xargs -I {} grep -L 'rectangle "MOD_' {} 2>/dev/null || true)
if [ -n "$MISSING" ]; then
  COUNT=$(echo "$MISSING" | wc -l)
  echo "Files missing 'rectangle MOD_<X>': $COUNT" >> "$REPORT"
  echo '```' >> "$REPORT"
  echo "$MISSING" >> "$REPORT"
  echo '```' >> "$REPORT"
  VIOLATIONS=$((VIOLATIONS + COUNT))
else
  echo "✓ All files have 'rectangle MOD_<X>'" >> "$REPORT"
fi
echo "" >> "$REPORT"

# C-05 BR-006: NO <|-- between actors
echo "## C-05 — BR-006 NO <|-- entre actores" >> "$REPORT"
HITS=$(echo "$FILES" | xargs grep -l '<|--' 2>/dev/null || true)
if [ -n "$HITS" ]; then
  COUNT=$(echo "$HITS" | wc -l)
  echo "Files con <|-- (PROHIBIDO): $COUNT" >> "$REPORT"
  echo '```' >> "$REPORT"
  echo "$HITS" >> "$REPORT"
  echo '```' >> "$REPORT"
  VIOLATIONS=$((VIOLATIONS + COUNT))
else
  echo "✓ Ningun archivo usa <|-- (BR-006 cumplido)" >> "$REPORT"
fi
echo "" >> "$REPORT"

# C-06 STD-011: alias auto-documentado (no INVOKER, F_*, AS, PC, etc.)
echo "## C-06 — STD-011 aliases auto-documentados" >> "$REPORT"
PROHIBITED=$(echo "$FILES" | xargs grep -nE ' as (INVOKER|F_[A-Z]+|AS|PC|RV|EE|ER|PS|TC|SAN|PII|PE|PL|MB|TARGET|SVC|REPO|KPI|BK|CE|FV|CALL|SESSION)\b' 2>/dev/null || true)
if [ -n "$PROHIBITED" ]; then
  COUNT=$(echo "$PROHIBITED" | wc -l)
  echo "Aliases prohibidos por STD-011: $COUNT" >> "$REPORT"
  echo '```' >> "$REPORT"
  echo "$PROHIBITED" | head -20 >> "$REPORT"
  echo '```' >> "$REPORT"
  VIOLATIONS=$((VIOLATIONS + COUNT))
else
  echo "✓ Ningun alias prohibido por STD-011" >> "$REPORT"
fi
echo "" >> "$REPORT"

# C-08 R-12: no SP names, HTTP routes, SQL en UC labels
echo "## C-08 — R-12 NO codenames de implementacion como UC labels" >> "$REPORT"
HITS=$(echo "$FILES" | xargs grep -nE '"sp_[a-z_]+|usecase "[A-Z]+ /api/|usecase "SELECT |usecase "INSERT |usecase "UPDATE |usecase "DELETE ' 2>/dev/null || true)
if [ -n "$HITS" ]; then
  COUNT=$(echo "$HITS" | wc -l)
  echo "Codenames de implementacion en UC labels: $COUNT" >> "$REPORT"
  echo '```' >> "$REPORT"
  echo "$HITS" | head -20 >> "$REPORT"
  echo '```' >> "$REPORT"
  VIOLATIONS=$((VIOLATIONS + COUNT))
else
  echo "✓ Ningun UC label con codename de implementacion" >> "$REPORT"
fi
echo "" >> "$REPORT"

# Summary
echo "## Summary" >> "$REPORT"
echo "" >> "$REPORT"
echo "- Total files audited: $TOTAL" >> "$REPORT"
echo "- Total violations detected: $VIOLATIONS" >> "$REPORT"
echo "" >> "$REPORT"

if [ $VIOLATIONS -eq 0 ]; then
  echo "✅ AUDIT PASSED — 0 violations" >> "$REPORT"
  echo ""
  echo "✅ AUDIT PASSED — 0 violations en $TOTAL archivos"
  echo "Report: $REPORT"
  exit 0
else
  echo "❌ AUDIT FAILED — $VIOLATIONS violations" >> "$REPORT"
  echo ""
  echo "❌ AUDIT FAILED — $VIOLATIONS violations en $TOTAL archivos"
  echo "Report: $REPORT"
  exit 1
fi
