.. meta::
 :artefacto: AT_UC_RPT_13_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_13_design:

==================================================
UC_RPT_13 — Reporte de Colas: Design View
==================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_RPT_13 tecnicamente.

.. uml::
 :caption: UC_RPT_13 — Design View (secuencia)

 @startuml

 actor "view_reports" as view_reports
 participant "Interfaz de Reportes" as Iface <<frontend>>
 participant "Servicio de Reportes" as SvcNode <<api>>
 database "MariaDB (base_ivr_*)" as Store <<sql>>

 view_reports -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_reports : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_RPT_13 — Reporte de Colas — Comunicacion entre Objetos

 @startuml

 object ":view_reports" as Actor
 object ":Interfaz de Reportes" as Iface
 object ":Servicio de Reportes" as Svc
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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml`
