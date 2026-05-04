.. meta::
 :artefacto: FR-024.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-024-01:

============================================================
FR-024.01: Iniciar llamada saliente desde campaña o callback
============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-024.01
 * - **Nombre**
   - Iniciar llamada saliente desde campaña o callback
 * - **UC Origen**
   - UC_OPR_03: Iniciar Llamada Saliente
 * - **Paso UC**
   - Pasos 1-8 del flujo principal
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

 El sistema DEBE iniciar una llamada saliente CUANDO un agente disponible solicita marcar a un destino válido de su campaña asignada o callback pendiente.

**Descripción:**

 Se valida: JWT + RBAC con initiate_outbound_call, formato del destino, que el destino esté en la lista permitida de la campaña y que el agente esté en estado available. Se invoca Telephony.dial y si hay pickup se establece bridge + state=busy + CallSession + AuditEvent OUTBOUND_CALL_INITIATED.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente en estado available solicita llamada saliente
 CUANDO POST con destination
 ENTONCES 200 con call_session_id
 
 Escenario 1: Destino válido y pickup
 DADO destino en lista permitida y responde
 ENTONCES bridge + state=busy + OUTBOUND_CALL_INITIATED
 
 Escenario 2: Agente no disponible
 DADO agent state != available
 ENTONCES 409
 
 Escenario 3: Destino fuera de lista
 DADO destino no en campaña asignada
 ENTONCES 403

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013, CNST-025

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_OPR_03: Iniciar Llamada Saliente
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-024-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_03
