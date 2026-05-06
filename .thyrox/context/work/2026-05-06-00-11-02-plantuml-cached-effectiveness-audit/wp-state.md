```yml
project: IACT-docs
work_package: 2026-05-06-00-11-02-plantuml-cached-effectiveness-audit
created_at: 2026-05-06 00:11:02
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-elicitation
target: Auditar por que percibimos que source/_ext/plantuml_cached.py "no se usa" cuando esta declarado en conf.py:44 y esta tomando efecto. Cuantificar hit rate, identificar fuentes de cache miss, proponer remediacion (prerender update o nuevo workflow).
predecessor_wp: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
trigger: build strict slow + socket timeout durante WP predecesor; sospecha de que cache no funcionaba.
```

# WP — PlantUML Cached Effectiveness Audit

## Trigger

Durante el cierre del WP predecesor (`use-case-view-uml07-standalone-pass`):

1. Build strict `-W` tomo ~15-20 minutos (anormal para Sphinx en docs).
2. La conexion API se cayo con socket error mid-build.
3. Sospecha del ejecutor: "no estamos usando `source/_ext/plantuml_cached.py`".

## Estado conocido al iniciar (Phase 1 DISCOVER)

### Configuracion declarativa

`source/conf.py:44` declara `plantuml_cached` en la lista
`extensions = [...]`, cargado **despues** de `sphinxcontrib.plantuml`.
Comentario en linea 39-41 confirma intencion:

> *"PlantUML para diagramas — plantuml_cached debe cargarse DESPUES
> de sphinxcontrib.plantuml para que el override del directive
> `uml` quede activo (last registration wins en docutils)."*

### Extension del cache

```
source/_generated_diagrams/   ← directorio cache de SVGs
  count SVGs: 1227
```

### Build evidence (sphinx-strict-final-2026-05-05T23-37-04.log)

```
plantuml_cached: miss hash=... docname=...   →  188 ocurrencias
```

Diagramas referenciados en source: **1119** directivas `.. uml::`
en 1038 archivos.

### Hit rate inicial calculado

```
hits = 1119 - 188  = 931
hit_rate = 931 / 1119 = 83.2%
miss_rate = 188 / 1119 = 16.8%
```

## Hipotesis preliminares

### H-1 — El cache SI funciona, pero esta desactualizado

83% hit rate sugiere que `plantuml_cached` opera. Los 188 misses
podrian ser:

- Nuevos diagramas creados despues del ultimo run del prerender
  (i.e. los 99 nuevos archivos del WP predecesor: 83 uml-07 + 16
  domain-model). 99 nuevos archivos pueden contener
  ~150-188 directivas `.. uml::` (algunos archivos tienen 1, otros
  2+).
- Cambio del archivo `source/_static/plantuml-styles.puml` que
  invalida hashes existentes.
- Modificaciones en diagramas existentes desde el ultimo prerender.

### H-2 — La percepcion de "no se usa" se debe al impacto de los misses

Cada miss invoca Java + PlantUML con tiempo ~5-15s. 188 misses
× 10s/miss = ~30 minutos de tiempo wall-clock dedicado solo a
generar diagramas no cacheados. Esto explicaria:

- Build strict de ~15-20 min observado.
- Socket timeout durante el build (la conexion API espera
  respuesta del proceso de build).

### H-3 — El prerender script debe correrse despues de cada batch

`scripts/prerender-plantuml.py` existe pero NO esta en el flujo
estandar post-creacion de diagramas. El predecesor
`use-case-view-uml07-standalone-pass` no lo invoco como SP-03
mandatorio.

### H-4 — La extension funciona pero el flujo no la aprovecha

El override esta activo (evidencia: el log dice
`"plantuml_cached: miss"`, lo cual solo se emite desde el
extension). Pero el ejecutor no sabe cuando correr prerender.

## Output esperado

1. `discover/plantuml-cached-effectiveness-audit-analysis.md` —
   inventario + hipotesis confirmadas/descartadas.
2. `analyze/cache-state-analysis.md` — counts exactos:
   - directivas `.. uml::` totales por modulo.
   - SVGs presentes en `_generated_diagrams/`.
   - Misses por modulo del ultimo build.
   - Tiempo medio de cada miss.
3. `analyze/prerender-script-analysis.md` — analisis del script
   `scripts/prerender-plantuml.py`:
   - cuando se corre.
   - que invalida cache.
   - integracion con CI.
4. `track/recommendations.md` — propuesta de:
   - run prerender ahora para llevar hit rate a 100%.
   - integrar prerender en SP-03 estandar de WPs futuros.
   - automatizar prerender en pre-commit hook.

## Stopping points

- **SP-01** (gate humano): aprobar bootstrap + analysis.
- **SP-02** (gate tecnico): correr prerender, verificar 0 misses
  en build siguiente.
- **SP-03** (gate humano): aprobar recomendaciones para
  estandarizacion en WPs futuros.

## Anatomia del WP

```
2026-05-06-00-11-02-plantuml-cached-effectiveness-audit/
├── wp-state.md                                         ← este
├── discover/
│   └── plantuml-cached-effectiveness-audit-analysis.md
├── analyze/
│   ├── cache-state-analysis.md
│   └── prerender-script-analysis.md
└── track/
    ├── recommendations.md
    └── plantuml-cached-effectiveness-audit-changelog.md
```
