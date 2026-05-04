.. meta::
 :artefacto: AT_UC_RPT_09_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_09_design_secuencia:

===================================
UC_RPT_09 — Design View (secuencia)
===================================

UC_RPT_09 — Configurar Filtros: Design View
====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_RPT_09 tecnicamente.

.. uml::
 :caption: UC_RPT_09 — Design View (secuencia)

 @startuml

 actor "filter_reports" as filter_reports
 participant "Interfaz de Reportes" as Iface <<frontend>>
 participant "Servicio de Reportes" as SvcNode <<api>>
 database "Almacen de datos (base_ivr_*)" as Store <<sql>>

 filter_reports -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> filter_reports : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-09/diagramas-uml`
