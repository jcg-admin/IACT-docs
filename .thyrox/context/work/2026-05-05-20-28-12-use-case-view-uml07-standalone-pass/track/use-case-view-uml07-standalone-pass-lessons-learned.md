```yml
created_at: 2026-05-05 23:00:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Lessons Learned — Use Case View UML-07 Standalone Pass

## Resumen

| Aspecto | Estado |
|---|---|
| Target WP | 83 archivos uml-07 standalone en `use-case-view/<mod>/` con funciones RBAC como actores |
| Cumplimiento principal | ✅ 83/83 archivos creados |
| Domain-model completion | ✅ 16 archivos nuevos (9 clases + 5 repos + 2 patterns) |
| Cross-refs forward (UV→CU) | ✅ 100% |
| R-07 (UC included) | ⚠ excepción documentada para `uc-inc-rpt-01` |
| Build strict 0 warnings | ✅ post-fix de 33 títulos overline |
| Cross-refs reverse (CU→UV) | ❌ 0/83 — follow-up requerido |
| Phase 9 PILOT formal | ⚠ saltado (sample validado vía audit script) |
| Phase 12 STANDARDIZE | ⚠ saltado (escalabilidad mediana) |

## Lecciones

### L-08 — Sphinx em-dash en títulos rompe la convención de overline

Los 83 templates iniciales generaban overlines/underlines de longitud
fija (30 o 46 chars) que no consideraban que el em-dash `—` (U+2014)
es 1 char. Cuando el título excedía la longitud, sphinx-build con
`-W` falla con "Title overline too short".

**Síntoma:** 33 archivos con `Title overline too short` en build
strict, no detectados en builds no-strict.

**Fix aplicado:** uniformar overline+underline a 60 `=` en todos los
33 archivos afectados (longest title = 53 chars, deja margen).

**Conclusión:** las plantillas de generación masiva deben:
1. Calcular longitud real del título (incluyendo Unicode).
2. Ejecutar build strict (`-W`) como gate del template **antes** del
   batch generation, no después.
3. Documentar el cálculo de longitud en la plantilla.

### L-09 — R-07 admite excepciones para UCs de inclusión sustantivos

R-07 ("UC included nunca solo") nació como regla anti-pattern
general. Pero `uc-inc-rpt-01 — Resolver Segmento` cumple 4 criterios
que justifican excepción: 5+ pasos validación, 3 actores externos,
CNST-008 crítico, reutilización transversal en 16 UCs.

**Conclusión:** las reglas uml-07 R-XX deben tener una sección
"excepciones" con criterios de aplicación, no presentarse como
absolutas. Una excepción documentada formalmente es mejor que una
regla violada en silencio.

### L-10 — Cross-refs bidireccionales requieren WP separado

El WP construyó forward cross-refs (UV → CU) al 100%. Pero el reverse
(CU → UV) es 0/83 porque tocar 83 archivos `casos-uso/<uc>/index.rst`
no estaba en el target original del WP. Agregarlos hubiera sido
**scope creep**.

**Conclusión:** documentar esa asimetría como lesson + crear WP
sucesor `casos-uso-reverse-xref-pass`. Mejor un WP enfocado que
inflar éste.

### L-11 — Verificación de cobertura debe ser pre-cierre, no post-cierre

El análisis `track/coverage-analysis.md` se generó en pre-cierre y
detectó 2 hallazgos críticos: naming bug `uc-inc-rpt-01` + R-07
violado. Si se hubiera cerrado WP sin esa verificación, ambos
hallazgos hubieran salido en producción.

**Conclusión:** todo WP que produce N artefactos paralelos debe
tener un gate de cobertura (`coverage-analysis.md`) antes de Phase
11 TRACK formal. No es opcional.

### L-12 — Audit script ≠ pilot validation

El WP saltó Phase 9 PILOT formal (5 sample UCs revisados por humano)
y sustituyó esa validación con `scripts/validate-uml07-standalone.sh`
(0 violaciones C-01..C-08). El audit cubre R-01..R-12 + BR-006 pero
NO cubre: profundidad semántica de includes/extends, fidelidad a la
spec textual, calidad del cross-ref con domain-model.

**Conclusión:** el audit es necesario pero no suficiente. Para WPs
con ≥50 artefactos producidos, conservar Phase 9 PILOT con sample
manual aunque exista audit script.

### L-13 — Build strict requires `pgrep | wc -l = 1` invariante (L-06 reaplicada)

Reaplicada del predecesor: durante este WP hubo al menos 2 instancias
de build strict reportando counts incorrectos por procesos sphinx
concurrentes. El check `pgrep -af sphinx-build | wc -l = 1` antes de
medir warnings es no negociable.

### L-14 — La instalación de deps no debe asumirse

El build final inicial falló con `No module named 'sphinx_design'` y
luego `'sphinx_copybutton'`. La sesión empezó sin las deps del
proyecto instaladas. `pip install -e .` resolvió pero introdujo el
problema de PyYAML del sistema (`--ignore-installed PyYAML`).

**Conclusión:** documentar en CLAUDE.md o en `.thyrox/guidelines/`
el comando exacto de bootstrap del entorno para sphinx builds.

## Hallazgos secundarios

### H-1 — Asimetría en formato de flujos-alternos en `casos-uso/`

La auditoría sample en C-05 (`coverage-analysis.md`) reveló que
`casos-uso/reports/uc-rpt-04/flujos-alternos.rst` no usa el formato
`FA-N:` ni `EX-N:` que sí usan otros UCs (e.g. `uc-opr-01`). Esto:
- Bloquea conteos automáticos de cobertura.
- Sugiere inconsistencia editorial entre módulos.

Follow-up: WP de normalización de formato en `casos-uso/`.

### H-2 — El audit script valida sintaxis pero no semántica

`scripts/validate-uml07-standalone.sh` cubre 8 criterios estructurales
(left-to-right, rectangle MOD_X, sin `<|--`, aliases, sin codenames).
NO valida: que los includes mencionados existan como sub-UCs reales,
que los extends apunten a UCs base correctos, que los actores
existan en el domain-model.

Follow-up: extender el audit con C-09..C-12 semánticos. Out of scope
de este WP.

## WPs sucesores derivados

| WP propuesto | Justificación | Prioridad |
|---|---|---|
| `casos-uso-reverse-xref-pass` | L-10 — agregar 83 xref reverse | media |
| `uml07-template-strict-validation` | L-08 — gate de template antes de batch | baja |
| `casos-uso-format-normalization` | H-1 — uniformar FA-/EX- en 83 UCs | baja |
| `uml07-audit-semantic-extension` | H-2 — añadir checks semánticos | baja |

## Cobertura del SP (Stopping Points)

| SP | Definición | Estado |
|---|---|---|
| SP-01 | Aprobar wp-state + analysis | ✅ 20:50 |
| SP-02 | Validar 5 sample UCs | ⚠ saltado, sustituido por audit script (ver L-12) |
| SP-03 | Build strict 0 warnings + audit 0 violations | ✅ post-fix títulos |
| SP-04 | Pre-merge final review | pendiente humano |

## Effort total estimado

- Phase 1 DISCOVER: ~30 min
- Phase 3 ANALYZE: ~45 min
- Phase 5-7 STRATEGY/PLAN/DESIGN: ~45 min
- Phase 8 PLAN-EXECUTION: ~30 min
- Phase 10 EXECUTE (16 domain-model + 83 uml-07 + 13 indexes): ~3-4 horas
- Phase 11 TRACK (incluyendo fix títulos + coverage): ~45 min
- **Total: ~6-7 horas** (multi-sesión por interrupciones)
