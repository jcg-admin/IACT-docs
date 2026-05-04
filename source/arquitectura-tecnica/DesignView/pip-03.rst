.. meta::
 :artefacto: AT_UC_PIP_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_03_design:

===================================================================
UC_PIP_03 — Consultar Disponibilidad de Datos: Design View
===================================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PIP_03 tecnicamente.

.. uml::
 :caption: UC_PIP_03 — Design View (secuencia)

 @startuml

 actor "view_data_availability" as view_data_availability
 participant "Interfaz de Pipeline" as Iface <<frontend>>
 participant "Servicio de Pipeline" as SvcNode <<api>>
 database "MariaDB (sp_etl_*)" as Store <<sql>>

 view_data_availability -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_data_availability : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_PIP_03 — Consultar Disponibilidad de Datos — Comunicacion entre Objetos

 @startuml

 object ":view_data_availability" as Actor
 object ":Interfaz de Pipeline" as Iface
 object ":Servicio de Pipeline" as Svc
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

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml`
