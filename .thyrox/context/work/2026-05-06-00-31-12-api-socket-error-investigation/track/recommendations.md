```yml
created_at: 2026-05-06 00:45:00
project: IACT-docs
work_package: 2026-05-06-00-31-12-api-socket-error-investigation
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Recomendaciones operacionales — Evitar `cli_sse_liveness_timeout`

> Causa raíz documentada en `analyze/socket-error-root-cause.md`:
> el cliente Claude Code usa SSE con liveness timeout. Tool_exec
> foreground >5 min sin output → el stream cae. Estas
> recomendaciones aplican a todos los WPs futuros con builds o
> comandos de larga duración.

## Reglas operacionales

### R-1 — Comandos >5 min siempre en background

Cualquier comando con duración estimada >5 minutos (build
completo, tests E2E, prerender masivo, batch generation) se lanza
con `nohup ... &` o `Bash run_in_background=true`. El agente
**NO** espera el resultado en foreground.

```bash
# CORRECTO
nohup bash -c "rm -rf build/html && sphinx-build -W -j auto ..." > "$LOG" 2>&1 &
disown

# INCORRECTO (foreground >5 min)
sphinx-build -W -j auto -b html source build/html
```

### R-2 — Monitor con grep line-buffered para outcome

Para comandos en background con outcome conocido (success/failure
markers), usar `Monitor` con `tail -f LOG | grep --line-buffered
"PATTERN"`. Cada línea emitida resetea el liveness timer.

```python
Monitor(
  command='tail -f $LOG | grep -E --line-buffered "^EXIT=|build succeeded|FAIL"',
  description="strict build outcome",
  timeout_ms=1800000  # 30 min, monitor sobrevive el build
)
```

### R-3 — Probes periódicos cuando no hay output natural

Si una espera no tiene marcadores naturales para grep (e.g.
proceso silencioso con outcome sólo al final), emitir tool_uses
cortos cada 3-4 min:

```bash
# Cada N minutos, hacer un check breve que produzca tool_use
ls -la <path>      # 0.1s, suficiente para mantener SSE vivo
git status --short # idem
```

### R-4 — Persistir logs en WP para evidencia

Logs de comandos largos siempre redirigidos a archivo dentro de
`{wp}/execute/build-logs/{contexto}-{ISO}.log`. El log permite:

- Recuperación tras un timeout (no se pierde el output).
- Evidencia para post-mortem si el comando falla.
- Trazabilidad cumple `.claude/rules/build-logs.md`.

### R-5 — Atacar la causa de fondo, no sólo el síntoma

Si los builds son lentos por causas resolubles (cache stale,
deps mal configuradas), priorizar resolver eso antes de aceptar
"el build dura 20 min y hay que esperarlo".

**Caso concreto en este proyecto:** el cache PlantUML está al
83% hit rate. Resolver via WP `plantuml-cache-prerender-update`
(sucesor del WP plantuml-cached-effectiveness-audit) reduce el
build de ~20 min a <5 min, eliminando la condición que dispara
el timeout.

## Reglas de invocación de tools (resumen)

| Caso | Patrón |
|---|---|
| Comando ≤30 s | `Bash` foreground normal |
| Comando 30 s – 5 min | `Bash` foreground con `timeout` parameter |
| Comando >5 min | `Bash run_in_background=true` + `Monitor` tail con grep |
| Build muy largo (>30 min) | Background detached + checks periódicos (R-3) |

## Anti-patrones documentados

### AP-1 — `Bash` foreground con `timeout` >5 min

```python
Bash(command="sphinx-build -W ...", timeout=600000)  # ❌ 10 min foreground
```

El parámetro `timeout` evita el kill local pero NO previene el
SSE liveness timeout del transporte.

### AP-2 — Esperar pasivamente "que termine"

```
Usuario: "espera a que termine el build"
Agente: <silencio durante 15 min>     ← el stream cae
```

Reemplazar con: lanzar background + Monitor + comunicar progreso
al usuario cada vez que el monitor emita.

### AP-3 — `sleep` largos

```bash
sleep 600  # ❌ 10 min sin output → SSE timeout
```

El sistema bloquea sleeps largos; usar `Monitor` con `until`
loop en su lugar.

## Documentar como guideline global

Esta recomendación debería propagarse a `.claude/rules/` o
`.thyrox/guidelines/` en un WP de standardize separado, para
que aplique a todos los proyectos que usen este harness, no
solo a IACT-docs.

**Path propuesto:** `.claude/rules/long-running-commands.md` o
similar. Crear como WP sucesor de standardize.

## Successor WPs

1. `plantuml-cache-prerender-update` — eliminar la causa de
   builds lentos (M-4, ya registrado en WP3).
2. `long-running-commands-guideline` — propagar R-1..R-5 a
   `.claude/rules/` como guideline global.
