.. meta::
 :artefacto: AT_UC_ALR_05_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_05_deploy:

==============================================================
UC_ALR_05 — Gestionar Suscripciones: Deployment View
==============================================================

Distribucion fisica de nodos y artefactos para UC_ALR_05.

.. uml::
 :caption: UC_ALR_05 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-05/requisitos-no-funcionales`
