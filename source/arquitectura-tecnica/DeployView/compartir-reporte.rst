.. meta::
 :artefacto: AT_UC_RPT_11_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_11_deploy:

========================================================
UC_RPT_11 — Compartir Reporte: Deployment View
========================================================

Distribucion fisica de nodos y artefactos para UC_RPT_11.

.. uml::
 :caption: UC_RPT_11 — Compartir Reporte — Deployment View

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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-11/requisitos-no-funcionales`
