.. meta::
 :artefacto: FR-070.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/caller
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-070-01:

================================================================================
FR-070.01: Ejecutar encuesta de satisfacción post-llamada y registrar respuestas
================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-070.01
 * - **Nombre**
   - Ejecutar encuesta de satisfacción post-llamada y registrar respuestas
 * - **UC Origen**
   - UC_CLI_05: Encuesta Post-Llamada
 * - **Paso UC**
   - Pasos 1-6 del flujo principal
 * - **Módulo**
   - MOD_Caller
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE ejecutar la encuesta de satisfacción CUANDO el agente cuelga y el sistema mantiene al llamante en línea, registrando cada respuesta DTMF o marca de skip.

**Descripción:**

 Agente cuelga, sistema mantiene caller en línea. SurveyRunner reproduce preguntas secuencialmente: reproduce audio, espera DTMF (con timeout), registra respuesta o marca como skip. INSERT SurveyResponse con todas las respuestas. Reproduce mensaje de agradecimiento. Hangup.

----

3. Criterio de Aceptación
-------------------------

::

 DADO llamante queda en línea tras cuelgue del agente
 CUANDO SurveyRunner inicia
 ENTONCES preguntas reproducidas y respuestas registradas
 
 Escenario 1: Respuesta completada
 DADO llamante responde todas las preguntas
 ENTONCES SurveyResponse completo + agradecimiento
 
 Escenario 2: Timeout sin respuesta
 DADO llamante no responde pregunta
 ENTONCES respuesta marcada como skip

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
   - BReq-001
 * - **UC**
   - UC_CLI_05: Encuesta Post-Llamada
 * - **TEST**
   - TST-fr-070-01 (pendiente)

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
   - Versión inicial derivada de UC_CLI_05
