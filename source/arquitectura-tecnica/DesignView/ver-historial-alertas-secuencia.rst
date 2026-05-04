.. meta::
 :artefacto: AT_UC_ALR_04_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_04_design_secuencia:

===================================
UC_ALR_04 — Design View (secuencia)
===================================

UC_ALR_04 — Ver Historial de Alertas: Design View
==========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ALR_04 tecnicamente.

.. uml::
 :caption: UC_ALR_04 — Design View (secuencia)

 @startuml

 actor "view_alert_history" as view_alert_history
 participant "Interfaz de Alertas" as Iface <<frontend>>
 participant "Servicio de Alertas" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 view_alert_history -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_alert_history : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml`
