.. meta::
 :artefacto: AT_UC_PIP_04_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_04_deploy:

======================================================================
UC_PIP_04 — Solicitar Reintento de Pipeline: Deployment View
======================================================================

Distribucion fisica de nodos y artefactos para UC_PIP_04.

.. uml::
 :caption: UC_PIP_04 — Deployment View

 @startuml

 node "DisparadorETL" as NodoFront
 node "MariaDB (etl_runs)" as NodoAPI
 database "MariaDB (sp_etl_*)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/requisitos-no-funcionales`
