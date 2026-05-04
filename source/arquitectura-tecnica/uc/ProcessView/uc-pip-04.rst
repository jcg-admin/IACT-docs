.. meta::
 :artefacto: AT_UC_PIP_04_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_04_process:

====================================================================
UC_PIP_04 — Solicitar Reintento de Pipeline: Process View
====================================================================

Flujo de actividades y concurrencia para UC_PIP_04.

.. uml::
 :caption: UC_PIP_04 — Process View (actividades)

 @startuml

 start
 :request_pipeline_retry solicita Solicitar Reintento de Pipeline;
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

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/flujo-principal`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/flujos-alternos`
