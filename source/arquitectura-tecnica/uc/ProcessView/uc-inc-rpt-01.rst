.. meta::
 :artefacto: AT_UC_INC_RPT_01_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_inc_rpt_01_process:

==========================================================
UC_INC_RPT_01 — Resolver Segmento: Process View
==========================================================

Flujo de actividades y concurrencia para UC_INC_RPT_01.

.. uml::
 :caption: UC_INC_RPT_01 — Process View (actividades)

 @startuml

 start
 :view_reports solicita Resolver Segmento;
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

 :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/flujo-principal`
 :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/flujos-alternos`
