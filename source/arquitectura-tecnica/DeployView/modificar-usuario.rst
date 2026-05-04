.. meta::
 :artefacto: AT_UC_USR_03_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_03_deploy:

========================================================
UC_USR_03 — Modificar Usuario: Deployment View
========================================================

Distribucion fisica de nodos y artefactos para UC_USR_03.

.. uml::
 :caption: UC_USR_03 — Modificar Usuario — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Apache + mod_wsgi" as WebServer {
   artifact "Django App" as App
 }
 database "MariaDB" as MariaDB

 Client --> WebServer : HTTPS
 WebServer --> MariaDB : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-03/requisitos-no-funcionales`
