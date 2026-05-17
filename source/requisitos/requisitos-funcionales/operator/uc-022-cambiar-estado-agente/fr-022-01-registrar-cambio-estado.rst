.. meta::
 :artefacto: FR-022.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-022-01:

=============================================================================
FR-022.01: Registrar cambio de estado del agente con validación de transición
=============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-022.01
 * - **Nombre**
   - Registrar cambio de estado del agente con validación de transición
 * - **UC Origen**
   - UC_OPR_01: Cambiar Estado del Agente
 * - **Paso UC**
   - Pasos 1-5 del flujo principal
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

 El sistema DEBE registrar el cambio de estado del agente CUANDO se solicita un nuevo estado, validando que la transición sea válida y que se proporcione razón cuando sea obligatorio.

**Descripción:**

 Se valida: new_state en enum, que la transición sea permitida por la máquina de estados, y que reason esté presente para estados break/training (CNST-032). El UPDATE de estado y el AuditEvent AGENT_STATE_CHANGED son atómicos. Se notifica al CallRouter post-commit.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente solicita cambio de estado a 'available'
 CUANDO POST con new_state=available
 ENTONCES 200 OK y estado actualizado + AuditEvent
 
 Escenario 1: Transición válida
 DADO agente en estado 'break' → available
 ENTONCES UPDATE + audit con from, to, reason, duration
 
 Escenario 2: Transición inválida
 DADO agente en estado 'busy' → break
 ENTONCES 422 transición no permitida
 
 Escenario 3: Break sin reason
 DADO new_state=break sin reason
 ENTONCES 422 reason requerido

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
   - UC_OPR_01: Cambiar Estado del Agente
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-022-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_01
