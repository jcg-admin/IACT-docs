.. meta::
 :artefacto: AT_UC_USR_01_USECASE
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

.. _at_uc_usr_01_crear_usuario:

==============================
UC_USR_01 — Crear Usuario
==============================

Crea un nuevo ``User`` en el sistema con datos basicos (username,
email, segmento). El sistema genera password inicial via
``PasswordGenerator``, lo entrega via ``InternalMessage`` (CNST-002
mailbox-or-abort) y descarta el plain text. Auditoria completa.

.. uml::
 :caption: UC_USR_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "create_users" as create_users
 actor "User destino" as User_destino <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "PasswordGenerator" as PasswordGenerator <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as UC_USR_01
   usecase "Verificar\ncreate_users" as VERIFICAR_AGR
   usecase "Validar payload\n(username, email, segmento)" as VALIDAR
   usecase "Validar unicidad\n(username, email)" as VALIDAR_UNIQUE
   usecase "Generar password\ninicial seguro" as GENERAR_PWD
   usecase "Persistir User\n(state=ACTIVE)" as PERSISTIR
   usecase "Enviar password\nvia InternalMessage" as ENVIAR_PWD
   usecase "Sanitizar logs\n(no plain pwd)" as SANITIZAR
   usecase "Emitir AuditEvent\nUSER_CREATED" as AUDITAR
 }

 create_users --> UC_USR_01

 UC_USR_01 ..> VERIFICAR_AGR : <<include>>
 UC_USR_01 ..> VALIDAR : <<include>>
 UC_USR_01 ..> VALIDAR_UNIQUE : <<include>>
 UC_USR_01 ..> GENERAR_PWD : <<include>>
 UC_USR_01 ..> PERSISTIR : <<include>>
 UC_USR_01 ..> ENVIAR_PWD : <<include>>
 UC_USR_01 ..> SANITIZAR : <<include>>
 UC_USR_01 ..> AUDITAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_UNIQUE --> UserRepo
 GENERAR_PWD --> PasswordGenerator
 PERSISTIR --> UserRepo
 ENVIAR_PWD --> InternalMailbox
 InternalMailbox --> User_destino
 SANITIZAR --> Sanitizer
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of GENERAR_PWD
   PasswordGenerator entrega plain
   text UNA sola vez via mailbox
   y descarta. UserRepo persiste solo
   password_hash (CNST-026).
 end note

 note bottom of ENVIAR_PWD
   CNST-001 NO email externo.
   CNST-002 mailbox interno
   obligatorio.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user` —
   entity persistida.
 - :doc:`/arquitectura-tecnica/domain-model/user-repo` —
   repositorio.
 - :doc:`/arquitectura-tecnica/domain-model/password-generator` —
   generador seguro.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   buzon del nuevo User.
 - :doc:`/arquitectura-tecnica/domain-model/internal-message` —
   item con password inicial.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   evita plain pwd en logs.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica create_users.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor USER_CREATED.
 - :doc:`/requisitos/casos-uso/users/uc-usr-01/index` —
   spec textual.
