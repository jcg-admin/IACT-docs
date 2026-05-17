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

.. uml::
 :caption: Flujo de autenticación — login exitoso (flujo principal).

 @startuml

 participant "Interfaz\nde Usuario" as Interfaz
 participant "Servicio\nde Autenticación" as SERVICIO_AUTH
 participant "Repositorio\nde Usuarios" as REPOSITORIO_USUARIOS
 participant "Repositorio\nde Sesiones" as SESSIONS

 Interfaz -> SERVICIO_AUTH ++ : POST /api/v1/auth/login\n{usuario, contraseña}
 SERVICIO_AUTH -> REPOSITORIO_USUARIOS ++ : verificar usuario activo
 return usuario encontrado y activo
 SERVICIO_AUTH -> SERVICIO_AUTH : validar contraseña contra hash almacenado
 SERVICIO_AUTH -> SESSIONS ++ : invalidar sesión previa (sesión única)
 return sesión previa invalidada
 SERVICIO_AUTH -> SESSIONS : registrar nueva sesión\n{ip, user-agent, timestamp}
 SERVICIO_AUTH -> SERVICIO_AUTH : generar token de autenticación\n(expiración 1 hora)
 return 200 + token de autenticación

 note right of SERVICIO_AUTH
   Timeout de 15 minutos por
   inactividad aplicado por
   middleware (Actor: Tiempo).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/auth/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
