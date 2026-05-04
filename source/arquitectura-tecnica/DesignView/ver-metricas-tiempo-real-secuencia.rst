.. meta::
 :artefacto: AT_UC_RPT_02_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_02_design_secuencia:

===================================
UC_RPT_02 — Design View (secuencia)
===================================

UC_RPT_02 — Ver Metricas en Tiempo Real: Design View
=============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_RPT_02 tecnicamente.

.. uml::
 :caption: UC_RPT_02 — Design View (secuencia)

 @startuml

 actor "view_kpis" as view_kpis
 participant "Interfaz de Reportes" as Iface <<frontend>>
 participant "Servicio de Reportes" as SvcNode <<api>>
 database "MariaDB (base_ivr_*)" as Store <<sql>>

 view_kpis -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_kpis : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-02/diagramas-uml`
