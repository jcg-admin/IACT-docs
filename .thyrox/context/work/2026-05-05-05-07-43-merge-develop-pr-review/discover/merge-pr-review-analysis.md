```yml
created_at: 2026-05-05 05:07:43
project: IACT-docs
work_package: 2026-05-05-05-07-43-merge-develop-pr-review
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Merge PR review — feature/solve-problem-docs → develop

## Resumen ejecutivo

**Veredicto: BLOQUEAR** — el merge no debe pasar a develop
en su estado actual. Hallazgo crítico F-01 (CI timeout)
hace que la rama no pueda construir en Actions con la
configuración actual. Requiere acción correctiva antes de
re-intentar el merge.

| Métrica | Valor |
|---|---|
| Commits ahead of develop | 645 |
| Commits behind develop | 0 |
| Files changed vs develop | 5,823 |
| Insertions / Deletions | 1,425,759 / 2,370 |
| RST source files | 2,647 |
| PlantUML directives | 965 |
| Local build duration | **~36 min** |
| CI `validate.yml` timeout | **20 min** |
| Local build (warnings) | **0** ✅ |
| Local build (succeeded) | **sí** ✅ |
| CI build (último run reportado) | **canceled at 24%** ❌ |

## Hallazgos por severidad

### F-01 BLOCKER — CI build timeout

**Evidencia (provista por el ejecutor):**

```
writing output... [ 24%] normativa/procedimientos/proc-gob-012-revision-documental
Error: The operation was canceled.
Terminate orphan process: pid (3459) (sphinx-build)
```

**Causa raíz (verificada localmente):**

- `.github/workflows/validate.yml` declara `timeout-minutes: 20`.
- Build local toma **35 min 44 s** (start 04:27:33, end 05:03:17).
- 965 directivas PlantUML — cada render via Java/PlantUML JAR
  toma 1-3 s en frío. 965 × 2 s ≈ 32 min solo en PlantUML.
- `-W` activo (warnings as errors) — cualquier warning vuelve
  el build rojo, pero el problema NO es warnings (son 0 local
  según F-04), es **tiempo de wall clock**.

**Impacto:** ningún CI run de la rama puede completarse;
imposible verificar el estado real de la PR vía GitHub Actions.

**Acciones correctivas (ordenadas por costo):**

| # | Acción | Esfuerzo |
|---|--------|----------|
| 1 | Subir `timeout-minutes: 20` → `60` en validate.yml | bajo |
| 2 | Activar `sphinx-build -j auto` (paralelo) | bajo |
| 3 | Cachear PlantUML output entre runs (actions/cache) | medio |
| 4 | Pre-renderizar PlantUML a SVG y commitearlos | medio |
| 5 | Split CI: build incremental por dominio | alto |

Recomendación inmediata: combinar #1 y #2.

### F-02 BLOCKER — Conflicto de convención de commits

**Evidencia:**

- `.claude/rules/commit-conventions.md` declara estilo Tim Pope
  desde ÉPICA 4 (subject imperativo, sin prefijo `type(scope):`).
- `.github/PULL_REQUEST_TEMPLATE` (citado por el ejecutor) pide
  "conventional commit messages (type(scope): description)".
- 0 de 645 commits del rango `origin/develop..HEAD` siguen el
  formato convencional.

**Inconsistencia documentada:** la regla del repo y el
template del PR se contradicen. Copilot reporta el incumplimiento
contra el template, pero los commits sí cumplen Tim Pope (la
política vigente del repo).

**Acciones correctivas:**

- Alinear el template del PR con `.claude/rules/commit-conventions.md`
  (eliminar la línea de "Conventional Commits" o reemplazarla por
  Tim Pope).
- O bien: revertir la regla a Conventional Commits (decisión del
  ejecutor — pero entonces los 645 commits violan la regla y
  habría que rehacer el historial, lo cual es destructivo).

**Recomendación:** ajustar el template (acción no destructiva).

### F-03 MAJOR — Cambios a `conf.py` y dependencias sin ADR visible

**Evidencia (diff origin/develop..HEAD):**

```python
# conf.py — extension changes
- 'myst_parser',
+ 'sphinx_tabs.tabs',

# nitpicky configurable (env var)
+ nitpicky = os.environ.get('SPHINX_NITPICKY', '0') == '1'

# suppress_warnings removed (anti-pattern detected)
- suppress_warnings = ['misc.highlighting_failure']

# plantuml_cfg_file added (path absoluto)
+ plantuml_cfg_file = _styles_puml
```

```toml
# pyproject.toml — dependencies removed
- "myst-parser==4.0.1"
- "sphinx-toolbox==4.1.2"
- "markdown-it-py==3.0.0"
- "mdit-py-plugins==0.5.0"
- "mdurl==0.1.2"
```

**Riesgo:** decisión de "remove Markdown support" tiene impacto
en cualquier `.md` existente y en cualquier proceso que dependa
de `myst-parser`. Requiere ADR explícito documentando decisión.

**Acciones correctivas:**

- Verificar existencia de ADR para "RST only — Markdown removed".
  Si existe, citar en la descripción del PR.
- Si no existe, redactar `adr-content-format-rst-only.md` antes
  del merge.
- Validar que ningún archivo en `source/` es `.md` que rompería:
  `find source -name "*.md"`.

### F-04 MINOR — Build limpio local (0 warnings)

**Verificado:** `make clean && make html` retorna
`build succeeded` con **cero** WARNING. El claim del commit
`42b9bf2b` ("Fix 168 pre-existing RST warnings to achieve
0-warning build") es **válido**.

Acción: ninguna. Reconfirmar en CI una vez resuelto F-01.

### F-05 MAJOR — Stack-agnostic incompleto (STD_010)

**Evidencia:** spot-check en `source/requisitos/casos-uso/auth/`:

```
uc-auth-01/implementacion-tecnica.rst:
   - Django + Django REST Framework (DRF)
   - DRF SimpleJWT (CNST-009)

uc-auth-04/testing.rst:
   import bcrypt, pytest
   @pytest.mark.django_db
   assert bcrypt.checkpw(b'NewSecure2026!@', ...)

uc-auth-02/testing.rst:
   from apps.auth_app.services import AuthService
```

56 ocurrencias de palabras-marker en cluster `auth/` y `users/`
(Django, DRF, bcrypt, imports Python concretos).

**Inconsistencia:** múltiples commits declaran "STD_010 abstracted
framework names" — pero los testing.rst de UCs originales
preservaron el código Python con dependencias concretas. La
abstracción se aplicó parcialmente.

**Acciones correctivas:**

- Decidir alcance de STD_010: ¿aplica también a testing.rst?
- Si sí: completar la abstracción en cluster auth/users/access
  pendientes. ~56 ocurrencias.
- Si no: documentar excepción en STD_010 (testing puede ser
  concreto por practicidad).

### F-06 MINOR — Cambios masivos a `domain-model/`

**Evidencia:** refactor "one class per file" produjo 26 archivos
nuevos en `domain-model/` con stubs y luego limpieza en commits
sucesivos (`Add 41 stub classes`, `Remove stub classes`,
`Fix user.rst — one class per file, no stubs`).

**Riesgo:** el flujo de stubs → no stubs sugiere iteración no
planeada. Validar:

- ¿Las 26 clases canónicas finales están todas alineadas con
  la nueva estructura?
- ¿Las referencias `:doc:` de UCs apuntan correctamente?

**Verificación:** build local pasa con 0 warnings → referencias
están sanas. Acción: ninguna inmediata.

### F-07 MINOR — Volumen y tamaño de la PR

**Métrica:** 645 commits, 5,823 archivos cambiados, ~1.4M
inserciones. Aun cuando todo es válido individualmente, la PR
es prácticamente irrevisable manualmente.

**Acciones correctivas (no bloqueantes):**

- Para futuras PRs: dividir trabajo grande en PRs por dominio
  (RST formatting, RBAC v5.5.0 reconciliation, Kruchten views,
  domain-model, etc.) en lugar de acumular 645 commits en una.
- Para esta PR: agregar tabla resumen en la descripción del
  PR mapeando los 16+ WPs cerrados a sus efectos arquitectónicos.

## Mapeo PR Checklist (validación independiente)

| Item | Copilot | Mi validación |
|------|---------|---------------|
| Tested locally (make html) | ✅ | ✅ verificado: 0 warnings, build OK |
| RST formatting | ✅ | ✅ implícito (0 warnings) |
| Conventional commit messages | ⚠️ no | ⚠️ correcto: NO siguen Conventional, SÍ siguen Tim Pope (regla vigente del repo). Conflicto template vs regla — F-02 |
| Documentation updated | ✅ | ✅ trivialmente verdadero (PR es 100% docs) |
| No breaking changes conf.py/deps | ⚠️ con cambios | ⚠️ confirmado — F-03; requiere ADR |

## Action plan (orden recomendado)

| ID | Acción | Bloqueante | Owner |
|----|--------|------------|-------|
| A-01 | Subir `timeout-minutes` a 60 + activar `-j auto` en `validate.yml` | sí (F-01) | DevOps |
| A-02 | Alinear `PULL_REQUEST_TEMPLATE.md` con `commit-conventions.md` (Tim Pope) | sí (F-02) | NestorMonroy |
| A-03 | Verificar / crear ADR para Markdown removal y `nitpicky` env var | sí (F-03) | NestorMonroy |
| A-04 | Decidir alcance STD_010 (testing.rst) y aplicar consistencia | no (F-05) | NestorMonroy |
| A-05 | Re-correr CI tras A-01..A-03 y confirmar pase | sí | NestorMonroy |
| A-06 | Agregar resumen ejecutivo de WPs cerrados en descripción del PR | no (F-07) | NestorMonroy |

## Veredicto final

**BLOQUEAR el merge a develop** hasta resolver A-01, A-02, A-03 y
A-05. Sin CI verde la PR no debe mergearse — la regla de no-merge-without-green-CI
está implícita por el `validate.yml` y debe respetarse.

A-04 y A-06 son recomendados pero no bloqueantes si se documentan
como deuda en `technical-debt.md`.
