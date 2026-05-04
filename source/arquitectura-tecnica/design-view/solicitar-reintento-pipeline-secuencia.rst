.. meta::
 :artefacto: AT_UC_PIP_04_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_04_design_secuencia:

===================================
UC_PIP_04 — Design View (secuencia)
===================================

UC_PIP_04 — Solicitar Reintento de Pipeline: Design View
=================================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PIP_04 tecnicamente.

.. uml::
 :caption: UC_PIP_04 — Design View (secuencia)

 @startuml

 actor "request_pipeline_retry" as request_pipeline_retry
 participant "Interfaz de Pipeline" as Iface <<frontend>>
 participant "Servicio de Pipeline" as SvcNode <<api>>
 database "Almacen de datos (sp_etl_*)" as Store <<sql>>

 request_pipeline_retry -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> request_pipeline_retry : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml`
