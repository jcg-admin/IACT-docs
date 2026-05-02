.. meta::
 :artefacto: ARQUITECTURA_SISTEMA_IACT
 :tipo: Arquitectura del Sistema
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-02
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arquitectura-sistema:

===========================
Arquitectura del Sistema
===========================

Vista general del sistema IACT: funcionalidades principales, flujo de
arquitectura y diagramas de flujo de datos (DFD Nivel 0 y Nivel 1).

----

1. Principales Funcionalidades
================================

Las principales funcionalidades del sistema IACT y sus descripciones
son las siguientes:

**Autenticacion JWT**
  Autentica al usuario mediante credenciales (usuario y contrasena).
  Emite un token JWT con vigencia configurable y carga los permisos
  RBAC asociados al usuario. Toda solicitud posterior requiere este
  token valido.

**Acceso a Modulos (Sesion Activa)**
  Una vez autenticado, el usuario accede a los modulos disponibles
  segun su rol: MOD_Reports, MOD_Pipeline ETL, MOD_Logs y
  MOD_Admin. El sistema filtra las opciones visibles en funcion del
  conjunto de funciones RBAC del usuario.

**Cierre de Sesion**
  Invalida el token JWT activo, registra la accion en ``audit_log``
  y termina el acceso del usuario a todos los recursos del sistema.

**Gestion Pipeline ETL** (MOD_Pipeline)
  Permite disparar, monitorear y reintentar el proceso ETL que extrae
  datos del Repositorio IVR (``tbl_historico_*``) y los carga en la
  Base Analitica IVR (``base_ivr_detalle``, ``base_ivr_clientes``)
  via los stored procedures ``sp_etl_*``. El registro de cada
  ejecucion se almacena en la tabla ``etl_runs`` de MariaDB con
  estados ``en_ejecucion``, ``exitoso`` y ``fallido``.

**Consulta de Logs** (MOD_Logs)
  Proporciona acceso a los logs del sistema IVR y al registro de
  auditoria de acciones de usuarios (``audit_log`` en PostgreSQL)
  para trazabilidad operacional y cumplimiento de CNST-006.

**MOD_Reports — Reportes IVR** (MOD_Reports)
  Modulo principal de analisis. Contiene 17 casos de uso de reporte
  que consultan la Base Analitica IVR via el Servicio de Reportes
  (``cursor.callproc`` sobre ``sp_rpt_*``). Todos los reportes
  incluyen ``UC_INC_RPT_01`` para resolver los segmentos del usuario.

**Base Analitica IVR**
  Repositorio de datos transformados (``base_ivr_detalle``,
  ``base_ivr_clientes``) que sirve como fuente exclusiva para todos
  los reportes. Alimentada por el ETL via ``sp_etl_*``.
  Los siete stored procedures de reporte (``sp_rpt_*``) leen
  exclusivamente de esta base.

**Alertas y Notificaciones**
  Notificaciones automaticas sobre umbrales criticos de tasa de
  abandono (BR-016: >30%), estado del pipeline ETL (fallo en
  ``etl_runs``) y ventana de sincronizacion ETL (CNST-008).

**Resolver Segmento** (UC_INC_RPT_01)
  Comportamiento comun incluido por todos los reportes: mapea los
  DIDs RBAC asignados al usuario a segmentos IVR
  (``nacional_A``, ``nacional_B``, ``Puebla``). Implementado por
  ``SegmentResolver`` con ``DID_MAP`` canonico.

**Auditoria de Acceso**
  Registro inmutable de acciones de modificacion en ``audit_log``
  (PostgreSQL). Cubre altas/bajas de usuarios, cambios RBAC,
  disparos manuales de ETL y cualquier accion de escritura sobre
  datos protegidos.

----

2. Arquitectura del Sistema — Diagrama General
================================================

El diagrama siguiente muestra todas las funcionalidades del sistema
en orden de acceso. Representa el flujo completo desde la
autenticacion hasta el cierre de sesion, incluyendo las rutas hacia
los modulos funcionales y sus interdependencias.

Los actores externos son el **Sistema IVR** (fuente de datos de
llamadas) y los **Usuarios IACT** (Supervisores de Operaciones y
Analistas de Datos). El sistema no tiene registro publico: las
cuentas son creadas por el Administrador IACT.

.. uml::
 :caption: Figura 1 — Arquitectura general del Sistema IACT

 @startuml
 skinparam rectangle {
   RoundCorner 10
   BackgroundColor white
   BorderColor #333333
   FontSize 11
 }
 skinparam arrowColor #333333

 rectangle "Sistema IVR\n(Fuente de datos)" as IVR
 rectangle "view_etl_status\n/ view_alerts" as SUP
 rectangle "view_reports\n/ view_dashboard" as ANA

 rectangle "1\nAutenticacion\nJWT" as P1
 rectangle "2\nDashboard IVR" as P2
 rectangle "3\nCierre de\nSesion" as P3
 rectangle "4\nGestion\nPipeline ETL" as P4
 rectangle "5\nConsulta\nde Logs" as P5
 rectangle "6\nMOD Reports\n(Reportes IVR)" as P6
 rectangle "7\nBase Analitica\nIVR" as P7
 rectangle "8\nAlertas y\nNotificaciones" as P8
 rectangle "9\nResolver\nSegmento\nUC_INC_RPT_01" as P9
 rectangle "10\nAuditoria\nde Acceso" as P10

 SUP --> P1
 ANA --> P1
 IVR --> P7

 P1 --> P2
 P2 --> P4
 P2 --> P5
 P2 --> P6
 P2 --> P8
 P6 --> P7
 P4 --> P9
 P7 --> P9
 P5 --> P10
 P8 --> P10
 P9 --> P3
 P10 --> P3

 @enduml

.. note::

 El flujo de datos empieza en la autenticacion JWT (1) a traves de
 la cual el usuario accede a todos los servicios disponibles hasta
 el cierre de sesion (3). Los modulos MOD_Reports (6) y Gestion
 Pipeline ETL (4) dependen de Resolver Segmento (9) para filtrar
 datos por segmento del usuario. La Base Analitica IVR (7) es
 alimentada por el ETL y consumida exclusivamente via
 ``sp_rpt_*``.

----

3. DFD Nivel 0 — Diagrama de Contexto
========================================

El diagrama de contexto muestra el sistema IACT como una caja
negra con sus entidades externas. Las entidades son los
**Usuarios IACT** (consumidores de servicios), el
**Sistema IVR** (proveedor de datos de llamadas) y el
**APScheduler/Cron** (disparador automatico del ETL).

.. uml::
 :caption: Figura 2 — DFD Nivel 0: Sistema IACT como caja negra

 @startuml
 skinparam rectangle {
   BackgroundColor white
   BorderColor #333333
   RoundCorner 5
 }
 skinparam arrowColor #333333

 rectangle "Sistema IVR\n(Fuente de datos)" as IVR
 rectangle "view_etl_status\n/ view_alerts" as SUP
 rectangle "view_reports
/ view_dashboard" as ANA
 rectangle "APScheduler\n/ Cron" as SCH

 rectangle "  1\n  Sistema IACT\n  (Analisis IVR Calls)  " as IACT

 IVR --> IACT : datos IVR raw
 SUP --> IACT : comandos ETL / alertas
 ANA --> IACT : solicitudes de reporte
 SCH --> IACT : disparo ETL automatico
 IACT --> SUP : estado pipeline / alertas
 IACT --> ANA : reportes IVR / dashboard

 @enduml

----

4. DFD Nivel 1 — Sub-procesos del Sistema
==========================================

El DFD Nivel 1 descompone el sistema IACT en sus sub-procesos
numerados con los flujos de datos entre ellos y los almacenes de
datos (``etl_runs``, ``base_ivr_*``, ``audit_log``,
``auth_session``).

.. uml::
 :caption: Figura 3 — DFD Nivel 1: descomposicion de sub-procesos

 @startuml
 skinparam rectangle {
   RoundCorner 10
   BackgroundColor white
   BorderColor #333333
   FontSize 10
 }
 skinparam database {
   BackgroundColor #f5f5f5
   BorderColor #555555
 }
 skinparam arrowColor #333333

 rectangle "Sistema IVR" as IVR
 rectangle "view_etl_status" as SUP
 rectangle "view_reports" as ANA
 rectangle "APScheduler" as SCH

 rectangle "1\nAutenticacion JWT" as P1
 rectangle "2\nDashboard IVR" as P2
 rectangle "3\nCierre de Sesion" as P3
 rectangle "4\nGestion\nPipeline ETL" as P4
 rectangle "5\nConsulta\nde Logs" as P5
 rectangle "6\nMOD Reports" as P6
 rectangle "7\nServicio de\nReportes\nsp_rpt_*" as P7
 rectangle "8\nAlertas" as P8
 rectangle "9\nResolver Segmento\nUC_INC_RPT_01" as P9
 rectangle "10\nAuditoria" as P10

 database "etl_runs" as DS1
 database "base_ivr_*" as DS2
 database "audit_log" as DS3
 database "auth_session" as DS4

 IVR --> P7 : datos IVR raw
 SUP --> P1 : credenciales
 ANA --> P1 : credenciales
 SCH --> P4 : disparo automatico

 P1 --> DS4 : crear sesion
 P1 --> P2 : JWT valido

 P2 --> P4
 P2 --> P5
 P2 --> P6
 P2 --> P8

 P4 --> DS1 : registrar ejecucion
 P4 --> P9

 P7 --> DS2 : leer datos analiticos
 DS2 --> P7

 P6 --> P9
 P9 --> P6 : segmentos del usuario

 DS1 --> P4 : historial ETL
 P5 --> DS3 : consultar logs

 P8 --> P10
 P5 --> P10
 P10 --> DS3 : registrar auditoria
 P9 --> P3
 P10 --> P3

 @enduml

.. note::

 Los almacenes de datos ``etl_runs`` y ``base_ivr_*`` residen en
 **MariaDB**. Los almacenes ``audit_log`` y ``auth_session``
 residen en **PostgreSQL** (tablas operacionales Django). Los
 stored procedures ``sp_rpt_*`` y ``sp_etl_*`` son parte del
 motor MariaDB y no del codigo Python.
