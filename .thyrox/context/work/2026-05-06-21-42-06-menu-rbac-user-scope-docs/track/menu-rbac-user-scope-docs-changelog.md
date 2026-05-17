```yml
created_at: 2026-05-07 01:45:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
version: 1.0.0
format: Keep a Changelog
```

# Changelog — WP menu-rbac-user-scope-docs

> Consolidacion de cambios del WP en formato Keep a Changelog.
> Fecha de inicio: 2026-05-06. Fecha de cierre: 2026-05-07.

## [1.0.0] — 2026-05-07 (cierre del WP)

### Added

**ADRs nuevos** (commit ``cd224ee5``):

- ``source/backend/adr-back-008-menuitem-wrapper-ux-sobre-function.rst``
  v1.0.0 — MenuItem como wrapper UX 1:1 sobre Function con
  ``on_delete=PROTECT``, lifecycle DRAFT/ACTIVE/DEPRECATED/
  ARCHIVED, invariantes I-1..I-4.
- ``source/backend/adr-back-009-cache-capabilities-degraded-mode.rst``
  v1.0.0 — TTL 300s, invalidacion explicita en UC transaccional,
  degraded mode ante falla del servicio de cache.
- ``source/backend/adr-back-010-function-is-critical-governance.rst``
  v1.0.0 — Flag ``Function.is_critical`` con bypass selectivo
  (AP-2b) + governance del flag separada de
  ``manage_function_catalog`` (vector de ataque mitigado).

**Constraints** (commit ``8ed97a16``):

- ``source/normativa/restricciones/cnst-032-menu-dinamico-obligatorio.rst``
  v2.0.0 — reescritura completa: MenuItem wrapper UX
  obligatorio, prohibiciones explicitas (3.1-3.4) que
  clausuran el anti-patron Diseno A.

**Documentos de arquitectura tecnica** (commit ``8ed97a16``,
``43624501``):

- ``source/arquitectura-tecnica/cache-strategy.rst`` v1.0.0 —
  motor concreto Redis 7.x, configuracion canonica, key
  namespace, politica de TTL, degraded mode.
- ``source/arquitectura-tecnica/scheduled-tasks.rst`` v1.0.0 —
  motor concreto Celery 5.x + beat, job
  ``auto_archive_menu_items``, identidad service account
  ``system``, observabilidad.

**Casos de uso nuevos** (commit ``86b1696f``, ``43624501``):

- ``source/requisitos/casos-uso/admin/uc-adm-04/`` —
  Gestionar Catalogo de MenuItems (12 archivos: index,
  informacion-general, actores-precondiciones,
  flujo-principal, flujos-alternos (5), excepciones (7),
  requisitos-no-funcionales, datos-involucrados,
  diagramas-uml/ (secuencia + actividad),
  criterios-aceptacion (CA-01..CA-10), patrones-diseno,
  implementacion-tecnica, testing).
- ``source/requisitos/casos-uso/admin/uc-adm-05/`` —
  Gestionar Lifecycle de MenuItem (12 archivos con state
  machine + 5 transiciones validas + flag block_auto_archive
  + job auto-archive a 90d + diagrama-de-estados).
- ``source/requisitos/casos-uso/permissions/uc-perm-08/extension-v560-menu-item-wrapper.rst``
  — extension UC_PERM_08 v5.6.0 con shape flat
  ``{capabilities, menu_items}``.

**Vista UC** (commit ``92ebeb0e``):

- ``source/arquitectura-tecnica/use-case-view/admin/uc-adm-04-gestionar-catalogo-menuitems.rst``
  — uml-07 standalone con 9 actors, 9 use cases.
- ``source/arquitectura-tecnica/use-case-view/admin/uc-adm-05-gestionar-lifecycle-menuitem.rst``
  — uml-07 standalone con 11 use cases.

**Domain model nuevas** (commit ``92ebeb0e``):

- ``source/arquitectura-tecnica/domain-model/menu-item.rst``
  v1.0.0 — wrapper UX entity con 17 atributos + state machine.
- ``source/arquitectura-tecnica/domain-model/menu-item-repo.rst``
  v1.0.0 — repository + queryset (visible/for_user/has_cycle/
  bulk_reorder/due_for_auto_archive).
- ``source/arquitectura-tecnica/domain-model/menu-lifecycle-service.rst``
  v1.0.0 — state machine + auto-archive policy 30/80/90d.
- ``source/arquitectura-tecnica/domain-model/user-capability-resolver.rst``
  v1.0.0 — resolver canonico con resolve/resolve_uncached/
  has_capability + 13 indices documentados.

**Technical debt** (commit ``92ebeb0e``):

- TD-RBAC-03 registrada en
  ``.thyrox/context/technical-debt.md`` —
  ``manage_critical_function_flag`` sin titular runtime
  (ADR-BACK-010 §3.6).

**Phase 11 documentos** (commits ``b156a314``, ``67cc7ccb``,
``92ebeb0e``, este):

- ``track/post-design-coverage-review.md`` — gaps G-1..G-10.
- ``track/dependency-graph-and-domain-model-coverage.md`` —
  decision Opcion B (67/80) + DAG + gaps G-11..G-18.
- ``track/deep-review-coverage.md`` — DR-1..DR-4 + decisiones
  D-DR-001..003.
- ``track/lessons-learned.md`` — aprendizajes del WP.
- ``track/menu-rbac-user-scope-docs-changelog.md`` (este).

### Changed

**RBAC catalogo** (commit ``89ef4d61``):

- ``source/requisitos/reglas-negocio/rbac/catalogo-funciones.rst``
  — header §3 con tabla diff baseline/extension/current.
  §3.11 MOD_Admin de 3 → 6 funciones con columna
  ``is_critical``: ``manage_menu_catalog``,
  ``manage_menu_lifecycle``, ``manage_critical_function_flag``
  agregadas.
- ``source/requisitos/reglas-negocio/rbac/mapeo-uc.rst``
  — scope note actualizada de "64 in-scope" a "67 in-scope
  (64 baseline + 3 extension)" + 3 filas nuevas.

**Reglas de negocio** (commit ``89ef4d61``):

- ``source/requisitos/reglas-negocio/br-006-rbac-flat-nist.rst``
  — conteos 64/77 → 67/80 en 3 ubicaciones; UC_ADM_04 y
  UC_ADM_05 agregados a "Casos de Uso afectados".

**Backend implementation guide** (commit ``8ed97a16``,
``89ef4d61``):

- ``source/backend/rbac-implementation-guide.rst`` — nueva
  seccion Q9 (MenuItem UI metadata layer +
  UserCapabilityResolver) con 9 sub-questions.
- Tests bootstrap: ``test_bootstrap_creates_64_in_scope_functions``
  → ``test_bootstrap_creates_67_in_scope_functions``;
  agregados ``test_bootstrap_v560_baseline_64_functions`` y
  ``test_manage_critical_function_flag_has_no_titular``.

**Vista UC + matriz** (commit ``92ebeb0e``):

- ``source/arquitectura-tecnica/use-case-view/admin/index.rst``
  v3.0.0 — diagrama PlantUML extendido con UC_ADM_04/05 +
  Planificador de Tareas. Tabla Casos de Uso con 2 filas
  nuevas. Tabla Funciones RBAC con 3 filas nuevas + columna
  ``is_critical``. Toctree con 2 entradas nuevas.
- ``source/arquitectura-tecnica/matriz-dependencias-uc-iact.rst``
  — nueva seccion 2.13 Cluster ADM (5 UCs); tabla 2.14 con
  total 80 → 85.

**Domain model existentes** (commit ``92ebeb0e``):

- ``source/arquitectura-tecnica/domain-model/function.rst``
  v2.0.0 — campo ``is_critical`` agregado con politica de uso;
  Module enum extendido (ADM, OPR, SUP); referencia a
  MenuItem wrapper.
- ``source/arquitectura-tecnica/domain-model/permission-cache.rst``
  v2.0.0 — seccion v5.6.x agregada con key namespace,
  degraded mode, bypass selectivo, ref a cache-strategy.
- ``source/arquitectura-tecnica/domain-model/menu.rst``
  v2.0.0 — DEPRECATED warning agregada (modelo legacy v5.0.0);
  superseded_by menu-item.
- ``source/arquitectura-tecnica/domain-model/effective-permissions-aggregator.rst``
  v1.1.0 — note de coexistencia con UserCapabilityResolver.
- ``source/arquitectura-tecnica/domain-model/index.rst``
  — 4 entradas nuevas registradas en BC RBAC toctree.

**Arquitectura tecnica index** (commit ``8ed97a16``):

- ``source/arquitectura-tecnica/index.rst`` — entradas
  ``cache-strategy`` y ``scheduled-tasks`` agregadas a
  "Analisis arquitectonicos".

**Backend index** (commit ``cd224ee5``):

- ``source/backend/index.rst`` — entradas ADR-BACK-008/009/010
  agregadas a "ADRs Backend".

**Admin module index** (commit ``86b1696f``, ``43624501``):

- ``source/requisitos/casos-uso/admin/index.rst`` — UC_ADM_04
  y UC_ADM_05 agregados a toctree.

**UC_PERM_08 index** (commit ``86b1696f``):

- ``source/requisitos/casos-uso/permissions/uc-perm-08/index.rst``
  — nueva toctree "Extensiones" con
  ``extension-v560-menu-item-wrapper``.

### Fixed (deep-review)

**Lista de capabilities is_critical=True alineada al catalogo**
(este commit, D-DR-001):

- ADR-BACK-010 §3.3 reescrita: 9 capabilities canonicas
  (``assign_functions``, ``revoke_functions``,
  ``assign_function_groups``, ``revoke_function_group``,
  ``assign_functions_to_group``, ``manage_function_catalog``,
  ``manage_menu_catalog``, ``manage_menu_lifecycle``,
  ``deactivate_users``).
- Removidas: ``manage_access_groups``, ``delete_function``,
  ``delete_access_group``, ``delete_user`` (no existen en
  catalogo IACT — el proyecto usa ``BR-009 baja logica``).
- ADR-BACK-010 §6.1 ``CRITICAL_INITIAL`` set actualizado +
  assertion en migration que valida codenames contra catalogo.
- function.rst "Catalogo inicial True" actualizado.

**Cross-refs entre ADRs** (D-DR-002):

- ADR-BACK-008 sección "Relacionados" agrega ADR-BACK-009 y
  ADR-BACK-010.

### Deprecated

- Clase ``Menu`` (domain-model) — modelo legacy v5.0.0/v5.5.0
  marcado DEPRECATED con migration path documentada en su rst.
- CNST-032 v1.0.0 — reemplazado por v2.0.0; historial de
  versiones preservado en §10 del archivo.

### Removed

- ``manage_access_groups``, ``delete_function``,
  ``delete_access_group`` de la lista canonica de capabilities
  ``is_critical=True`` — no existen en el catalogo IACT.

### Status de promocion a CHANGELOG.md raiz

Pendiente al merge a ``main`` con bump de version. Promover
las entradas de "Added" + "Changed" agrupadas como
"v5.6.x extension — Menu RBAC con User Scope".

## Aceptado / no fixeado

- **G-8 (CNST-033 cross-ref a CNST-032 v2.0.0):** diferido
  como mejora cosmetica no bloqueante.
- **Tests dinamicos en testing.rst de UCs nuevos:** son
  especificaciones; ejecucion real depende de codigo
  implementado en repositorio aparte.
- **Migration de datos legacy C_MENU2 → MenuItem:** out-of-scope
  declarado en strategy §11. El sistema no importa datos
  legacy.

## Refs (commits)

- ``cd224ee5`` — Phase 7 L1: ADR-BACK-008/009/010.
- ``8ed97a16`` — Phase 7 L2: CNST-032 v2.0.0 + Q9 ext +
  cache-strategy.
- ``86b1696f`` — Phase 7 L3: UC_ADM_04 + UC_PERM_08 ext.
- ``43624501`` — Phase 7 L4+L5: UC_ADM_05 + scheduled-tasks.
- ``b156a314`` — track/post-design-coverage-review (gaps).
- ``67cc7ccb`` — track/dependency-graph (Opcion B + gaps
  domain-model).
- ``89ef4d61`` — Phase 11 lote C-A: catalogo + mapeo + BR-006
  + tests.
- ``92ebeb0e`` — Phase 11 lotes C-B + C-C + C-D: vista UC +
  domain-model + misc.
- *(pendiente)* — Phase 11 deep-review fixes (este commit).
