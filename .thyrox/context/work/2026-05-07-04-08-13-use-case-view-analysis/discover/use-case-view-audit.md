```yml
created_at: 2026-05-07 04:15:00
project: IACT-docs
work_package: 2026-05-07-04-08-13-use-case-view-analysis
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Use-Case View — Auditoría Phase 1 DISCOVER

> Inventario completo + gap analysis + recomendaciones para
> ``source/arquitectura-tecnica/use-case-view/``.

## Sección 1 — Metodología

5 verificaciones ejecutadas con grep/find/wc:

1. Inventario de archivos por cluster.
2. Cross-check ``casos-uso/`` ↔ ``use-case-view/``.
3. Conformidad STD-010 (vocabulario abstracto).
4. Conformidad STD-011 (aliases).
5. Consistencia de conteos / referencias v5.6.x.

## Sección 2 — Inventario

### 2.1 Estructura

::

   source/arquitectura-tecnica/use-case-view/
   ├── index.rst                  (master index)
   ├── panorama-iact.rst          (vista transversal high-level)
   ├── mapa-funciones-rbac.rst    (mapa cluster → funciones)
   ├── access/      (8 archivos: 7 UC + index)
   ├── admin/       (6 archivos: 5 UC + index)  ← v5.6.x updated
   ├── alerts/      (6 archivos: 5 UC + index)
   ├── audit/       (5 archivos: 4 UC + index)
   ├── auth/        (6 archivos: 5 UC + index)
   ├── caller/      (6 archivos: 5 UC + index)
   ├── logs/        (8 archivos: 7 UC + index)
   ├── operator/    (11 archivos: 10 UC + index)
   ├── permissions/ (11 archivos: 10 UC + index)
   ├── pipeline/    (5 archivos: 4 UC + index)
   ├── reports/     (17 archivos: 16 UC + index)
   ├── supervision/ (4 archivos: 3 UC + index)
   └── users/       (5 archivos: 4 UC + index)

   Total: 101 archivos rst, 85 UCs.

### 2.2 Cross-check casos-uso ↔ use-case-view

.. list-table::
 :widths: 20 15 25 40
 :header-rows: 1

 * - Cluster
   - casos-uso/
   - use-case-view/
   - Estado paridad
 * - access
   - 7
   - 7
   - PARIDAD
 * - admin
   - 5
   - 5
   - PARIDAD (v5.6.x extension aplicada)
 * - alerts
   - 5
   - 5
   - PARIDAD
 * - audit
   - 4
   - 4
   - PARIDAD
 * - auth
   - 5
   - 5
   - PARIDAD
 * - caller
   - 5
   - 5
   - PARIDAD
 * - logs
   - 7
   - 7
   - PARIDAD
 * - operator
   - 10
   - 10
   - PARIDAD (cluster reservado v5.6.0)
 * - permissions
   - 10
   - 10
   - PARIDAD
 * - pipeline
   - 4
   - 4
   - PARIDAD
 * - reports
   - 16
   - 16
   - PARIDAD
 * - supervision
   - 3
   - 3
   - PARIDAD (cluster reservado v5.6.0)
 * - users
   - 4
   - 4
   - PARIDAD
 * - **Total**
   - **85**
   - **85**
   - PARIDAD

**Hallazgo positivo P-1:** paridad estructural perfecta
casos-uso ↔ use-case-view en todos los 13 clusters.

### 2.3 Conteo cross-check vs matriz-dependencias

Matriz declara total 85 UCs (post-Phase 11 cierre del WP
anterior). use-case-view aporta 85. **Coinciden.**

## Sección 3 — Gaps detectados

### G-UV-01 (Crítico): index.rst declara "83 UCs"

**Archivo:** ``source/arquitectura-tecnica/use-case-view/index.rst``
linea 25.

**Texto actual:**

   *"13 módulos, 1 diagrama por módulo, 83 UCs cubiertos en
   total."*

**Problema:** el conteo "83 UCs" esta desactualizado.
Inventario actual: **85 UCs** (los 2 nuevos UC_ADM_04 y
UC_ADM_05 del WP anterior fueron agregados pero el conteo
no se actualizo).

**Severidad:** Critico — discrepancia visible al lector.

### G-UV-02 (Medio): STD-010 violations en 3 archivos

.. list-table::
 :widths: 35 12 25 28
 :header-rows: 1

 * - Archivo
   - Linea
   - Termino prohibido
   - Sustitucion canonica
 * - ``panorama-iact.rst``
   - 126
   - "cron / APScheduler dispara"
   - "el Planificador de Tareas dispara"
 * - ``pipeline/index.rst``
   - 61
   - "Scheduler: actor sistema (cron / APScheduler)"
   - "Planificador de Tareas: actor sistema"
 * - ``audit/index.rst``
   - 20
   - "``audit_log`` (PostgreSQL)"
   - "``audit_log`` (repositorio operacional)"

**Severidad:** Medio — STD-010 §2 lista
``panorama-iact.rst`` y otros archivos de
``arquitectura-tecnica/`` como **fuera del ambito normativo**
(libre). Pero el principio recomienda usar vocabulario
canonico tambien aqui para coherencia. Decision pendiente
del ejecutor.

### G-UV-03 (Crítico): mapa-funciones-rbac.rst sin v5.6.x

**Archivo:** ``source/arquitectura-tecnica/use-case-view/mapa-funciones-rbac.rst``

**Problema:** ``grep`` retorna **0 menciones** de:

- ``manage_menu_catalog``
- ``manage_menu_lifecycle``
- ``manage_critical_function_flag``
- ``UC_ADM_04``
- ``UC_ADM_05``
- ``is_critical``
- ``v5.6.x``

El mapa de funciones RBAC NO refleja la extension v5.6.x
del WP anterior.

**Severidad:** Critico — el mapa es referencia canonica para
entender que UCs cubren que funciones.

### G-UV-04 (Crítico): panorama-iact.rst sin MenuItem

**Archivo:** ``source/arquitectura-tecnica/use-case-view/panorama-iact.rst``

**Problema:** ``grep`` retorna **0 menciones** de:

- ``MenuItem``
- ``v5.6.x``
- ``is_critical``
- ``UC_ADM_04``, ``UC_ADM_05``
- ``67`` o ``80`` (conteos actualizados)

El panorama high-level NO refleja la extension v5.6.x.

**Severidad:** Critico — panorama es la primera vista que un
lector consulta. Desincronizado del catalogo RBAC actual.

### G-UV-05 (Bajo): Otros conteos en panorama / mapa

A verificar en Phase 3 ANALYZE: si ``panorama-iact.rst`` y
``mapa-funciones-rbac.rst`` mencionan totales ``64/77/13`` o
similares en otros lugares.

## Sección 4 — Hallazgos positivos

### P-1: Paridad casos-uso ↔ use-case-view

Los 13 clusters mantienen estructura espejo exacta. Cada UC
en ``casos-uso/`` tiene su entry en ``use-case-view/`` con
el mismo nombre.

### P-2: STD-011 aliases conformes

Grep de ``as [A-Z][A-Z]?$`` o ``as [a-z][a-z]?$`` retorna
**0 violaciones** en use-case-view/. Los aliases ya estan
auto-documentados (impacto del WP previo
``2026-05-04-02-11-54-uml-alias-naming-fix``).

### P-3: Indices por cluster

Cada cluster tiene su ``index.rst`` consolidando los UCs.
Estructura uniforme.

### P-4: Cluster admin recien actualizado

El cluster ``admin/`` refleja v5.6.x (UC_ADM_04 y UC_ADM_05
agregados en commit ``92ebeb0e``). Sirve de **patron canonico**
para actualizar otros archivos transversales.

### P-5: Total 85 UCs consistente

El conteo total (85) coincide entre:

- ``use-case-view/`` (85 archivos uc-*.rst).
- ``casos-uso/`` (85 directorios).
- ``matriz-dependencias-uc-iact.rst`` §2.14 (total 85
  post-WP previo).

Salvo el ``index.rst`` desactualizado (G-UV-01), todos los
demas conteos son consistentes.

## Sección 5 — Stakeholders

- **Ejecutor (NestorMonroy):** decision sobre alcance de
  correcciones.
- **Arquitectura tecnica (auditor):** consume use-case-view
  como vista canonica.
- **Frontend dev (lector):** consulta panorama / mapa para
  entender que UCs estan disponibles.
- **WP previo `menu-rbac-user-scope-docs`:** dependencia
  upstream — sus correcciones (catalogo 67/80) requieren
  reflejarse en use-case-view.

## Sección 6 — Restricciones

- Phase 1 NO modifica source/ — solo analiza.
- Cumplir STD-010 + STD-011 en cualquier output.
- ``arquitectura-tecnica/`` esta **fuera de ambito** STD-010
  estricto pero sigue el principio por coherencia.
- Strict build (``-W``) tras cualquier cambio.

## Sección 7 — Recomendaciones (input a Phase 5/7)

### Tier 1 — Correcciones criticas (3 gaps)

1. **G-UV-01:** actualizar conteo "83 UCs" → "85 UCs" en
   ``index.rst:25``.
2. **G-UV-03:** actualizar ``mapa-funciones-rbac.rst`` con
   las 3 capabilities v5.6.x extension + UC_ADM_04/05 + nota
   sobre ``is_critical``.
3. **G-UV-04:** actualizar ``panorama-iact.rst`` con seccion
   v5.6.x extension (MenuItem wrapper UX, capabilities
   criticas, conteos 67/80, diff baseline/extension/current).

### Tier 2 — STD-010 alignment (3 ubicaciones)

4. **G-UV-02:** sustituir tecnologias concretas
   (``APScheduler``, ``PostgreSQL``) por terminos canonicos
   en 3 archivos.

### Tier 3 — Verificacion adicional (Phase 3)

5. Verificacion exhaustiva de cada index de cluster vs
   matriz-dependencias por si hay clusters con UCs que
   menciona el matriz pero no tienen entry en use-case-view
   (ya verificado: paridad 100% por counts).
6. Validacion de cross-refs entre clusters (e.g.,
   ``UC_ACC_05`` consumida por UC_ADM_01).
7. Verificacion de que cada uml-07 standalone en
   use-case-view tiene su spec completa en casos-uso/.

## Sección 8 — Estimación tamaño del WP

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Tier
   - Acciones
   - Tamaño
 * - Tier 1 (3 gaps)
   - Updates a 3 archivos top-level
   - Pequeño
 * - Tier 2 (3 ubicaciones)
   - Sustituciones STD-010 en 3 archivos
   - Pequeño
 * - Tier 3 (verificaciones)
   - 3 verificaciones cruzadas adicionales
   - Mediano

**Tamaño total propuesto:** mediano (Stages 1, 5, 7, 11).

## Sección 9 — Stopping points propuestos

- **SP-01** (humano): aprobar el plan correctivo (Tier 1 +
  Tier 2 + decisiones Tier 3) antes de Phase 7.
- **SP-02:** build strict 0 warnings tras cada lote.
- **SP-03** (humano): aprobar el cierre del WP.

## Sección 10 — Items para validar antes de Phase 5

1. ¿El ejecutor aprueba el alcance Tier 1 + Tier 2?
2. ¿Se ejecuta Tier 3 (verificaciones) en este WP o se
   difiere a otro?
3. ¿``arquitectura-tecnica/`` aplica STD-010 estricto o solo
   por coherencia?

## Refs

- WP previo:
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs`` (cerrado
  2026-05-07 04:08).
- WP hermano: ``2026-05-06-23-25-08-std-010-corpus-compliance``.
- Catalogo canonico:
  ``source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst``.
- Matriz: ``source/arquitectura-tecnica/matriz-dependencias-uc-iact.rst``.
- STDs: STD-010 (vocabulario abstracto), STD-011 (aliases).
