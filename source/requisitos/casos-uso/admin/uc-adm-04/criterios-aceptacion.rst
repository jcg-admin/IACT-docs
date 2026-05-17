.. meta::
 :artefacto: UC_ADM_04_CA
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

============================
9. Criterios de Aceptacion
============================

Formato Given/When/Then.

9.1 CA-01: CREATE exitoso con defaults
======================================

**DADO** un invoker con ``manage_menu_catalog`` y una
``Function`` activa sin ``MenuItem`` previo,

**CUANDO** ejecuta ``POST /api/v1/admin/menu-items/`` con
``{function_id, display_label, icon, route_path}``,

**ENTONCES**:

- Status 201.
- Body con ``id`` generado, ``status="DRAFT"``,
  ``deprecated_at=null``, ``archived_at=null``.
- Audit log contiene ``MENU_ITEM_CREATED`` con
  ``actor_id=invoker.id``.
- Cache ``menu:user:{id}`` invalidado para todos los users
  con la ``Function`` subyacente.

9.2 CA-02: CREATE rechazo por capability ausente
================================================

**DADO** un invoker sin ``manage_menu_catalog``,

**CUANDO** ejecuta el POST,

**ENTONCES**:

- Status 403.
- Audit log contiene ``CAPABILITY_DENIED``.
- Sin INSERT ni invalidacion.

9.3 CA-03: CREATE rechazo por Function inexistente
==================================================

**DADO** ``function_id`` inexistente o con
``is_active=False``,

**CUANDO** ejecuta el POST,

**ENTONCES**:

- Status 422.
- Cuerpo: ``{"errors": [{"field": "function",
  "code": "not_found_or_inactive"}]}``.

9.4 CA-04: CREATE rechazo por I-1 (Function ya con MenuItem)
============================================================

**DADO** ``function_id`` ya tiene un ``MenuItem`` asociado,

**CUANDO** ejecuta el POST,

**ENTONCES**:

- Status 409.
- Cuerpo incluye ``existing_menu_item_id``.

9.5 CA-05: UPDATE de display_label
==================================

**DADO** un ``MenuItem`` en ``status=ACTIVE``,

**CUANDO** invoker ejecuta ``PATCH .../{id}/`` con
``{display_label: "Nuevo Label"}``,

**ENTONCES**:

- Status 200.
- ``MenuItem.display_label`` actualizado en DB.
- Audit log contiene ``MENU_ITEM_UPDATED`` con
  ``before_state.display_label`` y ``after_state.display_label``.
- Cache invalidado.

9.6 CA-06: UPDATE bloqueado en ARCHIVED
=======================================

**DADO** un ``MenuItem`` en ``status=ARCHIVED``,

**CUANDO** invoker ejecuta PATCH con cualquier campo
mutating,

**ENTONCES**:

- Status 409.
- Cuerpo: ``{"error": "menu_item_archived"}``.
- Excepcion: PATCH para reactivar (transicion ARCHIVED →
  ACTIVE) NO esta cubierto por UC_ADM_04 — se maneja en
  UC_ADM_05.

9.7 CA-07: LIST con filtros
===========================

**DADO** invoker con la capability,

**CUANDO** ejecuta ``GET .../?status=DRAFT&module=ADM``,

**ENTONCES**:

- Status 200.
- Solo se devuelven items en ``status=DRAFT`` cuya
  ``Function.module="ADM"``.
- Paginado con ``page=1, page_size=50`` por default.

9.8 CA-08: Bulk reorder atomico
===============================

**DADO** invoker con la capability y 5 ``MenuItem``
existentes,

**CUANDO** ejecuta ``PATCH .../bulk-reorder/`` con la lista
de 5 ``{id, display_order}``,

**ENTONCES**:

- Status 200.
- Los 5 items reflejan el nuevo orden en DB.
- 1 sola entrada audit ``MENU_ITEM_BULK_REORDERED`` con
  lista de cambios.
- Si cualquier ID es invalido: rollback completo, status
  422, ningun cambio aplicado.

9.9 CA-09: Cache fail no bloquea operacion
==========================================

**DADO** servicio de cache caido (degraded mode),

**CUANDO** invoker ejecuta CREATE / UPDATE,

**ENTONCES**:

- Status 201 / 200 (operacion exitosa).
- Audit log contiene tanto ``MENU_ITEM_CREATED`` como
  ``CACHE_INVALIDATION_FAILED``.
- Metric ``rbac.cache.invalidation_failed`` +1.

9.10 CA-10: Capability bypass real (no cache stale)
===================================================

**DADO** invoker que tenia ``manage_menu_catalog`` cacheada
y le revocaron la capability hace 1 segundo,

**CUANDO** invoker ejecuta cualquier operacion mutating,

**ENTONCES**:

- Status 403 (la capability fue verificada en DB sin pasar
  por cache, gracias a ``is_critical=True``).
- No hay ventana de stale.
