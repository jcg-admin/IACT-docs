.. meta::
 :artefacto: AT_UC_SUP_01_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_01_design_secuencia:

===================================
UC_SUP_01 — Design View (secuencia)
===================================

UC_SUP_01 — Monitorear Llamada: Design View
====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_SUP_01 tecnicamente.

.. uml::
 :caption: UC_SUP_01 — Design View (secuencia)

 @startuml

 actor "monitor_live_calls" as monitor_live_calls
 participant "Interfaz de Supervision" as Iface <<frontend>>
 participant "Servicio de Supervision" as SvcNode <<api>>
 database "MariaDB (tbl_historico_*)" as Store <<sql>>

 monitor_live_calls -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> monitor_live_calls : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/diagramas-uml`
