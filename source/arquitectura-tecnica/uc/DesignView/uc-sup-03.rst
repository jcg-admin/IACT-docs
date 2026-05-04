.. meta::
 :artefacto: AT_UC_SUP_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_03_design:

=============================================================
UC_SUP_03 — Mensaje Broadcast al Equipo: Design View
=============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_SUP_03 tecnicamente.

.. uml::
 :caption: UC_SUP_03 — Design View (secuencia)

 @startuml

 actor "broadcast_team_messages" as broadcast_team_messages
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 broadcast_team_messages -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> broadcast_team_messages : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/diagramas-uml`
