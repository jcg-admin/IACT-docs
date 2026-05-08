.. meta::
 :artefacto: AT_RBAC_DIAG_CLASES_ENTIDADES
 :tipo: Diagrama Arquitectonico — Modelo RBAC
 :dominio: arquitectura_tecnica
 :subdominio: rbac/modelo-rbac-iact/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _rbac_clases_entidades:

=================================
Modelo de Clases — Entidades RBAC
=================================

.. uml::
 :caption: Entidades centrales del modelo RBAC IACT v5.6.0 — 64 funciones atomicas activas (catalogo declara 77, 13 reservadas open-closed), 12 grupos, 3 reglas de separacion.

 @startuml

 class User {
   + user_id : Integer
   + username : String
   + state : Enum
 }

 class Function {
   + function_id : String
   + name : String
   + category : String
   + state : Enum
 }

 class FunctionGroup {
   + group_id : String
   + name : String
   + description : String
 }

 class Assignment {
   + user_id : Integer
   + function_id : String
   + state : String
   + granted_at : DateTime
   + expires_at : DateTime
 }

 class GroupAssignment {
   + user_id : Integer
   + group_id : String
   + granted_at : DateTime
   + expires_at : DateTime
 }

 class SeparationRule {
   + rule_id : String
   + name : String
   + state : String
 }

 class SeparationRuleDetail {
   + rule_id : String
   + function_id : String
   + group_side : Enum
 }

 User "1" *-- "0..*" Assignment : tiene
 User "1" *-- "0..*" GroupAssignment : pertenece a
 Function "1" *-- "0..*" Assignment : asignada a
 FunctionGroup "1" *-- "0..*" GroupAssignment : asignado a
 FunctionGroup "1" *-- "0..*" Function : contiene
 SeparationRule "1" *-- "2..*" SeparationRuleDetail : define grupos
 Function "1" -- "0..*" SeparationRuleDetail : referenciada por

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
