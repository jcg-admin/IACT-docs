```yml
created_at: 2026-05-07 01:30:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 11 — TRACK (deep-review pre-cierre)
author: NestorMonroy
status: Borrador
version: 1.0.0
parent: track/dependency-graph-and-domain-model-coverage.md
```

# Deep-Review de Cobertura — pre-cierre del WP

> Auditoria sistematica que verifica si **todas las decisiones**
> discutidas/aprobadas en DISCOVER + STRATEGY del WP estan
> efectivamente implementadas en los artefactos de Phase 7
> DESIGN y los updates de corpus aplicados en Phase 11.

## Sección 1 — Metodologia

12 categorias verificadas con grep + read directos:

1. Key Ideas KI-1..KI-3
2. Fundamental Decisions P1-P4
3. Items pendientes (indices, degraded mode, DEPRECATED)
4. Gap #3 (auto-archive opt-out)
5. Gap #4 (is_critical bypass)
6. D-MOD-001 (sin MOD_MEN)
7. STD-010 vocabulario canonico
8. STD-011 aliases auto-documentados
9. Conteos del catalogo (67/80)
10. Domain-model classes
11. Tests guardrail
12. Trazabilidad cruzada

## Sección 2 — Resumen ejecutivo

.. list-table::
 :widths: 8 30 20 12 30
 :header-rows: 1

 * - #
   - Categoria
   - Estado
   - Severidad
   - Notas
 * - 1
   - KI-1..KI-3
   - PASS
   - —
   - 4 archivos cubren wrapper UX; I-1..I-4 en 3
 * - 2
   - P1-P4
   - PASS
   - —
   - 32 menciones de campos MenuItem; 13 indices
     verbatim en 3 archivos
 * - 3
   - Items pendientes
   - PASS
   - —
   - degraded mode + DEPRECATED policy completos
 * - 4
   - Gap #3 (auto-archive)
   - PASS
   - —
   - block_auto_archive triplet en MenuItem,
     UC_ADM_05, MenuLifecycleService
 * - 5
   - Gap #4 (is_critical)
   - **PARTIAL**
   - Critico
   - **DR-1: 3 de 9 capabilities iniciales no existen
     en el catalogo**
 * - 6
   - D-MOD-001
   - PASS
   - —
   - UC_ADM_04/05 en MOD_Admin confirmado
 * - 7
   - STD-010
   - PASS
   - —
   - JWT en uc-perm-08 ext es excepcion permitida §3.3
 * - 8
   - STD-011
   - PASS
   - —
   - Sin aliases <=2 letras en archivos del WP
 * - 9
   - Conteos 67/80
   - PASS
   - —
   - Consistente en catalogo, mapeo-uc, BR-006,
     rbac-impl-guide tests, matriz-dependencias
 * - 10
   - Domain-model
   - PASS
   - —
   - 4 clases nuevas + 4 actualizadas registradas
 * - 11
   - Tests guardrail
   - PASS
   - —
   - I-1..I-4 + CA-01..CA-12 + bootstrap 67
 * - 12
   - Trazabilidad cruzada
   - **PARTIAL**
   - Bajo
   - **DR-2: ADR-BACK-008 sin referencia a 009/010**
 * - extra
   - Phase 11 cierre formal
   - **GAP**
   - Bajo
   - **DR-4: changelog + lessons learned + wp-state
     no actualizado**

**Total:** 9 PASS / 2 PARTIAL / 1 GAP. Solo DR-1 es bloqueante
(inconsistencia entre ADR-BACK-010 y catalogo real).

## Sección 3 — Hallazgos detalle

### DR-1 (Critico): Catalogo de capabilities is_critical inconsistente

**Archivos afectados:**

- ``source/backend/adr-back-010-function-is-critical-governance.rst``
  §3.3
- Implicito en: cache-strategy.rst §4,
  user-capability-resolver.rst, function.rst,
  UC_ADM_04/UC_ADM_05 patrones-diseno,
  strategy/strategy-addendum-gaps-and-module.md §5,
  strategy/gap-3-4-decision-rationale.md §3,
  track/dependency-graph-and-domain-model-coverage.md §3.

**Problema:**

ADR-BACK-010 §3.3 declara 9 capabilities como
``is_critical=True`` en el catalogo inicial:

::

   1. assign_functions
   2. revoke_function_group
   3. manage_menu_catalog
   4. manage_menu_lifecycle
   5. manage_function_catalog
   6. manage_access_groups          ← NO existe en catalogo
   7. delete_user                    ← existe como deactivate_users
   8. delete_function                ← NO existe (BR-009 soft delete)
   9. delete_access_group            ← NO existe (BR-009 soft delete)

Verificacion via grep contra ``catalogo-funciones.rst``:

- ``manage_access_groups``: 0 menciones (no existe).
- ``delete_function``: 0 menciones (no existe).
- ``delete_access_group``: 0 menciones (no existe).
- ``delete_user``: existe SOLO como referencia historica
  (RENAME v5.4.0 → ``deactivate_users``).

**Causa raiz:** ADR-BACK-010 fue producido en L1 sin
verificacion contra el catalogo canonico. Las "capabilities
de delete agresivas" no existen en IACT — el proyecto usa
``BR-009 baja logica`` (soft delete con ``is_active=False``).

**Severidad:** Critico — un test que valide
``Function.objects.filter(codename__in=CRITICAL_INITIAL).update(is_critical=True)``
fallaria silenciosamente sobre 4 codenames inexistentes.

### DR-2 (Bajo): ADR-BACK-008 sin cross-ref a 009/010

**Archivo:** ``source/backend/adr-back-008-menuitem-wrapper-ux-sobre-function.rst``

**Problema:** la seccion "Relacionados" no incluye
ADR-BACK-009 (cache degraded mode) ni ADR-BACK-010
(``is_critical`` governance), aunque los UCs y el modelo
``MenuItem`` los consumen indirectamente.

**Severidad:** bajo — no rompe funcionalidad, solo navegacion
del corpus.

### DR-4 (Bajo): Phase 11 cierre formal incompleto

**Faltan:**

- ``track/{wp}-changelog.md`` con formato Keep-a-Changelog
  consolidando todos los cambios del WP.
- ``track/lessons-learned.md`` documentando aprendizajes.
- ``wp-state.md`` actualizado a ``current_phase: Phase 11
  TRACK`` y ``status: Cerrado`` o equivalente.

**Severidad:** bajo — cosmetico para cierre formal del WP.

## Sección 4 — Decisiones arquitectonicas

### D-DR-001: Lista canonica de capabilities is_critical=True

**Pregunta:** ¿que lista de capabilities debe declararse
``is_critical=True`` alineada al catalogo real?

**Decision:** alinear ADR-BACK-010 §3.3 al catalogo canonico
(Opcion A — conservadora). Lista actualizada:

.. list-table::
 :widths: 30 12 25 33
 :header-rows: 1

 * - Codename
   - Modulo
   - UC titular
   - Razon
 * - ``assign_functions``
   - ACC
   - UC-010, UC-042
   - Asigna Function a usuarios — modifica permisos
     de otros
 * - ``revoke_functions``
   - ACC
   - UC-010
   - Revoca Function de usuarios
 * - ``assign_function_groups``
   - ACC
   - UC-010
   - Asigna grupos de funciones — modifica permisos
 * - ``revoke_function_group``
   - PERM
   - UC_PERM_02
   - Revoca grupo asignado a usuario
 * - ``assign_functions_to_group``
   - PERM/ADM
   - UC_PERM_06, UC_ADM_03
   - Modifica composicion de AGRs
 * - ``manage_function_catalog``
   - ADM
   - UC_ADM_02
   - CRUD del catalogo Function
 * - ``manage_menu_catalog``
   - ADM (v5.6.x)
   - UC_ADM_04
   - CRUD MenuItem (v5.6.x extension)
 * - ``manage_menu_lifecycle``
   - ADM (v5.6.x)
   - UC_ADM_05
   - Transiciones de estado (v5.6.x extension)
 * - ``deactivate_users``
   - USR
   - UC_USR_xx
   - Soft delete user (BR-009)

**Total:** 9 capabilities (mismo numero, diferente
composicion respecto al ADR original).

**Removidas** del catalogo inicial:

- ``manage_access_groups`` (no existe — gestion de AGRs
  custom es UC_PERM_05/06 con caps existentes).
- ``delete_function``, ``delete_access_group`` (no existen —
  semantica soft delete via ``is_active=False`` cubierta
  por ``manage_function_catalog`` y similares).

**Cambio respecto al ADR original:**

- ``delete_user`` → ``deactivate_users`` (alineado a
  RENAME v5.4.0 documentado en catalogo §3.2).
- Agregadas: ``revoke_functions``, ``assign_function_groups``
  por simetria con sus contrapartes (si asignar es critico,
  revocar tambien lo es).

**Razonamiento:** ADR-BACK-010 declara la politica
**conceptualmente** (capabilities que modifican permisos de
otros, modifican catalogo RBAC, son irreversibles). La
implementacion concreta del catalogo inicial debe respetar
los nombres reales de capabilities en el catalogo. Mantener
caps que no existen es deuda tecnica oculta.

**Trade-off:** la lista actualizada cubre 9 capabilities
reales en lugar de 9 mixtas (5 reales + 4 inexistentes).
La cobertura de proteccion strong-consistency es **mas
amplia** (incluye ``revoke_functions``, ``assign_function_groups``
que no estaban antes).

### D-DR-002: Cross-refs entre ADR-BACK-008/009/010

**Decision:** ADR-BACK-008 agrega ADR-BACK-009 y ADR-BACK-010
en su seccion "Relacionados".

### D-DR-003: Phase 11 cierre formal — alcance

**Decision:** producir 3 artefactos:

1. ``track/menu-rbac-user-scope-docs-changelog.md`` —
   Keep-a-Changelog consolidando los 6 commits de Phase 7
   + 2 commits de Phase 11 + cambios menores.
2. ``track/lessons-learned.md`` — aprendizajes destacados:
   pre-validacion contra catalogo antes de redactar ADRs,
   STD-010 + STD-011 enforced en cada PR, manejo de gap #3
   y gap #4 con razonamiento del ejecutor preservado verbatim.
3. ``wp-state.md`` actualizado: ``current_phase: Phase 11
   TRACK``, ``status: En revision`` (cerrado tras aprobacion
   del ejecutor).

## Sección 5 — Plan correctivo

### Lote D-A: alinear lista de capabilities (DR-1, D-DR-001)

Archivos a modificar:

1. ``source/backend/adr-back-010-function-is-critical-governance.rst``:
   §3.3 (tabla catalogo inicial), §6.1 (migration
   ``CRITICAL_INITIAL`` set).
2. ``source/arquitectura-tecnica/cache-strategy.rst``:
   §4 (catalogo critico mencionado).
3. ``source/arquitectura-tecnica/domain-model/function.rst``:
   "Catalogo inicial True" en politica de uso.
4. ``source/requisitos/casos-uso/admin/uc-adm-04/patrones-diseno.rst``:
   referencia indirecta.
5. ``source/requisitos/casos-uso/admin/uc-adm-05/patrones-diseno.rst``:
   referencia indirecta.
6. ``source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst``:
   §3.11 columna ``is_critical`` y notas — verificar que
   las nuevas v5.6.x esten marcadas y las baseline mencionadas
   estan correctamente identificadas.
7. ``.thyrox/context/work/.../strategy/strategy-addendum-gaps-and-module.md``:
   §5 (catalogo inicial mencionado).
8. ``.thyrox/context/work/.../strategy/gap-3-4-decision-rationale.md``:
   §3 (catalogo del razonamiento).
9. ``.thyrox/context/work/.../track/dependency-graph-and-domain-model-coverage.md``:
   §3 catalogo critico mencionado.

### Lote D-B: cross-refs entre ADRs (DR-2, D-DR-002)

10. ``source/backend/adr-back-008-menuitem-wrapper-ux-sobre-function.rst``:
    seccion "Relacionados" agrega ADR-BACK-009 y 010.

### Lote D-C: Phase 11 cierre formal (DR-4, D-DR-003)

11. Crear ``.thyrox/context/work/.../track/menu-rbac-user-scope-docs-changelog.md``.
12. Crear ``.thyrox/context/work/.../track/lessons-learned.md``.
13. Actualizar ``.thyrox/context/work/.../wp-state.md``.

### Build + commit

- Sphinx strict EXIT=0 obligatorio.
- Commit unificado "Phase 11 deep-review fixes — capability
  catalog alignment + ADR cross-refs + WP closure".

## Sección 6 — PASS detalle (lo que SI esta cubierto)

### KI-1 wrapper UX lifecycle (PASS)

4 archivos contienen "wrapper UX" o "MenuItem.*wrapper" o
"OneToOneField.*Function":

- ``source/backend/adr-back-008-menuitem-wrapper-ux-sobre-function.rst``
- ``source/normativa/restricciones/cnst-032-menu-dinamico-obligatorio.rst``
- ``source/arquitectura-tecnica/domain-model/menu-item.rst``
- ``source/requisitos/casos-uso/admin/uc-adm-04/informacion-general.rst``

### KI-2 invariantes I-1..I-4 (PASS)

- ADR-BACK-008: 12 menciones de I-1..I-4 (definicion +
  tests).
- CNST-032 v2.0.0: 7 menciones (§2.3 invariantes
  obligatorias).
- MenuItem class: 6 menciones (anotaciones del diagrama).

### KI-3 cache + bypass (PASS)

TTL 300s y degraded mode presentes en:

- ADR-BACK-009 (politica conceptual)
- cache-strategy.rst (motor concreto)
- permission-cache.rst v2.0.0 (clase actualizada)
- user-capability-resolver.rst (clase nueva)

### P1 modelo MenuItem (PASS)

32 menciones agregadas de los 16 campos canonicos del
modelo en ``source/arquitectura-tecnica/domain-model/menu-item.rst``.

### 13 indices (PASS)

Verbatim en:

- ``source/backend/rbac-implementation-guide.rst``
  §Q9.7 "13 indices distribuidos en 4 tablas"
- ``source/arquitectura-tecnica/domain-model/user-capability-resolver.rst``
  "13 indices que sostienen P95"
- ADR-BACK-009 referencia "P3 del WP — 13 indices definidos"

### Conteos del catalogo (PASS)

Consistencia 67/80 verificada en:

- catalogo-funciones.rst (header + §3.11 con tabla diff)
- mapeo-uc.rst (scope note 67 + 3 nuevas filas)
- BR-006 (3 lugares actualizados + UCs afectados)
- rbac-implementation-guide.rst (tests bootstrap renombrado
  a 67 + test baseline 64 + test no_titular)
- matriz-dependencias-uc-iact.rst (cluster ADM 5 UCs +
  tabla 2.14 con total 85)

### Domain-model classes (PASS)

4 nuevas registradas en domain-model/index.rst BC RBAC
toctree:

- menu-item
- menu-item-repo
- menu-lifecycle-service
- user-capability-resolver

4 actualizadas:

- function.rst v2.0.0 (is_critical)
- permission-cache.rst v2.0.0 (politica v5.6.x)
- menu.rst v2.0.0 (DEPRECATED warning)
- effective-permissions-aggregator.rst v1.1.0 (coexistence)

### STD-011 aliases (PASS)

Validado por grep §7 de STD-011 sobre:

- arquitectura-tecnica/use-case-view/admin/
- domain-model/menu-item.rst, menu-item-repo.rst,
  menu-lifecycle-service.rst, user-capability-resolver.rst
- requisitos/casos-uso/admin/uc-adm-04/diagramas-uml/
- requisitos/casos-uso/admin/uc-adm-05/diagramas-uml/

Resultado: vacio (cero aliases <=2 letras).

## Sección 7 — Conclusion

Cobertura general **alta** (9/12 PASS). Las correcciones
restantes son:

- DR-1 (critico) — corregible con sustitucion de listas
  en ~9 archivos.
- DR-2 (bajo) — 1 edit.
- DR-4 (bajo) — 3 archivos nuevos / actualizados.

**Estimacion de cierre del WP:** un commit unificado
"Phase 11 deep-review fixes" cubre los 3 lotes D-A/D-B/D-C.

## Refs

- ``track/post-design-coverage-review.md`` (gaps G-1..G-10).
- ``track/dependency-graph-and-domain-model-coverage.md``
  (gaps G-11..G-18 + Opcion B).
- ``strategy/menu-rbac-user-scope-solution-strategy.md``
  (KI/P/AP).
- ``strategy/strategy-addendum-gaps-and-module.md``
  (gap #3, gap #4, D-MOD-001, DAG).
- ADR-BACK-008/009/010 (commit cd224ee5).
- CNST-032 v2.0.0 + Q9 + cache-strategy (commit 8ed97a16).
- UC_ADM_04 + UC_PERM_08 ext (commit 86b1696f).
- UC_ADM_05 + scheduled-tasks (commit 43624501).
- Phase 11 lote C-A (commit 89ef4d61).
- Phase 11 lotes C-B + C-C + C-D (commit 92ebeb0e).
