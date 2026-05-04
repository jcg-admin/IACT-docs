.. meta::
 :artefacto: FR-032.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-032-01:

==================================================================
FR-032.01: Renderizar dashboard con datos del segmento del usuario
==================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-032.01
 * - **Nombre**
   - Renderizar dashboard con datos del segmento del usuario
 * - **UC Origen**
   - UC_RPT_01: Ver Dashboard
 * - **Paso UC**
   - Pasos 1-9 del flujo principal
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

 El sistema DEBE renderizar el dashboard CUANDO un usuario con permiso view_reports lo solicita, mostrando únicamente los datos de su segmento resuelto (DIDs IVR asignados).

**Descripción:**

 Se valida JWT + RBAC view_reports, se resuelve el segmento del usuario (UC_INC_RPT_01), se consulta la fuente de datos filtrando por segmento, se aplica caché adaptativo y se retornan las métricas del período solicitado.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario con view_reports solicita GET /api/dashboard/?period=today
 CUANDO se procesa
 ENTONCES 200 con métricas del segmento del usuario
 
 Escenario 1: Con segmento asignado
 DADO user con DID asignado
 ENTONCES métricas del segmento nacional_A
 
 Escenario 2: Sin segmento
 DADO user sin DID asignado
 ENTONCES 403 EX-02 sin segmento

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011, CNST-017

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-001
 * - **UC**
   - UC_RPT_01: Ver Dashboard
 * - **TEST**
   - TST-fr-032-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_01
