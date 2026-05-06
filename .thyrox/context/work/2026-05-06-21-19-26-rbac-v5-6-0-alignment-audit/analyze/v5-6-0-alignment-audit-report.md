```yml
created_at: 2026-05-06 21:25:00
project: IACT-docs
work_package: 2026-05-06-21-19-26-rbac-v5-6-0-alignment-audit
phase: Phase 3 — ANALYZE (audit)
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Audit de Alineación RBAC v5.6.0 — Resultado

## Trigger

Ejecutor solicitó: "revisar que efectivamente ya esté todo alineado con la última versión del rbac, y sigo teniendo dudas con respecto a cómo se va a implementar o diagramar lo relacionado a los grupos".

## Audit ejecutado

### A. Versiones RBAC residuales

```bash
grep -rnE "RBAC v5\.[2-5]\.[0-9]+" source/ --exclude=v5.2.x|rbac-historia
```

**Resultado:** 0 ocurrencias residuales. ✅

### B. Conteos de funciones obsoletos (74, 73)

```bash
grep -rnE "[^/]7[34] funciones" source/
```

**Resultado:** 0 ocurrencias. ✅

### C. Vocabulario PROHIBIDO (CNST-033) residual

```bash
grep -rnE "admin_sistema|admin_seguridad" source/ --exclude=rbac-historia|cnst-033-vocabulario
```

**Resultado:** 0 ocurrencias. ✅

### D. `operador_etl` (no existe como AGR canónico)

**Resultado:** 1 ocurrencia en contexto histórico (renombrado documentado). ✅

### E. Formato AGR_NN malformado (underscore en lugar de dash)

**Resultado:** 0 ocurrencias. ✅

### F. "12 módulos" residual (debería ser 11 declarados / 9 activos + 2 reservados)

**Resultado:** 0 ocurrencias. ✅

### G. Conteos de funciones fuera de v5.6.0 (≠ 64 / ≠ 77)

**Resultado:** 3 ocurrencias en docs históricos:

- `adr-gob-009:210`: "~75 funciones" — contexto v4.0 legacy. ✅ OK.
- `gestion/evidencia/rbac-historia/modelo-rbac-v4-0-roles-jerarquicos-deprecado.rst:46,127`: "~75 funciones" — doc histórico de evidencia. ✅ OK.

### H. AGR-009 (canónico = `pipeline_admin_group`) usado correctamente

**Bugs detectados (3):**

| # | Archivo | Bug | Fix |
|---|---|---|---|
| H-1 | `casos-uso/permissions/uc-perm-10/requisitos-no-funcionales.rst:51` | "auditor (AGR-009) y daily audit (AGR-008)" — AGR-009 NO es auditor | Reemplazado con "AGR-008 ``auditor_group``" único |
| H-2 | `casos-uso/permissions/uc-perm-07/patrones-diseno.rst:103` | "AGR-008 (daily_audit_group) y AGR-009 (auditor)" — ambos mal asignados | "AGR-007 (``permission_admin_group``) y AGR-008 (``auditor_group``)" |
| H-3 | `casos-uso/permissions/uc-perm-08/flujos-alternos.rst:86` | "AGR-009 auditor / soporte" — AGR-009 es pipeline, no auditor | "AGR-008 (``auditor_group``) o AGR-010 (``system_admin_group``) para soporte" |

**Otros usos de AGR-009 verificados correctos:**

- `br-002-etl-batch-nocturno.rst`: contexto pipeline ETL ✅
- `auth/uc-auth-01/actores-precondiciones.rst`: tabla de mapping correcta ✅
- `metamodelos/mtm-03-metamodelo-rbac.rst`: contexto general ✅

### I. AGR-010 (canónico = `system_admin_group`)

**Resultado:** Todas las ocurrencias en `casos-uso/admin/uc-adm-03/` son correctas (system_admin_group para MOD_Admin). ✅

### J. AGR-011 / AGR-012 marcados como Reservado

**Resultado:** Todas las ocurrencias activas tienen marca de reserva o están en contexto histórico/range. ✅

## Cambios aplicados (B-1: bug fixes)

3 archivos corregidos para alinear con AGR canónico:

- `source/requisitos/casos-uso/permissions/uc-perm-10/requisitos-no-funcionales.rst`
- `source/requisitos/casos-uso/permissions/uc-perm-07/patrones-diseno.rst`
- `source/requisitos/casos-uso/permissions/uc-perm-08/flujos-alternos.rst`

## Cambios aplicados (B-2: clarificar diagramación de grupos)

Nuevo documento que responde a la pregunta del ejecutor sobre
**cómo se implementa/diagrama lo relacionado a grupos**:

`source/arquitectura-tecnica/rbac/modelo-rbac-iact/diagramas/bootstrap-grupos-predefinidos.rst`

Contenido:

1. **Tabla canónica de mapeo AGR-001..012 → AccessGroup** con
   estado v5.6.0 (in-scope vs reservado open-closed).
2. **Diagrama de actividad (PlantUML):** bootstrap automático
   via ``python manage.py migrate`` — muestra Operador → Django
   Migrations Engine → Data Migration → ``RunPython`` →
   creación idempotente de Functions, AccessGroups, SoD rules.
3. **Diagrama de secuencia (PlantUML):** resolución de permiso
   en runtime — ``user.has_perm("view_reports")`` →
   custom permission backend → AccessGroup M2M Function →
   union de codenames → permite/deniega.
4. **Pseudocódigo completo** de la data migration canónica
   con `PREDEFINED_GROUPS`, `SOD_RULES`, función
   `bootstrap_rbac` con `apps.get_model()` + `get_or_create`.
5. **Sección "Custom groups (`is_system=False`)":** explica
   cómo conviven grupos predefinidos (inmutables) con custom
   creables por `permission_admin` (AGR-007) en runtime via
   UC_PERM_05.
6. **Tabla SoD canónica** — 3 reglas v5.6.0 con grupos
   mutuamente exclusivos. Patrón explicado: todas separan
   `auditor_group` (AGR-008) de roles administrativos.
7. **Trazabilidad** — cross-links a ADR-BACK-007, modelo-datos,
   diagramas existentes (clases, enforcement, ciclo-vida),
   catalogo, grupos-funciones, sod, use-case-view/admin.

Agregado al toctree del index de diagramas RBAC. Bump del
index v1.0.0 → v1.1.0.

## Conclusión del audit

**Alineación con v5.6.0:** ahora completa tras los 3 fixes
de Sección H. Sin residuales semánticos ni de versionado.

**Documentación de grupos:** el nuevo
`bootstrap-grupos-predefinidos.rst` cubre las dudas del
ejecutor sobre:

- Cómo se materializan los 12 grupos al inicializar.
- Quién los crea (Django Migration Engine via `RunPython`).
- Cuándo (automáticamente con `migrate`).
- Con qué funciones (M2M idempotente).
- Cómo se enforzan en runtime (custom permission backend).
- Cómo conviven con custom groups (`is_system` flag).
- Cómo se modelan las reglas SoD (FK a AccessGroup).

## Status del WP

- B-1 (bug fixes alineación): ✅ 3 archivos corregidos.
- B-2 (clarificación de grupos): ✅ documento nuevo creado.
- Strict build: ⏳ pendiente verificación final.
