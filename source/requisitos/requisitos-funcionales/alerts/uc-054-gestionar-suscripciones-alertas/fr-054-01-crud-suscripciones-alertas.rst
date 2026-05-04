.. meta::
 :artefacto: FR-054.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/alerts
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-054-01:

=============================================================
FR-054.01: Crear y gestionar suscripciones a reglas de alerta
=============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-054.01
 * - **Nombre**
   - Crear y gestionar suscripciones a reglas de alerta
 * - **UC Origen**
   - UC_ALR_05: Gestionar Suscripciones a Alertas
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
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

 El sistema DEBE permitir suscribirse a reglas de alerta CUANDO el usuario solicita notificaciones, validando que el scope de la suscripción esté dentro del segmento del usuario destino.

**Descripción:**

 Self-subscribe: implícita manage_own_subscriptions. Suscribir a otros: subscribe_to_alert. Valida subscription_type, que la regla exista si se referencia rule_id, y scope ⊆ segmento del usuario target (CNST-008). INSERT Subscription + Audit. CRUD para list/delete.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario se suscribe a alerta de cola
 CUANDO POST con rule_id y subscription_type
 ENTONCES 201 + suscripción creada
 
 Escenario 1: Scope violado
 DADO regla en segmento no asignado
 ENTONCES 403

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-008, CNST-009, CNST-013

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-006
 * - **UC**
   - UC_ALR_05: Gestionar Suscripciones a Alertas
 * - **TEST**
   - TST-fr-054-01 (pendiente)

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
   - Versión inicial derivada de UC_ALR_05
