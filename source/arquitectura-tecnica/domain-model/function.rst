.. meta::
 :artefacto: AT_DM_CLASS_FUNCTION
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_function:

========
Function
========

Unidad atomica de permiso RBAC. Cada funcion corresponde a una
operacion del sistema (p.ej. ``view_reports``, ``acknowledge_alert``).
Las funciones se agrupan en ``FunctionGroup`` y se asignan a usuarios
via ``AccessGroup``.

.. uml::
 :caption: Clase Function — unidad atomica de permiso RBAC.

 @startuml

 class Function {
   + name : String          <<p.ej. view_reports>>
   + description : String
   + module : Module
   --
   + register()             <<sistema>>
   + view()                 <<view_assignments>>
 }

 enum Module {
   AUTH
   USR
   ACC
   PIP
   RPT
   ALR
   AUD
   LOG
 }

 Function "*" -- "1" Module : belongs_to

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/function-group`
 :doc:`/arquitectura-tecnica/domain-model/separation-rule`
