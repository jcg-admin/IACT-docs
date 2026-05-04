.. meta::
 :artefacto: AT_UC_RPT_04_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_04_process:

=====================================================
UC_RPT_04 — Exportar Reporte: Process View
=====================================================

Flujo de actividades y concurrencia para UC_RPT_04.

.. uml::
 :caption: UC_RPT_04 — Process View (actividades)

 @startuml

 start
 :export_csv solicita Exportar Reporte;
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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-04/flujo-principal`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-04/flujos-alternos`
