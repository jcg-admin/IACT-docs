.. meta::
 :artefacto: UC_USR_06
 :tipo: Caso de Uso (stub Reservado)
 :dominio: requisitos
 :subdominio: casos_uso/users
 :estado: Reservado
 :version: 0.1.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno
 :origen: incierto — referenciado en uc-auth-03/04/05
          sin decision arquitectonica formal documentada

.. _uc-usr-06:

==============================================
UC_USR_06 — Desbloquear Usuario (RESERVADO)
==============================================

.. warning:: **UC en estado Reservado — sin spec completa**

   Counterpart de UC_USR_05. Aparece referenciado en:

   - ``auth/uc-auth-03/flujos-alternos.rst:22`` —
     "desbloquee via UC_USR_06".
   - ``auth/uc-auth-04/flujos-alternos.rst:97`` —
     "(UC_USR_06) el User ya tenga contrasena".

   La investigacion del WP
   ``2026-05-07-04-08-13-use-case-view-analysis`` confirma
   que nunca existio commit de creacion de este UC.

   Estado **Reservado** hasta que el ejecutor confirme su
   alcance.

Resumen propuesto
=================

UC_USR_06 administraria la transicion inversa al bloqueo:
``state: BLOCKED -> ACTIVE``. Implica:

- Limpiar contador de intentos fallidos (BR-015).
- Auditar el desbloqueo (actor admin que lo emite).
- Notificar al usuario afectado (opcional).
- Re-emitir credenciales si se requiere reset de
  password.

Trazabilidad
============

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **ID**
   - UC_USR_06
 * - **Nombre propuesto**
   - Desbloquear Usuario
 * - **Modulo**
   - MOD_Users
 * - **Capability propuesta**
   - ``unblock_users`` (no existe en catalogo) o
     ``activate_users`` (no existe explicitamente; reverso
     de ``deactivate_users``)
 * - **Estado**
   - **Reservado**
 * - **Counterpart**
   - UC_USR_05 (Bloquear Usuario)

Decision pendiente
==================

Resolver junto con UC_USR_05 — ambos son symmetricos y
deberian decidirse en el mismo ADR.
