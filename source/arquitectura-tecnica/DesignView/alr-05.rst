.. meta::
 :artefacto: AT_UC_ALR_05_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_05_design:

=========================================================
UC_ALR_05 — Gestionar Suscripciones: Design View
=========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_ALR_05 tecnicamente.

.. uml::
 :caption: UC_ALR_05 — Design View (secuencia)

 @startuml

 actor "subscribe_to_alert" as subscribe_to_alert
 participant "Interfaz de Alertas" as Iface <<frontend>>
 participant "Servicio de Alertas" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 subscribe_to_alert -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> subscribe_to_alert : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_ALR_05 — Gestionar Suscripciones — Comunicacion entre Objetos

 @startuml

 object ":subscribe_to_alert" as Actor
 object ":Interfaz de Alertas" as Iface
 object ":Servicio de Alertas" as Svc
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

 :doc:`/requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml`
