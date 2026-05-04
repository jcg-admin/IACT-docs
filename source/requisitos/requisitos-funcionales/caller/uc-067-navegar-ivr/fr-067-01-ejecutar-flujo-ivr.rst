.. meta::
 :artefacto: FR-067.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/caller
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-067-01:

====================================================================
FR-067.01: Ejecutar flujo del menú IVR con registro de interacciones
====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-067.01
 * - **Nombre**
   - Ejecutar flujo del menú IVR con registro de interacciones
 * - **UC Origen**
   - UC_CLI_02: Navegar Menú IVR
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
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

 El sistema DEBE guiar al llamante por el árbol de menú IVR CUANDO el IVRRunner toma control de la sesión, registrando cada interacción como IVRSessionEvent.

**Descripción:**

 IVRRunner carga IVRDefinition para el DID/idioma. Reproduce nodo raíz. Espera input DTMF o voz (con timeout). Match input con opción: si nodo hijo, continúa navegación; si acción, la ejecuta (transfer a cola, info, etc.). Emite IVRSessionEvent por cada interacción (para UC_RPT_16).

----

3. Criterio de Aceptación
-------------------------

::

 DADO llamante navega el IVR
 CUANDO selecciona opción '1' para soporte
 ENTONCES navegación al nodo hijo + IVRSessionEvent registrado
 
 Escenario 1: Timeout sin input
 DADO llamante no presiona tecla en tiempo configurado
 ENTONCES repite prompt o redirige a cola

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-025

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-007
 * - **UC**
   - UC_CLI_02: Navegar Menú IVR
 * - **TEST**
   - TST-fr-067-01 (pendiente)

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
   - Versión inicial derivada de UC_CLI_02
