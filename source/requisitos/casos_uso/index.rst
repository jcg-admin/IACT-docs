.. meta::
   :project: IACT - Call Center Analytics
   :version: 4.0.0
   :date: 2026-01-06
   :status: En Desarrollo

.. _casos-uso-index:

==============================================
Casos de Uso - IACT Call Center Analytics v4.0
==============================================

1. Introducción
===============

Este documento contiene la especificación completa de los **49 Casos de Uso** del sistema
IACT (IVR Analytics & Customer Tracking) Call Center Analytics Dashboard.

1.1 Propósito
-------------

Documentar de forma exhaustiva los requisitos funcionales del sistema mediante casos de uso
que describen las interacciones entre los actores y el sistema.

1.2 Alcance
-----------

Los casos de uso cubren los **8 módulos funcionales** del sistema:

.. list-table::
   :widths: 15 30 10 45
   :header-rows: 1

   * - Código
     - Módulo
     - UC
     - Descripción
   * - AUTH
     - MOD_Auth
     - 5
     - Autenticación y gestión de sesiones
   * - USR
     - MOD_Users
     - 4
     - Gestión de usuarios e identidades
   * - ACC
     - MOD_Access
     - 9
     - Control de acceso RBAC
   * - PIP
     - MOD_Pipeline
     - 4
     - Supervisión del proceso ETL
   * - RPT
     - MOD_Reports
     - 14
     - Reportes, dashboard y exportación
   * - ALR
     - MOD_Alerts
     - 5
     - Alertas y notificaciones internas
   * - AUD
     - MOD_Audit
     - 4
     - Auditoría y compliance
   * - LOG
     - MOD_Logs
     - 4
     - Bitácoras técnicas del sistema
   * - **TOTAL**
             
     - **49**
             

1.3 Convenciones de Nomenclatura
--------------------------------

**Formato de Identificador:**

.. code-block:: text

   UC_[MOD]_[NN]

   Donde:
     UC    = Prefijo estándar "Caso de Uso"
     [MOD] = Código del módulo (AUTH, USR, ACC, PIP, RPT, ALR, AUD, LOG)
     [NN]  = Número secuencial dentro del módulo (01, 02, 03...)

   Ejemplos:
     UC_AUTH_01  →  Iniciar Sesión
     UC_USR_01   →  Crear Usuario
     UC_ACC_01   →  Asignar Funciones
     UC_RPT_06   →  Exportar CSV

1.4 Documentos Relacionados
---------------------------

- :doc:`actores` - Catálogo de actores (Agrupadores RBAC)
- :doc:`glosario` - Términos y definiciones
- :doc:`restricciones` - Restricciones de arquitectura (CNST)

2. Catálogo de Casos de Uso
===========================

Los casos de uso están organizados por módulos funcionales. Selecciona un módulo para ver
el detalle de sus casos de uso:

.. toctree::
   :maxdepth: 2
   :caption: Módulos de Casos de Uso

   auth/index
   users/index
   access/index
   pipeline/index
   reports/index
   alerts/index
   audit/index
   logs/index

3. Trazabilidad
===============

3.1 Matriz UC → Módulos
-----------------------

.. code-block:: text

   ┌──────────────────────────────────────────────────────────────────┐
   │                    DISTRIBUCIÓN DE UC POR MÓDULO                  │
   ├──────────────────────────────────────────────────────────────────┤
   │                                                                   │
   │  UC_AUTH_01 ──► UC_AUTH_05     │  MOD_Auth      │  5 UC          │
   │  UC_USR_01  ──► UC_USR_04      │  MOD_Users     │  4 UC          │
   │  UC_ACC_01  ──► UC_ACC_09      │  MOD_Access    │  9 UC          │
   │  UC_PIP_01  ──► UC_PIP_04      │  MOD_Pipeline  │  4 UC          │
   │  UC_RPT_01  ──► UC_RPT_14      │  MOD_Reports   │  14 UC         │
   │  UC_ALR_01  ──► UC_ALR_05      │  MOD_Alerts    │  5 UC          │
   │  UC_AUD_01  ──► UC_AUD_04      │  MOD_Audit     │  4 UC          │
   │  UC_LOG_01  ──► UC_LOG_04      │  MOD_Logs      │  4 UC          │
   │                                                                   │
   │  ════════════════════════════════════════════════════════════    │
   │                              TOTAL:  49 UC                        │
   └──────────────────────────────────────────────────────────────────┘

4. Historial de Cambios
=======================

.. list-table::
   :widths: 15 15 20 50
   :header-rows: 1

   * - Versión
     - Fecha
     - Autor
     - Cambios
   * - 4.0.0
     - 2026-01-06
     - Equipo IACT
     - Versión inicial v4.0 con nueva numeración UC_MOD_NN
