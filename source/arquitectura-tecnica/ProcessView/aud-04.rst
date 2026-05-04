.. meta::
 :artefacto: AT_UC_AUD_04_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_04_process:

==================================================================
UC_AUD_04 — Generar Reporte de Compliance: Process View
==================================================================

Flujo de actividades y concurrencia para UC_AUD_04.

.. uml::
 :caption: UC_AUD_04 — Process View (actividades)

 @startuml

 start
 :generate_compliance_report solicita Generar Reporte de Compliance;
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

 :doc:`/requisitos/casos-uso/audit/uc-aud-04/flujo-principal`
 :doc:`/requisitos/casos-uso/audit/uc-aud-04/flujos-alternos`
