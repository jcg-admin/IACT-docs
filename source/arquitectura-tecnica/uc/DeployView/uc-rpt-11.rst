.. meta::
 :artefacto: AT_UC_RPT_11_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
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
 :caption: UC_RPT_11 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB (base_ivr_*)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-11/requisitos-no-funcionales`
