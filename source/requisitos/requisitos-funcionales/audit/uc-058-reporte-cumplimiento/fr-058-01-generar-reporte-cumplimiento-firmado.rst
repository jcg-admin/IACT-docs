.. meta::
 :artefacto: FR-058.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/audit
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-058-01:

====================================================================================
FR-058.01: Generar reporte de cumplimiento con firma digital y almacenamiento seguro
====================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-058.01
 * - **Nombre**
   - Generar reporte de cumplimiento con firma digital y almacenamiento seguro
 * - **UC Origen**
   - UC_AUD_04: Generar Reporte de Cumplimiento
 * - **Paso UC**
   - Pasos 1-6 y W1-W7 del flujo principal
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

 El sistema DEBE generar reportes de cumplimiento normativo CUANDO un usuario autorizado lo solicita, firmando digitalmente el resultado y almacenándolo con URL firmada.

**Descripción:**

 Valida JWT + RBAC. Valida template y period. Encola ComplianceWorker. Worker: re-check permiso, ejecuta queries específicos del template, sanitiza y formatea, firma digitalmente (HMAC-SHA256 + timestamp), sube a storage, audit COMPLIANCE_REPORT_GENERATED con file_hash + signature, notificación por buzón.

----

3. Criterio de Aceptación
-------------------------

::

 DADO compliance officer solicita reporte anual
 CUANDO POST con template y year
 ENTONCES 202 + job_id
 
 Después de ejecución:
 ENTONCES archivo firmado en storage + notificación buzón + AuditEvent con file_hash

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
   - UC_AUD_04: Generar Reporte de Cumplimiento
 * - **TEST**
   - TST-fr-058-01 (pendiente)

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
   - Versión inicial derivada de UC_AUD_04
