```yml
created_at: 2026-05-06 19:30:00
project: IACT-docs
work_package: 2026-05-06-00-31-12-api-socket-error-investigation
phase: Phase 3 — ANALYZE (followup post-cierre)
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Followup — Persistencia de task entries del Monitor (R-2.0 nueva)

## Contexto

Este WP definio originalmente las reglas R-1..R-5 + AP-1..AP-5
para comandos de larga duración (>5 min). En particular R-2.1
(`tail -f --pid=$PID`) resuelve el ciclo de vida del proceso
observado: el monitor cierra limpiamente cuando el PID muere.

Tras varias sesiones de uso intensivo del patrón (WPs 1..4 de la
sesión 2026-05-06, ~31 invocaciones de Monitor), el ejecutor
reporto que sigue cancelando manualmente task entries en la UI.
Este artefacto documenta el análisis y el fix aplicado.

## Diagnóstico

### Lo que R-2.1 hace bien

`tail -f --pid=$PID | grep --line-buffered ...`:

- `tail` recibe EOF cuando $PID muere (extension GNU).
- `grep` recibe SIGPIPE → exita.
- El comando del Monitor termina → status reportado por el harness:
  `stream ended, status=completed, EXIT=0`.

Verificado en logs: `execute/build-logs/sphinx-strict-*.log`
muestran `EXIT=0` y notificaciones "build succeeded" + "stream
ended" llegan en pocos segundos al terminar el proceso.

**Conclusión:** R-2.1 funciona correctamente para el ciclo de
vida del proceso/stream.

### Lo que R-2.1 NO arregla — task entries en UI

El propio R-2.2 lo declara:

> *"Cada llamada a Monitor(...) crea un task entry persistente
> en el UI del usuario. Estos entries:*
> - *No se eliminan al expirar (timeout) — quedan visibles como
>   'Monitor timed out'.*
> - *No se eliminan al completar limpiamente — quedan visibles
>   como 'completed'.*
> - *Solo se descartan con TaskStop (no siempre disponible) o al
>   cerrar la sesión."*

**Hechos verificados:**

1. `TaskStop` **no está disponible** en el runtime de Claude Code
   actual (verificado vía `ToolSearch` el 2026-05-06: solo
   `Monitor` y `TodoWrite` retornan resultados; ningún `TaskStop`
   ni `KillBash`).
2. Por lo tanto, el agente **no puede cerrar entries
   programáticamente**. El ejecutor humano tiene que cancelar
   cada una.
3. Esto se acumula rápidamente — en una sesión normal con N
   builds estrictos, hay N entries persistentes en la UI.

### Conteo en sesión 2026-05-06 (4 WPs encadenados)

| WP | Builds (Monitor invocations) |
|---|---|
| WP-1 rbac-v5-6-0-corpus-alignment | 7 |
| WP-2 uc-opr-sup-reserved-open-closed | 8 |
| WP-3 mapeo-uc-completion | ~5 |
| WP-4 corpus-tech-debt-cleanup | 11 (con retries) |
| **Total acumulado** | **~31 task entries** |

Cada una requirió cancelación manual del ejecutor.

### Por qué se violó R-2.2

R-2.2 explícitamente dice: *"Reusar el mismo Monitor si se sigue
observando el mismo log/proceso, en lugar de cancelar y rearmar"*
y *"Un solo Monitor por work, no uno por iteración"*.

El agente violó esto: cada batch (B-1, B-2, ...) lanzó un
Monitor nuevo con un log distinto en lugar de reusar uno solo
que esperara la condición de salida del build.

## Solución aplicada — R-2.0 (NUEVO)

Para builds locales **estimados <5 min** (que son TODOS los
builds Sphinx del proyecto, típicamente 1-3 min), el patrón
correcto **NO es Monitor**.

### Patrón canónico R-2.0

```bash
# Lanzar build en background (detached, sin task entry)
nohup bash -c "make html SPHINXOPTS='-W -j auto' 2>&1; echo EXIT=\$?" \
    > "$LOG" 2>&1 &
PID=$!
disown $PID

# Esperar condición de salida con Bash run_in_background=true.
# Esto NO crea un task entry persistente — solo un shell que
# notifica al completarse.
Bash(
  command='until grep -qE "^EXIT=" "'$LOG'"; do sleep 2; done && tail -5 "'$LOG'"',
  run_in_background=true,
  description="esperar build sphinx"
)
```

**Resultado:**

- 1 notificación al chat cuando el build termina.
- 0 task entries persistentes.
- 0 cancelaciones manuales del ejecutor.

### Tabla de decisión

| Caso | Patrón canónico | Por qué |
|------|-----------------|---------|
| Build local **<5 min** | `Bash run_in_background=true` + `until` loop | Sin task entry persistente; notificación única al final |
| Build local **5-30 min** | `Monitor` con `tail -f --pid=$PID` (R-2.1) | Puede requerir progress mid-stream; entry persistente acceptable por tiempo total |
| Stream **sin fin** (logs en vivo, PR webhooks) | `Monitor persistent: true` + `TaskStop` al final (cuando exista) | Diseño exige Monitor; cleanup manual si no hay TaskStop |
| Operación **silenciosa** que no necesitas observar | `Bash run_in_background=true` directamente | Fire-and-forget |

### Reordenamiento R-2

- **R-2.0 (NUEVO, primero)**: Para builds <5 min usar `Bash
  run_in_background=true` + `until`. **NO Monitor.**
- R-2.1 (existente): Si Monitor es necesario, `tail -f --pid`
  para cierre limpio del stream.
- R-2.2 (existente): Reusar Monitors; minimizar el count.

## Fuente del fallo (root-cause secundaria)

El agente conocía R-2.2 pero **no la respetaba** porque no había
un patrón alternativo concreto y vinculante para builds cortos.
R-2.1 era la guía dominante en su contexto, así que aplicaba
Monitor por default sin cuestionarse.

R-2.0 (nuevo) corrige esto al **prohibir Monitor para builds
<5 min** y dar el patrón alternativo explícito.

## Aplicación

- `.claude/rules/long-running-commands.md` actualizado con R-2.0.
- Tabla de decisión agregada al inicio de la sección R-2.
- Patrón canónico Bash + `until` documentado.
- Anti-patrón AP-1 ampliado: lanzar Monitor para builds <5 min
  ahora también es anti-patrón.

## Prevención futura

Cuando el agente vaya a observar un proceso largo, primero debe
preguntarse:

1. ¿Duración estimada <5 min? → R-2.0 (Bash + until).
2. ¿Duración 5-30 min? → R-2.1 (Monitor + tail -f --pid).
3. ¿Sin fin natural? → R-2.2 (Monitor persistent + TaskStop).

Esto se documenta como árbol de decisión visible al inicio de la
regla.

## Refs

- WP origen: `2026-05-06-00-31-12-api-socket-error-investigation`.
- Sesión donde se detectó el problema: 2026-05-06 (WPs 1..4
  encadenados, ~31 entries acumuladas).
- Tool runtime verificado el 2026-05-06: `Monitor`, `TodoWrite`,
  `Bash` disponibles; `TaskStop` no expuesto.
