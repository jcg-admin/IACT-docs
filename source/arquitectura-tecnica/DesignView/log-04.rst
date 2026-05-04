.. meta::
 :artefacto: AT_UC_LOG_04_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_04_design:

===============================================
UC_LOG_04 — Exportar Logs: Design View
===============================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_LOG_04 tecnicamente.

.. uml::
 :caption: UC_LOG_04 — Design View (secuencia)

 @startuml

 actor "export_logs" as export_logs
 participant "Interfaz de Logs" as Iface <<frontend>>
 participant "Servicio de Logs" as SvcNode <<api>>
 database "MariaDB / Sistema" as Store <<sql>>

 export_logs -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> export_logs : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_LOG_04 — Exportar Logs — Comunicacion entre Objetos

 @startuml

 object ":export_logs" as Actor
 object ":Interfaz de Logs" as Iface
 object ":Servicio de Logs" as Svc
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

 :doc:`/requisitos/casos-uso/logs/uc-log-04/diagramas-uml`
