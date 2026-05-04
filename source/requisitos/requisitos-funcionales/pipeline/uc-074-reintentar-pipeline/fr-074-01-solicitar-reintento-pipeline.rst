.. meta::
 :artefacto: FR-074.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/pipeline
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-074-01:

=======================================================================================
FR-074.01: Solicitar reintento manual del pipeline con verificación de ejecución activa
=======================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-074.01
 * - **Nombre**
   - Solicitar reintento manual del pipeline con verificación de ejecución activa
 * - **UC Origen**
   - UC_PIP_04: Reintentar Pipeline ETL
 * - **Paso UC**
   - Pasos 1-6 del flujo principal
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

 El sistema DEBE permitir reintentar el pipeline ETL CUANDO un administrador con request_pipeline_retry lo solicita, validando que no haya ejecución activa y registrando el intento manual.

**Descripción:**

 Valida JWT + request_pipeline_retry. Valida trimestre en formato correcto, motivo ≥ 20 chars. Verifica no hay ejecución en curso (estado='en_ejecucion'). INSERT en Registro con estado='en_ejecucion' y ejecutado_por='manual'. Invoca Disparador ETL. Worker ejecuta ETL y actualiza estado al finalizar.

----

3. Criterio de Aceptación
-------------------------

::

 DADO admin solicita reintento del Q1
 CUANDO POST con trimestre=Q1_25 y motivo
 ENTONCES 202 y ETL iniciado
 
 Escenario 1: Ya en ejecución
 DADO hay ejecución activa
 ENTONCES 409 Conflict
 
 Escenario 2: Motivo muy corto
 DADO motivo de 10 chars
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
   - BReq-005
 * - **UC**
   - UC_PIP_04: Reintentar Pipeline ETL
 * - **TEST**
   - TST-fr-074-01 (pendiente)

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
   - Versión inicial derivada de UC_PIP_04
