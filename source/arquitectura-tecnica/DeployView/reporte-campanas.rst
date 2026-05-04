.. meta::
 :artefacto: AT_UC_RPT_14_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_14_deploy:

==========================================================
UC_RPT_14 — Reporte de Campanas: Deployment View
==========================================================

Distribucion fisica de nodos y artefactos para UC_RPT_14.

.. uml::
 :caption: UC_RPT_14 — Reporte de Campanas — Deployment View

 @startuml

 node "Cliente Web" as Client
 node "Servidor Web" as WebServer {
   artifact "Aplicacion Backend" as App
 }
 database "Almacen de datos" as Almacen de Datos

 Client --> WebServer : HTTPS
 WebServer --> Almacen de Datos : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-14/requisitos-no-funcionales`
