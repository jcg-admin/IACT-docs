.. meta::
 :artefacto: AT_UC_LOG_05_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_05_deploy:

==================================================================
UC_LOG_05 — Ver Logs de Infraestructura: Deployment View
==================================================================

Distribucion fisica de nodos y artefactos para UC_LOG_05.

.. uml::
 :caption: UC_LOG_05 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB / Sistema" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-05/requisitos-no-funcionales`
