```yml
project: IACT-docs
work_package: 2026-05-06-05-28-57-design-view-buildout
created_at: 2026-05-06 05:28:57
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-elicitation
size: mediano (Stages 1, 3, 5, 6, 8, 10, 11)
target: Construir source/arquitectura-tecnica/design-view/ completo per Kruchten 4+1 (vista logica) y catalogo UML del proyecto. Producir 4 tipos de diagramas (clases-paquetes, secuencias armonizadas, actividades, estados) usando vocabulario canonico del domain-model. NO redibujar clases del domain-model — DesignView es complementario.
predecessors:
  - 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass (UseCaseView completa)
  - 2026-05-05-21-56-47-functional-decomposition-antipattern-audit (audit Brown 1998 clean en domain-model)
  - 2026-05-06-01-29-18-plantuml-cache-corruption-remediation (cache regenerado 100%)
branch: feature/cnst-033-uml-conformance
reversibility: documentation
```

# WP — Design View Buildout

## Trigger

Per la jerarquia de dependencias declarada (DomainModel → UseCaseView → DesignView → ImplementationView/ProcessView/DeployView), DesignView es el siguiente bloqueador. Sus dependencias estan resueltas:

- DomainModel ✓ (85 archivos, audit Brown 1998 clean)
- UseCaseView ✓ (99 archivos uml-07 standalone)

DesignView desbloquea ImplementationView, ProcessView, DeployView.

## Estado actual de `design-view/`

| Aspecto | Estado |
|---|---|
| Total archivos .rst | 14 (`index.rst` + 13 `seq-{mod}.rst`) |
| Tipo de diagrama presente | Solo secuencias |
| Naming de actores | Localizado (`ServicioAcceso`, `ServicioRBAC`, `RepositorioAssignment`) — NO canonico |
| Cobertura tipos UML esperados | 1 de ~5 (faltan clases-paquetes, actividades, estados) |
| Consistencia con domain-model WP previo | ❌ usa nombres inventados; domain-model tiene `AuthorizationGuard`, `SeparationRuleRepo`, `AccessGroupRepo` |

## Catalogo UML interno consultado (`source/base-cognitiva/_uml/`)

| ID | Tipo | Aplica a DesignView |
|---|---|---|
| uml-03 | Uso orientacion objetos (clases) | ✅ class diagram per modulo |
| uml-04 | Uso de relaciones | ✅ aplicar en class diagrams |
| uml-05 | Agregacion/composicion/interfaces | ✅ idem |
| uml-08 | Diagramas de estados | ✅ ciclos de vida (Call, Alert, etc.) |
| uml-09 | Diagramas de secuencias | ✅ armonizar 14 existentes |
| uml-10 | Diagramas de colaboraciones | ⚠ alternativa a secuencias; NO duplicar |
| uml-11 | Diagramas de actividades | ✅ flujos cross-modulo |
| uml-12 | Componentes | ❌ va en ImplementationView |
| uml-13 | Distribucion | ❌ va en DeployView |
| uml-14 | Vistas arquitectonicas (Rozanski) | informativo, no produce artefactos aqui |

## Distincion clave: DesignView ≠ DomainModel

`domain-model/` ya cubre la **estructura estatica del vocabulario**: 85 clases con atributos, metodos, relaciones (User, Function, Assignment, AuthorizationGuard, etc.). DesignView debe ser **complementario**:

- **NO** redibujar clases del domain-model.
- **SI** mostrar **agrupacion de clases en paquetes/modulos**.
- **SI** mostrar **interaccion entre clases** para satisfacer UCs.
- **SI** mostrar **flujos de proceso** cross-modulo.
- **SI** mostrar **ciclos de vida** de entidades clave.

## Output esperado

| Tipo | Contenido | Cantidad | Naming |
|---|---|---|---|
| Class diagram — package overview | 13 modulos como packages + dependencias inter-modulo | 1 | `package-overview.rst` |
| Class diagram — por modulo | Cada modulo: que clases del domain-model usa + relaciones internas | 13 | `class-{mod}.rst` |
| Sequence diagram — armonizar | Update de 14 `seq-*.rst` con nombres canonicos | 14 (update) | `seq-{mod}.rst` (existente) |
| Activity diagram — flujos criticos | RBAC effective_set, ETL, Alert eval, SoD check, JWT auth, Export async | 6 | `act-{flujo}.rst` |
| State diagram — entidades con ciclo | Call, AlertEvent, PipelineExecution, Session, Assignment, ExportJob | 6 | `state-{entidad}.rst` |
| **Total** | | **40 archivos** (1 nuevo overview + 13 nuevos class + 14 update seq + 6 act + 6 state) | |

## Restricciones operacionales

- **Sin scripts de generacion masiva** (manual, igual que WP UseCaseView).
- **Vocabulario solo del domain-model canonico** (post-Brown audit).
- **Build logs ISO 8601** en `execute/build-logs/`.
- **R-1..R-2.2** de `.claude/rules/long-running-commands.md` para builds.
- **Branch:** `feature/cnst-033-uml-conformance`.
- **Tim Pope commits** (per `.claude/rules/commit-conventions.md`).

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Drift hacia ImplementationView (componentes) o DeployView (nodos) | Adherirse a uml-03..09 + 11; NO uml-12 ni uml-13 |
| R-02 | Duplicar clases del domain-model en class diagrams | En cada `class-{mod}.rst` referenciar via `:doc:` a domain-model y solo mostrar relaciones de uso |
| R-03 | Inconsistencia en nombres entre seq-* nuevos y armonizados | Audit script: validar que TODOS los actores `<<sistema>>` existan como archivos en domain-model/ |
| R-04 | 14 seq-* existentes pueden quedar peor tras armonizacion (perder contexto) | Hacer un commit por cada seq armonizado, revisable individualmente |
| R-05 | 40 archivos = 6-7 horas wall-clock | Stage 8 PLAN-EXECUTION desglosa en T-001..T-040 |
| R-06 | Falsos positivos PlantUML por sintaxis no estandar | Build strict `-W` post cada batch |

## Stopping points

- **SP-01** (gate humano): aprobar bootstrap + analysis. ✅ pre-aprobado en chat.
- **SP-02** (gate humano): aprobar Phase 5 STRATEGY (template + naming).
- **SP-03** (gate tecnico): build strict 0 warnings + audit C-01..C-06 0 violaciones tras cada batch (modulo).
- **SP-04** (gate humano): pre-cierre, coverage analysis (CLASS/SEQ/ACT/STATE vs UCs declarados).

## Stopping Point Manifest

| ID | Fase | Tipo | Evento | Accion requerida |
|---|---|---|---|---|
| SP-01 | 1→3 | gate-fase | analysis aprobado | Avanzar Phase 3 ANALYZE |
| SP-02 | 5→6 | gate-fase | strategy aprobada | Avanzar Phase 6 PLAN |
| SP-03 | 8→10 | gate-fase | task-plan validado | Avanzar Phase 10 EXECUTE |
| SP-04 | 10→11 | gate-tecnico | build clean + audit clean | Avanzar Phase 11 TRACK |
| SP-05 | 11→cierre | gate-humano | lessons + changelog aprobados | Cerrar WP |

## Anatomia del WP

```
2026-05-06-05-28-57-design-view-buildout/
├── wp-state.md                                    ← este
├── design-view-buildout-risk-register.md
├── discover/
│   └── design-view-buildout-analysis.md
├── analyze/
│   ├── current-state-coverage.md
│   ├── uml-types-mapping.md
│   └── domain-model-vocabulary-inventory.md
├── strategy/
│   └── design-view-buildout-solution-strategy.md
├── plan/
│   └── design-view-buildout-plan.md
├── plan-execution/
│   └── design-view-buildout-task-plan.md
├── execute/
│   └── build-logs/
└── track/
    ├── design-view-buildout-changelog.md
    └── design-view-buildout-lessons-learned.md
```
