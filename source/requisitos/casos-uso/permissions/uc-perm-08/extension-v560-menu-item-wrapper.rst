.. meta::
 :artefacto: UC_PERM_08_EXT_V560
 :tipo: Caso de Uso (extension)
 :dominio: requisitos
 :subdominio: casos_uso/permissions
 :estado: Borrador
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Importante

=====================================================
UC_PERM_08 — Extension v5.6.0: MenuItem Wrapper UX
=====================================================

Esta extension actualiza UC_PERM_08 para reflejar el modelo
RBAC v5.6.0 con la capa UX persistida ``MenuItem``
(ADR-BACK-008, CNST-032 v2.0.0). El UC base
:doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
sigue vigente; esta extension formaliza el shape concreto del
endpoint y la integracion con el catalogo de ``MenuItem``.

----

E.1 Cambio principal — endpoint canonico
========================================

E.1.1 Endpoint
--------------

::

   GET /api/v1/menu/
   Authorization: Bearer <jwt>

E.1.2 Shape de respuesta — flat
--------------------------------

::

   200 OK
   {
     "capabilities": [
       "view_reports",
       "manage_menu_catalog",
       "view_own_state"
     ],
     "menu_items": [
       {
         "id": 12,
         "codename": "view_reports",
         "display_label": "Mis Reportes",
         "icon": "BarChartIcon",
         "route_path": "/reports",
         "display_order": 10,
         "parent_id": null,
         "status": "ACTIVE"
       },
       {
         "id": 18,
         "codename": "manage_menu_catalog",
         "display_label": "Gestionar Menu",
         "icon": "MenuIcon",
         "route_path": "/admin/menu",
         "display_order": 90,
         "parent_id": 1,
         "status": "ACTIVE"
       }
     ]
   }

**Estructura flat** (no jerarquica). Frontend reconstruye
arbol via ``parent_id`` solo si necesita render anidado.

E.1.3 Por que flat y no nested
------------------------------

- **Composicion del lado del cliente:** el frontend ya
  tiene logica de tree para sidebar y breadcrumb. Recibir
  flat permite reusar esa logica.
- **Cache simple:** una sola key
  ``menu:user:{id}`` invalidable atomicamente.
- **STD-010 narrativa:** flat es el shape canonico
  documentado en CNST-032 v2.0.0 §2.2.

----

E.2 Computo del campo ``capabilities``
=======================================

E.2.1 Fuente
------------

``UserCapabilityResolver.resolve(user)`` — cache-first con
TTL 300s, degraded mode ante falla del servicio de cache
(ADR-BACK-009 + Q9.3 de
:doc:`/backend/rbac-implementation-guide`).

E.2.2 Computo
-------------

Set de codenames de ``Function`` activas asociadas a los
``AccessGroup`` del user via
``UserAccessGroupAssignment``, filtrando por
``expires_at`` no vencido.

E.2.3 Por que el frontend recibe el set completo
------------------------------------------------

El frontend usa ``capabilities`` para decisiones de UI
fuera del menu (e.g., mostrar / ocultar botones, tooltips
de acceso, redirecciones desde URL directa). Devolver solo
``menu_items`` no cubre esos casos.

----

E.3 Computo del campo ``menu_items``
=====================================

E.3.1 Filtro
------------

::

   MenuItem.objects.for_user(user)
     = MenuItem.objects.filter(
         status="ACTIVE",
         function__is_active=True,
         function__codename__in=user.capabilities,
       )

Items en ``DRAFT``, ``DEPRECATED`` o ``ARCHIVED`` con
visibilidad especial:

.. list-table::
 :widths: 20 20 30 30
 :header-rows: 1

 * - status
   - is_active Function
   - User con capability
   - En respuesta
 * - ACTIVE
   - True
   - Si
   - Si
 * - ACTIVE
   - True
   - No
   - No
 * - DRAFT
   - True
   - Si
   - No (solo preview admin)
 * - DEPRECATED
   - True
   - Si
   - Si, con flag ``status="DEPRECATED"``
 * - ARCHIVED
   - cualquiera
   - cualquiera
   - No
 * - cualquiera
   - False
   - cualquiera
   - No

E.3.2 Order
-----------

``ORDER BY display_order ASC``. Si el frontend reconstruye
arbol, debe respetar ``display_order`` dentro de cada
nivel ``parent_id``.

----

E.4 Cache
=========

E.4.1 Key pattern
-----------------

``menu:user:{user_id}`` — TTL 300s.

E.4.2 Invalidacion
------------------

Invalidacion explicita post-COMMIT en cada UC mutating
que afecte:

- El catalogo de ``MenuItem`` (UC_ADM_04, UC_ADM_05).
- La composicion de ``AccessGroup`` (UC_PERM_06).
- La asignacion de user a AGR (UC_PERM_05).
- La revocacion / expiracion de asignaciones (UC_PERM_07).

E.4.3 Falla del servicio de cache
---------------------------------

Degraded mode (ADR-BACK-009): el endpoint sirve la
respuesta consultando DB directamente. UC continua.

----

E.5 Defense-in-depth
=====================

El endpoint ``GET /api/v1/menu/`` es **filtro de
superficie**. Cada endpoint protegido del backend
verifica la capability **independientemente** del menu
servido (CNST-032 v2.0.0 §3.2 + UC_PERM_07 spec base).

Si un user con la capability revocada hace la peticion
durante la ventana TTL del cache, puede recibir el item
en la respuesta — pero el endpoint backend al que el
item apunta rechaza con 403 (la verificacion de capability
en cada request es la fuente de verdad de acceso, no el
menu).

Para capabilities con ``is_critical=True``, el endpoint
backend bypassa el cache (AP-2b de ADR-BACK-010), por lo
cual una revocacion se refleja inmediatamente en
verificacion.

----

E.6 Cambios respecto a UC_PERM_08 v5.0.0
========================================

.. list-table::
 :widths: 30 35 35
 :header-rows: 1

 * - Aspecto
   - v5.0.0 (base)
   - v5.6.0 (esta extension)
 * - Endpoint
   - ``GET /api/permisos/verificar/<user_id>/menu/``
   - ``GET /api/v1/menu/`` (sin ``user_id`` — toma del JWT)
 * - Computo del menu
   - funcion SQL legacy ``obtener_menu_usuario(user_id)``
   - Query del Servicio de Aplicacion sobre el Almacen de
     Datos via ``MenuItemRepo.for_user`` (motor concreto en
     ``arquitectura-tecnica/``)
 * - Shape
   - Jerarquico (dominio → seccion → accion)
   - Flat ``{capabilities, menu_items}``
 * - Persistencia del catalogo UX
   - No (computado siempre)
   - Si (``MenuItem`` lifecycle-managed)
 * - Cache
   - Implicita (DB query cache)
   - Explicita (``menu:user:{id}`` TTL 300s)
 * - Falla del cache
   - N/A
   - Degraded mode

----

E.7 Trazabilidad
================

- :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`.
- :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`.
- :doc:`/backend/adr-back-010-function-is-critical-governance`.
- :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`
  (v2.0.0 — wrapper UX obligatorio).
- :doc:`/backend/rbac-implementation-guide` §Q9.6 (codigo
  del endpoint ``UserMenuEndpoint``).
- WP de origen:
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``.
