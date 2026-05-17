```yml
created_at: 2026-05-04 20:08:37
project: THYROX
work_package: 2026-05-04-20-08-37-plantuml-syntax-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# R-10 — PlantUML Syntax Errors

## Origen

Build log `b75ert8rr`: 3 archivos con `error while running plantuml /
Syntax Error?`:

```
arquitectura-tecnica/modulos/user-identity/diagramas/clases-modulo-identidad.rst
  b'ERROR\n13\nSyntax Error?...'
requisitos/casos-uso/auth/uc-auth-01/datos-involucrados.rst
  b'ERROR\n19\nSyntax Error?...'
base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/proceso-definicion-arquitectonica.rst
  b'ERROR\n21\nSyntax Error?...'
```

## Diagnóstico — ejecución directa con PlantUML jar

Cada bloque fue extraído y ejecutado con `java -jar tools/plantuml.jar`
para obtener el número de línea exacto dentro del diagrama.

### Causa A — enum con separador `/` inválido (PROVEN)

`clases-modulo-identidad.rst` y `datos-involucrados.rst`: enums definidos
con valores separados por `/` en una sola línea:

```plantuml
enum UserState { ACTIVE / INACTIVE / BLOCKED }   ← INVÁLIDO
```

PlantUML no acepta `/` como separador de valores de enum. La sintaxis
correcta es un valor por línea dentro de `{ }`:

```plantuml
enum UserState {
  ACTIVE
  INACTIVE
  BLOCKED
}
```

### Causa B — label vacío en `rectangle ""` + flecha `<-->` inválida (PROVEN)

`proceso-definicion-arquitectonica.rst` bloque 1 (`uml14-tres-picos`):

1. `rectangle "" as MidLabel #White` — label vacío hace que PlantUML
   falle al resolver referencias a elementos internos en flechas.
   Fix: `rectangle " " as MidLabel` (espacio en lugar de vacío).

2. `<-->` no es una flecha válida en PlantUML. La bidireccional correcta
   es `<->`.

## Inventario — 3 archivos

| Archivo | Causa | Fix |
|---------|-------|-----|
| `user-identity/diagramas/clases-modulo-identidad.rst` | A | enum multi-línea |
| `uc-auth-01/datos-involucrados.rst` | A | enum multi-línea |
| `uml-14-.../proceso-definicion-arquitectonica.rst` | B | `""` → `" "` + `<-->` → `<->` |

## Verificación post-fix (PROVEN)

Script Python ejecutó PlantUML jar sobre cada bloque — los 3 archivos
retornan exit code 0.

Build post-fix: `build succeeded, 1 warning` (el warning de inline
emphasis en `proceso-definicion-arquitectonica.rst:486` es pre-existente,
no relacionado con PlantUML).

## Build logs

- `logs/build-after-fix-2026-05-04T200900.txt`
