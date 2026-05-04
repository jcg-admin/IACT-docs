.. meta::
 :artefacto: AT_UC_ACC_09_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_09_design_secuencia:

===================================
UC_ACC_09 — Design View (secuencia)
===================================

UC_ACC_09 — Auditar Cambios de Acceso: Design View
===========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_09 tecnicamente.

.. uml::
 :caption: UC_ACC_09 — Design View (secuencia)

 @startuml

 actor "view_audit_log" as view_audit_log
 participant "Interfaz de Control" as Iface <<frontend>>
 participant "Servicio de Acceso" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 view_audit_log -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_audit_log : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/access/uc-acc-09/diagramas-uml`
