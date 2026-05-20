.. meta::
   :artefacto: INICIATIVA-AUDITORIA-CROSS-STACK-FALSOS-POSITIVOS-Y-GHOST-SP
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-20T00:30:00
   :ultimo_cambio: 2026-05-20T00:45:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-auditoria-cross-stack-falsos-positivos-y-ghost-sp:

==============================================================================
Iniciativa: Auditoria Cross-Stack — Falsos Positivos + Ghost SP
==============================================================================

Origen
======

Sponsor solicito "NO QUEREMOS DEUDA TECNICA, vas a continuar
analiza y crea las iniciativas correctas". En respuesta, se
lanzo un agent Explore para producir audit cross-stack
de gaps reales en DB, API, UI, Docs.

El agent reporto **8 gaps** clasificados como 2×P0, 3×P1,
2×P2, 1×P3, proponiendo abrir 8 iniciativas atomicas. Antes
de abrir las iniciativas se aplico ``.claude/rules/grep-validated-audit.md``:
inspeccionar el bucket negativo de cada claim para detectar
SPECULATIVE camuflado de PROVEN.

Resultado de la verificacion
=============================

Tras verificacion completa: 7/8 fueron falsos positivos
(detectados antes de abrir iniciativas inutiles), 1 fue gap
real (cerrado), y el unico gap parcial (GAP-03) se cerro al
100% tras el sponsor exigir implementacion completa (no
parcial).

Estado final: **0 gaps abiertos**, 2 commits remediadores en
codigo (e454295 db, 2145b22 api), 1 iniciativa de registro.

.. list-table::
   :header-rows: 1
   :widths: 14 26 60

   * - Gap
     - Veredicto
     - Verificacion
   * - GAP-01 (12 SPs unused)
     - PARCIAL FP
     - 9 SPs RPT/ETL consumidos via ``cursor.callproc``;
       5 ETL son internos (llamados por sp_etl_maestro). 1
       referencia real ghost: ``sp_rpt_resumen_abandono_rollup``.
   * - GAP-02 (23 pytest.skip)
     - FALSO POSITIVO
     - 22 skips son data-dependent ("No hay funciones en BD"),
       no features sin implementar. Skip correcto.
   * - GAP-03 (85 viewsets sin UC)
     - CERRADO (era PARCIAL FP)
     - Agent dijo 174 vistas (47 reales) y 85 sin marker (10
       reales). Los 10 reales fueron taggeados con marker UC
       en commit ``2145b22`` (IACT-api), llegando a 47/47.
   * - GAP-04 (AuditLog.emit() inexistente)
     - FALSO POSITIVO
     - ``AuditLogService.emit()`` existe en
       ``apps/audit/services.py:323`` con 81 usos en produccion
       (excluye tests). Agent miro la clase ``AuditLog`` (modelo)
       en lugar de ``AuditLogService`` (servicio).
   * - GAP-05 (102 UCs sin testing.rst)
     - FALSO POSITIVO
     - 69 UCs in-scope, **0** sin testing.rst. Agent conto UCs
       out-of-scope (caller/operator/supervision/inclusion).
   * - GAP-06 (15+ .puml ghost)
     - FALSO POSITIVO
     - Las refs .puml ``BACK-*``/``FRONT-*``/``GOB-*``/``DEVOPS-*``
       son ejemplos textuales en
       ``normativa/gobernanza/adr-gob-006-diagramas-uml-casos-uso.rst``
       como template de nomenclatura, no referencias reales.
   * - GAP-07 (funciones_utilidad sin tests)
     - FALSO POSITIVO
     - 9 funciones son helpers internos de los SPs
       (``fn_did_segmento``, ``fn_normalizar_*``, ``ivr_*``).
       Documentadas como "Funciones internas — solo las usan
       los SPs" en HALLAZGOS-FASE6-FINAL.
   * - GAP-08 (170 serializers sin docs)
     - FALSO POSITIVO
     - Verificacion: TODOS los campos sensibles (password,
       password_confirm, new_password, etc.) tienen ``write_only=True``
       declarado correctamente. El grep del agent miraba 4
       coincidencias literales en una sola linea, ignorando
       declaraciones multi-linea donde ``serializers.CharField(``
       y ``write_only=True,`` viven en lineas separadas. La
       cobertura real de field-boundaries es 100% donde aplica.

Gap real cerrado
================

**GAP-01-real: ghost SP ``sp_rpt_resumen_abandono_rollup``**

El SP esta definido como archivo standalone en
``IACT-db/provisioners/mariadb/objetos/sps/sp_rpt_resumen_abandono_rollup.sql``
pero **ausente del bulk loader** ``sp_rpt_reportes.sql``.

La DB activa lo tiene cargado por accidente historico (mysqldump
de backup previo), pero un provisioning desde cero produciria
runtime errors al llamar el endpoint REST que invoca el SP.

API que lo consume:

* ``apps/reports/ivr_services.py`` lineas 95, 109 (``_call_sp``)
* ``apps/reports/ivr_views.py`` lineas 303, 320 (endpoint
  resumen abandono ejecutivo)

**Remediacion:** PR ``feature/integrar-sp-rpt-resumen-abandono-rollup``
en IACT-db. Anade el SP body al final de ``sp_rpt_reportes.sql``
manteniendo el patron de bulk load (un solo DELIMITER abierto
al inicio, cerrado al final). El archivo standalone permanece
como referencia detallada. Commit ``e454295`` empujado.

Verificacion: 153/153 tests de pipeline+reports OK con SP
cargado.

Decision sobre las iniciativas no-abiertas
===========================================

NO se abren las 7 iniciativas propuestas por el agent que eran
falsos positivos. Hacerlo seria deuda inversa: trabajo sin
problema real que distrae del trabajo verdadero. Esta iniciativa
queda como registro explicito de "estos gaps fueron verificados
y son falsos positivos, no requieren accion".

Lecciones
=========

L-1 — Aplicar grep-validated-audit ANTES de abrir iniciativas
--------------------------------------------------------------

El audit del agent tuvo 87.5% (7/8) de falsos positivos. Sin la
verificacion, hubieramos abierto 7 iniciativas inutiles,
incluyendo una P0 grande ("implementar AuditLogService.emit
completo") cuando el servicio ya existe con 81 usos.

L-2 — Auditar al auditor es protocolo, no neurosis
---------------------------------------------------

La regla ``.claude/rules/grep-validated-audit.md`` fue creada
por dos falsos positivos historicos (UC_RPT_05/06 y 58 FRs sin
TST). Hoy previene 7 falsos positivos mas. La regla esta
funcionando — debe seguir aplicandose a TODO audit, incluso
los del propio modelo.

L-3 — SPs deben tener un loader canonico
-----------------------------------------

El gap real surge de tener dos formas de definir SPs:

* Bulk loader (``sp_rpt_reportes.sql``) — cargado por provisioner
* Archivos standalone (``objetos/sps/<name>.sql``) — no cargados

El SP ``sp_rpt_resumen_abandono_rollup`` cayo en la grieta:
existia solo standalone, no en el bulk. Una iniciativa de
seguimiento ``unificar-loader-sps-mariadb`` podria estandarizar
el mecanismo. Se registra como deuda candidata, no prioritaria.
