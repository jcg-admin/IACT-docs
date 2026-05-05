.. meta::
 :artefacto: AT_DM_CLASS_IDEMPOTENCY_POLICY
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: CrossCutting
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _dm_class_idempotency_policy:

=================
IdempotencyPolicy
=================

Politica de idempotencia para POSTs sensibles que evita duplicar
operaciones por reintentos del cliente o problemas de red. Usa un
``request_id`` proporcionado por el cliente + ventana de deduplicacion
configurable; si llega un segundo request con el mismo ``request_id``
dentro de la ventana, devuelve el resultado cacheado del primero
sin re-ejecutar.

Aplica a operaciones de assignment, grant, revoke, schedule y otros
write paths donde la duplicacion accidental tiene impacto (audit
duplicado, doble email/notificacion, balance contable mal).

.. uml::
 :caption: Clase IdempotencyPolicy — dedup por request_id + ventana.

 @startuml

 class IdempotencyPolicy {
   - storage : CacheBackend
   - default_window : Duration
   --
   + register(request_id : String, response : Response, window : Duration) : void
   + lookup(request_id : String) : Response
   + is_replay(request_id : String) : Boolean
   + purge_expired() : Integer
 }

 class IdempotencyKey {
   + request_id : String
   + endpoint : String
   + actor_id : UUID
   + expires_at : DateTime
 }

 IdempotencyPolicy --> IdempotencyKey : usa

 note bottom of IdempotencyPolicy
   request_id obligatorio en headers
   o body de POST sensitivos.
   Ventana default 24h. Replay devuelve
   200 con response original (no error).
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que aplican IdempotencyPolicy:

- :doc:`/requisitos/casos-uso/access/uc-acc-01/index` —
  asignar funciones: filter idempotente (no re-asignar funciones
  ya asignadas).
- :doc:`/requisitos/casos-uso/permissions/uc-perm-03/index` —
  conceder permiso excepcional: dedup de grants en ventana.
- :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
  permiso temporal: register al persistir.

Relaciones
==========

- :doc:`assignment-repo` — la idempotencia se aplica antes de create.
- :doc:`exceptional-permission-repo` — idem para grant.
- :doc:`audit-service` — emite ``IDEMPOTENT_REPLAY`` cuando hay match.
