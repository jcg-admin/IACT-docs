.. meta::
 :artefacto: AT_UC_PERM_02_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_02_deploy:

===============================================================
UC_PERM_02 — Revocar Grupo a Usuario: Deployment View
===============================================================

Distribucion fisica de nodos y artefactos para UC_PERM_02.

.. uml::
 :caption: UC_PERM_02 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-02/requisitos-no-funcionales`
