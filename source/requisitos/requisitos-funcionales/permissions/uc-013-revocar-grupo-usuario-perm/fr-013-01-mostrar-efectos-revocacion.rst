.. meta::
 :artefacto: FR-013.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-013-01:

==============================================================
FR-013.01: Mostrar efectos de la revocación antes de confirmar
==============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-013.01
 * - **Nombre**
   - Mostrar efectos de la revocación antes de confirmar
 * - **UC Origen**
   - UC_PERM_02: Revocar Grupo a Usuario (vista PERM)
 * - **Paso UC**
   - Pasos 2-5 del flujo principal
 * - **Módulo**
   - MOD_Permissions
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE mostrar la composición completa del grupo y advertencias críticas CUANDO el administrador inicia la revocación de un grupo, antes de confirmarla.

**Descripción:**

 El modal de confirmación lista las funciones que se perderán con sus display_names. Si la revocación genera pérdida de capacidades críticas se muestran warnings. Los warnings críticos requieren doble confirmación.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un administrador inicia revocación de AGR 'user_admin_group' de Ana
 CUANDO clickea Revocar AGR
 ENTONCES el modal muestra 8 funciones a perder y cualquier warning crítico
 
 Escenario 1: Sin warnings
 DADO revocación sin impacto crítico
 ENTONCES modal normal con una confirmación
 
 Escenario 2: Con warnings críticos
 DADO revocación deja al User sin acceso a recursos activos
 ENTONCES modal con warnings y doble confirmación requerida

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_02: Revocar Grupo a Usuario (vista PERM)
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - FR-013.02
 * - **TEST**
   - TST-fr-013-01 (pendiente)

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
   - Versión inicial derivada de UC_PERM_02
