```yml
created_at: 2026-05-04 07:50:12
project: IACT-docs
work_package: 2026-05-04-07-50-12-mod-admin-requisitos-integration
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Discover — MOD_Admin Integración en source/requisitos/*

## Qué se hizo en el WP anterior

El WP `2026-05-04-07-25-32-uc-numbering-conflict` creó el esqueleto de
MOD_Admin:
- `source/arquitectura-tecnica/uc-module-view/mod-admin.rst` — UML + UC table
- `source/requisitos/casos-uso/admin/` — UC dirs: uc-adm-01, uc-adm-02, uc-adm-03
  con `informacion-general.rst` (Parte 1 únicamente)
- `catalogo-funciones.rst` §3.11 — 3 funciones ADM añadidas
- `br-006`, `br-007` — referencias UC corregidas a domain IDs

## Qué falta para integración completa

### Gap 1 — UC specs: solo Parte 1 (informacion-general)

Cada UC del patrón del proyecto tiene 10+ archivos:
```
uc-acc-05/
├── actores-precondiciones.rst
├── criterios-aceptacion.rst
├── datos-involucrados.rst
├── diagramas-uml/
├── excepciones.rst
├── flujo-principal.rst
├── flujos-alternos.rst
├── implementacion-tecnica.rst
├── index.rst
├── informacion-general.rst    ← solo este existe en admin/
├── patrones-diseno.rst
├── requisitos-no-funcionales.rst
└── testing.rst
```

Los uc-adm-01/02/03 tienen `informacion-general.rst` e `index.rst`.
Falta: 10 archivos RST más por UC (total: 30 archivos faltantes).

### Gap 2 — fr-010-02: referencia UC_043

`source/requisitos/requisitos-funcionales/fr-010-02-validar-sod-antes-asignar.rst`
tiene `UC_043→UC_078` pendiente según task-plan WP-1.

### Gap 3 — base-cognitiva/taxonomía: phantom UC refs

Archivos con UC-043..047 que necesitan actualización:
- `fnd-03-casos-de-uso.rst`: UC-043→UC_ADM_01, UC-044→UC_ACC_03,
  UC-045→UC_ADM_03, UC-046→UC_ADM_02, UC-047→UC_ACC_09
- `fnd-04-trazabilidad.rst`: `.. _uc-043:` → `.. _uc-adm-01:`
- `fnd-05-jerarquia-4-niveles.rst`: UC-043, UC-044, UC-047
- `txm-01-taxonomia-requisitos.rst`: lista UC-043

### Gap 4 — mapeo-uc.rst y rbac-core/

Arquitectura técnica tiene referencias UC-043 que apuntan al módulo
de acceso:
- `mapeo-uc.rst`
- `rbac-core/responsabilidades.rst`
- `rbac-core/casos-uso.rst`

### Gap 5 — tpl-uc-casos-de-uso.rst

Template normativa con `UC_043_Configurar_SoD` como ejemplo — debe
actualizarse a `UC_ADM_01_Gestionar_Ciclo_Vida_SoD`.

### Gap 6 — No existen uc-acc-06 y uc-acc-07

`update_separation_rule` y `disable_separation_rule` (nuevas v5.4.0)
no tienen UCs implementados. Están en el catálogo y referenciadas
como UC_ADM_01 ahora, pero el task-plan WP-1 no contemplaba crear
uc-acc-06/07 (el gap se resolvió por absorción en UC_ADM_01).

### Gap 7 — requisitos-funcionales: ¿existe FR para manage_function_catalog?

La función `manage_function_catalog` (nueva v5.6.0) probablemente
necesita un FR nuevo o actualización de FR existente.

## Archivos afectados (15 confirmados)

| Archivo | Gap | Acción |
|---------|-----|--------|
| `fr-010-02-validar-sod-antes-asignar.rst` | UC_043→UC_078 | Replace |
| `fnd-03-casos-de-uso.rst` | UC-043..047 | Replace con domain IDs |
| `fnd-04-trazabilidad.rst` | `.. _uc-043:` | Replace label + artefacto |
| `fnd-05-jerarquia-4-niveles.rst` | UC-043,044,047 | Replace |
| `txm-01-taxonomia-requisitos.rst` | UC-043 | Replace |
| `rbac-core/responsabilidades.rst` | UC_043 | Replace |
| `rbac-core/casos-uso.rst` | UC_043 | Replace |
| `mapeo-uc.rst` | UC-043 (3x) | Replace |
| `tpl-uc-casos-de-uso.rst` | UC_043_Configurar_SoD | Replace |
| `admin/uc-adm-01/` (10 archivos) | Faltan specs | Crear |
| `admin/uc-adm-02/` (10 archivos) | Faltan specs | Crear |
| `admin/uc-adm-03/` (10 archivos) | Faltan specs | Crear |
| `casos-uso/admin/` index | Verificar completo | Revisar |

## Prioridad de ejecución

**Alta** (phantom UCs activos en documentos importantes):
T-001..T-009: replace phantom UC refs en 9 archivos

**Media** (UC specs completas para el nuevo módulo):
T-010..T-012: crear 30 archivos faltantes de especificación

**Baja** (FR nuevo para manage_function_catalog):
T-013: analizar y crear si aplica
```
