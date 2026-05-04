.. meta::
 :artefacto: AT_UC_AUTH_03_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_03_domain:

========================================================
UC_AUTH_03 — Recuperar Contrasena: Domain Model
========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/auth/uc-auth-03/index`.

.. uml::
 :caption: UC_AUTH_03 — Domain Model

 @startuml

 left to right direction

 class User
 class InternalMailbox
 class AuditEvent

 User --> InternalMailbox
 InternalMailbox --> AuditEvent

 @enduml


.. uml::
 :caption: UC_AUTH_03 — Recuperar Contrasena — Estado de Session

 @startuml
 hide empty description

 [*] --> Iniciada : usuario solicita login
 Iniciada --> Validando : enviar credenciales
 Validando --> Activa : autenticacion exitosa
 Activa --> Cerrada : logout / timeout
 Validando --> [*] : credenciales invalidas

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/auth/uc-auth-03/index`
