.. meta::
 :artefacto: AT_UC_PIP_02_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_02_process:

==========================================================
UC_PIP_02 — Consultar Errores ETL: Process View
==========================================================

Flujo de actividades y concurrencia para UC_PIP_02.

.. uml::
 :caption: UC_PIP_02 — Process View (actividades)

 @startuml

 start
 :view_pipeline_errors solicita Consultar Errores ETL;
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

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/flujo-principal`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/flujos-alternos`
