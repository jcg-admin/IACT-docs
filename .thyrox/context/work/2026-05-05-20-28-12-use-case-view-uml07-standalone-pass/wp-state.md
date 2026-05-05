```yml
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
created_at: 2026-05-05 20:28:12
current_phase: Phase 10 — EXECUTE
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
sp_phase8_approved_at: 2026-05-05 21:50:00
sp_phase8_decisions:
  - std012_ubicacion: opcion 2 (auto-explicativo flat) — target del WP
  - std012_actualizar_versiones: pendiente WP futuro v1.1.0
  - std011_aliases: alias = label exacto, sin abreviar
  - ejecutar_loop: aprobado
sp01_approved_at: 2026-05-05 20:50:00
sp01_decisions:
  - status_inicial: Vigente v1.0.0
  - actores: funciones RBAC (P-15)
  - scope_domain_model_completion: incluido
sp_phase3_approved_at: 2026-05-05 21:05:00
sp_phase3_decisions:
  - clases_nuevas_aprobadas: 9 (AuthorizationGuard, BlacklistedToken, InternalMessage, PipelineExecutionRepo, MetricsCache, IdempotencyPolicy, ExpirationPolicy, PasswordGenerator, EffectivePermissionsAggregator)
  - repos_canonicos_aprobados: 5 (UserRepo, FunctionRepo, FunctionGroupRepo, SeparationRuleRepo, AccessGroupRepo)
  - specification_strategy_patterns: archivo separado documental
  - orden_ejecucion: 14 archivos domain-model PRIMERO, luego 83 uml-07 standalone
predecessor_wp: 2026-05-05-14-49-16-use-case-view-uml07-rebuild
target: Construir 83 archivos uml-07 standalone en source/arquitectura-tecnica/use-case-view/<module>/uc-XXX-NN-<slug>.rst con funciones RBAC como actores (P-15), nombres auto-explicativos, conforme a uml-07 R-01..R-12 y BR-006 Flat NIST. Adicionalmente, completar domain-model/* con clases y métodos faltantes referenciados por los UCs.
```

# WP — Use Case View UML-07 Standalone Pass

## Trigger

El WP predecesor (`2026-05-05-14-49-16-use-case-view-uml07-rebuild`) declaraba este mismo
target pero su sesión derivó hacia trabajo en `casos-uso/<mod>/<uc>/diagramas-uml/` (uml-06
embebido en spec textual). El target original — 83 archivos **uml-07 standalone** en
`use-case-view/<module>/` — quedó sin ejecutar.

Este WP retoma ese target con el insumo de los 83 diagramas uml-06 ya existentes
(53 nuevos del predecesor + 30 pre-existentes) como base de modelo.

## Distinción crítica (heredada del predecesor)

| Artefacto | Ubicación | Reference UML | Naturaleza |
|-----------|-----------|---------------|------------|
| `casos-uso/<mod>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` | `source/requisitos/...` | **uml-06** | Diagrama embebido en spec textual del UC (12 partes) |
| `use-case-view/<module>/uc-XXX-NN-<slug>.rst` | `source/arquitectura-tecnica/...` | **uml-07** | Diagrama arquitectónico standalone, auto-explicativo |

El target de este WP es la columna derecha — **uml-07 standalone**.

## Estado al iniciar

| Aspecto | Cuenta | Status |
|---|---|---|
| Inventario base (`discover/inventory.json` heredado) | 83 UCs | ✓ |
| Archivos uml-06 existentes en `casos-uso/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` | 83 | ✓ insumo |
| Archivos uml-07 standalone en `use-case-view/<module>/uc-XXX-NN-<slug>.rst` | **0** | ❌ — target |
| Module index files en `use-case-view/<module>/index.rst` | 13 | ✓ existen, requieren update |
| Domain-model files | 69 | ✓ insumo (cross-refs ya identificados) |

## Flow + lecciones heredadas del predecesor

Las 7 lecciones (L-01..L-07) del predecesor deben aplicarse:

1. **L-01** — Re-leer `wp-state.md::target` antes de cada Phase. ESTE WP ESTÁ FOCALIZADO
   EN: `use-case-view/<module>/uc-XXX-NN-<slug>.rst`. NO desviar a `casos-uso/`.
2. **L-02** — Cada artefacto declara `Tipo: uml-07 standalone`.
3. **L-03** — Nivel A profundo: leer `flujos-alternos.rst` + `excepciones.rst` +
   `criterios-aceptacion.rst` además de los 2 archivos del predecesor.
4. **L-04** — Cross-refs a domain-model en template inicial, no como add-on.
5. **L-05** — Build logs en formato ISO 8601 dentro del WP.
6. **L-06** — `pgrep -af "sphinx-build" | wc -l = 1` antes de medir warnings.
7. **L-07** — Branch protection: PR #14 ya abierta sobre `feature/cnst-033-uml-conformance`.
   Este WP NO toca esa rama; opera sobre nueva rama derivada de `feature/solve-problem-docs`
   tras merge del PR #14.

## Convenciones aplicadas (heredadas + refinadas)

### Naming auto-explicativo

`use-case-view/<module>/uc-XXX-NN-<slug-descriptivo>.rst`

| Antes (stub propuesto en WP previo) | Ahora (auto-explicativo) |
|--------------------------------------|---------------------------|
| `uc-acc-01/index.rst` | `uc-acc-01-asignar-funciones.rst` |
| `uc-rpt-04/index.rst` | `uc-rpt-04-exportar-reporte.rst` |
| `uc-auth-03/index.rst` | `uc-auth-03-recuperar-contrasena.rst` |

### Reglas

- Prefijo `uc-XXX-NN-` preserva trazabilidad al ID canónico de casos-uso.
- Slug en kebab-case en castellano (titulo del UC en casos-uso).
- Sin acentos, sin caracteres especiales.
- Sin sub-directorio: archivo directo en `<module>/`.

### Reglas uml-07 (de WP `use-case-view-uml07-conformance-pass` predecesor lejano)

| ID | Regla | Aplica per-UC |
|----|-------|---------------|
| R-01 | Actor iniciador izq, beneficiario der | ✓ donde semántica exista |
| R-02 | Stick figure + elipse | ✓ todos |
| R-03 | Rectangle = sistema (MOD_X) | ✓ todos |
| R-04 | Línea asociativa sin estereotipo | ✓ todos |
| R-05 | Jerarquía actores | ✗ — BR-006 Flat NIST prohíbe |
| R-06 | `<<include>>` con `..>` | ✓ donde aplique |
| R-07 | UC included nunca solo | ✓ — uc-inc-rpt-01 NO recibirá archivo standalone |
| R-08 | `<<extend>>` con `..>` (ext → base) | ✓ donde aplique |
| R-09 | Extension points en label del UC base | ✓ |
| R-10 | Generalización UCs `--|>` | △ — opcional, evaluar caso por caso |
| R-11 | UCs alto nivel con detalle | ✓ |
| R-12 | NO detalles implementación | ✓ — sin SP/SQL/codenames como UC |

### Restricciones IACT

- **BR-006 RBAC Flat NIST + CNST-005**: NO `<|--` entre actores.
- **CNST-033**: identificadores de actor en inglés (`Operator`, `Supervisor`, `Caller`).
- **STD-008**: identifiers en inglés.

### Funciones RBAC como actores (P-15, NO roles)

Coherente con el patrón de uml-06 del predecesor y con P-15 RBAC granular: el actor
en cada diagrama es la **función RBAC** que invoca el UC, no un rol agregador.

```
actor "view_reports" as INVOKER         ✓ correcto
actor "Reporter" as INVOKER              ✗ incorrecto (rol, no función)
```

**Razón:** un mismo rol agrupa N funciones, pero el UC se dispara por **una** función
específica (P-15). El actor del diagrama identifica esa función — más preciso para
trazabilidad RBAC y consistente con el sistema de assignments granular.

**Caller externo:** sí es un rol (no autenticado, sin función RBAC). Se mantiene como
`Caller <<externo>>`.

**Sistema:** entidades del propio sistema (servicios, repos, engines) van como actores
con stereotype `<<sistema>>` y nombre canónico del **domain-model**.

**Stereotypes de actor:**

| Stereotype | Cuándo | Ejemplo |
|---|---|---|
| (sin stereotype) | Función RBAC iniciadora del UC | `actor "view_reports" as INVOKER` |
| `<<beneficiario>>` | Otra función RBAC que recibe del UC (R-01 uml-07) | `actor "view_audit_log" as view_audit_log <<beneficiario>>` |
| `<<sistema>>` | Componente del domain-model (servicio/repo/engine) | `actor "PermissionCache" as PC <<sistema>>` |
| `<<externo>>` | Actor fuera del sistema (no autenticado) | `actor "Caller" as CALLER <<externo>>` |

## Estrategia de generación

### Insumos por UC

Para cada uno de los 83 UCs, leer:

1. `casos-uso/<mod>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` — uml-06 (modelo base).
2. `casos-uso/<mod>/<uc>/informacion-general.rst` — proposito, scope, BReq.
3. `casos-uso/<mod>/<uc>/actores-precondiciones.rst` — actores principales/secundarios.
4. `casos-uso/<mod>/<uc>/flujo-principal.rst` — pasos canónicos.
5. `casos-uso/<mod>/<uc>/flujos-alternos.rst` — extends candidatos.
6. `casos-uso/<mod>/<uc>/excepciones.rst` — error paths que pueden modelarse como extends.
7. `casos-uso/<mod>/<uc>/criterios-aceptacion.rst` — confirmar inclusiones.

### Transformación uml-06 → uml-07

1. **Actores** (mantener funciones RBAC, no roles):
   - INVOKER = función RBAC del UC (igual que uml-06 — P-15 granular).
   - Beneficiarios = funciones RBAC consumidoras con `<<beneficiario>>`.
   - Sistemas = entidades del **domain-model canónico** con `<<sistema>>` y
     **nombre exacto del archivo del domain-model** (e.g. `PermissionCache`,
     `AuditService`, `ExportWorker`).
   - Eliminar `<|--` entre actores (BR-006).
2. **Sanitizar usecases**:
   - Eliminar nombres de SP/SQL del label (R-12).
   - Verificar/corregir dirección de `<<extend>>` (R-08).
3. **Enriquecer**:
   - Agregar extends desde `flujos-alternos.rst` no presentes en uml-06.
   - Agregar extension points en labels del UC base (R-09).
   - Notas BR/CNST/P/ADR exhaustivas (incluyendo `criterios-aceptacion.rst`).
4. **Cross-refs**:
   - Sección `seealso` con `:doc:` a entidades relevantes del **domain-model**.
   - `:doc:` a UC backing si es vista alternativa (UC_PERM_NN → UC_ACC_NN).
   - `:doc:` a spec textual del UC (`/requisitos/casos-uso/<mod>/<uc>/index`).
5. **Completar domain-model si falta** (NUEVO scope vs predecesor):
   - Si un sistema referenciado en el UC NO existe en `domain-model/`, crearlo.
   - Si una clase existe pero le faltan métodos referenciados, completarlos.
   - Documentar adiciones en `analyze/domain-model-completion-analysis.md`.

### Ubicación final

```
use-case-view/<module>/uc-XXX-NN-<slug>.rst
```

## Output esperado

- **83 archivos** en `use-case-view/<module>/uc-XXX-NN-<slug>.rst`.
- **13 module index** actualizados con xref table apuntando a esos 83 archivos
  (en lugar de a `casos-uso/<uc>/diagramas-uml/diagrama-de-caso-de-uso`).
- **0 errores de pre-render PlantUML**.
- **Auditoría** con script: 0 violaciones de uml-07 R-01..R-12 + 0 violaciones de BR-006.
- **Build limpio** strict (`sphinx-build -W`) con 0 warnings nuevos.
- **Domain-model completado** — nuevas clases y métodos creados según gaps detectados
  en Phase 3 ANALYZE. Documento de gap analysis: `analyze/domain-model-completion-analysis.md`.
  Estimación inicial heredada del predecesor (Q3+Q4): ~18 clases nuevas + ~30 métodos.

## Riesgos identificados (heredados + nuevos)

- **R-01**: 53 UCs con uml-06 "shallow" como insumo. Mitigación: releer
  `flujos-alternos` y `excepciones` para enriquecer extends y notas.
- **R-02**: Mapping de funciones RBAC → roles canónicos puede tener ambiguedad
  (e.g. ¿UC_OPR_10 read_own_mailbox usa rol `Operator` o un rol más específico
  `Agent`?). Mitigación: usar tabla declarada arriba; si nuevo caso surge,
  documentar decisión en `decisions-log.md`.
- **R-03**: 83 archivos × tiempo de revisión humana = mucho effort. Mitigación:
  scripted generation con plantilla deterministica + validación incremental
  por módulo.
- **R-04 (nuevo)**: Drift de scope nuevamente. Mitigación: L-01 — re-leer
  `wp-state.md::target` antes de cada Phase. Auditoría continua que NO se
  tocan archivos en `casos-uso/`.

## Stopping points

- **SP-01** (gate humano): aprobar este `wp-state.md` + `discover/<wp>-analysis.md`
  antes de avanzar a Phase 5 STRATEGY.
- **SP-02** (gate humano): tras generar 5 archivos sample (uno por módulo principal),
  validar pattern con ejecutor antes de propagar a los 78 restantes.
- **SP-03** (gate técnico): build strict `-W` con 0 warnings + audit script
  con 0 violaciones después de cada batch.
- **SP-04** (gate humano): pre-merge final, build limpio + revisión humana de
  módulos críticos (operator, reports, audit).

## Decisiones del ejecutor (resueltas)

1. **Naming auto-explicativo**: APROBADO formato `uc-XXX-NN-<slug-descriptivo>.rst`.
2. **Actores = funciones RBAC** (P-15), NO roles. Coherente con uml-06 predecesor.
3. **Status inicial**: pendiente de confirmar — sugiero `Borrador v0.9` por riesgo R-01.
4. **Granularidad**: ejecución por módulos con SP-02 sample + SP-03 build por módulo.
5. **Rama**: `feature/cnst-033-uml-conformance` (la actual del PR #14). El WP continúa
   sobre la misma rama; el merge de PR #14 incluirá tanto el cierre del predecesor
   como el avance de este sucesor.

## Pendientes para SP-01 (gate humano)

Solo queda confirmar:

- ¿`status: Vigente v1.0.0` o `status: Borrador v0.9`?
- ¿OK avanzar a Phase 3 ANALYZE con el plan actualizado?

## Anatomía esperada del WP (cajones que se irán creando)

```
2026-05-05-20-28-12-use-case-view-uml07-standalone-pass/
├── wp-state.md                                ← este archivo
├── use-case-view-uml07-standalone-pass-risk-register.md
├── use-case-view-uml07-standalone-pass-exit-conditions.md   ← Phase 6
├── discover/                                  ← Phase 1 (en curso)
│   ├── use-case-view-uml07-standalone-pass-analysis.md
│   ├── inventory.json                         ← copia + actualización del predecesor
│   └── decisions-log.md
├── analyze/                                   ← Phase 3
│   └── role-mapping-deep-analysis.md
├── strategy/                                  ← Phase 5
│   └── use-case-view-uml07-standalone-pass-solution-strategy.md
├── plan/                                      ← Phase 6
│   └── use-case-view-uml07-standalone-pass-plan.md
├── design/                                    ← Phase 7
│   ├── use-case-view-uml07-standalone-pass-requirements-spec.md
│   └── template-uc-standalone.md
├── plan-execution/                            ← Phase 8
│   └── use-case-view-uml07-standalone-pass-task-plan.md   (T-NNN por módulo o por UC)
├── pilot/                                     ← Phase 9 (5 sample UCs)
│   └── pilot-results.md
├── execute/                                   ← Phase 10
│   ├── use-case-view-uml07-standalone-pass-execution-log.md
│   └── build-logs/                            ← logs ISO 8601
├── track/                                     ← Phase 11
│   ├── use-case-view-uml07-standalone-pass-lessons-learned.md
│   └── use-case-view-uml07-standalone-pass-changelog.md
└── standardize/                               ← Phase 12
    └── use-case-view-uml07-standalone-pass-patterns.md
```

## Próximos pasos

1. (este momento) Bootstrap del WP: `wp-state.md` + `discover/<wp>-analysis.md` +
   `<wp>-risk-register.md`.
2. **SP-01**: ejecutor aprueba bootstrap + responde 5 preguntas pendientes arriba.
3. (Phase 1 cierre) Inventory + decision log inicial.
4. **Gate Phase 1 → Phase 3** (saltamos Phase 2 BASELINE — no hay baseline cuantitativo).
5. (Phase 3) `analyze/role-mapping-deep-analysis.md` — validar mapping
   función → rol con específicos por módulo.
6. (Phase 5) `strategy/...-solution-strategy.md` — declarar template + sanitization
   pipeline + cross-refs.
7. (Phase 7) `design/...-requirements-spec.md` con plantilla canónica.
8. (Phase 9) 5 sample UCs (admin, operator, reports, supervision, caller).
9. **SP-02**: ejecutor valida sample.
10. (Phase 10) generación masiva por módulo, commits checkpoint Tim Pope.
11. **SP-03**: build strict + audit script post cada módulo.
12. (Phase 11) lessons + changelog.
13. (Phase 12) patrones reutilizables + final report.
