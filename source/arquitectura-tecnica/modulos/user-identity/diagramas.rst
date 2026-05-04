.. _arq-mod-002-diagramas:

================================================
ARQ_MOD_002 — Diagramas de Comportamiento
================================================


Ciclo de Vida del Usuario
=========================

.. uml::
 :caption: Ciclo de vida del usuario — estados y transiciones (BR-009 soft delete).

 @startuml

 [*] --> PENDIENTE_CONFIGURACION : alta en el sistema\n(create_users)

 PENDIENTE_CONFIGURACION --> ACTIVO : completa preguntas\nde seguridad

 ACTIVO --> INACTIVO : deactivate_users\n(soft delete, BR-009)
 ACTIVO --> BLOQUEADO : intentos fallidos exceden\numbral (ARQ_MOD_003)

 INACTIVO --> ACTIVO : update_users reactiva
 BLOQUEADO --> ACTIVO : update_users desbloquea

 note right of BLOQUEADO
   Solo RBAC (update_users)
   puede desbloquear — no el
   propio usuario.
 end note

 @enduml

----

Secuencia de Creacion de Usuario
===================================

.. uml::
 :caption: Secuencia create_users — alta de nuevo usuario con username y password temporal.

 @startuml

 actor "create_users" as ADMIN
 participant "UserEndpoint\n(/api/users/)" as Userendpoint
 database "auth_user\n(PostgreSQL)" as auth_user
 participant "InternalMailbox" as Internalmailbox
 participant "AuditLog" as Auditlog

 ADMIN -> Userendpoint : POST /api/users/ {email, first_name, last_name}
 Userendpoint -> Userendpoint : JWT + RBAC (create_users)
 alt sin permiso
   Userendpoint --> ADMIN : 403 Forbidden
 else con permiso
   Userendpoint -> Userendpoint : generar username (CNST-029)
   Userendpoint -> Userendpoint : generar password temporal
   Userendpoint -> auth_user : INSERT auth_user (is_active=True)
   auth_user --> Userendpoint : user_id
   Userendpoint -> Internalmailbox : INSERT bienvenida + password temporal
   Userendpoint -> Auditlog : INSERT USER_CREATED
   Userendpoint --> ADMIN : 201 Created + user_id
 end

 @enduml

----

Diagrama de clases — modulo identidad
=======================================

.. uml::
 :caption: Clases de identidad de usuario con atributos clave.

 @startuml

 class User {
   +id: int
   +username: str
   +email: str
   +is_active: bool
   +date_joined: datetime
   +last_login: datetime
   +create(): User
   +deactivate(): void
 }

 class Session {
   +user: User
   +jwt_token: str
   +ip_origen: str
   +created_at: datetime
   +expires_at: datetime
   +invalidate(): void
 }

 class AuditEvent {
   +user_id: int
   +accion: str
   +entidad: str
   +timestamp: datetime
   +ip_origen: str
 }

 User "1" *-- "0..*" Session
 User "1" --> "0..*" AuditEvent : genera

 @enduml
