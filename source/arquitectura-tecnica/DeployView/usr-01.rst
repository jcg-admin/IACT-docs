.. meta::
 :artefacto: AT_UC_USR_01_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_01_deploy:

====================================================
UC_USR_01 — Crear Usuario: Deployment View
====================================================

Distribucion fisica de nodos y artefactos para UC_USR_01.

.. uml::
 :caption: UC_USR_01 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-01/requisitos-no-funcionales`
