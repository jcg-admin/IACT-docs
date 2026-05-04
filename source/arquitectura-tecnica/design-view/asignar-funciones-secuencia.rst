.. meta::
 :artefacto: AT_UC_ACC_01_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_01_design_secuencia:

===================================
UC_ACC_01 — Design View (secuencia)
===================================

UC_ACC_01 — Asignar Funciones: Design View
===================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_01 tecnicamente.

.. uml::
 :caption: UC_ACC_01 — Design View (secuencia)

 @startuml

 actor "assign_functions" as assign_functions
 participant "Interfaz de Control" as Iface <<frontend>>
 participant "Servicio de Acceso" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 assign_functions -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> assign_functions : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-01/diagramas-uml`
