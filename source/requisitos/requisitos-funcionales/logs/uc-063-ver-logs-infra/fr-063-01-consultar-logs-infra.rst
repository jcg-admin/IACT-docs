.. meta::
 :artefacto: FR-063.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-063-01:

===========================================================================
FR-063.01: Consultar logs de infraestructura (host/container) con rango 24h
===========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-063.01
 * - **Nombre**
   - Consultar logs de infraestructura (host/container) con rango 24h
 * - **UC Origen**
   - UC_LOG_05: Ver Logs de Infraestructura
 * - **Paso UC**
   - Pasos 1-6 del flujo principal
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

 El sistema DEBE retornar logs de nivel infraestructura CUANDO un usuario con permisos de infraestructura los solicita, consultando el InfraLogStore con rango ≤ 24h.

**Descripción:**

 Valida JWT + RBAC (permisos infra). Valida range ≤ 24h. Query InfraLogStore (separado del LogStore de app). Sanitiza (no PII). Retorna 200.

----

3. Criterio de Aceptación
-------------------------

::

 DADO admin infra consulta logs del host
 CUANDO GET con range 12h
 ENTONCES logs de host/container sanitizados
 
 Escenario 1: Rango excedido
 DADO range > 24h
 ENTONCES 422

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-005, BReq-006
 * - **UC**
   - UC_LOG_05: Ver Logs de Infraestructura
 * - **TEST**
   - TST-fr-063-01 (pendiente)

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
   - Versión inicial derivada de UC_LOG_05
