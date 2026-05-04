```yml
created_at: 2026-05-04 04:52:25
project: IACT-docs
work_package: 2026-05-04-04-52-25-metodologia-uml-split
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Pendiente
```

# Task Plan — Split Diagramas en _metodologia y base-cognitiva

Dividir archivos con múltiples diagramas en archivos individuales con
nombres auto-descriptivos.

---

## Bloque A — _metodologia-aplicacion (15 archivos)

- [x] **T-001** Split `diagramas-secuencias.rst` (45 diagramas) → 41 archivos
- [x] **T-002** Split `relaciones-uml.rst` (31) → 28 archivos
- [x] **T-003** Split `analisis-dominio.rst` (31) → 27 archivos
- [x] **T-004** Split `diagramas-distribucion.rst` (29) → 18 archivos
- [x] **T-005** Split `diagramas-estados.rst` (21) → 21 archivos
- [x] **T-006** Split `diagramas-colaboraciones.rst` (21) → 21 archivos
- [x] **T-007** Split `diagramas-componentes.rst` (20) → 16 archivos
- [x] **T-008** Split `agregacion-interfaces.rst` (17) → 17 archivos
- [x] **T-009** Split `orientacion-objetos.rst` (15) → 14 archivos
- [x] **T-010** Split `casos-uso-diagramas.rst` (12) → 12 archivos
- [x] **T-011** Split `diagramas-uml.rst` (10) → 14 archivos
- [x] **T-012** Split `diagramas-actividades.rst` (7) → 6 archivos
- [x] **T-013** Split `patrones-diseno.rst` (6) → 6 archivos
- [x] **T-014** Split `casos-uso-especificacion.rst` (2) → 2 archivos
- [x] **T-015** Actualizar `_metodologia-aplicacion/index.rst`
- [x] **T-016** Commit: "Split metodologia-aplicacion multi-diagram files"

---

## Bloque B — base-cognitiva/_uml (14 archivos)

- [x] **T-017** Split `uml-02-orientacion-objetos.rst` (19) → 9 archivos
- [x] **T-018** Split `uml-04-uso-relaciones.rst` (16) → 12 archivos
- [x] **T-019** Split `uml-03-uso-orientacion-objetos.rst` (15) → 7 archivos
- [x] **T-020** Split `uml-10-diagramas-colaboraciones.rst` (13) → 12 archivos
- [x] **T-021** Split `uml-09-diagramas-secuencias.rst` (12) → 8 archivos
- [x] **T-022** Split `uml-01-introduccion.rst` (12) → 12 archivos
- [x] **T-023** Split `cuando-usar-cada-diagrama.rst` (12) → 12 archivos
- [x] **T-024** Split `uml-07-diagramas-casos-uso.rst` (11) → 10 archivos
- [x] **T-025** Split remaining files (uml-05..13 restantes) → totales
- [x] **T-026** Actualizar `base-cognitiva/_uml/index.rst`
- [x] **T-027** Commit: "Split base-cognitiva/_uml multi-diagram files"

---

## Bloque C — uc-inc-rpt-01 completeness (5 partes faltantes)

- [x] **T-028** Crear `flujos-alternos.rst` para uc-inc-rpt-01
- [x] **T-029** Crear `excepciones.rst`
- [x] **T-030** Crear `requisitos-no-funcionales.rst`
- [x] **T-031** `datos-involucrados.rst` ya existia — verificado
- [x] **T-032** Crear `patrones-diseno.rst`
- [x] **T-033** Actualizar `uc-inc-rpt-01/index.rst` toctree
- [ ] **T-034** Commit: "Complete uc-inc-rpt-01 spec (12/12 parts)"

---

## Orden de ejecución

```
A (T-001..T-016) → B (T-017..T-027) → C (T-028..T-034)
```

Cada bloque = 1 commit. Push al final de cada bloque.
