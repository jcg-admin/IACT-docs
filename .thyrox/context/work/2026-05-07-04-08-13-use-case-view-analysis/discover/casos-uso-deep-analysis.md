```yml
created_at: 2026-05-07 04:30:00
project: IACT-docs
work_package: 2026-05-07-04-08-13-use-case-view-analysis
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
parent: discover/use-case-view-audit.md
```

# Deep Analysis — source/requisitos/casos-uso/

> Auditoria profunda del cajon de UCs paralelo a
> ``use-case-view/``. 1503 archivos rst en 85 UCs distribuidos
> en 13 clusters.

## Sección 1 — Inventario

### 1.1 Estructura

::

   source/requisitos/casos-uso/
   ├── index.rst
   ├── access/        (7 UCs: 01-05, 08, 09)
   ├── admin/         (5 UCs: 01-05, todos en Borrador)
   ├── alerts/        (5 UCs)
   ├── audit/         (4 UCs)
   ├── auth/          (5 UCs)
   ├── caller/        (5 UCs)
   ├── logs/          (7 UCs)
   ├── operator/      (10 UCs, todos Reservado)
   ├── permissions/   (10 UCs)
   ├── pipeline/      (4 UCs)
   ├── reports/       (16 UCs)
   ├── supervision/   (3 UCs, todos Reservado)
   └── users/         (4 UCs)

   Total: 85 UCs, 1503 archivos rst.

### 1.2 Distribucion por estado

.. list-table::
 :widths: 15 12 12 12 12 12 25
 :header-rows: 1

 * - Cluster
   - Borrador
   - Vigente
   - Aprobado
   - Reservado
   - Sin estado
   - Notas
 * - access
   - 0
   - 7
   - 0
   - 0
   - 0
   - completo
 * - **admin**
   - **5**
   - **0**
   - **0**
   - **0**
   - **0**
   - **TODOS Borrador (incluye UC_ADM_01/02/03 v5.6.0
     baseline + UC_ADM_04/05 v5.6.x extension)**
 * - alerts
   - 0
   - 5
   - 0
   - 0
   - 0
   - completo
 * - audit
   - 0
   - 4
   - 0
   - 0
   - 0
   - completo
 * - auth
   - 0
   - 5
   - 0
   - 0
   - 0
   - completo
 * - caller
   - 0
   - 5
   - 0
   - 0
   - 0
   - completo
 * - logs
   - 0
   - 7
   - 0
   - 0
   - 0
   - completo
 * - **operator**
   - 0
   - 0
   - 0
   - **10**
   - 0
   - todos Reservado v5.6.0 (out-of-scope)
 * - permissions
   - 0
   - 10
   - 0
   - 0
   - 0
   - completo
 * - pipeline
   - 0
   - 4
   - 0
   - 0
   - 0
   - completo
 * - reports
   - 0
   - 15
   - 0
   - 0
   - **1**
   - **uc-inc-rpt-01 sin :estado: ni :version:**
 * - **supervision**
   - 0
   - 0
   - 0
   - **3**
   - 0
   - todos Reservado v5.6.0 (out-of-scope)
 * - users
   - 0
   - 4
   - 0
   - 0
   - 0
   - completo
 * - **Total**
   - **5**
   - **66**
   - **0**
   - **13**
   - **1**
   - 85

## Sección 2 — Gaps detectados

### G-CU-01 (Crítico): cluster admin TODO en Borrador

**Archivos:** los 5 UCs del cluster admin tienen
``:estado: Borrador``.

**Problema:** UC_ADM_01/02/03 son del baseline v5.6.0, ya
mergeados a main hace tiempo. UC_ADM_04/05 son del v5.6.x
extension recien creado. Todos siguen en Borrador.

**Causa raiz:** los 3 baseline (v5.6.0) estan estancados en
Borrador desde su creacion; los 2 nuevos heredaron el estado
inicial.

**Severidad:** Critico — el cluster admin es el plano de
configuracion del modelo RBAC; quedar en Borrador
permanentemente bloquea cualquier flujo de aprobacion
formal.

### G-CU-02 (Crítico): UC_INC_RPT_01 sin metadata

**Archivo:** ``source/requisitos/casos-uso/reports/uc-inc-rpt-01/index.rst``.

**Problema:** ``:estado:`` y ``:version:`` ausentes
(unico UC del corpus con esta condicion).

**Severidad:** Critico — quiebra patron de metadata global.

### G-CU-03 (Crítico): UC_ADM_04 / UC_ADM_05 sin diagrama-de-caso-de-uso

**Archivos:**

- ``source/requisitos/casos-uso/admin/uc-adm-04/diagramas-uml/``
- ``source/requisitos/casos-uso/admin/uc-adm-05/diagramas-uml/``

**Problema:** los 2 UCs nuevos (creados en WP previo) tienen
solo ``diagrama-de-secuencia.rst`` y ``diagrama-de-actividad.rst``
(o ``diagrama-de-estados.rst`` para UC_ADM_05). **Falta el
``diagrama-de-caso-de-uso.rst``** que es el uml-07 estandar
documentado en STD-011 y CNST-033.

**Comparacion:**

- UC_ACC_02 (estandar): 4 diagramas (caso-de-uso, secuencia,
  actividad, transicion-state).
- UC_ADM_04/05 (faltantes): 2 diagramas (sec, act/estados).

**Severidad:** Critico — diagrama-de-caso-de-uso es el uml-07
canonico (no es el de secuencia). Sin el, el UC no tiene
representacion estatica de actores + casos de uso vinculados.

### G-CU-04 (Crítico): UC_LOG_03 sin criterios-aceptacion

**Archivo:** ``source/requisitos/casos-uso/logs/uc-log-03/``.

**Problema:** falta ``criterios-aceptacion.rst`` (16 archivos
en lugar de 17).

**Severidad:** Critico — sin CA, el UC no tiene Given/When/Then
verificables.

### G-CU-05 (Crítico): UC_INC_RPT_01 sin criterios-aceptacion ni testing

**Archivo:** ``source/requisitos/casos-uso/reports/uc-inc-rpt-01/``.

**Problema:** faltan 2 archivos — ``criterios-aceptacion.rst``
y ``testing.rst``. Solo 15 archivos.

**Severidad:** Critico — UC sin CA ni tests es spec
incompleta.

### G-CU-06 (Importante): Nomenclatura inconsistente de diagramas

**Patron detectado:** 49 UCs tienen **pares duplicados**:

- ``caso-de-uso.rst`` (legacy: actor por nombre de rol,
  usa aliases cortos `admin`, `Create`).
- ``diagrama-de-caso-de-uso.rst`` (canonico per CNST-033 +
  STD-011: actor por codename de Function).

Los 49 pares NO son duplicado de contenido — son **dos
versiones del mismo diagrama** (legacy + canonico) que
coexisten en el toctree.

3 UCs tambien tienen ``actividad.rst`` (legacy) +
``diagrama-de-actividad.rst`` (canonico):

- UC_ADM_01, UC_ADM_02, UC_ADM_03 (cluster admin baseline).

**Severidad:** Importante — deuda tecnica de nomenclatura. La
existencia de la version legacy puede causar confusion. Pero
removerla rompe cross-refs si hay alguno.

### G-CU-07 (Crítico): UCs referenciados sin directorio

**4 UCs huerfanos referenciados:**

.. list-table::
 :widths: 20 50 30
 :header-rows: 1

 * - UC referenciado
   - Donde se cita
   - Estado
 * - ``UC_USR_05``
   - permissions/uc-perm-07/testing.rst,
     permissions/uc-perm-09/informacion-general.rst,
     auth/uc-auth-04/flujos-alternos.rst
   - **No existe directorio**
 * - ``UC_USR_06``
   - similares
   - **No existe directorio**
 * - ``UC_USR_07``
   - similares
   - **No existe directorio**
 * - ``UC_ACC_06``
   - users/uc-usr-02/informacion-general.rst
   - **No existe directorio**

**Cluster ACC tiene gap de numeracion:** uc-acc-01..05, 08,
09. Faltan 06 y 07.

**Cluster USR tiene 4 UCs:** uc-usr-01..04. UC_USR_05/06/07
referenciados pero no existen.

**Severidad:** Critico — referencias muertas. Pueden ser:

(a) UCs eliminados sin actualizar referencias.

(b) UCs reservados/futuros referenciados como si existieran.

(c) Errores de typo en las referencias.

### G-CU-08 (Bajo): TBD / TODO en 40 archivos

40 archivos contienen ``TBD``, ``TODO``, ``FIXME`` o
``pendiente``. Mayoria en uc-inc-rpt-01 (3 archivos),
uc-aud-01, uc-adm-05, uc-acc-03.

**Severidad:** Bajo — son TODOs reales pero pre-existentes,
no creados en WPs recientes.

## Sección 3 — Hallazgos positivos

### P-CU-1: Estructura uniforme

El estandar de 12 secciones core (informacion-general,
actores-precondiciones, flujo-principal, flujos-alternos,
excepciones, requisitos-no-funcionales, datos-involucrados,
diagramas-uml/, criterios-aceptacion, patrones-diseno,
implementacion-tecnica, testing) se respeta en **80 de los 85
UCs** (94%). Excepciones: G-CU-03, G-CU-04, G-CU-05.

### P-CU-2: STD-010 conformidad alta

0 violaciones de STD-010 fuera de implementacion-tecnica.rst
y testing.rst. Resultado del WP hermano
``2026-05-06-23-25-08-std-010-corpus-compliance``.

### P-CU-3: 13 clusters con paridad casos-uso ↔ use-case-view

100% paridad confirmada por inventario (ver
``discover/use-case-view-audit.md`` §2.2).

### P-CU-4: Reservados explicitos

OPR (10) y SUP (3) tienen ``:estado: Reservado`` consistente
— no se trata como Vigente por error.

## Sección 4 — Decisiones arquitectonicas pendientes

Antes de Phase 5/7 del WP, el ejecutor debe decidir:

### D-CU-001: Politica de transicion Borrador → Vigente

**Pregunta:** ¿se promueven los 5 UCs del cluster admin de
Borrador a Vigente en este WP, o requiere un proceso de
revision separado?

**Opciones:**

a. **Promover todos** (UC_ADM_01..05) a Vigente en este WP
   tras verificacion de completitud.
b. **Promover solo baseline** (UC_ADM_01..03) — UC_ADM_04/05
   estan tan recien creados que merecen ciclo de revision.
c. **Diferir promocion** — abrir WP separado para revision
   de promociones masivas.

**Recomendacion:** opcion **a** condicionada a resolver
G-CU-03 primero (UC_ADM_04/05 sin diagrama-de-caso-de-uso).

### D-CU-002: Politica de nomenclatura legacy

**Pregunta:** ¿que hacer con los pares
``caso-de-uso.rst`` + ``diagrama-de-caso-de-uso.rst``?

**Opciones:**

a. **Mantener ambos** (status quo) — versiones complementarias
   con audiencias distintas.
b. **Eliminar legacy** (``caso-de-uso.rst``,
   ``actividad.rst``) — solo conservar nombres canonicos.
c. **Renombrar legacy** a algo explicito como
   ``caso-de-uso-rol-friendly.rst`` para indicar que es la
   version "para humanos".

**Recomendacion:** opcion **b** — eliminar legacy. Los nombres
no canonicos son fuente de confusion. CNST-033 + STD-011
prescriben la version canonica. Si se necesita una vista
"rol-friendly", convertirla a una seccion de
``diagrama-de-caso-de-uso.rst`` con dos diagramas en el mismo
archivo.

### D-CU-003: UC_USR_05/06/07 y UC_ACC_06 — 4 referencias muertas

**Pregunta:** ¿son UCs futuros, eliminados, o errores?

**Investigacion requerida:**

1. ``git log -- source/requisitos/casos-uso/users/`` —
   ¿hubo UCs USR_05/06/07 que se eliminaron?
2. ``git log -- source/requisitos/casos-uso/access/uc-acc-06`` —
   ¿existio alguna vez?

**Opciones:**

a. Si nunca existieron: corregir referencias (typo o ID
   incorrecto).
b. Si fueron eliminados: actualizar referencias a los UCs
   reemplazo.
c. Si son futuros (reservados): crear directorios placeholder
   con ``:estado: Reservado``.

**Recomendacion:** abrir investigacion en Phase 3 ANALYZE.

### D-CU-004: Promover UC_INC_RPT_01

**Pregunta:** ¿completar y promover, o evaluar si sigue
siendo necesario?

**Opciones:**

a. Completar metadata + criterios-aceptacion + testing en
   este WP, promover a Vigente.
b. Marcar como Borrador hasta entender si es UC vigente.
c. Si esta deprecado, abrir WP de remocion.

**Recomendacion:** investigar antes de actuar.

## Sección 5 — Plan correctivo propuesto

### Tier 1 — Correcciones criticas (G-CU-01 a G-CU-05, G-CU-07)

1. Promover cluster admin de Borrador a Vigente (D-CU-001).
2. Resolver UC_INC_RPT_01 (D-CU-004): completar metadata +
   2 archivos faltantes.
3. Crear ``diagrama-de-caso-de-uso.rst`` para UC_ADM_04/05
   (G-CU-03).
4. Crear ``criterios-aceptacion.rst`` para UC_LOG_03 (G-CU-04).
5. Investigar y resolver 4 referencias muertas (D-CU-003).

### Tier 2 — Importante (G-CU-06)

6. Decidir y aplicar D-CU-002 (eliminacion o conservacion
   de legacy).

### Tier 3 — Bajo

7. Auditar 40 TODOs/TBDs y clasificar por categoria.

## Sección 6 — Estimación volumen

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Tier
   - Acciones
   - Volumen
 * - Tier 1
   - Promociones (5 UCs metadata),
     2 archivos nuevos UC_ADM_04/05,
     1 archivo nuevo UC_LOG_03,
     2 archivos UC_INC_RPT_01,
     investigacion git de 4 refs
   - Mediano
 * - Tier 2 (si Opcion B)
   - 49 archivos eliminados +
     toctree updates
   - Mediano
 * - Tier 3
   - Auditar 40 archivos
   - Pequeño

**Total alcance:** mediano-alto.

## Sección 7 — Stakeholders y stopping points

- **SP-01 (humano):** aprobar opciones de D-CU-001..004
  antes de Phase 7.
- **SP-02:** strict build EXIT=0 tras cada lote.
- **SP-03 (humano):** aprobar promociones masivas de
  Borrador → Vigente.

## Sección 8 — Items consolidados (use-case-view + casos-uso)

Este WP cubre dos cajones paralelos. Gaps consolidados:

.. list-table::
 :widths: 12 25 12 50
 :header-rows: 1

 * - ID
   - Cajon afectado
   - Severidad
   - Resumen
 * - G-UV-01
   - use-case-view
   - Critico
   - index.rst dice "83 UCs" — debe 85
 * - G-UV-02
   - use-case-view
   - Medio
   - STD-010 violations en 3 archivos
 * - G-UV-03
   - use-case-view
   - Critico
   - mapa-funciones-rbac sin v5.6.x
 * - G-UV-04
   - use-case-view
   - Critico
   - panorama-iact sin MenuItem
 * - G-CU-01
   - casos-uso
   - Critico
   - 5 UCs admin en Borrador
 * - G-CU-02
   - casos-uso
   - Critico
   - UC_INC_RPT_01 sin metadata
 * - G-CU-03
   - casos-uso
   - Critico
   - UC_ADM_04/05 sin diagrama-de-caso-de-uso
 * - G-CU-04
   - casos-uso
   - Critico
   - UC_LOG_03 sin criterios-aceptacion
 * - G-CU-05
   - casos-uso
   - Critico
   - UC_INC_RPT_01 sin CA ni testing
 * - G-CU-06
   - casos-uso
   - Importante
   - 49 pares legacy/canonico de diagramas
 * - G-CU-07
   - casos-uso
   - Critico
   - 4 UCs referenciados sin directorio
 * - G-CU-08
   - casos-uso
   - Bajo
   - 40 archivos con TBD/TODO/FIXME

**Total gaps:** 12 (4 use-case-view + 8 casos-uso). 8 criticos,
2 importantes/medios, 2 bajos.

## Refs

- ``discover/use-case-view-audit.md``.
- WP previo: ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``
  (cerrado).
- WP hermano: ``2026-05-06-23-25-08-std-010-corpus-compliance``
  (cerrado, alineo STD-010 en casos-uso).
- STD-010, STD-011, CNST-033.
- Catalogo: ``source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst``.
