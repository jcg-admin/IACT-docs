.. meta::
 :artefacto: AT_UC_CLI_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_03_design:

=================================================
UC_CLI_03 — Esperar en Cola: Design View
=================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_CLI_03 tecnicamente.

.. uml::
 :caption: UC_CLI_03 — Design View (secuencia)

 @startuml

 actor "CallerExterno" as CallerExterno
 participant "Interfaz de Llamadas" as Iface <<frontend>>
 participant "Servicio de Llamadas" as SvcNode <<api>>
 database "MariaDB (tbl_historico_*)" as Store <<sql>>

 CallerExterno -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> CallerExterno : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_CLI_03 — Esperar en Cola — Comunicacion entre Objetos

 @startuml

 object ":CallerExterno" as Actor
 object ":Interfaz de Llamadas" as Iface
 object ":Servicio de Llamadas" as Svc
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

 :doc:`/requisitos/casos-uso/caller/uc-cli-03/diagramas-uml`
