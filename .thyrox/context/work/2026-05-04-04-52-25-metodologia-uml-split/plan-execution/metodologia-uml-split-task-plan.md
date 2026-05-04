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

- [ ] **T-001** Split `diagramas-secuencias.rst` (45 diagramas)
  - Crear `diagramas-secuencias/` + 45 archivos individuales
- [ ] **T-002** Split `relaciones-uml.rst` (31)
- [ ] **T-003** Split `analisis-dominio.rst` (31)
- [ ] **T-004** Split `diagramas-distribucion.rst` (29)
- [ ] **T-005** Split `diagramas-estados.rst` (21)
- [ ] **T-006** Split `diagramas-colaboraciones.rst` (21)
- [ ] **T-007** Split `diagramas-componentes.rst` (20)
- [ ] **T-008** Split `agregacion-interfaces.rst` (17)
- [ ] **T-009** Split `orientacion-objetos.rst` (15)
- [ ] **T-010** Split `casos-uso-diagramas.rst` (12)
- [ ] **T-011** Split `diagramas-uml.rst` (10)
- [ ] **T-012** Split `diagramas-actividades.rst` (7)
- [ ] **T-013** Split `patrones-diseno.rst` (6)
- [ ] **T-014** Split `casos-uso-especificacion.rst` (2)
- [ ] **T-015** Actualizar `_metodologia-aplicacion/index.rst`
- [ ] **T-016** Commit: "Split metodologia-aplicacion multi-diagram files"

---

## Bloque B — base-cognitiva/_uml (14 archivos)

- [ ] **T-017** Split `uml-02-orientacion-objetos.rst` (19)
- [ ] **T-018** Split `uml-04-uso-relaciones.rst` (16)
- [ ] **T-019** Split `uml-03-uso-orientacion-objetos.rst` (15)
- [ ] **T-020** Split `uml-10-diagramas-colaboraciones.rst` (13)
- [ ] **T-021** Split `uml-09-diagramas-secuencias.rst` (12)
- [ ] **T-022** Split `uml-01-introduccion.rst` (12)
- [ ] **T-023** Split `cuando-usar-cada-diagrama.rst` (12)
- [ ] **T-024** Split `uml-07-diagramas-casos-uso.rst` (7)
- [ ] **T-025** Remaining files con 2-5 diagramas
- [ ] **T-026** Actualizar `base-cognitiva/_uml/index.rst`
- [ ] **T-027** Commit: "Split base-cognitiva/_uml multi-diagram files"

---

## Bloque C — uc-inc-rpt-01 completeness (5 partes faltantes)

- [ ] **T-028** Crear `flujos-alternos.rst` para uc-inc-rpt-01
- [ ] **T-029** Crear `excepciones.rst`
- [ ] **T-030** Crear `requisitos-no-funcionales.rst`
- [ ] **T-031** Crear `datos-involucrados.rst`
- [ ] **T-032** Crear `patrones-diseno.rst`
- [ ] **T-033** Actualizar `uc-inc-rpt-01/index.rst` toctree
- [ ] **T-034** Commit: "Complete uc-inc-rpt-01 spec (12/12 parts)"

---

## Orden de ejecución

```
A (T-001..T-016) → B (T-017..T-027) → C (T-028..T-034)
```

Cada bloque = 1 commit. Push al final de cada bloque.
