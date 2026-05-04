.. meta::
 :artefacto: AT_UC_RPT_09_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_09_deploy:

=========================================================
UC_RPT_09 — Configurar Filtros: Deployment View
=========================================================

Distribucion fisica de nodos y artefactos para UC_RPT_09.

.. uml::
 :caption: UC_RPT_09 — Configurar Filtros — Deployment View

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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-09/requisitos-no-funcionales`
