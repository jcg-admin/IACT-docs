.. meta::
 :artefacto: AT_UC_PIP_01_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_01_design:

================================================
UC_PIP_01 — Supervisar ETL: Design View
================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PIP_01 tecnicamente.

.. uml::
 :caption: UC_PIP_01 — Design View (secuencia)

 @startuml

 actor "view_pipeline_status" as view_pipeline_status
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (sp_etl_*)" as BaseDatos <<sql>>

 view_pipeline_status -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_pipeline_status : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml`
