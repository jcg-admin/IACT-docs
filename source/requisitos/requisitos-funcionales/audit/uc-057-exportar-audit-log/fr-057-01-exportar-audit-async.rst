.. meta::
 :artefacto: FR-057.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/audit
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-057-01:

============================================================================
FR-057.01: Exportar audit log asíncronamente con sanitización y notificación
============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-057.01
 * - **Nombre**
   - Exportar audit log asíncronamente con sanitización y notificación
 * - **UC Origen**
   - UC_AUD_03: Exportar Audit Log
 * - **Paso UC**
   - Pasos 1-8 del flujo principal y ejecución del worker
 * - **Módulo**
   - MOD_Audit
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE encolar una exportación de audit log CUANDO un usuario con export_audit_log lo solicita, con validación de volumen y re-verificación de permisos en el worker.

**Descripción:**

 Valida JWT + export_audit_log. Valida estimación ≤ 5M filas. Límite de jobs simultáneos. Crea ExportJob + AuditEvent AUDIT_EXPORT_QUEUED. Worker: re-check permiso, stream query, sanitize, escribir archivo, upload storage, mailbox notify, audit COMPLETED.

----

3. Criterio de Aceptación
-------------------------

::

 DADO auditor solicita exportación de 3M eventos
 CUANDO POST con filtros
 ENTONCES 202 con job_id
 
 Escenario 1: Volumen excedido
 DADO estimación > 5M filas
 ENTONCES 422

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-003, BReq-004
 * - **UC**
   - UC_AUD_03: Exportar Audit Log
 * - **TEST**
   - TST-fr-057-01 (pendiente)

----

6. Historial
------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambio
 * - 1.0.0
   - 2026-05-04
   - Versión inicial derivada de UC_AUD_03
