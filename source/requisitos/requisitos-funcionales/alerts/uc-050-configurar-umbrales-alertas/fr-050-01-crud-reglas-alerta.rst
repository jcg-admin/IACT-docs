.. meta::
 :artefacto: FR-050.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/alerts
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-050-01:

=====================================================================
FR-050.01: Crear y gestionar reglas de alerta con umbrales y acciones
=====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-050.01
 * - **Nombre**
   - Crear y gestionar reglas de alerta con umbrales y acciones
 * - **UC Origen**
   - UC_ALR_01: Configurar Umbrales de Alertas
 * - **Paso UC**
   - Pasos 1-8 y 3.2 del flujo principal
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

 El sistema DEBE permitir crear reglas de alerta CUANDO un usuario autorizado define umbrales con métrica, condición y acciones, validando que el scope esté dentro del segmento del propietario.

**Descripción:**

 Validaciones: metric en enum, scope ⊆ segmento del owner, condición coherente con métrica, mailbox targets existen. INSERT AlertRule + AuditEvent ALERT_RULE_CREATED + notificación al Evaluator para recarga. CRUD completo (update, delete, pause, resume) con audit por cada cambio.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario configura alerta 'ASL > 90s en cola_A'
 CUANDO POST con metric y threshold
 ENTONCES 201 + Evaluator recargado
 
 Escenario 1: Scope fuera de segmento
 DADO scope incluye DID no asignado
 ENTONCES 422

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
   - UC_ALR_01: Configurar Umbrales de Alertas
 * - **TEST**
   - TST-fr-050-01 (pendiente)

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
   - Versión inicial derivada de UC_ALR_01
