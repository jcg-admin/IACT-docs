.. meta::
 :artefacto: ARQUITECTURA_SISTEMA_IACT
 :tipo: Arquitectura del Sistema
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-02
 :ultimo_cambio: 2026-05-04
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
  ejecucion se almacena en la tabla ``etl_runs`` de Almacen de Datos con
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

2. Diagramas de Arquitectura
==============================

Un diagrama por archivo.

.. toctree::
 :maxdepth: 1
 :caption: Diagramas

 ArquitecturaSistema/arquitectura-general
 ArquitecturaSistema/dfd-nivel-0-contexto
 ArquitecturaSistema/dfd-nivel-1-subprocesos
