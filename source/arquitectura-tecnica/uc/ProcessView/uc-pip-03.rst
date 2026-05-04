.. meta::
 :artefacto: AT_UC_PIP_03_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_03_process:

======================================================================
UC_PIP_03 — Consultar Disponibilidad de Datos: Process View
======================================================================

Flujo de actividades y concurrencia para UC_PIP_03.

.. uml::
 :caption: UC_PIP_03 — Process View (actividades)

 @startuml

 start
 :view_data_availability solicita Consultar Disponibilidad de Datos;
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

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/flujo-principal`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/flujos-alternos`
