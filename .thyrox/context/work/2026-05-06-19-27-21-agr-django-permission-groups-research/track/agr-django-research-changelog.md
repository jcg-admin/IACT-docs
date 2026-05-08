```yml
created_at: 2026-05-06 19:52:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 11 — TRACK/EVALUATE (research-only WP)
author: NestorMonroy
status: En progreso
version: 1.0.0
```

# WP Changelog — AGR Django Permission Groups Research

## Naturaleza del WP

WP de **investigación pura** (research-only). No modifica
código RST publicado del corpus. Output esperado: análisis
respaldado por documentación oficial Django/DRF + recomendación.

## Trigger

> Ejecutor: "vamos a revisar si lo que tenemos de AGR-NNN es la
> forma correcta... Django y DRF son los frameworks del backend,
> prioridad oficial, búsqueda en inglés, guardar todo en el WP".

## Estrategia ejecutada (Phase 1 DISCOVER)

8 queries en inglés con priorización Tier 1 (sitios oficiales)
> Tier 2 (paquetes establecidos) > Tier 3 (comunidad
verificada).

| Q# | Pregunta | Tier respuesta |
|---|---|---|
| Q1 | Django auth.Group y auth.Permission | Tier 1 (docs.djangoproject.com) |
| Q2 | Bootstrap predefined groups via data migration | Tier 1 |
| Q3 | System groups inmutables (is_system pattern) | Tier 1+2 |
| Q4 | DRF DjangoModelPermissions + auth.Group integration | Tier 1 (django-rest-framework.org) |
| Q5 | Custom Group vs extender auth.Group | Tier 1 (Django Forum) + Tier 2 |
| Q6 | Permission codename naming convention | Tier 1 |
| Q7 | RBAC Separation of Duties patterns | Tier 2 (paquetes) |
| Q8 | django-guardian vs django-rules comparison | Tier 2 |

Cada query guardó hallazgos verbatim + sources verificables
en `research/raw/Q{N}-{slug}.md`.

## Hallazgos clave (Stage 3 ANALYZE — síntesis)

Síntesis completa en `analyze/django-rbac-idiomatic-analysis.md`.

### Veredicto técnico

| Decisión IACT | Django idiomatic | Veredicto |
|---|---|---|
| `Function` custom en lugar de `auth.Permission` | `auth.Permission` con custom codenames | ⚠️ Duplicación parcial |
| `AccessGroup` custom en lugar de `auth.Group` | `auth.Group` + data migration | ⚠️ Duplicación parcial |
| Naming `view_reports`, `export_csv` (snake_case verbo) | snake_case verbo | ✅ Idiomático |
| Bootstrap via `manage.py initialize_permissions` | Data migration `RunPython` | ⚠️ Funciona pero no canónico |
| `is_system=True` para grupos predefinidos | No nativo en Django | ⚠️ Custom razonable |
| `FunctionSeparationRule` para SoD | No nativo en Django | ✅ Necesario custom |
| Códigos AGR-001..012 como natural keys | Solo `name` como natural | ✅ Mejor |

### Recomendación final

**Recomendación A — Mantener custom + fixes idiomáticos:**

1. **A.1** Migrar bootstrap de `manage.py initialize_permissions`
   a data migration con `RunPython` (idiomatic Django; reduce
   setup manual).
2. **A.2** Documentar ADR formal:
   `adr-back-007-rbac-custom-vs-auth-group.md` con justificación
   de por qué AccessGroup custom (referencia ticket #29748).
3. **A.3** Considerar wrapper `OneToOneField` como alternativa
   (no urgente).
4. **A.4** Verificar que el backend tiene custom permission
   backend (`get_all_permissions()` retornando codes de
   `Function` vía `AccessGroup`).

Recomendaciones B (migrar a `auth.Group`) y C (wrapper hibrido)
se documentaron como alternativas pero requieren refactor
mayor que no se justifica dado el estado actual del corpus.

## Output del WP

```
2026-05-06-19-27-21-agr-django-permission-groups-research/
├── wp-state.md                                              ✅
├── research/raw/
│   ├── Q1-django-auth-group-permission-model.md             ✅
│   ├── Q2-django-data-migration-bootstrap-groups.md         ✅
│   ├── Q3-django-immutable-system-groups.md                 ✅
│   ├── Q4-drf-permissions-groups-authorization.md           ✅
│   ├── Q5-custom-group-vs-extend-auth-group.md              ✅
│   ├── Q6-permission-codename-naming.md                     ✅
│   ├── Q7-django-rbac-separation-of-duties.md               ✅
│   └── Q8-django-guardian-rules-comparison.md               ✅
├── analyze/
│   └── django-rbac-idiomatic-analysis.md                    ✅
└── track/
    └── agr-django-research-changelog.md                     ✅ (este)
```

## Pendientes derivados (próximos WPs sugeridos)

1. **Backend ADR**: crear `adr-back-007-rbac-custom-vs-auth-group.md`
   formalizando la decisión A en `source/backend/`.
2. **TD-RBAC-01** (deuda técnica): migrar bootstrap RBAC de
   management command a data migration. Owner: equipo backend.
3. **STD-014** (opcional): documentar la convención IACT con
   referencia a Django idiomatic patterns.

## Notas sobre R-2.0 (aplicado en este WP)

Este WP **no usó Monitor en absoluto** — solo `WebSearch` directos
y archivos `Write`. Cero task entries persistentes en la UI,
alineado con la nueva regla R-2.0.
