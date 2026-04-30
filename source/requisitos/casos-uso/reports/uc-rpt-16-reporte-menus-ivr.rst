.. meta::
 :artefacto: UC_RPT_16
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

===================================
UC_RPT_16: Ver Reporte de Menús IVR
===================================

.. note::

 Caso de uso nuevo en v5.4.0. Cubre análisis de comportamiento
 y problemas de los menús IVR del sistema. Decisión D-10
 (WP rbac-modelo-conceptual-cleanup).

 Trazabilidad: mencionado en frontend/analisis_api_frontend.rst
 como "menús problemáticos" — análisis de UX del IVR.

1. Resumen
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_RPT_16
 * - **Nombre**
   - Ver Reporte de Menús IVR
 * - **Actor Principal**
   - AGR-002: ``report_viewer_group``
 * - **Modulo**
   - MOD_Reports
 * - **Funcion RBAC**
   - RPT-001 ``view_reports`` (instancia: scope=menus_ivr)
 * - **Prioridad**
   - Media
 * - **Complejidad**
   - Media
 * - **BReq Origen**
   - BRQ-RPT-016

2. Descripcion
--------------

Permite consultar el desempeño de los menús del IVR (Interactive
Voice Response): cuántos usuarios se atascan en cada nodo, qué
opciones tienen mayor abandono, qué menús requieren rediseño.

**Características principales:**

- Visualización de árbol de menús con métricas por nodo.
- Métricas: ingresos al menú, tiempo promedio, opción elegida,
  tasa de abandono, tasa de timeout.
- Identificación automática de "menús problemáticos" (alta tasa
  de abandono o timeout).
- Filtrado por segmento (CNST-008) y rango de fechas.
- Datos de BD Analytics (CNST-007).

3. Diagrama de Caso de Uso
--------------------------

.. uml::
 :caption: Diagrama de Caso de Uso - UC_RPT_16

 @startuml
 left to right direction
 actor "AGR-002\nreport_viewer_group" as USER

 rectangle "MOD_Reports" {
 usecase "UC_RPT_16\nReporte Menús IVR" as UC16
 usecase "Ver árbol\nmenús" as ARB
 usecase "Identificar\nproblemáticos" as PROB
 usecase "Filtrar por\nfechas" as F
 usecase "Exportar\nReporte" as EXP
 }

 USER --> UC16
 UC16 --> ARB : include
 UC16 --> PROB : extend
 UC16 --> F : include
 UC16 --> EXP : extend
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
   - Existen datos de eventos de menús IVR en el rango solicitado.

4.2 Trigger
^^^^^^^^^^^

El usuario accede al reporte de menús IVR desde el menú.

4.3 Postcondiciones
^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Postcondicion
 * - POST-01
   - Se muestra el árbol de menús con métricas y resaltado de problemáticos.

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
   - Accede al reporte de menús IVR.
 * - 2
   - Sistema
   - Valida función RPT-001.
 * - 3
   - Usuario
   - Selecciona rango de fechas (default: último mes).
 * - 4
   - Sistema
   - Valida rango ≤ 2 años (CNST-015).
 * - 5
   - Sistema
   - Consulta BD Analytics (CNST-007) con filtro de segmento.
 * - 6
   - Sistema
   - Calcula métricas por nodo del árbol IVR.
 * - 7
   - Sistema
   - Identifica menús problemáticos (umbrales configurables).
 * - 8
   - Sistema
   - Renderiza árbol con resaltado.

6. Excepciones
--------------

6.1 EX-01: Sin Datos
^^^^^^^^^^^^^^^^^^^^

Si no hay eventos para el rango/segmento, mostrar reporte vacío.

7. Reglas de Negocio
--------------------

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Regla
   - Descripción
 * - BR-RPT-160
   - Umbral problemático
   - Tasa de abandono > N% marca el nodo como problemático
 * - BR-RPT-161
   - Filtro Segmento
   - Datos por segmento del usuario
 * - BR-RPT-162
   - Origen
   - BD Analytics (CNST-007)

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

9. Trazabilidad
---------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **BReq Origen**
   - BRQ-RPT-016
 * - **Funcion RBAC**
   - RPT-001 ``view_reports`` (instancia: scope=menus_ivr)
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
   - Versión inicial. Caso de uso nuevo en v5.4.0 — cubre análisis de menús IVR mencionado en frontend/analisis_api_frontend. Decision D-10.
