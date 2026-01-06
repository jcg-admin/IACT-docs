.. meta::
   :artefacto: UC_022
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-022:

==============================================================================
UC-022: Generar Reporte Analisis de Cuentas
==============================================================================

.. contents:: Contenido
   :local:
   :depth: 2

----

1. Resumen
----------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **ID**
     - UC-022
   * - **Nombre**
     - Generar Reporte Analisis de Cuentas
   * - **Actor Primario**
     - Analista Contable
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Reports
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Media
   * - **BReq Origen**
     - BReq-002: Generacion de Reportes

----

2. Descripcion
--------------

Genera analisis detallado de una cuenta especifica mostrando todos sus
movimientos, tendencias mensuales, promedios y graficos de comportamiento.
Permite analizar patrones y anomalias en cuentas individuales.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-022 Analisis Cuentas
   :align: center
   :scale: 90%

   @startuml
   left to right direction
   skinparam actorStyle awesome
   skinparam backgroundColor #FAFAFA
   skinparam usecase {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
   }

   actor "Analista\nContable" as ANA
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Reports" {
       usecase "UC-022:\nAnalisis\nCuentas" as UC022
       usecase "Seleccionar\nCuenta" as SC
       usecase "Ver\nTendencias" as VT
       usecase "Ver\nGraficos" as VG
       usecase "Detectar\nAnomalias" as DA
       usecase "Exportar" as EX
   }

   ANA --> UC022
   UC022 ..> SC : <<include>>
   UC022 ..> VT : <<include>>
   UC022 ..> VG : <<include>>
   UC022 ..> DA : <<extends>>
   UC022 ..> EX : <<extends>>
   UC022 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion RPT-006 (Analisis de Cuentas)
2. Usuario tiene segmentos asignados
3. Cuenta seleccionada tiene movimientos

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Reportes > Analisis de Cuentas".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Analisis generado con metricas y graficos
2. Tendencias calculadas
3. Anomalias identificadas (si existen)
4. Evento REPORT_GENERATED registrado

----

5. Flujo Normal
---------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a Analisis de Cuentas
     -
   * - 2
     -
     - Verifica permiso RPT-006
   * - 3
     -
     - Carga lista de cuentas disponibles
   * - 4
     - Selecciona cuenta a analizar
     -
   * - 5
     - Selecciona rango de fechas
     -
   * - 6
     - Presiona "Analizar"
     -
   * - 7
     -
     - Obtiene movimientos de la cuenta
   * - 8
     -
     - Calcula metricas estadisticas
   * - 9
     -
     - Genera series temporales mensuales
   * - 10
     -
     - Detecta anomalias (desviaciones)
   * - 11
     -
     - Genera graficos de tendencia
   * - 12
     -
     - Muestra dashboard de analisis
   * - 13
     -
     - Registra en auditoria

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-022 Analisis Cuentas
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Analista" as U
   participant "Frontend" as FE #E3F2FD
   participant "ReportController" as RC #E8F5E9
   participant "AnalysisService" as AS #E8F5E9
   participant "StatService" as ST #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Analisis
   FE -> RC: 2. GET /api/reports/analysis/accounts
   RC -> DB: SELECT * FROM cuentas
   RC --> FE: 3. [cuentas]

   FE --> U: 4. Lista de cuentas

   U -> FE: 5. Selecciona cuenta y periodo
   FE -> RC: 6. POST /api/reports/analysis\n{cuenta, fechaDesde, fechaHasta}
   activate RC

   RC -> AS: 7. analyzeAccount(cuenta, periodo)
   activate AS

   AS -> DB: 8. SELECT * FROM movimientos\nWHERE cuenta = ?\nAND fecha BETWEEN ? AND ?
   DB --> AS: [movimientos]

   AS -> ST: 9. calculateStats(movimientos)
   activate ST
   ST -> ST: 10. min, max, avg, stdDev
   ST --> AS: {stats}
   deactivate ST

   AS -> AS: 11. groupByMonth()
   note right: Series temporales

   AS -> ST: 12. detectAnomalies(data, stdDev)
   ST --> AS: [anomalias]
   note right: Valores > 2*stdDev

   AS -> AS: 13. generateChartData()

   AS -> AUD: 14. logEvent(REPORT_GENERATED)
   AUD -> DB: INSERT audit_log

   AS --> RC: 15. {stats, timeSeries,\nanomalies, chartData}
   deactivate AS

   RC --> FE: 16. 200 OK {analysis}
   deactivate RC

   FE --> U: 17. Dashboard de analisis con graficos
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Exportar Analisis
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario solicita exportar

Genera PDF con graficos incluidos o Excel con datos.

7.2 FA-2: Comparar con Otra Cuenta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario activa comparativo

Muestra dos cuentas lado a lado con metricas comparativas.

----

8. Excepciones
--------------

8.1 EX-1: Cuenta sin Movimientos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "La cuenta seleccionada no tiene movimientos en el periodo"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-022 Analisis Cuentas
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam activity {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
       DiamondBackgroundColor #FFF9C4
       DiamondBorderColor #F57C00
   }

   start
   :Accede a Analisis de Cuentas;
   :Verificar permiso RPT-006;

   if (Tiene permiso?) then (si)
       :Cargar cuentas disponibles;
       :Usuario selecciona cuenta;
       :Usuario selecciona periodo;

       :Obtener movimientos;

       if (Hay movimientos?) then (si)
           fork
               :Calcular estadisticas;
               note right: min, max, avg, stdDev
           fork again
               :Generar series mensuales;
           fork again
               :Detectar anomalias;
           end fork

           :Generar graficos;

           if (Hay anomalias?) then (si)
               #FFE0B2:Resaltar anomalias;
           else (no)
           endif

           :Mostrar dashboard analisis;
           #C8E6C9:Registrar auditoria;

       else (no)
           #FFE0B2:Sin movimientos;
       endif
       stop
   else (no)
       #FFCDD2:403 Forbidden;
       stop
   endif
   @enduml

----

10. Reglas de Negocio
---------------------

.. list-table::
   :widths: 12 25 63
   :header-rows: 1

   * - BR
     - Nombre
     - Aplicacion
   * - BR_008
     - Auditoria
     - Generacion registrada
   * - BR_009
     - Segmentacion
     - Solo centros del usuario
   * - BR_014
     - Anomalias
     - Valores > 2 desviaciones estandar

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-022.01
     - Verificar permiso RPT-006
   * - FR-022.02
     - Aplicar segmentacion (BR_009)
   * - FR-022.03
     - Permitir seleccionar cuenta especifica
   * - FR-022.04
     - Calcular estadisticas (min, max, promedio, desviacion)
   * - FR-022.05
     - Generar series temporales mensuales
   * - FR-022.06
     - Detectar y resaltar anomalias
   * - FR-022.07
     - Generar graficos de tendencia
   * - FR-022.08
     - Permitir comparar dos cuentas
   * - FR-022.09
     - Exportar a PDF con graficos

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-002
   * - **BR Aplicables**
     - BR_008, BR_009, BR_014
   * - **FR Derivados**
     - FR-022.01 a FR-022.09
   * - **Funcion RBAC**
     - RPT-006

----

13. Historial de Cambios
------------------------

.. list-table::
   :widths: 12 12 76
   :header-rows: 1

   * - Version
     - Fecha
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Version con PlantUML embebido. 3 diagramas.