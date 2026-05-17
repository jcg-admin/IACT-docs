```yml
created_at: 2026-05-05 20:28:12
project: IACT-docs
work_package: 2026-05-05-14-49-16-use-case-view-uml07-rebuild
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Lessons Learned — WP `use-case-view-uml07-rebuild`

## Resumen ejecutivo

| Aspecto | Estado |
|---|---|
| **Target original declarado** | Construir 83 diagramas per-UC en `use-case-view/<module>/uc-XXX-NN-<slug>.rst` (uml-07 standalone) |
| **Cumplimiento del target original** | ❌ **0 / 83** — scope desviado |
| **Trabajo entregado (auxiliar)** | ✅ 53 diagramas en `casos-uso/<mod>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` (uml-06 embebido) |
| **Cross-refs domain-model** | ✅ 53 archivos × 1-9 `:doc:` refs (≈250 cross-refs) |
| **CI desbloqueado** | ✅ PR #14 verde, mergeable_state: clean |
| **Build local** | ✅ 0 warnings sobre HEAD `43823a51` |
| **Sucesor** | WP `2026-05-05-20-28-12-use-case-view-uml07-standalone-pass` (en DISCOVER) |

## Contexto del desvío

### Lo que el WP declaraba

> `target: Construir 83 diagramas per-UC en use-case-view conforme a uml-07, con nombres auto-explicativos`
>
> `Ubicación final: use-case-view/<module>/uc-XXX-NN-<slug>.rst`

### Lo que ocurrió en sesión

El ejecutor pidió desbloquear CI de PR #14 (que estaba `unstable` por 73 warnings). El diagnóstico
mostró que la mayoría de los warnings (51 + 2 + 3) eran refs forward a archivos
`casos-uso/<mod>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` que no existían.

**Decisión tomada:** generar esos 53 archivos faltantes en su ubicación canónica (`casos-uso/`),
NO en `use-case-view/`. Esto desbloqueó CI pero **no es el target del WP**.

### Por qué el desvío fue razonable (en su momento)

1. CI rojo bloqueaba TODO PR posterior — necesitaba fix inmediato.
2. Los archivos faltantes en `casos-uso/` eran un gap pre-existente, independiente del WP.
3. Generar uml-06 (canónico embebido en spec) primero es buena base para uml-07 (standalone).

### Por qué el desvío fue problemático

1. Mezclar trabajo del WP con fix de CI hizo invisible que el target original no se cumplió.
2. La distinción uml-06 vs uml-07 (declarada en el propio `wp-state.md`) no se enfatizó durante
   la ejecución — terminamos creando uml-06 cuando el target era uml-07.
3. La tabla del `wp-state.md` ya advertía:

   | Artefacto | Reference uml | Contiene |
   |-----------|---------------|----------|
   | `casos-uso/<mod>/<uc>/diagramas-uml/` | uml-06 (introduccion) | Specs textuales |
   | `use-case-view/<mod>/` | **uml-07 (diagramas)** | **Diagramas standalone** |

   Pero esta tabla se ignoró durante el shift de scope.

## Lecciones

### L-01 — Re-leer `wp-state.md` antes de cada Phase

Cuando un WP cambia de fase o se reanuda en sesión nueva, releer el `wp-state.md::target`.
Si el trabajo en sesión no avanza ese target, eso es un **scope drift**, no progreso.

**Acción correctiva:** En la próxima sesión del nuevo WP, confirmar al iniciar:
- ¿Estamos avanzando el target? Sí/No.
- Si No, ¿es desvío justificado o estamos perdiendo el rumbo?

### L-02 — Distinguir uml-06 (embebido) vs uml-07 (standalone) explícitamente

El WP declaraba la distinción pero no la usaba en cada decisión. Resultado: 53 archivos
hechos en la ubicación equivocada para el WP, aunque correctos para la salud del repo.

**Acción correctiva:** En cada artefacto del nuevo WP, declarar arriba:

```
Tipo: uml-07 standalone (NO confundir con uml-06 en casos-uso/<uc>/diagramas-uml/)
```

### L-03 — Compresión de tiempo no equivale a Nivel A profundo

El plan original de Nivel A estimaba 5-10 días para 53 UCs (~30 min de spec read por UC).
La sesión los hizo en ~1h (~2-3 min por UC), leyendo solo 1-2 archivos de los 4-5 esperados.

**Resultado:** Diagramas funcionales pero con cobertura "Nivel A shallow":
- Actores principales correctos.
- Sub-usecases del flujo principal cubiertos.
- Sub-usecases de flujos alternos / excepciones **parciales**.
- Notas BR/CNST no exhaustivas.

**Acción correctiva:** En el sucesor `use-case-view-uml07-standalone-pass`, partir de los 53
uml-06 ya existentes pero releer `flujos-alternos.rst` + `excepciones.rst` + `criterios-aceptacion.rst`
para enriquecer extends y notas en la versión standalone.

### L-04 — Cross-refs a domain-model deben ser parte del template canónico

Los 53 archivos quedaron sin `:doc:` cross-refs hasta que el ejecutor lo pidió explícitamente.
Después se agregó como "tercer pase" sobre los mismos archivos.

**Acción correctiva:** En el sucesor, el template inicial debe incluir la sección `seealso`
con `:doc:` a domain-model **desde la primera versión**, no como add-on.

### L-05 — Build logs en formato ISO 8601 (regla nueva)

Durante la sesión se descubrió que los logs de build vivían en `/tmp` (efímeros) y con
naming `HH-MM` (sin fecha). Se codificó la regla en `.claude/rules/build-logs.md`:

- Logs van a `{wp}/{stage}/build-logs/{cmd}-{ctx}-{ISO}.log`
- ISO 8601: `YYYY-MM-DDTHH-MM-SS` (`:` reemplazado por `-` para filesystem)
- Comando canónico: `ISO=$(date -u +%Y-%m-%dT%H-%M-%S)`

Aplicado retroactivamente a 3 logs históricos del WP.

### L-06 — Race condition en builds simultáneos genera mediciones falsas

En sesión hubo 2 builds sphinx-build corriendo en paralelo sobre el mismo `build/`. Resultado:
warnings reportados (5) ≠ warnings reales (73). Detectado por re-build con `pgrep | wc -l = 1`.

**Acción correctiva:** Antes de declarar conteo de warnings, verificar
`pgrep -af "sphinx-build" | wc -l = 1` durante todo el run. La regla está documentada en
`build-logs.md`.

### L-07 — Branch protection es feature, no bug

Push a `feature/solve-problem-docs` falló con 403. Esto es correcto — la rama tiene branch
protection requiriendo PR. La solución correcta NO es bypass — es abrir PR (#14).

Ver `.claude/rules/git-flow.md` R-03/R-04 — codificada en otra sesión durante este WP.

## Trabajo entregado (efectivo, aunque desviado del target)

### En `casos-uso/` (uml-06 embebido) — 53 archivos

Todos contienen ahora un PlantUML real (no stubs) con:
- Section "8.1 Diagrama de caso de uso"
- Bloque `@startuml`/`@enduml` con `left to right direction`
- INVOKER (función RBAC del UC) + beneficiarios + Sistema actors
- Rectangle `MOD_<Module>` con UC principal + sub-usecases
- Relaciones `..>` con `<<include>>`/`<<extend>>`
- Notas BR/CNST/P
- Sección `.. seealso::` con `:doc:` cross-refs a domain-model

Distribución:
| Módulo | UCs Level A |
|---|---|
| admin | 3 |
| permissions | 3 |
| audit | 4 |
| pipeline | 4 |
| alerts | 5 |
| caller | 5 |
| supervision | 3 |
| reports | 9 |
| logs | 7 |
| operator | 10 |
| **Total** | **53** |

### En `domain-model/` — fixes

- 3 refs corregidos: `uc-acc-06/index` y `uc-acc-07/index` (no existen) → `uc-perm-03/04`.
- 7 typography fixes (Title underline/overline too short).

### Reglas codificadas

- `.claude/rules/build-logs.md` — ISO 8601 + WP path enforcement.
- `.claude/rules/git-flow.md` — feature/<wp> → solve-problem-docs → develop (R-01..R-08).

### CI

- PR #14 abierta, validate `success`, mergeable_state `clean`.
- HEAD `43823a51` — 44 commits, +23,109 / -2,032 LoC, 1,565 archivos.

## Trabajo NO entregado (target original)

- ❌ 83 archivos `use-case-view/<module>/uc-XXX-NN-<slug>.rst` (0 / 83).
- ❌ Module index updates con xref a esos 83 (0 / 13).
- ❌ Audit script de uml-07 R-01..R-12 conformance.

## Decisiones documentadas durante el WP

- **D-01**: codificar git-flow como `.claude/rules/`.
- **D-02**: R-03 — feature/<wp> → solve-problem-docs (no develop directo).
- **D-03**: PR #14 vehículo de integración.
- **D-04**: investigar CI antes de mergear (opción A).
- **D-05**: codificar build-logs.md (ISO 8601).
- **D-06**: fix CI minimal con rename ETL→Pipeline.
- **D-06b**: realización post-build limpio: 73 warnings reales (no 5 medidos por race).
- **D-07**: Híbrido B+A — stubs primero, luego Nivel A.
- **D-08**: pivot a Nivel A puro (53 uml-06 con seealso).
- **D-09**: cross-link 53 con domain-model (250+ refs).

Trazabilidad completa: `discover/decisions-log.md`.

## Métricas del WP

| Métrica | Valor |
|---|---|
| Duración total | ~6h (sesión continua + interrupciones) |
| Archivos creados/modificados | 53 (uml-06) + 12 (toctree) + 4 (fix domain-model + typography) + 5 (rules + scripts) |
| Commits | 7 checkpoint + 4 bootstrap = 11 commits del WP |
| Warnings antes / después | 73 → 0 |
| Build local final | `build succeeded` |
| CI PR #14 | `success` |

## Patrón identificado para STANDARDIZE futuro

**Patrón:** "Stub-first then upgrade" para WPs grandes con muchos archivos faltantes.

1. Generar stubs estructurados con marca TODO específica del WP.
2. Verificar CI verde con stubs (desbloquea integración).
3. Reemplazar stubs por contenido real, módulo por módulo.
4. Cross-references como pase final.

Pros: desbloqueo rápido de pipeline, deuda explícita, recovery por checkpoint.
Contras: tentación a marcar el WP como "completo" cuando aún hay TODO escondidos.

Mitigación: script `find-uc-stubs.sh` (genérico: `find-{type}-stubs.sh`) que detecta
el marcador y reporta cuenta de pendientes. Ya creado para este WP.

## Status final del WP

`Cerrado` — scope original NO completado, scope auxiliar completado, sucesor abierto.

## Sucesor

`2026-05-05-20-28-12-use-case-view-uml07-standalone-pass` — retoma el target original
(83 archivos uml-07 standalone en `use-case-view/<module>/`) tomando como insumo:

1. `discover/inventory.json` (hereda inventario de 83 UCs).
2. Los 53 archivos uml-06 + 30 pre-existentes en `casos-uso/<mod>/<uc>/diagramas-uml/`
   como base de modelo (actores/include/extend ya analizados).
3. Lecciones L-01..L-07 como guía de proceso.
