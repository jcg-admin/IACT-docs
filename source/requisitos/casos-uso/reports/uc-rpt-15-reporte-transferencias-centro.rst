.. meta::
 :artefacto: UC_RPT_15
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno
 :normativa: CNST_007, CNST_008, CNST_015

===================================================
UC_RPT_15: Ver Reporte de Transferencias por Centro
===================================================

.. note::

 Caso de uso nuevo en v5.4.0. Cubre análisis de transferencias
 entre centros — domain distinto a métricas de llamadas /
 agentes / colas / campañas. Decisión D-10 (WP
 rbac-modelo-conceptual-cleanup).

 Trazabilidad histórica: corresponde al UC-019 declarado en
 modelo RBAC v5.0/v5.1 (temp-holding) y mencionado en
 frontend/analisis_api_frontend.md.

1. Resumen
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_RPT_15
 * - **Nombre**
   - Ver Reporte de Transferencias por Centro
 * - **Actor Principal**
   - AGR-002: ``report_viewer_group``
 * - **Modulo**
   - MOD_Reports
 * - **Funcion RBAC**
   - RPT-001 ``view_reports`` (instancia: scope=transferencias_por_centro)
 * - **Prioridad**
   - Media
 * - **Complejidad**
   - Media
 * - **BReq Origen**
   - BRQ-RPT-015

2. Descripcion
--------------

Permite consultar el reporte de transferencias entre centros del
servicio IACT: cuántas llamadas se transfirieron desde un centro
a otro, en qué franjas horarias, con qué motivos, y qué
porcentaje de éxito tuvieron.

**Características principales:**

- Visualización tabular con filtros por centro origen / destino,
  rango de fechas, tipo de transferencia.
- Agregaciones por centro, día, semana, mes.
- Métricas: volumen, tasa de éxito, tiempo promedio en cola
  post-transferencia.
- Datos provenientes de BD Analytics (CNST-007).
- Filtrado automático por segmento del usuario (CNST-008).
- Rango máximo 2 años (CNST-015).

3. Diagrama de Caso de Uso
--------------------------

.. uml::
 :caption: Diagrama de Caso de Uso - UC_RPT_15

 @startuml
 left to right direction
 actor "AGR-002\nreport_viewer_group" as USER

 rectangle "MOD_Reports" {
 usecase "UC_RPT_15\nReporte Transferencias" as UC15
 usecase "Filtrar por\nCentros" as CTR
 usecase "Filtrar por\nFechas" as F
 usecase "Comparar\nPeriodos" as CMP
 usecase "Exportar\nReporte" as EXP
 }

 USER --> UC15
 UC15 --> CTR : include
 UC15 --> F : include
 UC15 --> CMP : extend
 UC15 --> EXP : extend
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
   - Existen datos de transferencias en el rango solicitado.

4.2 Trigger
^^^^^^^^^^^

El usuario accede al reporte de transferencias por centro desde el menú.

4.3 Postcondiciones
^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Postcondicion
 * - POST-01
   - Se muestra el reporte de transferencias con filtros aplicados.

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
   - Accede al reporte de transferencias por centro.
 * - 2
   - Sistema
   - Valida función RPT-001.
 * - 3
   - Sistema
   - Aplica filtro automático por segmento (CNST-008).
 * - 4
   - Usuario
   - Selecciona centros origen / destino y rango de fechas.
 * - 5
   - Sistema
   - Valida rango ≤ 2 años (CNST-015).
 * - 6
   - Sistema
   - Consulta BD Analytics (CNST-007).
 * - 7
   - Sistema
   - Renderiza tabla y métricas agregadas.

6. Excepciones
--------------

6.1 EX-01: Rango Excede 2 Años
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Como uc-rpt-03 EX-01: rechazo con código RPT-150.

6.2 EX-02: Sin Datos en Rango
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mostrar reporte vacío con mensaje informativo.

7. Reglas de Negocio
--------------------

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Regla
   - Descripción
 * - BR-RPT-150
   - Rango Máximo
   - 2 años (CNST-015)
 * - BR-RPT-151
   - Filtro Segmento
   - Datos siempre filtrados por segmento del usuario
 * - BR-RPT-152
   - Origen de datos
   - BD Analytics exclusivamente (CNST-007)

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
   - Máximo 2 años consultables

9. Trazabilidad
---------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **BReq Origen**
   - BRQ-RPT-015 (cubre necesidad UC-019 histórico)
 * - **Funcion RBAC**
   - RPT-001 ``view_reports`` (instancia: scope=transferencias_por_centro)
 * - **UCs Relacionados**
   - uc-rpt-03 (Históricos), uc-rpt-04 (Exportar), uc-rpt-12/13/14 (otros tipos de reportes)

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
   - Versión inicial. Caso de uso nuevo en v5.4.0 — cubre necesidad histórica UC-019 (Reporte de transferencias por centro). Decision D-10.
