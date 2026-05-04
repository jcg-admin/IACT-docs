.. meta::
 :artefacto: AT_UC_AUTH_01_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_01_process:

====================================================
UC_AUTH_01 — Iniciar Sesion: Process View
====================================================

Flujo de actividades y concurrencia para UC_AUTH_01.

.. uml::
 :caption: UC_AUTH_01 — Process View (actividades)

 @startuml

 start
 :Usuario solicita Iniciar Sesion;
 :Validar autenticacion y permisos RBAC;
 if (permisos validos?) then (si)
   :Ejecutar logica principal;
   :Persistir resultado;
   :Registrar AuditEvent;
   :Retornar respuesta exitosa;
 else (no)
   :Retornar error 403;
 endif
 stop

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-01/flujo-principal`
 :doc:`/requisitos/casos-uso/auth/uc-auth-01/flujos-alternos`
