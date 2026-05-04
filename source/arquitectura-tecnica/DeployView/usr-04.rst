.. meta::
 :artefacto: AT_UC_USR_04_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_04_deploy:

=======================================================
UC_USR_04 — Eliminar Usuario: Deployment View
=======================================================

Distribucion fisica de nodos y artefactos para UC_USR_04.

.. uml::
 :caption: UC_USR_04 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-04/requisitos-no-funcionales`
