.. _uc-usr-06-parte-01:

============================================
Parte 1 — Informacion general de UC_USR_06
============================================

1.1 Identificacion
==================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID UC**
   - UC_USR_06
 * - **Nombre**
   - Desbloquear Usuario
 * - **Version spec**
   - 1.0.0
 * - **Modulo**
   - MOD_Users
 * - **WP**
   - ``2026-05-08-04-10-27-uc-view-domain-alignment``

1.2 Proposito
=============

UC_USR_06 ejecuta el **desbloqueo administrativo** de un
User: transicion de su ``state`` de ``BLOCKED`` a
``ACTIVE``, y emision de AuditEvent ``USER_UNBLOCKED``
con referencia al evento de bloqueo original.

UC_USR_06 desbloquea ambos casos:

- **Bloqueo manual** (UC_USR_05): admin previamente
  ejecuto el bloqueo. Desbloquear es decision
  administrativa de revertir.
- **Bloqueo automatico** (BR-015): sistema disparo
  bloqueo por intentos fallidos. Desbloquear es decision
  administrativa tras verificar que no hubo intento de
  intrusion real (e.g., el User olvido la contrasena
  varias veces).

En ambos casos el AuditEvent ``USER_UNBLOCKED`` referencia
al ``original_block_event_id`` para preservar trazabilidad
completa: bloqueo → desbloqueo es un par auditable.

Diferencias con UCs vecinos:

- vs **UC_USR_05**: operacion inversa.
- vs **UC_USR_04**: NO desbloquea ELIMINATED — ese es
  estado terminal; recovery requiere otro UC futuro.
- vs **UC_AUTH_03 (recover password)**: recover-password
  resuelve credencial olvidada/comprometida; UC_USR_06
  resuelve estado bloqueado por sistema o admin.

1.3 Alcance
===========

1.3.1 IN
--------

- Transicion ``User.state: BLOCKED → ACTIVE``.
- Emision de ``AuditEvent USER_UNBLOCKED`` con
  ``actor_id`` (admin), ``target_user_id``,
  ``original_block_event_id`` (FK al USER_BLOCKED previo
  o ACCOUNT_LOCKED automatico), ``reason`` (motivo del
  desbloqueo, texto libre).
- Validacion de causa del bloqueo previo (lookup del
  ultimo AuditEvent del User para enriquecer el evento
  USER_UNBLOCKED).

1.3.2 OUT
---------

- Restauracion de Sessions cerradas — los Sessions
  permanecen ``CLOSED``; el User debe iniciar nueva
  sesion (UC_AUTH_01).
- Restauracion de tokens blacklistados — permanecen
  blacklistados; el User obtiene nuevos tokens al
  re-loguearse.
- Modificacion de Assignments (preservados durante el
  bloqueo) — UC_USR_06 NO los altera.
- Reset de password — UC_AUTH_03.
- Restauracion de User ELIMINATED — fuera de scope.

1.3.3 Posicion en flujo
-----------------------

UC_USR_06 es **operacion administrativa de
restauracion**. Casos tipicos:

- Conclusion de investigacion interna sin sancion.
- Verificacion de que el bloqueo automatico (BR-015) fue
  falso positivo — el User olvido password sin
  intencion maliciosa.
- Reactivacion de cuenta tras periodo de sancion
  cumplido.

Despues de UC_USR_06, el User puede iniciar sesion
normalmente. Los privilegios RBAC (Assignments) que tenia
antes del bloqueo siguen vigentes (no se borraron).

1.4 Trazabilidad inicial
========================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **BReq satisfecho**
   - BReq-004 (Cumplimiento de Seguridad y Auditoria).
 * - **Reglas de Negocio**
   - BR-015 (UC_USR_06 desbloquea bloqueos automaticos).
 * - **Restricciones (CNST canonicas)**
   - CNST-009 autenticacion,
     CNST-013 manejo estandar de excepciones,
     CNST-025 audit inmutable,
     CNST-026 sin PII en payload audit.
 * - **Funcion RBAC (canonica)**
   - ``unblock_users``.
 * - **AGR de conveniencia**
   - AGR-002 user_admin_group.
 * - **UC Relacionados**
   - UC_USR_05 (bloqueo — inversa),
     UC_AUTH_01 (login — habilitado tras unblock),
     UC_AUD_* (consulta del par bloqueo/desbloqueo).
 * - **Clase primaria**
   - ``User`` (escritura state).
 * - **Clases secundarias**
   - ``AuditEvent`` (consulta del block original +
     emision de USER_UNBLOCKED).
