.. meta::
 :artefacto: AT_UC_PERM_06_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_06_deploy:

=================================================================
UC_PERM_06 — Asignar Funciones a Grupo: Deployment View
=================================================================

Distribucion fisica de nodos y artefactos para UC_PERM_06.

.. uml::
 :caption: UC_PERM_06 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-06/requisitos-no-funcionales`
