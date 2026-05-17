```yml
created_at: 2026-05-04 19:36:59
project: THYROX
work_package: 2026-05-04-19-36-59-duplicate-labels-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# R-05 — Duplicate Label Warnings (autosectionlabel)

## Origen

Build post-R-04 (PROVEN — partial log en WP `2026-05-04-19-05-53-title-overlines-fix/logs/`)
produjo 33 advertencias `duplicate label`. Dos patrones distintos.

## Causa raíz

### Patrón 1 — 32 archivos de diagrama (*/diagramas/*.rst)

Todos los archivos siguen la misma estructura plantilla:

```rst
.. meta::
 ...

.. _arq_mod_XXX_label:

=================
Título del Diagrama      <- heading del documento (lines 15-17)
=================

Título del Diagrama      <- DUPLICADO (lines 19-20, mismo texto)
=================

.. uml::
 ...
```

`autosectionlabel` genera el label `path/file:título` para CADA sección
encontrada. Al haber dos secciones con el mismo texto, genera el mismo label
dos veces → `duplicate label` warning.

La segunda aparición del título (lines 19-21) fue incorporada al template
del WP que creó estos archivos, probablemente como separador visual. No
tiene función estructural — el contenido del diagrama sigue directamente.

**Fix:** Eliminar lines 19-21 (título + underline + blank) de los 32 archivos.

### Patrón 2 — 1 archivo especial

`domain-model/overview.rst` contenía `.. _modelo-dominio-iact:` como label
explícito. El mismo label ya existe en `modelo-dominio-iact.rst:12`.

Sphinx no permite dos documentos con el mismo label explícito. La colisión
ocurrió porque `overview.rst` fue creado como documento paraguas que embebió
el contenido de `modelo-dominio-iact.rst` incluyendo su label.

**Fix:** Renombrar el label en `overview.rst` a `.. _overview-modelo-dominio-iact:`
para preservar la capacidad de hacer `:ref:` al overview, sin colisionar con
el canonical `modelo-dominio-iact.rst`.

## Inventario

### Patrón 1 — 32 archivos (líneas 19-21 eliminadas)

| Módulo | Archivo |
|--------|---------|
| alerts | ciclo-vida-alerta.rst, componentes-mod-alerts.rst, secuencia-disparo-alerta-br016.rst |
| audit | componentes-mod-audit.rst, estados-exportacion-audit.rst, flujo-emision-evento-auditoria.rst |
| auth | diagrama-contexto-dependencias.rst, flujo-autenticacion.rst |
| caller | flujo-llamante-ivr.rst |
| etl-monitoring | componentes-mod-pipeline.rst, flujo-etl-nocturno.rst, sub-estados-proceso-etl.rst |
| operator | ciclo-vida-estado-agente.rst, componentes-mod-operator.rst, secuencia-atencion-llamada-entrante.rst |
| rbac-core | evaluacion-conflicto-sod.rst, precedencia-permisos.rst |
| supervision | barge-in-intervencion-tripartita.rst, componentes-mod-supervision.rst, flujo-monitoreo-tiempo-real.rst |
| sys-logs | componentes-mod-logs.rst, flujo-health-check.rst, secuencia-consulta-logs-sistema.rst |
| user-identity | ciclo-vida-usuario.rst, clases-modulo-identidad.rst, secuencia-creacion-usuario.rst |
| vis-reports | componentes-mod-reports.rst, flujo-acceso-visualizaciones.rst, secuencia-sp-rpt-flujo-completo.rst |
| rbac/modelo-rbac-iact/diagramas | ciclo-vida-asignacion.rst, clases-entidades-rbac.rst, flujo-enforcement-rbac.rst |

### Patrón 2 — 1 archivo

- `arquitectura-tecnica/domain-model/overview.rst` — label `modelo-dominio-iact`
  renombrado a `overview-modelo-dominio-iact`

## Método de corrección (PROVEN)

Script Python `fix_duplicate_labels.py` ejecutado en `/tmp/`:
- Patrón 1: verifica que line 16 (título doc) == line 19 (dup título), luego
  `del lines[18:21]` (título + underline + blank)
- Patrón 2: `str.replace` del label conflictivo en `overview.rst`

Resultado: 33/33 instancias corregidas en 33 archivos.

## Build logs

- `logs/build-after-fix-*.txt` — build post-fix: esperado 0 duplicate label warnings
