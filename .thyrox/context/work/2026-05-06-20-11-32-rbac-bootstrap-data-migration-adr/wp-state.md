```yml
project: IACT-docs
work_package: 2026-05-06-20-11-32-rbac-bootstrap-data-migration-adr
created_at: 2026-05-06 20:11:32
current_phase: Phase 1 — DISCOVER → EXECUTE
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeño (Stages 1, 10, 11)
target: Aplicar Recomendaciones A.1 + A.2 del WP-5 (research AGR-Django). A.1 = actualizar implementacion.rst para mostrar bootstrap canonico via data migration RunPython (en lugar de management command). A.2 = crear ADR formal adr-back-007-rbac-custom-vs-auth-group.rst justificando la decision de usar AccessGroup custom.
predecessor_wp: 2026-05-06-19-27-21-agr-django-permission-groups-research (cerrado, research-only)
trigger: continuar con pendientes — directiva del ejecutor.
```

# WP — RBAC Bootstrap Data Migration + ADR

## Trigger

WP-5 (research) recomendó dos fixes de bajo costo y alto valor:

- **A.1**: migrar bootstrap de `manage.py initialize_permissions`
  a data migration con `RunPython` — alineamiento idiomatic
  Django (Q2 verbatim).
- **A.2**: documentar ADR formal explicando por qué se usa
  `AccessGroup` custom en lugar de `auth.Group`.

Los items A.3 (wrapper OneToOneField) y A.4 (verificar backend
code) quedan fuera de scope — A.3 no es urgente, A.4 requiere
acceso al repo backend real.

## Plan

### B-1 — A.1 Update implementacion.rst

`source/arquitectura-tecnica/rbac/modelo-rbac-iact/
implementacion.rst` §9.5 actualmente muestra:

```bash
# Inicializar RBAC v5.6.0
python manage.py initialize_permissions

# O paso a paso:
python manage.py initialize_functions # 64 funciones activas (in-scope)
python manage.py initialize_function_groups # 12 grupos
python manage.py initialize_separation_rules # 3 reglas SoD
```

Aplicar:

- Reemplazar el management command como **alternativa secundaria**.
- Documentar **data migration con RunPython** como patrón
  canónico per docs.djangoproject.com.
- Citar verbatim source.
- Mantener el management command como **convenience wrapper**
  para operadores que quieran re-bootstrap manual.

### B-2 — A.2 Crear ADR backend

Nuevo archivo: `source/backend/adr-back-007-rbac-custom-vs-auth-group.rst`.

Estructura ADR (template `tpl-adr` del proyecto):

- Status: Aceptado
- Context: Django provee auth.Group nativo; ¿por qué IACT usa
  AccessGroup custom?
- Decision: Mantener custom, con justificación basada en
  research/raw/Q5 (ticket #29748, OneToOneField wrapper, etc.).
- Consequences: pierde compatibilidad con tooling Django pero
  gana flexibilidad (is_system, audit, custom assignment
  metadata).
- Alternatives considered: B (migrar) y C (wrapper) — explicadas.
- Refs: WP-5 research/raw/Q5 + Q1 + Q2.

### B-3 — Strict build (R-2.0)

Lanzar build con `Bash run_in_background=true` + `until` —
**NO Monitor** per R-2.0 nueva.

## Restricciones

- NO modificar código backend real (es WP de docs).
- NO inventar URLs ni decisiones — todo respaldado por WP-5
  research/raw/.
- Build strict (sphinx -W): obligatorio.
- Cumplir R-2.0 — sin Monitor.

## Riesgos

| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | El template `tpl-adr` puede tener formato específico | Leer un ADR backend existente (adr-back-005 o 006) antes de escribir |
| R-02 | Cross-references rotas (`:doc:` con paths nuevos) | Build strict captura cualquier ref rota |
| R-03 | Conflicto con ADR-back-001 (grupos funcionales sin jerarquía) | Cross-link explícito; ADR-007 complementa, no contradice |

## Stopping points

- **SP-01**: gate humano declarado innecesario.
- **SP-02**: build strict 0 warnings.
