.. meta::
 :artefacto: FR-029.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/operator
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-029-01:

=============================================================
FR-029.01: Consultar métricas de desempeño propias del agente
=============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-029.01
 * - **Nombre**
   - Consultar métricas de desempeño propias del agente
 * - **UC Origen**
   - UC_OPR_08: Ver Métricas Propias del Agente
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
 * - **Módulo**
   - MOD_Operator
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar las métricas de desempeño del agente autenticado CUANDO solicita su dashboard personal, usando caché con TTL corto para reducir carga.

**Descripción:**

 Valida JWT (no requiere RBAC adicional — es vista propia). Consulta caché (TTL 30s). En cache miss, query AgentDailyStat WHERE agent_id = invoker.id y calcula KPIs derivados (TMO, AHT, etc.). Si el agente optó por ranking, incluye posición anonimizada del equipo.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un agente solicita sus métricas del día
 CUANDO GET /api/me/metrics/
 ENTONCES 200 con KPIs del día
 
 Escenario 1: Cache hit
 DADO métricas cacheadas
 ENTONCES respuesta < 10ms con datos del caché
 
 Escenario 2: Cache miss
 DADO sin caché
 ENTONCES query BD + KPIs calculados + cache warm

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
   - BReq-001
 * - **UC**
   - UC_OPR_08: Ver Métricas Propias del Agente
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-029-01 (pendiente)

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
   - Versión inicial derivada de UC_OPR_08
