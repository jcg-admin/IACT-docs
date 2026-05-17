.. meta::
 :artefacto: FR-056.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/audit
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-056-01:

==========================================================================
FR-056.01: Búsqueda full-text en audit log con throttling y meta-auditoría
==========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-056.01
 * - **Nombre**
   - Búsqueda full-text en audit log con throttling y meta-auditoría
 * - **UC Origen**
   - UC_AUD_02: Buscar en Audit Log
 * - **Paso UC**
   - Pasos 1-9 del flujo principal
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

 El sistema DEBE permitir búsqueda full-text en el audit log CUANDO un usuario con search_audit_log lo solicita, aplicando throttling y registrando la búsqueda como meta-evento.

**Descripción:**

 Valida JWT + search_audit_log. Valida: query no vacío, date range obligatorio ≤ 90 días. Aplica throttle (search costoso). Search en FTS engine + filtros. Sanitiza resultados. Meta-audit AUDIT_SEARCH_QUERIED con query (sin PII en query) + filtros.

----

3. Criterio de Aceptación
-------------------------

::

 DADO auditor busca 'AGR_ASSIGNED' con date range
 CUANDO POST query
 ENTONCES resultados sanitizados + AUDIT_SEARCH_QUERIED
 
 Escenario 1: Sin date range
 DADO query sin date_from/date_to
 ENTONCES 422 date range obligatorio
 
 Escenario 2: Throttle activo
 DADO rate limit excedido
 ENTONCES 429

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011, CNST-013, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-003, BReq-004
 * - **UC**
   - UC_AUD_02: Buscar en Audit Log
 * - **TEST**
   - TST-fr-056-01 (pendiente)

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
   - Versión inicial derivada de UC_AUD_02
