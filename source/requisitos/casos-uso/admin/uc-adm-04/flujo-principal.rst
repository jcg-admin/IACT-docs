.. meta::
 :artefacto: UC_ADM_04_FLUJO
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

==========================
3. Flujo Principal
==========================

Caso: invoker con ``manage_menu_catalog`` crea un
``MenuItem`` nuevo asociado a una ``Function`` ya existente.

::

   PASO 1   Invoker abre catalogo de MenuItems        (Interfaz de Usuario)
   PASO 2   Selecciona "Crear MenuItem"               (Interfaz de Usuario)
   PASO 3   Selecciona Function del catalogo
            (codename, name, module)                  (Interfaz de Usuario)
   PASO 4   Define metadata UX:
            display_label, icon, route_path,
            display_order, parent (opcional)          (Interfaz de Usuario)
   PASO 5   Confirma                                  (Interfaz de Usuario)
   PASO 6   POST /api/v1/admin/menu-items/            (Interfaz de Usuario → Servicio de Aplicacion)
   PASO 7   Verificar capability con bypass de cache  (Servicio de Aplicacion)
   PASO 8   Validar Function existe + is_active       (Servicio de Aplicacion → Almacen de Datos)
   PASO 9   Validar Function NO tiene MenuItem ya     (Servicio de Aplicacion → Almacen de Datos)
   PASO 10  Validar parent existe + NOT ARCHIVED      (Servicio de Aplicacion → Almacen de Datos)
   PASO 11  Validar invariantes I-1..I-3              (Servicio de Aplicacion)
   PASO 12  BEGIN TRANSACTION                         (Servicio de Aplicacion)
   PASO 13  INSERT MenuItem (status=DRAFT)            (Servicio de Aplicacion → Almacen de Datos)
   PASO 14  Registrar AuditEvent
            (event_type=MENU_ITEM_CREATED)            (Servicio de Aplicacion → Almacen de Datos)
   PASO 15  COMMIT                                    (Servicio de Aplicacion)
   PASO 16  Invalidar cache de menu post-COMMIT       (Servicio de Aplicacion → Servicio de Cache)
   PASO 17  Responder 201 Created con MenuItem        (Servicio de Aplicacion → Interfaz de Usuario)
   PASO 18  Mostrar confirmacion + redirigir a
            preview admin del nuevo item              (Interfaz de Usuario)

3.1 Detalles por paso
=====================

PASO 7 — Verificacion de capability
-----------------------------------

``manage_menu_catalog.is_critical=True``, por lo cual el
``UserCapabilityResolver.has_capability`` consulta DB sin
pasar por el servicio de cache (AP-2b — bypass). Esto
garantiza strong consistency: si la capability fue revocada
antes de este request, la verificacion lo detecta sin
ventana de stale.

PASO 8-10 — Validaciones de pre-insert
--------------------------------------

- (P3 reforzado) ``Function`` existe y esta activa.
- (I-1 reforzado) ``Function`` no tiene ``MenuItem``
  previo. Si lo tiene, redirigir a UPDATE.
- (P4 reforzado) ``parent`` (si se especifico) existe y
  no esta ARCHIVED.

PASO 13 — INSERT con defaults
-----------------------------

``status="DRAFT"``, ``deprecated_at=NULL``,
``archived_at=NULL``, ``block_auto_archive=False``,
``created_by=invoker``.

PASO 14 — Audit event
---------------------

::

   {
     "event_type": "MENU_ITEM_CREATED",
     "actor_id": <invoker.id>,
     "timestamp": <ISO>,
     "menu_item_id": <created.id>,
     "function_codename": "<codename>",
     "snapshot": { display_label, icon, route_path,
                   display_order, parent_id, status }
   }

PASO 16 — Invalidacion de cache
-------------------------------

Se invalidan dos sets de keys post-COMMIT:

- ``menu:user:{id}`` para todos los users con la capability
  subyacente (set obtenido de
  ``UserAccessGroupAssignment`` filtrado por AGR que
  contiene la ``Function``).
- ``func:critical_set`` (si la nueva ``Function`` es
  critica — caso raro en UC_ADM_04 que solo crea wrapper
  UX sobre Function existente).

Si el servicio de cache falla, el UC continua con
log + telemetria (degraded mode — ADR-BACK-009).

3.2 Variantes del flujo principal
=================================

UC_ADM_04 cubre tres operaciones:

- **CREATE:** descrita arriba.
- **UPDATE:** flujo equivalente con ``PATCH /api/v1/admin/menu-items/{id}/``,
  cambios limitados a metadata UX (no cambia
  ``function`` ni ``status``). Audit event
  ``MENU_ITEM_UPDATED`` con ``before_state`` + ``after_state``.
- **READ / LIST:** ``GET /api/v1/admin/menu-items/`` para
  consulta. Sin invalidacion de cache. Soporta filtros por
  ``status``, ``module``.
