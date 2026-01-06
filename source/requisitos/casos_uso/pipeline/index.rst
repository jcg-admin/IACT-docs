cat > /mnt/user-data/outputs/casos_uso_v2/pipeline/index.rst << 'EOF'
.. meta::
   :artefacto: index_pipeline
   :tipo: Indice
   :dominio: requisitos
   :subdominio: casos_uso/pipeline
   :estado: Completado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _casos-uso-pipeline-index:

==============================================================================
MOD_Pipeline: Casos de Uso de Pipeline ETL
==============================================================================

Modulo de Pipeline de Datos - Version 2.0 con diagramas PlantUML completos.

.. contents:: Contenido
   :local:
   :depth: 2

----

Resumen
-------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Modulo**
     - MOD_Pipeline
   * - **UC Documentados**
     - 4 (UC-050 a UC-053)
   * - **Version**
     - 2.0.0 (con PlantUML)
   * - **Estado**
     - Completado
   * - **BReq Origen**
     - BReq-001: Automatizacion del Procesamiento
   * - **BR Aplicables**
     - BR_001, BR_008, BR_020-BR_023

----

Casos de Uso
------------

.. list-table::
   :widths: 12 35 12 12 12 17
   :header-rows: 1

   * - ID
     - Nombre
     - Complej.
     - Diag.
     - FR
     - Estado
   * - UC-050
     - Ejecutar Pipeline de Datos
     - Alta
     - 3
     - 13
     - Completado
   * - UC-051
     - Monitorear Estado del Pipeline
     - Media
     - 3
     - 11
     - Completado
   * - UC-052
     - Configurar Pipeline de Datos
     - Alta
     - 3
     - 14
     - Completado
   * - UC-053
     - Consultar Historial Ejecuciones
     - Media
     - 3
     - 13
     - Completado

----

Descripcion de Casos de Uso
---------------------------

UC-050: Ejecutar Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^

Ejecuta el pipeline ETL completo: escanea directorio de entrada, valida
archivos, transforma datos segun reglas, carga en BD transaccionalmente
y mueve archivos a procesados/errores. Soporta ejecucion manual y programada.

- **Actor:** Administrador de Datos / Scheduler
- **FR Derivados:** 13
- **Funcion RBAC:** PIP-001
- **BR:** BR_001, BR_008, BR_020, BR_021

UC-051: Monitorear Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Visualiza estado de ejecucion en tiempo real via WebSocket: progreso,
archivos procesados, errores, metricas de rendimiento. Permite cancelar
ejecucion en curso con rollback automatico.

- **Actor:** Administrador de Datos / Operador
- **FR Derivados:** 11
- **Funciones RBAC:** PIP-002 (monitorear), PIP-003 (cancelar)
- **BR:** BR_008, BR_022

UC-052: Configurar Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configura todos los parametros del pipeline: directorios, patrones,
reglas de transformacion, mapeos de campos, scheduler (cron),
notificaciones y manejo de errores. Incluye validacion y dry-run.

- **Actor:** Administrador de Datos
- **FR Derivados:** 14
- **Funcion RBAC:** PIP-004
- **BR:** BR_001, BR_008, BR_023

UC-053: Historial de Ejecuciones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consulta historial completo con filtros avanzados, detalle de archivos
y errores, exportacion a CSV/Excel, tendencias y re-ejecucion de fallidos.

- **Actor:** Administrador de Datos / Auditor
- **FR Derivados:** 13
- **Funcion RBAC:** PIP-005

----

Metricas del Modulo
-------------------

.. list-table::
   :widths: 40 30 30
   :header-rows: 1

   * - Metrica
     - Valor
     - Notas
   * - UC Documentados
     - 4
     - 100%
   * - FR Derivados
     - 51
     - ~13 por UC
   * - Diagramas PlantUML
     - 12
     - 3 por UC
   * - Lineas documentacion
     - ~2,500
     - Total modulo
   * - Promedio lineas/UC
     - ~575
     - Alta calidad

----

Funciones RBAC del Modulo
-------------------------

.. list-table::
   :widths: 12 35 53
   :header-rows: 1

   * - Codigo
     - Nombre
     - UC que Requiere
   * - PIP-001
     - Ejecutar Pipeline
     - UC-050, UC-053 (re-ejecutar)
   * - PIP-002
     - Monitorear Pipeline
     - UC-051
   * - PIP-003
     - Cancelar Pipeline
     - UC-051 (cancelar ejecucion)
   * - PIP-004
     - Configurar Pipeline
     - UC-052
   * - PIP-005
     - Consultar Historial
     - UC-053

----

Reglas de Negocio Aplicables
----------------------------

.. list-table::
   :widths: 12 30 58
   :header-rows: 1

   * - BR
     - Nombre
     - UC que Implementan
   * - BR_001
     - Automatizacion
     - UC-050 (scheduler), UC-052 (config cron)
   * - BR_008
     - Auditoria
     - UC-050, UC-051, UC-052 (eventos registrados)
   * - BR_020
     - Integridad Contable
     - UC-050 (validacion debito=credito)
   * - BR_021
     - Atomicidad ETL
     - UC-050 (transaccion con rollback)
   * - BR_022
     - Cancelacion Segura
     - UC-051 (rollback al cancelar)
   * - BR_023
     - Config Inmutable
     - UC-052 (no editar si RUNNING)

----

.. toctree::
   :maxdepth: 1
   :caption: Casos de Uso

   UC_050_Ejecutar_Pipeline
   UC_051_Monitorear_Pipeline
   UC_052_Configurar_Pipeline
   UC_053_Historial_Pipeline

----

Historial de Cambios
--------------------

.. list-table::
   :widths: 12 12 76
   :header-rows: 1

   * - Version
     - Fecha
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Fase 4 regenerada: 4 UC con PlantUML completo, uno por uno
