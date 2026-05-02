.. _modelo-rbac-iact-diagramas:

========================================
Modelo RBAC IACT — Diagramas
========================================


Modelo de Clases — Entidades RBAC
===================================

.. uml::
 :caption: Entidades centrales del modelo RBAC IACT v5.5.0 — 74 funciones atomicas, 12 grupos, 3 reglas SoD.

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

 class SoDRule {
   + rule_id : String
   + name : String
   + state : String
 }

 class SoDRuleDetail {
   + rule_id : String
   + function_id : String
   + group_side : Enum
 }

 User "1" *-- "0..*" Assignment : tiene
 User "1" *-- "0..*" GroupAssignment : pertenece a
 Function "1" *-- "0..*" Assignment : asignada a
 FunctionGroup "1" *-- "0..*" GroupAssignment : asignado a
 FunctionGroup "1" *-- "0..*" Function : contiene
 SoDRule "1" *-- "2..*" SoDRuleDetail : define grupos
 Function "1" -- "0..*" SoDRuleDetail : referenciada por

 @enduml


Flujo de Enforcement RBAC
==========================

.. uml::
 :caption: Secuencia de enforcement — cada request valida funcion atomica antes de ejecutar.

 @startuml

 actor "Usuario" as U
 participant "Endpoint" as E
 participant "AuthGuard" as AG
 participant "FunctionCheck" as FC
 database "AssignmentRepo" as AR
 participant "SoDValidator" as SV
 participant "Handler" as H

 U -> E : HTTP request + JWT
 E -> AG : validar token
 AG -> AG : decodificar JWT
 alt token invalido
   AG --> U : 401 Unauthorized
 else token valido
   AG -> FC : verificar funcion requerida
   FC -> AR : consultar funciones efectivas\n(directas + via grupo)
   AR --> FC : conjunto de funciones activas
   alt funcion ausente
     FC --> U : 403 Forbidden
   else funcion presente
     FC -> SV : verificar SoD\n(no conflicto en conjunto)
     alt viola SoD
       SV --> U : 409 SoD Violation
     else SoD ok
       FC -> H : ejecutar handler
       H --> U : 200 / 201 response
     end
   end
 end

 @enduml


Ciclo de Vida de una Asignacion
================================

.. uml::
 :caption: Estados de una asignacion de funcion — incluye expiracion automatica.

 @startuml

 [*] --> PENDING_VALIDATION : assign_functions invocado

 PENDING_VALIDATION --> ACTIVE : SoD ok + INSERT exitoso
 PENDING_VALIDATION --> REJECTED : viola SoD (EX-07)

 ACTIVE --> EXPIRED : expires_at alcanzado\n(job nocturno)
 ACTIVE --> REVOKED : revoke_functions invocado\n(UC_ACC_02)
 ACTIVE --> ACTIVE : re-asignacion\n(idempotente — 200)

 EXPIRED --> [*]
 REVOKED --> [*]
 REJECTED --> [*]

 note right of ACTIVE
   Cache de permisos invalidado
   en cada transicion.
 end note

 @enduml
