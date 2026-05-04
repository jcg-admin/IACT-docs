.. meta::
 :artefacto: AT_UC_ACC_04_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_04_design_secuencia:

===================================
UC_ACC_04 — Design View (secuencia)
===================================

UC_ACC_04 — Asignar Agrupador: Design View
===================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_04 tecnicamente.

.. uml::
 :caption: UC_ACC_04 — Design View (secuencia)

 @startuml

 actor "assign_function_groups" as assign_function_groups
 participant "Interfaz de Control" as Iface <<frontend>>
 participant "Servicio de Acceso" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 assign_function_groups -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> assign_function_groups : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-04/diagramas-uml`
