.. meta::
 :artefacto: AT_UC_RPT_09_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_09_process:

=======================================================
UC_RPT_09 — Configurar Filtros: Process View
=======================================================

Flujo de actividades y concurrencia para UC_RPT_09.

.. uml::
 :caption: UC_RPT_09 — Process View (actividades)

 @startuml

 start
 :filter_reports solicita Configurar Filtros;
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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-09/flujo-principal`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-09/flujos-alternos`
