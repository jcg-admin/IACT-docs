.. meta::
 :artefacto: AT_UC_USR_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_03_usecase:

========================================================
UC_USR_03 — Modificar Usuario: Use Case View
========================================================

Actores RBAC, relaciones y confines del sistema para UC_USR_03.

.. uml::
 :caption: UC_USR_03 — Use Case View

 @startuml

 left to right direction

 actor "update_users"

 rectangle "MOD_Users" {
   usecase "UC_USR_03\nModificar Usuario" as UCUSR03
 }

 "update_users" --> UCUSR03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/users/uc-usr-03/actores-precondiciones`
