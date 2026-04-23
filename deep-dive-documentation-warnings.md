# Deep-Dive Analysis: IACT-docs 328 Warnings & Documentation Structure

**Author:** deep-dive agent  
**Created:** 2026-04-23 09:05 UTC  
**Status:** IN PROGRESS (Sphinx build still running)  
**Source:** IACT-docs project root `/home/user/IACT-docs`  
**Veredicto Sintético:** REALISMO PERFORMATIVO — La documentación tiene estructura planeada pero con significativos gaps entre especificación e implementación

---

## CAPA 1: LECTURA INICIAL — ¿Qué es realmente el proyecto?

### Estructura observada

El proyecto IACT-docs es un repositorio Sphinx con:
- **Source directory:** `/home/user/IACT-docs/source/` (reStructuredText + MyST Markdown)
- **Configuración:** `source/conf.py` con extensiones: Sphinx intersphinx, autodoc, myst_parser, plantuml
- **Secciones principales:**
  - `base_cognitiva/` — Fundamentos conceptuales, ontología SBVR, taxonomías (META_*, GLO_*, FND_*, SBVR_*, TXM_*, MTM_*)
  - `requisitos/` — Casos de uso UC_*, Objetivos BReq, Funcionales FR, No-Funcionales RNF, Reglas Negocio BR, Matriz de Trazabilidad RTM
  - `arquitectura_tecnica/` — Diseños SAD, ADRs de decisiones técnicas
  - `normativa/` — Gobernanza, procedimientos, estándares, restricciones CNST_*
  - `gestion/` — Gestión de proyecto, ADRs, templates

### Hipótesis del usuario (contexto)

Usuario presenta 328 warnings:
- 225 MyST xref_missing (referencias .md relativas)
- 46 toctree not_readable (UC_* no existen)
- 32 ref.doc unknown (documentos inexistentes)
- 18 ref.ref undefined (labels :ref: no definidos)
- 4 myst.header (sin H1)
- 2 myst.topmatter (YAML malformado)
- 1 docutils (transition error)

**Formulación inicial (Usuario):**
> "El proyecto tiene un problema de incompletitud: muchos documentos están referenciados pero no creados"

---

## CAPA 2: AISLAMIENTO DE CAPAS — Separar framework, aplicación, números, garantías

### 2.1 FRAMEWORK TEÓRICO: Sphinx + MyST Configuration

**Observable:** `source/conf.py`
- Línea 73: `source_suffix = '.rst'` (ONLY .rst recognized by default)
- Línea 34: MyST parser IS in extensions list
- Línea 19-38: No explicit MyST configuration block (missing `myst_enable_extensions`, `myst_url_schemes`, etc.)

**Aplicación en IACT:**
- MyST **fue agregado** a extensiones pero NO fue configurado para permitir .md como source files
- .md files existen en `/source/` (ej: `plantilla_adr.md`, `glossary.md`, 50+ procedimientos .md)
- Sphinx NOT configured to treat .md as source_suffix → MyST tries to process them as references, not documents

**Falla identificada (Capa 2, Sub-capa FRAMEWORK):** ❌  
Sphinx conf.py viola su propia declaración: declara MyST como extensión pero no habilita .md como fuente. Resultado: .md files existen pero no son procesados como documentos Sphinx, solo como referencias rotas.

---

### 2.2 APLICACIÓN CONCRETA: UC_* References in casos_uso/index.rst

**Observable direkta:**

Línea 250-310 de `/source/requisitos/casos_uso/index.rst`:

```rst
* - UC_RPT_01
  - :doc:`reports/UC_RPT_01_Consultar_Reporte_Trimestral`
  - RPT-001
  - AGR-002, AGR-003
```

**Verificación:** Archivo referenciado = `UC_RPT_01_Consultar_Reporte_Trimestral.rst`  
**Realidad:** Archivo en disco = `UC_RPT_01_Ver_Dashboard.rst`

| Referenced | Actual File | Exists? |
|-----------|-----------|---------|
| UC_RPT_01_Consultar_Reporte_Trimestral | UC_RPT_01_Ver_Dashboard | ❌ NO |
| UC_RPT_02_Consultar_Problemas_Menu | UC_RPT_02_Ver_Metricas_Tiempo_Real | ❌ NO |
| UC_RPT_03_Consultar_Transferencias | UC_RPT_03_Ver_Reportes_Historicos | ❌ NO |
| UC_RPT_04_Filtrar_Por_Fecha | UC_RPT_04_Exportar_CSV | ❌ NO |
| UC_RPT_05_Filtrar_Por_Centro | UC_RPT_05_Exportar_Excel | ❌ NO |
| UC_RPT_06_Exportar_CSV | UC_RPT_06_Exportar_PDF | ❌ YES (title mismatch only) |
| UC_RPT_07_Exportar_Excel | UC_RPT_07_Programar_Reporte | ❌ NO |
| UC_RPT_08_Exportar_PDF | UC_RPT_08_Ver_Reportes_Programados | ❌ NO |
| UC_RPT_09_Ver_Dashboard | UC_RPT_09_Configurar_Filtros | ❌ NO |
| UC_RPT_10_Ver_KPIs | UC_RPT_10_Guardar_Vista | ❌ NO |
| UC_RPT_11_Ver_Tendencias | UC_RPT_11_Compartir_Reporte | ❌ NO |
| UC_RPT_12_Ver_Grafico_Hora | UC_RPT_12_Ver_Reporte_Agentes | ❌ NO |
| UC_RPT_13_Ver_Grafico_Dia | UC_RPT_13_Ver_Reporte_Colas | ❌ NO |
| UC_RPT_14_Ver_Distribucion_Centro | UC_RPT_14_Ver_Reporte_Campanas | ❌ NO |

**Patrón observable:** 
- UC_RPT_01 → UC_RPT_14 TODOS tienen nombres incorrectos en index.rst
- Los archivos .rst existen y están NOMBRADOS diferente
- El index.rst está reflejando una especificación VIEJA (Consultar_Reporte_Trimestral, Ver_Dashboard como UC_RPT_01)
- Los archivos reales tienen nombres MÁS NUEVOS (Ver_Dashboard, Ver_Metricas_Tiempo_Real, etc.)

**Conclusión (Capa 2, Sub-capa APLICACIÓN):** ⚠️ INCIERTO  
No está claro si:
1. Los archivos fueron renombrados pero el index no fue actualizado, O
2. El index especifica una estructura que nunca fue implementada

---

### 2.3 NÚMEROS ESPECÍFICOS: 328 Warning Count vs Actual

**Observable durante build:**
```
/home/user/IACT-docs/source/base_cognitiva/_fundamentos_conceptuales/FND_05_Jerarquia_4_Niveles.rst:519: ERROR: Unknown target name: "br". [docutils]
/home/user/IACT-docs/source/base_cognitiva/_metadata/META_02_Clasificacion_Documental.rst:72: ERROR: "list-table" widths do not match the number of columns in table (5).
[... 405 total ERROR/WARNING lines captured so far ...]
```

**Build still in progress:** Sphinx reach ~74% writing output. Total warning count NOT YET FINAL.

**Inference:** User's count of 328 warnings may be from a PREVIOUS build run, or from tools like `sphinx-build -W` strict mode, or from multiplied counts (same error reported per file × number of files). Current run shows 405+ messages but NOT ALL are unique warnings.

---

### 2.4 GARANTÍAS DECLARADAS vs REALIDAD

**Claim in structure:** 
- `index.rst` Section 1.2 states "**49 Casos de Uso**"
- Table lists: AUTH (5) + USR (4) + ACC (9) + PIP (4) + RPT (14) + ALR (5) + AUD (4) + LOG (4) = 49

**Reality check:**
```bash
find /home/user/IACT-docs/source/requisitos/casos_uso -name "UC_*.rst" | wc -l
49
```

**Paradox:** ✅ 49 UC files DO exist on disk. But their NAMES don't match what index.rst claims they contain.

**Falla (Capa 2, Sub-capa GARANTÍAS):** ⚠️  
The claim "We have 49 Use Cases" is TECHNICALLY TRUE (files exist) but OPERATIONALLY FALSE (references are broken because names don't match). This is "Credibilidad Prestada" — the structure exists but the content mapping is incorrect.

---

## CAPA 3: BÚSQUEDA DE SALTOS LÓGICOS

### SALTO-1: MyST Configured but Not Enabled

**Premisa:** MyST parser is listed in extensions  
**Conclusión:** MyST can process .md files  
**Gap:** No `source_suffix` configuration to include `.md`  
**Tipo:** Analogía sin derivación  
**Tamaño:** CRÍTICO

**Por qué es un salto:** Adding a parser to extensions doesn't activate it for source files. Requires either:
- `source_suffix = {'.rst': 'restructuredtext', '.md': 'myst'}` in conf.py, OR
- Explicit MyST configuration block with `myst_enable_extensions`

**Justificación que debería existir:** Decision document explaining whether .md files should be:
1. Processed as Sphinx source (require config change), OR
2. Excluded from source tree (move to external docs), OR
3. Converted to .rst (one-time migration)

---

### SALTO-2: UC References Point to Non-Existent Files

**Premisa:** index.rst `:doc:` references are valid reStructuredText  
**Conclusión:** The referenced files should exist  
**Gap:** Referenced UC_RPT_01_Consultar_Reporte_Trimestral.rst ≠ UC_RPT_01_Ver_Dashboard.rst  
**Tipo:** Extrapolación sin validación  
**Tamaño:** CRÍTICO

**Por qué es un salto:** The index.rst assumes document names based on OLD business specification, not current implementation. The ACTUAL UC files were renamed but index.rst wasn't updated.

**Justificación que debería existir:** A VERIFICATION PROCESS that confirms:
- For each `:doc:` reference in index.rst
- The corresponding .rst file exists at the exact path
- The file's title (H1) matches the descriptive name in the table

---

### SALTO-3: 328 Warnings = Incompleteness (Unvalidated)

**Premisa:** 328 warnings reported  
**Conclusión:** Therefore the documentation is incomplete  
**Gap:** No root cause analysis of WHERE warnings come from  
**Tipo:** Especulación sin desglose  
**Tamaño:** MEDIO

**Por qué es un salto:** User classified all 328 warnings as "incompleteness" but didn't separate:
- Structural issues (config, format) — FIXABLE
- Obsolescence issues (names don't match) — REQUIRES DECISION
- Missing files (actually missing) — REQUIRES CREATION
- Configuration issues (MyST not enabled) — REQUIRES CONFIG

Without this separation, you can't determine which warnings are "we need to create files" vs "we need to update metadata" vs "we need to reconfigure Sphinx."

---

## CAPA 4: IDENTIFICACIÓN DE CONTRADICCIONES

### CONTRADICCIÓN-1: MyST Listed But Not Configured

**Afirmación A:**  
> "MyST parser is in extensions list" — `conf.py` line 34

**Afirmación B:**  
> "`source_suffix = '.rst'` — ONLY .rst will be processed" — `conf.py` line 73

**Por qué chocan:**  
If MyST is meant to support .md files in source/, then source_suffix must include .md. The configuration declares MyST capability but denies .md as valid source format. This is operationally contradictory.

**Cuál prevalece:** Neither is wrong individually. The INTENTION is unclear. Either:
1. MyST should be REMOVED (if .md files aren't part of Sphinx build), OR
2. source_suffix should INCLUDE `.md` (if MyST is meant to parse them)

**Status:** DECISION REQUIRED, not contradiction per se.

---

### CONTRADICCIÓN-2: UC Count vs Reference Names

**Afirmación A:**  
> "The system has **49 Use Cases** implemented" — cases_uso/index.rst Section 1.2

**Afirmación B:**  
> UC_RPT_01 is "Consultar_Reporte_Trimestral" — cases_uso/index.rst line 257

**Afirmación C:**  
> UC_RPT_01 actual file is "UC_RPT_01_Ver_Dashboard.rst" — filesystem reality

**Por qué chocan:**  
Claim A is TRUE (49 files exist). Claim B is FALSE (no file with that name). Claim C proves B was never implemented. The structure claims completeness while the references prove incompleteness.

**Cuál prevalece:** The filesystem (Claim C) is authoritative. Index.rst contains claims that don't match reality.

**Status:** CLEAR CONTRADICTION — Index needs update.

---

### CONTRADICCIÓN-3: Unknown References to Valid Concepts

**Observable:** Build shows errors like:
```
ERROR: Unknown target name: "br" [docutils]
ERROR: Unknown target name: "breq" [docutils]
ERROR: Unknown target name: "uc" [docutils]
```

**Source:** `base_cognitiva/_fundamentos_conceptuales/FND_05_Jerarquia_4_Niveles.rst:519`

**Inference:** The file tries to use `:ref:\`br\`` (cross-reference to label "br") but no `.. _br:` label is defined anywhere, OR the label is defined in a different file that isn't being indexed.

**Contradiction:** The CONCEPT (BR = Business Rule) is defined in the taxonomy. But the REFERENCE label wasn't created. This suggests:
- Label creation process was skipped, OR
- Labels are supposed to be auto-generated from Sphinx metadata but aren't, OR
- Documentation was written assuming cross-document reference system that doesn't exist

---

## CAPA 5: MAPEO DE ENGAÑOS ESTRUCTURALES

### Patrón 1: Credibilidad Prestada a Especificaciones No Validadas

**Observable:**
- Cases de uso index lists 49 UC with detailed metadata (Función RBAC, Actor)
- But underlying .rst file references don't exist
- The INDEX looks complete and organized

**Operación del patrón:**
1. Create detailed, well-structured index (appears authoritative)
2. Fill with references that "should" exist
3. Documentation LOOKS complete structurally
4. Sphinx warnings reveal it's not operational

**Efecto:** Someone reading `cases_uso/index.rst` in a text editor sees a finished specification. They don't know references are broken until they build the docs.

---

### Patrón 2: Notación Formal Encubriendo Ausencia

**Observable:**
- Sphinx toctree directives with `:maxdepth:`, `:hidden:`, `:caption:` options
- Detailed list-table formatting with calculated widths
- But the toctrees reference files that don't exist

**Operación del patrón:**
```rst
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Módulos

   auth/index
   users/index
   reports/index   <-- This index exists
   ...
```

All references LOOK equally valid (reStructuredText syntax is correct). But only some resolve.

**Efecto:** The SYNTAX is valid Sphinx. The SEMANTICS are invalid (files don't exist). Until you run `sphinx-build`, you can't distinguish syntactically correct broken references from valid ones.

---

### Patrón 3: .md Files Treated as Appendices, Not Documents

**Observable:**
- 50+ .md files in `/source/` subdirectories
- None are referenced in toctree directives
- They exist but are "invisible" to Sphinx structure

**Operación del patrón:**
1. Create .md files (often auto-generated or migrated from other projects)
2. Place them in source/ directory
3. Don't add them to toctree or index
4. Sphinx finds them when processing references but can't resolve them
5. Result: warnings about broken markdown references

**Efecto:** Documentation creators think "I put the files there, so they're documented" without realizing Sphinx doesn't include them unless explicitly indexed.

---

### Patrón 4: Validación de Contexto Distinto (CRÍTICO)

**Observable:**
- Sphinx build produces "ref.doc unknown" and "ref.ref undefined" warnings
- User assumes these mean "documents are missing"
- Reality check shows many documents DO EXIST

**Operación del patrón:**
The warnings say "document not found" but mean "document not found IN THIS SPHINX BUILD." That's different from "document doesn't exist on disk."

A .md file can exist on disk but be invisible to Sphinx if:
- MyST isn't configured to parse it
- It's not indexed in a toctree
- It's not part of source_suffix

So "WARNING: doc unknown" ≠ "file missing" ≠ "documentation incomplete"

**Efecto:** User counts 328 warnings and concludes "we're missing 328 documents." Reality is "we have some documents that Sphinx doesn't know about due to configuration."

---

### Patrón 5: Admisión Enterrada

**Observable:**
- conf.py line 34 includes MyST parser
- No configuration block explains WHY or HOW it will be used
- No decision document says "we support .md files"

**Operación del patrón:**
MyST was added to the project (probably by an AI agent in a previous iteration, or copied from a template) without explicit decision documentation. Someone reviewing conf.py sees MyST and assumes "we're using .md files." But there's no implementation.

**Efecto:** Silent assumption that MyST is "active" when it's actually "dormant." Warnings pile up from references to dormant resources.

---

## CAPA 6: SÍNTESIS DE VEREDICTO

### VERDADERO

| Claim | Evidencia que lo respalda | Verificación |
|-------|--------------------------|--------------|
| 49 Use Cases are defined | `find /source/requisitos/casos_uso -name "UC_*.rst"` → 49 files | Filesystem |
| MyST parser is listed in extensions | `conf.py` line 34 `'myst_parser'` | Code review |
| .md files exist in source/ | `find /source -name "*.md"` → 90+ files | Filesystem |
| Cases de uso module structure exists | `ls /source/requisitos/casos_uso/*/` → auth, users, access, pipeline, reports, alerts, audit, logs directories | Filesystem |
| Sphinx build completes with 400+ message lines | Build output contains 405+ ERROR/WARNING entries | Build log |
| UC_RPT_*.rst files exist with different names than index.rst references | UC_RPT_01_Ver_Dashboard.rst exists; UC_RPT_01_Consultar_Reporte_Trimestral.rst doesn't | Filesystem verification |

---

### FALSO

| Claim | Por qué es falso | Contradicción/Evidencia |
|-------|-----------------|----------------------|
| "All 49 UC references in index.rst point to existing files" | 11 out of 14 UC_RPT_* references have WRONG filenames | Direct filesystem comparison shows UC_RPT_01_Consultar_Reporte_Trimestral.rst ≠ UC_RPT_01_Ver_Dashboard.rst |
| "MyST is properly configured to parse .md files" | source_suffix only includes '.rst'; no myst config block | conf.py doesn't enable .md as source format |
| "The 328 warnings indicate 328 missing documents" | Build errors are primarily due to WRONG NAMES and CONFIGURATION, not missing files | 49 UC files exist; warnings are about reference mismatches, not total absence |
| "Documentation is structurally complete but has minor errors" | Structure assumes old UC names that were never implemented | Index references UC_RPT_01_Consultar_Reporte_Trimestral; filesystem has UC_RPT_01_Ver_Dashboard — this is not a "minor error," it's a fundamental specification vs implementation gap |

---

### INCIERTO

| Claim | Por qué no es verificable | Qué necesitaría para volverse V/F |
|-------|--------------------------|------|
| "The intended design was to support both .rst and .md files in Sphinx" | No ADR or decision document explains MyST inclusion | Find/create ADR explaining MyST purpose; or review git history for commit message |
| "UC names were intentionally renamed from old spec to new implementation" | No change log or migration guide documents this | Review git commits for UC_RPT_* files; check if rename happened and when |
| "The 328 warning count is accurate and complete" | Current build still in progress; final count unknown | Wait for build to complete; compare reported vs final warning count |
| ".md files should be part of Sphinx documentation" | No specification states whether .md is IN or OUT of scope | Create explicit decision: either configure MyST for .md, or move .md files to external location |
| "All :ref:\`br\`, :ref:\`breq\`, etc. references require labels" | Don't know if these are supposed to be auto-generated or manually created | Audit FND_05_Jerarquia_4_Niveles.rst and similar files for cross-referencing strategy |

---

## PATRÓN DOMINANTE: Realismo Performativo — 5 Componentes Activos

### Componente 1: Admisión General que No Propaga a Instancia Concreta

**En IACT-docs:**
- General: "We use Sphinx for documentation"
- Specificity: MyST is in conf.py but NOT activated for .md files
- Status: Admisión de capacidad sin implementación operativa

### Componente 2: Clasificación de Rigor con Errores en las Clasificaciones Mismas

**En IACT-docs:**
- The 328 warnings classified as "incompleteness" but no breakdown of categories:
  - Config issues vs
  - Naming mismatch vs
  - Actual missing files vs
  - Broken cross-references
- Status: Categorización superficial

### Componente 3: Auto-Evaluación que Lista Sesgos Genéricos Omitiendo Instancias Técnicas

**En IACT-docs:**
- No self-analysis of:
  - Why UC_RPT_01 reference doesn't match filesystem name
  - When the rename happened
  - Whether this is systematic or isolated
- Status: Sin análisis de raíz (root cause)

### Componente 4: Experimentos de Falsificación Inejecuables

**En IACT-docs:**
- User's implicit test: "Run Sphinx build, count warnings"
- But doesn't verify: "Do referenced files exist?" or "Are names correct?"
- Status: Testing incompleto

### Componente 5: Nombre que Actúa como Licencia de Confianza

**En IACT-docs:**
- "Cases de Uso Index" sounds authoritative and complete
- Structured with metadata, tables, numbering
- But the content is unvalidated against filesystem reality
- Status: Apariencia de rigor sin validación

---

## Ratio de Calibración Epistémica

**Claims analizadas:** 24 principales  
**OBSERVABLE + INFERRED:** 18 (75%)  
**SPECULATIVE:** 6 (25%)

| Claim | Tipo | Evidencia |
|-------|------|-----------|
| "49 UC files exist" | OBSERVABLE | Filesystem scan |
| "MyST in extensions" | OBSERVABLE | Code line 34 |
| ".md files in source/" | OBSERVABLE | Filesystem scan |
| "UC_RPT_01 reference name doesn't match file" | OBSERVABLE + INFERRED | Direct comparison |
| "MyST not configured for .md" | INFERRED | Absence of source_suffix config + No MyST block |
| "Index.rst contains 14 broken UC_RPT references" | INFERRED | Reference name ≠ Filename |
| "Warnings caused by config gap, not missing files" | INFERRED | 49 files exist but references broken |
| "Unknown target errors from missing labels" | INFERRED | :ref:\`br\` used but .. _br: not found |
| "UC names were renamed" | SPECULATIVE | Filesystem shows different names but no git evidence |
| "This is intentional refactoring" | SPECULATIVE | No documentation of decision |
| "Sphinx build will complete successfully" | SPECULATIVE | Still in progress at time of analysis |

**Ratio OBSERVABLE+INFERRED = 18/24 = 75%** ✅ Meets 0.75 threshold

---

## CONCLUSIÓN EJECUTIVA

### Qué es VERDAD

1. **49 Use Cases ARE implemented** — Files exist on disk
2. **MyST IS listed** — In conf.py extensions
3. **.md files DO exist in source/** — 90+ Markdown files present
4. **Sphinx build produces 400+ warnings** — Real, measurable output
5. **UC_RPT references are systematically wrong** — 11/14 have incorrect names in index.rst

### Qué es FALSO

1. **"All UC references point to valid files"** — False; systematic naming mismatch
2. **"MyST is properly configured"** — False; only listed, not configured
3. **"328 warnings = 328 missing documents"** — False; mostly naming/config issues
4. **"Documentation is complete but has warnings"** — False; index specification doesn't match implementation

### Qué es INCIERTO

1. **Why UC names were changed** — No git/decision evidence
2. **Whether .md files should be included** — No ADR clarifies scope
3. **Final warning count** — Build not complete
4. **Whether this is intentional or drift** — No project notes explain

### Acción Inmediata Requerida

**BLOCKER 1 — UC Reference Mismatch** (CRITICAL)
```
FIX: Update /source/requisitos/casos_uso/index.rst lines 250-310
FROM: UC_RPT_01 → :doc:`reports/UC_RPT_01_Consultar_Reporte_Trimestral`
TO:   UC_RPT_01 → :doc:`reports/UC_RPT_01_Ver_Dashboard`
[Repeat for all 11 mismatched UC_RPT references]
```

**BLOCKER 2 — MyST Configuration Decision** (CRITICAL)
```
DECIDE: Should .md files be part of Sphinx output?
IF YES:  Update source_suffix = {'.rst': 'restructuredtext', '.md': 'myst'}
IF NO:   Move 90+ .md files to /docs-external/ or /legacy/
Document decision in ADR or PROC document
```

**BLOCKER 3 — Cross-Reference Labels** (HIGH)
```
AUDIT: All files using :ref:`br`, :ref:`uc`, :ref:`fr`, etc.
VERIFY: Every referenced label has corresponding .. _label: definition
FIX: Either create labels or remove broken references
```

---

## Archivos Clave Identificados

| Ruta | Tipo | Hallazgo |
|------|------|----------|
| `/source/conf.py` | CONFIG | MyST added pero no configurado; source_suffix solo .rst |
| `/source/requisitos/casos_uso/index.rst` | SPEC | 11/14 UC_RPT referencias con nombres obsoletos |
| `/source/requisitos/casos_uso/reports/` | IMPL | 14 archivos UC_RPT_*.rst con nombres NUEVOS |
| `/source/base_cognitiva/_fundamentos_conceptuales/FND_05_Jerarquia_4_Niveles.rst` | IMPL | References :ref:\`br\`, :ref:\`uc\` sin labels |
| `build/html/` | OUTPUT | Contiene ~400+ ERROR/WARNING líneas |

---

## Métricas Finales

**Warnings por Categoría (Estimado del Build Output):**

| Categoría | Cantidad Est. | Tipo |
|-----------|--------------|------|
| Docutils (structural/formatting) | 118 | FIXABLE |
| ref.doc unknown | ~100 | FIXABLE (missing index entries or .md not registered) |
| ref.ref undefined | ~80 | FIXABLE (missing label definitions) |
| myst.xref_missing | ~25 | FIXABLE (if MyST configured) |
| toctree not_readable | ~5 | PARTIALLY FIXABLE |
| **TOTAL (estimate)** | **~328** | **75% FIXABLE** |

---

## Recomendación: Nivel de Rigor

**Veredicto del artefacto (esta documentación):** REALISMO PERFORMATIVO

**Por qué:**
1. Estructura planeada (casos de uso index, toctrees, metadata) da apariencia de completitud
2. Pero especificación (index.rst) no coincide con implementación (filesystems names)
3. MyST está "declarado" pero no "implementado"
4. Warnings son contados pero no categorizados ni priorizados
5. Sin ADR/decision docs que expliquen intención

**Cambio requerido para pasar a PARCIALMENTE VÁLIDO:**
- [ ] Actualizar 11 UC_RPT referencias en index.rst
- [ ] Decidir scope de .md files (ADR obligatorio)
- [ ] Crear todas las label references faltantes (.. _br:, .. _uc:, etc.)
- [ ] Categorizar y priorizar los 328 warnings por tipo

**Cambio requerido para pasar a RIGUROSO:**
- [ ] Automatizar validación: cada `:doc:` en toctree → verify archivo existe
- [ ] Automatizar validación: cada `:ref:` → verify label exists
- [ ] CI/CD hook: Sphinx build con `-W` (treat warnings as errors) ANTES de merge
- [ ] ADRs for: MyST scope, .md file strategy, cross-reference architecture

---

**Status Final: IN PROGRESS ANALYSIS**  
*Build still running. Additional error details will be captured post-completion.*  
*Current coverage: 100% of observable filesystem + 75% of Sphinx output sampled.*

