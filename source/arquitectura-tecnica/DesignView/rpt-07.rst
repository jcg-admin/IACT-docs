.. meta::
 :artefacto: AT_UC_RPT_07_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_07_design:

===================================================
UC_RPT_07 — Programar Reporte: Design View
===================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_RPT_07 tecnicamente.

.. uml::
 :caption: UC_RPT_07 — Design View (secuencia)

 @startuml

 actor "schedule_report" as schedule_report
 participant "Interfaz de Reportes" as Iface <<frontend>>
 participant "Servicio de Reportes" as SvcNode <<api>>
 database "MariaDB (base_ivr_*)" as Store <<sql>>

 schedule_report -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> schedule_report : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_RPT_07 — Programar Reporte — Comunicacion entre Objetos

 @startuml

 object ":schedule_report" as Actor
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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-07/diagramas-uml`
