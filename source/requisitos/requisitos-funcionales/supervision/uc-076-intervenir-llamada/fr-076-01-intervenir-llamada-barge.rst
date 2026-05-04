.. meta::
 :artefacto: FR-076.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/supervision
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-076-01:

=================================================================================
FR-076.01: Intervenir en llamada activa con audio bidireccional o toma de control
=================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-076.01
 * - **Nombre**
   - Intervenir en llamada activa con audio bidireccional o toma de control
 * - **UC Origen**
   - UC_SUP_02: Intervenir en Llamada (Barge-In)
 * - **Paso UC**
   - Pasos 1-6 del flujo principal
 * - **Módulo**
   - MOD_Supervision
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE permitir al supervisor intervenir en una llamada activa CUANDO lo solicita, estableciendo audio bidireccional (barge) o tomando control completo (take-over).

**Descripción:**

 Valida JWT + RBAC. Valida segmento + reason. Modo barge: Telephony.bridge_3way con audio bidireccional supervisor. Modo take-over: supervisor barge + agente disconnect (variante). Audit CALL_BARGED con mode.

----

3. Criterio de Aceptación
-------------------------

::

 DADO supervisor interviene en llamada problemática
 CUANDO POST con mode=barge
 ENTONCES bridge_3way establecido + CALL_BARGED
 
 Escenario 1: Take-over
 DADO mode=take_over
 ENTONCES agente desconectado + supervisor toma la llamada

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-008, CNST-009, CNST-013, CNST-025

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_SUP_02: Intervenir en Llamada (Barge-In)
 * - **TEST**
   - TST-fr-076-01 (pendiente)

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
   - Versión inicial derivada de UC_SUP_02
