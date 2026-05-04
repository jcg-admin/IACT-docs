.. meta::
 :artefacto: AT_UC_RPT_16_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_16_process:

=========================================================
UC_RPT_16 — Reporte de Menus IVR: Process View
=========================================================

Flujo de actividades y concurrencia para UC_RPT_16.

.. uml::
 :caption: UC_RPT_16 — Process View (actividades)

 @startuml

 start
 :view_reports solicita Reporte de Menus IVR;
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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-16/flujo-principal`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-16/flujos-alternos`
