.. meta::
 :artefacto: AT_UC_LOG_03_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_03_deploy:

==================================================
UC_LOG_03 — Buscar Logs: Deployment View
==================================================

Distribucion fisica de nodos y artefactos para UC_LOG_03.

.. uml::
 :caption: UC_LOG_03 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB / Sistema" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-03/requisitos-no-funcionales`
