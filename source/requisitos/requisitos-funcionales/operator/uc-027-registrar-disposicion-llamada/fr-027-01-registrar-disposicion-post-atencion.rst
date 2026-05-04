.. meta::
 :artefacto: FR-027.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-027-01:

=================================================================
FR-027.01: Registrar disposición de llamada y transicionar estado
=================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-027.01
 * - **Nombre**
   - Registrar disposición de llamada y transicionar estado
 * - **UC Origen**
   - UC_OPR_06: Registrar Disposición de Llamada
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

 El sistema DEBE registrar el código de disposición de una llamada finalizada CUANDO el agente selecciona el resultado de la atención, sanitizando las notas y transicionando automáticamente el estado a disponible.

**Descripción:**

 Se valida JWT + ownership de la llamada, que el disposition_code esté en el catálogo activo y se sanitizan las notas (sin PII). UPDATE CallSession.disposition + AuditEvent DISPOSITION_SET. Post-commit: transición automática del estado del agente ACW → available.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente en estado ACW (after-call-work) selecciona disposición
 CUANDO POST con disposition_code y notas
 ENTONCES 200 + disposición registrada + estado → available
 
 Escenario 1: Código válido
 DADO code='resolved' en catálogo activo
 ENTONCES UPDATE + DISPOSITION_SET + state=available
 
 Escenario 2: Código no en catálogo
 DADO code='custom_code' no existente
 ENTONCES 422

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_OPR_06: Registrar Disposición de Llamada
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-027-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_06
