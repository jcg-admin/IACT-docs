.. meta::
   :artefacto: UC_052
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/pipeline
   :modulo: MOD_Pipeline
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-052:

==============================================================================
UC-052: Configurar Pipeline de Datos
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
     - UC-052
   * - **Nombre**
     - Configurar Pipeline de Datos
   * - **Actor Primario**
     - Administrador de Datos
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Pipeline
   * - **Complejidad**
     - Alta
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-001: Automatizacion del Procesamiento

----

2. Descripcion
--------------

Permite configurar los parametros del pipeline ETL: directorios de entrada/salida,
reglas de transformacion, mapeos de campos, programacion de ejecucion automatica
y notificaciones.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-052 Configurar Pipeline
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
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Pipeline" {
       usecase "UC-052:\nConfigurar\nPipeline" as UC052
       usecase "Config\nDirectorios" as CD
       usecase "Config\nReglas" as CR
       usecase "Config\nScheduler" as CS
       usecase "Config\nNotificaciones" as CN
   }

   ADM --> UC052
   UC052 ..> CD : <<include>>
   UC052 ..> CR : <<include>>
   UC052 ..> CS : <<include>>
   UC052 ..> CN : <<include>>
   UC052 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion PIP-004 (Configurar Pipeline)
2. Pipeline no esta en ejecucion

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Configuracion de Pipeline".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Configuracion guardada en BD
2. Evento PIPELINE_CONFIGURED registrado (BR_008)
3. Scheduler actualizado si cambio programacion

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
     - Accede a Configuracion Pipeline
     -
   * - 2
     -
     - Verifica permiso PIP-004
   * - 3
     -
     - Carga configuracion actual
   * - 4
     -
     - Muestra formulario con tabs
   * - 5
     - Modifica parametros deseados
     -
   * - 6
     - Presiona "Guardar Configuracion"
     -
   * - 7
     -
     - Valida parametros
   * - 8
     -
     - Guarda en pipeline_config
   * - 9
     -
     - Actualiza scheduler si aplica
   * - 10
     -
     - Registra PIPELINE_CONFIGURED (BR_008)
   * - 11
     -
     - Muestra confirmacion

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-052 Configurar Pipeline
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Admin" as ADM
   participant "Frontend" as FE #E3F2FD
   participant "PipelineController" as PC #E8F5E9
   participant "ConfigService" as CS #E8F5E9
   participant "SchedulerService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a Configuracion
   FE -> PC: 2. GET /api/pipeline/config
   activate PC
   PC -> DB: SELECT * FROM pipeline_config
   PC --> FE: 3. {config}
   deactivate PC

   FE --> ADM: 4. Formulario con tabs

   ADM -> FE: 5. Modifica configuracion
   ADM -> FE: 6. Guardar

   FE -> PC: 7. PUT /api/pipeline/config\n{directories, rules, schedule}
   activate PC

   PC -> CS: 8. updateConfig(newConfig)
   activate CS

   CS -> CS: 9. validateConfig()
   CS -> DB: 10. UPDATE pipeline_config

   alt Schedule cambio
       CS -> SS: 11. updateSchedule(cron)
       SS -> SS: Actualizar cron job
   end

   CS -> AUD: 12. logEvent(PIPELINE_CONFIGURED)
   AUD -> DB: INSERT audit_log

   CS --> PC: 13. {saved: true}
   deactivate CS

   PC --> FE: 14. 200 OK
   deactivate PC
   FE --> ADM: 15. "Configuracion guardada"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Validacion Fallida
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Si directorio no existe o cron invalido, muestra error especifico.

----

8. Excepciones
--------------

8.1 EX-1: Pipeline en Ejecucion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No se puede modificar configuracion mientras pipeline esta en ejecucion"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-052 Configurar Pipeline
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start

   :Accede a Configuracion;
   :Verificar permiso PIP-004;

   if (Tiene permiso?) then (si)

       if (Pipeline RUNNING?) then (si)
           #FFCDD2:Error: En ejecucion;
           stop
       else (no)
       endif

       :Cargar config actual;
       :Mostrar formulario;
       :Usuario modifica;
       :Validar parametros;

       if (Valido?) then (si)
           :Guardar en BD;

           if (Schedule cambio?) then (si)
               :Actualizar cron job;
           else (no)
           endif

           #C8E6C9:Registrar auditoria;
           #C8E6C9:Mostrar confirmacion;
       else (no)
           #FFE0B2:Mostrar errores;
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
   * - BR_001
     - Automatizacion
     - Configuracion de scheduler para ejecucion automatica
   * - BR_008
     - Auditoria
     - Cambios de configuracion registrados

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-052.01
     - Verificar permiso PIP-004
   * - FR-052.02
     - No permitir config si pipeline RUNNING
   * - FR-052.03
     - Configurar directorios entrada/salida/errores
   * - FR-052.04
     - Configurar reglas de transformacion
   * - FR-052.05
     - Configurar mapeos de campos
   * - FR-052.06
     - Configurar expresion cron para scheduler
   * - FR-052.07
     - Configurar notificaciones (email, webhook)
   * - FR-052.08
     - Validar existencia de directorios
   * - FR-052.09
     - Registrar cambios en auditoria

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-001
   * - **BR Aplicables**
     - BR_001, BR_008
   * - **FR Derivados**
     - FR-052.01 a FR-052.09
   * - **UC Relacionados**
     - UC-050 (usa config)
   * - **Funcion RBAC**
     - PIP-004: Configurar Pipeline

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