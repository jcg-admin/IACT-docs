```yml
created_at: 2026-04-29 14:56:40
project: IACT-docs
work_package: 2026-04-29-14-56-40-std007-rename-cleanup
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# STD_007 Violations Inventory

23 archivos con violación de patrón específico (§4.x), todos
pasan hard checks de §3.x.

## Categoría 1 — STD sin número (§4.1)

Patrón requerido: `STD_<NNN>_<Descripcion_PascalCase>.rst`

| Actual | Propuesto | Notas |
|--------|-----------|-------|
| `STD_Naming_Identificadores.rst` | **REQUIERE DECISIÓN** | Posible duplicado/overlap con STD_002_Nomenclatura_Proyecto.rst y STD_007_Convencion_Naming.rst. Verificar contenido antes de renombrar |
| `STD_Profesional_Documentacion.rst` | `STD_008_Profesional_Documentacion.rst` (asumiendo nuevo) | Verificar que sea standalone |

**Acción Cat 1**: revisar contenido + decidir consolidar o
asignar STD_008 / STD_009.

## Categoría 2 — PROCED/PROC/RNF con `_` en descripción (§4.2)

Patrón requerido: `<PREFIX>-<MOD>-<NNN>-<descripcion-kebab>.rst`

| Actual | Propuesto |
|--------|-----------|
| `RNF-PROC-001_PROCESO_SDLC.rst` | `RNF-PROC-001-proceso-sdlc.rst` |
| `RNF-PROC-002_METRICAS_PROCESO.rst` | `RNF-PROC-002-metricas-proceso.rst` |
| `PROC-DEV-001-pipeline_trabajo_iact.rst` | `PROC-DEV-001-pipeline-trabajo-iact.rst` |
| `PROC-DEV-002-sdlc_process.rst` | `PROC-DEV-002-sdlc-process.rst` |
| `PROC-DEVOPS-001-devops_automation.rst` | `PROC-DEVOPS-001-devops-automation.rst` |
| `PROC-GOB-001-mapeo_procesos_templates.rst` | `PROC-GOB-001-mapeo-procesos-templates.rst` |
| `PROC-QA-001-actividades_garantia_documental.rst` | `PROC-QA-001-actividades-garantia-documental.rst` |
| `PROC-QA-002-estrategia_qa.rst` | `PROC-QA-002-estrategia-qa.rst` |
| `PROCED-DEV-001-crear_pull_request.rst` | `PROCED-DEV-001-crear-pull-request.rst` |
| `PROCED-DEV-002-code_review.rst` | `PROCED-DEV-002-code-review.rst` |
| `PROCED-DEV-003-resolver_conflictos_merge.rst` | `PROCED-DEV-003-resolver-conflictos-merge.rst` |
| `PROCED-DEVOPS-001-deploy_staging.rst` | `PROCED-DEVOPS-001-deploy-staging.rst` |
| `PROCED-GOB-001-crear_adr.rst` | `PROCED-GOB-001-crear-adr.rst` |
| `PROCED-GOB-002-actualizar_documentacion.rst` | `PROCED-GOB-002-actualizar-documentacion.rst` |
| `PROCED-QA-001-ejecutar_tests.rst` | `PROCED-QA-001-ejecutar-tests.rst` |

15 archivos. Transformación mecánica: `_` → `-` en descripción
(después del 3er `-`). MAYÚSCULAS (`RNF_PROC_*_*`) → minúsculas.

## Categoría 3 — Guías sin prefijo con `_` (§4.4)

Patrón requerido: `<descripcion-kebab>.rst`

| Actual | Propuesto | Ubicación |
|--------|-----------|-----------|
| `plantilla_adr.rst` | `plantilla-adr.rst` | normativa/estandares/plantillas/ |
| `deployment_plan.rst` | `deployment-plan.rst` | gestion/pm/ |
| `checklist_trazabilidad_requisitos.rst` | `checklist-trazabilidad-requisitos.rst` | gestion/pm/checklists/ |
| `checklist_desarrollo.rst` | `checklist-desarrollo.rst` | gestion/pm/checklists/ |
| `checklist_testing.rst` | `checklist-testing.rst` | gestion/pm/checklists/ |
| `checklist_cambios_documentales.rst` | `checklist-cambios-documentales.rst` | gestion/pm/checklists/ |

6 archivos. Transformación mecánica: `_` → `-`.

## Resumen total

- **23 archivos a renombrar**
- **22 mecánicos** (transformación `_` → `-` o `MAYÚS` → `minus`)
- **1 con decisión** (`STD_Naming_Identificadores` — posible duplicado)

## Verificación cruzada

Files listados arriba PASAN hard checks (§3.x):
- 0 espacios
- 0 tildes/eñe
- 0 paréntesis
- 0 versión en filename
- 0 > 100 chars

Solo violan patrón categorial (§4.x).
