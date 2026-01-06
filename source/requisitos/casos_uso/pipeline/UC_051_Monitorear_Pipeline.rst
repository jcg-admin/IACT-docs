.. meta::
   :artefacto: UC_051
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/pipeline
   :modulo: MOD_Pipeline
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-051:

==============================================================================
UC-051: Monitorear Estado del Pipeline
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
     - UC-051
   * - **Nombre**
     - Monitorear Estado del Pipeline
   * - **Actor Primario**
     - Administrador de Datos / Operador
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Pipeline
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-001: Automatizacion del Procesamiento

----

2. Descripcion
--------------

Permite visualizar en tiempo real el estado de ejecucion del pipeline ETL,
incluyendo progreso actual (archivos y registros procesados), errores
encontrados, tiempo transcurrido y metricas de rendimiento. Utiliza
WebSocket para actualizaciones en tiempo real sin necesidad de refresh
manual. Permite cancelar ejecucion en curso si el usuario tiene permisos.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-051 Monitorear Pipeline
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
   actor "Operador" as OP
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Pipeline" {
       usecase "UC-051:\nMonitorear\nPipeline" as UC051
       usecase "Ver Progreso\nTiempo Real" as VPR
       usecase "Ver Lista\nErrores" as VLE
       usecase "Ver Metricas\nRendimiento" as VMR
       usecase "Cancelar\nEjecucion" as CE
       usecase "Descargar\nLog" as DL
   }

   ADM --> UC051
   OP --> UC051
   UC051 ..> VPR : <<include>>
   UC051 ..> VLE : <<include>>
   UC051 ..> VMR : <<include>>
   UC051 ..> CE : <<extends>>
   UC051 ..> DL : <<extends>>
   UC051 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion PIP-002 (Monitorear Pipeline)
2. Existe al menos una ejecucion de pipeline registrada
3. Conexion WebSocket disponible para tiempo real

4.2 Trigger
^^^^^^^^^^^

- Usuario accede a "Monitor de Pipeline" en menu
- Usuario hace clic en "Ver Estado" desde ejecucion reciente
- Redireccion automatica tras iniciar ejecucion

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Estado actual del pipeline visible en tiempo real
2. Metricas de progreso actualizadas cada 2 segundos
3. Si se cancela: evento PIPELINE_CANCELLED registrado

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
     - Accede a Monitor de Pipeline
     -
   * - 2
     -
     - Verifica permiso PIP-002
   * - 3
     -
     - Obtiene estado actual del pipeline
   * - 4
     -
     - Renderiza dashboard de monitoreo
   * - 5
     -
     - Si RUNNING: abre conexion WebSocket
   * - 6
     - Visualiza progreso inicial
     -
   * - 7
     -
     - WebSocket envia actualizaciones (cada 2s)
   * - 8
     - Observa progreso en tiempo real
     -
   * - 9
     - (Opcional) Expande seccion de errores
     -
   * - 10
     -
     - Muestra lista de errores con detalle
   * - 11
     - (Opcional) Descarga log completo
     -
   * - 12
     -
     - Pipeline finaliza (COMPLETED/FAILED)
   * - 13
     -
     - Cierra WebSocket, muestra resumen final

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-051 Monitorear Pipeline
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin/Operador" as U
   participant "Frontend" as FE #E3F2FD
   participant "PipelineController" as PC #E8F5E9
   participant "WebSocketServer" as WS #E8F5E9
   participant "MonitorService" as MS #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Monitor
   FE -> PC: 2. GET /api/pipeline/status
   activate PC

   PC -> DB: 3. SELECT * FROM pipeline_runs\nORDER BY started_at DESC LIMIT 1
   DB --> PC: {currentRun}

   PC -> DB: 4. SELECT COUNT(*) as errors\nFROM pipeline_errors\nWHERE run_id = ?
   DB --> PC: {errorCount}

   PC --> FE: 5. {run, progress, metrics, errors}
   deactivate PC

   FE --> U: 6. Dashboard de monitoreo

   alt Pipeline en ejecucion (status=RUNNING)
       FE -> WS: 7. WebSocket CONNECT\n/ws/pipeline/{runId}
       activate WS
       WS --> FE: 8. Connection established

       loop Mientras status = RUNNING
           WS -> MS: 9. getProgress(runId)
           MS -> DB: SELECT progress FROM pipeline_runs
           MS --> WS: {progress}

           WS --> FE: 10. {filesProcessed, recordsProcessed,\ncurrentFile, elapsedTime, errors}
           FE --> U: 11. Actualiza UI en tiempo real
           note right: Barra de progreso\nContadores\nTiempo transcurrido

           FE -> FE: 12. sleep(2000ms)
       end

       WS --> FE: 13. {status: 'COMPLETED',\nfinalMetrics}
       deactivate WS
       FE --> U: 14. "Pipeline finalizado"\nMuestra resumen
   end

   opt Usuario expande errores
       U -> FE: 15. Clic en "Ver Errores"
       FE -> PC: 16. GET /api/pipeline/runs/{id}/errors
       activate PC
       PC -> DB: SELECT * FROM pipeline_errors\nWHERE run_id = ?
       PC --> FE: 17. [errors with details]
       deactivate PC
       FE --> U: 18. Lista de errores expandida
   end

   opt Usuario descarga log
       U -> FE: 19. Clic en "Descargar Log"
       FE -> PC: 20. GET /api/pipeline/runs/{id}/log
       PC --> FE: 21. log.txt (binary)
       FE --> U: 22. Descarga archivo
   end
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Cancelar Ejecucion en Curso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 8 del flujo normal

**Condicion:** Usuario con permiso PIP-003 hace clic en "Cancelar"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 8.1
     - Sistema muestra dialogo de confirmacion
   * - 8.2
     - Usuario confirma cancelacion
   * - 8.3
     - Sistema envia señal de cancelacion al proceso
   * - 8.4
     - ETLEngine detiene procesamiento de forma segura
   * - 8.5
     - Sistema ejecuta rollback de transaccion pendiente
   * - 8.6
     - Actualiza status=CANCELLED con metricas parciales
   * - 8.7
     - Registra evento PIPELINE_CANCELLED en auditoria
   * - 8.8
     - WebSocket notifica cancelacion a clientes

**Retorno:** Paso 13 (muestra resumen de cancelacion)

7.2 FA-2: Reconexion WebSocket
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Durante loop de paso 7-12

**Condicion:** Conexion WebSocket se pierde

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 7.1
     - Frontend detecta desconexion
   * - 7.2
     - Muestra indicador "Reconectando..."
   * - 7.3
     - Intenta reconexion (hasta 5 intentos, backoff exponencial)
   * - 7.4
     - Si reconecta: continua con datos actualizados
   * - 7.5
     - Si falla: cambia a polling HTTP cada 5 segundos

**Retorno:** Continua monitoreo

7.3 FA-3: Ver Ejecucion Pasada
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** No hay ejecucion en curso, usuario selecciona ejecucion anterior

Sistema muestra estado final sin WebSocket (solo lectura).

----

8. Excepciones
--------------

8.1 EX-1: Sin Ejecuciones Registradas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** No existen registros en pipeline_runs

**Mensaje:** "No hay ejecuciones de pipeline registradas. Ejecute el pipeline para comenzar."

8.2 EX-2: Sin Permiso para Cancelar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario intenta cancelar sin PIP-003

**Mensaje:** "No tiene permisos para cancelar ejecuciones. Contacte al administrador."

8.3 EX-3: Pipeline Ya Finalizado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario intenta cancelar pipeline no RUNNING

**Mensaje:** "El pipeline ya ha finalizado y no puede cancelarse."

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-051 Monitorear Pipeline
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

   :Accede a Monitor de Pipeline;
   :Verificar permiso PIP-002;

   if (Tiene permiso?) then (si)
       :Obtener estado actual;
       :Renderizar dashboard;

       if (Pipeline RUNNING?) then (si)
           :Abrir WebSocket;

           while (Pipeline en ejecucion?) is (si)
               :Recibir actualizacion;
               :Actualizar UI;

               fork
                   :Mostrar progreso;
               fork again
                   :Actualizar contadores;
               fork again
                   :Actualizar tiempo;
               end fork

               if (Usuario cancela?) then (si)
                   if (Tiene PIP-003?) then (si)
                       :Confirmar cancelacion;
                       :Enviar señal CANCEL;
                       :Rollback transaccion;
                       #FFE0B2:status = CANCELLED;
                       #C8E6C9:Registrar auditoria;
                   else (no)
                       #FFCDD2:Sin permiso;
                   endif
               else (no)
               endif

               if (WebSocket desconectado?) then (si)
                   :Intentar reconexion;
                   if (Reconexion exitosa?) then (no)
                       :Cambiar a polling HTTP;
                   else (si)
                   endif
               else (no)
               endif

           endwhile (no - finalizado)

           :Cerrar WebSocket;
       else (no)
           :Mostrar estado final;
       endif

       :Mostrar resumen;

       if (Ver errores?) then (si)
           :Cargar lista errores;
           :Mostrar detalle;
       else (no)
       endif

       if (Descargar log?) then (si)
           :Generar archivo log;
           :Descargar;
       else (no)
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
     - Aplicacion en este UC
   * - BR_008
     - Auditoria
     - PIPELINE_CANCELLED registrado si se cancela
   * - BR_022
     - Cancelacion Segura
     - Rollback automatico al cancelar, datos consistentes

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-051.01
     - Sistema DEBE verificar permiso PIP-002
   * - FR-051.02
     - Sistema DEBE mostrar estado actual (RUNNING, COMPLETED, FAILED, CANCELLED)
   * - FR-051.03
     - Sistema DEBE actualizar progreso via WebSocket cada 2 segundos
   * - FR-051.04
     - Sistema DEBE mostrar: archivos procesados/total, registros, tiempo
   * - FR-051.05
     - Sistema DEBE mostrar contador de errores con acceso a detalle
   * - FR-051.06
     - Sistema DEBE mostrar metricas de rendimiento (registros/segundo)
   * - FR-051.07
     - Sistema DEBE permitir cancelar ejecucion (requiere PIP-003)
   * - FR-051.08
     - Sistema DEBE ejecutar rollback automatico al cancelar
   * - FR-051.09
     - Sistema DEBE registrar cancelacion en auditoria
   * - FR-051.10
     - Sistema DEBE reconectar WebSocket automaticamente
   * - FR-051.11
     - Sistema DEBE permitir descargar log completo de ejecucion

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-001
   * - **BR Aplicables**
     - BR_008, BR_022
   * - **FR Derivados**
     - FR-051.01 a FR-051.11 (11 requerimientos)
   * - **UC Relacionados**
     - UC-050 (Ejecutar), UC-053 (Historial)
   * - **Funciones RBAC**
     - PIP-002: Monitorear, PIP-003: Cancelar

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
     - Version completa con PlantUML. WebSocket detallado. Cancelacion con rollback.