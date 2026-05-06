```yml
created_at: 2026-05-06 21:12:00
project: IACT-docs
work_package: 2026-05-06-20-11-32-rbac-bootstrap-data-migration-adr
phase: Phase 11 — TRACK/EVALUATE (lessons learned)
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Lessons Learned — RBAC Bootstrap Data Migration + ADR

## Contexto

WP de aplicación de Recommendation A.1 + A.2 derivadas del WP-5 (research). Output: actualización de `implementacion.rst` §9.5 + ADR-BACK-007 nuevo.

## Lecciones de proceso

### LP-01 — Aplicar recomendaciones inmediatamente después del research

**Observación:** WP-5 entregó la recomendación A el 2026-05-06 19:50. WP-6 la ejecutó 21 minutos después (20:11). Esa proximidad temporal mantuvo el contexto fresco — no hubo costo de re-cargar el research.

**Aplicación:** Cuando un research WP entrega recomendaciones rentables, abrir el WP de aplicación en la misma sesión.

### LP-02 — ADR con quotes verbatim del research preserva auditabilidad

**Observación:** ADR-BACK-007 cita verbatim 5+ sources oficiales con URL completa. Cualquier lector futuro puede verificar las afirmaciones sin depender de la memoria del autor.

**Aplicación:** Todos los ADRs del proyecto deben citar verbatim las sources que sustentan la decisión. Codificado como convención en patterns P-02 (standardize/).

### LP-03 — Strict build expone errores RST que tests no cubren

**Observación:** Build B-3 falló con 4 warnings RST (transition final, bold multilínea, document begin transition). Sin strict build (`-W`) estos errors hubieran pasado a producción de docs.

**Aplicación:** R-2.0 + strict build en CI son no-negociables para docs RST. Confirmar que cualquier nuevo artefacto en `source/` se ejecuta bajo el mismo régimen.

### LP-04 — R-2.0 cumplido en práctica reduce ruido de UI

**Observación:** WP-6 lanzó 2 builds via `Bash run_in_background=true` + `until` loop (no Monitor). Cero task entries persistentes generadas.

**Aplicación:** Patrón confirmado y documentado en R-2.0. Ya está aplicándose en WP-6 y WP-7 sin esfuerzo adicional.

## Lecciones de contenido

### LC-01 — Bootstrap data migration es un patrón reusable

**Observación:** El patrón `RunPython` con `apps.get_model()` + `get_or_create` aplica a cualquier seed data Django (no solo RBAC). Ej: catálogos de productos, configuración inicial, lookup tables.

**Aplicación:** Patrón formalizado como P-03 en `standardize/rbac-bootstrap-adr-patterns.md`. Reusable en futuros WPs que toquen Django apps con seed data.

### LC-02 — ADR es complemento, no sustituto, del research

**Observación:** El ADR sintetiza la decisión y cita el research. NO duplica el research en el ADR — el research vive en su WP propio. Esto evita drift (si research cambia, ADR debe actualizarse explícitamente).

**Aplicación:** ADRs siempre llevan referencia explícita al WP de research que los respalda. Como hecho en ADR-BACK-007 §7 "Trazabilidad" → "Research soporte: WP 2026-05-06-19-27-21..."

### LC-03 — Documentación de "convenience wrapper" debe ser explícita

**Observación:** El management command `manage.py initialize_permissions` se preserva como conveniencia, **NO** como fuente. Esta distinción (fuente canónica vs wrapper) requiere texto explícito o se pierde — los desarrolladores asumen que ambos son equivalentes.

**Aplicación:** En `implementacion.rst` §9.5.2 se escribió "**NO es la fuente canónica**" en negrita. Esta práctica de marcar trade-offs explícitamente debe replicarse en docs de wrappers/alternativas.

## Lecciones de timing

### LT-01 — WPs de aplicación con scope acotado cierran rápido

**Observación:** WP-6 ejecutó B-1 (update §9.5) + B-2 (crear ADR) + 2 builds + 2 fix RST + commit en ~25 minutos. Scope acotado = ejecución rápida.

**Aplicación:** Mantener WPs de aplicación con scope ≤2 batches cuando sea posible. WPs grandes deben dividirse en sucesores antes de empezar.

### LT-02 — RST de ADR puede romper build con bold multilínea

**Observación:** Bold `**...**` que cruza líneas en RST genera warning "Inline strong start-string without end-string". Aprendido en build B-3 retry.

**Aplicación:** Mantener `**bold**` en una sola línea o reformatear como `**header**: prose` si es largo. Ya aplicado en ADR-BACK-007 §3.1.b.

## Riesgos identificados (no realizados)

- **R-01:** ADR contradicción con ADR-BACK-001/005/006 → **Verificado**: complementan, no contradicen. ADR-BACK-007 §0 "Relacionados (vigentes)" lo lista.
- **R-02:** Cross-references rotas en `:doc:` → **Mitigado** por strict build.
- **R-03:** Refactor sugerido en A.3/A.4 sin owner → **Aceptado** como TD-RBAC-01/02 con criterios de cierre.

## Métricas

- Archivos modificados: 2 (`implementacion.rst`, `index.rst` backend).
- Archivos creados: 1 (`adr-back-007-rbac-custom-vs-auth-group.rst`).
- Builds ejecutados: 2 (1 falló por warnings RST, retry pasó).
- Tiempo wall-clock: ~25 minutos (bootstrap → commit).
- Cross-references nuevas: 6 (`:doc:` desde ADR-BACK-007 a otros ADRs/CNST/docs).
- Quotes verbatim de sources oficiales en ADR: 5+.

## Refs

- WP: `2026-05-06-20-11-32-rbac-bootstrap-data-migration-adr`.
- WP predecesor (research): `2026-05-06-19-27-21-agr-django-permission-groups-research`.
- ADR creado: `source/backend/adr-back-007-rbac-custom-vs-auth-group.rst`.
- Doc actualizado: `source/arquitectura-tecnica/rbac/modelo-rbac-iact/implementacion.rst` §9.5.
- Patterns extraidos: `standardize/rbac-bootstrap-adr-patterns.md` (P-01..P-05).
