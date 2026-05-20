.. meta::
 :artefacto: FR-047.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-047-01:

==========================================================================================
FR-047.01: Resolver el segmento de datos accesible del usuario mediante DIDs IVR asignados
==========================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-047.01
 * - **Nombre**
   - Resolver el segmento de datos accesible del usuario mediante DIDs IVR asignados
 * - **UC Origen**
   - UC_INC_RPT_01: Resolver Segmento del Usuario
 * - **Paso UC**
   - Pasos 1-3 del flujo principal
 * - **Módulo**
   - MOD_Reports
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE resolver el conjunto de segmentos accesibles para un usuario CUANDO se invoca como inclusión en cualquier UC de reporte, consultando los DIDs IVR asignados por RBAC.

**Descripción:**

 Consulta la configuración RBAC del usuario para obtener los DIDs IVR asignados. Mapea cada DID a su segmento (nacional_A, nacional_B, Puebla, etc.). Si el usuario tiene permiso de administrador global, retorna todos los segmentos. Si no tiene ningún DID asignado y no es admin: retorna error EX-02 (sin segmento). Este UC es siempre invocado como paso de inclusión, no directamente por el usuario.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario con DID 19028031 asignado
 CUANDO se resuelve el segmento
 ENTONCES retorna [nacional_A]
 
 Escenario 1: Admin global
 DADO usuario con permiso admin global
 ENTONCES retorna todos los segmentos
 
 Escenario 2: Sin DID asignado
 DADO usuario sin ningún DID y sin admin global
 ENTONCES EX-02 sin segmento

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
   - BReq-001
 * - **UC**
   - UC_INC_RPT_01: Resolver Segmento del Usuario
 * - **TEST**
   - TST-fr-047-01 (pendiente)

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
   - Versión inicial derivada de UC_INC_RPT_01
