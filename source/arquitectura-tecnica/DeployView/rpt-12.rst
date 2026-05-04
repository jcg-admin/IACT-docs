.. meta::
 :artefacto: AT_UC_RPT_12_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_12_deploy:

=========================================================
UC_RPT_12 — Reporte de Agentes: Deployment View
=========================================================

Distribucion fisica de nodos y artefactos para UC_RPT_12.

.. uml::
 :caption: UC_RPT_12 — Reporte de Agentes — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Apache + mod_wsgi" as WebServer {
   artifact "Django App" as App
 }
 database "MariaDB" as DB

 Client --> WebServer : HTTPS
 WebServer --> DB : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-12/requisitos-no-funcionales`
