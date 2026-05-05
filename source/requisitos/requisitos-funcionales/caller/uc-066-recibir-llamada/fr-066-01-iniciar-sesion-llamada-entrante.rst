.. meta::
 :artefacto: FR-066.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/caller
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-066-01:

====================================================================
FR-066.01: Iniciar sesión de llamada con hash del caller y auditoría
====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-066.01
 * - **Nombre**
   - Iniciar sesión de llamada con hash del caller y auditoría
 * - **UC Origen**
   - UC_CLI_01: Recibir Llamada Entrante
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
 * - **Módulo**
   - MOD_Caller
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE iniciar una sesión de llamada CUANDO llega una llamada al DID, hasheando el caller_id para privacidad, creando el registro de sesión y emitiendo el evento de auditoría CALL_STARTED.

**Descripción:**

 TelephonyClient acepta la llamada. caller_id capturado + hasheado inmediatamente (PII pipeline, CNST-026). INSERT CallSession con caller_hash (no caller_id raw). Reproduce greeting audio. Pasa a IVR (UC_CLI_02) o direct queue. Audit CALL_STARTED con caller_hash + DID.

----

3. Criterio de Aceptación
-------------------------

::

 DADO llamada entrante al DID 19028031
 CUANDO TelephonyClient acepta
 ENTONCES CallSession creada con caller_hash + CALL_STARTED emitido
 
 Escenario 1: Hash inmediato
 DADO caller_id numérico
 ENTONCES solo caller_hash almacenado, nunca caller_id raw

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_CLI_01: Recibir Llamada Entrante
 * - **TEST**
   - TST-fr-066-01 (pendiente)

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
   - Versión inicial derivada de UC_CLI_01
