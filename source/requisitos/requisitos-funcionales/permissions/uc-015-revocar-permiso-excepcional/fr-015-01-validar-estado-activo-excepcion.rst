.. meta::
 :artefacto: FR-015.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-015-01:

=====================================================================
FR-015.01: Validar estado activo antes de revocar permiso excepcional
=====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-015.01
 * - **Nombre**
   - Validar estado activo antes de revocar permiso excepcional
 * - **UC Origen**
   - UC_PERM_04: Revocar Permiso Excepcional
 * - **Paso UC**
   - Pasos 6-10 del flujo principal
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

 El sistema DEBE verificar que el permiso excepcional existe, está en estado ACTIVE y pertenece al usuario destino CUANDO se solicita su revocación.

**Descripción:**

 El backend localiza el permiso por ID, valida que state==ACTIVE (rechaza si ya REVOKED o EXPIRED), verifica que user_id coincide con la URL y aplica la restricción anti-self (P-11). El revoke_reason es obligatorio.

----

3. Criterio de Aceptación
-------------------------

::

 DADO una solicitud de revocación de permiso excepcional
 CUANDO el backend procesa la solicitud
 ENTONCES valida estado y pertenencia antes de revocar
 
 Escenario 1: Permiso ACTIVE
 DADO state=ACTIVE y user_id correcto
 ENTONCES procede a revocar
 
 Escenario 2: Permiso ya REVOKED
 DADO state=REVOKED
 ENTONCES 409 InvalidState
 
 Escenario 3: URL mismatch
 DADO user_id en URL ≠ user_id del permiso
 ENTONCES 404

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_04: Revocar Permiso Excepcional
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - FR-015.02
 * - **TEST**
   - TST-fr-015-01 (pendiente)

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
   - Versión inicial derivada de UC_PERM_04
