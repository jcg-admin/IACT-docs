.. _uc-usr-05-parte-01:

============================================
Parte 1 — Informacion general de UC_USR_05
============================================

1.1 Identificacion
==================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID UC**
   - UC_USR_05
 * - **Nombre**
   - Bloquear Usuario (manual administrativo)
 * - **Version spec**
   - 1.0.0
 * - **Modulo**
   - MOD_Users
 * - **WP**
   - ``2026-05-08-04-10-27-uc-view-domain-alignment``

1.2 Proposito
=============

UC_USR_05 ejecuta el **bloqueo administrativo manual** de
un User: transicion de su ``state`` a ``BLOCKED``, cierre
de Sessions activas, y blacklisting de tokens vivos. La
cuenta y todos sus Assignments se conservan intactos para
posible desbloqueo posterior (UC_USR_06).

El bloqueo manual existe como UC distinto del bloqueo
automatico (BR-015) por dos razones:

- **Trazabilidad de actor**: un evento de bloqueo manual
  identifica al admin que lo origino, no al sistema.
- **Razon de bloqueo distinta**: BR-015 dispara por
  intentos fallidos (riesgo de credencial comprometida);
  UC_USR_05 dispara por decision administrativa
  (compliance, investigacion, sancion).

Diferencias clave con UCs vecinos:

- vs **UC_USR_04 (eliminar)**: UC_USR_04 es terminal
  (``state → ELIMINATED``, no reversible), UC_USR_05 es
  reversible (``state → BLOCKED``, recuperable via
  UC_USR_06).
- vs **BR-015**: misma transicion ``ACTIVE → BLOCKED``
  pero actor distinto (admin vs sistema) y AuditEvent
  con ``reason`` distinta (``ADMIN_BLOCK`` vs
  ``FAILED_LOGIN_LIMIT``).

1.3 Alcance
===========

1.3.1 IN
--------

- Transicion ``User.state: ACTIVE → BLOCKED`` (origen
  ACTIVE unicamente; otros estados → flujo de excepcion).
- Cierre de todas las Sessions ACTIVE
  (``state → CLOSED``, ``close_reason='USER_BLOCKED'``).
- Blacklisting de refresh tokens vivos del User.
- Emision de ``AuditEvent USER_BLOCKED`` con
  ``actor_id`` (admin), ``target_user_id`` (bloqueado),
  ``reason`` (string libre del admin), contadores.
- Captura del motivo administrativo (campo libre obligatorio).

1.3.2 OUT
---------

- Bloqueo automatico (BR-015) — disparado por sistema, no
  por admin; aunque la transicion es la misma, el actor y
  el AuditEvent son distintos.
- Eliminacion logica (UC_USR_04).
- Desbloqueo (UC_USR_06).
- Reset de password (UC_AUTH_03).

1.3.3 Posicion en flujo
-----------------------

UC_USR_05 es **operacion administrativa intermedia y
reversible**. Casos tipicos:

- Empleado bajo investigacion interna; bloqueo preventivo.
- Cuenta comprometida con sospecha pero sin certeza
  (eliminacion seria desproporcionada).
- Sancion temporal por incumplimiento de politica.

Despues de UC_USR_05, el User no puede iniciar sesion
hasta que UC_USR_06 lo desbloquee. Las sesiones existentes
se invalidan inmediatamente.

1.4 Trazabilidad inicial
========================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **BReq satisfecho**
   - BReq-004 (Cumplimiento de Seguridad y Auditoria).
 * - **BRQ legacy**
   - BRQ-USR-005 (parcial).
 * - **Reglas de Negocio**
   - BR-015 (Bloqueo Intentos Fallidos — semantica relacionada
     pero automatica, no manual).
 * - **Restricciones (CNST canonicas)**
   - CNST-009 autenticacion de API,
     CNST-013 manejo estandar de excepciones,
     CNST-025 audit inmutable,
     CNST-026 sin PII en payload audit.
 * - **Funcion RBAC (canonica)**
   - ``block_users`` — la dependencia del UC es la
     funcion, no un AGR especifico.
 * - **AGR de conveniencia**
   - AGR-002 user_admin_group contiene esta funcion.
 * - **UC Relacionados**
   - UC_USR_06 (desbloqueo — inversa),
     UC_USR_04 (eliminar — terminal alternativa),
     UC_AUTH_05 (gestion sessions — patron de cierre masivo),
     UC_AUD_* (consulta historica del bloqueo).
 * - **Clase primaria**
   - ``User`` (escritura state).
 * - **Clases secundarias**
   - ``Session`` (escritura masiva — close),
     ``BlacklistedToken`` (INSERT N),
     ``AuditEvent`` (emision USER_BLOCKED).
