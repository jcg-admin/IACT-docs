.. meta::
 :artefacto: FR-069.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/caller
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-069-01:

==========================================================================
FR-069.01: Registrar solicitud de callback del llamante con hash de número
==========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-069.01
 * - **Nombre**
   - Registrar solicitud de callback del llamante con hash de número
 * - **UC Origen**
   - UC_CLI_04: Solicitar Callback
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

 El sistema DEBE registrar una solicitud de callback CUANDO el llamante acepta la oferta de callback, hasheando el número de contacto y emitiendo el evento CALLBACK_REQUESTED.

**Descripción:**

 Sistema ofrece callback (prompt audio). Llamante confirma (DTMF). Captura número de callback (default = caller_id; opción ingresar otro). Hash + persist CallbackEntry. Audit CALLBACK_REQUESTED. Mensaje de confirmación al llamante. Hangup.

----

3. Criterio de Aceptación
-------------------------

::

 DADO llamante acepta oferta de callback
 CUANDO confirma con DTMF '1'
 ENTONCES CallbackEntry creado con hash + CALLBACK_REQUESTED + hangup
 
 Escenario 1: Número alternativo
 DADO llamante ingresa número diferente
 ENTONCES número alternativo hasheado como callback_hash

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
   - UC_CLI_04: Solicitar Callback
 * - **TEST**
   - TST-fr-069-01 (pendiente)

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
   - Versión inicial derivada de UC_CLI_04
