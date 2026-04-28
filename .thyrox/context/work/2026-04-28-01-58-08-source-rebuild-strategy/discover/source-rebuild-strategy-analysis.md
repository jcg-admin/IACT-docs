```yml
created_at: 2026-04-28 01:58:08
project: IACT-docs
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Phase 1 DISCOVER — Source Rebuild Strategy

## 1. Estado actual de `source/` (verificado)

```
source/                         379 .rst, 0 .md
├── _static/                      0 .rst
├── _templates/                   0 .rst
├── arquitectura_tecnica/        15 .rst
├── base_cognitiva/              33 .rst   ← punto de partida
├── gestion/                     15 .rst
├── normativa/                  149 .rst
├── plantuml-guide/               8 .rst
└── requisitos/                 158 .rst
```

Verificado con `find source -name "*.rst" | wc -l` → 379.

## 2. Hipótesis estratégica

Reconstruir `source/` desde cero, dominio por dominio, sobre un
snapshot inmutable (`temp-backup/`) que se versiona en git para
trazabilidad total.

**Por qué esto puede ser superior al cleanup incremental:**

- 34 patrones de naming distintos → cualquier renombre crea N
  refs rotas. Reconstruir aplicando STD_007 desde el principio
  evita el flicker continuo de "build se rompe / se arregla".
- 147 hyperlinks rotos no están distribuidos uniformemente —
  dominios con peor estado (procedimientos: 67 archivos) cargan
  el resto al hacer build con `-W`.
- El cleanup incremental requiere *holding pattern* (mantener
  todo funcional mientras se reescribe) — el rebuild permite
  trabajar en cada dominio aislado sin tocar los demás.

**Riesgo principal del rebuild:** perder contenido valioso al no
re-incorporarlo. Mitigación: `temp-backup/` versionado +
checklist de cobertura por dominio (cada artefacto del backup
debe estar marcado "incorporado", "descartado-con-razón" o
"pendiente").

## 3. Inventario de `base_cognitiva/` (dominio inicial)

33 archivos en 4 sub-dominios:

| Sub-dominio | Archivos | Patrón |
|-------------|----------|--------|
| `_fundamentos_conceptuales/` | FND_01..FND_07 + index | `FND_NN_Nombre.rst` |
| `_metadata/` | META_01..META_05 + index | `META_NN_Nombre.rst` |
| `_ontologia_sbvr/` | SBVR_01..SBVR_05 + index | `SBVR_NN_Nombre.rst` |
| `_taxonomias_y_metamodelos/` | metamodelos/ + taxonomias/ + index | `MTM_NN_*`, `TXM_NN_*` |
| (raíz) | glossary, glosario_babok_pmbok_iso, IACT_Glossary_v1_0_0, index | mixto |

Observaciones inmediatas:

- Underscores como prefijo de directorio (`_fundamentos_*`) — Sphinx
  los trata como ocultos en algunos contextos.
- Mezcla de patrones en raíz: `glossary.rst` (inglés), `glosario_babok_pmbok_iso.rst`
  (snake_case), `IACT_Glossary_v1_0_0.rst` (PascalCase + version).
- Convención `MOD_NN_Nombre.rst` (PascalCase con guion bajo) viola
  STD_007 (kebab-case recomendado), pero hay 33 archivos que
  comparten la convención — decisión: mantenerla con justificación
  o migrar.

## 4. Decisiones pendientes (a resolver en este WP)

### D1: ¿Versión final del backup?

- Opción A: `temp-backup/source-2026-04-28/` versionado en feature
  branch, gitignored en main.
- Opción B: rama dedicada `backup/source-pre-rebuild` con `source/`
  intacto, y feature branch limpio.
- **Decisión confirmada por ejecutor: A — temp-backup/ versionado.**

### D2: ¿Dominio inicial?

- **Decisión confirmada por ejecutor: `base_cognitiva/`.**
- Justificación: provee el vocabulario (glosario, ontología, fundamentos)
  del que dependen los demás dominios. Empezar aquí da el
  diccionario de términos que el resto va a usar.

### D3: ¿Build con `-W` durante rebuild?

- **Decisión confirmada por ejecutor: NO usar `-W` durante el
  rebuild.** Recuperar `-W` al final, cuando todos los dominios
  estén reconstruidos.

### D4: ¿Convención sobre prefijos numéricos en filenames?

STD_007 dice "no prefijos numéricos en filenames". Pero los
artefactos actuales usan `FND_01_*`, `META_01_*`, `MTM_01_*`,
`UC_001_*`, `BR_001_*`, `FR_001_*`, `NFR_001_*`, etc.

Tensión: el ID semántico `FND-01`, `UC-001` ES significativo
(tracking ID), mientras que el prefijo numérico de orden visual
(`01-`, `02-`) NO lo es.

- Opción A: tratar `MOD_NN_Nombre.rst` como caso especial (ID =
  parte del filename) y permitirlo con regla explícita en STD_007.
- Opción B: mover el ID al frontmatter y renombrar todos los
  archivos a kebab-case puro (`fundamentos-concepto-requisito.rst`).
- **Pendiente decisión del ejecutor en próxima iteración.**

### D5: ¿Strategy de re-incorporación de contenido?

Dos sub-opciones:

- "Lift and shift normalizado": leer cada archivo del backup,
  aplicar STD_007 al filename y refs, mantener el contenido tal
  cual.
- "Refactor con corte editorial": leer el contenido, decidir si
  se mantiene, fusiona, divide o descarta.

- **Pendiente decisión del ejecutor.**

## 5. Orden de reconstrucción propuesto

Ordenado de menos a más dependencias salientes:

1. **`base_cognitiva/`** (33 archivos) — diccionario, sin
   dependencias hacia otros dominios.
2. **`normativa/estandares/`** (~10 archivos) — STDs y guías de
   estilo, depende del glosario.
3. **`normativa/procedimientos/`** (~67 archivos) — depende de
   estándares.
4. **`normativa/gobernanza/`** + **`normativa/restricciones/`** —
   dependen de procedimientos y estándares.
5. **`requisitos/`** (158 archivos) — depende del glosario y de
   las plantillas de estándares.
6. **`arquitectura_tecnica/`** (15 archivos) — depende de
   requisitos.
7. **`gestion/`** (15 archivos) — depende de todos los anteriores.
8. **`plantuml-guide/`** (8 archivos) — independiente, se puede
   hacer en cualquier momento o eliminar si no es esencial.

## 6. Criterios de aceptación por dominio

Cada WP de rebuild de dominio debe cumplir:

1. ✅ Build exit 0 con `sphinx-build -b html` (sin `-W`).
2. ✅ Todos los archivos del dominio en backup están marcados como
   incorporado / descartado-con-razón / pendiente.
3. ✅ Filenames y refs cumplen STD_007 (verificable por script).
4. ✅ Cero refs apuntando al backup (`temp-backup/`).
5. ✅ index.rst del dominio lista todo el contenido en toctree.

## 7. Bridge plan — mantener build verde durante rebuild

Durante el rebuild incremental:

- `source/index.rst` lista solo los dominios reconstruidos.
- Dominios pendientes viven en `temp-backup/` (no en toctree de
  source/). Sphinx no los conoce → no genera refs ni warnings.
- Refs entre dominios reconstruidos: usar `:ref:` con anchor explícito
  (no `:doc:` con path) para que un futuro renombre no rompa.
- Recuperar `-W` solo cuando los 7 dominios estén reconstruidos.

## 8. Hallazgos abiertos (para próxima iteración)

- F-01: definir D4 (prefijos numéricos vs IDs semánticos en filenames).
- F-02: definir D5 (lift-and-shift vs refactor con corte editorial).
- F-03: inventariar contenido específico de `base_cognitiva/` antes
  del primer WP de rebuild (qué se conserva, qué se fusiona).
- F-04: decidir destino de `plantuml-guide/` (mantener / eliminar /
  mover a `arquitectura_tecnica/`).
- F-05: confirmar si `_static/` y `_templates/` quedan en `source/`
  o se mueven (son infra de Sphinx, no contenido).
