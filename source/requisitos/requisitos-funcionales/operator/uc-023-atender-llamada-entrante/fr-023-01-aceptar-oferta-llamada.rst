.. meta::
 :artefacto: FR-023.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-023-01:

=======================================================================
FR-023.01: Aceptar oferta de llamada y establecer canal de comunicación
=======================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-023.01
 * - **Nombre**
   - Aceptar oferta de llamada y establecer canal de comunicación
 * - **UC Origen**
   - UC_OPR_02: Atender Llamada Entrante
 * - **Paso UC**
   - Pasos 3-8 del flujo principal
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

 El sistema DEBE establecer el canal de comunicación entre agente y llamante CUANDO el agente acepta la oferta de llamada, validando que la oferta es vigente y pertenece al agente.

**Descripción:**

 El backend valida JWT, verifica que call_id corresponde a una oferta activa para el agente, invoca Telephony.bridge(agent, caller), actualiza state=busy y crea el registro CallSession con evento CALL_ANSWERED de forma atómica.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente recibe oferta de llamada y clickea answer
 CUANDO POST con call_id
 ENTONCES 200 OK con info de llamada y canal establecido
 
 Escenario 1: Oferta vigente
 DADO call_id pertenece al agente con oferta activa
 ENTONCES bridge establecido + state=busy
 
 Escenario 2: Oferta expirada
 DADO oferta ya no vigente
 ENTONCES 409 oferta no disponible

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
   - UC_OPR_02: Atender Llamada Entrante
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-023-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_02
