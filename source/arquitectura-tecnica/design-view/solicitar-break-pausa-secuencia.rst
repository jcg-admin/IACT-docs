.. meta::
 :artefacto: AT_UC_OPR_07_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_07_design_secuencia:

===================================
UC_OPR_07 — Design View (secuencia)
===================================

UC_OPR_07 — Solicitar Break Pausa: Design View
=======================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_07 tecnicamente.

.. uml::
 :caption: UC_OPR_07 — Design View (secuencia)

 @startuml

 actor "request_break" as request_break
 participant "Interfaz de Operador" as Iface <<frontend>>
 participant "Servicio de Operador" as SvcNode <<api>>
 database "Almacen de datos (tbl_historico_*)" as Store <<sql>>

 request_break -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> request_break : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-07/diagramas-uml`
