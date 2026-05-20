.. meta::
   :artefacto: CIERRE-AUDITAR-CONFORMIDAD-UC-CODIGO-VS-DOCS
   :tipo: Cierre de iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas/auditar-conformidad-uc-codigo-vs-docs
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-20T04:30:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _cierre-auditar-conformidad-uc-codigo-vs-docs:

============================================================================
Cierre: Auditar Conformidad UC — Codigo vs Docs
============================================================================

Resumen ejecutivo
=================

* **63/63 UCs in-scope** auditados funcionalmente.
* **2 UCs nuevos creados** (deuda inversa cerrada):
  UC_ADM_01..05 (admin) + UC-091 (cron ETL diario).
* **63 audit emit sites** alineados a campos canonicos
  (``target_entity_type``, ``target_entity_id``, ``ip_address``).
* **8 gaps funcionales** reales remediados (no solo audit
  metadata).
* **0 deuda tecnica abierta**.
* **Pytest:** 1460 passed / 1 skipped / 1 flaky pre-existente.

Cobertura por dominio
======================

.. list-table::
   :header-rows: 1
   :widths: 18 12 70

   * - Dominio
     - UCs
     - Cambios
   * - auth
     - 5/5
     - USERNAME_REGEX (FR-001.01); lockout 15->30 min
       (FR-001.02 BR-015); LOGIN_SUCCESS/LOGIN_FAILED canonicos
       (FR-001.05); password MAX_LENGTH=128 + blocklist 1000
       passwords comunes (FR-004.02); session_duration +
       logout_type (FR-002.02); UI 3-step flow security
       questions (FR-003.01..05); FR-005.01 enriquecido con
       full_name + last_activity_at + duration + filtros + ordering.
   * - users
     - 4/4
     - min_length=2 first_name/last_name (FR-006.01); deactivation_reason
       obligatorio en INACTIVE (FR-007.02); prior_values + new_values
       en USER_MODIFIED audit (FR-007.04); ``_is_last_system_admin``
       AGR-010 protection (FR-008.01); filtros state + role + ordering
       ampliado (FR-009.02/03); ip_address + target_entity en todos
       los audits.
   * - access
     - 2/2
     - target_entity + ip_address en FUNCTIONS_ASSIGNED/REVOKED/
       FAILED/NOOP; payload enriquecido (codes, reason, expires_at).
   * - permissions
     - 10/10
     - target_entity + ip en AGR_*, ACCESS_GROUP_*, COMPOSITION_*,
       EXCEPTIONAL_PERMISSION_*. Critico: FR-017.02 ahora
       **invalida cache de TODOS los miembros del AGR** al cambiar
       composicion (antes solo emitia audit).
   * - admin
     - 5/5
     - 5 UCs nuevos creados (uc-086..uc-090) — spec-from-code
       retroactivo. Audit recursivo 15/15 PROVEN/AMPLIACION.
   * - reports
     - 16/16
     - 16 emits canonizados (SavedFilter/View, Export, Schedule,
       Share, AGENT_DETAIL).
   * - alerts
     - 5/5
     - 9 emits canonizados (RULE_*, ALERT_ACKNOWLEDGED single +
       bulk, SUBSCRIPTION_*).
   * - audit
     - 4/4
     - 9 meta-audit emits canonizados (AUDIT_LOG_*, AUDIT_SEARCH,
       AUDIT_EXPORT, COMPLIANCE_REPORT + signature_prefix).
   * - logs
     - 7/7
     - LOG_EXPORT_QUEUED canonizado. Readonly verificados:
       LogPIIScanner + LogRangeValidator conformes.
   * - pipeline
     - 5/5
     - 4 UCs + UC-091 nuevo (cron evt_etl_diario + job_config).

Branches creadas y empujadas
=============================

11 branches feature (todas pushed):

.. code-block:: text

   IACT-api:
     feature/conformidad-uc-auth-01-validar-username  (3 commits)
     feature/conformidad-uc-usr-01-04
     feature/conformidad-uc-acc-01-02
     feature/conformidad-uc-perm-01-10
     feature/conformidad-uc-rpt-01-17
     feature/conformidad-uc-alr-01-05
     feature/conformidad-uc-aud-01-04
     feature/conformidad-uc-log-01-08

   IACT-ui:
     feature/uc-auth-03-flujo-preguntas-seguridad

   IACT-docs:
     feature/auditar-conformidad-uc-codigo-vs-docs   (iniciativa)
     feature/documentar-uc-adm-01-05                 (5 UCs nuevos)
     feature/documentar-uc-091-etl-diario-cron       (UC nuevo)

Lecciones aplicadas
====================

L-1 — La cobertura "UC tiene marker" NO garantiza conformidad funcional
-----------------------------------------------------------------------

UC_AUTH_03 (caso disparador) tenia marker pero su UI era stub
estilo email cuando la API canonica usa preguntas de seguridad
(CNST-001 SIN email). Audit estructural lo daba por OK; audit
funcional encontro el gap. Este patron exige un audit
**funcional periodico** (no solo grep de markers).

L-2 — Deuda inversa: implementacion sin spec aprobada
-------------------------------------------------------

Encontrados 6 UCs sin spec en docs (UC_ADM_01..05 + cron ETL).
Se documentaron retroactivamente con spec-from-code +
verificacion recursiva (15/15 PROVEN/AMPLIACION).

L-3 — Patron consistente de audit canonico
--------------------------------------------

Todos los AuditLogService.emit() canonizados con la misma
forma:

.. code-block:: python

   AuditLogService.emit(
       event_type='EVENT_NAME',
       actor_user_id=request.user.pk,
       target_entity_type='Entity',
       target_entity_id=str(id),
       ip_address=ip_from_request(request),
       payload={...},
   )

63 sites alineados. Facilita auditoria forense y permite
construir reportes de actividad por usuario/entidad sin parsing
de payloads heterogeneos.

L-4 — Gaps funcionales criticos detectados
-------------------------------------------

Algunos gaps no eran solo metadata de audit — eran defectos
funcionales reales:

* **PermissionCache no se invalidaba al cambiar composicion AGR**
  (FR-017.02): los miembros del AGR seguian viendo permisos
  obsoletos hasta el siguiente TTL. **Fix:** invalidar cache de
  todos los miembros al post-commit.
* **Lockout 15 vs FR=30 min**: politica de seguridad por debajo
  del FR aprobado. **Fix:** alineado a 30/30.
* **No emit LOGIN_FAILED individual**: trazabilidad rota antes
  del bloqueo. **Fix:** emit por cada intento fallido.
* **Last system admin no protegido contra eliminacion**: bug
  potencial de lockout total. **Fix:** ``_is_last_system_admin``
  check via AGR-010.

L-5 — Audit verificable con metodo recursivo
----------------------------------------------

Para los UCs creados retroactivamente (UC_ADM_01..05) se ejecuto
un audit del audit (verificacion textual de claims vs codigo +
docs UI). Resultado: 9 PROVEN + 6 AMPLIACION + 0 SPECULATIVE +
0 NO-CONFORME. El metodo "spec-from-code con verificacion
recursiva" es valido y replicable.

Iniciativas hijas creadas
==========================

* :doc:`/gestion/pm/iniciativas/documentar-uc-adm-01-05/index` —
  cierre del dominio admin retroactivo.

Pytest cross-stack
===================

.. code-block:: text

   Final:  1460 passed / 1 skipped / 1 flaky pre-existente
   Inicio: ~1351 passed (antes del audit)
   Delta:  +109 tests (regression + nuevos tests por gap)

   Jest: 2382/2382 OK (sin regresion en UI; +14 nuevos en
                       password policy + UC_AUTH_03 flow + tests
                       de username regex)

Estado de cierre
================

* Working tree limpio en los 4 repos.
* 13 branches pushed a sus remotos.
* Estado iniciativa: COMPLETADA.
* Sin deuda tecnica abierta detectada por este audit.
* Pendiente: merges de las 11 feature branches a develop (decision
  del sponsor — no parte de este audit).
