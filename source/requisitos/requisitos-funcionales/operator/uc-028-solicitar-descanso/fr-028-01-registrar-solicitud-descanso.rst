.. meta::
 :artefacto: FR-028.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-028-01:

===========================================================
FR-028.01: Registrar solicitud de descanso con tipo y cuota
===========================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-028.01
 * - **Nombre**
   - Registrar solicitud de descanso con tipo y cuota
 * - **UC Origen**
   - UC_OPR_07: Solicitar Descanso
 * - **Paso UC**
   - Pasos 1-6 del flujo principal
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

 El sistema DEBE registrar una solicitud de descanso del agente CUANDO se proporciona un tipo de descanso válido y el agente no ha excedido su cuota, delegando el cambio de estado al servicio de estados.

**Descripción:**

 Se valida JWT, que break_type esté en el enum permitido (coffee, lunch, bathroom, training, meeting) y que el agente no haya agotado la cuota para ese tipo de descanso en el día. Delega a UC_OPR_01 con new_state=break + reason=break_type. Inicia timer de duración máxima.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente disponible solicita descanso coffee
 CUANDO POST con break_type=coffee
 ENTONCES 200 + state=break + timer iniciado
 
 Escenario 1: Cuota disponible
 DADO agente no ha excedido cuota coffee del día
 ENTONCES estado cambia a break
 
 Escenario 2: Cuota agotada
 DADO agente ya usó cuota de coffee
 ENTONCES 422 cuota excedida

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
   - UC_OPR_07: Solicitar Descanso
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-028-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_07
