.. meta::
 :artefacto: FR-052.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/alerts
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-052-01:

=============================================================================
FR-052.01: Reconocer alerta firing con nota y suprimir notificaciones futuras
=============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-052.01
 * - **Nombre**
   - Reconocer alerta firing con nota y suprimir notificaciones futuras
 * - **UC Origen**
   - UC_ALR_03: Reconocer Alerta
 * - **Paso UC**
   - Pasos 1-9 del flujo principal
 * - **Módulo**
   - MOD_Alerts
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE marcar una alerta firing como acknowledged CUANDO un usuario con acknowledge_alert lo solicita, verificando que el scope de la alerta esté dentro del segmento del usuario.

**Descripción:**

 Valida JWT + acknowledge_alert. Carga la alerta, verifica scope ⊆ segmentos del usuario, valida state=firing. Atómico: UPDATE Alert (state=acknowledged, ack_by, ack_at, ack_note) + AuditEvent ALERT_ACKNOWLEDGED. Post-update: suprimir notificaciones futuras de esta alerta mientras siga acknowledged.

----

3. Criterio de Aceptación
-------------------------

::

 DADO supervisor reconoce alerta 'ASL crítico en cola_A'
 CUANDO POST con ack_note
 ENTONCES 200 + state=acknowledged + notificaciones suprimidas
 
 Escenario 1: Alerta ya acknowledged
 DADO state=acknowledged
 ENTONCES 409
 
 Escenario 2: Fuera de segmento
 DADO alerta en segmento no asignado
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
   - BReq-006
 * - **UC**
   - UC_ALR_03: Reconocer Alerta
 * - **TEST**
   - TST-fr-052-01 (pendiente)

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
   - Versión inicial derivada de UC_ALR_03
