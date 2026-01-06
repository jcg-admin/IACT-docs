.. meta::
   :artefacto: UC_028
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-028:

==============================================================================
UC-028: Ver Dashboard Operativo
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
     - UC-028
   * - **Nombre**
     - Ver Dashboard Operativo
   * - **Actor Primario**
     - Gerente de Operaciones / Controller
   * - **Actores Secundarios**
     - Ninguno
   * - **Modulo**
     - MOD_Reports
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Media
   * - **BReq Origen**
     - BReq-003: Visualizacion de Indicadores

----

2. Descripcion
--------------

Muestra dashboard con indicadores operativos: estado del pipeline ETL,
cantidad de registros procesados, errores de procesamiento, tiempos
de ejecucion y estado de alertas. Incluye monitoreo en tiempo real.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-028 Dashboard Operativo
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

   actor "Gerente\nOperaciones" as GOP
   actor "Controller" as CTR

   rectangle "MOD_Reports" {
       usecase "UC-028:\nDashboard\nOperativo" as UC028
       usecase "Ver Estado\nPipeline" as VEP
       usecase "Ver\nErrores" as VER
       usecase "Ver\nTiempos" as VT
       usecase "Ver\nAlertas" as VA
   }

   GOP --> UC028
   CTR --> UC028
   UC028 ..> VEP : <<include>>
   UC028 ..> VER : <<include>>
   UC028 ..> VT : <<include>>
   UC028 ..> VA : <<include>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion DSH-003 (Dashboard Operativo)
2. Existen datos de ejecucion del sistema

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Dashboard > Operativo".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Dashboard renderizado con metricas operativas
2. Estado actual del pipeline visible
3. Alertas activas mostradas

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
     - Accede a Dashboard Operativo
     -
   * - 2
     -
     - Verifica permiso DSH-003
   * - 3
     -
     - Obtiene estado actual del pipeline
   * - 4
     -
     - Obtiene estadisticas de procesamiento
   * - 5
     -
     - Obtiene errores recientes
   * - 6
     -
     - Obtiene alertas activas
   * - 7
     -
     - Renderiza dashboard con widgets
   * - 8
     - Visualiza metricas operativas
     -
   * - 9
     -
     - Auto-refresh cada 30 segundos

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-028 Dashboard Operativo
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   actor "Gerente" as U
   participant "Frontend" as FE #E3F2FD
   participant "DashboardController" as DC #E8F5E9
   participant "PipelineService" as PS #E8F5E9
   participant "AlertService" as AS #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Dashboard Operativo
   FE -> DC: 2. GET /api/dashboard/operations
   activate DC

   DC -> PS: 3. getPipelineStatus()
   activate PS
   PS -> DB: SELECT * FROM pipeline_runs\nORDER BY started_at DESC LIMIT 1
   PS --> DC: {status, lastRun}
   deactivate PS

   DC -> PS: 4. getProcessingStats()
   activate PS
   PS -> DB: SELECT COUNT(*), SUM(records)\nFROM pipeline_runs\nWHERE fecha >= today - 7
   PS --> DC: {runs, totalRecords, avgTime}
   deactivate PS

   DC -> PS: 5. getRecentErrors()
   PS -> DB: SELECT * FROM pipeline_errors LIMIT 10
   PS --> DC: [errors]

   DC -> AS: 6. getActiveAlerts()
   activate AS
   AS -> DB: SELECT * FROM alerts\nWHERE status = 'ACTIVE'
   AS --> DC: [alerts]
   deactivate AS

   DC --> FE: 7. {pipeline, stats, errors, alerts}
   deactivate DC

   FE --> U: 8. Dashboard con widgets

   loop Cada 30 segundos
       FE -> DC: 9. GET /api/dashboard/operations/refresh
       DC --> FE: 10. {updated data}
       FE --> U: 11. Actualiza UI
   end
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Acceder a Detalle de Error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usuario hace clic en error para ver detalle completo.

7.2 FA-2: Ejecutar Pipeline Manual
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usuario con permiso puede iniciar ejecucion desde dashboard.

----

8. Excepciones
--------------

8.1 EX-1: Sin Ejecuciones
^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay ejecuciones de pipeline registradas"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-028 Dashboard Operativo
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso DSH-003;

   fork
       :Obtener estado pipeline;
       if (Pipeline RUNNING?) then (si)
           #FFF9C4:Mostrar progreso;
       else (no)
           :Mostrar ultimo estado;
       endif
   fork again
       :Obtener estadisticas 7 dias;
       :Calcular promedios;
   fork again
       :Obtener errores recientes;
   fork again
       :Obtener alertas activas;
   end fork

   :Renderizar dashboard;

   while (Usuario en dashboard?) is (si)
       :Esperar 30 segundos;
       :Refresh automatico;
   endwhile (no)
   stop
   @enduml

----

10. Reglas de Negocio
---------------------

No aplica BR especificas (dashboard de monitoreo).

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-028.01
     - Verificar permiso DSH-003
   * - FR-028.02
     - Mostrar estado actual del pipeline
   * - FR-028.03
     - Mostrar registros procesados (7 dias)
   * - FR-028.04
     - Mostrar tiempo promedio de ejecucion
   * - FR-028.05
     - Mostrar errores recientes
   * - FR-028.06
     - Mostrar alertas activas
   * - FR-028.07
     - Auto-refresh cada 30 segundos
   * - FR-028.08
     - Permitir acceso a detalle de errores

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-003
   * - **FR Derivados**
     - FR-028.01 a FR-028.08
   * - **UC Relacionados**
     - UC-050, UC-051 (Pipeline)
   * - **Funcion RBAC**
     - DSH-003

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
