.. meta::
 :artefacto: AT_UC_CLI_02_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_02_process:

================================================
UC_CLI_02 — Navegar IVR: Process View
================================================

Flujo de actividades y concurrencia para UC_CLI_02.

.. uml::
 :caption: UC_CLI_02 — Process View (actividades)

 @startuml

 start
 :CallerExterno solicita Navegar IVR;
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

 :doc:`/requisitos/casos-uso/caller/uc-cli-02/flujo-principal`
 :doc:`/requisitos/casos-uso/caller/uc-cli-02/flujos-alternos`
