```yml
created_at: 2026-05-02 02:34:35
project: IACT-docs
work_package: 2026-05-02-02-34-35-plantuml-warnings-fix
phase: Phase 11 — TRACK
author: NestorMonroy
status: Cerrado
```

# Changelog — plantuml-warnings-fix

## Fixed

- Removidas líneas `!include plantuml-styles.puml` de 42 archivos RST
  en base-cognitiva, normativa, requisitos/_metodologia-aplicacion
  (sphinxcontrib-plantuml escribe a /tmp/ — paths relativos no resuelven)

- `source/conf.py`: agregado `plantuml_cfg_file` con path absoluto
  al styles file (silenciosamente ignorado por sphinxcontrib-plantuml
  0.26 — el fix efectivo son los !include removidos)

- `source/requisitos/casos-uso/operator/uc-opr-03/patrones-diseno.rst`:
  bullet list sin línea en blanco → agregada línea en blanco (W-01)

- `source/requisitos/casos-uso/operator/uc-opr-07/patrones-diseno.rst`:
  bullet list sin línea en blanco → agregada línea en blanco (W-02)

- `source/requisitos/casos-uso/permissions/uc-perm-03/diagramas-uml.rst`:
  mensaje de secuencia multi-línea RST → combinado con `\n` (W-08)

- `source/requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml.rst`:
  tres labels multi-línea (sequence + activity) → combinados con `\n` (W-09)

- `source/requisitos/casos-uso/users/uc-usr-03/diagramas-uml.rst`:
  label activity multi-línea + cinco `:action; stop` antes de
  partition block → label combinado + stops en línea separada (W-10)

- `source/requisitos/casos-uso/access/uc-acc-01/diagramas-uml.rst`:
  dos labels activity multi-línea en diagrama SoD → combinados (W-06)

- `source/arquitectura-tecnica/modelo-dominio-iact.rst`:
  removidos 9 `!include` + expandidos 12 inline enums a syntax
  multilínea (PlantUML 1.2024.7 no soporta inline enum en class
  diagrams) (W-05)

- `source/requisitos/casos-uso/access/uc-acc-05/diagramas-uml.rst`:
  label multi-línea en state transition (diagrama 4) → combinado
  con `\n` (W-07)

- `scripts/setup.sh`: agregado paso 3/7 para instalar graphviz
  (apt/brew) — requerido por PlantUML para use-case y class diagrams
  (D-02/D-08)

- `scripts/setup.sh`: renumerados pasos 1/6..6/6 → 1/7..7/7

## Added

- `.thyrox/context/work/2026-05-02-02-34-35-plantuml-warnings-fix/execute/scripts/diagnose-plantuml-diagrams.py`:
  script para extraer y testear diagramas PlantUML en archivos RST

- `.thyrox/context/work/2026-05-02-02-34-35-plantuml-warnings-fix/execute/scripts/fix-modelo-dominio.py`:
  script para remover !include y expandir inline enums en modelo-dominio-iact.rst

## Status de promoción a CHANGELOG.md raíz

No aplica bump de versión en esta iteración — cambios son correcciones
de warnings de build, sin cambios de funcionalidad pública.
Promover en el próximo release que incluya contenido nuevo.
