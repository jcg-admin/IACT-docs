.. meta::
 :artefacto: AT_UC_OPR_08_DESIGN_COMUNICACION
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_08_design_comunicacion:

=============================================================
UC_OPR_08 — Ver Propio Dashboard — Comunicacion entre Objetos
=============================================================

.. uml::
 :caption: UC_OPR_08 — Ver Propio Dashboard — Comunicacion entre Objetos

 @startuml

 object ":view_own_performance_dashboard" as Actor
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

 :doc:`/requisitos/casos-uso/operator/uc-opr-08/diagramas-uml`

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-08/diagramas-uml`
