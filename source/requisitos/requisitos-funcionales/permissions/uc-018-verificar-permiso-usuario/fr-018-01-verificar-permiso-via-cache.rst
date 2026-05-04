.. meta::
 :artefacto: FR-018.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-018-01:

=======================================================
FR-018.01: Verificar permiso mediante caché (fast path)
=======================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-018.01
 * - **Nombre**
   - Verificar permiso mediante caché (fast path)
 * - **UC Origen**
   - UC_PERM_07: Verificar Permiso de Usuario
 * - **Paso UC**
   - Pasos 4-6 del flujo principal
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

 El sistema DEBE retornar el resultado de verificación de permiso desde el caché CUANDO el conjunto efectivo del usuario está disponible en caché, sin consultar la base de datos.

**Descripción:**

 El fast path consulta la clave cache:{user_id}:permissions y retorna allowed=true/false con source=cache. El caché es la ruta principal para verificaciones frecuentes (menú dinámico, guards de API).

----

3. Criterio de Aceptación
-------------------------

::

 DADO un usuario con caché de permisos válido
 CUANDO GET /api/users/{id}/permissions/check/?function=view_reports
 ENTONCES respuesta con allowed y source=cache sin consulta a BD
 
 Escenario 1: Hit de caché con permiso
 DADO función en conjunto efectivo cacheado
 ENTONCES allowed=true, source=cache, latencia <10ms
 
 Escenario 2: Hit de caché sin permiso
 DADO función no en conjunto efectivo
 ENTONCES allowed=false, source=cache

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
   - UC_PERM_07: Verificar Permiso de Usuario
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - FR-018.02
 * - **TEST**
   - TST-fr-018-01 (pendiente)

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
