```yml
created_at: 2026-05-07 04:55:00
project: IACT-docs
work_package: 2026-05-07-04-50-49-std-012-prefix-normalization
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Inventario + Plan de Ejecución — STD-012 v1.1.0

> Cuantificacion exacta del alcance de la operacion antes
> de Phase 7. Ejecutor pidio: *"realiza un analisis de
> cuantos se van a actualizar"*.

## Sección 1 — Resumen ejecutivo

.. list-table::
 :widths: 35 15 50
 :header-rows: 1

 * - Metrica
   - Cantidad
   - Detalle
 * - Total archivos legacy en ``diagramas-uml/``
   - **195**
   - sin prefijo ``diagrama-de-``
 * - Legacy con contenido de diagrama
   - **193**
   - tienen ``@startuml`` o ``.. uml::``
 * - Legacy auxiliares (no diagrama)
   - **2**
   - texto narrativo, NO renombrar
 * - **Tipo A: DELETE** (legacy con par canonical)
   - **49**
   - solo ``caso-de-uso.rst``
 * - **Tipo B: RENAME** (legacy sin par canonical)
   - **144**
   - todos los demas tipos
 * - Toctree (``index.rst``) afectados
   - **50**
   - de los 85 totales
 * - Cross-refs externos
   - **0**
   - cero referencias fuera de ``diagramas-uml/``
 * - Archivos canonicos existentes (mantener)
   - **192**
   - con prefijo ``diagrama-de-`` ya correcto

**Total operaciones de archivo:**

- 49 deletes
- 144 renames (git mv)
- 50 toctree updates
- 1 update normativo (STD-012 v1.0.0 → v1.1.0)

**Riesgo de cross-refs rotos:** **bajo** — STD-012 mismo es
la unica referencia externa al patron legacy.

## Sección 2 — Inventario detallado por tipo

### 2.1 Tipo A — DELETE (49 archivos)

| Pattern | Count | Justification |
|---|---|---|
| ``caso-de-uso.rst`` con ``diagrama-de-caso-de-uso.rst`` en mismo dir | 49 | El canonical contiene info mas rica (codenames RBAC vs roles, includes/extends explicitos). Verificado en muestras uc-adm-01/02/03. |

**Distribucion por cluster:**

::

   admin: 3 (uc-adm-01, 02, 03)
   alerts: 5 (uc-alr-01..05)
   audit: 4 (uc-aud-01..04)
   caller: 5 (uc-cli-01..05)
   logs: 7 (uc-log-01..07)
   operator: 9
   pipeline: 4
   reports: 9
   supervision: 3

   Total: 49

**Acción:** ``git rm`` los 49 archivos.

### 2.2 Tipo B — RENAME (144 archivos)

#### B.1 — Tipos principales (90 archivos)

| Source pattern | Target pattern | Count |
|---|---|---|
| ``actividad.rst`` | ``diagrama-de-actividad.rst`` | 46 |
| ``secuencia.rst`` | ``diagrama-de-secuencia.rst`` | 24 |
| ``clases.rst`` | ``diagrama-de-clases.rst`` | 14 |
| ``componentes.rst`` | ``diagrama-de-componentes.rst`` | 6 |

#### B.2 — Estados (23 archivos)

| Source | Target | Count |
|---|---|---|
| ``estado.rst`` (singular) | ``diagrama-de-estado.rst`` | 6 |
| ``estado-{descripcion}.rst`` | ``diagrama-de-estado-{descripcion}.rst`` | 14 |
| ``estados-{descripcion}.rst`` | ``diagrama-de-estados-{descripcion}.rst`` | 3 |

Ejemplos especificos:

- ``estado-de-la-llamada.rst`` (×2) →
  ``diagrama-de-estado-de-la-llamada.rst``
- ``estado-funcion.rst`` →
  ``diagrama-de-estado-funcion.rst``
- ``estado-sod-rule.rst`` →
  ``diagrama-de-estado-sod-rule.rst``
- ``estados-exceptionalpermission.rst`` →
  ``diagrama-de-estados-exceptionalpermission.rst``

#### B.3 — Variantes con sufijo (~31 archivos)

Por familia:

::

   actividad-aplicar.rst         → diagrama-de-actividad-aplicar.rst
   actividad-cold.rst            → diagrama-de-actividad-cold.rst
   actividad-compartir.rst       → diagrama-de-actividad-compartir.rst
   actividad-crear.rst           → diagrama-de-actividad-crear.rst
   actividad-warm.rst            → diagrama-de-actividad-warm.rst

   secuencia-detalle.rst         → diagrama-de-secuencia-detalle.rst
   secuencia-de-exportacion-de-logs.rst
                                  → diagrama-de-secuencia-de-exportacion-de-logs.rst
   secuencia-de-exportacion-de-audit-log.rst
                                  → diagrama-de-secuencia-de-exportacion-de-audit-log.rst
   secuencia-de-consulta-pipeline-log.rst
                                  → diagrama-de-secuencia-de-consulta-pipeline-log.rst
   secuencia-con-tail-sse.rst    → diagrama-de-secuencia-con-tail-sse.rst
   secuencia-push.rst            → diagrama-de-secuencia-push.rst
   secuencia-urgente.rst         → diagrama-de-secuencia-urgente.rst
   secuencia-warm.rst            → diagrama-de-secuencia-warm.rst

   componente-fts.rst            → diagrama-de-componente-fts.rst
   componentes-export.rst        → diagrama-de-componentes-export.rst
   componentes-pipeline-log.rst  → diagrama-de-componentes-pipeline-log.rst

   pipeline.rst                  → diagrama-de-pipeline.rst
   pipeline-pii.rst              → diagrama-de-pipeline-pii.rst
   pipeline-metricas.rst         → diagrama-de-pipeline-metricas.rst
   pipeline-de-infraestructura.rst
                                  → diagrama-de-pipeline-de-infraestructura.rst

   flujo-de-firma.rst            → diagrama-de-flujo-de-firma.rst
   flujo-de-anonimizacion-etl.rst
                                  → diagrama-de-flujo-de-anonimizacion-etl.rst

   distribucion-de-menus.rst     → diagrama-de-distribucion-de-menus.rst
   diagrama-agr-como-agregacion.rst
                                  → diagrama-de-agr-como-agregacion.rst (rename del prefijo "diagrama-" a "diagrama-de-")

   caso-de-uso-relacion-de-inclusion.rst
                                  → diagrama-de-caso-de-uso-relacion-de-inclusion.rst

   verify.rst                    → diagrama-de-verify.rst (auditoria)
   tree.rst                      → diagrama-de-tree.rst
   tail.rst                      → diagrama-de-tail.rst
   modes.rst                     → diagrama-de-modes.rst (×2)
   impacto.rst                   → diagrama-de-impacto.rst

### 2.3 Excluidos del rename (2 archivos)

| Archivo | Razon |
|---|---|
| ``notas-sobre-los-diagramas.rst`` | Texto narrativo, no diagrama UML |
| ``tail-sse.rst`` (uc-log-07) | No contiene ``@startuml`` — es texto/codigo |

## Sección 3 — Toctree afectados (50 archivos)

Cada UC con un archivo legacy renombrado/eliminado tiene
su ``diagramas-uml/index.rst`` que referencia el nombre
legacy en su toctree. Ejemplos:

.. code-block:: rst

   .. toctree::
    :maxdepth: 1

    diagrama-de-caso-de-uso
    caso-de-uso          ← eliminar esta linea (Tipo A delete)
    actividad            ← cambiar a diagrama-de-actividad (Tipo B rename)

Distribucion (50 toctree afectados de 85 totales — los
35 restantes ya tienen solo nombres canonicos):

- admin: 5 (todos los uc-adm tienen pares legacy)
- alerts: 5
- audit: 4
- caller: 5
- logs: 7
- operator: 10
- pipeline: 4
- reports: 8
- supervision: 2

## Sección 4 — Cross-refs externos

Verificacion ejecutada:

.. code-block:: bash

   grep -rnE "diagramas-uml/(caso-de-uso|actividad|\
   secuencia|clases|estado|componentes)\b" \
     source/ --include="*.rst" \
     | grep -v "/diagramas-uml/"

**Resultado: 0 referencias fuera de ``diagramas-uml/``.**

La unica referencia externa documentada es ``STD-012``
mismo (en su tabla de tipos de diagrama), que se actualiza
con el cambio normativo.

**Riesgo de breakage:** muy bajo.

## Sección 5 — Archivos canonicos existentes (preservar)

192 archivos ya con prefijo correcto, distribuidos:

.. list-table::
 :widths: 50 25 25
 :header-rows: 1

 * - Pattern canonico
   - Count
   - Estado
 * - ``diagrama-de-caso-de-uso.rst``
   - 85
   - Preservar (incluye 49 que reemplazan delete + 36 ya solos)
 * - ``diagrama-de-actividad.rst``
   - 31
   - Preservar
 * - ``diagrama-de-secuencia.rst``
   - 25
   - Preservar
 * - ``diagrama-de-clases.rst``
   - 6
   - Preservar
 * - ``diagrama-de-estado.rst``
   - 5
   - Preservar
 * - ``diagrama-de-coexistencia-acc-perm.rst``
   - 3
   - Preservar
 * - ``diagrama-de-secuencia-listado.rst``
   - 2
   - Preservar
 * - ``diagrama-de-estados-user-state.rst``
   - 2
   - Preservar
 * - ``diagrama-de-estados-user-first-login.rst``
   - 2
   - Preservar
 * - ``diagrama-de-estados-exceptionalpermission.rst``
   - 2
   - Preservar
 * - Otros con prefijo (1 cada uno)
   - 29
   - Preservar

## Sección 6 — Plan de ejecucion en 2 commits

### Commit 1 — Cambio normativo (STD-012 v1.1.0)

**Archivos modificados:** 1

- ``source/normativa/estandares/std-012-tipos-de-diagramas-uml.rst``:
  bumpear version 1.0.0 → 1.1.0; modificar **unicamente**
  las secciones de nomenclatura para incluir prefijo
  obligatorio; agregar nota explicita en historial sobre
  el motivo (alineamiento con STD-011 + practica reciente).

**Sin cambios** a:

- Archivos de UCs.
- Toctrees.
- Otros STDs.

**Mensaje del commit:** explica la decision Opcion B,
referencia el WP previo donde se detecto la inconsistencia,
referencia STD-011.

**Build check:** strict EXIT=0 (esperado — solo cambia un
archivo de norma sin cross-refs rotos).

### Commit 2 — Operaciones de archivo

**Operaciones:**

- ``git rm`` × 49 archivos legacy de tipo ``caso-de-uso.rst``.
- ``git mv`` × 144 archivos legacy → con prefijo
  ``diagrama-de-``.
- Modificar 50 ``diagramas-uml/index.rst`` para
  actualizar toctrees.

**Mensaje del commit:** explicito sobre la operacion en
masa, refleja la lista canonica de pares deleted +
renamed por tipo, cita STD-012 v1.1.0 (commit 1) como
respaldo normativo.

**Build check:** strict EXIT=0 obligatorio.

### Por que 2 commits separados

Condicion explicita del ejecutor: *"el commit de
actualizacion de STD-012 sea separado del commit de
renombrado de archivos para que el historico sea
auditable"*.

Beneficios:

- ``git log -- source/normativa/`` muestra solo el cambio
  normativo.
- ``git log -- source/requisitos/`` muestra solo el
  cambio de archivos.
- ``git revert`` puede aplicarse a uno sin tocar el otro
  (e.g., revertir las operaciones de archivo manteniendo
  la actualizacion normativa).

## Sección 7 — Sub-clusters de ejecucion del Commit 2

Para reducir el riesgo de errores, ejecutar las
operaciones en lotes verificados:

.. list-table::
 :widths: 8 30 12 50
 :header-rows: 1

 * - Lote
   - Operacion
   - Archivos
   - Verificacion
 * - L-1
   - Delete 49 ``caso-de-uso.rst`` (Tipo A)
   - 49 deletes
   - canonical existe en mismo dir
 * - L-2
   - Rename 46 ``actividad.rst`` → canonical
   - 46 renames
   - dest no existe en mismo dir
 * - L-3
   - Rename 24 ``secuencia.rst`` → canonical
   - 24 renames
   - dest no existe en mismo dir
 * - L-4
   - Rename 14 ``clases.rst`` → canonical
   - 14 renames
   - dest no existe en mismo dir
 * - L-5
   - Rename 6 ``componentes.rst`` → canonical
   - 6 renames
   - dest no existe en mismo dir
 * - L-6
   - Rename estados (6 + 14 + 3 = 23)
   - 23 renames
   - dest no existe en mismo dir
 * - L-7
   - Rename variantes con sufijo (~31)
   - ~31 renames
   - dest no existe en mismo dir
 * - L-8
   - Update 50 toctree
   - 50 modificaciones
   - sphinx build EXIT=0

**Total operaciones del commit 2:** 49 + 144 = **193
operaciones de archivo + 50 toctree updates.**

## Sección 8 — Riesgos identificados

### R-1 (Bajo): conflicto de rename si dest existe

**Mitigacion:** la verificacion previa muestra que ningun
archivo legacy comparte directorio con su contraparte
canonico. Si por algun caso aparece (e.g., bug en un
WP previo), el ``git mv`` falla y se aborta el lote.

### R-2 (Bajo): toctree con sintaxis fuera de patron

**Mitigacion:** strict build detecta references rotas. Si
algun toctree tiene formato inusual (e.g., con `:caption:`
o leading spaces no estandar), el lote L-8 lo detecta.

### R-3 (Bajo): archivos auxiliares mal categorizados

**Mitigacion:** ya hice grep por ``@startuml``. Los 2
archivos sin diagrama estan identificados explicitamente
y excluidos. Si surge ambiguedad en otro archivo (e.g.,
``flujo-de-firma.rst`` tiene tanto texto como diagrama),
inspecion manual antes del rename.

### R-4 (Muy bajo): cross-ref externo no detectado

**Mitigacion:** grep verifico cero refs externas. Si
aparece alguna durante el build, error sphinx la detecta
y el commit 2 no se completa.

## Sección 9 — Items para SP-01 (decision del ejecutor)

Antes de ejecutar Phase 7, confirmar:

1. **¿Apruebas el plan de 2 commits separados** (commit 1
   normativo + commit 2 operaciones)?
2. **¿Apruebas los 144 renames + 49 deletes** segun la
   distribucion documentada?
3. **¿Apruebas la exclusion** de los 2 archivos
   auxiliares (``notas-sobre-los-diagramas.rst``,
   ``tail-sse.rst``)?
4. **¿Apruebas el wording del cambio normativo** STD-012
   v1.1.0 (a redactar en Phase 5/7)?

## Refs

- WP previo:
  ``2026-05-07-04-08-13-use-case-view-analysis``
  (G-CU-06 escindido aqui).
- Inconsistencia detectada: STD-011 vs STD-012.
- Decision del ejecutor: Opcion B — actualizar STD-012.
- Build: ``make html SPHINXOPTS='-W -j auto'`` debe
  retornar EXIT=0 tras cada commit.
