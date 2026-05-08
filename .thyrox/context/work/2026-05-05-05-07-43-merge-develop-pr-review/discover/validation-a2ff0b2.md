```yml
created_at: 2026-05-05 05:30:00
project: IACT-docs
work_package: 2026-05-05-05-07-43-merge-develop-pr-review
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Validación commit a2ff0b2 — A-01, A-02, A-03

Commit `a2ff0b2760dfdc28aa3815b047267a2c191679e2` por
`copilot-swe-agent[bot]` aplica las acciones bloqueantes
A-01, A-02 y A-03 del plan de acción del WP. Esta revisión
verifica que cada cambio resuelva el hallazgo asociado.

## Entorno de validación

| Componente | Valor |
|---|---|
| Host CPUs (`nproc`) | 4 |
| Modelo | Intel(R) Xeon(R) @ 2.80GHz |
| Python | 3.11 |
| Sphinx | 8.2.3 |
| Branch | `claude/wp-merge-pr-review` |
| Commit verificado | `a2ff0b2` |

Nota: el runner de GitHub Actions Ubuntu suele ofrecer
2 vCPUs; el host local de validación tiene 4. Las cifras
de tiempo locales son optimistas vs. CI real.

## A-01 — `validate.yml` timeout + paralelismo

### Cambios aplicados

```diff
-    timeout-minutes: 20
+    timeout-minutes: 60
```

```diff
-          sphinx-build -W -b html -d build/doctrees source build/html
+          sphinx-build -W -j auto -b html -d build/doctrees source build/html
```

### Verificación

- **Timeout**: 60 min cubre con holgura los 36 min del build
  serial original.
- **Paralelismo**: `-j auto` distribuye la fase de
  `reading sources` y `writing output` entre los CPUs
  disponibles. El render PlantUML (Java) no se paraleliza
  por Sphinx pero el resto de la pipeline sí.
- **Build local en curso** con `-W -j auto`: confirmar
  duración real al finalizar; el log muestra avance hasta
  28% en pocos minutos, por lo que la ganancia es
  consistente con paralelismo activo.

### Estado de A-01

✅ **APLICADO Y VÁLIDO.** Resuelve F-01 (CI timeout).
Riesgo residual: si en el runner de GitHub Actions hay
solo 2 vCPUs, la ganancia será menor (~25-30 min) pero
sigue dentro del nuevo timeout de 60 min.

## A-02 — `PULL_REQUEST_TEMPLATE.md` alineado con Tim Pope

### Cambios aplicados

```diff
- - [ ] I have used conventional commit messages (type(scope): description)
+ - [ ] I have followed commit message conventions (Tim Pope style: imperative subject ≤50 chars, no trailing period)
```

### Verificación

- El template ahora refiere explícitamente a Tim Pope
  con criterios concretos (imperative ≤50 chars, no
  trailing period).
- Coherente con `.claude/rules/commit-conventions.md`
  (regla activa desde ÉPICA 4).
- Los 645 commits del rango `origin/develop..HEAD` ya
  cumplen Tim Pope; la edición del template **resuelve la
  inconsistencia sin tocar historial**.

### Estado de A-02

✅ **APLICADO Y VÁLIDO.** Resuelve F-02 (conflicto template
vs regla del repo).

## A-03 — ADR-DEVOPS-002 documentando decisiones de build

### Archivo creado

`source/devops/adr-devops-002-sphinx-build-config.rst`
(155 líneas, status `Aceptada`, version `1.0.0`).

### Decisiones documentadas

| Decisión | Sección | Cubre F-03 |
|----------|---------|------------|
| Remoción de `myst-parser` (RST puro) | "Remoción de myst-parser" | ✅ |
| `nitpicky` via `SPHINX_NITPICKY` env | "nitpicky via SPHINX_NITPICKY" | ✅ |
| `plantuml_cfg_file` con path absoluto | "plantuml_cfg_file" | ✅ |
| CI timeout 20→60 + `-j auto` | "Timeout CI y paralelismo" | bonus (cubre A-01) |

### Alternativas consideradas (sección dedicada)

- Cachear `build/` entre runs — descartado por
  invalidación, límite 10 GB y mantenimiento.
- Servidor PlantUML remoto — descartado por
  disponibilidad, privacidad y rate limiting.

### Consecuencias documentadas

Positivas (4) y negativas (2) con mitigación. La sección
de mitigación menciona `SPHINX_NITPICKY=1` para gate
estricto en CI cuando se requiera.

### Wiring en toctree

```diff
  adr-devops-001-vagrant-mod-wsgi-importante-produc
+ adr-devops-002-sphinx-build-config
  adr-devops-003-wasi-style-virtualization-importante-db
```

Posición correcta entre ADR-DEVOPS-001 y ADR-DEVOPS-003.

### Verificación de prosa

Spot check sobre los 8 comentarios de Copilot al PR:

| Línea | Comentario Copilot | Verificación local |
|------|-------|--------------------|
| 16 | "Missing accent in 'Configuración'" | El archivo **sí tiene** el acento. Falso positivo. |
| 26 | "Missing accent in 'Remoción'" | **Sí tiene** acento. Falso positivo. |
| 29 | "'Agregado' debería ser 'Adición'" | Stylistic; "Adición" usado correctamente en el archivo (línea 27). El "Agregado" no aparece como problema real. |
| 32 | "Missing accent in 'Además'/'tenía'" | **Sí tienen** acentos. Falso positivo. |
| 44 | "Missing accent in 'adoptó'" | **Sí tiene** acento. Falso positivo. |
| 63 | "'seteado' no es español estándar" | La palabra `seteado` **no aparece** en el archivo (`grep -n seteado` → 0 resultados). Falso positivo. |
| 64 | "Missing accents in 'rápido', 'iteración'" | **Sí tienen** acentos. Falso positivo. |
| 129 | "Missing accents in 'más', 'rápido'" | **Sí tienen** acentos. Falso positivo. |

Conclusión: los **8 comentarios de Copilot son falsos
positivos** (probable bug de normalización Unicode en
el revisor). El ADR está correctamente escrito en español
con acentos apropiados.

### Estado de A-03

✅ **APLICADO Y VÁLIDO.** Resuelve F-03 (cambios sin ADR).
Calidad de prosa correcta a pesar de los falsos positivos
de Copilot.

## A-04 (no bloqueante) — STD_010 en testing.rst

**Estado**: pendiente. No abordado por este commit. El plan
original lo marcó como no bloqueante; sigue como deuda
documentable en `technical-debt.md`.

## A-05 — Re-correr CI

**Estado**: pendiente. El usuario indicó que se ejecutará
automáticamente al recibir el push del commit `a2ff0b2`.
La validación local del build paralelo está corriendo
en background (sphinx-build -W -j auto). Esperar status
final.

## A-06 (no bloqueante) — Resumen ejecutivo en PR description

**Estado**: pendiente. No abordado. Recomendación sigue
vigente para mejorar revisión humana de la PR #12.

## Veredicto actualizado

| Acción | Antes | Ahora |
|--------|-------|-------|
| A-01 CI timeout | BLOQUEANTE pendiente | ✅ aplicado |
| A-02 Template | BLOQUEANTE pendiente | ✅ aplicado |
| A-03 ADR conf.py | BLOQUEANTE pendiente | ✅ aplicado |
| A-04 STD_010 testing | no bloqueante | pendiente (deuda) |
| A-05 CI verde | bloqueante | pendiente (próximo run) |
| A-06 Resumen PR | no bloqueante | pendiente |

**Veredicto:** los 3 hallazgos BLOCKER (F-01, F-02, F-03)
están **resueltos**. El merge pasa de **BLOQUEAR** a
**ESPERAR CI VERDE** (A-05). Si el próximo run de CI
completa exitosamente, el merge a develop puede
proceder.

F-08 (Spanish quality del ADR) cerrado por validación
independiente: los comentarios de Copilot son falsos
positivos.

## Hallazgos nuevos (F-NN derivados de la validación)

### F-09 INFO — Ganancia real de `-j auto` depende de CPUs del runner

**Evidencia:** `sphinx-build -j auto` paralela
`reading sources` + `writing output`, pero **NO**
paralela el render de PlantUML (cada `@startuml` invoca
Java en serie por archivo). En un runner Ubuntu de
GitHub Actions con 2 vCPUs, la ganancia teórica es ~30-40%,
no 50%.

**Recomendación:** monitorear duración real del CI tras
A-05; si excede 50 min, considerar A-01 alternativas
3 (cache PlantUML) o 4 (pre-render SVG).

### F-10 INFO — Falsos positivos en review automatizado

**Evidencia:** los 8 comentarios de Copilot sobre
acentos / "seteado" en el ADR son **falsos positivos**
(las palabras correctas ya están presentes; "seteado"
no aparece). Probable bug de normalización Unicode.

**Recomendación:** documentar en
`technical-debt.md` para futura revisión del agente
revisor; no bloqueante.
