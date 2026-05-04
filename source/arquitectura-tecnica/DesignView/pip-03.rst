.. meta::
 :artefacto: AT_UC_PIP_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_03_design:

===================================================================
UC_PIP_03 — Consultar Disponibilidad de Datos: Design View
===================================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PIP_03 tecnicamente.

.. uml::
 :caption: UC_PIP_03 — Design View (secuencia)

 @startuml

 actor "view_data_availability" as view_data_availability
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (sp_etl_*)" as BaseDatos <<sql>>

 view_data_availability -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_data_availability : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml`
