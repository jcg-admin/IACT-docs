.. meta::
 :artefacto: AT_UC_OPR_04_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_04_design_secuencia:

===================================
UC_OPR_04 — Design View (secuencia)
===================================

UC_OPR_04 — Hold Unhold Llamada: Design View
=====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_04 tecnicamente.

.. uml::
 :caption: UC_OPR_04 — Design View (secuencia)

 @startuml

 actor "hold_calls" as hold_calls
 participant "Interfaz de Operador" as Iface <<frontend>>
 participant "Servicio de Operador" as SvcNode <<api>>
 database "MariaDB (tbl_historico_*)" as Store <<sql>>

 hold_calls -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> hold_calls : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-04/diagramas-uml`
