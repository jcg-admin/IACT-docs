.. meta::
 :artefacto: AT_UC_SUP_01_DESIGN_COMUNICACION
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_01_design_comunicacion:

===========================================================
UC_SUP_01 — Monitorear Llamada — Comunicacion entre Objetos
===========================================================

.. uml::
 :caption: UC_SUP_01 — Monitorear Llamada — Comunicacion entre Objetos

 @startuml

 object ":monitor_live_calls" as Actor
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

 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/diagramas-uml`

.. seealso::

 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/diagramas-uml`
