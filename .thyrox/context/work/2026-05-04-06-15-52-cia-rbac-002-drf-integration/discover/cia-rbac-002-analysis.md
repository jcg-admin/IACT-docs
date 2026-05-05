```yml
created_at: 2026-05-04 06:15:52
project: IACT-docs
work_package: 2026-05-04-06-15-52-cia-rbac-002-drf-integration
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# Discover — CIA-RBAC-002 + ADR-GOB-010 DRF Integration

## Problema

`@require_function('RPT-001')` usa `function_id` como argumento.
CIA-RBAC-002 establece que el argumento correcto es el `name`
(codename en snake_case), no el `function_id`.

Ejemplo incorrecto detectado en `analisis-errores-modelo-rbac-v5-2-0.rst`:

```python
@require_function('RPT-001')   # INCORRECTO — function_id
```

Correcto según DEC-001 de CIA-RBAC-002:

```python
@require_function('view_reports')  # CORRECTO — codename
```

## Alcance

### Documentos nuevos a crear

| Artefacto | Destino | Descripción |
|-----------|---------|-------------|
| CIA-RBAC-002 | `source/gestion/evidencia/rbac-arquitectura/cia-rbac-002-arquitectura-permisos-drf.rst` | Change Impact Assessment: 6 decisiones arquitectónicas |
| ADR-GOB-010 | `source/normativa/gobernanza/adr-gob-010-rbac-autorizacion-drf-backend.rst` | ADR: adopción de FunctionAuthorization custom backend |

### Archivos a corregir (notación incorrecta)

| Archivo | Líneas | Problema |
|---------|--------|---------|
| `source/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0.rst` | ~578, ~587 | `@require_function('RPT-001')` → `@require_function('view_reports')` |
| `source/arquitectura-tecnica/matriz-dependencias-uc-iact.rst` | ~1116, ~1332, ~1377 | `@require_function('FUNC-NNN')` → codename real |
| `source/requisitos/casos-uso/permissions/uc-perm-07/informacion-general.rst` | ~52 | `@require_function('F_CODE')` → codename real |

### Directorios nuevos

- `source/gestion/evidencia/rbac-arquitectura/` — subdirectorio para
  CIAs y documentos de arquitectura RBAC vigentes (no históricos)

## Decisiones clave de CIA-RBAC-002

- **DEC-001**: `calculate_effective_functions()` retorna `Set[str]` de
  `name` (codename), NO `function_id`
- **DEC-002**: Codenames exclusivamente `snake_case`
- **DEC-003**: Backend `FunctionAuthorization` intercepta `has_perm()`
- **DEC-004**: Clase `Perm` centraliza constantes (evita literals)
- **DEC-005**: `FunctionPermission(BasePermission)` para DRF
- **DEC-006**: `app_label` resuelto dinámicamente vía `AppConfig`

## Trazabilidad

- CIA-RBAC-002 referencia ADR-GOB-008 (coexistencia ACC+PERM)
- ADR-GOB-010 supersede la parte de implementación DRF de ADR-GOB-009
- ADR-GOB-009 permanece vigente para el modelo conceptual (no supersedido)
