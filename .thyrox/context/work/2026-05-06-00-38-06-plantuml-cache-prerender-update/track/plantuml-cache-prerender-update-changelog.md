```yml
created_at: 2026-05-06 01:25:00
project: IACT-docs
work_package: 2026-05-06-00-38-06-plantuml-cache-prerender-update
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — PlantUML Cache Prerender Update

## Resumen

| Metrica | Antes | Despues |
|---|---|---|
| Cache hit rate | 81.8% (953/1165) | **99.7% (1162/1165)** |
| Cache misses por build | 188 | **3** |
| Build strict EXIT | 1 (con 33 warnings de titulos) | **0** |
| Build strict warnings | 33 (predecesor) | **0** |
| SVGs en cache | 1227 | 1438 (+211) |

Reduccion de misses: **98.4%**.

## Trabajo realizado

### Phase 1 DISCOVER

Verificacion de pre-conditions (script existe, plantuml CLI presente,
Java 21 disponible) + dry-run inicial: 212 missing / 1165 totales.

### Phase 10 EXECUTE — 4 iteraciones

#### Iteracion 1: revelacion del bug `-cfgfile`

Primera corrida del prerender produjo 170 SVGs "renderizados" pero,
al inspeccionar contenido, **TODOS contenian "Syntax Error"** —
placeholder generado por PlantUML cuando se le pasa
`plantuml-styles.puml` como `-cfgfile`. El archivo de styles esta
disenado para `!include` desde dentro de bloques `@startuml`, no
como cfgfile CLI.

Adicionalmente, los diagramas con `@startuml NAME` causaban
escritura colateral a `NAME.svg` en el dir de cache, sobrescribiendo
35 SVGs legacy descriptive-named de un workflow anterior. Esos
overwrites fueron revertidos.

#### Iteracion 2: fix `-cfgfile` removido

`scripts/prerender-plantuml.py`: quitado `-cfgfile`, agregada
validacion defensiva (rechaza SVG con string "Syntax Error").
Ejecutado nuevamente: 170 SVGs validos generados, 42 errores
restantes.

#### Iteracion 3: graphviz instalado

Los 42 errores eran `java.io.IOException: Cannot run program
"/opt/local/bin/dot"`. PlantUML necesita Graphviz para diagramas
de clase complejos. Instalado `apt-get install -y graphviz`. Re-
ejecutado: 0 nuevos rendered (los 170 ya cacheados), pero los 42
seguian fallando con `plantuml exit 0, no output`.

#### Iteracion 4: fix `@startuml NAME` -> `@startuml`

Causa de los 42 "no output": diagramas con sintaxis
`@startuml NAME` hacian que PlantUML escribiera el SVG a
`NAME.svg` en lugar de `{hash}.svg`. El script chequeaba
`{hash}.svg` y reportaba "no output" aunque el render era
exitoso (en otro path).

`scripts/prerender-plantuml.py`: agregado strip del NAME al
escribir el .puml. PlantUML usa el stem del .puml file como
nombre default → `{hash}.svg` correcto. Re-ejecutado: 41/42
renderizados, 1 falso positivo aceptado.

### Phase 11 TRACK

Build strict de verificacion: **EXIT=0, 0 warnings, 3 misses**.

## Added

- 211 SVGs hash-named en `source/_generated_diagrams/`.
- `execute/build-logs/prerender-{ISO}.log` (4 corridas).
- `execute/build-logs/sphinx-strict-post-prerender-2026-05-06T00-52-22.log`.
- Este changelog.

## Changed / Fixed

- `scripts/prerender-plantuml.py`:
  1. Removido `-cfgfile` (causaba "Syntax Error" SVGs).
  2. Agregada validacion defensiva contra SVGs con "Syntax Error".
  3. Strip de `@startuml NAME` antes de escribir `.puml` para
     forzar output al hash filename.

## Removed

- N/A.

## Known issues residuales

### 3 cache misses en runtime build

Diagramas que no fueron pre-renderizados:

```
base-cognitiva/_uml/uml-12-diagramas-componentes/una-pagina-web-con-un-applet-java
base-cognitiva/plantuml-guide/ejemplos/test-component-diagram
base-cognitiva/plantuml-guide/ejemplos/test-uc-diagram
```

Hipotesis: el hash computado en runtime difiere del que el script
calcula para esos casos especificos (probablemente por estructura
inusual de los bloques o normalizacion de indentacion). Investigar
en WP separado si se desea llevar el cache al 100%.

### 1 falso positivo conocido en prerender

`source/normativa/gobernanza/adr-gob-002-plantuml-para-diagramas.rst`
contiene multiples `@startuml` dentro de bloques `.. code:: text`
(ejemplos de sintaxis PlantUML, no diagramas reales). El regex del
script extrae estos bloques erroneamente, pero a runtime sphinx los
trata como code-blocks sin invocar PlantUML, asi que sin impacto
real en el build.

Mejora futura: el script deberia parsear `.. uml::` directives
explicitamente en lugar de buscar `@startuml..@enduml` con regex
naive.

### 35 legacy descriptive-named SVGs

`source/_generated_diagrams/` contiene 35 SVGs nombrados
descriptivamente (e.g. `IACT-Architecture.svg`,
`UC-BACK-001-login-usuario.svg`). Son artefactos de un workflow
previo, no usados por el cache hash-named actual. No afectan al
build pero ocupan espacio. Limpieza opcional en WP separado.

## Verified

- 211 SVGs nuevos validados (0 contienen "Syntax Error").
- Build strict post-prerender: EXIT=0, 0 warnings.
- Hit rate: 99.7% (1162/1165).
- WP siguio R-1..R-5 de `.claude/rules/long-running-commands.md`:
  todos los prerenders en background, monitor con grep
  line-buffered, logs persistidos en `execute/build-logs/`.

## Status de promocion a CHANGELOG.md raiz

Aplicable cuando se haga merge a main con bump de version. Las
3 mejoras al script (R-1, R-2, R-3) y los 211 SVGs cacheados son
cambios sustantivos al artefacto del proyecto.

## WPs sucesores derivados

1. `prerender-script-uml-directive-parser` — reemplazar regex
   naive por parser de `.. uml::` directives. Eliminaria el falso
   positivo de adr-gob-002 (low priority).
2. `prerender-cache-runtime-hash-debug` — investigar las 3 hash
   discrepancies entre prerender y runtime (low priority).
3. `legacy-svg-cleanup` — eliminar los 35 descriptive-named SVGs
   no usados (low priority, optional).

## Refs

- WP que registro la necesidad: `2026-05-06-00-11-02-plantuml-cached-effectiveness-audit`.
- WP de la causa raiz socket: `2026-05-06-00-31-12-api-socket-error-investigation`.
- Reglas operacionales seguidas: `.claude/rules/long-running-commands.md`.
- Build strict log: `execute/build-logs/sphinx-strict-post-prerender-2026-05-06T00-52-22.log`.
- Commits: `f10631c7` (fix cfgfile), `06ca12be` (fix NAME strip), `255fab7d` (211 SVGs).
