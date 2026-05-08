.. meta::
 :artefacto: FR-010.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/access
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-01-07
 :autor: Equipo IACT
 :clasificacion: Interno

.. _fr-010-02:

=======================================
FR-010.02: Validar separacion antes de asignar
=======================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-010.02
 * - **Nombre**
   - Validar restricciones de separacion antes de asignar funciones
 * - **UC Origen**
   - UC_010: Asignar Funciones a Usuario
 * - **Paso UC**
   - Paso 5 del flujo normal, FA-1
 * - **Módulo**
   - MOD_Access
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Validación

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE validar que las funciones seleccionadas no violen
 restricciones de Separación de Funciones (separation of duties) CUANDO el admin
 intenta asignarlas (BR_007).

**Descripción:**

 Proceso de validación de separacion:
 
 1. Obtiene funciones actuales del usuario
 2. Combina con funciones seleccionadas para asignar
 3. Consulta tabla de restricciones de separacion
 4. Verifica cada par de funciones contra restricciones
 5. Si hay conflicto, bloquea asignación y muestra detalle
 
 **Tabla de Restricciones de Separacion:**
 
 - funcion_a: código de función
 - funcion_b: código de función incompatible
 - motivo: razón del conflicto
 - severidad: HARD (bloquea) / SOFT (advierte)
 
 **Ejemplo de Conflicto:**
 
 - assign_functions vs view_separation_rules
 - Motivo: "Quien asigna no debe auditar sus propias asignaciones"

----

3. Criterio de Aceptación
-------------------------

::

 DADO admin seleccionando funciones para asignar
 CUANDO confirma la selección
 ENTONCES el sistema valida separacion antes de proceder
 
 Escenario 1: Sin conflictos de separacion
 DADO funciones seleccionadas sin conflictos
 CUANDO se valida separacion
 ENTONCES validación pasa exitosamente
 Y se permite continuar con asignación
 
 Escenario 2: Conflicto HARD detectado
 DADO función assign_functions ya asignada
 Y se intenta asignar view_separation_rules
 CUANDO se valida
 ENTONCES se muestra "Conflicto de separacion: assign_functions incompatible con view_separation_rules"
 Y se muestra motivo del conflicto
 Y se BLOQUEA la asignación
 
 Escenario 3: Conflicto SOFT detectado
 DADO conflicto de severidad SOFT
 CUANDO se valida
 ENTONCES se muestra advertencia
 Y se permite continuar con confirmación adicional
 
 Escenario 4: Múltiples conflictos
 DADO selección con 3 conflictos de separacion
 CUANDO se valida
 ENTONCES se muestran los 3 conflictos en lista
 Y se indica cuáles son HARD y cuáles SOFT

----

4. Reglas y Restricciones
-------------------------

- **BR aplicables:**
  - BR_007: Separación de Funciones (separation of duties)
 
- **CNST aplicables:**
  - CNST-010: Segregación de funciones

**Configuración de separacion:**

Las restricciones de separacion se configuran en UC_ADM_01 y son mantenidas
por el administrador de seguridad.

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004: Cumplimiento de Seguridad
 * - **UC**
   - UC_010: Asignar Funciones
 * - **Depende de**
   - FR-010.01, UC_ADM_01 (configuración de separacion)
 * - **Requerido por**
   - FR-010.03
 * - **BR**
   - BR_007
 * - **CNST**
   - CNST-010
 * - **TEST**
   - TST-FR-010.02 (pendiente)

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
   - 2026-01-07
   - Versión inicial derivada de UC_010
