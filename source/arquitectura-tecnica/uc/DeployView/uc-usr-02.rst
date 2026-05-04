.. meta::
 :artefacto: AT_UC_USR_02_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_02_deploy:

=========================================================
UC_USR_02 — Consultar Usuarios: Deployment View
=========================================================

Distribucion fisica de nodos y artefactos para UC_USR_02.

.. uml::
 :caption: UC_USR_02 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-02/requisitos-no-funcionales`
