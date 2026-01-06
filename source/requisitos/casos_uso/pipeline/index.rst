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

Modulo de Pipeline de Datos - Version 2.0 con diagramas PlantUML.

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
     - BR_001, BR_008

----

Casos de Uso
------------

.. list-table::
   :widths: 12 35 15 15 23
   :header-rows: 1

   * - ID
     - Nombre
     - Complej.
     - Diag.
     - Estado
   * - UC-050
     - Ejecutar Pipeline de Datos
     - Alta
     - 3
     - Completado
   * - UC-051
     - Monitorear Estado del Pipeline
     - Media
     - 3
     - Completado
   * - UC-052
     - Configurar Pipeline de Datos
     - Alta
     - 3
     - Completado
   * - UC-053
     - Consultar Historial Ejecuciones
     - Baja
     - 3
     - Completado

----

Descripcion de Casos de Uso
---------------------------

UC-050: Ejecutar Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^

Ejecuta el pipeline ETL que procesa archivos de entrada, transforma datos
segun reglas de negocio y carga en BD. Soporta ejecucion manual y programada.

- **Actor:** Administrador de Datos / Scheduler
- **FR Derivados:** 11
- **Funcion RBAC:** PIP-001

UC-051: Monitorear Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Visualiza en tiempo real el estado de ejecucion via WebSocket, con progreso,
errores y metricas de rendimiento.

- **Actor:** Administrador de Datos / Operador
- **FR Derivados:** 7
- **Funcion RBAC:** PIP-002, PIP-003 (cancelar)

UC-052: Configurar Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configura parametros del pipeline: directorios, reglas de transformacion,
scheduler y notificaciones.

- **Actor:** Administrador de Datos
- **FR Derivados:** 9
- **Funcion RBAC:** PIP-004

UC-053: Historial de Ejecuciones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consulta historial con filtros, detalle de archivos procesados y errores.
Permite exportar a CSV/Excel.

- **Actor:** Administrador de Datos / Auditor
- **FR Derivados:** 8
- **Funcion RBAC:** PIP-005

----

Metricas
--------

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
     - 35
     - ~9 por UC
   * - Diagramas PlantUML
     - 12
     - 3 por UC
   * - Lineas documentacion
     - ~1,615
     - Total modulo

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
     - UC-050
   * - PIP-002
     - Monitorear Pipeline
     - UC-051
   * - PIP-003
     - Cancelar Pipeline
     - UC-051 (opcional)
   * - PIP-004
     - Configurar Pipeline
     - UC-052
   * - PIP-005
     - Consultar Historial
     - UC-053

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
     - Fase 4 completada: 4 UC con PlantUML embebido
