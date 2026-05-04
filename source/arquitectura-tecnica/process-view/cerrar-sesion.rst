.. meta::
 :artefacto: AT_UC_AUTH_02_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_02_process:

===================================================
UC_AUTH_02 — Cerrar Sesion: Process View
===================================================

Flujo de actividades y concurrencia para UC_AUTH_02.

.. uml::
 :caption: UC_AUTH_02 — Process View (actividades)

 @startuml

 start
 :close_user_session solicita Cerrar Sesion;
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

 :doc:`/requisitos/casos-uso/auth/uc-auth-02/flujo-principal`
 :doc:`/requisitos/casos-uso/auth/uc-auth-02/flujos-alternos`
