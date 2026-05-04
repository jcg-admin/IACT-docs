.. meta::
 :artefacto: AT_UC_SUP_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_02_design:

=====================================================
UC_SUP_02 — Barge-in en Llamada: Design View
=====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_SUP_02 tecnicamente.

.. uml::
 :caption: UC_SUP_02 — Design View (secuencia)

 @startuml

 actor "barge_in_calls" as barge_in_calls
 participant "Interfaz de Supervision" as Iface <<frontend>>
 participant "Servicio de Supervision" as SvcNode <<api>>
 database "MariaDB (tbl_historico_*)" as Store <<sql>>

 barge_in_calls -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> barge_in_calls : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_SUP_02 — Barge-in en Llamada — Comunicacion entre Objetos

 @startuml

 object ":barge_in_calls" as Actor
 object ":Interfaz de Supervision" as Iface
 object ":Servicio de Supervision" as Svc
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

 :doc:`/requisitos/casos-uso/supervision/uc-sup-02/diagramas-uml`
