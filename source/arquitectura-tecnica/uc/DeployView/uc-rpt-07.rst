.. meta::
 :artefacto: AT_UC_RPT_07_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_07_deploy:

========================================================
UC_RPT_07 — Programar Reporte: Deployment View
========================================================

Distribucion fisica de nodos y artefactos para UC_RPT_07.

.. uml::
 :caption: UC_RPT_07 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB (base_ivr_*)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-07/requisitos-no-funcionales`
