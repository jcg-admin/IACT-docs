.. meta::
 :artefacto: UC_ADM_05_CA
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

============================
9. Criterios de Aceptacion
============================

9.1 CA-01: DRAFT → ACTIVE exitoso
==================================

**DADO** un MenuItem en DRAFT con Function activa,

**CUANDO** invoker con ``manage_menu_lifecycle`` ejecuta
``POST .../publish/``,

**ENTONCES**:

- Status 200.
- ``status="ACTIVE"``, ``deprecated_at=null``,
  ``archived_at=null``.
- Audit ``LIFECYCLE_TRANSITION DRAFT->ACTIVE``.
- Cache invalidado.

9.2 CA-02: ACTIVE → DEPRECATED registra deprecated_at
=====================================================

**DADO** un MenuItem ACTIVE,

**CUANDO** invoker ejecuta ``POST .../deprecate/``,

**ENTONCES**:

- ``status="DEPRECATED"``, ``deprecated_at`` igual a
  ``timestamp`` del COMMIT (precision segundos).
- Endpoint ``GET /api/v1/menu/`` devuelve el item con
  ``status="DEPRECATED"``.

9.3 CA-03: DEPRECATED → ACTIVE limpia campos derivados
======================================================

**DADO** un MenuItem DEPRECATED con
``deprecated_at != null`` y ``block_auto_archive=True``,

**CUANDO** invoker ejecuta ``POST .../reactivate/``,

**ENTONCES**:

- ``status="ACTIVE"``, ``deprecated_at=null``,
  ``block_auto_archive=False``, ``block_reason=""``,
  ``block_set_by=null``, ``block_set_at=null``.

9.4 CA-04: DEPRECATED → ARCHIVED preserva deprecated_at
=======================================================

**DADO** un MenuItem DEPRECATED con
``deprecated_at='2026-04-01'``,

**CUANDO** invoker ejecuta ``POST .../archive/``,

**ENTONCES**:

- ``status="ARCHIVED"``, ``archived_at`` igual al COMMIT,
  ``deprecated_at`` SIGUE siendo ``'2026-04-01'``.

9.5 CA-05: Transicion invalida rechazada
========================================

**DADO** un MenuItem en DRAFT,

**CUANDO** invoker intenta ``POST .../deprecate/`` (DRAFT
no puede ir directo a DEPRECATED),

**ENTONCES**:

- Status 409.
- Cuerpo: ``{"error": "invalid_transition",
  "current_status": "DRAFT", "requested": "DEPRECATED"}``.
- Sin cambios en DB.

9.6 CA-06: Publicar con Function inactiva rechazado
===================================================

**DADO** un MenuItem DRAFT cuya Function tiene
``is_active=False``,

**CUANDO** invoker ejecuta publish,

**ENTONCES**:

- Status 422 con
  ``{"error": "function_inactive"}``.
- Sin transicion.

9.7 CA-07: block_reason invalido rechazado
==========================================

**DADO** un MenuItem DEPRECATED,

**CUANDO** invoker ejecuta ``POST .../block-archive/``
con ``block_reason="X"``,

**ENTONCES**:

- Status 422 con error de longitud minima 20.

9.8 CA-08: Auto-archive a 90d con block=False
=============================================

**DADO** un MenuItem DEPRECATED con
``deprecated_at = now() - 91 dias`` y
``block_auto_archive=False``,

**CUANDO** el Planificador ejecuta el job diario,

**ENTONCES**:

- ``status="ARCHIVED"``, ``archived_at=now()``.
- Audit ``LIFECYCLE_AUTO_ARCHIVED`` con
  ``actor='system'``, ``days_in_deprecated=91``.
- Notificacion al system_admin con resumen.

9.9 CA-09: Auto-archive bloqueado por block=True
================================================

**DADO** un MenuItem DEPRECATED con
``deprecated_at = now() - 91 dias`` y
``block_auto_archive=True``,

**CUANDO** el Planificador ejecuta el job,

**ENTONCES**:

- ``status="DEPRECATED"`` SIN cambios.
- Critical alert al system_admin (no warning, alert
  porque excedio 90d con bloqueo activo).

9.10 CA-10: Pre-archive notification a 80d
==========================================

**DADO** un MenuItem DEPRECATED con
``deprecated_at = now() - 81 dias`` y
``block_auto_archive=False``,

**CUANDO** el Planificador ejecuta el job de notificacion,

**ENTONCES**:

- Sin cambios en DB.
- Notificacion ``"auto-archive en 9 dias"`` enviada al
  system_admin.

9.11 CA-11: ARCHIVED invisible en endpoint
==========================================

**DADO** un MenuItem ARCHIVED,

**CUANDO** un user con la capability subyacente consulta
``GET /api/v1/menu/``,

**ENTONCES**:

- ``menu_items`` NO incluye el item.
- ``capabilities`` SI incluye el codename (la capability
  sigue accesible via URL directa).

9.12 CA-12: Idempotencia del job de auto-archive
================================================

**DADO** que el Planificador ejecuto el job hoy a las
02:00 procesando 5 items,

**CUANDO** el Planificador re-ejecuta el job hoy a las
03:00 (re-trigger manual),

**ENTONCES**:

- 0 items procesados (ya archivados).
- 0 audits adicionales.
- 0 notificaciones duplicadas.
