.. meta::
 :artefacto: AT_UC_RPT_02_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_02_process:

================================================================
UC_RPT_02 — Ver Metricas en Tiempo Real: Process View
================================================================

Flujo de actividades y concurrencia para UC_RPT_02.

.. uml::
 :caption: UC_RPT_02 — Process View (actividades)

 @startuml

 start
 :view_kpis solicita Ver Metricas en Tiempo Real;
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

 :doc:`/requisitos/casos-uso/reports/uc-rpt-02/flujo-principal`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-02/flujos-alternos`
