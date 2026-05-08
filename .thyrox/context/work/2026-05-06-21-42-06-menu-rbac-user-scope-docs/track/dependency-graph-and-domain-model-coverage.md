```yml
created_at: 2026-05-07 00:45:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
version: 1.0.0
parent: track/post-design-coverage-review.md
```

# Dependency Graph + Domain Model Coverage Analysis

> Analisis post-Phase 7 que documenta la decision arquitectonica
> sobre conteo de capabilities, presenta el grafo de dependencias
> de los 10 artefactos producidos, y verifica si faltan clases
> en ``source/arquitectura-tecnica/domain-model/``.

## Sección 1 — Decision arquitectonica aprobada (Opcion B)

**Pregunta cerrada:** ¿las 3 nuevas capabilities cuentan como
activas en v5.6.x?

**Decision:** **Opcion B — 67/80 con label "v5.6.x extension"**.

### Razonamiento

| Aspecto | Opcion A (v5.6.0 in-scope) | Opcion B (v5.6.x extension) | Opcion C (66/80) |
|---|---|---|---|
| Conteo activas | 67/80 | 67/80 con nota | 66/80 |
| Trazabilidad al WP origen | implicita | **explicita** | implicita |
| ``manage_critical_function_flag`` activa | si | si (sin titular) | no |
| Cambio en RBAC v5.6.0 baseline | si | no (es extension) | menor |
| Costo de actualizar BR-006 | conteo solo | conteo + nota | conteo solo |

**Ganador (Opcion B):** preserva v5.6.0 baseline intacto (catalogo
inicial fue 64/77 con MOD_Admin de 3 caps); las nuevas son
**extensiones v5.6.x trazables** al WP
``2026-05-06-21-42-06-menu-rbac-user-scope-docs``.

### Aplicacion concreta

Donde se documenta el conteo, agregar tabla diff:

::

   v5.6.0 baseline       : 64 activas / 77 declaradas / 13 reservadas
   v5.6.x WP-menu-rbac   : +3 activas (MOD_Admin extension)
                              · manage_menu_catalog (UC_ADM_04)
                              · manage_menu_lifecycle (UC_ADM_05)
                              · manage_critical_function_flag (sin titular)
   v5.6.x current        : 67 activas / 80 declaradas / 13 reservadas

## Sección 2 — Grafo de dependencias de los 10 artefactos

### 2.1 Diagrama (DAG)

::

   ┌─────────────────────────────────────────────────────────────┐
   │                       L1 (paralelo)                          │
   │                                                              │
   │  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
   │  │ ADR-BACK-008    │  │ ADR-BACK-009    │  │ ADR-BACK-010 │ │
   │  │ MenuItem wrapper│  │ Cache degraded  │  │ is_critical  │ │
   │  │ UX over Function│  │ mode politics   │  │ governance   │ │
   │  └────────┬────────┘  └────────┬────────┘  └──────┬───────┘ │
   └───────────┼────────────────────┼───────────────────┼─────────┘
               │                    │                   │
   ┌───────────┼────────────────────┼───────────────────┼─────────┐
   │           v                    v                   v          │
   │                       L2 (paralelo)                           │
   │                                                              │
   │  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
   │  │ CNST-032 v2.0.0 │  │ rbac-impl-guide │  │ cache-       │ │
   │  │ (rewrite)       │  │ §Q9 ext         │  │ strategy.rst │ │
   │  └────────┬────────┘  └────────┬────────┘  └──────┬───────┘ │
   └───────────┼────────────────────┼───────────────────┼─────────┘
               │                    │                   │
   ┌───────────┼────────────────────┼───────────────────┼─────────┐
   │           v                    v                              │
   │                          L3                                  │
   │  ┌──────────────────────┐  ┌──────────────────────────┐      │
   │  │ UC_ADM_04            │  │ UC_PERM_08 ext v5.6.0    │      │
   │  │ manage_menu_catalog  │  │ (extension-v560-...)     │      │
   │  └──────────┬───────────┘  └──────────────────────────┘      │
   └─────────────┼────────────────────────────────────────────────┘
                 │
   ┌─────────────┼────────────────────────────────────────────────┐
   │             v                                                │
   │                          L4                                  │
   │  ┌──────────────────────┐                                    │
   │  │ UC_ADM_05            │                                    │
   │  │ manage_menu_lifecycle│                                    │
   │  └──────────┬───────────┘                                    │
   └─────────────┼────────────────────────────────────────────────┘
                 │
   ┌─────────────┼────────────────────────────────────────────────┐
   │             v                                                │
   │                          L5                                  │
   │  ┌──────────────────────┐                                    │
   │  │ scheduled-tasks.rst  │                                    │
   │  │ (auto_archive_*)     │                                    │
   │  └──────────────────────┘                                    │
   └──────────────────────────────────────────────────────────────┘

### 2.2 Aristas (relaciones)

.. list-table::
 :widths: 25 30 45
 :header-rows: 1

 * - Origen
   - Destino
   - Tipo de dependencia
 * - ADR-BACK-008
   - CNST-032 v2.0.0
   - CNST-032 cita ADR como fundamento
 * - ADR-BACK-008
   - rbac-impl-guide §Q9
   - Q9 implementa el modelo del ADR
 * - ADR-BACK-008
   - UC_ADM_04
   - UC_ADM_04 maneja el modelo definido en ADR
 * - ADR-BACK-009
   - cache-strategy.rst
   - cache-strategy implementa el motor que ADR define
 * - ADR-BACK-009
   - rbac-impl-guide §Q9.4
   - Q9.4 codifica invalidate_user_capabilities helper
 * - ADR-BACK-010
   - rbac-impl-guide §Q9.3
   - Q9.3 implementa has_capability con bypass
 * - ADR-BACK-010
   - UC_ADM_04 / UC_ADM_05
   - Las 2 caps usan is_critical=True
 * - CNST-032 v2.0.0
   - UC_ADM_04
   - UC_ADM_04 cumple invariantes I-1..I-4
 * - CNST-032 v2.0.0
   - UC_PERM_08 ext
   - UC_PERM_08 implementa endpoint canonico
 * - rbac-impl-guide §Q9
   - UC_ADM_04 / UC_ADM_05 / UC_PERM_08 ext
   - UCs referencian Q9 como guia tecnica
 * - cache-strategy.rst
   - UC_ADM_04 / UC_ADM_05
   - UCs referencian para invalidacion concreta
 * - UC_ADM_04
   - UC_ADM_05
   - UC_ADM_05 transiciona items creados por UC_ADM_04
 * - UC_ADM_05
   - scheduled-tasks.rst
   - Job auto_archive_menu_items definido aqui

### 2.3 Verificacion topologica

- **Sin ciclos:** confirmado (DAG valido).
- **Sin orphans:** todos los 10 artefactos consumidos por ≥ 1
  otro o por usuario final del sistema.
- **Niveles:** 5 lotes paralelos, profundidad maxima 5.
- **Reduccion de tiempo de Phase 7:** estimada 50% por
  paralelismo intra-lote.

## Sección 3 — Auditoria del Domain Model

### 3.1 Clases existentes en ``source/arquitectura-tecnica/domain-model/``

Total: 87 archivos (84 clases + index + overview + diagrama).

**Clases relacionadas con RBAC:**

.. list-table::
 :widths: 35 25 40
 :header-rows: 1

 * - Clase existente
   - Estado actual
   - Estado deseado v5.6.x
 * - ``Function``
   - Vigente
   - **Update**: agregar campo ``is_critical``
 * - ``AccessGroup``
   - Vigente
   - Sin cambios
 * - ``AccessGroupFunction``
   - Vigente
   - Sin cambios (alias de FunctionGroupMembership)
 * - ``FunctionGroup``
   - Vigente
   - Sin cambios
 * - ``Assignment``
   - Vigente
   - Sin cambios
 * - ``ExceptionalPermission``
   - Vigente
   - Sin cambios
 * - ``EffectivePermissionsAggregator``
   - Vigente
   - **Update / replace** por ``UserCapabilityResolver``
 * - ``PermissionCache``
   - Vigente
   - **Update**: documentar key pattern ``caps:user:{id}``,
     TTL 300s, degraded mode
 * - ``Menu``
   - Vigente (modelo v5.0.0 transient)
   - **Deprecate** o **redefinir** como response DTO del
     endpoint flat (no entidad persistida)
 * - ``NavDomain`` / ``Section`` / ``Action``
   - Vigente (jerarquia transient v5.0.0)
   - Marcar como **legacy v5.0.0** o eliminar — el shape
     flat de v5.6.x no necesita arbol persistido
 * - ``SeparationRule`` / ``SeparationRuleRepo``
   - Vigente
   - Sin cambios
 * - ``Session`` / ``BlacklistedToken``
   - Vigente
   - Sin cambios

### 3.2 Clases FALTANTES en domain-model

.. list-table::
 :widths: 35 20 45
 :header-rows: 1

 * - Clase requerida
   - Severidad
   - Razon
 * - ``MenuItem``
   - **Critico**
   - Modelo persistente nuevo de Phase 7. No existe.
     Define el wrapper UX (ADR-BACK-008).
 * - ``MenuItemRepo`` (o ``MenuItemQuerySet``)
   - **Critico**
   - Manager con ``visible()``, ``for_user(user)`` —
     consumido por ``UserMenuView``.
 * - ``UserCapabilityResolver``
   - **Critico**
   - Resolver con ``resolve()``, ``resolve_uncached()``,
     ``has_capability()``. Ya documentado en
     rbac-impl-guide §Q9.3 pero sin clase formal en
     domain-model.
 * - ``MenuLifecycleService``
   - Importante
   - State machine para transiciones de UC_ADM_05.
     Ya en implementacion-tecnica de UC_ADM_05 §11.3
     pero sin formalizar como clase de dominio.
 * - ``CriticalCapabilityCatalog`` (o helper)
   - Medio
   - Cache de ``func:critical_set`` con TTL 60s.
     Fragmento de ``UserCapabilityResolver`` o clase
     separada — decision pendiente.
 * - ``MenuArchivePolicy`` (o ``DeprecatedAgePolicy``)
   - Medio
   - Encapsula thresholds 30d / 80d / 90d. Fragmento
     de ``MenuLifecycleService`` o clase separada —
     decision pendiente.
 * - ``UserMenuView`` (Application Service)
   - Bajo
   - Endpoint adapter ``GET /api/v1/menu/``. Vista mas
     que clase de dominio — puede vivir en capa
     "application services" o similar.

### 3.3 Resumen de gaps de domain-model

**3 clases criticas faltantes:**

1. ``MenuItem`` — entidad persistida del nuevo modelo.
2. ``MenuItemRepo`` — repository pattern para queries.
3. ``UserCapabilityResolver`` — resolver con bypass de cache.

**2 clases importantes faltantes:**

4. ``MenuLifecycleService`` — state machine.
5. (bonus si se separa) ``MenuArchivePolicy``.

**Clases existentes a actualizar:**

- ``Function`` → agregar ``is_critical``.
- ``EffectivePermissionsAggregator`` → reemplazar o
  aliar con ``UserCapabilityResolver``.
- ``PermissionCache`` → documentar nueva politica.
- ``Menu`` → deprecar o redefinir como DTO.
- ``NavDomain`` / ``Section`` / ``Action`` → marcar
  como legacy v5.0.0.

## Sección 4 — Plan de cierre del WP

### 4.1 Gaps consolidados (post-design-coverage-review + esta auditoria)

.. list-table::
 :widths: 5 50 15 30
 :header-rows: 1

 * - ID
   - Gap
   - Severidad
   - Categoria
 * - G-1
   - catalogo-funciones.rst MOD_Admin "3 funciones"
   - Critico
   - Catalogo
 * - G-2
   - mapeo-uc.rst sin UC_ADM_04/05
   - Critico
   - Catalogo
 * - G-3
   - BR-006 conteo 64/77
   - Critico
   - Catalogo
 * - G-4
   - use-case-view/admin sin nuevos UCs
   - Importante
   - Vista UC
 * - G-5
   - matriz-dependencias-uc-iact sin nuevos UCs
   - Importante
   - Vista UC
 * - G-6
   - TD-RBAC-03 no registrado
   - Medio
   - Tech debt
 * - G-7
   - "Django ORM" en uc-perm-08 ext
   - Medio
   - STD-010
 * - G-8
   - CNST-033 sin cross-ref
   - Bajo
   - Diferible
 * - G-9
   - Tests bootstrap conteo 64
   - Bajo
   - Catalogo (con G-3)
 * - **G-11 (nuevo)**
   - **Domain-model: MenuItem class**
   - **Critico**
   - **Domain model**
 * - **G-12 (nuevo)**
   - **Domain-model: MenuItemRepo / MenuItemQuerySet class**
   - **Critico**
   - **Domain model**
 * - **G-13 (nuevo)**
   - **Domain-model: UserCapabilityResolver class**
   - **Critico**
   - **Domain model**
 * - **G-14 (nuevo)**
   - **Domain-model: MenuLifecycleService class**
   - **Importante**
   - **Domain model**
 * - **G-15 (nuevo)**
   - **Domain-model: Function update con is_critical**
   - **Importante**
   - **Domain model update**
 * - **G-16 (nuevo)**
   - **Domain-model: PermissionCache update con politica nueva**
   - **Medio**
   - **Domain model update**
 * - **G-17 (nuevo)**
   - **Domain-model: Menu / NavDomain / Section / Action — deprecar v5.0.0**
   - **Medio**
   - **Domain model legacy**
 * - **G-18 (nuevo)**
   - **Domain-model: EffectivePermissionsAggregator alias / replace**
   - **Medio**
   - **Domain model update**

### 4.2 Lotes de cierre propuestos

**Lote C-A — Catalogo (G-1, G-2, G-3, G-9):**

- Actualizar catalogo-funciones.rst §3.11 MOD_Admin con
  6 funciones (3 v5.6.0 + 3 v5.6.x extension), tabla
  diff baseline/extension/current.
- mapeo-uc.rst con filas UC_ADM_04 / UC_ADM_05.
- BR-006 con conteo 67/80 y nota v5.6.x.
- rbac-impl-guide tests bootstrap con conteo 67.

**Lote C-B — Vista UC (G-4, G-5):**

- use-case-view/admin/index.rst: agregar UC_ADM_04/05 a
  diagrama PlantUML + tabla.
- Crear uc-adm-04-resumen y uc-adm-05-resumen en
  use-case-view/admin/.
- matriz-dependencias-uc-iact.rst: agregar filas.

**Lote C-C — Domain model (G-11..G-18):**

- Crear ``menu-item.rst``, ``menu-item-repo.rst``,
  ``user-capability-resolver.rst``,
  ``menu-lifecycle-service.rst``.
- Actualizar ``function.rst`` con ``is_critical``.
- Actualizar ``permission-cache.rst`` con politica
  degraded + key patterns.
- Actualizar ``menu.rst`` con nota "v5.0.0 legacy" o
  redefinir como DTO.
- Actualizar ``effective-permissions-aggregator.rst``
  con cross-ref a ``user-capability-resolver.rst``.
- Actualizar ``index.rst`` del domain-model con los
  nuevos archivos.

**Lote C-D — Misc (G-6, G-7):**

- technical-debt.md: agregar TD-RBAC-03.
- uc-perm-08 ext linea 242: corregir "Django ORM".

**Lote C-E (diferible) — G-8:** CNST-033 cross-ref —
post-cierre del WP.

### 4.3 Volumen estimado

.. list-table::
 :widths: 25 30 25 20
 :header-rows: 1

 * - Lote
   - Archivos modificados
   - Archivos nuevos
   - Tiempo estimado
 * - C-A (catalogo)
   - 4
   - 0
   - bajo
 * - C-B (vista UC)
   - 2
   - 2
   - medio
 * - C-C (domain model)
   - 5
   - 4
   - alto
 * - C-D (misc)
   - 2
   - 0
   - bajo
 * - **Total**
   - **13**
   - **6**
   - **medio-alto**

## Sección 5 — Plan ejecutable propuesto

1. **Resolver §1** (Opcion B aprobada — registrado).
2. **Aplicar Lote C-A** (catalogo) — base de todos los demas.
3. **Aplicar Lote C-D** (misc — STD-010 y tech debt) en
   paralelo con C-A.
4. **Aplicar Lote C-B** (vista UC) — depende de C-A
   (conteo en index podria referenciar 67).
5. **Aplicar Lote C-C** (domain model) — el mas extenso;
   ejecuta despues de C-B.
6. Build sphinx strict EXIT=0 al final.
7. Commit "Close coverage gaps + domain-model classes for
   menu RBAC".
8. Phase 11 TRACK formal con changelog completo del WP +
   lessons learned.

**Lote C-E (G-8 CNST-033)** queda diferido como TD-DOC-NN
para iteracion futura.

## Refs

- ``track/post-design-coverage-review.md`` (gaps G-1..G-10).
- ``strategy/menu-rbac-user-scope-solution-strategy.md``.
- ``strategy/strategy-addendum-gaps-and-module.md``.
- ADR-BACK-008/009/010 (commits cd224ee5).
- CNST-032 v2.0.0 + Q9 + cache-strategy (commit 8ed97a16).
- UC_ADM_04 + UC_PERM_08 ext (commit 86b1696f).
- UC_ADM_05 + scheduled-tasks (commit 43624501).
- ``source/arquitectura-tecnica/domain-model/`` (87 archivos
  existentes — 5 nuevos + 5 updates requeridos).
