.. meta::
 :artefacto: AT_DM_CLASS_EXPIRATION_POLICY
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _dm_class_expiration_policy:

================
ExpirationPolicy
================

Politica de expiracion automatica para entidades con TTL: ``ExceptionalPermission``,
sesiones JWT, exports de auditoria, callbacks programados, etc. Centraliza la
logica de validacion de bounds (1h-30d), calculo de ``expires_at``, y deteccion
de proximidad de vencimiento para notificaciones.

Consumida por workers cron que purgan o recalculan estados expirados, y por
servicios que crean entidades temporales para validar el ``expires_at`` solicitado.

.. uml::
 :caption: Clase ExpirationPolicy — bounds + deteccion de vencimiento.

 @startuml

 class ExpirationPolicy {
   - min_ttl : Duration
   - max_ttl : Duration
   - notify_before : Duration
   --
   + validate_bounds(expires_at : DateTime) : Boolean
   + calculate_expiry(now : DateTime, ttl : Duration) : DateTime
   + is_expired(entity : Expirable) : Boolean
   + is_near_expiry(entity : Expirable, threshold : Duration) : Boolean
   + find_expiring_in(window : Duration) : List<Expirable>
 }

 interface Expirable {
   + expires_at : DateTime
 }

 ExpirationPolicy ..> Expirable : evalua

 note bottom of ExpirationPolicy
   BR-008: bounds 1h-30d para
   ExceptionalPermission.
   notify_before default 24h
   antes de expirar.
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que aplican ExpirationPolicy:

- :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
  permiso temporal: validate_bounds(expires_at) antes de persist.
- :doc:`/requisitos/casos-uso/access/uc-acc-09/index` —
  vencimiento de agrupador: cron consume find_expiring_in.

Relaciones
==========

- :doc:`exceptional-permission` — entidad principal con expiracion.
- :doc:`exceptional-permission-repo` — find_expiring_in se delega aqui.
- :doc:`session` — tokens JWT con ``exp`` validado contra esta policy.
- :doc:`audit-service` — emite ``EXPIRED_REMOVED`` cuando cron purga.
