```yml
project: IACT-docs
work_package: 2026-05-07-23-30-26-use-case-view-users-alignment
created_at: 2026-05-07 23:30:26
closed_at: 2026-05-08 00:35:00
current_phase: Phase 11 — TRACK
status: Cerrado (TR-02 build diferido al final de la cola)
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeno (3 archivos a crear + 1 toctree update + verifs)
target: Alinear `source/arquitectura-tecnica/use-case-view/users/` con `source/requisitos/casos-uso/users/` — completar los 3 UCs Reservado faltantes (uc-usr-05, uc-usr-06, uc-usr-07) en use-case-view siguiendo el mismo patron que en casos-uso/users/index.rst (toctree separado para Reservados con stubs warning + cross-refs).
predecessor_wp: 2026-05-07-23-15-00-endpoint-sod-rules-rename (cerrado)
trigger: directiva del ejecutor "lo que se tiene en source/requisitos/casos-uso/ se debe de tener en source/arquitectura-tecnica/use-case-view/*"
```

# WP — use-case-view users alignment

## Trigger

El ejecutor pidio verificar paridad estructural entre
`source/requisitos/casos-uso/` y
`source/arquitectura-tecnica/use-case-view/`. La auditoria
encontro que **12 de 13 clusters tienen paridad perfecta**;
solo `users` esta desalineado.

## Hallazgo del audit estructural

| Cluster | use-case-view | casos-uso | Diff |
|---|---|---|---|
| access | 7 | 7 | OK |
| admin | 5 | 5 | OK |
| alerts | 5 | 5 | OK |
| audit | 4 | 4 | OK |
| auth | 5 | 5 | OK |
| caller | 5 | 5 | OK |
| logs | 7 | 7 | OK |
| operator | 10 | 10 | OK |
| permissions | 10 | 10 | OK |
| pipeline | 4 | 4 | OK |
| reports | 16 | 16 | OK |
| supervision | 3 | 3 | OK |
| **users** | **4** | **7** | **DIFF=3** |

Total: use-case-view=85, casos-uso=88 (delta = 3 UCs).

## UCs faltantes en use-case-view

Los 3 UCs faltantes estan en estado **Reservado** en
casos-uso (planificados sin spec completa):

- **UC_USR_05** — Bloquear Usuario (RESERVADO).
  Referenciado en uc-auth-03, uc-auth-04, uc-auth-05.
- **UC_USR_06** — Desbloquear Usuario (RESERVADO).
  Counterpart de UC_USR_05.
- **UC_USR_07** — Editar Perfil Propio (RESERVADO).
  Referenciado en uc-usr-02.

## Decision arquitectonica (a confirmar en Phase 5)

El patron observado en `casos-uso/users/index.rst` separa
explicitamente los UCs Reservado en su propio toctree con
caption "UCs Reservados (planificados, sin spec completa)".

**Approach propuesto** para use-case-view/users/:

1. Crear 3 archivos placeholder
   `use-case-view/users/uc-usr-{05,06,07}-{slug}.rst` con
   metadata `:estado: Reservado`, warning explicito, y
   cross-ref al stub en casos-uso. Sin diagrama plantuml
   (no hay spec para diagramar).
2. Actualizar `use-case-view/users/index.rst`:
   - Agregar seccion "UCs Reservados" en la tabla.
   - Agregar segundo toctree con los 3 placeholders.
3. Validacion: build clean serial sin warnings.

## Output esperado del WP

**Phase 1 DISCOVER:** este analisis (commiteado).

**Phase 5 STRATEGY:** confirmar approach (placeholders +
seccion index), o descartarlo (ej: si la decision es no
exponer Reservados en use-case-view).

**Phase 8 PLAN EXECUTION:** task-plan con 4 tareas atomicas:

- T-001..T-003: crear 1 placeholder por UC Reservado.
- T-004: actualizar use-case-view/users/index.rst.

**Phase 11 TRACK:** build clean serial + cierre.

## Restricciones

- NO crear diagramas plantuml en los placeholders (los UCs
  son Reservado, no hay spec para representar).
- Mantener metadata `:estado: Reservado` y `:version: 0.1.0`
  consistente con casos-uso.
- Cross-refs `:doc:` a los stubs en casos-uso obligatorios.
- Strict build (`-W -j 1`) tras los cambios.

## Stopping points

- **SP-01** (humano): aprobar approach (placeholders vs
  excluir vs spec completa) antes de Phase 7/8.
- **SP-02:** strict build EXIT=0.
- **SP-03** (humano): aprobar cierre.

## Out-of-scope

- Promover los 3 Reservados a Borrador/Vigente — requiere
  ADR formal y spec completa, no aplica a este WP.
- Verificar paridad de contenido detallado UC-por-UC entre
  use-case-view y casos-uso (alcance distinto: este WP solo
  cubre paridad estructural).

## Hipotesis iniciales

1. 3 archivos a crear (placeholder Reservado).
2. 1 archivo a modificar (use-case-view/users/index.rst).
3. 0 cross-refs rotos esperados.
4. Esfuerzo: 30-60 min.
