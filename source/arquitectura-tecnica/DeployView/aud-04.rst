.. meta::
 :artefacto: AT_UC_AUD_04_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_04_deploy:

====================================================================
UC_AUD_04 — Generar Reporte de Compliance: Deployment View
====================================================================

Distribucion fisica de nodos y artefactos para UC_AUD_04.

.. uml::
 :caption: UC_AUD_04 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB (audit_log)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/audit/uc-aud-04/requisitos-no-funcionales`
