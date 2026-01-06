.. meta::
   :artefacto: UC_053
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/pipeline
   :modulo: MOD_Pipeline
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-053:

==============================================================================
UC-053: Consultar Historial de Ejecuciones
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
     - UC-053
   * - **Nombre**
     - Consultar Historial de Ejecuciones
   * - **Actor Primario**
     - Administrador de Datos / Auditor
   * - **Actores Secundarios**
     - Ninguno
   * - **Modulo**
     - MOD_Pipeline
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Media
   * - **BReq Origen**
     - BReq-001: Automatizacion del Procesamiento

----

2. Descripcion
--------------

Permite consultar el historial completo de ejecuciones del pipeline con
filtros avanzados por fecha, estado, tipo de ejecucion y resultado.
Muestra metricas detalladas de cada ejecucion, permite acceder al
detalle de archivos procesados y errores, y exportar el historial
para auditorias externas.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-053 Historial Pipeline
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

   actor "Administrador\nDatos" as ADM
   actor "Auditor" as AUD

   rectangle "MOD_Pipeline" {
       usecase "UC-053:\nHistorial\nEjecuciones" as UC053
       usecase "Filtrar por\nFecha" as FF
       usecase "Filtrar por\nEstado" as FE
       usecase "Ver Detalle\nEjecucion" as VDE
       usecase "Ver Archivos\nProcesados" as VAP
       usecase "Ver Errores" as VER
       usecase "Exportar\nHistorial" as EH
       usecase "Re-ejecutar\nFallido" as REF
   }

   ADM --> UC053
   AUD --> UC053
   UC053 ..> FF : <<include>>
   UC053 ..> FE : <<include>>
   UC053 ..> VDE : <<extends>>
   UC053 ..> VAP : <<extends>>
   UC053 ..> VER : <<extends>>
   UC053 ..> EH : <<extends>>
   UC053 ..> REF : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion PIP-005 (Consultar Historial)
2. Existen registros de ejecucion en pipeline_runs

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Historial de Pipeline" desde menu.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Lista de ejecuciones mostrada segun filtros aplicados
2. Metricas agregadas calculadas (totales, promedios)

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
     - Accede a Historial de Pipeline
     -
   * - 2
     -
     - Verifica permiso PIP-005
   * - 3
     -
     - Carga ultimas 50 ejecuciones (default)
   * - 4
     -
     - Calcula metricas agregadas
   * - 5
     -
     - Muestra tabla con paginacion
   * - 6
     - (Opcional) Aplica filtro por fecha
     -
   * - 7
     -
     - Actualiza resultados
   * - 8
     - (Opcional) Aplica filtro por estado
     -
   * - 9
     -
     - Actualiza resultados
   * - 10
     - (Opcional) Clic en fila de ejecucion
     -
   * - 11
     -
     - Muestra detalle en panel lateral
   * - 12
     - (Opcional) Expande archivos procesados
     -
   * - 13
     -
     - Lista archivos con metricas individuales
   * - 14
     - (Opcional) Expande errores
     -
   * - 15
     -
     - Muestra errores con detalle y linea

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-053 Historial Pipeline
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin/Auditor" as U
   participant "Frontend" as FE #E3F2FD
   participant "PipelineController" as PC #E8F5E9
   participant "HistoryService" as HS #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Historial
   FE -> PC: 2. GET /api/pipeline/runs?limit=50
   activate PC

   PC -> HS: 3. getRuns(filters)
   activate HS

   HS -> DB: 4. SELECT id, started_at, finished_at,\nstatus, files_processed, records_processed,\nerror_count\nFROM pipeline_runs\nORDER BY started_at DESC\nLIMIT 50
   DB --> HS: [runs]

   HS -> DB: 5. SELECT status, COUNT(*) as count,\nAVG(duration) as avgDuration\nFROM pipeline_runs\nGROUP BY status
   DB --> HS: [aggregates]

   HS --> PC: 6. {runs, aggregates, total}
   deactivate HS

   PC --> FE: 7. 200 OK {history}
   deactivate PC

   FE --> U: 8. Tabla de ejecuciones\n+ Metricas agregadas
   note right
       Columnas:
       ID | Fecha | Estado | Duracion
       Archivos | Registros | Errores
   end note

   U -> FE: 9. Aplica filtro: status=FAILED
   FE -> PC: 10. GET /api/pipeline/runs?status=FAILED
   PC --> FE: 11. [failedRuns]
   FE --> U: 12. Solo ejecuciones fallidas

   U -> FE: 13. Clic en ejecucion #123
   FE -> PC: 14. GET /api/pipeline/runs/123
   activate PC

   PC -> DB: 15. SELECT * FROM pipeline_runs\nWHERE id = 123
   PC -> DB: 16. SELECT * FROM pipeline_files\nWHERE run_id = 123
   PC -> DB: 17. SELECT * FROM pipeline_errors\nWHERE run_id = 123

   PC --> FE: 18. {run, files, errors, log}
   deactivate PC

   FE --> U: 19. Panel lateral con detalle completo

   opt Exportar
       U -> FE: 20. Clic "Exportar CSV"
       FE -> PC: 21. GET /api/pipeline/runs/export?format=csv&filters=...
       PC --> FE: 22. CSV file
       FE --> U: 23. Descarga historial.csv
   end

   opt Re-ejecutar fallido
       U -> FE: 24. Clic "Re-ejecutar" (requiere PIP-001)
       FE -> PC: 25. POST /api/pipeline/runs/123/retry
       note right: Copia archivos de\n/errors a /input\ny ejecuta
       PC --> FE: 26. {newRunId}
       FE --> U: 27. Redirige a Monitor
   end
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Exportar a Excel
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario selecciona formato Excel

Genera archivo XLSX con formato y graficos incluidos.

7.2 FA-2: Re-ejecutar Ejecucion Fallida
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 10 del flujo normal

**Condicion:** Usuario con PIP-001 selecciona ejecucion FAILED

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 10.1
     - Usuario hace clic en "Re-ejecutar"
   * - 10.2
     - Sistema solicita confirmacion
   * - 10.3
     - Sistema copia archivos de /errors/{fecha} a /input
   * - 10.4
     - Sistema inicia nueva ejecucion (UC-050)
   * - 10.5
     - Redirige a Monitor (UC-051)

**Retorno:** UC-051

7.3 FA-3: Comparar Ejecuciones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario selecciona dos ejecuciones

Muestra comparativo lado a lado de metricas.

7.4 FA-4: Ver Tendencias
^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario activa vista de tendencias

Muestra graficos de tendencia: ejecuciones por dia, tasa de exito, tiempo promedio.

----

8. Excepciones
--------------

8.1 EX-1: Sin Historial
^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** No existen registros en pipeline_runs

**Mensaje:** "No hay ejecuciones de pipeline registradas. Ejecute el pipeline para comenzar."

8.2 EX-2: Ejecucion No Encontrada
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** ID de ejecucion no existe

**Mensaje:** "La ejecucion #XXX no fue encontrada."

**Codigo HTTP:** 404 Not Found

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-053 Historial Pipeline
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

   :Accede a Historial;
   :Verificar permiso PIP-005;

   if (Tiene permiso?) then (si)
       :Cargar ultimas 50 ejecuciones;
       :Calcular metricas agregadas;
       :Mostrar tabla paginada;

       while (Usuario interactua?) is (si)
           split
               :Filtrar por fecha;
               :Actualizar resultados;
           split again
               :Filtrar por estado;
               :Actualizar resultados;
           split again
               :Ver detalle ejecucion;
               :Mostrar panel lateral;

               fork
                   :Ver archivos procesados;
               fork again
                   :Ver errores;
               fork again
                   :Descargar log;
               end fork

           split again
               :Exportar historial;
               if (Formato?) then (CSV)
                   :Generar CSV;
               else (Excel)
                   :Generar XLSX;
               endif
               :Descargar archivo;

           split again
               :Re-ejecutar fallido;
               if (Tiene PIP-001?) then (si)
                   :Copiar archivos a /input;
                   :Iniciar nueva ejecucion;
                   :Ir a Monitor (UC-051);
                   stop
               else (no)
                   #FFCDD2:Sin permiso;
               endif

           split again
               :Ver tendencias;
               :Generar graficos;
           end split

       endwhile (Salir)

       stop
   else (no)
       #FFCDD2:403 Forbidden;
       stop
   endif
   @enduml

----

10. Reglas de Negocio
---------------------

No aplica BR especificas (caso de uso de consulta).

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-053.01
     - Sistema DEBE verificar permiso PIP-005
   * - FR-053.02
     - Sistema DEBE listar ejecuciones con paginacion (50 por pagina)
   * - FR-053.03
     - Sistema DEBE mostrar: ID, fecha, estado, duracion, archivos, registros, errores
   * - FR-053.04
     - Sistema DEBE calcular metricas agregadas (totales, promedios, tasas)
   * - FR-053.05
     - Sistema DEBE filtrar por rango de fechas
   * - FR-053.06
     - Sistema DEBE filtrar por estado (COMPLETED, FAILED, CANCELLED, PARTIAL)
   * - FR-053.07
     - Sistema DEBE filtrar por tipo (manual, programado)
   * - FR-053.08
     - Sistema DEBE mostrar detalle de ejecucion con archivos y errores
   * - FR-053.09
     - Sistema DEBE permitir descargar log de ejecucion
   * - FR-053.10
     - Sistema DEBE exportar historial a CSV
   * - FR-053.11
     - Sistema DEBE exportar historial a Excel con formato
   * - FR-053.12
     - Sistema DEBE permitir re-ejecutar ejecucion fallida (requiere PIP-001)
   * - FR-053.13
     - Sistema DEBE mostrar graficos de tendencia

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-001
   * - **FR Derivados**
     - FR-053.01 a FR-053.13 (13 requerimientos)
   * - **UC Relacionados**
     - UC-050 (re-ejecutar), UC-051 (monitor post re-ejecucion)
   * - **Funcion RBAC**
     - PIP-005: Consultar Historial

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
     - Version completa con PlantUML. Re-ejecucion. Tendencias. Exportacion.
