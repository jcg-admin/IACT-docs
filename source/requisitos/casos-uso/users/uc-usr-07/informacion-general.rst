.. _uc-usr-07-parte-01:

============================================
Parte 1 — Informacion general de UC_USR_07
============================================

1.1 Identificacion
==================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID UC**
   - UC_USR_07
 * - **Nombre**
   - Editar Perfil Propio
 * - **Version spec**
   - 1.0.0
 * - **Modulo**
   - MOD_Users
 * - **WP**
   - ``2026-05-08-04-10-27-uc-view-domain-alignment``

1.2 Proposito
=============

UC_USR_07 permite que el User autenticado edite **campos
no sensibles de su propio perfil** sin requerir
intervencion administrativa.

Campos editables:

- ``full_name`` — nombre completo del User.
- ``email`` — email de contacto (con re-verificacion de
  unicidad).

Campos NO editables (requieren UC_USR_03 admin):

- ``username`` (login id, inmutable).
- ``state`` (lifecycle managed).
- ``primary_access_group_id`` (privilegio).
- ``segment_id`` (data scope).
- ``user_id`` (PK).

Diferencias con UCs vecinos:

- vs **UC_USR_03**: UC_USR_03 lo ejecuta un admin sobre
  otro User; UC_USR_07 lo ejecuta el User sobre si mismo.
  Capability distinta (``edit_own_profile`` vs
  ``modify_users``).
- vs **UC_AUTH_04 (cambiar password)**: UC_USR_07 NO
  toca password. Cambio de password es flujo de
  credenciales con su propia logica de validacion.

1.3 Alcance
===========

1.3.1 IN
--------

- Actualizacion de ``User.full_name`` (texto, max 255).
- Actualizacion de ``User.email`` con verificacion:

  - Formato valido (regex RFC 5322 simple).
  - Unicidad (no colision con email de otro User).

- Emision de ``AuditEvent PROFILE_UPDATED`` con diff
  (campos modificados y valores antes/despues — sin
  guardar PII en payload, solo flags de cambio).

1.3.2 OUT
---------

- Cualquier cambio de campos sensibles — UC_USR_03.
- Cambio de password — UC_AUTH_04.
- Edicion del perfil de otro User — UC_USR_03.
- Cambio de username — no permitido por ningun UC
  (username es identidad inmutable).

1.3.3 Posicion en flujo
-----------------------

UC_USR_07 es **operacion frecuente self-service**. Casos
tipicos:

- User actualiza su email tras cambio de proveedor.
- User corrige tipo en su nombre completo.

UC_USR_07 NO afecta sesion, permisos, ni auditoria
operacional. La sesion del User permanece vigente tras
la edicion.

1.4 Trazabilidad inicial
========================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **BReq satisfecho**
   - BReq-002 (Experiencia de Usuario), BReq-004
     (Auditoria).
 * - **Restricciones (CNST canonicas)**
   - CNST-009 autenticacion,
     CNST-013 manejo estandar de excepciones,
     CNST-025 audit inmutable,
     CNST-026 sin PII en payload audit.
 * - **Funcion RBAC (canonica)**
   - ``edit_own_profile`` (default a todos los Users
     activos — asignacion automatica al crear User).
 * - **AGR**
   - No aplica — la funcion ``edit_own_profile`` se
     asigna directamente al User al creacion (UC_USR_01),
     no a traves de AGR.
 * - **UC Relacionados**
   - UC_USR_03 (modificacion administrativa),
     UC_AUTH_04 (cambiar password),
     UC_AUD_* (consulta del PROFILE_UPDATED).
 * - **Clase primaria**
   - ``User`` (escritura full_name / email).
 * - **Clases secundarias**
   - ``AuditEvent`` (emision PROFILE_UPDATED).
