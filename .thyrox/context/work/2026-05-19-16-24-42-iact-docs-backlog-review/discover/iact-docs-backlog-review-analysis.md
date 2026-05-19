```yml
created_at: 2026-05-19 16:24:42
project: IACT-docs
work_package: 2026-05-19-16-24-42-iact-docs-backlog-review
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Backlog Review + Normativa Gap Analysis — IACT-docs

> Branch: `feature/iact-docs-backlog-review` (creada desde `develop`).
> Objetivo declarado por el ejecutor:
> 1. Analizar los pendientes del repo.
> 2. Analizar las normativas para crear una normativa nueva.

Este documento consolida ambos análisis. La segunda parte es la
**recomendación accionable**: propone candidatos concretos para crear
una nueva normativa a partir de los huecos observables en el corpus
`source/normativa/`.

---

## Parte 1 — Inventario de pendientes (PROVEN)

### 1.1 Estado de la sesión activa

Fuente: `.thyrox/context/now.md` (último update `2026-05-08 23:55:22`).

- **WP activo declarado:** `2026-05-08-23-51-53-design-view-fill`,
  Stage 1 DISCOVER (flow THYROX).
- **Estado real del WP:** sólo contiene `track/wp-changelog.md` con
  versión 1.0.0 marcada `Aprobado` el 2026-05-08. No hay artefactos
  de discover/analyze/plan-execution propios — el changelog dice que
  cierra H-CONTENT-1 del WP previo `dag-completion-loop`. **El WP está
  funcionalmente cerrado** aunque `now.md` lo declara como activo
  (desincronización entre estado de sesión y artefactos).
- **Branch en `now.md`:** se mencionan `claude/review-ucs-work-state-phwmj`
  y `feature/solve-problem-docs` en distintos resúmenes — no hay
  branch única consistente con el WP activo.

**Hallazgo H-01 (INFERRED):** El estado de sesión (`now.md`,
`focus.md`) no refleja el estado real del repo. Último update real
de focus es del 2026-04-29; `now.md` mezcla varias sesiones sin
ordenar.

### 1.2 Deuda técnica pendiente

Fuente: `.thyrox/context/technical-debt.md`.

| ID | Severidad | Estado | Resolución requerida |
|----|-----------|--------|----------------------|
| TD-001 | baja (reclasificada) | `[~]` aceptado | — |
| TD-002 | media | `[x]` resuelto 2026-05-06 | — |
| TD-003 | media | `[x]` resuelto 2026-05-06 | — |
| TD-004 | baja | `[x]` resuelto 2026-05-06 | — |
| TD-005 | baja | `[x]` resuelto 2026-05-06 | — |
| TD-006 | media | `[x]` resuelto (preexistente) | — |
| TD-007 | baja | `[~]` obsoleto 2026-05-06 | — |
| **TD-RBAC-03** | **media** | **`[ ] Pendiente`** | ADR explícito para `manage_critical_function_flag` |

**Hallazgo H-02 (PROVEN):** Existe **1 sola** entrada de deuda técnica
pendiente: TD-RBAC-03, originada en ADR-BACK-010 §3.6 (2026-05-07).
Requiere ADR que decida entre (a) asignar capability a un AGR
reservado, o (b) feature flag con gate doble.

### 1.3 Task plans con tareas no marcadas

`find .thyrox/context/work -name '*task-plan*.md'` → ~40 archivos.
Top 10 con más tareas sin marcar:

| Tareas pendientes / total | Task plan |
|--------------------------:|-----------|
| 154 / 154 | `2026-05-05-20-28-12-use-case-view-uml07-standalone-pass/` |
| 116 / 116 | `2026-05-07-14-49-04-uml-diagrams-deep-audit/` |
| 85 / 85 | `2026-04-23-18-51-33-plantuml-java-integration-impl/` |
| 83 / 83 | `2026-05-02-05-32-56-arq-mod-cajones/` |
| 72 / 75 | `2026-05-06-06-32-20-spanish-class-names-corpus-audit/` |
| 55 / 55 | `2026-05-02-06-33-05-rbac-cajones/` |
| 38 / 38 | `2026-05-07-23-36-40-use-case-view-std-010-compliance/` |
| 35 / 35 | `2026-04-29-09-52-26-source-final-cleanup/` |
| 34 / 34 | `2026-05-08-04-10-27-uc-view-domain-alignment/` |
| 32 / 32 | `2026-04-29-18-15-42-rbac-adr-superseding/` |

**Hallazgo H-03 (INFERRED):** La mayoría de estos planes son de WPs
que el ROADMAP no lista como "en curso". Probable causa: el trabajo
se ejecutó pero los checkboxes nunca se marcaron — el commit fue la
señal de cierre, no el `[x]` del plan. **No son backlog real**, son
artefactos históricos. Sólo los WPs declarados "en curso" en
ROADMAP.md son candidatos a backlog vivo.

### 1.4 Iniciativas declaradas "en curso" en ROADMAP.md

| ÉPICA | WP | Estado declarado |
|------:|----|------------------|
| 4 | repository-diagnostics | Phase 11 TRACK — pendiente CLOSURE-NOTICE |
| 5 | zero-warnings-build | Phase 11 TRACK — pendiente CLOSURE-NOTICE |
| 6 | deployment-pipeline | Phase 10 EXECUTE — bloqueado por refs muertas |
| 7 | source-references-audit | Phase 1 DISCOVER — audit-only |
| 9 | bootstrap-hardening | Phase 1 DISCOVER — F-NEW-8/9 pendientes |
| 10 | multi-wp-state-strategy | Phase 1 DISCOVER — pausado |
| — | source-rebuild hijos | 14/16 CERRADO v1, 2 DIFERIDO (infrastructure, operations) |

**Hallazgo H-04 (PROVEN):** ROADMAP no se actualiza desde finales de
abril. Las 6 ÉPICAs en curso llevan ~3 semanas sin movimiento
declarado. Decisión necesaria del ejecutor: cerrar lo cerrable
(ÉPICA 4, 5), abandonar lo bloqueado (ÉPICA 6), retomar lo pausado
(ÉPICA 7, 9, 10), o continuar otra dirección.

### 1.5 Build status

Último estado declarado (focus.md, 2026-04-29):
`make clean && make html` → `build succeeded` con 0 WARN / 0 ERR / 0 CRIT.
**No verificado en esta sesión.**

---

## Parte 2 — Análisis de normativas y propuesta de nueva

### 2.1 Inventario del corpus `source/normativa/`

| Subdominio | Archivos | Rango de IDs |
|------------|---------:|--------------|
| `estandares/` | 23 RST | `STD-001`..`STD-013` (huecos en 003, 004, 005) + 6 ADRs/guías no numeradas |
| `restricciones/` | 33 RST | `CNST-001`..`CNST-033` (contiguo) |
| `procedimientos/` | 75 RST | 7 series (ver tabla) |
| `gobernanza/` | 13 RST | `ADR-GOB-001`..`ADR-GOB-010` + `documentacion-corporativa` + `raci-rbac/` |
| `guias/` | 2 RST | sin numeración consistente |

**Series de procedimientos (último número usado):**

| Serie | Último | Significado del prefijo |
|-------|-------:|-------------------------|
| `proc-dev` | 004 | desarrollo backend / frontend |
| `proc-devops` | 002 | CI/CD, automatización |
| `proc-doc` | 014 | documentación |
| `proc-gob` | 013 | gobernanza |
| `proc-ops` | 003 | operación / despliegue |
| `proc-qa` | 004 | calidad / aseguramiento documental |
| `proc-req` | 019 | requisitos / UCs / FRs |

### 2.2 Huecos observables (PROVEN — del listado de archivos)

#### Huecos en numeración

- **STD-003, STD-004, STD-005:** ausentes. La serie salta de `std-002`
  a `std-006`. Los huecos son técnicos (no documentados como
  reservados); pueden llenarse con nuevas normativas o renumerarse.
- **CNST:** sin huecos. Próximo libre: `CNST-034`.
- **ADR-GOB:** sin huecos. Próximo libre: `ADR-GOB-011`.
- **PROC-DEV/DEVOPS/OPS/QA:** todos con números bajos y sin huecos.

#### Huecos temáticos (INFERRED — del cruce de existentes vs prácticas
implícitas)

| # | Tema | Evidencia de la ausencia |
|---|------|--------------------------|
| G-1 | **Logging y observabilidad estructurada** | `CNST-024` obliga JSON pero no hay STD que defina esquema, niveles, correlación de request id, ni redacción de PII (que `CNST-026` prohíbe sin definir cómo se aplica al log) |
| G-2 | **Manejo de errores y mapeo a HTTP** | `CNST-013` obliga "manejo estandarizado de excepciones DRF" sin definir el mapping excepción→status code ni el contrato de payload de error |
| G-3 | **Estrategia de testing y coverage** | No existe ningún STD/PROC sobre testing. La serie `proc-qa` cubre QA documental, no de código |
| G-4 | **Versionado de API REST** | `STD-013` cubre URLs y verbos, no estrategia de versionado (URI vs header, política de deprecación) |
| G-5 | **Gestión de secretos / configuración por entorno** | `ADR-sensitive-info-policy` (en `.thyrox/`) define qué es sensible, pero no hay STD/PROC en `source/normativa/` que normalice variables de entorno, rotación, almacenamiento |
| G-6 | **Procedimientos de seguridad** | No existe la serie `proc-sec`. Hay temas sueltos (RBAC, auth) pero ningún procedimiento (e.g. revocar credenciales, responder incidente, revisar auditoría) |
| G-7 | **Guía de creación de un ADR** | El corpus tiene ~30 ADRs entre `source/` y `.thyrox/context/decisions/` pero no hay una guía que estandarice su redacción |
| G-8 | **Política de rotación / expiración de capabilities** | `CNST-031` define permisos temporales máximo 6 meses, pero no hay PROC que describa el flujo de renovación / expiración |

### 2.3 Propuesta — candidatos a nueva normativa

Recomiendo **STD-014 — Logging y Observabilidad Estructurada** como
primera nueva normativa, por tres razones:

1. **Cierra un loop ya abierto:** `CNST-024` (JSON obligatorio) y
   `CNST-026` (PII prohibida en logs) son restricciones sin
   estándar que las haga ejecutables. Hoy la regla existe pero no
   el "cómo".
2. **Impacto transversal:** afecta backend, frontend (errores),
   infrastructure (agregación), auditoría (CNST-025). Una sola
   normativa desbloquea consistencia en 4 dominios.
3. **Bajo riesgo de regresión:** define convenciones nuevas que no
   contradicen ninguna existente.

**Alternativas equivalentes en utilidad** (si el ejecutor prefiere
otro tema):

| Candidato | ID propuesto | Cubre el gap | Esfuerzo |
|-----------|--------------|--------------|----------|
| Logging y observabilidad estructurada | `STD-014` | G-1 | M |
| Manejo de excepciones y mapeo HTTP | `STD-003` (llena hueco) | G-2 | M |
| Estrategia de testing | `STD-004` (llena hueco) | G-3 | L |
| Versionado de API REST | `STD-005` (llena hueco) | G-4 | S |
| Gestión de secretos | `STD-015` | G-5 | M |
| Procedimientos de seguridad (serie nueva) | `PROC-SEC-001` | G-6 | L (es una serie completa) |
| Guía de redacción de ADRs | `GUIA-GOB-003` | G-7 | S |
| Procedimiento de renovación de capabilities | `PROC-GOB-014` | G-8 | M |

S = small (un día), M = medium (2-3 días), L = large (≥1 semana).

### 2.4 Esqueleto sugerido para STD-014

```rst
.. _std-014:

================================================================
STD-014 — Logging y Observabilidad Estructurada
================================================================

:Identificador: STD-014
:Estado: Vigente
:Versión: 1.0.0
:Aplica a: Backend Django, frontend React, infrastructure
:Relacionados: CNST-024, CNST-025, CNST-026, ADR-GOB-XXX

Propósito
=========
Definir el esquema, niveles y contrato de los logs estructurados
exigidos por CNST-024, de forma que la prohibición de PII en logs
(CNST-026) y la inmutabilidad de auditoría (CNST-025) sean
verificables automáticamente.

Esquema obligatorio del evento de log
=====================================
Campos: ``timestamp``, ``level``, ``service``, ``request_id``,
``user_id`` (hashed), ``event``, ``message``, ``context`` ...

Niveles y semántica
===================
``DEBUG | INFO | WARNING | ERROR | CRITICAL`` — criterios y ejemplos.

Correlación de requests
=======================
Cabecera ``X-Request-ID``, propagación cross-service,
trace context.

Redacción de PII
================
Lista de campos prohibidos en texto plano; función ``redact()``;
testing.

Casos de prueba
===============
Fixture que valida el schema; test que falla si aparece PII.

Trazabilidad
============
- CNST-024 obliga JSON → este STD define el JSON.
- CNST-026 prohíbe PII → este STD define cómo no exponerla.
- CNST-025 obliga auditoría inmutable → este STD distingue
  log operacional de audit log.
```

---

## Parte 3 — Decisión requerida del ejecutor

Para avanzar necesito una decisión de las siguientes en este orden:

1. **¿Tema de la nueva normativa?** Recomendado: `STD-014` (logging).
   Alternativas válidas en §2.3.
2. **¿Renumerar los huecos de STD (003, 004, 005)?** O dejarlos como
   huecos y usar la siguiente disponible (014).
3. **¿Sincronizar `now.md` y ROADMAP.md** antes o después de crear la
   normativa? Recomendado: sincronizar primero — el estado actual no
   refleja la realidad y bloquea cualquier nuevo WP que dependa de
   fase declarada.

---

## Anexo — Comandos de verificación usados

```bash
ls .thyrox/context/work/ | wc -l                          # 190 WPs históricos
grep -E "^## TD-|^Estado: " .thyrox/context/technical-debt.md
find .thyrox/context/work -name "*task-plan*.md"
ls source/normativa/estandares/ | grep -oE "std-[0-9]+"
ls source/normativa/restricciones/ | grep -oE "cnst-[0-9]+" | sort -u
ls source/normativa/procedimientos/ | grep -oE "proc-[a-z]+-[0-9]+"
```

Todos los números citados en este documento provienen de la salida de
estos comandos en la rama `feature/iact-docs-backlog-review`
ejecutados el 2026-05-19.
