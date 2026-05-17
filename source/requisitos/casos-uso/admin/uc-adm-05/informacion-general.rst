.. meta::
 :artefacto: UC_ADM_05_INFO
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

==============================
1. Informacion General
==============================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **ID**
   - UC_ADM_05
 * - **Nombre**
   - Gestionar Lifecycle de MenuItem
 * - **Modulo**
   - MOD_Admin
 * - **Capability**
   - ``manage_menu_lifecycle`` (``is_critical=True``)
 * - **AGR titular**
   - AGR-010 (``system_admin``)
 * - **Criticidad**
   - Importante
 * - **Estado**
   - Borrador

1.1 Resumen
===========

UC_ADM_05 documenta las **transiciones de estado** del
``MenuItem`` (DRAFT → ACTIVE, ACTIVE → DEPRECATED,
DEPRECATED → ACTIVE, DEPRECATED → ARCHIVED, ARCHIVED →
ACTIVE) y la gestion del flag ``block_auto_archive`` que
controla el auto-archive a los 90 dias en DEPRECATED.

UC_ADM_05 NO modifica metadata UX (label, icon, route_path,
display_order, parent) — eso es UC_ADM_04.

1.2 Maquina de estados
======================

::

   ┌──────────┐  publicar    ┌───────────┐  deprecar      ┌───────────────┐
   │  DRAFT   │ ───────────> │  ACTIVE   │ ──────────────>│  DEPRECATED   │
   │          │              │           │                │               │
   └──────────┘              └─────────^─┘                └──────^──────┬─┘
                                       │ reactivar                │     │
                                       │                          │     │ archivar
                                       └──────────────────────────┘     │ (manual o
                                                                          auto a 90d
                                                                          si !block)
                                                                       ┌─v────────┐
                                                  reactivar            │          │
                                                  ┌───────────────────>│ ARCHIVED │
                                                  │                    │          │
                                                  └────────────────────┴──────────┘

Las 6 transiciones cubiertas:

1. DRAFT → ACTIVE (publicar)
2. ACTIVE → DEPRECATED (deprecar)
3. DEPRECATED → ACTIVE (reactivar)
4. DEPRECATED → ARCHIVED (archivar manual)
5. DEPRECATED → ARCHIVED (auto-archive a 90d, condicional)
6. ARCHIVED → ACTIVE (reactivar)

1.3 Politica de auto-archive (gap #3 resuelto)
==============================================

El Planificador de Tareas ejecuta diariamente el job de
verificacion de items en DEPRECATED:

.. list-table::
 :widths: 20 80
 :header-rows: 1

 * - Dia desde DEPRECATED
   - Accion
 * - 30
   - Warning a system_admin: "MenuItem >30d en DEPRECATED"
 * - 80
   - Pre-archive notification: "auto-archive en 10 dias
     salvo block_auto_archive=True"
 * - 90
   - Auto-archive si NOT ``block_auto_archive``;
     o critical alert si ``block_auto_archive=True``

**Por que el warning a 80 dias y no antes (e.g., 60d):**
80 dias es la **ultima ventana** de 10 dias antes del
auto-archive a 90d. El warning a 30d ya alerto al admin de
forma temprana. El warning a 80d es la senal "decision o
accion explicita ya"; mas temprano se confunde con el
warning genericos a 30d.

1.4 Flag ``block_auto_archive``
===============================

Para mantener un item en DEPRECATED indefinidamente, el
admin debe activar el flag con justificacion. Requiere:

- ``block_auto_archive=True``.
- ``block_reason`` no vacio y ≥ 20 caracteres.
- ``block_set_by`` registrado.
- ``block_set_at`` registrado.
- Audit log con la activacion del flag.

Cualquier cambio del flag genera entrada de audit log
adicional.

1.5 Reglas de negocio referenciadas
====================================

- BR-MENU-01..04 (CNST-032 v2.0.0).
- BR-AUDIT-01 (audit log obligatorio).

1.6 ADRs aplicables
====================

- :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`
  (estados DRAFT/ACTIVE/DEPRECATED/ARCHIVED).
- :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
  (invalidacion de cache).
- :doc:`/backend/adr-back-010-function-is-critical-governance`
  (capability bypass de cache).
- WP origen ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``
  strategy addendum gap #3.
