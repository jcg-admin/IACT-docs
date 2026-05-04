.. meta::
 :artefacto: AT_UC_OPR_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_02_design:

==========================================================
UC_OPR_02 — Atender Llamada Entrante: Design View
==========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_02 tecnicamente.

.. uml::
 :caption: UC_OPR_02 — Design View (secuencia)

 @startuml

 actor "answer_inbound_calls" as answer_inbound_calls
 participant "Interfaz de Operador" as Iface <<frontend>>
 participant "Servicio de Operador" as SvcNode <<api>>
 database "MariaDB (tbl_historico_*)" as Store <<sql>>

 answer_inbound_calls -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> answer_inbound_calls : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_OPR_02 — Atender Llamada Entrante — Comunicacion entre Objetos

 @startuml

 object ":answer_inbound_calls" as Actor
 object ":Interfaz de Operador" as Iface
 object ":Servicio de Operador" as Svc
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

 :doc:`/requisitos/casos-uso/operator/uc-opr-02/diagramas-uml`
