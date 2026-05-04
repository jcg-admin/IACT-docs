.. meta::
 :artefacto: AT_UC_ALR_05_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_05_process:

============================================================
UC_ALR_05 — Gestionar Suscripciones: Process View
============================================================

Flujo de actividades y concurrencia para UC_ALR_05.

.. uml::
 :caption: UC_ALR_05 — Process View (actividades)

 @startuml

 start
 :subscribe_to_alert solicita Gestionar Suscripciones;
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

 :doc:`/requisitos/casos-uso/alerts/uc-alr-05/flujo-principal`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-05/flujos-alternos`
