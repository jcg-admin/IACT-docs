```yml
created_at: 2026-05-05 16:10:00
project: IACT-docs
work_package: 2026-05-05-14-49-16-use-case-view-uml07-rebuild
phase: Phase 1 — DISCOVER
author: Nestor Monroy
status: Activo
version: 1.0.0
```

# Decisions Log — WP use-case-view-uml07-rebuild

> Decisiones tomadas durante el WP, ordenadas cronológicamente.
> Decisiones globales (no específicas del WP) van a `.thyrox/context/decisions/`.
> Decisiones aquí están ligadas al contexto puntual de este WP.

## D-01 — Crear `.claude/rules/git-flow.md` como regla auto-cargada

**Fecha:** 2026-05-05 ~14:50
**Contexto:** El proyecto venía sin convención escrita de branching;
varios WPs habían acumulado deuda de proceso (commits post-merge en
`claude/wp-merge-pr-review`, intentos de PR a `develop` directo).

**Decisión:** Codificar la política de branching como regla
auto-cargada (`.claude/rules/git-flow.md`), no sólo como ADR. Las
reglas en `.claude/rules/` cargan en cada sesión (I-009) — críticas
para que cualquier sesión futura respete el flujo sin tener que
consultar un ADR.

**Alternativas descartadas:**

- *Sólo ADR en `.thyrox/context/decisions/`:* lazy-load, no garantiza
  que se aplique sin lectura explícita.
- *Sólo entrada en CLAUDE.md:* mezcla convenciones operacionales con
  contexto del proyecto. Las reglas merecen archivo propio.

**Refs:** PR #14, commit `9007137d`, ADR-pendiente.

---

## D-02 — R-03: `feature/<wp>` integra a `feature/solve-problem-docs`, NO a `develop`

**Fecha:** 2026-05-05 ~14:55
**Contexto:** Sub-features del refactor masivo de docs IACT (cnst-033,
arquitectura-tecnica-content, repository-diagnostics, etc.) deben
agruparse antes de tocar `develop`. Sin rama de feature padre, cada
PR a `develop` exponía 30+ commits poco relacionados.

**Decisión:** `feature/solve-problem-docs` es la rama padre del trabajo
en curso. Todos los `feature/<wp-slug>` mergean primero ahí. Sólo cuando
solve-problem-docs está coherente y validado, se integra a `develop` con
PR independiente.

**Alternativas descartadas:**

- *PR directo a `develop`:* viola separación de scope, dificulta revert.
- *Rama `develop-iact-docs` paralela:* añade complejidad sin valor sobre
  una rama feature padre.

**Beneficios:**

- Aislar feature completo del resto de develop.
- Validar coherencia entre sub-features.
- Revert quirúrgico (sólo el merge a develop, no commits).
- Code review por sub-feature en su scope.

**Refs:** `.claude/rules/git-flow.md` R-03, post-mortem en R-08.

---

## D-03 — PR #14 como vehículo de integración (no `git push` directo)

**Fecha:** 2026-05-05 16:00
**Contexto:** Tras el merge local `feature/cnst-033-uml-conformance →
feature/solve-problem-docs`, el push falló con HTTP 403 — branch
protection en `feature/solve-problem-docs` requiere PR.

**Decisión:** Aceptar la branch protection (no buscar bypass).
Crear PR #14 vía GitHub MCP. Resetear local refs no destructivamente
(`git branch -f` en lugar de `git reset --hard`) para evitar
divergencia con origen.

**Alternativas descartadas:**

- *`git push --force` con bypass:* ni siquiera lo intenté — viola
  política de R-04 y la safety norm general (CLAUDE.md).
- *Pedir override de protection a admin:* innecesario; el PR es
  exactamente el mecanismo correcto.

**Refs:** PR #14, commit local `4066f925` (descartado vía branch -f).

---

## D-04 — Investigar CI antes de mergear PR #14 (opción A sobre B/C)

**Fecha:** 2026-05-05 16:05
**Contexto:** PR #14 abrió con `mergeable_state: unstable` — el job
`validate` (sphinx-build -W + validate-plantuml) reporta failure tras
29 minutos.

**Decisión:** Reproducir el strict build localmente antes de mergear.
Identificar causa exacta del failure. Decidir fix vs override basado
en el diagnóstico, no en suposiciones.

**Alternativas descartadas:**

- *(B) Mergear igualmente:* propaga build roto a rama padre. Eleva
  costo de cualquier integración futura desde otra sub-feature.
- *(C) Mergear ahora, fix después:* aceptable si el fallo fuera
  conocido como cosmético. Sin diagnóstico previo es apuesta a ciegas.

**Beneficio principal de A:** 5-10 min de costo, ganamos información
para decidir entre fix-blocking, fix-deferred, u override informado.

**Output esperado:** archivo
`discover/build-logs/sphinx-strict-pr14-{HH-MM}.log` con causa raíz
identificada.

**Refs:** PR #14 check_run 74443710941, run 25385055640.

---

## D-05 — Codificar regla de persistencia de build logs

**Fecha:** 2026-05-05 16:10
**Contexto:** Durante D-04 redirigí output de `sphinx-build -W` a
`/tmp/sphinx.log`. El ejecutor (humano) corrigió: los build logs
deben vivir en el WP activo, no en `/tmp`.

**Decisión:** Crear `.claude/rules/build-logs.md` que codifica:

- Logs de build van a `{wp}/{stage}/build-logs/{cmd}-{ctx}-{HH-MM}.log`.
- Naming: `sphinx-strict-pr14-16-10.log`.
- Excepción: builds exploratorios < 30s sin warnings nuevos pueden ir
  a stdout.
- Trazabilidad: claims que citan logs deben referenciar el archivo.

**Alternativas descartadas:**

- *Memoria informal:* falla — el ejecutor tuvo que recordármelo.
- *Sólo nota en CLAUDE.md:* mezcla convenciones operacionales.

**Beneficio:** logs son evidencia diagnóstica reproducible. En `/tmp`
se pierden y los claims que dependen de ellos se degradan a SPECULATIVE
(I-012 + evidence-classification).

**Refs:** `.claude/rules/build-logs.md`.

---

## D-06 — Fix de CI failure: rename ETL→Pipeline en uc-log-02

**Fecha:** 2026-05-05 16:50
**Contexto:** Strict build local reproduce el failure de CI con
**4 warnings reales** (la 5ª es ruido de race condition por dos builds
simultáneos):

- 2 warnings `toc.not_readable`: `uc-log-02/diagramas-uml/index.rst:7`
  refiere `componentes-pipeline-log` y `secuencia-de-consulta-pipeline-log`
  pero los archivos tienen el nombre antiguo `*-etl-log.rst`.
- 2 warnings `toc.not_included`: los 2 archivos `*-etl-log.rst` quedaron
  huérfanos.

**Causa raíz:** El sweep ETL→Pipeline (CNST-033 §8.2) actualizó el toctree
referenciador (`index.rst`) pero olvidó renombrar los 2 archivos
referenciados. Es deuda del WP `domain-model-residual-spanish-pass`.

**Decisión:** Fix minimal — rename de los 2 archivos vía `git mv` y
actualizar sólo los títulos H1 internos para reflejar "Pipeline log".

**Alcance NO incluido (separado como TD):**

- PlantUML interno en estos 2 archivos sigue usando `ETLScheduler`,
  `sp_etl_maestro`, `/logs/etl/`, `ETLLogEndpoint`. Estos son
  identificadores que reflejan implementación real (component IDs,
  stored procedure names, HTTP routes). Su rename a Pipeline requiere
  decisión arquitectónica separada que CNST-033 no resolvió.
- Crear TD-NN en `.thyrox/context/technical-debt.md` para tracking.

**Refs:** `discover/build-logs/sphinx-strict-pr14-16-15.log` (5 warnings
identificadas), `discover/build-logs/sphinx-strict-postfix-*.log`
(verificación post-fix), commits del WP `domain-model-residual-spanish-pass`.

**Verificación:** Postfix build ejecutándose. Espera EXIT=0 + 0 warnings
para validar fix antes de commit.

**ACTUALIZACIÓN POST-COMMIT (16:55):** El build limpio (single, no race
condition) revela que el fix de D-06 sólo resuelve **4 de ~73 warnings**.
La medición original de "5 warnings" provino de dos builds corriendo
concurrentemente y stompando entre sí — observable falso. Ver D-06b.

---

## D-06b — Realización: el CI failure no es 4 warnings, es ~73

**Fecha:** 2026-05-05 16:55
**Contexto:** Post-commit `405751c1` (rename ETL→Pipeline en uc-log-02),
ejecuté un build limpio (single process, doctrees cleared) para validar
0 warnings. Resultado parcial al 69% del build: **73 warnings ya
contadas**, build aún corriendo.

**Reclasificación de warnings:**

| Categoría | Count aprox | Patrón |
|-----------|-------------|--------|
| `toc.not_readable` + `toc.not_included` (uc-log-02) | 4 | Resuelto por D-06 |
| `Title overline/underline too short` | ~12 | Typography (RST estricto) |
| `unknown document — domain-model → casos-uso` | ~3 | UC paths que no existen |
| `unknown document — use-case-view/{module}/index.rst → diagrama-de-caso-de-uso` | ~50+ | **Forward refs del WP conformance-pass a archivos que pertenecen al WP rebuild (este WP, en DISCOVER)** |

**Causa raíz arquitectónica:** El WP `use-case-view-uml07-conformance-pass`
escribió `:doc:` refs en 11 archivos `use-case-view/{module}/index.rst`
asumiendo que cada UC de `casos-uso/` tendría un sub-archivo
`diagramas-uml/diagrama-de-caso-de-uso.rst`. Pero la creación de esos
sub-archivos pertenece al WP activo `use-case-view-uml07-rebuild`,
que sigue en Phase 1 DISCOVER.

**Implicación:** El fix de D-06 era necesario pero no suficiente. PR #14
sigue con CI roto.

**Decisión metodológica:** No comprometerme con un fix más antes de:

1. Esperar el build limpio completo (conteo final exacto).
2. Presentar al ejecutor las 3 alternativas:
   - **Path 1:** Remover los `:doc:` forward-refs en los 11 module
     index.rst (~30 min, pierde cross-references hasta que rebuild WP
     los re-cree).
   - **Path 2:** Crear stubs `diagrama-de-caso-de-uso.rst` para
     ~80 UCs (~1-2h scripted, deja stubs visibles en docs publicados).
   - **Path 3:** Bloquear PR #14, avanzar WP rebuild hasta EXECUTE
     (días/semanas, integración limpia).

**Refs:** `discover/build-logs/sphinx-strict-postfix-16-51.log` (en
progreso, build limpio); commit `405751c1` (fix parcial).

**Lección registrada como invariante:**

- Nunca confiar en un build con 2+ procesos sphinx-build simultáneos.
  Race condition produce conteos falsamente bajos.
- Antes de declarar "X warnings", verificar `pgrep -af "sphinx-build" |
  wc -l` = 1 durante todo el run.

---

## Decisiones pendientes

- **D-07 (post-merge PR #14):** orden de revisión de `feature/
  arquitectura-tecnica-content` y `claude/review-project-config-V8Fg5`.
- **TD-NN (track separado):** vocabulario PlantUML interno
  (ETLScheduler, sp_etl_maestro, /logs/etl/, ETLLogEndpoint) — decidir
  si CNST-033 §8.2 lo cubre o requiere addendum.
