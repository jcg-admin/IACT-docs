```yml
type: Convención de Proyecto
category: Operación del agente — comandos de larga duración
version: 1.0.0
created_at: 2026-05-06 00:42:00
updated_at: 2026-05-06 00:42:00
applies_to: IACT-docs v1.0.0+
origin_wp: 2026-05-06-00-31-12-api-socket-error-investigation
```

# Long-running commands — patrones de invocación

> Cargado automáticamente. Aplica a TODA invocación de comandos
> shell estimados >5 minutos de duración.

## Por qué existe esta regla

El cliente Claude Code se comunica con el backend Anthropic vía
**SSE (Server-Sent Events)** con liveness timeout (~5 min en
sesiones normales). Cuando un `tool_exec` foreground se ejecuta
sin producir mensajes durante esa ventana, el stream cae con:

```
API Error: The socket connection was closed unexpectedly.
```

Wrapper user-facing del evento interno `cli_sse_liveness_timeout`.

Causa raíz documentada en
`.thyrox/context/work/2026-05-06-00-31-12-api-socket-error-investigation/`.

## Reglas operacionales

### R-1 — Comandos >5 min siempre en background

Cualquier comando con duración estimada >5 minutos (build
completo, tests E2E, prerender masivo, batch generation) se lanza
detached. **NUNCA** esperar foreground.

```bash
# CORRECTO — detached con disown
nohup bash -c "long_command ..." > "$LOG" 2>&1 &
disown $!

# CORRECTO — Bash tool con run_in_background=true
Bash(command="long_command ...", run_in_background=true)

# INCORRECTO — foreground >5 min, dispara SSE timeout
sphinx-build -W -j auto -b html source build/html
```

### R-2 — Monitor con grep line-buffered para outcome

Para comandos en background con outcome conocido (success/failure
markers), usar `Monitor` con `tail -f LOG | grep --line-buffered
"PATTERN"`. Cada línea emitida es un evento que mantiene el
stream SSE vivo.

```python
Monitor(
  command='tail -f $LOG | grep -E --line-buffered "^EXIT=|build succeeded|FAIL|Error"',
  description="strict build outcome",
  timeout_ms=1800000  # 30 min, sobrevive el comando
)
```

**Cobertura del filtro**: incluir TODOS los estados terminales
(success, failure, error). Un filtro que sólo matchea success
deja al monitor silencioso ante un crash → indistinguible de
"sigue corriendo".

### R-3 — Probes periódicos cuando no hay output natural

Si la operación no tiene markers para grep (p.ej., proceso
silencioso con outcome sólo al final), emitir tool_uses cortos
cada 3-4 min:

```bash
ls -la <path>      # 0.1s, suficiente para mantener SSE vivo
git status --short
```

### R-4 — Persistir logs en el WP activo

Logs siempre redirigidos a archivo dentro de
`{wp}/execute/build-logs/{contexto}-{ISO}.log`. Cumple
`.claude/rules/build-logs.md` y permite recovery tras timeouts.

```bash
WP=.thyrox/context/work/{wp-activo}
ISO=$(date -u +%Y-%m-%dT%H-%M-%S)
LOG="$WP/execute/build-logs/{contexto}-$ISO.log"
mkdir -p "$(dirname "$LOG")"
nohup bash -c "long_command ..." > "$LOG" 2>&1 &
```

### R-5 — Atacar la causa de fondo, no sólo el síntoma

Si los builds son lentos por causas resolubles (cache stale,
deps mal configuradas), priorizar resolverlo antes de aceptar
"el build dura 20 min y hay que esperarlo".

**Ejemplo en este proyecto:** el cache PlantUML al 83% provocaba
builds de ~20 min. WP `plantuml-cache-prerender-update` lleva el
cache a ~100%, reduciendo el build a <5 min y eliminando la
condición que dispara el timeout.

## Tabla de decisión

| Duración estimada | Patrón |
|---|---|
| ≤30 s | `Bash` foreground normal |
| 30 s – 5 min | `Bash` foreground con `timeout_ms` |
| 5 min – 30 min | `Bash run_in_background=true` + `Monitor` (R-2) |
| >30 min | Background detached + `Monitor` con timeout extendido + checks periódicos (R-3) |

## Anti-patrones prohibidos

### AP-1 — Foreground con timeout >5 min

```python
Bash(command="sphinx-build -W ...", timeout=600000)  # ❌ 10 min foreground
```

El parámetro `timeout` evita el kill local pero **no** previene
el SSE liveness timeout del transporte. El tool_exec puede
completar localmente pero la conexión al servidor ya cayó.

### AP-2 — Esperar pasivamente "que termine"

```
Usuario: "espera a que termine el build"
Agente: <silencio durante 15 min>     ← el stream cae
```

Reemplazar con: lanzar background + Monitor + comunicar progreso
al usuario cuando el monitor emita.

### AP-3 — `sleep` largos

```bash
sleep 600  # ❌ 10 min sin output → SSE timeout
```

El harness bloquea sleeps largos. Para esperar una condición,
usar `Monitor` con `until` loop o polling con intervalos cortos.

### AP-4 — `tail -f` sin límite ni filtro

```python
Monitor(command="tail -f /var/log/app.log", ...)  # ❌
```

Sin filtro:
- Genera demasiados eventos → harness los suprime.
- Sin estado terminal claro → ambiguo si crashea.

Siempre incluir `grep --line-buffered "PATRÓN_ESTADO_TERMINAL"`.

### AP-5 — `tail -f` sin `--line-buffered` en grep

```bash
tail -f log | grep "ERROR"  # ❌ buffering retrasa eventos 60+ s
```

El buffer de pipe acumula líneas hasta llenarse. Para flujo
inmediato:

```bash
tail -f log | grep --line-buffered "ERROR"
```

## Relación con otras reglas

- **`build-logs.md`**: define dónde van los logs (R-4 invoca
  esa regla). Compatible y complementaria.
- **`thyrox-invariants.md`**: I-013 sobre context pruning entre
  stages. Si un comando largo cruza un cierre de stage, marcar
  como "pendiente:re-verificar".
- **`commit-conventions.md`**: Tim Pope; aplicable a commits que
  registren ejecución de comandos largos.

## Referencias

- WP de origen: `2026-05-06-00-31-12-api-socket-error-investigation/`.
  - `analyze/socket-error-root-cause.md` — evidencia textual del
    error y mecanismo.
  - `track/recommendations.md` — origen de R-1..R-5 y AP-1..AP-3.
- Logs evidencia: `/tmp/claude-code-*.diag.log`
  (`cli_sse_liveness_timeout`, `cli_sse_reconnect_attempt`).
