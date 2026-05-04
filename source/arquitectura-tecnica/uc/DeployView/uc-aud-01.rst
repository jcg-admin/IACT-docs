.. meta::
 :artefacto: AT_UC_AUD_01_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_01_deploy:

==================================================================
UC_AUD_01 — Consultar Auditoria General: Deployment View
==================================================================

Distribucion fisica de nodos y artefactos para UC_AUD_01.

.. uml::
 :caption: UC_AUD_01 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB (audit_log)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/audit/uc-aud-01/requisitos-no-funcionales`
