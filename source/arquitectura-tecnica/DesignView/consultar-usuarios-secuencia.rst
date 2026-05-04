.. meta::
 :artefacto: AT_UC_USR_02_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_02_design_secuencia:

===================================
UC_USR_02 — Design View (secuencia)
===================================

UC_USR_02 — Consultar Usuarios: Design View
====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_USR_02 tecnicamente.

.. uml::
 :caption: UC_USR_02 — Design View (secuencia)

 @startuml

 actor "list_users" as list_users
 participant "Interfaz de Usuarios" as Iface <<frontend>>
 participant "Servicio de Usuarios" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 list_users -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> list_users : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-02/diagramas-uml`
