.. meta::
   :artefacto: INICIATIVA-AUDITAR-CONFORMIDAD-UC-CODIGO-VS-DOCS
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: EN-CURSO
   :version: 1.0.0
   :fecha_creacion: 2026-05-20T01:30:00
   :ultimo_cambio: 2026-05-20T01:30:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-auditar-conformidad-uc-codigo-vs-docs:

================================================================================
Iniciativa: Auditar Conformidad UC — Codigo vs Docs (Funcional, no estructural)
================================================================================

Origen
======

Sponsor identifico que la cobertura "UC tiene marker" (cerrada
en ``auditoria-cross-stack-falsos-positivos-y-ghost-sp``) NO
garantiza que el flujo implementado **se comporte como dicen
los docs**. Caso encontrado:

* **UC_AUTH_03 — Recuperar Password**: docs declaran flujo de
  preguntas de seguridad (FR-003-01..05, CNST-001 SIN email).
  Codigo: API correcto, **UI era stub estilo email** ("recibiras
  instrucciones", lo cual nunca ocurre porque la API no envia
  email). Marker UC_AUTH_03 existia en UI pero el comportamiento
  no.

Pregunta del sponsor: "hay varios UCs que no has implementado".
Esta iniciativa la responde de forma sistematica.

Diferencia con iniciativas previas
====================================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Iniciativa
     - Pregunta que responde
     - Tipo de verificacion
   * - ``auditar-cobertura-uc-implementacion``
     - "El UC tiene marker en codigo?"
     - Estructural (grep)
   * - ``alinear-numeracion-uc-api-ui``
     - "UC docs ↔ UC code estan numerados igual?"
     - Mapping
   * - ``auditar-conformidad-fr-tests-aceptacion``
     - "Cada FR tiene un TST que lo prueba?"
     - Cobertura de tests
   * - **ESTA iniciativa**
     - **"El comportamiento implementado coincide con los
       FR-NNN-NN declarados?"**
     - **Funcional**

Alcance
=======

Audit funcional sobre los **64 UCs in-scope** (excluye los
documentados OUT por sponsor: ``UC_OPR_*``, ``UC_SUP_*``,
``UC_CLI_01..05``, ``UC_INC_RPT_01``).

Para cada UC con marker en codigo:

1. Leer los FR-NNN-NN declarados en
   ``source/requisitos/requisitos-funcionales/<dominio>/uc-NNN-*/``.
2. Verificar que el comportamiento en codigo (API + UI + DB)
   implementa cada FR. Buscar:

   * Endpoint con request body alineado a la spec.
   * Validaciones declaradas (longitud minima, formato, etc).
   * Eventos de audit emitidos donde el FR lo exige.
   * UI navega los pasos correctos del flujo.

3. Si discrepa: registrar gap concreto + remediacion propuesta.

Metodologia
===========

Aplicar ``.claude/rules/grep-validated-audit.md``: cada claim
"X esta implementado conforme a Y" requiere observable PROVEN
(inspeccion del codigo + comparacion textual con FR).

NO usar agent que solo haga grep. La verificacion debe ser
texto vs texto (FR dice "debe rechazar respuesta < 3 chars" →
buscar la validacion en codigo).

Fases
=====

**FASE 1 — Triage por dominio**

Para cada dominio del scope (auth, users, access, permissions,
reports, alerts, audit, logs, pipeline), levantar el inventario
de UCs + FRs. Output: tabla de prioridad por sensibilidad de
seguridad.

**FASE 2 — Audit funcional por UC**

Por cada UC, abrir su carpeta de docs, leer cada FR, verificar
en codigo. Output: ``conformance-{dominio}.rst`` con tabla:

.. code-block:: text

   UC | FR | Doc dice | Codigo hace | Veredicto
   UC_AUTH_03 | FR-003-02 | mostrar pregunta seguridad
                   | UI implementa flujo 3 pasos | CONFORME
   UC_AUTH_03 | FR-003-04 | generar password temporal
                   | API genera + flag force_change | CONFORME

**FASE 3 — Remediacion**

Por cada veredicto NO-CONFORME, abrir iniciativa hija
``implementar-conformidad-{uc}`` o agregar tarea concreta a
esta iniciativa si es pequeno.

**FASE 4 — Cierre**

Cobertura 64/64 UCs verificados; gaps reales todos cerrados o
escalados como iniciativa propia.

Criterio de salida
==================

* 64/64 UCs in-scope con veredicto explicito (CONFORME |
  PARCIAL | NO-CONFORME | OUT-OF-SCOPE).
* 0 gaps de comportamiento abiertos sin iniciativa de
  remediacion.
* Caso de referencia documentado (UC_AUTH_03) como template.

Caso de referencia (closure parcial)
======================================

**UC_AUTH_03 — REMEDIADO durante la apertura de esta iniciativa.**

* Gap: UI stub email-style, contradicia FR-003-02 (mostrar
  preguntas) y FR-003-04 (validar respuestas antes de generar
  password).
* Remediacion: PR ``feature/uc-auth-03-flujo-preguntas-seguridad``
  en IACT-ui (commit ``ff71ba0``). 3 pasos UI: username →
  preguntas → reset. 7 tests jest verifican el flujo. Total
  suite jest 2382 OK.
* Veredicto post-fix: **CONFORME**.

Este es el template a aplicar para cualquier otro UC con
gap similar.

Tareas operativas pre-cierre
=============================

* T-001: revisar UC_USR_01..04 (creacion de usuario y modificacion).
* T-002: revisar UC_USR_05/06 (block/unblock) — flujo + audit.
* T-003: revisar UC_USR_07 (perfil propio) — UI + audit.
* T-004: revisar UC_AUTH_01/02/04/05 — flujos de sesion.
* T-005: revisar UC_RPT_01..17 — consumo de SPs + filtros.
* T-006: revisar UC_ALR_01..05 — reglas + suscripciones.
* T-007: revisar UC_AUD_01..04 — query + export.
* T-008: revisar UC_LOG_01..08 — endpoints + filtros.
* T-009: revisar UC_ACC_01..09 — asignacion + revocacion.
* T-010: revisar UC_PERM_01..10 — grupos + auditoria.
* T-011: revisar UC_PIP_01..05 — monitor + retry.
