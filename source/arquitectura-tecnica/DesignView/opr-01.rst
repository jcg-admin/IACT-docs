.. meta::
 :artefacto: AT_UC_OPR_01_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_01_design:

===========================================================
UC_OPR_01 — Cambiar Estado del Agente: Design View
===========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_01 tecnicamente.

.. uml::
 :caption: UC_OPR_01 — Design View (secuencia)

 @startuml

 actor "manage_own_agent_state" as manage_own_agent_state
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (tbl_historico_*)" as BaseDatos <<sql>>

 manage_own_agent_state -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> manage_own_agent_state : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-01/diagramas-uml`
