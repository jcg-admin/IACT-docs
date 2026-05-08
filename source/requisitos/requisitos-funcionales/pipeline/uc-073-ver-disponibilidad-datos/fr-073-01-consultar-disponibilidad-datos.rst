.. meta::
 :artefacto: FR-073.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/pipeline
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-073-01:

====================================================================
FR-073.01: Consultar estado de frescura de los datos IVR disponibles
====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-073.01
 * - **Nombre**
   - Consultar estado de frescura de los datos IVR disponibles
 * - **UC Origen**
   - UC_PIP_03: Ver Disponibilidad de Datos
 * - **Paso UC**
   - Pasos 1-5 del flujo principal
 * - **Módulo**
   - MOD_Pipeline
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar el estado de disponibilidad de los datos IVR CUANDO un usuario con view_data_availability lo solicita, calculando minutos desde el último ETL exitoso.

**Descripción:**

 Valida JWT + view_data_availability. Consulta última ejecución exitosa para el trimestre indicado (default: trimestre activo). Calcula minutos_desde_etl = now() - finished_at. Estado_frescura: fresco (<720 min) / degradado (720-1440 min) / vencido (≥1440 min). Sin ejecución exitosa: estado_frescura=vencido.

----

3. Criterio de Aceptación
-------------------------

::

 DADO analista solicita disponibilidad de datos
 CUANDO GET /api/v1/datos/disponibilidad/?trimestre=Q1_25
 ENTONCES 200 con minutos_desde_etl y estado_frescura
 
 Escenario 1: Datos frescos
 DADO último ETL exitoso hace 30 min
 ENTONCES estado_frescura=fresco
 
 Escenario 2: Sin ETL exitoso
 DADO sin ejecución exitosa para el trimestre
 ENTONCES estado_frescura=vencido

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-017

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-005
 * - **UC**
   - UC_PIP_03: Ver Disponibilidad de Datos
 * - **TEST**
   - TST-fr-073-01 (pendiente)

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
   - Versión inicial derivada de UC_PIP_03
