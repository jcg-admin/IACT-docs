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
     - Baja
   * - **Prioridad**
     - Media
   * - **BReq Origen**
     - BReq-001: Automatizacion del Procesamiento

----

2. Descripcion
--------------

Permite consultar el historial de ejecuciones del pipeline con filtros por
fecha, estado y tipo de ejecucion. Incluye metricas de cada ejecucion y
permite acceder al detalle de errores.

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
       usecase "Ver\nDetalle" as VD
       usecase "Exportar" as EX
   }

   ADM --> UC053
   AUD --> UC053
   UC053 ..> FF : <<include>>
   UC053 ..> FE : <<include>>
   UC053 ..> VD : <<extends>>
   UC053 ..> EX : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion PIP-005 (Consultar Historial)
2. Existen registros de ejecucion

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Historial de Pipeline".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Lista de ejecuciones mostrada segun filtros

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
     - Accede a Historial
     -
   * - 2
     -
     - Verifica permiso PIP-005
   * - 3
     -
     - Carga ultimas 50 ejecuciones
   * - 4
     -
     - Muestra tabla con metricas
   * - 5
     - (Opcional) Aplica filtros
     -
   * - 6
     -
     - Actualiza resultados
   * - 7
     - (Opcional) Clic en ejecucion
     -
   * - 8
     -
     - Muestra detalle con archivos y errores

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
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Historial
   FE -> PC: 2. GET /api/pipeline/runs?limit=50
   activate PC

   PC -> DB: 3. SELECT * FROM pipeline_runs\nORDER BY started_at DESC\nLIMIT 50
   DB --> PC: [runs]

   PC --> FE: 4. {runs, total}
   deactivate PC

   FE --> U: 5. Tabla de ejecuciones
   note right: Columnas: ID, Fecha,\nStatus, Duracion, Registros

   U -> FE: 6. Filtrar por FAILED
   FE -> PC: 7. GET /api/pipeline/runs?status=FAILED
   PC --> FE: 8. [failedRuns]
   FE --> U: 9. Solo ejecuciones fallidas

   U -> FE: 10. Clic en ejecucion #123
   FE -> PC: 11. GET /api/pipeline/runs/123
   activate PC

   PC -> DB: SELECT * FROM pipeline_runs WHERE id=123
   PC -> DB: SELECT * FROM pipeline_files WHERE run_id=123
   PC -> DB: SELECT * FROM pipeline_errors WHERE run_id=123

   PC --> FE: 12. {run, files, errors}
   deactivate PC

   FE --> U: 13. Modal con detalle completo
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Exportar Historial
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usuario puede exportar historial filtrado a CSV/Excel.

7.2 FA-2: Re-ejecutar desde Historial
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usuario con PIP-001 puede re-ejecutar una ejecucion fallida.

----

8. Excepciones
--------------

8.1 EX-1: Sin Historial
^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay ejecuciones registradas"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-053 Historial Pipeline
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start

   :Accede a Historial;
   :Verificar permiso PIP-005;

   if (Tiene permiso?) then (si)
       :Cargar ultimas 50 ejecuciones;
       :Mostrar tabla;

       while (Usuario interactua?) is (si)
           split
               :Filtrar por fecha;
           split again
               :Filtrar por estado;
           split again
               :Ver detalle ejecucion;
               :Mostrar archivos y errores;
           split again
               :Exportar a CSV/Excel;
           end split

           :Actualizar vista;
       endwhile (no)

       stop
   else (no)
       #FFCDD2:403 Forbidden;
       stop
   endif
   @enduml

----

10. Reglas de Negocio
---------------------

No aplica BR especificas (solo consulta).

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-053.01
     - Verificar permiso PIP-005
   * - FR-053.02
     - Listar ejecuciones con paginacion
   * - FR-053.03
     - Mostrar: ID, fecha, status, duracion, registros
   * - FR-053.04
     - Filtrar por rango de fechas
   * - FR-053.05
     - Filtrar por estado (COMPLETED, FAILED, CANCELLED)
   * - FR-053.06
     - Ver detalle con archivos procesados
   * - FR-053.07
     - Ver detalle de errores por archivo
   * - FR-053.08
     - Exportar historial a CSV/Excel

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-001
   * - **FR Derivados**
     - FR-053.01 a FR-053.08
   * - **UC Relacionados**
     - UC-050, UC-051
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
     - Version con PlantUML embebido (Sphinx)
