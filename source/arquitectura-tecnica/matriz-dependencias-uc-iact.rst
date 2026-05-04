.. meta::
 :artefacto: MATRIZ_DEPENDENCIAS_UC_IACT
 :tipo: Analisis Arquitectonico
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _matriz-dependencias-uc-iact:

==============================
MATRIZ DEPENDENCIAS UC IACT
==============================

.. note::

 **Analisis canonico de dependencias** entre los 80 casos de uso
 vigentes del catalogo IACT. Producido por el WP
 ``2026-05-01-05-17-20-uc-dependency-matrix-iact`` y promovido a
 ``source/`` por el WP
 ``2026-05-01-06-24-28-promote-matriz-dependencias-to-source``.

 **Documentos vinculados:**

 - :doc:`/arquitectura-tecnica/modelo-dominio-iact` v1.0.0
   (25 clases canonicas, 7 bounded contexts).
 - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` v5.5.0
   (74 funciones RBAC).

 **Convencion de nombres**: identificadores en ingles (clases,
 funciones, atributos); prosa, comentarios y notas en espanol.

----

PARTE 1 — Resumen ejecutivo
===========================

1.1 Resumen ejecutivo
---------------------

El catalogo IACT esta formado por **80 casos de uso** agrupados en
**12 clusters funcionales** (AUTH, USR, ACC, PERM, RPT, ALR, PIP, AUD,
LOG, OPR, SUP, CLI) que operan sobre **25 clases de dominio** distribuidas en
**7 bounded contexts** (Auth, RBAC, Calls, Reports & Metrics,
Pipeline ETL, Alerts, Audit, Logs).

Esta matriz analiza las dependencias estructurales entre los 80 UCs
para identificar:

- **Cuales UCs son criticos** — sin ellos el sistema no entrega su
  valor de negocio (analytics IVR + RBAC granular + auditoria
  compliance).
- **Cual es el flujo minimo end-to-end** que el sistema debe soportar
  para considerarse operativo.
- **Que dependencias son transversales** — invocadas implicitamente
  por casi todos los UCs (autenticacion, verificacion de permiso,
  emision de auditoria).
- **Que dependencias son cuellos de botella** — puntos del grafo cuya
  falla deja sin servicio a varios consumidores aguas abajo.

**Alcance por fase:**

- **Fase 1 (alcance de esta entrega):** analytics IVR + RBAC granular —
  clusters AUTH, USR, ACC, PERM, RPT, ALR, PIP, AUD, LOG (61 UCs base).
  Criticos: maximizar **cohesion** (cada servicio realiza una funcion
  completa y unica) y minimizar **acoplamiento** (clases aisladas del
  efecto rippling).

- **Fase 2 (fuera de scope actual):** operacion del call center —
  clusters OPR, SUP, CLI (19 UCs). Se incluyen en el diseno por
  principio **Open/Closed**: la arquitectura del nucleo permite
  incorporarlos sin modificar Fase 1. Son mencionados en esta matriz
  para que el modelo de dominio los contemple desde el inicio, pero
  **no forman parte de la primera entrega funcional**.

1.2 Distribucion por criticidad
-------------------------------

.. list-table::
 :widths: 25 15 60
 :header-rows: 1

 * - Criticidad
   - UCs
   - Definicion operativa
 * - CRITICOS
   - 8 (10%)
   - Sin estos, IACT Fase 1 no opera. Concentrados en RPT, PIP,
     AUTH y RBAC core.
 * - ALTOS
   - 34 (43%)
   - Esenciales operativos. Sin ellos el sistema funciona en modo
     degradado.
 * - MEDIOS
   - 24 (30%)
   - Funcionalidades importantes prescindibles en una primera
     version funcional.
 * - BAJOS
   - 13 (16%)
   - Opcionales / sub-features avanzadas.
 * - **Fase 2** (OPR/SUP/CLI)
   - 19
   - Operacion del call center. Fuera del scope de Fase 1;
     incluidos por diseno Open/Closed.

**Total catalogo: 8 + 34 + 24 + 13 + 19 (Fase 2) = 80 UCs** (verificado 2.13).
Los 61 de Fase 1 = clusters AUTH, USR, ACC, PERM, RPT, ALR, PIP, AUD, LOG.

1.2.1 Los 8 UCs CRITICOS — Fase 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los CRITICOS de Fase 1 son los que tienen mayor impacto en el
**valor de negocio central**: reportes IVR, dashboard analitico,
pipeline ETL y el nucleo RBAC que los habilita. Sin cualquiera
de ellos el producto no entrega su propuesta de valor.

::

   UC_RPT_01   Ver Dashboard         (UI principal del producto)
   UC_PIP_01   Supervisar ETL        (sin ETL no hay analytics — prereq RPT)
   UC_AUTH_01  Iniciar Sesion        (entrada universal)
   UC_AUTH_04  Cambiar Contrasena    (forzado primer login, CNST-003)
   UC_PERM_07  Verificar Permiso     (gate seguridad universal — T-02)
   UC_USR_02   Consultar Usuarios    (baseline admin RBAC)
   UC_ACC_03   Consultar Permisos    (visibilidad RBAC minima)
   UC_AUD_01   Consultar Auditoria   (compliance mandatorio CNST-025)

.. note::

   UC_OPR_02 (Atender Llamada) pertenece al cluster OPR — **Fase 2**.
   Aparece en el catalogo por diseno Open/Closed (la arquitectura lo
   soporta sin modificar el nucleo), pero no es critico para la
   primera entrega funcional.

1.3 Flujo critico identificado
------------------------------

A diferencia de un ecommerce (Login → Catalogo → Carrito → Pago), el
flujo critico de IACT no es un unico pipeline lineal. IACT es una
**plataforma de analytics IVR + RBAC** con **cuatro caminos criticos
de Fase 1** segun el actor:

**Ruta A — ETL (background)**: pre-requisito de todos los demas
caminos. Sin ETL no hay analytics.

::

   ETL externo (background)
        ↓
   UC_PIP_01  Supervisar ETL
   (carga datos en BD analitica segun ventana CNST-006/008)
        ↓
   Datos analiticos disponibles

**Ruta B — Usuario con view_reports**: camino de **valor de negocio
central** — reportes y dashboard IVR.

::

   UC_AUTH_01 → [primer login: UC_AUTH_04] → UC_PERM_07
        ↓
   UC_RPT_01  Ver Dashboard  ← valor principal del producto

**Ruta C — Administrador RBAC**: camino de bootstrap y administracion.

::

   UC_AUTH_01 → UC_PERM_07
        ↓
   UC_USR_02 + UC_ACC_03 (visibilidad RBAC minima)

**Ruta D — Auditor**: camino de compliance (CNST-025).

::

   UC_AUTH_01 → UC_PERM_07
        ↓
   UC_AUD_01  Consultar Auditoria

.. note::

   La operacion del call center (Ruta E: OPR / SUP / CLI) es **Fase 2**
   y no forma parte del flujo critico de la primera entrega.

1.4 Tres dependencias transversales
-----------------------------------

.. list-table::
 :widths: 15 25 60
 :header-rows: 1

 * - ID
   - Nombre
   - Cobertura
 * - **T-01**
   - Sesion activa (CNST-003)
   - 78 / 80 UCs (todos no publicos). Pre-condicion universal.
     Excepciones: UC_AUTH_01 + UC_CLI_01..05 (actores publicos sin sesion).
 * - **T-02**
   - Verificar permiso (UC_PERM_07)
   - 78 / 80 UCs. Invocado implicitamente en cada request.
     Excepciones: UC_AUTH_01 + UC_CLI_01..05 (sin RBAC propio).
 * - **T-03**
   - Emitir AuditEvent (CNST-025)
   - 39 / 80 UCs (todas las operaciones de escritura).
     Incluye OPR-02/05/06 (call state changes) y SUP-02 (barge-in).

1.5 Densidad del grafo
----------------------

::

   Nodos:                       80 UCs
   Aristas REQUIERE explicitas: ~90
   Aristas T-01:                78
   Aristas T-02:                78
   Aristas T-03:                35
   UCs raiz (REQUIERE = none):  23
   Camino critico minimo:       4 UCs
   Centralidad alta:            UC_AUTH_01, UC_PERM_07, UC_PIP_01

----

PARTE 2 — Tabla maestra de los 80 UCs
=====================================

Ficha por UC organizada por los 12 clusters. Cada ficha incluye los
campos clave para analisis de dependencias.

2.0 Convenciones de la ficha
----------------------------

Cada UC se documenta con:

- **Criticidad** — CRITICO / ALTO / MEDIO / BAJO.
- **Complejidad** — ALTA / MEDIA / BAJA y dias estimados.
- **Actor** — actor primario.
- **Incluye** — operaciones internas.
- **Patrones** — patrones de diseno aplicables.
- **Clase Dominio** — clases canonicas tocadas.
- **Funcion RBAC** — funciones de modelo-rbac-iact v5.5.0.
- **Dependencias** — UCs que invoca o requiere.
- **Cat Z.2.A** — categoria del programa Z.2.A (1..5).

2.1 Cluster AUTH (5 UCs)
------------------------

Responsabilidad: gate de entrada al sistema, gestion del ciclo de
vida de Session, y notificacion de cambios sensibles via
InternalMailbox. **2 CRITICOS + 2 ALTOS + 1 MEDIO**.

.. list-table::
 :widths: 18 12 10 25 35
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio (primaria + secundarias)
 * - UC_AUTH_01 Iniciar Sesion
   - CRITICO
   - 5
   - publico (post-login AUTH-001)
   - ``Session``, ``User``, ``AuditEvent``
 * - UC_AUTH_02 Cerrar Sesion
   - ALTO
   - 1
   - sesion propia
   - ``Session``, ``AuditEvent``
 * - UC_AUTH_03 Recuperar Contrasena
   - MEDIO
   - 3
   - AUTH-003 ``reset_password``
   - ``User``, ``InternalMailbox``, ``AuditEvent``
 * - UC_AUTH_04 Cambiar Contrasena
   - CRITICO
   - 2
   - usuario sobre si mismo
   - ``User``, ``AuditEvent``
 * - UC_AUTH_05 Gestionar Sesiones
   - ALTO
   - 3
   - AUTH-001/002/004
   - ``Session``, ``User``, ``AuditEvent``

2.2 Cluster USR (4 UCs)
-----------------------

Responsabilidad: CRUD del catalogo de usuarios. Toda modificacion
con ciclo de vida soft-delete (BR-009 v2.0.0). **1 CRITICO + 3 ALTOS**.

.. list-table::
 :widths: 18 12 10 25 35
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_USR_01 Crear Usuario
   - ALTO
   - 4
   - USR-001 ``create_users``
   - ``User``, ``Assignment``, ``AccessGroup``, ``AuditEvent``
 * - UC_USR_02 Consultar Usuarios
   - CRITICO
   - 3
   - USR-005, USR-009
   - ``User``, ``Assignment``, ``AccessGroup``
 * - UC_USR_03 Modificar Usuario
   - ALTO
   - 3
   - USR-002 ``update_users``
   - ``User``, ``Session``, ``AuditEvent``
 * - UC_USR_04 Eliminar (Deactivate) Usuario
   - ALTO
   - 2
   - USR-003 ``deactivate_users`` (rename Z.2 D-01)
   - ``User``, ``Session``, ``AuditEvent``

2.3 Cluster ACC (7 UCs)
-----------------------

Responsabilidad: asignar/revocar funciones, agrupadores
predefinidos, permisos excepcionales y reglas SoD.
**1 CRITICO + 4 ALTOS + 1 MEDIO + 1 BAJO**.

.. list-table::
 :widths: 18 12 10 25 35
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_ACC_01 Asignar Funciones
   - ALTO
   - 4
   - ACC-001 ``assign_functions``
   - ``Assignment``, ``Function``, ``User``, ``AuditEvent``
 * - UC_ACC_02 Revocar Funciones
   - ALTO
   - 2
   - ACC-002 ``revoke_functions``
   - ``Assignment``, ``Function``, ``User``, ``AuditEvent``
 * - UC_ACC_03 Consultar Permisos
   - CRITICO
   - 3
   - ACC-003 ``view_assignments``
   - ``Assignment``, ``Function``, ``User``
 * - UC_ACC_04 Asignar Agrupador
   - ALTO
   - 2
   - ACC-004 ``assign_function_groups``
   - ``Assignment``, ``AccessGroup``, ``User``, ``AuditEvent``
 * - UC_ACC_05 Gestionar SoD
   - ALTO
   - 5
   - ACC-005/011/012 (per Z.2 D-01)
   - ``SeparationRule``, ``Function``, ``AuditEvent``
 * - UC_ACC_08 Permiso Temporal
   - MEDIO
   - 3
   - ACC-001 (reuso)
   - ``ExceptionalPermission``, ``User``, ``Function``, ``AuditEvent``
 * - UC_ACC_09 Auditar Cambios de Acceso
   - BAJO
   - 2
   - AUD-001 ``view_audit_log``
   - ``AuditEvent``, ``User``, ``Assignment``

2.4 Cluster PERM (10 UCs) — vista tecnica del RBAC
--------------------------------------------------

Responsabilidad: vista tecnica de las operaciones RBAC, coexistencia
con ACC declarada en ADR-GOB-008. **1 CRITICO + 5 ALTOS + 2 MEDIOS +
2 BAJOS**.

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio (primaria)
 * - UC_PERM_01 Asignar Grupo a Usuario
   - ALTO
   - 2
   - ACC-004
   - ``Assignment``
 * - UC_PERM_02 Revocar Grupo a Usuario
   - ALTO
   - 2
   - ACC-008
   - ``Assignment``
 * - UC_PERM_03 Conceder Permiso Excepcional
   - MEDIO
   - 3
   - ACC-009
   - ``ExceptionalPermission``
 * - UC_PERM_04 Revocar Permiso Excepcional
   - MEDIO
   - 1
   - ACC-010
   - ``ExceptionalPermission``
 * - UC_PERM_05 Crear Grupo de Permisos
   - ALTO
   - 2
   - ACC-006
   - ``FunctionGroup``
 * - UC_PERM_06 Asignar Funciones a Grupo
   - ALTO
   - 3
   - ACC-007
   - ``FunctionGroup``, ``Function``
 * - UC_PERM_07 Verificar Permiso de Usuario
   - CRITICO
   - 4
   - ACC-003
   - ``Assignment``, ``ExceptionalPermission``
 * - UC_PERM_08 Generar Menu Dinamico
   - ALTO
   - 3
   - CNST-032 SQL ``get_user_menu``
   - ``Assignment``, ``Function``
 * - UC_PERM_09 Auditar Acceso
   - BAJO
   - 1
   - AUD-001
   - ``AuditEvent``
 * - UC_PERM_10 Consultar Auditoria de Permisos
   - BAJO
   - 2
   - AUD-002
   - ``AuditEvent``

2.5 Cluster RPT (16 UCs)
------------------------

Responsabilidad: visualizacion de metricas del call center,
exportacion, programacion, vistas guardadas, instancias por scope.
**1 CRITICO + 3 ALTOS + 10 MEDIOS + 2 BAJOS** (incl. UC_INC_RPT_01).

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio (primaria)
 * - UC_RPT_01 Ver Dashboard
   - CRITICO
   - 5
   - ``view_reports``
   - ``Report`` (scope=GENERAL)
 * - UC_RPT_02 Ver Metricas Tiempo Real
   - ALTO
   - 4
   - ``view_dashboard``
   - ``Report``
 * - UC_RPT_03 Ver Reportes Historicos
   - ALTO
   - 4
   - ``filter_reports``
   - ``Report``
 * - UC_RPT_04 Exportar Reporte (Larman)
   - ALTO
   - 6
   - ``export_csv`` / ``export_excel`` / ``export_pdf``
   - ``ExportJob``
 * - UC_RPT_07 Programar Reporte
   - MEDIO
   - 3
   - ``schedule_report``
   - ``ScheduledReport``
 * - UC_RPT_08 Ver Reportes Programados
   - MEDIO
   - 2
   - ``view_reports`` (filtrada)
   - ``ScheduledReport``
 * - UC_RPT_09 Configurar Filtros
   - BAJO
   - 2
   - ``filter_reports`` (preset)
   - ``Report``
 * - UC_RPT_10 Guardar Vista
   - BAJO
   - 2
   - ``save_view``
   - ``SavedView``
 * - UC_RPT_11 Compartir Reporte
   - MEDIO
   - 3
   - ``share_report``
   - ``Report``, ``InternalMailbox``
 * - UC_RPT_12 Ver Reporte Agentes
   - MEDIO
   - 2
   - ``view_reports`` (variante AGENTS)
   - ``Report``, ``Call``
 * - UC_RPT_13 Ver Reporte Colas
   - MEDIO
   - 2
   - ``view_reports`` (variante QUEUES)
   - ``Report``, ``Call``
 * - UC_RPT_14 Ver Reporte Campanas
   - MEDIO
   - 2
   - ``view_reports`` (variante CAMPAIGNS)
   - ``Report``, ``Campaign``
 * - UC_RPT_15 Reporte Transferencias Centro
   - MEDIO
   - 3
   - ``view_reports`` (instancia D-10)
   - ``Report`` (scope=TRANSFERENCES)
 * - UC_RPT_16 Reporte Menus IVR
   - MEDIO
   - 3
   - ``view_reports`` (instancia D-10)
   - ``Report`` (scope=IVR_MENUS)
 * - UC_RPT_17 Reporte Clientes Unicos
   - MEDIO
   - 3
   - ``view_reports`` (instancia D-10)
   - ``Report`` (scope=UNIQUE_CLIENTS)

2.6 Cluster ALR (5 UCs)
-----------------------

Responsabilidad: closed-loop alerting. **0 CRITICOS + 3 ALTOS +
2 MEDIOS**.

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_ALR_01 Configurar Umbrales
   - ALTO
   - 3
   - ALR-002 ``configure_thresholds``
   - ``Threshold``, ``Metric``
 * - UC_ALR_02 Ver Alertas Activas
   - ALTO
   - 2
   - ALR-001 ``view_alerts``
   - ``Alert``
 * - UC_ALR_03 Reconocer Alerta
   - ALTO
   - 2
   - ALR-007 ``acknowledge_alert`` (NUEVA Z.2 D-02)
   - ``Alert``, ``AuditEvent``
 * - UC_ALR_04 Ver Historial Alertas
   - MEDIO
   - 2
   - ALR-006
   - ``Alert``
 * - UC_ALR_05 Gestionar Suscripciones (Larman)
   - MEDIO
   - 4
   - ALR-008/009/010 (split Z.2 D-03)
   - ``Subscription``, ``Alert``, ``InternalMailbox``

2.7 Cluster PIP (4 UCs)
-----------------------

Responsabilidad: supervision del pipeline ETL. **1 CRITICO + 3 ALTOS**.

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_PIP_01 Supervisar ETL
   - CRITICO
   - 4
   - PIP-001 ``view_pipeline_status``
   - ``ETLEjecucion``
 * - UC_PIP_02 Consultar Errores ETL
   - ALTO
   - 2
   - PIP-002 ``view_pipeline_errors``
   - ``ETLEjecucion``
 * - UC_PIP_03 Consultar Disponibilidad
   - ALTO
   - 2
   - PIP-003 ``view_data_availability``
   - ``ETLEjecucion``
 * - UC_PIP_04 Solicitar Reintento
   - ALTO
   - 3
   - PIP-004 ``request_pipeline_retry``
   - ``ETLEjecucion``, ``AuditEvent``

2.8 Cluster AUD (4 UCs)
-----------------------

Responsabilidad: auditoria inmutable (CNST-025). **1 CRITICO +
2 ALTOS + 1 MEDIO**.

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_AUD_01 Consultar Auditoria
   - CRITICO
   - 3
   - AUD-001 ``view_audit_log``
   - ``AuditEvent``
 * - UC_AUD_02 Buscar Auditoria
   - ALTO
   - 3
   - AUD-002 ``search_audit_log``
   - ``AuditEvent``
 * - UC_AUD_03 Exportar Auditoria
   - ALTO
   - 3
   - AUD-003 ``export_audit_log``
   - ``AuditEvent``, ``ExportJob``
 * - UC_AUD_04 Generar Reporte Compliance
   - MEDIO
   - 5
   - AUD-004 ``generate_compliance_report``
   - ``AuditEvent``

2.9 Cluster LOG (7 UCs)
-----------------------

Responsabilidad: logs aplicativos / ETL / infraestructura mas
SystemHealth (snapshot) y TechnicalMetric (agregacion, no log per
Z.2 D-05). **0 CRITICOS + 2 ALTOS + 2 MEDIOS + 3 BAJOS**.

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_LOG_01 Consultar Logs Sistema
   - ALTO
   - 2
   - LOG-001 ``view_application_logs`` (rename Z.2 D-05)
   - ``ApplicationLog``
 * - UC_LOG_02 Consultar Logs ETL
   - ALTO
   - 2
   - LOG-004 ``view_etl_logs`` (NUEVA)
   - ``ETLLog``, ``ETLEjecucion``
 * - UC_LOG_03 Buscar Logs
   - BAJO
   - 3
   - LOG-003 ``search_logs`` (NUEVA)
   - ``ApplicationLog``
 * - UC_LOG_04 Exportar Logs
   - MEDIO
   - 3
   - LOG-002 ``export_logs``
   - ``ApplicationLog``, ``ExportJob``
 * - UC_LOG_05 Ver Logs Infraestructura
   - MEDIO
   - 2
   - LOG-005 ``view_infrastructure_logs`` (NUEVA)
   - ``InfrastructureLog``
 * - UC_LOG_06 Ver Estado Sistema
   - BAJO
   - 2
   - LOG-006 ``view_system_health`` (NUEVA)
   - ``SystemHealth``
 * - UC_LOG_07 Ver Metricas Tecnicas
   - BAJO
   - 3
   - LOG-007 ``view_technical_metrics`` (NUEVA)
   - ``TechnicalMetric``

2.10 Cluster OPR (10 UCs) — Fase 2
------------------------------------

.. note::

   **Fase 2 — fuera del scope de la primera entrega funcional.**
   Incluido en el catalogo por principio **Open/Closed**: el modelo
   de dominio soporta estos UCs sin modificar el nucleo de Fase 1
   (clusters AUTH..LOG). UC_OPR_02 era CRITICO en versiones anteriores
   de esta matriz; fue reclasificado al consolidar el alcance por fases.

Responsabilidad: operacion del agente en el call center — ciclo de vida
de estado, atencion de llamadas, transferencia, disposicion y
autogestion. **0 CRITICOS (Fase 1) + 4 ALTOS + 3 MEDIOS + 2 BAJOS** +
UC_OPR_02 (CRITICO de Fase 2).

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_OPR_01 Cambiar Estado del Agente
   - ALTO
   - 2
   - OPR-001 ``manage_own_agent_state``
   - ``AgentState``, ``AgentSession``
 * - UC_OPR_02 Atender Llamada Entrante
   - CRITICO
   - 2
   - OPR-002 ``receive_inbound_calls``
   - ``Call``, ``AgentSession``
 * - UC_OPR_03 Realizar Llamada Saliente
   - ALTO
   - 3
   - OPR-003 ``place_outbound_calls``
   - ``Call``, ``AgentSession``
 * - UC_OPR_04 Hold / Unhold Llamada
   - MEDIO
   - 2
   - OPR-004 ``hold_resume_calls``
   - ``Call``
 * - UC_OPR_05 Transferir Llamada
   - ALTO
   - 2
   - OPR-005 ``transfer_calls``
   - ``Call``, ``TransferEvent``
 * - UC_OPR_06 Ingresar Disposition
   - ALTO
   - 2
   - OPR-006 ``submit_call_disposition``
   - ``Call``, ``Disposition``
 * - UC_OPR_07 Solicitar Break / Pausa
   - MEDIO
   - 2
   - OPR-007 ``request_break``
   - ``AgentState``
 * - UC_OPR_08 Ver Propio Dashboard
   - MEDIO
   - 2
   - OPR-008 ``view_own_performance``
   - ``AgentDashboard``
 * - UC_OPR_09 Ver Propio Historial de Llamadas
   - BAJO
   - 3
   - OPR-009 ``view_own_call_history``
   - ``Call``, ``AgentSession``
 * - UC_OPR_10 Recibir Notificacion Supervisor
   - BAJO
   - 2
   - OPR-010 ``read_own_mailbox``
   - ``InternalMailbox``

2.11 Cluster SUP (3 UCs) — Fase 2
-----------------------------------

.. note::

   **Fase 2 — fuera del scope de la primera entrega funcional.**

Responsabilidad: supervision en tiempo real del equipo de agentes —
monitoreo de llamadas activas, intervencion y comunicacion de equipo.
**0 CRITICOS + 1 ALTO + 1 MEDIO + 1 BAJO**.

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_SUP_01 Monitorear Llamada (Whisper)
   - ALTO
   - 3
   - SUP-001 ``monitor_live_calls``
   - ``Call``, ``AgentSession``
 * - UC_SUP_02 Barge-in en Llamada
   - MEDIO
   - 3
   - SUP-002 ``barge_in_calls``
   - ``Call``, ``AgentSession``
 * - UC_SUP_03 Mensaje Broadcast al Equipo
   - BAJO
   - 2
   - SUP-003 ``broadcast_team_messages``
   - ``InternalMailbox``

2.12 Cluster CLI (5 UCs) — Fase 2
-----------------------------------

.. note::

   **Fase 2 — fuera del scope de la primera entrega funcional.**

Responsabilidad: ciclo de vida del llamante externo — desde marcado
hasta calificacion post-atencion. Actor sin RBAC; interactua con el
PBX y el IVR. **0 CRITICOS + 2 ALTOS + 1 MEDIO + 2 BAJOS**.

.. list-table::
 :widths: 22 12 10 26 30
 :header-rows: 1

 * - UC
   - Criticidad
   - Dias
   - Funcion RBAC
   - Clase Dominio
 * - UC_CLI_01 Iniciar Llamada al Call Center
   - ALTO
   - 1
   - (ninguna — actor externo sin RBAC)
   - ``Call``, ``tbl_historico_*``
 * - UC_CLI_02 Navegar IVR
   - ALTO
   - 1
   - (ninguna — actor externo sin RBAC)
   - ``Call``, ``tbl_historico_*``
 * - UC_CLI_03 Esperar en Cola
   - MEDIO
   - 1
   - (ninguna — actor externo sin RBAC)
   - ``Call``, ``AgentSession``
 * - UC_CLI_04 Solicitar Callback
   - BAJO
   - 2
   - (ninguna — actor externo sin RBAC)
   - ``Call``
 * - UC_CLI_05 Calificar Atencion (Post-Call)
   - BAJO
   - 1
   - (ninguna — actor externo sin RBAC)
   - ``Call``, ``base_ivr_*``

2.13 Verificacion cuantitativa
------------------------------

.. list-table::
 :widths: 14 10 10 10 10 12
 :header-rows: 1

 * - Cluster
   - Criticos
   - Altos
   - Medios
   - Bajos
   - Total
 * - AUTH
   - 2
   - 2
   - 1
   - 0
   - 5
 * - USR
   - 1
   - 3
   - 0
   - 0
   - 4
 * - ACC
   - 1
   - 4
   - 1
   - 1
   - 7
 * - PERM
   - 1
   - 5
   - 2
   - 2
   - 10
 * - RPT
   - 1
   - 3
   - 10
   - 2
   - 16
 * - ALR
   - 0
   - 3
   - 2
   - 0
   - 5
 * - PIP
   - 1
   - 3
   - 0
   - 0
   - 4
 * - AUD
   - 1
   - 2
   - 1
   - 0
   - 4
 * - LOG
   - 0
   - 2
   - 2
   - 3
   - 7
 * - OPR
   - 1
   - 4
   - 3
   - 2
   - 10
 * - SUP
   - 0
   - 1
   - 1
   - 1
   - 3
 * - CLI
   - 0
   - 2
   - 1
   - 2
   - 5
 * - **Total**
   - **9**
   - **34**
   - **24**
   - **13**
   - **80**

----

PARTE 3 — Matriz compacta UC → INCLUYE → EXTIENDE → REQUIERE
============================================================

Vista tecnica una linea por UC. Las dependencias transversales (T-01,
T-02, T-03) se omiten aqui — viven en Parte 4.

3.1 UCs raiz (REQUIERE = ninguno)
---------------------------------

23 UCs no requieren otro UC explicito (solo transversales):

::

   UC_AUTH_01, UC_USR_02, UC_ACC_03, UC_ACC_05,
   UC_PERM_05, UC_PERM_07, UC_RPT_01 (con prereq datos),
   UC_ALR_01, UC_PIP_01, UC_AUD_01,
   UC_LOG_01, UC_LOG_05, UC_LOG_06, UC_LOG_07
   + 4 menores

3.2 UCs con mayor in-degree
---------------------------

::

   UC_AUTH_01      universal (T-01, todos los UCs no publicos)
   UC_PERM_07      universal (T-02)
   UC_RPT_01       14 invocaciones (todo el cluster RPT)
   UC_PIP_01       4 invocaciones (PIP_02..04, LOG_02)
   UC_AUD_01       4 invocaciones (AUD_02..04, ACC_09, PERM_09)
   UC_USR_02       3 invocaciones (USR_03, USR_04, ACC_04)
   UC_AUTH_05      3 invocaciones (USR_03, USR_04, AUTH_02)

3.3 Cadenas de dependencia por cluster
--------------------------------------

**Cluster AUTH (intra)**::

   UC_AUTH_01 → (raiz)
   UC_AUTH_02 → UC_AUTH_01
   UC_AUTH_03 → UC_USR_03 (cross USR)
   UC_AUTH_04 → UC_AUTH_01
   UC_AUTH_05 → UC_AUTH_01, UC_AUTH_02

**Cluster USR (intra + cross)**::

   UC_USR_01 → UC_ACC_01, UC_ACC_04
   UC_USR_02 → (raiz)
   UC_USR_03 → UC_USR_02, UC_AUTH_05
   UC_USR_04 → UC_USR_02, UC_AUTH_05

**Cluster ACC (intra + cross AUD)**::

   UC_ACC_01 → UC_ACC_05
   UC_ACC_02 → UC_ACC_01
   UC_ACC_03 → (raiz)
   UC_ACC_04 → UC_USR_02, UC_ACC_03
   UC_ACC_05 → (raiz)
   UC_ACC_08 → UC_ACC_03
   UC_ACC_09 → UC_AUD_01

**Cluster PERM (vista tecnica del RBAC)**::

   UC_PERM_01 → UC_PERM_05
   UC_PERM_02 → UC_PERM_01
   UC_PERM_03 → UC_PERM_04 (caso inverso)
   UC_PERM_04 → UC_PERM_03
   UC_PERM_05 → (raiz)
   UC_PERM_06 → UC_PERM_05, UC_ACC_05
   UC_PERM_07 → (raiz, requerido por TODO UC operativo)
   UC_PERM_08 → UC_PERM_07
   UC_PERM_09 → UC_AUD_01
   UC_PERM_10 → UC_AUD_02

**Cluster RPT (15 UCs, hub: RPT_01 + cross PIP)**::

   UC_RPT_01 → UC_PIP_01 (datos analiticos)
   UC_RPT_02 → UC_RPT_01, UC_ALR_01, UC_ALR_02
   UC_RPT_03 → UC_RPT_01
   UC_RPT_04 → UC_RPT_01
   UC_RPT_07 → UC_RPT_01, UC_RPT_04
   UC_RPT_08 → UC_RPT_07
   UC_RPT_09 → UC_RPT_03, UC_RPT_10
   UC_RPT_10 → UC_RPT_03, UC_RPT_09
   UC_RPT_11 → UC_RPT_01
   UC_RPT_12 → UC_RPT_01
   UC_RPT_13 → UC_RPT_01
   UC_RPT_14 → UC_RPT_01
   UC_RPT_15 → UC_RPT_03, UC_RPT_04
   UC_RPT_16 → UC_RPT_03, UC_RPT_04
   UC_RPT_17 → UC_RPT_03, UC_RPT_04

**Cluster ALR (closed-loop)**::

   UC_ALR_01 → (raiz)
   UC_ALR_02 → UC_ALR_01
   UC_ALR_03 → UC_ALR_02
   UC_ALR_04 → UC_ALR_02
   UC_ALR_05 → UC_ALR_01, UC_ALR_02

**Cluster PIP (cluster cerrado + 1 cross LOG)**::

   UC_PIP_01 → (raiz, prereq de RPT)
   UC_PIP_02 → UC_PIP_01
   UC_PIP_03 → UC_PIP_01
   UC_PIP_04 → UC_PIP_01, UC_PIP_02

**Cluster AUD (consumidor universal de AuditEvent)**::

   UC_AUD_01 → (raiz, hub de auditoria)
   UC_AUD_02 → UC_AUD_01
   UC_AUD_03 → UC_AUD_01 o UC_AUD_02
   UC_AUD_04 → UC_AUD_01, UC_AUD_03

**Cluster LOG (con cross PIP)**::

   UC_LOG_01 → (raiz)
   UC_LOG_02 → UC_PIP_01 (cross-cluster)
   UC_LOG_03 → UC_LOG_01
   UC_LOG_04 → UC_LOG_01 o UC_LOG_03
   UC_LOG_05 → (raiz)
   UC_LOG_06 → (raiz)
   UC_LOG_07 → (raiz)

----

PARTE 4 — Dependencias transversales en detalle
===============================================

4.1 Dependencia T-01 — Sesion activa
------------------------------------

**Definicion**: cualquier UC operativo (no publico) requiere una
``Session.state = ACTIVE`` valida.

**Cobertura**: 78 / 80. Excepciones: UC_AUTH_01 + UC_CLI_01..05 y
UC_AUTH_03 (paso de validacion de token de recuperacion).

**Mecanismo**: middleware HTTP que extrae el token de autenticación del header
``Authorization``, valida firma + expiracion (CNST-002), resuelve
Session, verifica ``state = ACTIVE``, aplica CNST-003 (sesion unica).
Falla → 401.

**Riesgo**: SPOF del producto. Mitigado con replica BD, cache local
TTL CNST-002, health check en UC_LOG_06.

4.2 Dependencia T-02 — Verificar permiso
----------------------------------------

**Definicion**: cualquier UC operativo invoca implicitamente
UC_PERM_07 con el par ``(user_id, function_id)`` antes de ejecutar
su flujo.

**Cobertura**: 78 / 80.

**Orden de precedencia interno** (UC_PERM_07):

1. Revocaciones excepcionales (state ACTIVE, fecha vigente) →
   DENEGADO.
2. Concesiones excepcionales (CNST-031) → AUTORIZADO.
3. Asignaciones por FunctionGroup → AUTORIZADO.
4. Asignaciones directas → AUTORIZADO.
5. Sin match → DENEGADO.

**Mecanismo**: decorador ``@require_function('<codename>')`` sobre cada
controller. Cache LRU TTL ~60s. Invalidacion al ejecutar UC_ACC_01,
_02, UC_PERM_01..04, _06.

**Performance target**: < 50 ms (per cabecera de UC_PERM_07).

**Riesgo**: politica IACT es **fail-closed estricto** (CNST-030). Si
T-02 falla deniega — peor que T-01 pero mejor que bypass total RBAC.

4.3 Dependencia T-03 — Emitir AuditEvent
----------------------------------------

**Definicion**: toda operacion de **escritura** en cualquier cluster
emite uno o mas ``AuditEvent`` inmutables (CNST-025).

**Cobertura**: 39 / 80 UCs (los de escritura). Los 41 UCs restantes
son lectura pura.

**Mecanismo**: middleware "audit emitter" como observer de los
metodos de servicio de escritura. Cada metodo declara ``EventType``
via decorador ``@audits('PERMISSION_GRANT')``. Insercion **post-commit**
en transaccion separada (la falla del audit no aborta la operacion
pero genera alarma).

**Riesgo**: si T-03 falla silenciosamente, perdida de compliance.
Mitigado con health check del servicio audit en UC_LOG_06, alerta
automatica si rate baja debajo de baseline (UC_ALR_03), reconciliacion
periodica via UC_AUD_04.

----

PARTE 5 — Matriz de criticidad y duracion
=========================================

5.1 Metodo de estimacion
------------------------

.. list-table::
 :widths: 20 20 60
 :header-rows: 1

 * - Complejidad
   - Dias tipicos
   - Criterio
 * - BAJA
   - 1-2
   - Un solo flujo principal, sin alternos significativos, ≤3
     constraints, ≤2 clases tocadas.
 * - MEDIA
   - 3-4
   - 1-2 flujos alternos, 3-5 constraints, hasta 4 clases, validacion
     moderada.
 * - ALTA
   - 5-7
   - Flujos asincronos, transacciones distribuidas (Saga),
     multiples clases, integracion externa, performance critico.

Asumido: 1 desarrollador full-time (~6h productivas/dia). Incluye
analisis + implementacion + tests + code review + documentacion.

5.2 Totales por criticidad
--------------------------

.. list-table::
 :widths: 30 15 25 15
 :header-rows: 1

 * - Criticidad
   - UCs
   - Person-days
   - Porcentaje
 * - CRITICOS
   - 8
   - 29
   - 17%
 * - ALTOS
   - 27
   - 75
   - 44%
 * - MEDIOS
   - 18
   - 49
   - 29%
 * - BAJOS
   - 8
   - 17
   - 10%
 * - **Total UCs**
   - **61**
   - **170**
   - **100%**

5.3 Overhead del proyecto
-------------------------

::

   Modelo de datos (migraciones para 25 clases)        15 dias
   Middleware Auth + RBAC (T-01 + T-02)                10 dias
   Middleware Audit Emitter (T-03)                      5 dias
   Diseno de UI / componentes compartidos              20 dias
   ETL pipeline (background)                           15 dias
   Setup infraestructura (ADR-DEVOPS-001)               8 dias
   Tests E2E + ambientes                               10 dias
   Documentacion + ADRs                                 5 dias
   ----------------------------------------------------------
   Subtotal overhead                                   88 dias

   Total proyecto = 170 + 88 = 258 person-days

   Con 1 dev:                       ~52 sem  (~12 meses)
   Con 2 devs:                      ~30 sem  (~7 meses)
   Con 4 devs:                      ~15 sem  (~3.5 meses)

5.4 Timeline propuesto (15 sprints, 2 devs)
-------------------------------------------

::

   Sprint 1-2     Setup + Auth/RBAC core            4 sem
   Sprint 3       Pipeline + Dashboard              2 sem
   Sprint 4-5     Admin RBAC                        4 sem
   Sprint 6       Auditoria                         2 sem
   Sprint 7-8     RBAC avanzado / PERM              4 sem
   Sprint 9-11    Reportes (cluster RPT completo)   6 sem
   Sprint 12      Alertas                           2 sem
   Sprint 13      Pipeline avanzado                 2 sem
   Sprint 14      Logs + monitoring                 2 sem
   Sprint 15      Compliance avanzado               2 sem
   ----------------------------------------------------
   Total          15 sprints                        30 sem

5.5 Reglas de orden topologico
------------------------------

1. UCs con REQUIERE = ninguno se implementan primero.
2. **UC_PERM_07** antes que cualquier UC con T-02.
3. **UC_AUTH_01** antes que cualquier UC con T-01.
4. **UC_PIP_01** antes que cualquier UC del cluster RPT que dependa
   de datos.
5. **UC_RPT_01** antes que UC_RPT_02..17.
6. **UC_AUD_01** antes que UC_AUD_02, _03, _04 y UC_PERM_09, _10,
   UC_ACC_09.

----

PARTE 6 — Patrones de diseno aplicados a IACT
=============================================

6.1 Patrones GoF/POSA aplicados
-------------------------------

.. list-table::
 :widths: 22 12 66
 :header-rows: 1

 * - Patron
   - UCs
   - Funcion en IACT
 * - **Command**
   - 17
   - Audit trail — toda escritura es Command serializado como
     AuditEvent.
 * - **Facade**
   - 16
   - Vista unificada para consultas que agregan datos de multiples
     clases.
 * - **Strategy**
   - 14
   - Algoritmos intercambiables — formato export, search engines,
     cache backends, scope filters.
 * - **Observer**
   - 14
   - Eventos cross-cutting — invalidacion de caches, propagacion de
     cambios, streaming.
 * - **Specification**
   - 14
   - Encapsulacion de criterios de busqueda compuestos.
 * - **State**
   - 7
   - Toda clase con state enum y BR-009 v2.0.0.
 * - **Visitor**
   - 6
   - Operaciones agregadas sobre estructuras complejas (resolucion
     RBAC, metricas).
 * - **Decorator**
   - 4
   - Cache, rate limiting, caducidad.
 * - **Composite**
   - 4
   - Estructuras jerarquicas (menus, dashboards, services_status).
 * - **Memento**
   - 3
   - Snapshots persistentes (SavedView, SystemHealth).
 * - **Builder**
   - 4
   - Construccion paso a paso (username generator, PDF, presets).
 * - **Factory**
   - 2
   - Construccion centralizada de entidades complejas.
 * - **Template Method**
   - 2
   - Workflows con pasos fijos y partes variables.
 * - **Chain of Responsibility**
   - 2
   - Validaciones / precedencia de permisos.
 * - **Saga**
   - 3
   - Transacciones distribuidas async (export jobs).

6.2 Patrones cross-cutting IACT-especificos
-------------------------------------------

Ocho patrones propios del proyecto que emergen del analisis:

**Patron P-01 — RBAC Decorator** (59 UCs):
Decorador ``@require_function('<codename>')`` sobre cada controller.
Materializa T-02 a nivel de codigo. Reduce duplicacion.

**Patron P-02 — Audit Emitter** (35 UCs):
Middleware observer que se suscribe a metodos de escritura. Cada
metodo declara ``EventType`` via decorador. Insercion post-commit en
transaccion separada. Materializa T-03.

**Patron P-03 — BR-009 Soft Delete** (~35 clases):
Cada entidad con ciclo de vida expone atributo ``state`` con enum
especifico y operacion ``deactivate()`` o ``disable()``. Cero clases
con ``delete()``. Materializa BR-009 v2.0.0 alcance global.

**Patron P-04 — Filtered Variant (Camino C)** (5 UCs):
Una unica funcion RBAC (``view_reports``) mas un atributo ``scope``
en ``Report``. Las variantes (RPT_08, _09, _12, _13, _14) no son UCs
autonomos sino instancias filtradas. Materializa Z.2 D-10.

**Patron P-05 — ACC-PERM Coexistence** (10 UCs):
Cada UC_PERM_NN cita la funcion RBAC backing del cluster ACC (1:1
mapping). Operan sobre las mismas clases del dominio (Assignment,
FunctionGroup, ExceptionalPermission). Materializa ADR-GOB-008.

**Patron P-06 — Larman Consolidation** (2 UCs):
Un solo UC (UC_RPT_04 "Exportar Reporte") con flujos alternativos
por formato; tres funciones RBAC distintas (export_csv / export_excel / export_pdf) para
SoD. Capa UC y capa RBAC son ortogonales. Mismo patron en
UC_ALR_05.

**Patron P-07 — Async Throttled Export** (3 UCs):
Cola asincrona abstracta (CNST-019 v3.0.0) + throttling abstracto
por recursos (CNST-020 v3.0.0) + notificacion via InternalMailbox.
UC_RPT_04, UC_AUD_03, UC_LOG_04.

**Patron P-08 — Internal Mailbox Delivery** (6 UCs):
Clase ``InternalMailbox`` 1:1 con ``User``. Toda notificacion
(export listo, recovery password, alerta suscrita, reporte
compartido) entregada via ``InternalMailbox.deliver_message()``.
Materializa CNST-001.

6.3 Componentes infra reutilizables (Stage 7 DESIGN futuro)
-----------------------------------------------------------

Cinco componentes capturan ~80% de la infraestructura cross-cutting:

1. **Decorador** ``@require_function`` (~30 LOC, reutilizado por 59
   UCs).
2. **Middleware** ``AuditEmitter`` (~50 LOC, reutilizado por 35 UCs).
3. **Mixin** ``LifecycleEntity`` con ``state`` + ``deactivate()``
   (~35 clases).
4. **Servicio** ``ExportJobScheduler`` (CNST-019/020 v3.0.0,
   reutilizado por UC_RPT_04, UC_AUD_03, UC_LOG_04).
5. **Servicio** ``InternalMailbox`` (CNST-001, reutilizado por 6 UCs).

----

PARTE 7 — Criterios OOD: cohesion y acoplamiento
=================================================

El criterio central para clasificar la criticidad de un UC en IACT
es su posicion en los ejes de **cohesion** y **acoplamiento** del
modelo OOD (Object-Oriented Design).

7.1 Cohesion
------------

La cohesion describe el grado de relacion interna de un servicio o
clase. Los criterios aplicados son:

**Cohesion de servicio:**
Un servicio realiza una (entera) y solo una funcion. Si para
describirlo se necesitan sentencias compuestas, multiples verbos,
"_y_" u "_o_", el servicio es demasiado complejo y debe partirse.

**Cohesion de clase:**
Los atributos y servicios de una clase deben ser maximos en cohesion:
sin atributos no usados, sin servicios que no sean propios de la
responsabilidad de la clase.

**Cohesion de herencia (generalizacion/especializacion):**
Las jerarquias deben ser coherentes y sensatas. Si las modificaciones
de mantenimiento las descohesionan, hay que redisenar las jerarquias.

**Aplicacion en IACT:**
Los clusters RPT (reportes) y PIP (pipeline ETL) tienen la cohesion
mas alta — cada UC hace exactamente una cosa y la hace completa.
UC_RPT_01 (Ver Dashboard) = un dashboard, un punto de entrada.
UC_PIP_01 (Supervisar ETL) = un estado del pipeline, una vista.

7.2 Acoplamiento
----------------

El acoplamiento describe el grado de interdependencia entre
objetos/clases. Los criterios son:

**Minimo acoplamiento de interacciones (uso o mensajes):**
Si una clase esta conectada con muchas otras, aunque aislada, produce
el efecto *rippling*: una modificacion resuena en todo el sistema.

**Maximo acoplamiento de herencia:**
Debe utilizarse toda la herencia del padre y extenderse solo lo
necesario.

**Evitar el acoplamiento "mensaje pass-through":**
Si una clase intermedia no realiza ninguna tarea (solo es
intermediaria), cualquier cambio en la llamada obliga a modificar los
tres objetos. La solucion es pedir directamente al objeto que interesa.

**Aplicacion en IACT:**

.. list-table::
 :widths: 20 20 60
 :header-rows: 1

 * - UC / Componente
   - Acoplamiento
   - Razon
 * - UC_PERM_07
   - Alto (T-02)
   - 78/80 UCs dependen de el — riesgo de rippling critico.
     Mitigado: interfaz minima ``(user_id, function_id)`` +
     cache LRU. Pass-through controlado.
 * - UC_AUTH_01
   - Alto (T-01)
   - 78/80 UCs lo requieren como prerequisito de sesion.
     Aislado via middleware — no acoplamiento directo UC-a-UC.
 * - UC_RPT_01
   - Medio
   - Hub del cluster RPT (14 UCs extienden). Acoplamiento de
     herencia / extension, no de mensajes.
 * - Clusters OPR/SUP/CLI
   - Bajo (diseno)
   - Fase 2 — diseno Open/Closed asegura que su incorporacion
     no modifica el nucleo. Acoplamiento controlado via
     interfaces del dominio (Call, AgentSession).

**Conclusion OOD:**
La criticidad de un UC es proporcional al impacto de su falla en la
cohesion y acoplamiento del sistema. Los 8 CRITICOS de Fase 1 son
exactamente los que, si fallan, rompen la cohesion de valor del
producto o crean efecto rippling sistemico.

----

Conclusion — metricas y proximos pasos
======================================

C.1 Metricas globales
---------------------

::

   Casos de uso vigentes:           80 (verificado en tabla 2.13)
     └─ Fase 1 (clusters AUTH..LOG): 61 UCs
     └─ Fase 2 (clusters OPR/SUP/CLI): 19 UCs
   Clusters funcionales:            12 (AUTH, USR, ACC, PERM, RPT,
                                     ALR, PIP, AUD, LOG, OPR, SUP, CLI)
   Clases canonicas de dominio:     25
   Bounded contexts:                7
   Funciones RBAC:                  74 (v5.5.0)

   Distribucion criticidad (Fase 1):
     CRITICOS:  8 (RPT_01, PIP_01, AUTH_01, AUTH_04,
                   PERM_07, USR_02, ACC_03, AUD_01)
     ALTOS:    34
     MEDIOS:   24
     BAJOS:    13

   Aristas REQUIERE explicitas:     ~90
   Aristas T-01:                    78 (total catalogo)
   Aristas T-02:                    78 (total catalogo)
   Aristas T-03:                    39 (operaciones escritura)
   UCs raiz:                        23
   Camino critico minimo:            4 UCs

   Person-days UCs (Fase 1):        170
   Person-days overhead:             88
   Person-days total Fase 1:        258
   Sprints propuestos (Fase 1):      15

   Patrones GoF/POSA aplicados:     15 distintos
   Patrones cross-cutting IACT:      8
   Componentes infra reutilizables:  5

C.2 Hallazgos consolidados
--------------------------

.. list-table::
 :widths: 8 15 77
 :header-rows: 1

 * - ID
   - Tipo
   - Descripcion
 * - H-M01
   - OBSERVABLE
   - Los 8 CRITICOS son solo 13% del catalogo pero concentran las 4
     rutas criticas. Su fallo deja el sistema sin valor.
 * - H-M02
   - OBSERVABLE
   - 78/80 UCs requieren T-01 + T-02. El middleware Auth + RBAC es
     el componente con mayor leverage del proyecto.
 * - H-M03
   - OBSERVABLE
   - UC_PERM_07 es el cuello de botella mas critico. Performance
     <50ms requerido; sin cache LRU + invalidacion correcta el
     sistema no escala.
 * - H-M04
   - OBSERVABLE
   - UC_PIP_01 es prerequisito background de todos los UCs RPT y
     ALR. Si el ETL falla, dashboard muestra datos stale. Requiere
     health check + alerta automatica.
 * - H-M05
   - INFERRED
   - Cluster RPT (15 UCs, 41 person-days) es el mas voluminoso. 14
     de 15 UCs RPT extienden UC_RPT_01 — paralelizable tras
     UC_RPT_01.
 * - H-M06
   - OBSERVABLE
   - Los 8 patterns cross-cutting IACT capturan ~80% de la
     infraestructura del sistema. Implementarlos bien es decisivo.
 * - H-M07
   - OBSERVABLE
   - Solo 18 UCs son raices. Implementacion debe respetar orden
     topologico per Parte 5 § 5.5.
 * - H-M08
   - INFERRED
   - Cluster AUD tiene UC_AUD_01 como hub: extendido por UC_AUD_02,
     _03, _04 + UC_PERM_09, _10, UC_ACC_09. Hub mas concentrado del
     sistema.

C.3 Proximos pasos
------------------

**Inmediato:**

1. Cierre del WP analitico
   ``2026-05-01-05-17-20-uc-dependency-matrix-iact``.
2. Promocion del documento a ``source/arquitectura-tecnica/`` (este
   archivo).

**Corto plazo:**

3. Stage 7 DESIGN para implementacion: usar el orden topologico de
   Parte 5 § 5.5 + los 5 componentes cross-cutting de § 6.3 como
   guia de diseno tecnico (modelos / servicios / middleware).
4. Materializar los 8 CRITICOS primero (sprints 1-3).
5. Implementar el middleware T-02 / T-03 junto con UC_PERM_07.

**Mediano plazo:**

6. Validacion con stakeholders reales (cuando esten disponibles).
7. Refinamiento de estimaciones tras los primeros sprints.
8. Visualizaciones PlantUML adicionales del grafo si requeridas.

**Largo plazo:**

9. WP de implementacion real: ADRs de implementacion (módulos de aplicación,
   modelos, vistas, tests) usando ADR-DEVOPS-001.
10. Operacion y monitoreo: aplicar UCs LOG_05/06/07 como
    observabilidad del sistema en produccion.

C.4 Trazabilidad
----------------

Anclajes verificados:

- :doc:`/arquitectura-tecnica/modelo-dominio-iact` v1.0.0.
- :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` v5.5.0.
- WP fundacional: ``2026-05-01-02-01-06-domain-model-canonization``
  (cerrado).
- WP de correcciones:
  ``2026-05-01-03-29-03-uc-corrections-against-canonical-model``
  (cerrado, 61/61 UCs base + 18 nuevos OPR/SUP/CLI en v5.5.0).
- WP analitico:
  ``2026-05-01-05-17-20-uc-dependency-matrix-iact`` (cerrado, 6
  partes + conclusion).
- ADR-GOB-008 — coexistencia ACC ↔ PERM.
- BR-009 v2.0.0, BR-011 v2.0.0.
- CNST-001, _002, _003, _006/007/008, _015, _019 v3.0.0, _020
  v3.0.0, _024, _025, _030, _031, _032.
- Programa Z: Z.1.C, Z.2 (D-01..D-11), Z.2.A (5 categorias Cat 1..5).

C.5 Evolucion del documento
---------------------------

Este es el primer analisis canonico de dependencias del proyecto.
Versionado SemVer 2.0.0 a partir de v1.0.0:

- **MAJOR** cuando cambien las clases del modelo de dominio o el
  catalogo de UCs.
- **MINOR** cuando se agreguen UCs o se refinen criticidades.
- **PATCH** para correcciones documentales sin cambios estructurales.
