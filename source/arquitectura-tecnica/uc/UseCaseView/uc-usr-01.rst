.. meta::
 :artefacto: AT_UC_USR_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_01_usecase:

====================================================
UC_USR_01 — Crear Usuario: Use Case View
====================================================

Actores RBAC, relaciones y confines del sistema para UC_USR_01.

.. uml::
 :caption: UC_USR_01 — Use Case View

 @startuml

 left to right direction

 actor "create_users"

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as UCUSR01
 }

 "create_users" --> UCUSR01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/users/uc-usr-01/actores-precondiciones`
