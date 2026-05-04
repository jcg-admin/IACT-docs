.. meta::
 :artefacto: FR-040.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-040-01:

===========================================================================
FR-040.01: Compartir vista de reporte con usuario o grupo, con notificación
===========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-040.01
 * - **Nombre**
   - Compartir vista de reporte con usuario o grupo, con notificación
 * - **UC Origen**
   - UC_RPT_11: Compartir Reporte
 * - **Paso UC**
   - Pasos 1-8 del flujo principal
 * - **Módulo**
   - MOD_Reports
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE permitir compartir una vista de reporte con otro usuario o grupo CUANDO el propietario lo solicita con permiso share_reports, validando que el target exista, no sea el propietario y que expires_at sea futuro.

**Descripción:**

 Valida JWT + share_reports. Valida que view_id existe y owner == invoker, que target (usuario o AGR) existe, target ≠ owner, expires_at > now(). Crea ShareEntry + AuditEvent REPORT_SHARED + notificación por buzón interno al receptor.

----

3. Criterio de Aceptación
-------------------------

::

 DADO supervisor comparte vista con AGR 'team_alpha'
 CUANDO POST con view_id y target=agr_id
 ENTONCES 201 + notificación en buzón del receptor
 
 Escenario 1: Auto-compartir
 DADO target == owner
 ENTONCES 422
 
 Escenario 2: Target no existe
 DADO AGR inexistente
 ENTONCES 404

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
   - BReq-001, BReq-007
 * - **UC**
   - UC_RPT_11: Compartir Reporte
 * - **TEST**
   - TST-fr-040-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_11
