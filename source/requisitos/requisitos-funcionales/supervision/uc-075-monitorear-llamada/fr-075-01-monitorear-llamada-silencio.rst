.. meta::
 :artefacto: FR-075.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/supervision
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-075-01:

=====================================================================
FR-075.01: Monitorear llamada activa en modo escucha sin intervención
=====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-075.01
 * - **Nombre**
   - Monitorear llamada activa en modo escucha sin intervención
 * - **UC Origen**
   - UC_SUP_01: Monitorear Llamada (Escucha)
 * - **Paso UC**
   - Pasos 1-8 del flujo principal
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

 El sistema DEBE permitir al supervisor escuchar una llamada activa en modo silencio CUANDO lo solicita con razón justificada, validando que el agente esté en su segmento.

**Descripción:**

 Valida JWT + RBAC. Valida que el agente target esté dentro del segmento del supervisor (CNST-008). Reason ≥ 20 chars obligatorio. Telephony.bridge_listen (supervisor escucha, no habla con llamante). Tono audible al agente 'monitor on' (política de transparencia). Audit CALL_MONITORED con mode + reason.

----

3. Criterio de Aceptación
-------------------------

::

 DADO supervisor monitorea llamada del agente Ana
 CUANDO POST con agent_id y reason
 ENTONCES bridge_listen establecido + tono al agente + CALL_MONITORED
 
 Escenario 1: Agente fuera de segmento
 DADO agente en otro segmento
 ENTONCES 403
 
 Escenario 2: Reason insuficiente
 DADO reason de 10 chars
 ENTONCES 422

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
   - UC_SUP_01: Monitorear Llamada (Escucha)
 * - **TEST**
   - TST-fr-075-01 (pendiente)

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
   - Versión inicial derivada de UC_SUP_01
