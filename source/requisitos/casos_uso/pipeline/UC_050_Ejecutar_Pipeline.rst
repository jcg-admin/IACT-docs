.. meta::
   :artefacto: UC_050
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/pipeline
   :modulo: MOD_Pipeline
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-050:

==============================================================================
UC-050: Ejecutar Pipeline de Datos
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
     - UC-050
   * - **Nombre**
     - Ejecutar Pipeline de Datos
   * - **Actor Primario**
     - Administrador de Datos / Sistema (Scheduler)
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Pipeline
   * - **Complejidad**
     - Alta
   * - **Prioridad**
     - Critica
   * - **BReq Origen**
     - BReq-001: Automatizacion del Procesamiento

----

2. Descripcion
--------------

Permite ejecutar el pipeline ETL de datos contables que procesa archivos
desde el directorio de entrada, los transforma segun reglas de negocio,
y carga los resultados en la base de datos para reportes. El pipeline
puede ejecutarse manualmente o programado (BR_001).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-050 Ejecutar Pipeline
   :align: center
   :scale: 90%

   @startuml
   left to right direction
   skinparam actorStyle awesome
   skinparam backgroundColor #FAFAFA
   skinparam usecase {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
       BorderThickness 2
   }

   actor "Administrador\nDatos" as ADM
   actor "Scheduler\n(Cron)" as SCH #LightGray
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Pipeline" {
       usecase "UC-050:\nEjecutar\nPipeline" as UC050
       usecase "Validar\nArchivos" as VA
       usecase "Transformar\nDatos" as TD
       usecase "Cargar\nBD" as CBD
       usecase "Registrar\nEvento" as RE
       usecase "UC-051:\nMonitorear" as UC051
   }

   ADM --> UC050 : manual
   SCH --> UC050 : programado
   UC050 ..> VA : <<include>>
   UC050 ..> TD : <<include>>
   UC050 ..> CBD : <<include>>
   UC050 ..> RE : <<include>>
   UC050 .> UC051 : <<extends>>
   UC050 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Si manual: Usuario tiene funcion PIP-001 (Ejecutar Pipeline)
2. Archivos de entrada disponibles en directorio configurado
3. No hay otra ejecucion del mismo pipeline en curso

4.2 Trigger
^^^^^^^^^^^

- Manual: Usuario hace clic en "Ejecutar Pipeline"
- Automatico: Scheduler dispara segun programacion (BR_001)

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Datos procesados y cargados en tablas destino
2. Archivos movidos a directorio de procesados
3. Evento PIPELINE_EXECUTED registrado (BR_008)
4. Metricas de ejecucion disponibles

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Errores no corrompen datos existentes (transaccional)
2. Archivos con error se mueven a directorio de errores
3. Log detallado de cada paso disponible

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
     - Inicia ejecucion de pipeline
     -
   * - 2
     -
     - Verifica no hay ejecucion en curso
   * - 3
     -
     - Crea registro de ejecucion (status=RUNNING)
   * - 4
     -
     - Escanea directorio de entrada
   * - 5
     -
     - Valida formato y estructura de archivos
   * - 6
     -
     - Inicia transaccion de BD
   * - 7
     -
     - Transforma datos segun reglas
   * - 8
     -
     - Carga datos en tablas destino
   * - 9
     -
     - Commit de transaccion
   * - 10
     -
     - Mueve archivos a /procesados
   * - 11
     -
     - Actualiza status=COMPLETED
   * - 12
     -
     - Registra PIPELINE_EXECUTED (BR_008)
   * - 13
     -
     - Notifica finalizacion

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-050 Ejecutar Pipeline
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center
   skinparam participant {
       BackgroundColor #E8F5E9
       BorderColor #388E3C
   }
   skinparam database {
       BackgroundColor #FFF3E0
       BorderColor #F57C00
   }

   actor "Admin/Scheduler" as ACT
   participant "Frontend/Cron" as FE #E3F2FD
   participant "PipelineController" as PC #E8F5E9
   participant "PipelineService" as PS #E8F5E9
   participant "ETLEngine" as ETL #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0
   collections "FileSystem" as FS #ECEFF1

   ACT -> FE: 1. Ejecutar Pipeline
   FE -> PC: 2. POST /api/pipeline/execute
   activate PC

   PC -> PS: 3. execute()
   activate PS

   PS -> DB: 4. SELECT * FROM pipeline_runs\nWHERE status='RUNNING'
   DB --> PS: [] (ninguno en curso)

   PS -> DB: 5. INSERT INTO pipeline_runs\n(status='RUNNING', started_at)
   DB --> PS: {runId}

   PS -> FS: 6. scanDirectory(/input)
   FS --> PS: [file1.csv, file2.csv]

   PS -> ETL: 7. validateFiles(files)
   activate ETL
   ETL -> ETL: 8. Validar formato, headers
   ETL --> PS: {valid: true}

   PS -> DB: 9. BEGIN TRANSACTION

   loop Para cada archivo
       ETL -> FS: 10. readFile(file)
       FS --> ETL: {data}

       ETL -> ETL: 11. transform(data, rules)
       note right: Aplica reglas de\nnegocio y mapeos

       ETL -> DB: 12. INSERT/UPDATE datos
   end

   PS -> DB: 13. COMMIT
   deactivate ETL

   PS -> FS: 14. moveFiles(/input -> /processed)

   PS -> DB: 15. UPDATE pipeline_runs\nSET status='COMPLETED',\nfinished_at, records_processed

   PS -> AUD: 16. logEvent(PIPELINE_EXECUTED,\n{runId, files, records})
   activate AUD
   AUD -> DB: INSERT audit_log
   note right: BR_008
   AUD --> PS: OK
   deactivate AUD

   PS --> PC: 17. {runId, status, metrics}
   deactivate PS

   PC --> FE: 18. 200 OK {execution}
   deactivate PC

   FE --> ACT: 19. "Pipeline completado\nX registros procesados"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Sin Archivos para Procesar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 4 del flujo normal

**Condicion:** Directorio de entrada vacio

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 4.1
     - Sistema detecta directorio vacio
   * - 4.2
     - Registra ejecucion con status=NO_DATA
   * - 4.3
     - Notifica "Sin archivos para procesar"

**Retorno:** Fin del caso de uso

7.2 FA-2: Error en Validacion de Archivo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 5 del flujo normal

**Condicion:** Archivo no cumple formato esperado

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 5.1
     - Sistema detecta error de formato
   * - 5.2
     - Mueve archivo a /errores con detalle
   * - 5.3
     - Continua con siguientes archivos
   * - 5.4
     - Al final, status=PARTIAL si hubo errores

**Retorno:** Paso 6 con archivos validos

7.3 FA-3: Error en Carga de Datos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 8 del flujo normal

**Condicion:** Error de BD durante INSERT/UPDATE

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 8.1
     - Sistema detecta error de BD
   * - 8.2
     - Ejecuta ROLLBACK de transaccion
   * - 8.3
     - Mueve archivos a /errores
   * - 8.4
     - Actualiza status=FAILED
   * - 8.5
     - Registra error detallado en log

**Retorno:** Fin del caso de uso (con error)

----

8. Excepciones
--------------

8.1 EX-1: Pipeline Ya en Ejecucion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Existe otra ejecucion con status=RUNNING

**Accion del Sistema:** Rechaza nueva ejecucion

**Mensaje al Usuario:** "Pipeline ya en ejecucion. Espere a que finalice."

8.2 EX-2: Sin Permiso de Ejecucion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario no tiene funcion PIP-001

**Accion del Sistema:** Retorna 403 Forbidden

**Mensaje al Usuario:** "No tiene permisos para ejecutar el pipeline"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-050 Ejecutar Pipeline
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

   :Solicita ejecucion de pipeline;

   if (Pipeline en curso?) then (si)
       #FFCDD2:Error: Ya en ejecucion;
       stop
   else (no)
   endif

   :Crear registro RUNNING;
   :Escanear directorio entrada;

   if (Hay archivos?) then (si)

       :Validar archivos;

       fork
           :Archivos validos;
       fork again
           :Archivos invalidos\n-> mover a /errores;
       end fork

       if (Hay archivos validos?) then (si)

           :BEGIN TRANSACTION;

           while (Mas archivos?) is (si)
               :Leer archivo;
               :Transformar datos;
               :Cargar en BD;

               if (Error?) then (si)
                   #FFCDD2:ROLLBACK;
                   :status = FAILED;
                   :Mover a /errores;
                   stop
               else (no)
               endif
           endwhile (no)

           :COMMIT;
           :Mover a /procesados;
           :status = COMPLETED;

       else (no)
           :status = FAILED;
       endif

   else (no)
       :status = NO_DATA;
   endif

   #C8E6C9:Registrar auditoria (BR_008);
   :Notificar resultado;

   stop
   @enduml

----

10. Reglas de Negocio
---------------------

.. list-table::
   :widths: 12 25 63
   :header-rows: 1

   * - BR
     - Nombre
     - Aplicacion en este UC
   * - BR_001
     - Automatizacion
     - Pipeline puede ejecutarse automaticamente via scheduler
   * - BR_008
     - Auditoria
     - PIPELINE_EXECUTED registra metricas de ejecucion

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-050.01
     - Sistema DEBE verificar permiso PIP-001 para ejecucion manual
   * - FR-050.02
     - Sistema DEBE impedir ejecucion concurrente del mismo pipeline
   * - FR-050.03
     - Sistema DEBE escanear directorio de entrada configurado
   * - FR-050.04
     - Sistema DEBE validar formato y estructura de archivos
   * - FR-050.05
     - Sistema DEBE transformar datos segun reglas configuradas
   * - FR-050.06
     - Sistema DEBE cargar datos en transaccion atomica
   * - FR-050.07
     - Sistema DEBE mover archivos procesados a /procesados
   * - FR-050.08
     - Sistema DEBE mover archivos con error a /errores
   * - FR-050.09
     - Sistema DEBE registrar metricas de ejecucion
   * - FR-050.10
     - Sistema DEBE registrar evento en auditoria (BR_008)
   * - FR-050.11
     - Sistema DEBE soportar ejecucion programada (scheduler)

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-001: Automatizacion del Procesamiento
   * - **BR Aplicables**
     - BR_001 (Automatizacion), BR_008 (Auditoria)
   * - **FR Derivados**
     - FR-050.01 a FR-050.11 (11 requerimientos)
   * - **UC Relacionados**
     - UC-051 (Monitorear), UC-052 (Configurar), UC-053 (Historial)
   * - **Actores RBAC**
     - AGR-003: admin_datos
   * - **Funciones RBAC**
     - PIP-001: Ejecutar Pipeline

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
     - Version con PlantUML embebido (Sphinx). 3 diagramas.