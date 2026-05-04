.. meta::
 :artefacto: AT_UC_PERM_09_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_09_design:

=================================================
UC_PERM_09 — Auditar Acceso: Design View
=================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PERM_09 tecnicamente.

.. uml::
 :caption: UC_PERM_09 — Design View (secuencia)

 @startuml

 actor "view_audit_log" as view_audit_log
 participant "Interfaz de Permisos" as Iface <<frontend>>
 participant "Servicio de Permisos" as SvcNode <<api>>
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


.. uml::
 :caption: UC_PERM_09 — Auditar Acceso — Comunicacion entre Objetos

 @startuml

 object ":view_audit_log" as Actor
 object ":Interfaz de Permisos" as Iface
 object ":Servicio de Permisos" as Svc
 object ":Repositorio" as Repo
 object ":Almacen de Datos" as Store

 Actor -> Iface : 1: solicitar accion
 Iface -> Svc : 2: invocar endpoint
 Svc -> Svc : 3: validar RBAC
 Svc -> Repo : 4: ejecutar operacion
 Repo -> Store : 5: query / SP
 Store --> Repo : 6: resultado
 Repo --> Svc : 7: entidad
 Svc --> Iface : 8: respuesta
 Iface --> Actor : 9: renderizar

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-09/diagramas-uml`
