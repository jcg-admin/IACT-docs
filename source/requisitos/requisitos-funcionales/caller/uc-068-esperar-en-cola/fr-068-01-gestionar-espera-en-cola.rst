.. meta::
 :artefacto: FR-068.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/caller
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-068-01:

=========================================================================
FR-068.01: Gestionar espera del llamante en cola con mensajes de posición
=========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-068.01
 * - **Nombre**
   - Gestionar espera del llamante en cola con mensajes de posición
 * - **UC Origen**
   - UC_CLI_03: Esperar en Cola
 * - **Paso UC**
   - Pasos 1-6 del flujo principal
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

 El sistema DEBE gestionar la espera del llamante en cola CUANDO es encolado, manteniendo música/mensajes de posición actualizados y registrando eventos de cola.

**Descripción:**

 INSERT QueueEntry con posición calculada. Reproduce music on hold + mensaje de bienvenida + estimación de espera. Cada N min: actualiza mensaje con posición actual. CallRouter asigna agente disponible. Cuando agente acepta (UC_OPR_02): bridge + DELETE QueueEntry. Eventos: QueueEvent (entered, position_changed, exited, abandoned).

----

3. Criterio de Aceptación
-------------------------

::

 DADO llamante encolado en cola_soporte
 CUANDO entra a la cola
 ENTONCES QueueEntry creado + mensajes de posición
 
 Escenario 1: Agente disponible
 DADO agente acepta la llamada
 ENTONCES bridge + QueueEntry eliminado + QueueEvent exited

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
   - UC_CLI_03: Esperar en Cola
 * - **TEST**
   - TST-fr-068-01 (pendiente)

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
   - Versión inicial derivada de UC_CLI_03
