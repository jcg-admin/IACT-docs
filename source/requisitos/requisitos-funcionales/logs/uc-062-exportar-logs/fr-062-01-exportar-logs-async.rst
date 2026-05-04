.. meta::
 :artefacto: FR-062.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-062-01:

=======================================================================
FR-062.01: Exportar logs asíncronamente con re-verificación de permisos
=======================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-062.01
 * - **Nombre**
   - Exportar logs asíncronamente con re-verificación de permisos
 * - **UC Origen**
   - UC_LOG_04: Exportar Logs
 * - **Paso UC**
   - Pasos del flujo principal (crear job y worker)
 * - **Módulo**
   - MOD_Logs
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE encolar una exportación de logs CUANDO un usuario autorizado lo solicita, ejecutando la exportación asíncronamente con re-verificación de permisos en el worker.

**Descripción:**

 Estructura idéntica a UC_RPT_04 y UC_AUD_03. POST → JWT + RBAC → Validar → Crear ExportJob → Encolar → Audit QUEUED → 202. Worker: re-check permiso → stream LogStore → sanitize → escribir → upload storage → mailbox notify → audit COMPLETED.

----

3. Criterio de Aceptación
-------------------------

::

 DADO admin solicita exportación de logs de la semana
 CUANDO POST con filtros
 ENTONCES 202 con job_id
 
 Después:
 ENTONCES archivo en storage + notificación buzón

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-005
 * - **UC**
   - UC_LOG_04: Exportar Logs
 * - **TEST**
   - TST-fr-062-01 (pendiente)

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
   - Versión inicial derivada de UC_LOG_04
