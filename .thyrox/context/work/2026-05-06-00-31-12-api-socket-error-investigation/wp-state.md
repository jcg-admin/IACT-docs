```yml
project: IACT-docs
work_package: 2026-05-06-00-31-12-api-socket-error-investigation
created_at: 2026-05-06 00:31:12
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-elicitation
target: Investigar por que ocurrio el error "API Error: The socket connection was closed unexpectedly. For more information, pass `verbose: true` in the second argument to fetch()" durante la sesion del WP use-case-view-uml07-standalone-pass. Identificar causa raiz, mecanismo de fallo y mitigaciones.
trigger: Error reportado por el ejecutor durante el cierre del WP predecesor.
related_wps:
  - 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass (sesion donde ocurrio)
  - 2026-05-06-00-11-02-plantuml-cached-effectiveness-audit (causa probable: build de 15-20 min)
```

# WP — API Socket Error Investigation

## Trigger

Durante la sesion del WP `use-case-view-uml07-standalone-pass`,
mientras se ejecutaba el strict build final de Sphinx, el ejecutor
reporto el siguiente error:

```
API Error: The socket connection was closed unexpectedly.
For more information, pass `verbose: true` in the second
argument to fetch()
```

El error interrumpio la sesion mid-build. Tras reanudar, el build
se relanzo y completo exitosamente (EXIT=0, 0 warnings).

## Contexto temporal

- 22:49:28 UTC: build strict relanzado tras instalar deps.
- ~23:05 UTC: build llegaba al 53% writing output (slow).
- algun momento entre 23:05 y la reanudacion: socket close error.
- 23:37:04 UTC: build relanzado en background.
- ~00:00 UTC: build succeeded (~25 min wall-clock total).

## Hipotesis preliminares

### H-1 — Timeout de keepalive del transporte HTTP/WS

El cliente Claude Code mantiene una conexion persistente con la
API. Si el transporte (HTTP/2 streaming, WebSocket o similar)
tiene un keepalive timeout y el lado del agente no envia frames
durante ese intervalo, la conexion se cierra.

Sintoma compatible: error `socket connection closed unexpectedly`
sin error de aplicacion explicito.

### H-2 — Build de larga duracion sin tool_use intermedio

El build sphinx corrio en foreground por minutos sin emitir
tool_use ni texto. La capa de transporte puede interpretarlo como
"conexion ociosa" y cerrarla. El servidor podria tener un timeout
de respuesta de N minutos, despues del cual cancela la request.

### H-3 — Reverse proxy / load balancer con idle timeout

Entre el cliente Claude Code y el backend de Anthropic puede haber
un load balancer o proxy con timeout configurado (ej. 60s, 5 min,
10 min). Si el agente no produce output durante ese periodo, el
proxy cierra la conexion.

### H-4 — Build a 100% CPU bloquea event loop del cliente

Si Java + PlantUML estaban consumiendo todos los cores con `-j auto`,
el proceso Claude Code podria estar starved y no responder a
keepalives, llevando al servidor a cerrar la conexion.

### H-5 — Memoria / OOM partial

Sphinx `-j auto` con muchos workers puede consumir mucha RAM. Si
hubo OOM partial, kernel pudo matar un sub-proceso del cliente,
rompiendo la conexion.

## Output esperado

1. `discover/api-socket-error-investigation-analysis.md` —
   contexto, hipotesis, evidencia disponible.
2. (opcional Phase 3) `analyze/socket-error-root-cause.md` — analisis
   con datos del transporte, logs del cliente Claude Code, syslog
   del host.
3. `track/recommendations.md` — mitigaciones propuestas:
   - Operaciones de larga duracion siempre en background con
     monitor.
   - Keep-alive con tool_use periodico (e.g. progress check cada N
     minutos).
   - Configuracion de timeout del cliente.
4. `track/changelog.md` — cierre formal.

## Restricciones del scope

### In-scope

- Investigar la causa del error socket en el contexto de THIS sesion.
- Documentar mitigaciones aplicables a futuros WPs con builds
  largos.

### Out-of-scope

- Modificar el codigo de Claude Code (no es nuestro repo).
- Reportar bugs upstream a Anthropic (decision del ejecutor, no
  automatica).
- Investigar otros tipos de errores de red.

## Metodo de investigacion

### Datos disponibles

1. **Timestamp del build interrumpido**: 22:49:28 UTC log file.
2. **Tiempo wall-clock del build exitoso (post-recovery)**: ~25 min.
3. **Mensaje exacto del error** del transcript (ya capturado arriba).
4. **Logs del cliente Claude Code**: si existen en
   `/tmp/claude-*` o `~/.claude/logs/`.
5. **Logs del kernel host**: `dmesg`, `journalctl` (si accesible).

### Datos NO disponibles

- Logs del backend de Anthropic (cerrado).
- Configuracion exacta de timeouts del proxy/LB intermedio.
- Topologia de red del cliente (firecracker init?).

### Heuristica de descarte

| Hipotesis | Como descartar |
|---|---|
| H-1 keepalive | Buscar configuracion de timeout en cliente Claude Code |
| H-2 idle build | Confirmar correlacion temporal: build de N min == socket close |
| H-3 proxy idle | Buscar evidencia de proxy en headers o trace |
| H-4 CPU starvation | Verificar carga durante build (`top`, `htop` historicos si hay) |
| H-5 OOM partial | Buscar `Out of memory` en `dmesg`/`journalctl` |

## Stopping points

- **SP-01** (gate humano): aprobar bootstrap + analysis. Decidir si
  Phase 3 ANALYZE profundo es necesario o early-close basta.
- **SP-02** (gate humano): aprobar recomendaciones (track/).

## Anatomia esperada

```
2026-05-06-00-31-12-api-socket-error-investigation/
├── wp-state.md                                       ← este
├── discover/
│   └── api-socket-error-investigation-analysis.md
├── analyze/   (opcional)
│   └── socket-error-root-cause.md
└── track/
    ├── recommendations.md
    └── api-socket-error-investigation-changelog.md
```

## Hipotesis prioritaria

**H-2 (idle build sin tool_use)** es la mas plausible dado:

- El error ocurrio durante un build sphinx que duro >15 min sin
  emitir nada al canal de comunicacion del agente.
- La capa de transporte HTTP entre cliente Claude Code y backend
  Anthropic tipicamente tiene timeouts de 60s-10min.
- El build no es un tool_use estandar; es ejecucion en background
  detached. El cliente esperaba el output sin enviar keepalives.

Esto sugiere que la mitigacion principal es: **NUNCA esperar en
foreground builds >5 min**. Siempre lanzarlos detached + monitor +
checks periodicos con tool_use intermedio.
