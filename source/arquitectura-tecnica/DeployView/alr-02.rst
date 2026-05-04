.. meta::
 :artefacto: AT_UC_ALR_02_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_02_deploy:

==========================================================
UC_ALR_02 — Ver Alertas Activas: Deployment View
==========================================================

Distribucion fisica de nodos y artefactos para UC_ALR_02.

.. uml::
 :caption: UC_ALR_02 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-02/requisitos-no-funcionales`
