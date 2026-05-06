.. meta::
 :artefacto: AT_DESIGN_STATE_ASSIGNMENT
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: Assignment
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_design_state_assignment:

============================================================
Design View — Ciclo de Vida: Assignment
============================================================

Maquina de estados de la entidad ``Assignment``. Cubre el ciclo
de una asignacion de FunctionGroup a un User: creacion (con
verificacion SoD), expiracion natural por TTL, o revocacion
explicita.

Per BR-009, las "bajas" son logicas — el Assignment nunca se
elimina, transita a un estado terminal (expired/revoked).

.. uml::
 :caption: Assignment FSM — active -> expired | revoked.

 @startuml

 [*] --> active : create()\n[SoD check OK]

 active --> active : update(expires_at)\n(extiende ttl)

 active --> expired : expires_at reached
 active --> revoked : Admin.revoke()

 expired --> [*]
 revoked --> [*]

 note right of active
   Verify SoD se aplica antes
   de crear. Solo Assignments
   en estado=active cuentan
   en effective_set.
 end note

 note right of expired
   No DELETE — fila persiste
   con state=expired para
   trazabilidad (BR-009).
 end note

 note right of revoked
   Admin revoke() emite
   AuditEvent type=high.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/seq-access`
 - :doc:`/arquitectura-tecnica/design-view/act-sod-check`
 - :doc:`/arquitectura-tecnica/design-view/act-rbac-effective-set-eval`
 - :doc:`/arquitectura-tecnica/design-view/class-access`
 - :doc:`/arquitectura-tecnica/use-case-view/access/index`
 - :doc:`/arquitectura-tecnica/domain-model/assignment`
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo`
