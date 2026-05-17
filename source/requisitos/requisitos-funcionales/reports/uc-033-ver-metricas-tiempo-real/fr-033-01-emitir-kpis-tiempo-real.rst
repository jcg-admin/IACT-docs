.. meta::
 :artefacto: FR-033.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-033-01:

===============================================================================
FR-033.01: Emitir KPIs en tiempo real mediante SSE/WS con filtrado por segmento
===============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-033.01
 * - **Nombre**
   - Emitir KPIs en tiempo real mediante SSE/WS con filtrado por segmento
 * - **UC Origen**
   - UC_RPT_02: Ver Métricas en Tiempo Real
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

 El sistema DEBE emitir actualizaciones de KPIs en tiempo real CUANDO un usuario con permiso view_kpis establece una conexión SSE/WS, filtrando los datos a su segmento resuelto.

**Descripción:**

 Se valida JWT en el handshake, se verifica RBAC view_kpis, se resuelve el segmento (UC_INC_RPT_01). El servidor emite eventos con los KPIs actualizados periódicamente. La conexión se cierra si JWT expira o el usuario pierde el permiso.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario abre conexión SSE con JWT
 CUANDO handshake exitoso
 ENTONCES stream de KPIs del segmento del usuario
 
 Escenario 1: KPIs actualizados
 DADO métrica cambia
 ENTONCES evento emitido al cliente en ≤ 5s
 
 Escenario 2: JWT expirado
 DADO JWT vence durante la sesión
 ENTONCES conexión cerrada con código de expiración

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-017

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-001
 * - **UC**
   - UC_RPT_02: Ver Métricas en Tiempo Real
 * - **TEST**
   - TST-fr-033-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_02
