.. meta::
 :artefacto: AT_UC_RPT_08_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_08_deploy:

===============================================================
UC_RPT_08 — Ver Reportes Programados: Deployment View
===============================================================

Distribucion fisica de nodos y artefactos para UC_RPT_08.

.. uml::
 :caption: UC_RPT_08 — Ver Reportes Programados — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Apache + mod_wsgi" as WebServer {
   artifact "Django App" as App
 }
 database "Almacen de datos" as Almacen de Datos

 Client --> WebServer : HTTPS
 WebServer --> Almacen de Datos : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-08/requisitos-no-funcionales`
