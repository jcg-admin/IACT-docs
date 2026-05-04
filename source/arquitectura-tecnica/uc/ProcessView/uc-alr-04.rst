.. meta::
 :artefacto: AT_UC_ALR_04_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_04_process:

=============================================================
UC_ALR_04 — Ver Historial de Alertas: Process View
=============================================================

Flujo de actividades y concurrencia para UC_ALR_04.

.. uml::
 :caption: UC_ALR_04 — Process View (actividades)

 @startuml

 start
 :view_alert_history solicita Ver Historial de Alertas;
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

 :doc:`/requisitos/casos-uso/alerts/uc-alr-04/flujo-principal`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-04/flujos-alternos`
