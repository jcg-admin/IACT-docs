.. meta::
 :artefacto: FR-055.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/audit
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-055-01:

=================================================================================
FR-055.01: Consultar audit log general con cursor y meta-auditoría de la consulta
=================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-055.01
 * - **Nombre**
   - Consultar audit log general con cursor y meta-auditoría de la consulta
 * - **UC Origen**
   - UC_AUD_01: Consultar Audit Log General
 * - **Paso UC**
   - Pasos 1-10 del flujo principal
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

 El sistema DEBE retornar eventos de auditoría general CUANDO un usuario con view_audit_log los consulta, registrando la propia consulta como meta-evento de auditoría.

**Descripción:**

 Valida JWT + view_audit_log. Query AuditRepo con cursor-based pagination. Sanitiza respuesta (trunca payload para no exponer datos sensibles). Registra meta-audit GENERAL_AUDIT_QUERIED. Si el meta-audit falla, retorna 503 (la consulta del log requiere trazabilidad).

----

3. Criterio de Aceptación
-------------------------

::

 DADO auditor solicita eventos de las últimas 24h
 CUANDO GET con filtros
 ENTONCES 200 con eventos paginados + GENERAL_AUDIT_QUERIED emitido
 
 Escenario 1: Meta-audit fallido
 DADO error en emisión de meta-audit
 ENTONCES 503 (trazabilidad requerida)

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-014, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-003, BReq-004
 * - **UC**
   - UC_AUD_01: Consultar Audit Log General
 * - **TEST**
   - TST-fr-055-01 (pendiente)

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
   - Versión inicial derivada de UC_AUD_01
