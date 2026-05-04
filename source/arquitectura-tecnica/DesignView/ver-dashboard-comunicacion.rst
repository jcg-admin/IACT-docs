.. meta::
 :artefacto: AT_UC_RPT_01_DESIGN_COMUNICACION
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_01_design_comunicacion:

======================================================
UC_RPT_01 — Ver Dashboard — Comunicacion entre Objetos
======================================================

.. uml::
 :caption: UC_RPT_01 — Ver Dashboard — Comunicacion entre Objetos

 @startuml

 object ":view_dashboard" as Actor
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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-01/diagramas-uml`

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-01/diagramas-uml`
