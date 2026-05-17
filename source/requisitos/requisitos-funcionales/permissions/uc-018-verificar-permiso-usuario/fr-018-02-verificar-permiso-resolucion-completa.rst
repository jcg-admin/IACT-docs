.. meta::
 :artefacto: FR-018.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-018-02:

=====================================================================
FR-018.02: Verificar permiso mediante resolución completa (slow path)
=====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-018.02
 * - **Nombre**
   - Verificar permiso mediante resolución completa (slow path)
 * - **UC Origen**
   - UC_PERM_07: Verificar Permiso de Usuario
 * - **Paso UC**
   - Pasos 7-10 del flujo principal
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

 El sistema DEBE resolver el conjunto efectivo de permisos del usuario desde la base de datos CUANDO no hay caché disponible, considerando AGRs asignados y permisos excepcionales vigentes.

**Descripción:**

 El slow path resuelve: AGRs activos del usuario → funciones de cada AGR, permisos excepcionales ACTIVE con expires_at > now(). Construye el conjunto efectivo, lo cachea y retorna el resultado. El caché se calienta con TTL configurado.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un usuario sin caché de permisos
 CUANDO se verifica una función
 ENTONCES resolución completa desde BD + caché calentado
 
 Escenario 1: Miss de caché
 DADO caché expirado o inexistente
 ENTONCES resolución BD + write al caché + allowed=true/false
 
 Escenario 2: Sin permisos asignados
 DADO usuario sin AGRs ni excepcionales activos
 ENTONCES allowed=false, conjunto vacío cacheado

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011, CNST-017

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_07: Verificar Permiso de Usuario
 * - **Depende de**
   - FR-018.01
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-018-02 (pendiente)

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
   - Versión inicial derivada de UC_PERM_07
