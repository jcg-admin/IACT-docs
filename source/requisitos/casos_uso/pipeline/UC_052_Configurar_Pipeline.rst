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

Permite configurar todos los parametros del pipeline ETL: directorios de
entrada/salida/errores, patrones de archivos, reglas de transformacion,
mapeos de campos, validaciones, expresion cron para ejecucion automatica,
configuracion de notificaciones y opciones de manejo de errores.
Los cambios solo aplican a ejecuciones futuras.

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
       usecase "Config Reglas\nTransformacion" as CRT
       usecase "Config Mapeo\nCampos" as CMC
       usecase "Config\nScheduler" as CS
       usecase "Config\nNotificaciones" as CN
       usecase "Config Manejo\nErrores" as CME
       usecase "Validar\nConfiguracion" as VC
   }

   ADM --> UC052
   UC052 ..> CD : <<include>>
   UC052 ..> CRT : <<include>>
   UC052 ..> CMC : <<include>>
   UC052 ..> CS : <<include>>
   UC052 ..> CN : <<include>>
   UC052 ..> CME : <<include>>
   UC052 ..> VC : <<include>>
   UC052 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion PIP-004 (Configurar Pipeline)
2. Pipeline no esta en ejecucion (status != RUNNING)
3. Acceso al sistema de archivos para validar directorios

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Configuracion de Pipeline" desde menu administracion.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Configuracion guardada en tabla pipeline_config
2. Scheduler actualizado si cambio expresion cron
3. Evento PIPELINE_CONFIGURED registrado (BR_008)
4. Configuracion activa para proximas ejecuciones

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
     - Verifica pipeline no esta en ejecucion
   * - 4
     -
     - Carga configuracion actual
   * - 5
     -
     - Muestra formulario con tabs/secciones
   * - 6
     - Modifica configuracion de directorios
     -
   * - 7
     - Modifica reglas de transformacion
     -
   * - 8
     - Modifica mapeo de campos
     -
   * - 9
     - Modifica programacion (cron)
     -
   * - 10
     - Modifica notificaciones
     -
   * - 11
     - Presiona "Validar Configuracion"
     -
   * - 12
     -
     - Ejecuta validaciones completas
   * - 13
     -
     - Muestra resultado de validacion
   * - 14
     - Presiona "Guardar Configuracion"
     -
   * - 15
     -
     - Guarda en pipeline_config
   * - 16
     -
     - Actualiza scheduler si aplica
   * - 17
     -
     - Registra PIPELINE_CONFIGURED (BR_008)
   * - 18
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
   participant "ValidationService" as VS #E8F5E9
   participant "SchedulerService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0
   collections "FileSystem" as FS #ECEFF1

   ADM -> FE: 1. Accede a Configuracion
   FE -> PC: 2. GET /api/pipeline/config
   activate PC

   PC -> DB: 3. SELECT * FROM pipeline_runs\nWHERE status = 'RUNNING'
   DB --> PC: [] (ninguno)

   PC -> DB: 4. SELECT * FROM pipeline_config
   DB --> PC: {currentConfig}

   PC --> FE: 5. {config, isLocked: false}
   deactivate PC

   FE --> ADM: 6. Formulario con tabs:\n- Directorios\n- Reglas\n- Mapeo\n- Scheduler\n- Notificaciones

   ADM -> FE: 7. Modifica configuracion
   note right
       inputDir: /data/input
       outputDir: /data/processed
       errorDir: /data/errors
       filePattern: *.csv
       cron: 0 6 * * *
   end note

   ADM -> FE: 8. Clic "Validar"
   FE -> PC: 9. POST /api/pipeline/config/validate\n{newConfig}
   activate PC

   PC -> VS: 10. validateConfig(config)
   activate VS

   VS -> FS: 11. checkDirectory(inputDir)
   FS --> VS: {exists: true, writable: true}

   VS -> FS: 12. checkDirectory(outputDir)
   VS -> FS: 13. checkDirectory(errorDir)

   VS -> VS: 14. validateCronExpression(cron)
   VS -> VS: 15. validateTransformRules(rules)
   VS -> VS: 16. validateFieldMappings(mappings)

   VS --> PC: 17. {valid: true, warnings: []}
   deactivate VS

   PC --> FE: 18. {valid: true}
   deactivate PC
   FE --> ADM: 19. "Configuracion valida"

   ADM -> FE: 20. Clic "Guardar"
   FE -> PC: 21. PUT /api/pipeline/config\n{config}
   activate PC

   PC -> CS: 22. saveConfig(config)
   activate CS

   CS -> DB: 23. UPDATE pipeline_config\nSET ... WHERE id = 1
   DB --> CS: OK

   alt Cron cambio
       CS -> SS: 24. updateSchedule(newCron)
       activate SS
       SS -> SS: 25. Actualizar cron job
       SS --> CS: OK
       deactivate SS
   end

   CS -> AUD: 26. logEvent('PIPELINE_CONFIGURED',\n{changes, oldConfig, newConfig})
   activate AUD
   AUD -> DB: INSERT INTO audit_log
   AUD --> CS: OK
   deactivate AUD

   CS --> PC: 27. {saved: true}
   deactivate CS

   PC --> FE: 28. 200 OK
   deactivate PC
   FE --> ADM: 29. "Configuracion guardada exitosamente"
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Validacion Fallida
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 12 del flujo normal

**Condicion:** Configuracion no pasa validaciones

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 12.1
     - Sistema detecta errores de validacion
   * - 12.2
     - Muestra lista de errores por seccion
   * - 12.3
     - Resalta campos con error en formulario
   * - 12.4
     - Boton "Guardar" permanece deshabilitado

**Retorno:** Usuario corrige y vuelve a validar

7.2 FA-2: Probar Configuracion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario quiere probar sin guardar

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 11.1
     - Usuario hace clic en "Probar con Archivo"
   * - 11.2
     - Sistema permite seleccionar archivo de prueba
   * - 11.3
     - Ejecuta pipeline en modo dry-run (sin guardar datos)
   * - 11.4
     - Muestra resultado de transformacion sin persistir

**Retorno:** Usuario decide si guardar configuracion

7.3 FA-3: Importar/Exportar Configuracion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario quiere respaldar o restaurar configuracion

Sistema permite exportar a JSON e importar desde archivo.

----

8. Excepciones
--------------

8.1 EX-1: Pipeline en Ejecucion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Existe ejecucion con status=RUNNING

**Mensaje:** "No se puede modificar configuracion mientras el pipeline esta en ejecucion. Espere a que finalice."

**Accion:** Formulario en modo solo lectura

8.2 EX-2: Directorio No Existe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Directorio configurado no existe o no es accesible

**Mensaje:** "El directorio [X] no existe o no tiene permisos de escritura."

8.3 EX-3: Expresion Cron Invalida
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Formato de cron no valido

**Mensaje:** "Expresion cron invalida. Formato esperado: minuto hora dia mes diaSemana"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-052 Configurar Pipeline
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

   :Accede a Configuracion;
   :Verificar permiso PIP-004;

   if (Tiene permiso?) then (si)

       if (Pipeline RUNNING?) then (si)
           #FFE0B2:Modo solo lectura;
           :Mostrar config actual;
           stop
       else (no)
       endif

       :Cargar configuracion actual;
       :Mostrar formulario;

       repeat
           :Usuario modifica parametros;

           partition "Secciones de Configuracion" {
               split
                   :Directorios;
                   note right: input, output, errors
               split again
                   :Reglas Transformacion;
               split again
                   :Mapeo Campos;
               split again
                   :Scheduler (cron);
               split again
                   :Notificaciones;
               split again
                   :Manejo Errores;
               end split
           }

           :Validar configuracion;

           if (Errores?) then (si)
               #FFCDD2:Mostrar errores;
               :Resaltar campos;
           else (no)
               #C8E6C9:Configuracion valida;

               if (Probar?) then (si)
                   :Ejecutar dry-run;
                   :Mostrar resultado;
               else (no)
               endif
           endif

       repeat while (Corregir?) is (si)
       -> Guardar;

       :Guardar en BD;

       if (Cron cambio?) then (si)
           :Actualizar scheduler;
       else (no)
       endif

       #C8E6C9:Registrar auditoria (BR_008);
       :Mostrar confirmacion;

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
     - Configuracion de expresion cron para ejecucion automatica
   * - BR_008
     - Auditoria
     - Cambios de configuracion registrados con diff
   * - BR_023
     - Config Inmutable en Ejecucion
     - No permitir cambios mientras pipeline RUNNING

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-052.01
     - Sistema DEBE verificar permiso PIP-004
   * - FR-052.02
     - Sistema DEBE bloquear edicion si pipeline RUNNING
   * - FR-052.03
     - Sistema DEBE permitir configurar directorios (input/output/errors)
   * - FR-052.04
     - Sistema DEBE permitir configurar patron de archivos
   * - FR-052.05
     - Sistema DEBE permitir configurar reglas de transformacion
   * - FR-052.06
     - Sistema DEBE permitir configurar mapeo de campos origen-destino
   * - FR-052.07
     - Sistema DEBE permitir configurar expresion cron
   * - FR-052.08
     - Sistema DEBE permitir configurar notificaciones (email, webhook)
   * - FR-052.09
     - Sistema DEBE permitir configurar manejo de errores (saltar/fallar)
   * - FR-052.10
     - Sistema DEBE validar existencia y permisos de directorios
   * - FR-052.11
     - Sistema DEBE validar expresion cron
   * - FR-052.12
     - Sistema DEBE permitir probar configuracion (dry-run)
   * - FR-052.13
     - Sistema DEBE actualizar scheduler automaticamente
   * - FR-052.14
     - Sistema DEBE registrar cambios en auditoria con diff

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-001
   * - **BR Aplicables**
     - BR_001, BR_008, BR_023
   * - **FR Derivados**
     - FR-052.01 a FR-052.14 (14 requerimientos)
   * - **UC Relacionados**
     - UC-050 (usa configuracion)
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
     - Version completa con PlantUML. Secciones detalladas. Dry-run incluido.