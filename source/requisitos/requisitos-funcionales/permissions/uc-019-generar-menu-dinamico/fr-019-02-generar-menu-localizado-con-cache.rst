.. meta::
 :artefacto: FR-019.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-019-02:

=================================================================
FR-019.02: Generar menú localizado con caché por usuario y locale
=================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-019.02
 * - **Nombre**
   - Generar menú localizado con caché por usuario y locale
 * - **UC Origen**
   - UC_PERM_08: Generar Menú Dinámico
 * - **Paso UC**
   - Pasos 8-9 del flujo principal
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

 El sistema DEBE construir el menú en el idioma del usuario y cachearlo por combinación usuario+locale CUANDO el menú se genera exitosamente.

**Descripción:**

 El locale se resuelve con precedencia: query param > Accept-Language header > User.preferred_locale > 'es' (default). El menú se cachea bajo la clave menu:{user_id}:{locale} para evitar regeneración en solicitudes subsiguientes. En hit de caché se retorna con campo cache=true.

----

3. Criterio de Aceptación
-------------------------

::

 DADO GET /api/me/menu/?locale=en
 CUANDO el menú se genera
 ENTONCES ítems en inglés y caché con clave menu:{id}:en
 
 Escenario 1: Cache hit
 DADO menú cacheado para el usuario en locale es
 ENTONCES respuesta inmediata con cache=true
 
 Escenario 2: Locale fallback
 DADO sin query param ni header
 ENTONCES locale = User.preferred_locale o 'es'

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
   - UC_PERM_08: Generar Menú Dinámico
 * - **Depende de**
   - FR-019.01
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-019-02 (pendiente)

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
