.. _arq-mod-001-diagramas:

==============================================
ARQ_MOD_001 — Diagramas de Comportamiento
==============================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Flujo de Autenticacion
=======================

.. uml::
 :caption: Flujo de autenticación — login exitoso (flujo principal).

 @startuml

 participant "Interfaz\nde Usuario" as UI
 participant "Servicio\nde Autenticación" as AUTH
 participant "Repositorio\nde Usuarios" as USERS
 participant "Repositorio\nde Sesiones" as SESSIONS

 UI -> AUTH ++ : POST /api/v1/auth/login\n{usuario, contraseña}
 AUTH -> USERS ++ : verificar usuario activo
 return usuario encontrado y activo
 AUTH -> AUTH : validar contraseña contra hash almacenado
 AUTH -> SESSIONS ++ : invalidar sesión previa (sesión única)
 return sesión previa invalidada
 AUTH -> SESSIONS : registrar nueva sesión\n{ip, user-agent, timestamp}
 AUTH -> AUTH : generar token de autenticación\n(expiración 1 hora)
 return 200 + token de autenticación

 note right of AUTH
   Timeout de 15 minutos por
   inactividad aplicado por
   middleware (Actor: Tiempo).
 end note

 @enduml

----

Diagrama de Contexto (Dependencias)
=====================================

.. uml::
 :caption: Dependencias del módulo AUTH — componentes que requiere y que lo requieren.

 @startuml

 component "ARQ_MOD_001\nAutenticación" as AUTH
 component "ARQ_MOD_002\nIdentidad de Usuario" as USR
 component "ARQ_MOD_003\nControl de Acceso\n(RBAC)" as RBAC
 component "ARQ_MOD_007\nAuditoría" as AUD

 AUTH --> USR : verifica usuario activo
 AUTH --> RBAC : obtiene roles para claims del token
 AUTH --> AUD : emite evento login/logout

 @enduml
