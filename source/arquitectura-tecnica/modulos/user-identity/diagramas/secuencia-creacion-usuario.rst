.. meta::
 :artefacto: ARQ_MOD_002_DIAG_SECUENCIA_CREACION
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/user-identity/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_002_secuencia_creacion_usuario:

================================
Secuencia de Creacion de Usuario
================================

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
   Userendpoint -> auth_user : registrar auth_user (is_active=True)
   auth_user --> Userendpoint : user_id
   Userendpoint -> Internalmailbox : registrar bienvenida + password temporal
   Userendpoint -> Auditlog : registrar USER_CREATED
   Userendpoint --> ADMIN : 201 Created + user_id
 end

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/user-identity/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
