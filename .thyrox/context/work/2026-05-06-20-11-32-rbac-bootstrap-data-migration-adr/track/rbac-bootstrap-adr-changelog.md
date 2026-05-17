```yml
created_at: 2026-05-06 20:15:00
project: IACT-docs
work_package: 2026-05-06-20-11-32-rbac-bootstrap-data-migration-adr
phase: Phase 10 — EXECUTE
author: NestorMonroy
status: En progreso
version: 1.0.0
```

# WP Changelog — RBAC Bootstrap Data Migration + ADR

## Trigger

Continuar con pendientes de WP-5
(``2026-05-06-19-27-21-agr-django-permission-groups-research``)
recomendaciones A.1 y A.2.

## B-1 — A.1 Update implementacion.rst §9.5

`source/arquitectura-tecnica/rbac/modelo-rbac-iact/
implementacion.rst` §9.5 reescrita:

- Título "Management Command" → "Bootstrap del catálogo RBAC"
  (refleja el alcance real, no solo el comando).
- Patrón canónico (§9.5.1): data migration con ``RunPython``
  documentada con ejemplo Python idiomatic Django.
- Cross-link a `ADR-BACK-007` y a docs.djangoproject.com
  (Migration Operations + provide initial data).
- Beneficios listados (idempotencia, ejecución automática con
  migrate, ``apps.get_model()`` para versión histórica).
- Management command (§9.5.2) preservado como **convenience
  wrapper** explícitamente "**NO es la fuente canónica**" —
  delega en las funciones de la data migration.

## B-2 — A.2 ADR-BACK-007 (NUEVO)

Nuevo archivo: `source/backend/adr-back-007-rbac-custom-vs-auth-group.rst`.

Estructura siguiendo el template de ADRs backend del proyecto
(adr-back-005 como referencia):

- Estado y metadata (Aprobada).
- §1 Contexto y Problema — pregunta arquitectónica.
- §2 Factores de Decisión.
- §3 Decisión:
  - §3.1 Por qué NO ``auth.Group`` (3 razones con quotes
    verbatim de Django Forum y ticket #29748).
  - §3.2 Bootstrap canónico via data migration (con quotes de
    docs.djangoproject.com).
- §4 Consecuencias (positivas, negativas aceptadas, neutrales).
- §5 Alternativas Consideradas:
  - §5.1 Alternativa B (migrar a ``auth.Group``) — descartada
    por costo.
  - §5.2 Alternativa C (wrapper ``OneToOneField``) — TD-RBAC-02
    para evaluación futura.
- §6 Implementación con ejemplo de data migration completo.
- §7 Trazabilidad: relacionados ADR-BACK-001/005/006, CNST-029,
  WP-5 research/raw/Q1..Q8.
- §8 Referencias verbatim a:
  - Docs oficiales Django + DRF.
  - Tickets / discusiones (ticket #29748, Django Forum).
  - Fundamento teórico (paper Purdue SoD).

Agregado al toctree de `source/backend/index.rst`.
Bump `:version:` 1.0.0 → 1.1.0; `:ultimo_cambio:` → 2026-05-06.

## Verificación

- Strict build (`-W`) — pending al cerrar este artefacto.
- Cross-references nuevas:
  - implementacion.rst §9.5 → adr-back-007.
  - adr-back-007 → adr-back-001, adr-back-005, adr-back-006,
    cnst-029, modelo-rbac-iact/index.

## Cumplimiento de R-2.0

WP-6 cumple **R-2.0** estrictamente: build strict lanzado con
`Bash run_in_background=true` + `until` loop, **sin Monitor**.
**Cero task entries persistentes** generadas en la UI.

## Status del WP

- B-1: ✅ implementacion.rst §9.5 actualizado.
- B-2: ✅ ADR-BACK-007 creado + agregado al toctree.
- B-3: ⏳ strict build pending (R-2.0 background).

## Pendientes derivados

- **TD-RBAC-01** (declarado en WP-5): migrar bootstrap real del
  backend a data migration. Owner: equipo backend (no es scope
  IACT-docs).
- **TD-RBAC-02** (NUEVO): re-evaluar Alternativa C (wrapper
  OneToOneField) si el proyecto adopta paquetes que dependen
  de ``auth.Group``. Owner: arquitectura.
