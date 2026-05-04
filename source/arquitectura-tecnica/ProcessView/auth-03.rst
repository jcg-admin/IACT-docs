.. meta::
 :artefacto: AT_UC_AUTH_03_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_03_process:

==========================================================
UC_AUTH_03 — Recuperar Contrasena: Process View
==========================================================

Flujo de actividades y concurrencia para UC_AUTH_03.

.. uml::
 :caption: UC_AUTH_03 — Process View (actividades)

 @startuml

 start
 :reset_password solicita Recuperar Contrasena;
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

 :doc:`/requisitos/casos-uso/auth/uc-auth-03/flujo-principal`
 :doc:`/requisitos/casos-uso/auth/uc-auth-03/flujos-alternos`
