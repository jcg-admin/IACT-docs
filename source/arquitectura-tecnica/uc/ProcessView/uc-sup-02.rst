.. meta::
 :artefacto: AT_UC_SUP_02_PROCESS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_02_process:

========================================================
UC_SUP_02 — Barge-in en Llamada: Process View
========================================================

Flujo de actividades y concurrencia para UC_SUP_02.

.. uml::
 :caption: UC_SUP_02 — Process View (actividades)

 @startuml

 start
 :barge_in_calls solicita Barge-in en Llamada;
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

 :doc:`/requisitos/casos-uso/supervision/uc-sup-02/flujo-principal`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-02/flujos-alternos`
