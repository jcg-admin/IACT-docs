.. meta::
 :artefacto: FR-021.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-021-01:

==================================================================
FR-021.01: Consultar eventos de auditoría con filtros y paginación
==================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-021.01
 * - **Nombre**
   - Consultar eventos de auditoría con filtros y paginación
 * - **UC Origen**
   - UC_PERM_10: Consultar Auditoría de Permisos
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
 * - **Módulo**
   - MOD_Permissions
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar eventos de auditoría filtrados y paginados CUANDO un administrador autorizado consulta el log de auditoría de permisos.

**Descripción:**

 La consulta soporta filtros: actor_id, event_type (en enum), date_from/date_to (rango ≤ 90 días para modo online), page_size (≤ 200). Usa cursor-based pagination para consistencia. La consulta se dirige a la réplica de lectura. El response sanitiza PII (nombres/emails en hash). Requiere función view_audit_log.

----

3. Criterio de Aceptación
-------------------------

::

 DADO GET /api/audit-events/?event_type=AGR_REVOKED&date_from=X&date_to=Y
 CUANDO el administrador consulta
 ENTONCES lista paginada de eventos con cursor
 
 Escenario 1: Rango válido
 DADO date_from y date_to con diferencia < 90 días
 ENTONCES resultados de la réplica con cursor de siguiente página
 
 Escenario 2: Rango excedido
 DADO rango > 90 días
 ENTONCES 422 con mensaje de límite
 
 Escenario 3: Sin permiso view_audit_log
 DADO usuario sin la función
 ENTONCES 403 + AuditEvent UNAUTHORIZED

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-014, CNST-017, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_10: Consultar Auditoría de Permisos
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-021-01 (pendiente)

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
   - Versión inicial derivada de UC_PERM_10
