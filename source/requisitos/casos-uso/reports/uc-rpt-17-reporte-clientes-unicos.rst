.. meta::
 :artefacto: UC_RPT_17
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno
 :normativa: CNST_007, CNST_008, CNST_015, CNST_026

=========================================
UC_RPT_17: Ver Reporte de Clientes Únicos
=========================================

.. note::

 Caso de uso nuevo en v5.4.0. Cubre análisis de unicidad y
 recurrencia de clientes en el servicio IACT. Decisión D-10
 (WP rbac-modelo-conceptual-cleanup).

 Trazabilidad: mencionado en frontend/analisis_api_frontend.md
 como métrica de cliente.

1. Resumen
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_RPT_17
 * - **Nombre**
   - Ver Reporte de Clientes Únicos
 * - **Actor Principal**
   - AGR-002: ``report_viewer_group``
 * - **Modulo**
   - MOD_Reports
 * - **Funcion RBAC**
   - RPT-001 ``view_reports`` (instancia: scope=clientes_unicos)
 * - **Prioridad**
   - Media
 * - **Complejidad**
   - Media
 * - **BReq Origen**
   - BRQ-RPT-017

2. Descripcion
--------------

Permite consultar métricas de clientes únicos en el servicio IACT:
cuántos clientes distintos llamaron en un periodo, frecuencia de
recurrencia, distribución por horario, retorno tras transferencia.

**Características principales:**

- Conteo de clientes únicos por periodo (día / semana / mes).
- Análisis de recurrencia: distribución de "número de llamadas
  por cliente único".
- Identificación de clientes con alta frecuencia (top callers).
- PII enmascarada en visualización (CNST-026): se muestran
  identificadores opacos, no datos personales.
- Filtrado por segmento (CNST-008).
- Rango máximo 2 años (CNST-015).
- Datos desde BD Analytics (CNST-007).

3. Diagrama de Caso de Uso
--------------------------

.. uml::
 :caption: Diagrama de Caso de Uso - UC_RPT_17

 @startuml
 left to right direction
 actor "AGR-002\nreport_viewer_group" as USER

 rectangle "MOD_Reports" {
 usecase "UC_RPT_17\nClientes Únicos" as UC17
 usecase "Ver conteo\núnicos" as CNT
 usecase "Distribución\nrecurrencia" as REC
 usecase "Top callers\n(opacos)" as TOP
 usecase "Filtrar\nfechas" as F
 }

 USER --> UC17
 UC17 --> CNT : include
 UC17 --> REC : include
 UC17 --> TOP : extend
 UC17 --> F : include
 @enduml

4. Contexto de Ejecucion
------------------------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Precondicion
 * - PRE-01
   - Usuario tiene sesión activa con función RPT-001.
 * - PRE-02
   - Existen datos de llamadas en el rango solicitado.

4.2 Trigger
^^^^^^^^^^^

El usuario accede al reporte de clientes únicos desde el menú.

4.3 Postcondiciones
^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Postcondicion
 * - POST-01
   - Se muestran métricas con identificadores opacos (sin PII).

5. Flujo Normal
---------------

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Acción
 * - 1
   - Usuario
   - Accede al reporte de clientes únicos.
 * - 2
   - Sistema
   - Valida función RPT-001.
 * - 3
   - Usuario
   - Selecciona rango de fechas y agregación (día/semana/mes).
 * - 4
   - Sistema
   - Valida rango ≤ 2 años (CNST-015).
 * - 5
   - Sistema
   - Consulta BD Analytics (CNST-007) con filtro segmento.
 * - 6
   - Sistema
   - Calcula clientes únicos y distribución de recurrencia.
 * - 7
   - Sistema
   - Aplica enmascaramiento PII (CNST-026) en identificadores.
 * - 8
   - Sistema
   - Renderiza tabla y gráficos.

6. Excepciones
--------------

6.1 EX-01: Sin Datos
^^^^^^^^^^^^^^^^^^^^

Reporte vacío con mensaje informativo.

7. Reglas de Negocio
--------------------

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Regla
   - Descripción
 * - BR-RPT-170
   - PII enmascarada
   - Identificadores opacos en visualización (CNST-026)
 * - BR-RPT-171
   - Filtro Segmento
   - Datos por segmento del usuario
 * - BR-RPT-172
   - Rango Máximo
   - 2 años (CNST-015)

8. Restricciones de Arquitectura
--------------------------------

.. list-table::
 :widths: 15 25 60
 :header-rows: 1

 * - CNST
   - Nombre
   - Aplicación
 * - CNST_007
   - BD Dual
   - Datos desde BD Analytics
 * - CNST_008
   - Segmentos
   - Filtro automático
 * - CNST_015
   - Retención
   - Máximo 2 años
 * - CNST_026
   - PII
   - Identificadores enmascarados en UI

9. Trazabilidad
---------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **BReq Origen**
   - BRQ-RPT-017
 * - **Funcion RBAC**
   - RPT-001 ``view_reports`` (instancia: scope=clientes_unicos)
 * - **UCs Relacionados**
   - uc-rpt-03 (Históricos), uc-rpt-04 (Exportar)

10. Historial de Cambios
------------------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-04-30
   - Versión inicial. Caso de uso nuevo en v5.4.0 — cubre métrica de cliente único mencionada en frontend/analisis_api_frontend. Decision D-10.
