.. meta::
 :artefacto: FR-026.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-026-01:

===========================================================
FR-026.01: Transferir llamada a agente o cola (warm o cold)
===========================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-026.01
 * - **Nombre**
   - Transferir llamada a agente o cola (warm o cold)
 * - **UC Origen**
   - UC_OPR_05: Transferir Llamada
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
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

 El sistema DEBE transferir una llamada activa a otro agente o cola CUANDO el agente propietario lo solicita, soportando transferencia consulta (warm) y directa (cold).

**Descripción:**

 Se valida JWT + ownership de la llamada, que el target esté disponible o la cola sea válida. Warm transfer: Telephony.consult → presentar caso → complete-transfer. Cold transfer: Telephony.transfer directo. En ambos casos: TransferEvent + AuditEvent CALL_TRANSFERRED atómico.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente en llamada activa solicita transferencia
 CUANDO POST con target y tipo
 ENTONCES 200 y llamada transferida
 
 Escenario 1: Warm transfer exitoso
 DADO agente B disponible
 ENTONCES consulta → presentación → transferencia completa
 
 Escenario 2: Cold transfer exitoso
 DADO cola válida
 ENTONCES transferencia directa + CALL_TRANSFERRED
 
 Escenario 3: Target no disponible
 DADO agente B en estado busy
 ENTONCES 409

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
   - UC_OPR_05: Transferir Llamada
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-026-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_05
