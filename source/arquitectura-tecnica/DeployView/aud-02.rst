.. meta::
 :artefacto: AT_UC_AUD_02_DEPLOY
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_02_deploy:

=======================================================
UC_AUD_02 — Buscar Auditoria: Deployment View
=======================================================

Distribucion fisica de nodos y artefactos para UC_AUD_02.

.. uml::
 :caption: UC_AUD_02 — Deployment View

 @startuml

 node "React Frontend" as NodoFront
 node "Django API" as NodoAPI
 database "MariaDB (audit_log)" as NodoBD

 NodoFront --> NodoAPI : HTTPS / REST
 NodoAPI --> NodoBD : TCP / SQL

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/audit/uc-aud-02/requisitos-no-funcionales`
