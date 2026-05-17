.. meta::
 :artefacto: UC_ADM_04_INFO
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
   - UC_ADM_04
 * - **Nombre**
   - Gestionar Catalogo de MenuItems
 * - **Modulo**
   - MOD_Admin
 * - **Capability**
   - ``manage_menu_catalog`` (``is_critical=True``)
 * - **AGR titular**
   - AGR-010 (``system_admin``)
 * - **Criticidad**
   - Importante
 * - **Estado**
   - Borrador (Phase 7 — WP menu-rbac-user-scope)

1.1 Resumen
===========

UC_ADM_04 documenta el flujo de **alta, edicion y consulta**
del catalogo de MenuItems. El ``system_admin`` crea
``MenuItem`` como wrapper UX 1:1 sobre una ``Function``
existente del catalogo RBAC, define la metadata visual
(label, icono, orden, ruta) y define la jerarquia visual via
``parent``. NO modifica permisos: la capability subyacente
(``Function``) ya existe.

UC_ADM_04 NO gestiona transiciones de estado del lifecycle
(DRAFT → ACTIVE → DEPRECATED → ARCHIVED) — eso es UC_ADM_05.

1.2 Objetivo
============

Permitir que el ``system_admin`` mantenga el catalogo UX del
menu sincronizado con el catalogo RBAC v5.6.0:

- Cuando se agrega una nueva ``Function`` que debe verse en
  el sidebar, crear su ``MenuItem`` wrapper.
- Cuando cambia el label visual de una capability ya
  existente, editar el ``MenuItem``.
- Cuando se quiere reorganizar el orden o jerarquia visual,
  ajustar ``display_order`` y ``parent``.

1.3 Ambito
==========

**In-scope:**

- CRUD de ``MenuItem`` (excepto cambios de ``status``).
- Validacion de invariantes I-1..I-4 (ver CNST-032 v2.0.0).
- Audit trail de cada cambio.

**Out-of-scope:**

- Transiciones de estado (UC_ADM_05).
- Creacion / modificacion del catalogo de ``Function``
  (UC_ADM_03).
- Asignacion de ``Function`` a AGR (UC_PERM_06).

1.4 Reglas de negocio referenciadas
====================================

- **BR-MENU-01..04** — visibilidad por estado y capability
  (CNST-032 v2.0.0 §5).
- **BR-AUDIT-01** — todo cambio de catalogo deja entrada
  en audit log.

1.5 Constraints normativas
==========================

- :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
  (v2.0.0 — wrapper UX obligatorio).
- :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`
  (parent es UI, no jerarquia de permisos).
- :doc:`/normativa/estandares/std-010-vocabulario-abstracto`
  (vocabulario canonico en narrativa).

1.6 ADRs aplicables
====================

- :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`.
- :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`.
- :doc:`/backend/adr-back-010-function-is-critical-governance`.
