.. meta::
 :artefacto: AT_UC_ACC_05_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_05_design:

======================================================
UC_ACC_05 — Gestionar Reglas SoD: Design View
======================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ACC_05 tecnicamente.

.. uml::
 :caption: UC_ACC_05 — Design View (secuencia)

 @startuml

 actor "view_separation_rules" as view_separation_rules
 participant "Interfaz de Control" as Iface <<frontend>>
 participant "Servicio de Acceso" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 view_separation_rules -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_separation_rules : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_ACC_05 — Gestionar Reglas SoD — Comunicacion entre Objetos

 @startuml

 object ":view_separation_rules" as Actor
 object ":Interfaz de Control" as Iface
 object ":Servicio de Acceso" as Svc
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

 :doc:`/requisitos/casos-uso/access/uc-acc-05/diagramas-uml`
