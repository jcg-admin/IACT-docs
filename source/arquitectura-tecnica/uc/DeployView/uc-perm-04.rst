.. meta::
 :artefacto: AT_UC_PERM_04_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_04_deploy:

===================================================================
UC_PERM_04 — Revocar Permiso Excepcional: Deployment View
===================================================================

Distribucion fisica de nodos y artefactos para UC_PERM_04.

.. uml::
 :caption: UC_PERM_04 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-04/requisitos-no-funcionales`
