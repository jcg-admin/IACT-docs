.. meta::
   :artefacto: MATRIZ-IMPLEMENTACION-UC-API-UI
   :tipo: Matriz
   :dominio: gestion
   :subdominio: pm/iniciativas/auditar-implementacion-ucs-api-ui
   :repo_objetivo: multiple
   :estado: Completada
   :version: 1.0.0
   :fecha_creacion: 2026-07-03T22:15:30
   :ultimo_cambio: 2026-07-03T22:15:30
   :autor: NestorMonroy
   :clasificacion: Interno

.. _matriz-implementacion-uc-api-ui:

==============================================================
Matriz: Implementacion UC docs -> IACT-api / IACT-ui
==============================================================

Matriz completa de los 88 UCs declarados en
``source/requisitos/requisitos-funcionales/`` contra la
presencia de su marker canonico en ``IACT-api`` (``*.py``) e
``IACT-ui`` (``src/**``). Metodologia, comandos exactos y
hallazgos: ver
:doc:`deep-analisis-auditar-implementacion-ucs-api-ui`.

Convenciones de la columna Estado:

* **Implementado** — marker canonico con hit fuerte (explicito
  o compuesto que nombra el numero) en api Y en ui.
* **Implementado (marker api solo en rango)** — funcionalidad
  verificada por endpoint en api, pero el marker granular solo
  aparece en comentarios de rango (``UC_ADM_01..03``).
* **Implementado (api-only por diseno)** — UC de actor Sistema,
  sin superficie UI esperada.
* **OUT (out-of-scope v5.6.0)** — modulo reservado; docs lo
  declaran fuera de alcance y no existe marker en codigo
  (verificado, 0 hits).

.. list-table::
   :header-rows: 1
   :widths: 10 30 14 20 12 14

   * - Dominio
     - UC (docs)
     - Marker
     - api
     - ui
     - Estado
   * - auth
     - uc-001-iniciar-sesion
     - ``UC_AUTH_01``
     - si
     - si
     - Implementado
   * - auth
     - uc-002-cerrar-sesion
     - ``UC_AUTH_02``
     - si
     - si
     - Implementado
   * - auth
     - uc-003-recuperar-password
     - ``UC_AUTH_03``
     - si
     - si
     - Implementado
   * - auth
     - uc-004-cambiar-password
     - ``UC_AUTH_04``
     - si
     - si
     - Implementado
   * - auth
     - uc-005-gestionar-sesiones
     - ``UC_AUTH_05``
     - si
     - si
     - Implementado
   * - users
     - uc-006-crear-usuario
     - ``UC_USR_01``
     - si
     - si
     - Implementado
   * - users
     - uc-007-modificar-usuario
     - ``UC_USR_03``
     - si
     - si
     - Implementado
   * - users
     - uc-008-baja-usuario
     - ``UC_USR_04``
     - si
     - si
     - Implementado
   * - users
     - uc-009-listar-usuarios
     - ``UC_USR_02``
     - si
     - si
     - Implementado
   * - access
     - uc-010-asignar-funciones
     - ``UC_ACC_01``
     - si
     - si
     - Implementado
   * - access
     - uc-011-revocar-funciones
     - ``UC_ACC_02``
     - si
     - si
     - Implementado
   * - permissions
     - uc-012-asignar-grupo-usuario-perm
     - ``UC_PERM_01``
     - si
     - si
     - Implementado
   * - permissions
     - uc-013-revocar-grupo-usuario-perm
     - ``UC_PERM_02``
     - si
     - si
     - Implementado
   * - permissions
     - uc-014-conceder-permiso-excepcional-perm
     - ``UC_PERM_03``
     - si
     - si
     - Implementado
   * - permissions
     - uc-015-revocar-permiso-excepcional
     - ``UC_PERM_04``
     - si
     - si
     - Implementado
   * - permissions
     - uc-016-gestionar-grupo-permisos
     - ``UC_PERM_05``
     - si
     - si
     - Implementado
   * - permissions
     - uc-017-asignar-funciones-grupo
     - ``UC_PERM_06``
     - si
     - si
     - Implementado
   * - permissions
     - uc-018-verificar-permiso-usuario
     - ``UC_PERM_07``
     - si
     - si
     - Implementado
   * - permissions
     - uc-019-generar-menu-dinamico
     - ``UC_PERM_08``
     - si
     - si
     - Implementado
   * - permissions
     - uc-020-auditar-acceso
     - ``UC_ACC_09``
     - si
     - si
     - Implementado
   * - permissions
     - uc-021-consultar-auditoria-permisos
     - ``UC_PERM_10``
     - si
     - si
     - Implementado
   * - operator
     - uc-022-cambiar-estado-agente
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-023-atender-llamada-entrante
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-024-iniciar-llamada-saliente
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-025-pausar-llamada
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-026-transferir-llamada
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-027-registrar-disposicion-llamada
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-028-solicitar-descanso
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-029-ver-metricas-propias
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-030-ver-historial-llamadas
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - operator
     - uc-031-leer-buzon-interno
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - reports
     - uc-032-ver-dashboard
     - ``UC_RPT_01``
     - si
     - si
     - Implementado
   * - reports
     - uc-033-ver-metricas-tiempo-real
     - ``UC_RPT_02``
     - si
     - si
     - Implementado
   * - reports
     - uc-034-ver-reportes-historicos
     - ``UC_RPT_03``
     - si
     - si
     - Implementado
   * - reports
     - uc-035-exportar-reporte
     - ``UC_RPT_04``
     - si
     - si
     - Implementado
   * - reports
     - uc-036-programar-reporte
     - ``UC_RPT_07``
     - si
     - si
     - Implementado
   * - reports
     - uc-037-ver-reportes-programados
     - ``UC_RPT_08``
     - si
     - si
     - Implementado
   * - reports
     - uc-038-gestionar-filtros-guardados
     - ``UC_RPT_09``
     - si
     - si
     - Implementado
   * - reports
     - uc-039-guardar-vista
     - ``UC_RPT_10``
     - si
     - si
     - Implementado
   * - reports
     - uc-040-compartir-reporte
     - ``UC_RPT_11``
     - si
     - si
     - Implementado
   * - reports
     - uc-041-reporte-agentes
     - ``UC_RPT_12``
     - si
     - si
     - Implementado
   * - reports
     - uc-042-reporte-colas
     - ``UC_RPT_13``
     - si
     - si
     - Implementado
   * - reports
     - uc-043-reporte-campanas
     - ``UC_RPT_14``
     - si
     - si
     - Implementado
   * - reports
     - uc-044-reporte-transferencias
     - ``UC_RPT_15``
     - si
     - si
     - Implementado
   * - reports
     - uc-045-reporte-menus-ivr
     - ``UC_RPT_16``
     - si
     - si
     - Implementado
   * - reports
     - uc-046-reporte-clientes-unicos
     - ``UC_RPT_17``
     - si
     - si
     - Implementado
   * - alerts
     - uc-050-configurar-umbrales-alertas
     - ``UC_ALR_01``
     - si
     - si
     - Implementado
   * - alerts
     - uc-051-ver-alertas-activas
     - ``UC_ALR_02``
     - si
     - si
     - Implementado
   * - alerts
     - uc-052-reconocer-alerta
     - ``UC_ALR_03``
     - si
     - si
     - Implementado
   * - alerts
     - uc-053-ver-historial-alertas
     - ``UC_ALR_04``
     - si
     - si
     - Implementado
   * - alerts
     - uc-054-gestionar-suscripciones-alertas
     - ``UC_ALR_05``
     - si
     - si
     - Implementado
   * - audit
     - uc-055-consultar-audit-log
     - ``UC_AUD_01``
     - si
     - si
     - Implementado
   * - audit
     - uc-056-buscar-en-audit-log
     - ``UC_AUD_02``
     - si
     - si
     - Implementado
   * - audit
     - uc-057-exportar-audit-log
     - ``UC_AUD_03``
     - si
     - si
     - Implementado
   * - audit
     - uc-058-reporte-cumplimiento
     - ``UC_AUD_04``
     - si
     - si
     - Implementado
   * - logs
     - uc-059-ver-logs-aplicacion
     - ``UC_LOG_01``
     - si
     - si
     - Implementado
   * - logs
     - uc-060-ver-logs-etl
     - ``UC_LOG_02``
     - si
     - si
     - Implementado
   * - logs
     - uc-061-buscar-en-logs
     - ``UC_LOG_03``
     - si
     - si
     - Implementado
   * - logs
     - uc-062-exportar-logs
     - ``UC_LOG_04``
     - si
     - si
     - Implementado
   * - logs
     - uc-063-ver-logs-infra
     - ``UC_LOG_05``
     - si
     - si
     - Implementado
   * - logs
     - uc-064-ver-estado-sistema
     - ``UC_LOG_06``
     - si
     - si
     - Implementado
   * - logs
     - uc-065-ver-metricas-rendimiento
     - ``UC_LOG_07``
     - si
     - si
     - Implementado
   * - caller
     - uc-066-recibir-llamada
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - caller
     - uc-067-navegar-ivr
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - caller
     - uc-068-esperar-en-cola
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - caller
     - uc-069-solicitar-callback
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - caller
     - uc-070-encuesta-post-llamada
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - pipeline
     - uc-071-ver-estado-pipeline
     - ``UC_PIP_01``
     - si
     - si
     - Implementado
   * - pipeline
     - uc-072-ver-errores-pipeline
     - ``UC_PIP_02``
     - si
     - si
     - Implementado
   * - pipeline
     - uc-073-ver-disponibilidad-datos
     - ``UC_PIP_03``
     - si
     - si
     - Implementado
   * - pipeline
     - uc-074-reintentar-pipeline
     - ``UC_PIP_04``
     - si
     - si
     - Implementado
   * - supervision
     - uc-075-monitorear-llamada
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - supervision
     - uc-076-intervenir-llamada
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - supervision
     - uc-077-enviar-mensaje-masivo
     - —
     - n/a
     - n/a
     - OUT (out-of-scope v5.6.0)
   * - access
     - uc-078-permisos-efectivos-del-usuario
     - ``UC_ACC_03``
     - si
     - si
     - Implementado
   * - access
     - uc-079-asignar-agrupador-a-usuario
     - ``UC_ACC_04``
     - si
     - si
     - Implementado
   * - access
     - uc-080-reglas-de-separacion-de-funciones
     - ``UC_ACC_05``
     - si
     - si
     - Implementado
   * - logs
     - uc-081-ver-eventos-pipeline-analitico
     - ``UC_LOG_08``
     - si
     - si
     - Implementado
   * - pipeline
     - uc-082-gestionar-configuracion-job-etl
     - ``UC_PIP_05``
     - si
     - si
     - Implementado
   * - users
     - uc-083-bloquear-usuario
     - ``UC_USR_05``
     - si
     - si
     - Implementado
   * - users
     - uc-084-desbloquear-usuario
     - ``UC_USR_06``
     - si
     - si
     - Implementado
   * - users
     - uc-085-editar-perfil-propio
     - ``UC_USR_07``
     - si
     - si
     - Implementado
   * - admin
     - uc-086-catalogo-reglas-separacion-funciones
     - ``UC_ADM_01``
     - funcional (endpoint /api/access/separation-rules/ — apps/access/urls.py:94)
     - si
     - Implementado (marker api solo en rango)
   * - admin
     - uc-087-catalogo-funciones-rbac
     - ``UC_ADM_02``
     - funcional (endpoint /api/access/functions/ (apps/access/urls.py:131))
     - si
     - Implementado (marker api solo en rango)
   * - admin
     - uc-088-catalogo-grupos-acceso
     - ``UC_ADM_03``
     - si
     - si
     - Implementado
   * - admin
     - uc-089-catalogo-menu-items
     - ``UC_ADM_04``
     - si
     - si
     - Implementado
   * - admin
     - uc-090-ciclo-vida-menu-items
     - ``UC_ADM_05``
     - si
     - si
     - Implementado
   * - pipeline
     - uc-091-ejecucion-programada-etl-diario
     - ``ETLScheduler``
     - si (scheduler.py)
     - n/a (actor Sistema)
     - Implementado (api-only por diseno)

Conteos agregados
==================

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Bucket
     - Conteo
     - Detalle
   * - UCs declarados en docs
     - 88
     - ``find source/requisitos/requisitos-funcionales -mindepth 2 -maxdepth 2 -type d -name "uc-*" | wc -l``
   * - OUT (out-of-scope v5.6.0)
     - 18
     - operator (10) + caller (5) + supervision (3)
   * - In-scope
     - 70
     - 88 - 18
   * - Implementados en api
     - 70/70
     - 67 marker directo + 2 funcionales con marker en rango
       (uc-086, uc-087) + 1 scheduler sin marker UC (uc-091)
   * - Implementados en ui (aplicables)
     - 69/69
     - uc-091 no aplica (actor Sistema)
   * - Gaps de implementacion docs -> codigo
     - 0
     - ningun UC in-scope sin implementacion

