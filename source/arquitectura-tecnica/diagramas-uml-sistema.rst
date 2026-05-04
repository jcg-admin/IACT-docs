.. meta::
 :artefacto: DIAGRAMAS_UML_SISTEMA_IACT
 :tipo: Indice — Diagramas UML del Sistema
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-02
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _diagramas-uml-sistema:

=========================
Diagramas UML del Sistema
=========================

Coleccion de diagramas UML que documentan la arquitectura, comportamiento
e interacciones del sistema IACT. Los actores se nombran por su grupo
RBAC en ingles (``view_reports``, ``request_pipeline_retry``, etc.)
conforme al catalogo de funciones del sistema.

----

1. Especificacion de Actores (Funciones RBAC)
=============================================

**view_reports**
  Usuario con funcion ``view_reports`` y ``view_dashboard``. Puede
  visualizar el Dashboard IVR y todos los reportes del MOD_Reports.
  Accede via ``GET /api/reportes/`` con filtrado automatico por
  segmento IVR (``UC_INC_RPT_01``).

**view_pipeline_status**
  Usuario con funciones ``view_reports``, ``view_alerts`` y
  ``view_pipeline_status``. Supervisa KPIs de calidad, alertas de umbral
  BR-016 y el estado del pipeline ETL en tiempo real.

**request_pipeline_retry**
  Usuario con funciones ``view_pipeline_status``, ``view_pipeline_errors``,
  ``view_data_availability`` y ``request_pipeline_retry``. Dispara,
  monitorea y reintenta el proceso ETL via ``sp_etl_maestro``.

**assign_functions**
  Usuario con funciones ``create_users``, ``update_users``,
  ``deactivate_users``, ``assign_functions``, ``revoke_functions``.
  Es el unico que puede modificar ``AccessGroup`` y
  ``AccessFunction`` en PostgreSQL.

**view_audit_log**
  Usuario con funciones ``view_audit_log``, ``search_audit_log``,
  ``export_audit_log``. Solo lectura sobre ``audit_log``
  (PostgreSQL). SoD: no puede tener funciones de AGR-006.

**Sistema IVR (Fuente de Datos)**
  Entidad externa. Provee datos de llamadas en ``tbl_historico_*``
  dentro de Almacen de Datos. No interactua directamente con IACT — sus
  tablas son leidas por ``sp_etl_*``.

**APScheduler / Cron**
  Disparador automatico del pipeline ETL. Invoca el management
  command ``sync_etl`` segun CNST-008 (ventana de 6 a 12 horas).

----

2. Especificacion de Casos de Uso
===================================

**Autenticar JWT**

  *Descripcion:* Autentica al usuario mediante credenciales (username
  y password), emite un token JWT y carga sus funciones RBAC.

  *Flujo basico:* El sistema valida en PostgreSQL, genera JWT con
  payload RBAC y retorna token al cliente.

  *Flujo alternativo:* Tras 3 intentos fallidos: bloqueo temporal.

  *Precondicion:* No hay precondicion — es el primer caso de uso.

  *Postcondicion:* El token JWT contiene las funciones RBAC activas.

**Acceder a Modulos**

  *Descripcion:* El sistema filtra los modulos visibles segun las
  funciones RBAC del JWT activo del usuario.

  *Flujo basico:* El frontend consulta las funciones del JWT y
  renderiza solo los modulos autorizados.

  *Flujo alternativo:* El usuario puede cerrar sesion.

  *Precondicion:* Token JWT valido con al menos una funcion RBAC.

  *Postcondicion:* El usuario accede al modulo elegido.

**Ver Dashboard IVR** (UC_RPT_01)

  *Descripcion:* Vista ejecutiva con KPIs del IVR — TMO, nivel
  de servicio y tasa de abandono filtrados por segmento.

  *Flujo basico:* ``<<include>> UC_INC_RPT_01`` → resolver
  segmentos → ``callproc(sp_rpt_centros_xsegmento)``.

  *Flujo alternativo:* Auto-refresh cada 30 segundos via cache.

  *Precondicion:* Funcion ``view_dashboard`` en JWT activo.

  *Postcondicion:* KPIs del trimestre actual mostrados.

**Ver Reportes IVR** (UC_RPT_02..17)

  *Descripcion:* Modulo de 17 reportes. Todos incluyen
  ``<<include>> UC_INC_RPT_01`` (Resolver Segmento).

  *Flujo basico:* Usuario elige trimestre y tipo; el sistema
  llama al ``sp_rpt_*`` correspondiente filtrando por segmentos.

  *Flujo alternativo:* Cambiar trimestre y re-consultar.

  *Precondicion:* Funcion ``view_reports`` en JWT activo.

  *Postcondicion:* Datos del reporte disponibles para exportar.

**Resolver Segmento** (UC_INC_RPT_01)

  *Descripcion:* Comportamiento comun a todos los reportes. Mapea
  los DIDs RBAC del usuario a segmentos IVR.

  *Flujo basico:* Lee DIDs del JWT → mapea via ``DID_MAP``
  (``19028031:nacional_A``, ``19020001:nacional_B``,
  ``19020084:Puebla``) → retorna lista de segmentos activos.

  *Flujo alternativo:* Sin DIDs → 400 ``USER_WITHOUT_SEGMENT``.

  *Precondicion:* Token JWT valido.

  *Postcondicion:* Lista de segmentos disponible para filtrar.

**Gestionar Pipeline ETL** (UC_PIP_01..04)

  *Descripcion:* Disparar, monitorear y reintentar el ETL via
  ``sp_etl_maestro``. Registro en ``etl_runs``.

  *Flujo basico:* Usuario dispara ETL → se crea registro
  ``en_ejecucion`` en ``etl_runs`` → ``sp_etl_maestro`` ejecuta
  → estado actualizado a ``exitoso`` o ``fallido``.

  *Flujo alternativo:* Si falla: ``request_pipeline_retry`` (UC_PIP_04)
  via ``sp_etl_historico``.

  *Precondicion:* Funcion ``view_pipeline_status`` o ``request_pipeline_retry``.

  *Postcondicion:* Estado de ejecucion en ``etl_runs``.

**Consultar Logs** (UC_LOG_*)

  *Descripcion:* Acceso a logs del sistema IVR y al registro de
  auditoria de acciones de usuarios.

  *Flujo basico:* Consultar ``audit_log`` (PostgreSQL) para el
  rango de fechas solicitado.

  *Flujo alternativo:* No hay flujo alternativo.

  *Precondicion:* Funcion ``view_audit_log`` en JWT activo.

  *Postcondicion:* Logs mostrados con paginacion.

**Cerrar Sesion**

  *Descripcion:* Invalida el JWT activo y registra en
  ``audit_log`` (PostgreSQL).

  *Flujo basico:* Termina el acceso a todos los recursos.

  *Flujo alternativo:* No hay flujo alternativo.

  *Precondicion:* Token JWT valido.

  *Postcondicion:* Usuario sin acceso a los recursos.

----

3. Diagramas UML (uno por archivo)
====================================

Los diagramas estan organizados en :doc:`system-view/index` (12 diagramas:
casos de uso, clases, actividad, maquina de estados, secuencia, comunicacion,
componentes, despliegue estandar, despliegue multi-cliente y sub-maquinas
ETL/Reporte).

.. seealso::

 :doc:`system-view/index`
 :doc:`vistas-kruchten`
