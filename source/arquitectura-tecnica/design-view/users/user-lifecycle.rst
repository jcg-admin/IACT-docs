.. meta::
 :artefacto: AT_DESIGN_STATE_USER
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: User
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_design_state_user:

============================================================
Design View — Ciclo de Vida: User
============================================================

Maquina de estados de la entidad ``User``. Cubre desde la
creacion del usuario hasta su bloqueo administrativo, con
transiciones reversibles entre activo e inactivo y terminal
en bloqueado.

.. uml::
 :caption: User FSM — ACTIVE / INACTIVE / BLOCKED.

 @startuml

 [*] --> ACTIVE : Admin.create_user()

 ACTIVE --> INACTIVE : Admin.deactivate()\n(suspension temporal)
 INACTIVE --> ACTIVE : Admin.reactivate()

 ACTIVE --> BLOCKED : Admin.block()\nor SystemPolicy.block()
 INACTIVE --> BLOCKED : Admin.block()

 BLOCKED --> [*] : Admin.purge()\n(GDPR / retencion)

 note right of ACTIVE
   El usuario puede autenticar y
   recibir tokens JWT. Sus permisos
   efectivos se derivan de los
   grupos asignados (RBAC).
 end note

 note right of INACTIVE
   No autentica. Tokens activos NO
   se revocan automaticamente —
   expiran por TTL natural.
   Reversible sin perdida de
   asignaciones de grupos.
 end note

 note bottom of BLOCKED
   No autentica. Todos los tokens
   activos del usuario se revocan
   inmediatamente (jti blacklist).
   Decision administrativa o por
   politica del sistema (e.g.
   N intentos fallidos).
 end note

 @enduml

Reglas de transicion
=====================

.. list-table::
 :widths: 25 25 50
 :header-rows: 1

 * - Transicion
   - Trigger
   - Efecto colateral
 * - ``[*] → ACTIVE``
   - ``Admin.create_user()``
   - Asignacion inicial de grupos (UC_USR_01)
 * - ``ACTIVE → INACTIVE``
   - ``Admin.deactivate()``
   - Sin revocacion de tokens
 * - ``INACTIVE → ACTIVE``
   - ``Admin.reactivate()``
   - Mantiene asignaciones de grupos previas
 * - ``ACTIVE → BLOCKED``
   - ``Admin.block()`` o politica
   - Revoca todos los tokens via jti blacklist
 * - ``INACTIVE → BLOCKED``
   - ``Admin.block()``
   - Idem
 * - ``BLOCKED → [*]``
   - ``Admin.purge()``
   - Eliminacion fisica (GDPR / retencion)

Cualquier otra combinacion responde HTTP 409 Conflict.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user` — entidad
   y atributo ``state``.
 - :doc:`bounded-context` — contexto del modulo Users.
 - :doc:`interaction-pattern` — patron de orquestacion
   user-admin.
 - :doc:`/arquitectura-tecnica/design-view/auth/session-lifecycle` —
   relacion con ciclo de vida de sesion.
