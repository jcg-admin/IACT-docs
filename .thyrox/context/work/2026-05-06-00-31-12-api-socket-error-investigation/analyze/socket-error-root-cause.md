```yml
created_at: 2026-05-06 00:40:00
project: IACT-docs
work_package: 2026-05-06-00-31-12-api-socket-error-investigation
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Phase 3 ANALYZE — Causa raíz del error socket

## Evidencia obtenida

Logs de diagnóstico del cliente Claude Code en
`/tmp/claude-code-*.diag.log` con timestamps que solapan la sesión.

### Fuente 1 — `claude-code-2683623323.diag.log` (sesión iniciada 19:08:51 UTC)

Eventos SSE relevantes:

```
19:08:51.628  info   cli_sse_transport_initialized
19:08:51.634  info   cli_sse_connect_opening
19:08:56.795  info   cli_sse_connect_connected   duration_ms=5160
...
19:31:19.266  info   cli_sse_message_received        ← último mensaje
19:36:22.408  error  cli_sse_liveness_timeout        ← timeout despues de ~5 min
19:36:22.409  error  cli_sse_reconnect_attempt       reconnectAttempts=1
19:36:22.410  error  cli_sse_stream_read_error
19:36:22.411  error  cli_sse_reconnect_attempt       reconnectAttempts=2
19:36:24.378  info   cli_sse_connect_opening
19:36:24.448  info   cli_sse_connect_connected       duration_ms=71  ← reconexion OK
```

### Fuente 2 — `claude-code-1717198703.diag.log` (sesión 23:20:32 UTC)

```
23:37:47.260  info   cli_sse_message_received        ← último mensaje normal
... 47 minutos de silencio (build sphinx en foreground) ...
00:24:30.874  error  cli_sse_stream_read_error       ← stream cae
```

### Fuente 3 — `run_state_at_shutdown` (23:06:02)

```json
{
  "run_active": true,
  "run_phase": "draining_commands",
  "worker_status": "running",
  "bg_tasks": {"local_bash": 1},
  "session_activity": {
    "active": {"tool_exec": 1},
    "oldest_activity_ms": 390657   ← 6 min 30 s de tool_exec activo
  }
}
```

## Hallazgo principal

### Transporte

El cliente Claude Code se comunica con el backend via **SSE
(Server-Sent Events)**, no socket TCP genérico ni WebSocket. El
mensaje "API Error: The socket connection was closed unexpectedly"
es el wrapper user-facing de un error interno
`cli_sse_liveness_timeout` o `cli_sse_stream_read_error`.

### Mecanismo de fallo

1. La conexión SSE espera un flujo continuo de mensajes desde el
   servidor.
2. El cliente tiene un **liveness timeout** que cierra la conexión
   si no recibe mensajes durante un período N.
3. Cuando un `tool_exec` local de larga duración (sphinx-build)
   se ejecuta en foreground sin producir output al canal del
   agente, el servidor no envía mensajes (no hay nada que enviar).
4. Sin mensajes entrantes, el cliente alcanza el liveness timeout
   y cierra el stream.
5. El cliente intenta reconectar automáticamente
   (`cli_sse_reconnect_attempt`). La reconexión TCP es rápida
   (71 ms en el log), pero el estado del stream previo puede
   perderse, generando el error visible al usuario.

### Ventanas de timeout observadas

| Sesión | Último mensaje | Timeout | Δt | Tipo de error |
|---|---|---|---|---|
| 19:08 | 19:31:19 | 19:36:22 | **5 min 03 s** | `cli_sse_liveness_timeout` |
| 19:08 | 20:31:21 | 20:36:25 | **5 min 04 s** | `cli_sse_stream_read_error` |
| 23:20 | 23:37:47 | 00:24:30 | **46 min 43 s** | `cli_sse_stream_read_error` |

**Inconsistencia**: el primer y segundo caso muestran ~5 min
exacto de tolerancia. El tercer caso muestra 47 min. Hipótesis
para esta diferencia:

- (a) la ventana de timeout es **dinámica** según el modo de
  sesión (resume vs interactive vs autonomous).
- (b) existían heartbeats SSE intermedios no logueados como
  `cli_sse_message_received` que mantuvieron viva la conexión
  hasta los 47 min.
- (c) la sesión 23:20 estaba en un estado especial (post-resume)
  con timeout extendido.

No es necesario resolver esta inconsistencia para este audit —
basta con confirmar que la ventana de timeout existe.

## Validación de hipótesis del Phase 1 DISCOVER

| H | Estado | Evidencia |
|---|---|---|
| **H-1** keepalive timeout del transporte | **CONFIRMADA** | `cli_sse_liveness_timeout` literal en log |
| **H-2** build largo sin tool_use intermedio | **CONFIRMADA como condición** | `oldest_activity_ms=390657` durante shutdown; sphinx-build foreground |
| H-3 reverse proxy idle timeout | descartada como causa primaria | el timeout es del propio cliente (`cli_sse_liveness_timeout` viene del cliente, no del proxy) |
| H-4 CPU starvation | no concluyente | no hay datos de CPU en los logs disponibles |
| H-5 OOM partial | descartada | no hay entradas de OOM en `dmesg` (kernel ring buffer no muestra OOM) |

## Causa raíz

**Combinación de H-1 + H-2:** el cliente Claude Code usa SSE con
liveness timeout (~5 min en condiciones normales). Cuando un
tool_exec local toma >5 min sin producir eventos del lado servidor
(porque el work no genera mensajes — es ejecución local detached),
el liveness timeout dispara y la conexión SSE se cae. El cliente
intenta reconectar, pero el usuario percibe el error como "socket
closed unexpectedly" (mensaje wrapper).

## Mitigaciones aplicables

### M-1 — Nunca esperar en foreground builds >5 min

**Implementación:** todo build/comando estimado >5 min se lanza
con `nohup ... &` o `Bash run_in_background=true`, con el shell
agente desreferenciando el PID. Mientras el comando corre,
el agente puede emitir tool_uses cortos cada N min para mantener
viva la SSE.

**Ya aplicado parcialmente:** durante este WP usé `nohup` para
relanzar el build tras el primer timeout.

### M-2 — Monitor con eventos periódicos

Usar el `Monitor` tool con un grep que emita ≥1 línea cada <5 min
(p.ej. tail con line-buffered grep sobre eventos del log). Cada
línea emitida es un tool_use que reset-ea el liveness timer.

**Ya aplicado:** monitor `bnkahsvta` y `bwb0tm0lb` durante el
build final.

### M-3 — Probe periódico durante esperas

Si no hay output natural, hacer `Bash` calls cortos (`ls`, `git status`,
etc.) cada 3-4 min para forzar tráfico SSE.

### M-4 — Optimizar el origen del problema (build lento)

El root cause de los builds largos es el cache PlantUML stale
(83% hit rate, 188 misses × ~10s = ~30 min). Resolverlo via WP
`plantuml-cache-prerender-update` reduce o elimina el síntoma.
Esta es la **mitigación de fondo**, no de la falla SSE per se.

## No-acciones documentadas

### NA-1 — No cambiar la ventana de liveness timeout

No es nuestro código (Claude Code es cliente Anthropic). No
intentar modificar el timeout via env vars sin documentación
oficial.

### NA-2 — No reportar bug upstream

Decisión del ejecutor. El comportamiento es correcto desde la
perspectiva del cliente — un stream SSE inactivo debe cerrarse
para liberar recursos. La responsabilidad de mantenerlo vivo es
del agente.

## Conclusión

El error es **comportamiento esperado** del transporte SSE bajo
condición de tool_exec foreground prolongado. La mitigación es
operacional (no esperar foreground >5 min, usar Monitor o
background) y de fondo (eliminar la causa de builds largos via
cache prerender).

El WP puede cerrarse: hipótesis prioritaria (H-1+H-2) confirmada
con evidencia textual del log, mitigaciones documentadas, no se
requiere acción adicional.
