.. meta::
   :artefacto: index_casos_uso_v2
   :tipo: Indice Maestro
   :dominio: requisitos
   :subdominio: casos_uso
   :estado: En Desarrollo
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _casos-uso-v2-index:

==============================================================================
Catalogo de Casos de Uso v2.0 (con PlantUML)
==============================================================================

Nivel 2 de la Jerarquia de Requisitos IACT - Version con diagramas PlantUML.

.. contents:: Contenido
   :local:
   :depth: 2

----

Proposito
---------

Este catalogo contiene los 49 Casos de Uso del proyecto IACT, documentados
con diagramas PlantUML embebidos usando Sphinx y sphinxcontrib-plantuml.

----

Resumen General
---------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Total UC**
     - 49
   * - **Modulos**
     - 8
   * - **Version Documentos**
     - 2.0.0
   * - **Diagramas por UC**
     - 3 (Caso de Uso, Secuencia, Actividad)
   * - **Build System**
     - Sphinx + sphinxcontrib-plantuml

----

Distribucion por Modulo
-----------------------

.. list-table::
   :widths: 20 35 10 15 20
   :header-rows: 1

   * - Modulo
     - Descripcion
     - UC
     - Rango
     - Estado
   * - MOD_Auth
     - Autenticacion
     - 5
     - UC-001 a UC-005
     - Pendiente
   * - MOD_Users
     - Gestion de Usuarios
     - 4
     - UC-006 a UC-009
     - Pendiente
   * - MOD_Access
     - Control de Acceso (RBAC)
     - 9
     - UC-010, 011, 041-047
     - Pendiente
   * - MOD_Pipeline
     - Pipeline ETL
     - 4
     - UC-050 a UC-053
     - Pendiente
   * - MOD_Reports
     - Reportes y Dashboard
     - 14
     - UC-017 a UC-030
     - Pendiente
   * - MOD_Alerts
     - Alertas
     - 5
     - UC-036 a UC-040
     - Pendiente
   * - MOD_Audit
     - Auditoria
     - 4
     - UC-060 a UC-063
     - Pendiente
   * - MOD_Logs
     - Bitacoras
     - 4
     - UC-070 a UC-073
     - Pendiente

----

Trazabilidad BReq -> UC
-----------------------

.. list-table::
   :widths: 20 35 45
   :header-rows: 1

   * - BReq
     - Nombre
     - UC Relacionados
   * - BReq-001
     - Visibilidad Metricas IVR
     - UC-025 a UC-030, UC-050 a UC-053
   * - BReq-002
     - Reduccion Tiempo Incidentes
     - UC-036 a UC-040
   * - BReq-003
     - Decisiones Informadas
     - UC-017 a UC-024
   * - BReq-004
     - Cumplimiento Seguridad
     - UC-001 a UC-011, UC-041-047, UC-060-073
   * - BReq-005
     - Integridad Datos
     - UC-050 a UC-053

----

Diagramas Incluidos
-------------------

Cada UC v2.0 incluye 3 diagramas PlantUML:

1. **Diagrama de Caso de Uso**

   Muestra actores y sus relaciones con el caso de uso.

2. **Diagrama de Secuencia**

   Muestra la interaccion entre componentes durante el flujo normal.

3. **Diagrama de Actividad**

   Muestra el flujo de decisiones y caminos alternos.

----

Estructura de Directorios
-------------------------

::

   casos_uso_v2/
       index.rst                    <- Este archivo
       _static/
           plantuml_styles.iuml     <- Estilos comunes PlantUML
       auth/
           index.rst
           UC_001_Iniciar_Sesion.rst
           UC_002_Cerrar_Sesion.rst
           ...
       users/
       access/
       pipeline/
       reports/
       alerts/
       audit/
       logs/

----

Contenido por Modulo
--------------------

.. toctree::
   :maxdepth: 2
   :caption: Modulos

   auth/index
   users/index
   access/index
   pipeline/index
   reports/index
   alerts/index
   audit/index
   logs/index

----

Referencias
-----------

- TPL_002 v2.0: Plantilla de UC con PlantUML
- FND_03 v1.3.0: Casos de Uso (definicion)
- FND_05: Jerarquia de 4 Niveles
- PLAN_UC_v2_PLANTUML_v1_1_0.md: Plan de ejecucion

----

Historial de Cambios
--------------------

.. list-table::
   :widths: 12 12 20 56
   :header-rows: 1

   * - Version
     - Fecha
     - Autor
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Equipo IACT
     - Estructura inicial. Indices por modulo. Estilos PlantUML.
