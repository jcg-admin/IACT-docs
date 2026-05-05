.. meta::
 :artefacto: AT_IMPL_MOD_ACCESS
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_access:

==========================================
Implementation View — MOD_Access
==========================================

Componentes y paquetes de codigo del modulo de control de acceso.
Cubre asignacion y revocacion de ``FunctionGroup`` / ``AccessGroup``
con verificacion de ``SeparationRule`` (SoD, CNST-030).

.. uml::
 :caption: Implementation View MOD_Access — componentes RBAC con SoD.

 @startuml

 package "MOD_Access" {
   component "AssignmentView\nSoDCheckView\nRevokeAssignmentView" as AccessView <<api>>
   component "AssignmentSerializer" as AccessSerializer <<serializer>>
   component "AccessService\nverificar SeparationRule\nasignar/revocar grupos" as AccessService <<service>>
   component "AssignmentRepository\nSoDRepository" as AccessRepo <<repository>>
   component "AssignmentORM\nSeparationRuleORM\nFunctionGroupORM" as AccessORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 AccessView --> AccessSerializer : valida
 AccessView --> AccessService : invoca
 AccessService --> AccessRepo : consulta / persiste
 AccessRepo --> AccessORM : mapea
 AccessORM --> AlmacenDatos : SQL

 note right of AccessService
   Assignment{state:AssignmentState}.
   SeparationRule.conflicting_functions verifica SoD.
   CNST-030: enforcement en tiempo de asignacion.
   AuditEvent{ACCESS_CHANGE} en cada operacion.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/assignment`
 :doc:`/arquitectura-tecnica/domain-model/separation-rule`
