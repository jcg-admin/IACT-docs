.. meta::
 :artefacto: FR-014.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-014-01:

==================================================================
FR-014.01: Validar justificación y período del permiso excepcional
==================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-014.01
 * - **Nombre**
   - Validar justificación y período del permiso excepcional
 * - **UC Origen**
   - UC_PERM_03: Conceder Permiso Excepcional (vista PERM)
 * - **Paso UC**
   - Pasos 5-11 del flujo principal
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

 El sistema DEBE validar la justificación, el período de vigencia y las restricciones SoD CUANDO se solicita un permiso excepcional, antes de persistirlo.

**Descripción:**

 La validación incluye: función grant_exceptional_permission, restricción anti-self (P-11), justificación obligatoria no vacía, expires_at dentro de los límites permitidos, filtro de idempotencia y validación SoD del conjunto efectivo post-concesión.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un administrador envía POST con justification y expires_at
 CUANDO se procesa la solicitud
 ENTONCES se validan todas las reglas antes de persistir
 
 Escenario 1: Validación exitosa
 DADO payload completo y SoD sin conflicto
 ENTONCES INSERT ExceptionalPermission
 
 Escenario 2: Auto-concesión bloqueada
 DADO invoker == target_user
 ENTONCES 403 (P-11 anti-self)
 
 Escenario 3: expires_at fuera de límites
 DADO expires_at > max_permitido
 ENTONCES 422 con detalle del límite

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-005, CNST-009, CNST-013, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_03: Conceder Permiso Excepcional (vista PERM)
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - FR-014.02
 * - **TEST**
   - TST-fr-014-01 (pendiente)

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
   - Versión inicial derivada de UC_PERM_03
