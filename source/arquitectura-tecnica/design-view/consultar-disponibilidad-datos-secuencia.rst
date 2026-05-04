.. meta::
 :artefacto: AT_UC_PIP_03_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_03_design_secuencia:

===================================
UC_PIP_03 — Design View (secuencia)
===================================

UC_PIP_03 — Consultar Disponibilidad de Datos: Design View
===================================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PIP_03 tecnicamente.

.. uml::
 :caption: UC_PIP_03 — Design View (secuencia)

 @startuml

 actor "view_data_availability" as view_data_availability
 participant "Interfaz de Pipeline" as Iface <<frontend>>
 participant "Servicio de Pipeline" as SvcNode <<api>>
 database "Almacen de datos (sp_etl_*)" as Store <<sql>>

 view_data_availability -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_data_availability : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml`
