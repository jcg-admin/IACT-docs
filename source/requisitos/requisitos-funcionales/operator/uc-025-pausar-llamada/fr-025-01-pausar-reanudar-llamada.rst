.. meta::
 :artefacto: FR-025.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-025-01:

======================================================================
FR-025.01: Pausar y reanudar audio de llamada con tracking de duración
======================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-025.01
 * - **Nombre**
   - Pausar y reanudar audio de llamada con tracking de duración
 * - **UC Origen**
   - UC_OPR_04: Pausar Llamada (Hold/Unhold)
 * - **Paso UC**
   - Pasos 1-6 del flujo principal (hold y unhold)
 * - **Módulo**
   - MOD_Operator
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE pausar el audio bidireccional de la llamada CUANDO el agente solicita hold, registrando el inicio del hold; y reanudarla CUANDO solicita unhold, acumulando la duración total de hold en la sesión.

**Descripción:**

 Hold: valida JWT + ownership de la llamada (la llamada es del invoker), invoca Telephony.hold(call_id), registra CallSession.hold_started_at y emite AuditEvent CALL_HELD. Unhold: espejo con Telephony.unhold + acumula hold_duration_seconds += delta + AuditEvent CALL_UNHELD.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente en llamada activa solicita hold
 CUANDO POST hold
 ENTONCES 200 + hold_started_at registrado + CALL_HELD
 
 DADO el mismo agente solicita unhold
 CUANDO POST unhold
 ENTONCES 200 + hold_duration_seconds acumulado + CALL_UNHELD
 
 Escenario: No propietario
 DADO otro agente intenta hold de llamada ajena
 ENTONCES 403

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-025

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_OPR_04: Pausar Llamada (Hold/Unhold)
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-025-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_04
