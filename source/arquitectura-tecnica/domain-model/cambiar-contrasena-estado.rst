.. meta::
 :artefacto: AT_UC_AUTH_04_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_04_domain_estado:

===================================================
UC_AUTH_04 — Cambiar Contrasena — Estado de Session
===================================================

.. uml::
 :caption: UC_AUTH_04 — Cambiar Contrasena — Estado de Session

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
 :doc:`/requisitos/casos-uso/auth/uc-auth-04/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/auth/uc-auth-04/index`
