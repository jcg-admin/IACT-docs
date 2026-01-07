.. meta::
   :project: IACT - Call Center Analytics
   :version: 4.0.0
   :date: 2026-01-06
   :status: En Desarrollo

.. _casos-uso-index:

==================================================
Casos de Uso - IACT Call Center Analytics v4.0
==================================================

.. contents:: Tabla de Contenidos
   :depth: 2
   :local:

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
     -
     - **49**
     -

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

2.1 MOD_Auth - Autenticación (5 UC)
-----------------------------------

.. list-table::
   :widths: 15 40 25 20
   :header-rows: 1

   * - ID
     - Nombre
     - Función RBAC
     - Actor
   * - UC_AUTH_01
     - :doc:`auth/UC_AUTH_01_Iniciar_Sesion`
     - (público)
     - Usuario
   * - UC_AUTH_02
     - :doc:`auth/UC_AUTH_02_Cerrar_Sesion`
     - (público)
     - Usuario
   * - UC_AUTH_03
     - :doc:`auth/UC_AUTH_03_Recuperar_Contrasena`
     - AUT-003
     - AGR-006
   * - UC_AUTH_04
     - :doc:`auth/UC_AUTH_04_Cambiar_Contrasena`
     - (público)
     - Usuario
   * - UC_AUTH_05
     - :doc:`auth/UC_AUTH_05_Gestionar_Sesiones`
     - AUT-001, AUT-002, AUT-004
     - AGR-006

2.2 MOD_Users - Gestión de Usuarios (4 UC)
------------------------------------------

.. list-table::
   :widths: 15 40 25 20
   :header-rows: 1

   * - ID
     - Nombre
     - Función RBAC
     - Actor
   * - UC_USR_01
     - :doc:`users/UC_USR_01_Crear_Usuario`
     - USR-001
     - AGR-006
   * - UC_USR_02
     - :doc:`users/UC_USR_02_Consultar_Usuarios`
     - USR-002, USR-005, USR-006
     - AGR-006
   * - UC_USR_03
     - :doc:`users/UC_USR_03_Modificar_Usuario`
     - USR-003, USR-007, USR-008, USR-009
     - AGR-006
   * - UC_USR_04
     - :doc:`users/UC_USR_04_Eliminar_Usuario`
     - USR-004
     - AGR-006

2.3 MOD_Access - Control de Acceso RBAC (9 UC)
----------------------------------------------

.. list-table::
   :widths: 15 40 25 20
   :header-rows: 1

   * - ID
     - Nombre
     - Función RBAC
     - Actor
   * - UC_ACC_01
     - :doc:`access/UC_ACC_01_Asignar_Funciones`
     - ACC-001
     - AGR-007
   * - UC_ACC_02
     - :doc:`access/UC_ACC_02_Revocar_Funciones`
     - ACC-002
     - AGR-007
   * - UC_ACC_03
     - :doc:`access/UC_ACC_03_Consultar_Permisos`
     - ACC-003
     - AGR-007
   * - UC_ACC_04
     - :doc:`access/UC_ACC_04_Asignar_Agrupador`
     - ACC-004
     - AGR-007
   * - UC_ACC_05
     - :doc:`access/UC_ACC_05_Gestionar_SoD`
     - ACC-005
     - AGR-007
   * - UC_ACC_06
     - :doc:`access/UC_ACC_06_Gestionar_Segmentos`
     - ACC-006
     - AGR-007
   * - UC_ACC_07
     - :doc:`access/UC_ACC_07_Asignar_Segmento`
     - USR-010
     - AGR-007
   * - UC_ACC_08
     - :doc:`access/UC_ACC_08_Permiso_Temporal`
     - ACC-001
     - AGR-007
   * - UC_ACC_09
     - :doc:`access/UC_ACC_09_Auditar_Cambios_Acceso`
     - (lectura)
     - AGR-008

2.4 MOD_Pipeline - Supervisión ETL (4 UC)
-----------------------------------------

.. list-table::
   :widths: 15 40 25 20
   :header-rows: 1

   * - ID
     - Nombre
     - Función RBAC
     - Actor
   * - UC_PIP_01
     - :doc:`pipeline/UC_PIP_01_Supervisar_ETL`
     - PIP-001
     - AGR-009
   * - UC_PIP_02
     - :doc:`pipeline/UC_PIP_02_Consultar_Errores_ETL`
     - PIP-002
     - AGR-009
   * - UC_PIP_03
     - :doc:`pipeline/UC_PIP_03_Consultar_Disponibilidad`
     - PIP-003
     - AGR-009
   * - UC_PIP_04
     - :doc:`pipeline/UC_PIP_04_Solicitar_Reintento`
     - PIP-004
     - AGR-009

2.5 MOD_Reports - Reportes y Dashboard (14 UC)
----------------------------------------------

.. list-table::
   :widths: 15 40 25 20
   :header-rows: 1

   * - ID
     - Nombre
     - Función RBAC
     - Actor
   * - UC_RPT_01
     - :doc:`reports/UC_RPT_01_Consultar_Reporte_Trimestral`
     - RPT-001
     - AGR-002, AGR-003
   * - UC_RPT_02
     - :doc:`reports/UC_RPT_02_Consultar_Problemas_Menu`
     - RPT-001
     - AGR-002, AGR-003
   * - UC_RPT_03
     - :doc:`reports/UC_RPT_03_Consultar_Transferencias`
     - RPT-001
     - AGR-002, AGR-003
   * - UC_RPT_04
     - :doc:`reports/UC_RPT_04_Filtrar_Por_Fecha`
     - RPT-003
     - AGR-002, AGR-003
   * - UC_RPT_05
     - :doc:`reports/UC_RPT_05_Filtrar_Por_Centro`
     - RPT-003
     - AGR-002, AGR-003
   * - UC_RPT_06
     - :doc:`reports/UC_RPT_06_Exportar_CSV`
     - RPT-004
     - AGR-003, AGR-004
   * - UC_RPT_07
     - :doc:`reports/UC_RPT_07_Exportar_Excel`
     - RPT-005
     - AGR-003, AGR-004
   * - UC_RPT_08
     - :doc:`reports/UC_RPT_08_Exportar_PDF`
     - RPT-006
     - AGR-003, AGR-004
   * - UC_RPT_09
     - :doc:`reports/UC_RPT_09_Ver_Dashboard`
     - RPT-002
     - AGR-001, AGR-002, AGR-003
   * - UC_RPT_10
     - :doc:`reports/UC_RPT_10_Ver_KPIs`
     - RPT-007
     - AGR-002, AGR-003
   * - UC_RPT_11
     - :doc:`reports/UC_RPT_11_Ver_Tendencias`
     - RPT-008
     - AGR-002, AGR-003
   * - UC_RPT_12
     - :doc:`reports/UC_RPT_12_Ver_Grafico_Hora`
     - RPT-008
     - AGR-002, AGR-003
   * - UC_RPT_13
     - :doc:`reports/UC_RPT_13_Ver_Grafico_Dia`
     - RPT-008
     - AGR-002, AGR-003
   * - UC_RPT_14
     - :doc:`reports/UC_RPT_14_Ver_Distribucion_Centro`
     - RPT-008
     - AGR-002, AGR-003

2.6 MOD_Alerts - Alertas y Notificaciones (5 UC)
------------------------------------------------

.. list-table::
   :widths: 15 40 25 20
   :header-rows: 1

   * - ID
     - Nombre
     - Función RBAC
     - Actor
   * - UC_ALR_01
     - :doc:`alerts/UC_ALR_01_Configurar_Alerta`
     - ALR-002
     - AGR-005
   * - UC_ALR_02
     - :doc:`alerts/UC_ALR_02_Consultar_Alertas`
     - ALR-001
     - AGR-005
   * - UC_ALR_03
     - :doc:`alerts/UC_ALR_03_Pausar_Alerta`
     - ALR-004
     - AGR-005
   * - UC_ALR_04
     - :doc:`alerts/UC_ALR_04_Eliminar_Alerta`
     - ALR-005
     - AGR-005
   * - UC_ALR_05
     - :doc:`alerts/UC_ALR_05_Gestionar_Destinatarios`
     - ALR-003
     - AGR-005

2.7 MOD_Audit - Auditoría (4 UC)
--------------------------------

.. list-table::
   :widths: 15 40 25 20
   :header-rows: 1

   * - ID
     - Nombre
     - Función RBAC
     - Actor
   * - UC_AUD_01
     - :doc:`audit/UC_AUD_01_Consultar_Auditoria`
     - AUD-001, AUD-002
     - AGR-008
   * - UC_AUD_02
     - :doc:`audit/UC_AUD_02_Generar_Reporte_Compliance`
     - AUD-004
     - AGR-008
   * - UC_AUD_03
     - :doc:`audit/UC_AUD_03_Exportar_Auditoria`
     - AUD-003
     - AGR-008
   * - UC_AUD_04
     - :doc:`audit/UC_AUD_04_Registrar_Evento`
     - (sistema)
     - Sistema

2.8 MOD_Logs - Bitácoras Técnicas (4 UC)
----------------------------------------

.. list-table::
   :widths: 15 40 25 20
   :header-rows: 1

   * - ID
     - Nombre
     - Función RBAC
     - Actor
   * - UC_LOG_01
     - :doc:`logs/UC_LOG_01_Consultar_Logs`
     - LOG-001
     - AGR-010
   * - UC_LOG_02
     - :doc:`logs/UC_LOG_02_Filtrar_Logs`
     - LOG-001
     - AGR-010
   * - UC_LOG_03
     - :doc:`logs/UC_LOG_03_Exportar_Logs`
     - LOG-002
     - AGR-010
   * - UC_LOG_04
     - :doc:`logs/UC_LOG_04_Configurar_Retencion`
     - (admin)
     - AGR-009

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

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Documentación Base

   actores
   glosario
   restricciones

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Módulos

   auth/index
   users/index
   access/index
   pipeline/index
   reports/index
   alerts/index
   audit/index
   logs/index