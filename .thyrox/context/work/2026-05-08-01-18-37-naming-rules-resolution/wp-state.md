```yml
project: IACT-docs
work_package: 2026-05-08-01-18-37-naming-rules-resolution
created_at: 2026-05-08 01:18:37
closed_at: 2026-05-08 02:00:00
current_phase: Phase 11 — TRACK
status: Cerrado (4 decisiones aplicadas en loop)
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeno-mediano (4 decisiones normativas + 4-5 archivos modificados)
target: Resolver las 4 decisiones normativas pendientes del WP `clean-code-naming-audit`. (D1) Alinear `backend/conventions.rst` con CLEAN_CODE §6.2 — Opcion A (no es WP separado, pertenece aqui por ser cambio acotado). (D4) Excepcion formal RBAC en STD-010. (D2) Scope STD-010 con clarificacion de exempt para metodologia + sistemas externos + index.rst por contenido. (D3) Verificar codigo de `ResumenSaludBuilder` y decidir caso puntual. Ejecucion en loop, no audit.
predecessor_wp: 2026-05-08-01-07-10-clean-code-naming-audit (cerrado, audit-only)
trigger: ejecutor proporciono respuestas detalladas a las 4 decisiones del audit y solicito ejecucion en loop documentando todos los hallazgos
```

# WP — naming-rules-resolution (4 decisiones)

## Trigger

Tras cerrar el WP `clean-code-naming-audit`, el ejecutor
respondio las 4 decisiones pendientes con razonamiento
detallado y orden recomendado:

1. D1 (conflicto `backend/conventions.rst`): **Opcion A** —
   alinear.
2. D4 (RBAC en prosa): excepcion **formal** en STD-010.
3. D2 (scope STD-010): metodologia exenta; index.rst por
   contenido; externos exentos con nota formal.
4. D3 (`ResumenSaludBuilder`): verificar codigo antes de
   decidir.

Orden de resolucion documentado por el ejecutor:
**D1 → D4 → D2 → D3** (D1 y D4 desbloquean alcance real,
D2 clarifica scope, D3 es caso puntual).

## Naturaleza del WP

EXECUTE en loop. Cada decision es una secuencia de:

1. Hallazgo (lo que se observa hoy).
2. Decision aplicada.
3. Cambio ejecutado.
4. Validacion.

Todo se documenta en `discover/decisions-log.md` (un solo
artefacto que registra el flujo de las 4 decisiones).

## Output esperado

**EXECUTE:**

- D1: actualizar `source/backend/conventions.rst` para
  alinear con CLEAN_CODE §6.2 + agregar referencia
  autoritativa.
- D4: agregar seccion "Excepciones explicitas" a STD-010
  con la regla RBAC.
- D2: agregar seccion al ambito de STD-010 con
  clarificaciones (metodologia, sistemas externos,
  index.rst por contenido).
- D3: leer codigo (o spec si solo hay docs) de
  `ResumenSaludBuilder`, decidir y aplicar (preservar o
  renombrar).

**TRACK:**

- changelog.md.
- decisions-log.md (artefacto principal del WP).
- wp-state.md status=Cerrado.

## Restricciones

- D1 y D2/D4 son **modificaciones a documentos normativos**
  — bumpear `:version:` segun SemVer (probablemente MINOR
  por ampliacion sin contradicciones).
- D3 NO modifica codigo Python (no existe en este repo);
  solo modifica docs si el rename es justificado.
- Todos los cambios son consistentes con WPs previos
  cerrados.

## Stopping points

- **SP-01 (humano):** revisar D1+D4 actualizados antes de
  D2.
- **SP-02 (humano):** aprobar cierre del WP.

## Refs

- WP `clean-code-naming-audit` (cerrado, audit-only).
- CLEAN_CODE_NAMING_PRINCIPLES v1.0.0.
- STD-010 v1.0.0 (sera bumpeado por D2+D4).
- backend/conventions.rst (sera actualizado por D1).
