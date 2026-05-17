.. meta::
 :artefacto: FR-019.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-019-01:

===========================================================
FR-019.01: Resolver conjunto efectivo de permisos para menú
===========================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-019.01
 * - **Nombre**
   - Resolver conjunto efectivo de permisos para menú
 * - **UC Origen**
   - UC_PERM_08: Generar Menú Dinámico
 * - **Paso UC**
   - Pasos 4-7 del flujo principal
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

 El sistema DEBE resolver el conjunto completo de permisos efectivos del usuario CUANDO se solicita el menú dinámico y no hay caché, invocando el servicio de verificación en bulk.

**Descripción:**

 El servicio invoca PermissionService.check_bulk con TODAS las function_codes registradas para construir el conjunto efectivo completo. Este conjunto determina qué elementos del menú son visibles para el usuario.

----

3. Criterio de Aceptación
-------------------------

::

 DADO GET /api/me/menu/ sin caché disponible
 CUANDO se genera el menú
 ENTONCES se resuelve el conjunto efectivo completo
 
 Escenario 1: Usuario con permisos
 DADO usuario con 5 funciones activas
 ENTONCES menú incluye los ítems correspondientes a esas 5 funciones
 
 Escenario 2: Usuario sin permisos
 DADO usuario sin AGRs ni excepcionales
 ENTONCES menú mínimo (solo ítems públicos)

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_08: Generar Menú Dinámico
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - FR-019.02
 * - **TEST**
   - TST-fr-019-01 (pendiente)

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
   - Versión inicial derivada de UC_PERM_08
