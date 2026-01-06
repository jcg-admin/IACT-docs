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
     - Ninguno
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

Permite visualizar en tiempo real el estado de ejecucion del pipeline,
incluyendo progreso actual, archivos procesados, errores encontrados
y metricas de rendimiento.

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

   rectangle "MOD_Pipeline" {
       usecase "UC-051:\nMonitorear\nPipeline" as UC051
       usecase "Ver\nProgreso" as VP
       usecase "Ver\nErrores" as VE
       usecase "Ver\nMetricas" as VM
       usecase "Cancelar\nEjecucion" as CE
   }

   ADM --> UC051
   OP --> UC051
   UC051 ..> VP : <<include>>
   UC051 ..> VE : <<include>>
   UC051 ..> VM : <<include>>
   UC051 ..> CE : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion PIP-002 (Monitorear Pipeline)
2. Existe al menos una ejecucion de pipeline

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Monitor de Pipeline" en dashboard.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Estado actual del pipeline visible en pantalla
2. Actualizacion en tiempo real via WebSocket (si esta en curso)

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
     - Si hay ejecucion activa, abre WebSocket
   * - 5
     -
     - Muestra dashboard con metricas
   * - 6
     - Visualiza progreso en tiempo real
     -
   * - 7
     -
     - Actualiza metricas cada 2 segundos
   * - 8
     - (Opcional) Expande seccion de errores
     -
   * - 9
     -
     - Muestra detalle de archivos con error

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
   participant "WebSocket" as WS #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Monitor
   FE -> PC: 2. GET /api/pipeline/status
   activate PC

   PC -> DB: 3. SELECT * FROM pipeline_runs\nORDER BY started_at DESC LIMIT 1
   DB --> PC: {currentRun}

   PC --> FE: 4. {status, progress, metrics}
   deactivate PC

   FE --> U: 5. Dashboard inicial

   alt Pipeline en ejecucion (RUNNING)
       FE -> WS: 6. Connect /ws/pipeline/{runId}
       activate WS

       loop Mientras status = RUNNING
           WS -> DB: 7. Poll status
           WS --> FE: 8. {progress, records, errors}
           FE --> U: 9. Actualizar UI
       end

       WS --> FE: 10. {status: COMPLETED}
       deactivate WS
       FE --> U: 11. "Pipeline finalizado"
   end

   U -> FE: 12. Expande "Ver Errores"
   FE -> PC: 13. GET /api/pipeline/runs/{id}/errors
   PC -> DB: SELECT * FROM pipeline_errors
   PC --> FE: 14. [errors]
   FE --> U: 15. Lista de errores con detalle
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Cancelar Ejecucion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 6 del flujo normal

**Condicion:** Usuario con PIP-003 hace clic en "Cancelar"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 6.1
     - Sistema solicita confirmacion
   * - 6.2
     - Usuario confirma cancelacion
   * - 6.3
     - Sistema envia señal de cancelacion
   * - 6.4
     - Pipeline finaliza con status=CANCELLED
   * - 6.5
     - Sistema registra en auditoria

**Retorno:** Paso 5 (actualiza dashboard)

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
   :caption: Actividad - UC-051 Monitorear Pipeline
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start

   :Accede a Monitor;
   :Verificar permiso PIP-002;

   if (Tiene permiso?) then (si)
       :Obtener estado actual;
       :Mostrar dashboard;

       if (Pipeline RUNNING?) then (si)
           :Abrir WebSocket;

           while (RUNNING?) is (si)
               :Recibir actualizacion;
               :Actualizar UI;

               if (Usuario cancela?) then (si)
                   :Enviar cancelacion;
                   :status = CANCELLED;
               else (no)
               endif
           endwhile (no)

           :Cerrar WebSocket;
       else (no)
           :Mostrar ultimo estado;
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

No aplica BR especificas (solo consulta).

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
     - Sistema DEBE mostrar estado actual del pipeline
   * - FR-051.03
     - Sistema DEBE actualizar en tiempo real via WebSocket
   * - FR-051.04
     - Sistema DEBE mostrar progreso (archivos procesados/total)
   * - FR-051.05
     - Sistema DEBE mostrar errores encontrados
   * - FR-051.06
     - Sistema DEBE mostrar metricas (tiempo, registros/seg)
   * - FR-051.07
     - Sistema DEBE permitir cancelar ejecucion (PIP-003)

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-001
   * - **FR Derivados**
     - FR-051.01 a FR-051.07
   * - **UC Relacionados**
     - UC-050 (Ejecutar)
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
     - Version con PlantUML embebido (Sphinx)
