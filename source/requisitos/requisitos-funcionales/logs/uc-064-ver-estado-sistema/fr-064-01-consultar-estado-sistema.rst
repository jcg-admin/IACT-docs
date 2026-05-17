.. meta::
 :artefacto: FR-064.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-064-01:

==========================================================================
FR-064.01: Consultar estado integrado del sistema con caché de 30 segundos
==========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-064.01
 * - **Nombre**
   - Consultar estado integrado del sistema con caché de 30 segundos
 * - **UC Origen**
   - UC_LOG_06: Ver Estado del Sistema
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
 * - **Módulo**
   - MOD_Logs
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar el estado de salud integrado del sistema CUANDO un usuario lo solicita, combinando servicios, dependencias, ETL y alertas activas con caché de 30 segundos.

**Descripción:**

 Valida JWT + RBAC. Cache lookup (TTL 30s). En miss: query paralelo de servicios + dependencias + ETL (UC_PIP_01 summary) + alertas activas (count UC_ALR_02). Compute overall_status = peor estado individual. Cache write.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita estado del sistema
 CUANDO GET /api/system/status/
 ENTONCES 200 con overall_status y detalle por componente
 
 Escenario 1: Cache hit
 DADO estado cacheado
 ENTONCES respuesta inmediata
 
 Escenario 2: Servicio degradado
 DADO ETL con estado 'degradado'
 ENTONCES overall_status = 'degradado'

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
   - BReq-006
 * - **UC**
   - UC_LOG_06: Ver Estado del Sistema
 * - **TEST**
   - TST-fr-064-01 (pendiente)

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
   - Versión inicial derivada de UC_LOG_06
