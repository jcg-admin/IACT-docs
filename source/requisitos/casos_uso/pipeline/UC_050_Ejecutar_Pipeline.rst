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
     - Administrador de Datos
   * - **Actores Secundarios**
     - Scheduler (Cron), Sistema de Auditoria
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

Permite ejecutar el pipeline ETL (Extract-Transform-Load) de datos contables
que procesa archivos desde el directorio de entrada, aplica transformaciones
segun reglas de negocio configuradas, valida integridad de datos y carga
los resultados en la base de datos para reportes. Soporta ejecucion manual
por usuario autorizado o programada automaticamente via scheduler (BR_001).
Implementa procesamiento transaccional con rollback en caso de error.

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
       usecase "Escanear\nDirectorio" as ED
       usecase "Validar\nArchivos" as VA
       usecase "Transformar\nDatos" as TD
       usecase "Cargar\nBase Datos" as CBD
       usecase "Mover\nProcesados" as MP
       usecase "Registrar\nEvento" as RE
       usecase "UC-051:\nMonitorear" as UC051
   }

   ADM --> UC050 : ejecuta manual
   SCH --> UC050 : ejecuta programado
   UC050 ..> ED : <<include>>
   UC050 ..> VA : <<include>>
   UC050 ..> TD : <<include>>
   UC050 ..> CBD : <<include>>
   UC050 ..> MP : <<include>>
   UC050 ..> RE : <<include>>
   UC050 .> UC051 : <<extends>>
   UC050 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Si ejecucion manual: Usuario tiene funcion PIP-001 (Ejecutar Pipeline)
2. Archivos de entrada disponibles en directorio configurado (/data/input)
3. No existe otra ejecucion del mismo pipeline en curso (status=RUNNING)
4. Configuracion del pipeline validada y activa
5. Conexion a base de datos disponible

4.2 Trigger
^^^^^^^^^^^

- **Manual:** Usuario hace clic en "Ejecutar Pipeline" desde interfaz
- **Automatico:** Scheduler dispara segun expresion cron configurada (BR_001)

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Datos procesados y cargados en tablas destino
2. Archivos procesados movidos a /data/processed/{fecha}/
3. Archivos con error movidos a /data/errors/{fecha}/
4. Registro de ejecucion con status=COMPLETED
5. Metricas de ejecucion registradas (tiempo, registros, errores)
6. Evento PIPELINE_EXECUTED registrado en auditoria (BR_008)

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Errores no corrompen datos existentes (transaccion atomica)
2. Archivos originales preservados en caso de fallo
3. Log detallado de cada paso disponible para diagnostico
4. Estado del pipeline siempre consistente

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
     - Inicia ejecucion de pipeline (manual o scheduler)
     -
   * - 2
     -
     - Verifica permiso PIP-001 (si manual)
   * - 3
     -
     - Verifica no hay ejecucion en curso
   * - 4
     -
     - Crea registro pipeline_runs (status=RUNNING)
   * - 5
     -
     - Escanea directorio /data/input
   * - 6
     -
     - Filtra archivos por patron configurado (*.csv)
   * - 7
     -
     - Valida formato y estructura de cada archivo
   * - 8
     -
     - Inicia transaccion de base de datos
   * - 9
     -
     - Por cada archivo valido: lee, transforma, carga
   * - 10
     -
     - Ejecuta validaciones de integridad
   * - 11
     -
     - Commit de transaccion
   * - 12
     -
     - Mueve archivos procesados a /data/processed/
   * - 13
     -
     - Actualiza registro (status=COMPLETED, metricas)
   * - 14
     -
     - Registra evento PIPELINE_EXECUTED (BR_008)
   * - 15
     -
     - Envia notificacion de finalizacion (si configurado)

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
   participant "ValidationService" as VS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0
   collections "FileSystem" as FS #ECEFF1

   ACT -> FE: 1. Ejecutar Pipeline
   FE -> PC: 2. POST /api/pipeline/execute
   activate PC

   PC -> PS: 3. checkRunning()
   PS -> DB: SELECT * FROM pipeline_runs\nWHERE status='RUNNING'
   DB --> PS: [] (ninguno activo)

   PC -> PS: 4. execute()
   activate PS

   PS -> DB: 5. INSERT INTO pipeline_runs\n(status='RUNNING', started_at=NOW())
   DB --> PS: {runId: 123}

   PS -> FS: 6. scanDirectory(/data/input, '*.csv')
   FS --> PS: [file1.csv, file2.csv, file3.csv]

   PS -> VS: 7. validateFiles(files)
   activate VS
   loop Para cada archivo
       VS -> VS: checkFormat()
       VS -> VS: checkHeaders()
       VS -> VS: checkEncoding()
   end
   VS --> PS: {valid: [f1,f2], invalid: [f3]}
   deactivate VS

   PS -> FS: 8. moveToErrors(invalidFiles)

   PS -> DB: 9. BEGIN TRANSACTION
   activate ETL

   loop Para cada archivo valido
       PS -> ETL: 10. process(file)
       ETL -> FS: 11. readFile(file)
       FS --> ETL: {rawData}

       ETL -> ETL: 12. transform(rawData, rules)
       note right
           Aplica reglas:
           - Mapeo de campos
           - Conversiones
           - Calculos
       end note

       ETL -> DB: 13. INSERT/UPDATE datos_contables
       DB --> ETL: {rowsAffected}

       PS -> PS: 14. updateProgress(file, rows)
   end
   deactivate ETL

   PS -> VS: 15. validateIntegrity()
   VS -> DB: SELECT SUM(debito), SUM(credito)
   VS --> PS: {balanced: true}

   PS -> DB: 16. COMMIT

   PS -> FS: 17. moveFiles(/input -> /processed/{date})

   PS -> DB: 18. UPDATE pipeline_runs\nSET status='COMPLETED',\nfinished_at=NOW(),\nrecords_processed=X,\nfiles_processed=Y

   PS -> AUD: 19. logEvent('PIPELINE_EXECUTED',\n{runId, files, records, duration})
   activate AUD
   AUD -> DB: INSERT INTO audit_log
   note right: BR_008
   AUD --> PS: OK
   deactivate AUD

   PS --> PC: 20. {runId, status: 'COMPLETED',\nmetrics: {...}}
   deactivate PS

   PC --> FE: 21. 200 OK {execution}
   deactivate PC

   FE --> ACT: 22. "Pipeline completado exitosamente\n3 archivos, 1,500 registros en 45s"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Directorio de Entrada Vacio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 5 del flujo normal

**Condicion:** No hay archivos en /data/input que coincidan con patron

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 5.1
     - Sistema detecta directorio vacio o sin archivos validos
   * - 5.2
     - Actualiza registro con status=NO_DATA
   * - 5.3
     - Registra evento informativo en auditoria
   * - 5.4
     - Notifica "Sin archivos para procesar"

**Retorno:** Fin del caso de uso (exito sin datos)

7.2 FA-2: Archivo con Formato Invalido
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 7 del flujo normal

**Condicion:** Archivo no cumple formato esperado (headers, encoding, estructura)

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 7.1
     - ValidationService detecta error de formato
   * - 7.2
     - Registra detalle del error (linea, campo, valor)
   * - 7.3
     - Mueve archivo a /data/errors/{fecha}/ con log adjunto
   * - 7.4
     - Continua procesando archivos restantes
   * - 7.5
     - Al finalizar, status=PARTIAL_SUCCESS si hubo errores

**Retorno:** Paso 8 con archivos validos restantes

7.3 FA-3: Error Durante Transformacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 12 del flujo normal

**Condicion:** Error en regla de transformacion o datos invalidos

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 12.1
     - ETLEngine detecta error de transformacion
   * - 12.2
     - Registra linea y detalle del error
   * - 12.3
     - Segun configuracion: salta linea o falla archivo completo
   * - 12.4
     - Si falla archivo: rollback parcial y mover a errores

**Retorno:** Continua con siguiente registro/archivo

7.4 FA-4: Error de Base de Datos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 13 del flujo normal

**Condicion:** Error de constraint, conexion o espacio en BD

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 13.1
     - Sistema detecta error de base de datos
   * - 13.2
     - Ejecuta ROLLBACK de transaccion completa
   * - 13.3
     - Preserva archivos en /data/input (no procesados)
   * - 13.4
     - Actualiza status=FAILED con mensaje de error
   * - 13.5
     - Envia alerta a administradores

**Retorno:** Fin del caso de uso (fallo)

7.5 FA-5: Validacion de Integridad Fallida
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 15 del flujo normal

**Condicion:** Suma de debitos != suma de creditos

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 15.1
     - Sistema detecta descuadre contable
   * - 15.2
     - Ejecuta ROLLBACK
   * - 15.3
     - Registra detalle del descuadre
   * - 15.4
     - status=FAILED, motivo="Descuadre contable"

**Retorno:** Fin del caso de uso (fallo)

----

8. Excepciones
--------------

8.1 EX-1: Pipeline Ya en Ejecucion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Existe registro con status=RUNNING para este pipeline

**Accion del Sistema:** Rechaza nueva ejecucion inmediatamente

**Mensaje al Usuario:** "Pipeline ya en ejecucion (ID: XXX). Espere a que finalice o cancele la ejecucion actual."

**Codigo HTTP:** 409 Conflict

8.2 EX-2: Sin Permiso de Ejecucion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario no tiene funcion PIP-001 asignada

**Accion del Sistema:** Rechaza solicitud

**Mensaje al Usuario:** "No tiene permisos para ejecutar el pipeline. Contacte al administrador."

**Codigo HTTP:** 403 Forbidden

8.3 EX-3: Configuracion Invalida
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Pipeline no tiene configuracion activa o esta incompleta

**Accion del Sistema:** Rechaza ejecucion

**Mensaje al Usuario:** "El pipeline no esta configurado correctamente. Revise la configuracion."

**Codigo HTTP:** 400 Bad Request

8.4 EX-4: Sistema de Archivos No Disponible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Directorio /data/input no accesible

**Accion del Sistema:** Falla con error de sistema

**Mensaje al Usuario:** "Error de acceso al sistema de archivos. Contacte soporte tecnico."

**Codigo HTTP:** 503 Service Unavailable

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

   if (Ejecucion manual?) then (si)
       :Verificar permiso PIP-001;
       if (Tiene permiso?) then (si)
       else (no)
           #FFCDD2:403 Forbidden;
           stop
       endif
   else (scheduler)
   endif

   :Verificar pipeline en curso;
   if (Hay ejecucion RUNNING?) then (si)
       #FFCDD2:409 Conflict:\nPipeline ya en ejecucion;
       stop
   else (no)
   endif

   :Crear registro RUNNING;
   :Escanear directorio entrada;

   if (Hay archivos?) then (si)

       :Validar formato archivos;

       partition "Clasificacion de Archivos" {
           fork
               :Archivos validos\n-> lista procesamiento;
           fork again
               :Archivos invalidos\n-> mover a /errors;
           end fork
       }

       if (Hay archivos validos?) then (si)

           #C8E6C9:BEGIN TRANSACTION;

           while (Mas archivos por procesar?) is (si)
               :Leer archivo;
               :Transformar segun reglas;

               if (Error transformacion?) then (si)
                   if (Config: fallar archivo?) then (si)
                       :Mover archivo a /errors;
                   else (saltar linea)
                       :Registrar error, continuar;
                   endif
               else (no)
                   :Cargar en BD;

                   if (Error BD?) then (si)
                       #FFCDD2:ROLLBACK;
                       :status = FAILED;
                       :Preservar archivos;
                       stop
                   else (no)
                   endif
               endif

               :Actualizar progreso;
           endwhile (no)

           :Validar integridad contable;

           if (Debitos = Creditos?) then (si)
               #C8E6C9:COMMIT;
               :Mover archivos a /processed;

               if (Hubo errores parciales?) then (si)
                   :status = PARTIAL_SUCCESS;
               else (no)
                   :status = COMPLETED;
               endif
           else (no)
               #FFCDD2:ROLLBACK;
               :status = FAILED;
               :Motivo: Descuadre contable;
               stop
           endif

       else (no)
           :status = FAILED;
           :Todos los archivos invalidos;
       endif

   else (no)
       :status = NO_DATA;
   endif

   #C8E6C9:Registrar auditoria (BR_008);
   :Actualizar metricas;

   if (Notificaciones activas?) then (si)
       :Enviar notificacion resultado;
   else (no)
   endif

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
     - Pipeline puede ejecutarse automaticamente via cron scheduler
   * - BR_008
     - Auditoria Completa
     - Evento PIPELINE_EXECUTED registra: runId, archivos, registros, duracion, errores
   * - BR_020
     - Integridad Contable
     - Suma de debitos debe igualar suma de creditos antes de commit
   * - BR_021
     - Atomicidad ETL
     - Procesamiento es transaccional, rollback completo en caso de fallo

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
     - Sistema DEBE escanear directorio de entrada segun patron configurado
   * - FR-050.04
     - Sistema DEBE validar formato, headers y encoding de archivos
   * - FR-050.05
     - Sistema DEBE transformar datos segun reglas configuradas
   * - FR-050.06
     - Sistema DEBE procesar en transaccion atomica con rollback
   * - FR-050.07
     - Sistema DEBE validar integridad contable antes de commit
   * - FR-050.08
     - Sistema DEBE mover archivos procesados a /processed/{fecha}
   * - FR-050.09
     - Sistema DEBE mover archivos con error a /errors/{fecha}
   * - FR-050.10
     - Sistema DEBE registrar metricas: tiempo, registros, archivos, errores
   * - FR-050.11
     - Sistema DEBE registrar evento PIPELINE_EXECUTED en auditoria
   * - FR-050.12
     - Sistema DEBE soportar ejecucion programada via cron
   * - FR-050.13
     - Sistema DEBE enviar notificaciones segun configuracion

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-001: Automatizacion del Procesamiento de Datos
   * - **BR Aplicables**
     - BR_001, BR_008, BR_020, BR_021
   * - **FR Derivados**
     - FR-050.01 a FR-050.13 (13 requerimientos)
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
     - Version completa con PlantUML embebido (Sphinx). 3 diagramas detallados. Flujos alternos expandidos.