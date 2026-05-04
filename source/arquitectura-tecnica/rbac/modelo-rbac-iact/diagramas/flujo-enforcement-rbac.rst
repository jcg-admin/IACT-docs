.. meta::
 :artefacto: AT_RBAC_DIAG_FLUJO_ENFORCEMENT
 :tipo: Diagrama Arquitectonico — Modelo RBAC
 :dominio: arquitectura_tecnica
 :subdominio: rbac/modelo-rbac-iact/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _rbac_flujo_enforcement:

=========================
Flujo de Enforcement RBAC
=========================

Flujo de Enforcement RBAC
==========================

.. uml::
 :caption: Secuencia de enforcement — cada request valida funcion atomica antes de ejecutar.

 @startuml

 actor "Usuario" as Usuario
 participant "Endpoint" as Endpoint
 participant "AuthGuard" as AuthGuard
 participant "FunctionCheck" as FunctionCheck
 database "AssignmentRepo" as AssignmentRepo
 participant "SoDValidator" as SoDValidator
 participant "Handler" as Handler

 Usuario -> Endpoint : HTTP request + JWT
 Endpoint -> AuthGuard : validar token
 AuthGuard -> AuthGuard : decodificar JWT
 alt token invalido
   AuthGuard --> Usuario : 401 Unauthorized
 else token valido
   AuthGuard -> FunctionCheck : verificar funcion requerida
   FunctionCheck -> AssignmentRepo : consultar funciones efectivas\n(directas + via grupo)
   AssignmentRepo --> FunctionCheck : conjunto de funciones activas
   alt funcion ausente
     FunctionCheck --> Usuario : 403 Forbidden
   else funcion presente
     FunctionCheck -> SoDValidator : verificar SoD\n(no conflicto en conjunto)
     alt viola SoD
       SoDValidator --> Usuario : 409 SoD Violation
     else SoD ok
       FunctionCheck -> Handler : ejecutar handler
       Handler --> Usuario : 200 / 201 response
     end
   end
 end

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
