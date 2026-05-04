.. meta::
 :artefacto: ARQ_MOD_001_DIAG_FLUJO_AUTH
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/auth/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_001_flujo_autenticacion:

======================
Flujo de Autenticacion
======================

Flujo de Autenticacion
=======================

.. uml::
 :caption: Flujo de autenticación — login exitoso (flujo principal).

 @startuml

 participant "Interfaz\nde Usuario" as Interfaz
 participant "Servicio\nde Autenticación" as AUTH
 participant "Repositorio\nde Usuarios" as USERS
 participant "Repositorio\nde Sesiones" as SESSIONS

 Interfaz -> AUTH ++ : POST /api/v1/auth/login\n{usuario, contraseña}
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

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/auth/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
