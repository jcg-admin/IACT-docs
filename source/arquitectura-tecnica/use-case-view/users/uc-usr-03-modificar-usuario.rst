.. meta::
 :artefacto: AT_UC_USR_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: users
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_usr_03_modificar_usuario:

==============================
UC_USR_03 — Modificar Usuario
==============================

Actualiza metadata de un User existente (display_name, segmento, etc.).
``username`` y ``email`` son inmutables tras creacion (P-44 analogo).
Cambio de segmento dispara invalidacion de cache de permisos del User
(efectos en CNST-008 isolation).

.. uml::
 :caption: UC_USR_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "modify_users" as modify_users
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_03\nModificar Usuario" as UC_USR_03
   usecase "Verificar\nmodify_users" as VERIFICAR_AGR
   usecase "Validar campos\nmodificables" as VALIDAR
   usecase "Validar User existe\n+ state ACTIVE" as VALIDAR_STATE
   usecase "Persistir cambios" as PERSISTIR
   usecase "Invalidar cache\nsi cambia segmento" as INVALIDAR
   usecase "Emitir AuditEvent\nUSER_UPDATED" as AUDITAR
 }

 modify_users --> UC_USR_03

 UC_USR_03 ..> VERIFICAR_AGR : <<include>>
 UC_USR_03 ..> VALIDAR : <<include>>
 UC_USR_03 ..> VALIDAR_STATE : <<include>>
 UC_USR_03 ..> PERSISTIR : <<include>>
 UC_USR_03 ..> INVALIDAR : <<include>>
 UC_USR_03 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_STATE --> UserRepo
 PERSISTIR --> UserRepo
 INVALIDAR --> PermissionCache
 AUDITAR --> AuditService
 PERSISTIR --> User_destino
 AuditService --> view_audit_log

 note bottom of VALIDAR
   username + email inmutables.
   Modificable: display_name,
   segmento, metadata custom.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user` —
   entity actualizada.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   invalidada por cambio de segmento.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica modify_users.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor USER_UPDATED.
 - :doc:`/requisitos/casos-uso/users/uc-usr-03/index` —
   spec textual.
