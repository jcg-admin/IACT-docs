.. meta::
 :artefacto: AT_UC_ACC_03_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_03_design_secuencia:

===================================
UC_ACC_03 — Design View (secuencia)
===================================

UC_ACC_03 — Consultar Permisos Efectivos: Design View
==============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_03 tecnicamente.

.. uml::
 :caption: UC_ACC_03 — Design View (secuencia)

 @startuml

 actor "view_assignments" as view_assignments
 participant "Interfaz de Control" as Iface <<frontend>>
 participant "Servicio de Acceso" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 view_assignments -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_assignments : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-03/diagramas-uml`
