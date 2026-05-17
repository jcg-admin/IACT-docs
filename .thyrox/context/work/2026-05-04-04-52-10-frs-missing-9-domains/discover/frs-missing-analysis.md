```yml
created_at: 2026-05-04 04:52:10
project: IACT-docs
work_package: 2026-05-04-04-52-10-frs-missing-9-domains
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# DISCOVER — FRs Faltantes (9 dominios sin ningún FR)

## Problema

Los 80 UCs del sistema tienen especificaciones completas de 12 partes en
`source/requisitos/casos-uso/`. Sin embargo, los requisitos funcionales
derivados (`source/requisitos/requisitos-funcionales/`) solo existen para
3 dominios: `auth`, `users`, `access`.

Los 9 dominios restantes NO tienen ningún FR derivado.

## Hallazgos (PROVEN)

```bash
find source/requisitos/requisitos-funcionales -mindepth 1 -maxdepth 1 -type d
→ access/
→ auth/
→ users/

find source/requisitos/casos-uso -mindepth 1 -maxdepth 1 -type d
→ access/ (7 UCs: acc-01..acc-09)
→ alerts/ (5 UCs: alr-01..alr-05)
→ audit/ (4 UCs: aud-01..aud-04)
→ auth/ (5 UCs: auth-01..auth-05)
→ caller/ (5 UCs: cli-01..cli-05)
→ logs/ (7 UCs: log-01..log-07)
→ operator/ (10 UCs: opr-01..opr-10)
→ permissions/ (10 UCs: perm-01..perm-10)
→ pipeline/ (4 UCs: pip-01..pip-04)
→ reports/ (17 UCs: rpt-01..rpt-17 + inc-rpt-01)
→ supervision/ (3 UCs: sup-01..sup-03)
→ users/ (4 UCs: usr-01..usr-04)
```

### Dominios faltantes

| Dominio | UCs | FRs existentes |
|---------|-----|----------------|
| alerts | 5 | 0 |
| audit | 4 | 0 |
| caller | 5 | 0 |
| logs | 7 | 0 |
| operator | 10 | 0 |
| permissions | 10 | 0 |
| pipeline | 4 | 0 |
| reports | 18 | 0 |
| supervision | 3 | 0 |

**Total UCs sin FRs derivados: 66 de 80**

### FRs existentes (referencia)

- `auth`: FR-001 (5 FRs) + FR-002 (3) + FR-003 (4) + FR-004 (4) + FR-005 (3) = 19 FRs
- `users`: FR-006 (5) + FR-007 (4) + FR-008 (4) + FR-009 (4) = 17 FRs
- `access`: FR-010 (4) + FR-011 (3) = 7 FRs
- **Total existente: 43 FRs para 11 UCs**

## Decisiones tomadas

### D-001: Alcance del trabajo

**El trabajo de este WP es derivar FRs para los 9 dominios faltantes.**

Cada UC tiene un spec completa de 12 partes. Los FRs se derivan de:
- `flujo-principal.rst` (pasos del flujo normal)
- `criterios-aceptacion.rst` (escenarios BDD)
- `datos-involucrados.rst` (entidades y reglas)

### D-002: Estrategia de derivación

Seguir el protocolo del ADR `adr-edicion-fr-estrategia-reescritura.md`:
1. Leer el UC (flujo-principal + criterios-aceptacion)
2. Determinar cuántos FRs se derivan (tipicamente 3-5 por UC)
3. Usar el template FR estándar
4. Verificar resultado antes de commitear

### D-003: Prioridad de dominios

Orden sugerido por criticidad del sistema:
1. `permissions` (10 UCs) — RBAC core
2. `operator` (10 UCs) — operación diaria
3. `reports` (18 UCs) — alto volumen
4. `alerts` (5 UCs) — monitoring
5. `audit` (4 UCs) — compliance
6. `logs` (7 UCs) — observabilidad
7. `caller` (5 UCs) — IVR
8. `pipeline` (4 UCs) — ETL
9. `supervision` (3 UCs) — supervisión

### D-004: Nomenclatura de FRs

Continuando la numeración existente:
- `auth` usa FR-001..005
- `users` usa FR-006..009
- `access` usa FR-010..011
- `permissions` → FR-012..021 (10 UCs × ~4 FRs = ~40 FRs)
- `operator` → FR-022..031
- etc.

Alternativa: usar código del dominio (FR-PRM-01.01, FR-OPR-02.03, etc.)
→ **Decisión: usar el patrón existente `fr-{NNN}-{NN}-{desc}.rst`**
→ numeración continua desde FR-012

### D-005: Volumen estimado

66 UCs × promedio 4 FRs = ~264 FRs nuevos
Este WP es el más grande — se trabajará por dominio en batches.
