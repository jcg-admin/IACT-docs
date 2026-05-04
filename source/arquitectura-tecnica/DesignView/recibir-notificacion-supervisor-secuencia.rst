.. meta::
 :artefacto: AT_UC_OPR_10_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_10_design_secuencia:

===================================
UC_OPR_10 — Design View (secuencia)
===================================

UC_OPR_10 — Recibir Notificacion Supervisor: Design View
=================================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_10 tecnicamente.

.. uml::
 :caption: UC_OPR_10 — Design View (secuencia)

 @startuml

 actor "read_own_mailbox" as read_own_mailbox
 participant "Interfaz de Operador" as Iface <<frontend>>
 participant "Servicio de Operador" as SvcNode <<api>>
 database "MariaDB (tbl_historico_*)" as Store <<sql>>

 read_own_mailbox -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> read_own_mailbox : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-10/diagramas-uml`
