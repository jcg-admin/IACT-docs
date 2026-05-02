.. _modelo-rbac-iact-catalogo:

==========================================
Modelo RBAC IACT — Catalogo de Funciones
==========================================

3. CATÁLOGO DE 73 FUNCIONES
===========================



3.1 MOD_Auth (4 funciones)
--------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - AUTH-001
   - `view_own_sessions`
   - auth:view_own_sessions
   - UC-005
   - Ve sesiones activas propias del usuario (RENAME v5.4.0 desde ``manage_sessions`` — SRP scope propio)
 * - AUTH-002
   - `close_user_session`
   - auth:close_session
   - UC-005
   - Cierra sesión de otro usuario
 * - AUTH-003
   - `reset_password`
   - auth:reset_password
   - UC-003
   - Genera contraseña temporal
 * - AUTH-004
   - `view_all_active_sessions`
   - auth:view_all_sessions
   - UC-005
   - Ve TODAS las sesiones activas del sistema (RENAME v5.4.0 desde ``view_active_sessions`` — SRP scope sistema; admin)


**CNST aplicables:**
- CNST-001: NO email (recuperación por buzón interno)
- CNST-002: Sesión única por usuario, timeout 15 min

**Implementación backend:**

.. code-block:: python

 from apps.access.decorators import require_function
 
 @require_function('AUTH-001') # view_own_sessions
 def view_own_sessions_view(request):
 """Sesiones activas propias del usuario."""
 pass


----

3.2 MOD_Users (9 funciones)
---------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - USR-001
   - `create_users`
   - users:create
   - UC-006
   - Crea nuevos usuarios
 * - USR-002
   - `update_users`
   - users:update
   - UC-007
   - Modifica datos de usuarios
 * - USR-003
   - `deactivate_users`
   - users:deactivate
   - UC-008
   - Baja lógica de usuarios (RENAME v5.4.0 desde ``delete_users`` — semántica soft delete; BR-009 global)
 * - USR-004
   - `list_users`
   - users:list
   - UC-009
   - Lista usuarios con filtros
 * - USR-005
   - `search_users`
   - users:search
   - UC-009
   - Busca usuarios por criterios
 * - USR-006
   - `block_users`
   - users:block
   - UC-007
   - Bloquea acceso de usuario
 * - USR-007
   - `unblock_users`
   - users:unblock
   - UC-007
   - Desbloquea usuario
 * - USR-008
   - `reactivate_users`
   - users:reactivate
   - UC-007
   - Reactiva usuario inactivo
 * - USR-009
   - `view_users`
   - users:view
   - UC-009
   - Consulta información de usuarios


**CAMBIO v5.2.1:**
- Todos los nombres en inglés
- ``update_users`` (NO "modify")
- Sin función USR-010 (eliminada en v5.2.0)

**CNST aplicables:**
- CNST-001: NO email (notificaciones por buzón interno)
- CNST-005: Bajas siempre lógicas, nunca físicas
- CNST-005: Username autogenerado

**Implementación backend:**

.. code-block:: python

 @require_function('USR-001') # create_users
 def create_user_view(request):
 """Creación de usuario."""
 pass


----

3.3 MOD_Access (12 funciones)
-----------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - ACC-001
   - `assign_functions`
   - access:assign
   - UC-010, UC-042
   - Asigna funciones a usuarios
 * - ACC-002
   - `revoke_functions`
   - access:revoke
   - UC-010
   - Revoca funciones de usuarios
 * - ACC-003
   - `view_assignments`
   - access:view
   - UC-011, UC-044
   - Ve asignaciones de funciones
 * - ACC-004
   - `assign_function_groups`
   - access:assign_group
   - UC-010
   - Asigna grupos de funciones
 * - ACC-005
   - `view_separation_rules`
   - access:view_sod
   - UC-043
   - Ve reglas SoD configuradas (RENAME v5.4.0 desde ``manage_separation_rules`` — split SRP B2)
 * - ACC-006
   - `create_function_group`
   - access:create_group
   - UC_PERM_05
   - Crea grupo de funciones custom (admin tech) (NUEVA v5.3.0)
 * - ACC-007
   - `assign_functions_to_group`
   - access:assign_to_group
   - UC_PERM_06
   - Asigna funciones a un grupo (custom o predefinido) (NUEVA v5.3.0)
 * - ACC-008
   - `grant_exceptional_permission`
   - access:grant_exceptional
   - UC_PERM_03
   - Otorga permiso temporal excepcional con justificación (CNST-031) (NUEVA v5.3.0)
 * - ACC-009
   - `revoke_exceptional_permission`
   - access:revoke_exceptional
   - UC_PERM_04
   - Revoca permiso excepcional antes del vencimiento (NUEVA v5.3.0)
 * - ACC-010
   - `revoke_function_group`
   - access:revoke_group
   - UC_PERM_02
   - Revoca grupo asignado a usuario (NUEVA v5.3.0)
 * - ACC-011
   - `update_separation_rule`
   - access:update_sod
   - UC-043
   - Actualiza parámetros de regla SoD existente (NUEVA v5.4.0 — split SRP de ACC-005)
 * - ACC-012
   - `disable_separation_rule`
   - access:disable_sod
   - UC-043
   - Desactiva regla SoD temporalmente (toggle on/off; BR-009 global) (NUEVA v5.4.0 — split SRP de ACC-005)


**CAMBIO v5.4.0:**
- ACC-005 RENAME ``manage_separation_rules`` → ``view_separation_rules``
- ACC-011/012 NUEVAS (split SRP B2; gestión SoD ahora granular)

**CAMBIO v5.2.1:**
- ``assign_function_groups`` (completo, NO "assign_groupers")
- Sin función ACC-006 (eliminada en v5.2.0)

**Componente SEC_RULES:**
- Middleware automático de enforcement
- No visible al usuario
- Valida permisos en cada request

**CNST aplicables:**
- CNST-005: Flat RBAC (sin jerarquías)
- CNST-005: SoD obligatorio
- CNST-005: Permisos temporales: justificación mín 20 chars, vencimiento máx 6 meses

----

3.4 MOD_Pipeline (4 funciones)
------------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - PIP-001
   - `view_pipeline_status`
   - pipeline:view_status
   - UC-050
   - Ve estado actual del ETL
 * - PIP-002
   - `view_pipeline_errors`
   - pipeline:view_errors
   - UC-051
   - Consulta errores del ETL
 * - PIP-003
   - `view_data_availability`
   - pipeline:availability
   - UC-052
   - Ve disponibilidad de datos
 * - PIP-004
   - `request_pipeline_retry`
   - pipeline:retry
   - UC-053
   - Solicita reintento de ETL


**CAMBIO v5.2.1:**
- ``view_pipeline_status`` (NO "ve_estado_etl", evita acrónimo ETL en nombre)
- ``request_pipeline_retry`` (NO "solicita_reintento_etl")

**CNST aplicables:**
- CNST-003: BD IVR solo lectura
- CNST-003: ETL cada 6-12 horas
- CNST-003: NO real-time
- CNST-009: Auditar cambios críticos

------------------------------------------

3.5 MOD_Reports (11 funciones) CORE NEGOCIO
-------------------------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - RPT-001
   - `view_reports`
   - reports:view
   - UC-017, UC-018, UC-019
   - Ve reportes tabulares
 * - RPT-002
   - `view_dashboard`
   - reports:dashboard
   - UC-025
   - Ve dashboard principal
 * - RPT-003
   - `filter_reports`
   - reports:filter
   - UC-020, UC-021
   - Aplica filtros a reportes
 * - RPT-004
   - `export_csv`
   - reports:export_csv
   - UC-022
   - Exporta a CSV (límite: 100K registros)
 * - RPT-005
   - `export_excel`
   - reports:export_excel
   - UC-023
   - Exporta a Excel (límite: 50K registros)
 * - RPT-006
   - `export_pdf`
   - reports:export_pdf
   - UC-024
   - Exporta a PDF (límite: 10K registros)
 * - RPT-007
   - `view_kpis`
   - reports:kpis
   - UC-025
   - Ve KPIs estáticos
 * - RPT-008
   - `view_charts`
   - reports:charts
   - UC-027, UC-028, UC-029
   - Ve gráficos predefinidos
 * - RPT-009
   - `schedule_report`
   - reports:schedule
   - UC_RPT_07
   - Programa generación automática de reportes (NUEVA v5.3.0 — restaura ``programa_reportes`` v5.0_1/v5.1)
 * - RPT-010
   - `save_view`
   - reports:save_view
   - UC_RPT_10
   - Persiste configuración de filtros como vista personalizada (NUEVA v5.3.0)
 * - RPT-011
   - `share_report`
   - reports:share
   - UC_RPT_11
   - Comparte reporte con otros usuarios via URL/buzón interno (NUEVA v5.3.0 — restaura ``comparte_reportes`` v5.0_1/v5.1)


**CAMBIO v5.3.0:**

- Agregadas 3 funciones nuevas (RPT-009..011): ``schedule_report``,
  ``save_view``, ``share_report``.
- ``schedule_report`` y ``share_report`` son **restauraciones** del
  catálogo v5.0_1/v5.1 (eliminadas erróneamente en v5.1.1).
- ``save_view`` es feature nueva (no existía en versiones previas).

**CAMBIO v5.2.1:**

- ``view_charts`` (NO "ve_graficos", "charts" es estándar para gráficos de datos)
- ``filter_reports`` (NO "filtra_reportes")

**CNST aplicables:**
- CNST-003: Datos desfasados 6-12h, NO real-time
- CNST-006: Rango máximo 2 años en filtros
- CNST-007: Límites por formato (CSV: 100K, Excel: 50K, PDF: 10K)
- CNST-007: Throttling por rol

**Límites de exportación:**


.. list-table::
 :widths: 25 25 25 25
 :header-rows: 1

 * - Formato
   - Max Registros
   - Límite Diario
   - Timeout
 * - CSV
   - 100,000
   - 10 exportaciones
   - 60s
 * - Excel
   - 50,000
   - 5 exportaciones
   - 90s
 * - PDF
   - 10,000
   - 3 exportaciones
   - 120s


----

3.6 MOD_Alerts (10 funciones)
-----------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - ALR-001
   - `view_alerts`
   - alerts:view
   - UC-039
   - Ve alertas propias
 * - ALR-002
   - `configure_alerts`
   - alerts:configure
   - UC-036
   - Configura alertas personales
 * - ALR-003
   - `configure_team_alerts`
   - alerts:config_team
   - UC-040
   - Configura alertas de equipo
 * - ALR-004
   - `pause_alerts`
   - alerts:pause
   - UC-038
   - Pausa alertas temporalmente
 * - ALR-005
   - `disable_alerts`
   - alerts:disable
   - UC-038
   - Desactiva alerta (toggle on/off; BR-009 global) (RENAME v5.4.0 desde ``delete_alerts`` — no eliminar)
 * - ALR-006
   - `view_alert_history`
   - alerts:history
   - UC-039
   - Ve historial de alertas
 * - ALR-007
   - `acknowledge_alert`
   - alerts:acknowledge
   - uc-alr-03
   - Reconoce alerta (state transition ACTIVE → ACKNOWLEDGED) (NUEVA v5.4.0 — closed-loop alerts)
 * - ALR-008
   - `subscribe_to_alert`
   - alerts:subscribe
   - uc-alr-05
   - Suscribe usuario a tipo de alerta (NUEVA v5.4.0 — split SRP suscripciones)
 * - ALR-009
   - `unsubscribe_from_alert`
   - alerts:unsubscribe
   - uc-alr-05
   - Desuscribe usuario de tipo de alerta (NUEVA v5.4.0 — split SRP suscripciones)
 * - ALR-010
   - `configure_subscription_severity`
   - alerts:config_severity
   - uc-alr-05
   - Configura nivel mínimo de severidad para notificación (NUEVA v5.4.0 — split SRP suscripciones)


**CAMBIO v5.4.0:**
- ALR-005 RENAME ``delete_alerts`` → ``disable_alerts`` (BR-009 no eliminar)
- ALR-007 NUEVA acknowledge_alert (closed-loop)
- ALR-008/009/010 NUEVAS (split SRP de ``manage_alert_subscriptions`` propuesta)

**CAMBIO v5.2.1:**
- ``configure_team_alerts`` (NO "configura_alertas_equipo")
- ``view_alert_history`` (NO "ve_historial_alertas")

**CNST aplicables:**
- CNST-001: NO email (solo buzón interno)
- CNST-004: Máximo 50 destinatarios por alerta
- CNST-009: Auditar configuración de alertas

----

3.7 MOD_Audit (4 funciones)
---------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - AUD-001
   - `view_audit_log`
   - audit:view
   - UC-061
   - Ve registros de auditoría
 * - AUD-002
   - `search_audit_log`
   - audit:search
   - UC-061
   - Busca en auditoría
 * - AUD-003
   - `export_audit_log`
   - audit:export
   - UC-063
   - Exporta registros de auditoría
 * - AUD-004
   - `generate_compliance_report`
   - audit:compliance
   - UC-062
   - Genera reporte de cumplimiento


**CAMBIO v5.2.1:**
- ``view_audit_log`` (NO "ve_auditoria", "log" explícito)
- ``generate_compliance_report`` (NO "genera_reporte_compliance")

**CNST aplicables:**
- CNST-008: Registros inmutables (append-only)
- CNST-008: Retención mínima 2 años
- CNST-008: Sin PII innecesaria
- CNST-009: Checksum SHA-256 por registro

----

3.8 MOD_Logs (7 funciones)
--------------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - LOG-001
   - `view_application_logs`
   - logs:view_app
   - uc-log-01
   - Ve logs de aplicación (errores 500, INFO/WARN/ERROR, tracebacks) (RENAME v5.4.0 desde ``view_technical_logs`` — SRP, ya no genérico)
 * - LOG-002
   - `export_logs`
   - logs:export
   - uc-log-04
   - Exporta paquete de logs a CSV/JSON
 * - LOG-003
   - `search_logs`
   - logs:search
   - uc-log-03
   - Busca logs por criterios (timestamp, severity, source) (NUEVA v5.3.0)
 * - LOG-004
   - `view_etl_logs`
   - logs:view_etl
   - uc-log-02
   - Ve logs específicos del proceso ETL (sync IVR→Analytics, métricas carga) (NUEVA v5.4.0 — SRP)
 * - LOG-005
   - `view_infrastructure_logs`
   - logs:view_infra
   - uc-log-05
   - Ve logs de infraestructura (timeouts, up/down, conectividad DB) (NUEVA v5.4.0 — SRP)
 * - LOG-006
   - `view_system_health`
   - logs:view_health
   - uc-log-06
   - Ve estado de salud del sistema y servicios externos (UP/DOWN/DEGRADED) (NUEVA v5.4.0 — gap UC_081)
 * - LOG-007
   - `view_technical_metrics`
   - logs:view_metrics
   - uc-log-07
   - Ve métricas técnicas agregadas (CPU, memoria, latencia P95) (NUEVA v5.4.0 — gap UC_083)


**CAMBIO v5.4.0:**

- LOG-001 RENAME ``view_technical_logs`` → ``view_application_logs``
  (SRP: ya no cubre ETL ni infra)
- LOG-004 NUEVA ``view_etl_logs`` (uc-log-02 deja de ser instancia)
- LOG-005 NUEVA ``view_infrastructure_logs`` (uc-log-05 nuevo)
- LOG-006 NUEVA ``view_system_health`` (gap UC_081 ARQ-MOD-008)
- LOG-007 NUEVA ``view_technical_metrics`` (gap UC_083 ARQ-MOD-008)

**CAMBIO v5.3.0:**

- Agregada ``search_logs`` (LOG-003) para sustentar UC_LOG_03 que
  citaba función inexistente.

**CAMBIO v5.2.1:**
- Nombres en inglés (NO "ve_logs_tecnicos")

**CNST aplicables:**
- CNST-008: Sin PII (contraseñas, tokens enmascarados)
- CNST-008: Formato JSON estructurado
- CNST-008: Retención 30-90 días según tipo

**Diferencia con MOD_Audit:**
- **MOD_Audit:** Eventos de negocio (quién hizo qué)
- **MOD_Logs:** Eventos técnicos (errores, performance)

----

3.9 MOD_Operator (9 funciones)
-------------------------------

Funciones de los agentes (operadores) del call center IACT.
Estas funciones se auto-otorgan al activar el perfil de operador;
la granularidad permite restricciones futuras por servicio o turno.

.. list-table::
 :widths: 15 30 25 10 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - OPR-001
   - `manage_own_agent_state`
   - operator:agent_state
   - UC_OPR_01
   - Cambia propio estado de disponibilidad (available/busy/break/offline)
 * - OPR-002
   - `answer_inbound_calls`
   - operator:answer
   - UC_OPR_02
   - Atiende llamada entrante asignada por el enrutador
 * - OPR-003
   - `make_outbound_calls`
   - operator:dial_out
   - UC_OPR_03
   - Realiza llamada saliente autorizada
 * - OPR-004
   - `hold_calls`
   - operator:hold
   - UC_OPR_04
   - Pone en espera o retoma llamada activa
 * - OPR-005
   - `transfer_calls`
   - operator:transfer
   - UC_OPR_05
   - Transfiere llamada a otro agente o cola
 * - OPR-006
   - `enter_call_disposition`
   - operator:disposition
   - UC_OPR_06
   - Registra resultado de la llamada (disposition code)
 * - OPR-007
   - `request_break`
   - operator:break
   - UC_OPR_07
   - Solicita pausa autorizada (break/lunch/training)
 * - OPR-008
   - `view_own_performance_dashboard`
   - operator:own_dashboard
   - UC_OPR_08
   - Consulta propio dashboard de métricas de desempeño
 * - OPR-009
   - `view_own_call_history`
   - operator:own_history
   - UC_OPR_09
   - Consulta historial personal de llamadas atendidas/realizadas


**CNST aplicables:**
- CNST-009: Autenticación requerida para toda acción operativa
- CNST-025: Cambios de estado auditados
- CNST-013: Manejo estándar de errores

**Nota v5.5.0:**
Módulo nuevo derivado del análisis de UC_OPR_01..10.
Funciones implícitas en versiones anteriores — ahora formalizadas
como atómicas para soporte de restricciones futuras por servicio.

----

3.10 MOD_Supervision (3 funciones)
------------------------------------

Funciones de supervisores que intervienen en tiempo real sobre
agentes y llamadas activas. Requieren asignación explícita
(no auto-otorgadas como MOD_Operator).

.. list-table::
 :widths: 15 30 25 10 20
 :header-rows: 1

 * - ID
   - Función
   - Capacidad
   - UC
   - Descripción
 * - SUP-001
   - `monitor_live_calls`
   - supervision:monitor
   - UC_SUP_01
   - Escucha llamada activa en modo silent (sin intervención)
     o whisper (habla solo al agente, cliente no oye)
 * - SUP-002
   - `barge_in_calls`
   - supervision:barge_in
   - UC_SUP_02
   - Interviene en llamada activa habilitando canal tripartito
 * - SUP-003
   - `broadcast_team_messages`
   - supervision:broadcast
   - UC_SUP_03
   - Envía mensaje de texto a todos los agentes del equipo


**CNST aplicables:**
- CNST-009: Autenticación requerida
- CNST-025: Toda supervisión auditada (quién monitoreó qué llamada)
- BR-009: Registros de supervisión inmutables

**Nota legal:**
SUP-001 (monitor_live_calls) y SUP-002 (barge_in_calls) generan
notificación audible al agente (tono de supervisión) por obligación
legal de compliance. El sistema emite el tono automáticamente.

**Nota v5.5.0:**
Módulo nuevo derivado del análisis de UC_SUP_01..03.

