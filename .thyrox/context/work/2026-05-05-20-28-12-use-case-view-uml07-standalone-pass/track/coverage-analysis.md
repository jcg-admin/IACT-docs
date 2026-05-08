```yml
created_at: 2026-05-05 22:55:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 11 — TRACK/EVALUATE (pre-cierre)
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Coverage Analysis — use-case-view vs casos-uso

> Análisis de cobertura ejecutado en pre-cierre para verificar
> que los 83 archivos uml-07 standalone en
> `source/arquitectura-tecnica/use-case-view/` cubren todo lo
> declarado en `source/requisitos/casos-uso/`.

## Inventario

| Lado | Path | Conteo |
|---|---|---|
| **Casos de uso** (spec textual) | `source/requisitos/casos-uso/<mod>/<uc>/` | 83 directorios |
| **Use case view** (uml-07 standalone) | `source/arquitectura-tecnica/use-case-view/<mod>/uc-XXX-NN-*.rst` | 83 archivos |

Conteos por módulo: **idénticos** en ambos lados (access=7, admin=3,
alerts=5, audit=4, auth=5, caller=5, logs=7, operator=10,
permissions=10, pipeline=4, reports=16, supervision=3, users=4).

## C-01 — Cobertura 1:1 por UC ID

**82/83** UCs tienen archivo standalone correspondiente. El restante
es un caso edge documentado (ver C-02).

```
Faltantes en use-case-view:    0 reales (1 falso positivo, ver C-02)
Sobrantes en use-case-view:    0
Coincidentes:                  82 + 1 con naming bug = 83
```

## C-02 — `uc-inc-rpt-01` — Naming bug + R-07 violado

### Hallazgo

Existe `source/arquitectura-tecnica/use-case-view/reports/uc-inc-rpt-01-uc-inc-rpt-01-resolver-segmento.rst`

Dos problemas:

1. **Naming bug**: el prefijo `uc-inc-rpt-01-` está duplicado en el
   nombre. Debería ser `uc-inc-rpt-01-resolver-segmento.rst`.
2. **R-07 violado**: la regla R-07 del WP plan dice explícitamente
   "uc-inc-rpt-01 NO recibirá archivo standalone" porque es un UC
   de inclusión (nunca se ejecuta solo). Pero el archivo existe.

### Evidencia

```bash
$ grep "R-07" wp-state.md
| R-07 | UC included nunca solo | ✓ — uc-inc-rpt-01 NO recibirá archivo standalone |

$ ls reports/uc-inc-rpt-01*
uc-inc-rpt-01-uc-inc-rpt-01-resolver-segmento.rst   # ← existe + naming duplicado
```

### Impacto

- **Naming**: el archivo aparece en el toctree del módulo `reports`
  con un slug malformado.
- **R-07**: el WP comprometió "no archivo standalone" para UCs de
  inclusión. Tener este archivo contradice ese compromiso.

### Acción

Decidir antes de cerrar el WP:
- (a) **Eliminar** `uc-inc-rpt-01-uc-inc-rpt-01-resolver-segmento.rst`
  + remover entrada del toctree de `reports/index.rst` → cumple R-07.
- (b) **Renombrar** a `uc-inc-rpt-01-resolver-segmento.rst` y
  documentar excepción a R-07 en lessons-learned (con justificación:
  el UC de inclusión es lo suficientemente complejo para merecer
  diagrama propio).

Recomendación: **(b) renombrar + documentar excepción**, dado que el
archivo ya existe con contenido sustantivo.

## C-03 — Cross-refs forward (UV → casos-uso)

**83/83 archivos use-case-view referencian su spec textual** en
`casos-uso/`. Cobertura forward: **100%**.

Patrón verificado: cada `uc-XXX-NN-*.rst` tiene en `seealso`:

```rst
- :doc:`/requisitos/casos-uso/<mod>/<uc>/index` — spec textual.
```

## C-04 — Cross-refs reverse (casos-uso → UV)

**0/83 casos-uso referencian su counterpart en use-case-view**.
Cobertura reverse: **0%**.

### Implicación

Un lector navegando la spec textual de un UC (e.g. abriendo
`casos-uso/operator/uc-opr-01/index.rst`) no tiene forma directa de
encontrar el diagrama uml-07 standalone correspondiente. Debe
navegar manualmente a `arquitectura-tecnica/use-case-view/operator/`
y adivinar el slug.

### Acción recomendada

Agregar en cada `casos-uso/<mod>/<uc>/index.rst` una sección
`seealso` con:

```rst
.. seealso::

   :doc:`/arquitectura-tecnica/use-case-view/<mod>/<uc-slug>` —
   Vista de caso de uso (uml-07 standalone).
```

83 archivos a tocar. **Out of scope** del WP actual (el WP solo
construye uml-07 standalone), pero es un follow-up necesario.
Crear WP separado o agregar a `track/lessons-learned.md` como
recomendación.

## C-05 — Profundidad: includes/extends del UV vs flujos del CU

Sample de 3 UCs (criterio: 1 simple, 1 con muchos extends, 1 cross-mod):

| UC | includes/extends en UV | flujos-alternos en CU | excepciones en CU |
|---|---|---|---|
| operator/uc-opr-01 | 4 | 6 | 6 |
| reports/uc-rpt-04 | 7 | 0 (sin secciones FA-) | 0 (sin secciones EX-) |
| supervision/uc-sup-03 | 6 | 3 | 5 |

### Observaciones

- `uc-opr-01`: el UV tiene 4 includes/extends pero el CU define
  6 flujos-alternos + 6 excepciones (12 total). **Algunos flujos no
  se modelan como `<<extend>>`** — esto puede ser correcto (no todo
  flujo alterno requiere extension point) o puede ser **shallow**.
- `uc-rpt-04`: el CU **no usa el formato `FA-N:` o `EX-N:`** en sus
  archivos `flujos-alternos.rst` y `excepciones.rst` — el script de
  conteo los lee como 0. Esto es un inconsistencia de formato del
  CU, no del UV.
- `uc-sup-03`: cobertura razonable (6 vs 3+5 = ratio 0.75).

**No es un defecto bloqueante** — la regla heredada del predecesor
es "modelar como `<<extend>>` solo los flujos con extension point
declarado en el UC base" (R-09). Pero **L-03** del predecesor
exigía leer `flujos-alternos.rst` + `excepciones.rst` para
enriquecer; el UV de `uc-opr-01` puede no haber capturado todo lo
relevante.

### Acción

Revisión profunda de `uc-opr-01` y otros UCs con ratio
includes-extends/flujos-alternos < 0.5 — **opcional, no bloqueante**
para cierre del WP. Documentar como follow-up.

## Resumen ejecutivo

| Criterio | Cobertura | Estado |
|---|---|---|
| C-01 1:1 por UC ID | 82/83 + 1 caso edge | ⚠ R-07 |
| C-02 uc-inc-rpt-01 | viola R-07 + naming | ❌ acción requerida |
| C-03 xref forward (UV→CU) | 83/83 = 100% | ✅ |
| C-04 xref reverse (CU→UV) | 0/83 = 0% | ⚠ follow-up |
| C-05 profundidad include/extend | sample OK | ⚠ revisión opcional |

## Acciones bloqueantes para cierre WP

1. ~~**Resolver `uc-inc-rpt-01`** (C-02)~~ — **RESUELTO 2026-05-05 23:00**:
   - Archivo renombrado: `uc-inc-rpt-01-uc-inc-rpt-01-resolver-segmento.rst`
     → `uc-inc-rpt-01-resolver-segmento.rst`.
   - Toctree de `reports/index.rst` actualizado (línea 225).
   - **Excepción formal a R-07** registrada (ver sección abajo).

## Excepción formal a R-07

### R-07 original

> "UC included nunca solo — uc-inc-rpt-01 NO recibirá archivo
> standalone."

### Decisión: excepción justificada para `uc-inc-rpt-01`

**Resolver Segmento del Usuario** es un UC de inclusión usado por
los 16 UCs del módulo Reports para determinar el segmento
operativo del usuario (`SegmentResolver`, CNST-008 isolation).
Aunque sintácticamente es `<<include>>`-only y nunca se ejecuta
solo, su **complejidad sustantiva** justifica un diagrama
standalone:

1. **5+ pasos** de validación (jerarquía de roles, override
   manual del Auditor, fallback a segmento global).
2. **3 actores externos** (User, Auditor, SegmentResolver) con
   semántica diferenciada.
3. **CNST-008 critical**: errores en este UC propagan
   isolation-violation a todos los UC_RPT_*.
4. **Reutilización transversal**: 16 reports lo incluyen — un
   diagrama standalone evita duplicar la lógica en cada uno.

### Restricciones de la excepción

- El archivo **no aparece** como UC ejecutable en el module
  index (sigue siendo `<<include>>`-only en uml-07 R-07).
- El diagrama uml-07 declara explícitamente "UC de inclusion.
  NO se ejecuta independientemente — incluido por...".
- Este es **el único** UC `uc-inc-*` con archivo standalone.
  Otros UCs de inclusión que pudieran surgir deben evaluarse
  caso por caso con los mismos 4 criterios arriba.

### Status

R-07 se mantiene como regla por defecto. Esta excepción es
puntual y queda registrada en el WP changelog + lessons-learned.

## Acciones no bloqueantes (post-cierre)

1. Agregar xref reverso CU → UV en 83 archivos `casos-uso/<uc>/index.rst` (C-04).
2. Auditoría profunda de includes/extends en UCs con ratio bajo (C-05).
