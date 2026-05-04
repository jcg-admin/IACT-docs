.. meta::
 :artefacto: FR-051.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/alerts
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-051-01:

=======================================================================
FR-051.01: Consultar alertas activas filtradas por segmento y severidad
=======================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-051.01
 * - **Nombre**
   - Consultar alertas activas filtradas por segmento y severidad
 * - **UC Origen**
   - UC_ALR_02: Ver Alertas Activas
 * - **Paso UC**
   - Pasos 1-8 del flujo principal
 * - **Módulo**
   - MOD_Alerts
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar alertas en estado firing o acknowledged CUANDO un usuario con view_alerts las solicita, filtradas por segmento y ordenadas por severidad descendente.

**Descripción:**

 Valida JWT + view_alerts + segmento. Query AlertRepo: state ∈ {firing, acknowledged}, scope ⊆ segmentos del usuario. Ordenado severidad DESC, fired_at DESC.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita alertas activas
 CUANDO GET con filtros
 ENTONCES lista de alertas del segmento ordenada por severidad
 
 Escenario 1: Sin alertas activas
 DADO no hay alertas firing o acked
 ENTONCES lista vacía 200

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-014

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-006
 * - **UC**
   - UC_ALR_02: Ver Alertas Activas
 * - **TEST**
   - TST-fr-051-01 (pendiente)

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
   - Versión inicial derivada de UC_ALR_02
