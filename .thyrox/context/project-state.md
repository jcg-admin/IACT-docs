```yml
type: Dashboard de Proyecto
category: Estado Actual
project: IACT-docs
version: 1.0.0
created_at: 2026-04-23 08:45:00
updated_at: 2026-04-23 08:45:00
purpose: Dashboard del proyecto IACT-docs — estado actual y navegación
```

# Project State — IACT-docs

## Status General

**Proyecto:** IACT-docs — Documentación del Sistema IACT  
**ÉPICA:** 1 — config-review-iact-docs  
**Versión:** 1.0.0  
**Estado:** En desarrollo — Phase 1 DISCOVER completada  
**WP actual:** `.thyrox/context/work/2026-04-23-07-04-55-config-review-iact-docs/`  
**Rama activa:** `feature/project-setup`  
**Última actualización:** 2026-04-23 08:45:00

**Hito actual:**
- Phase 1 DISCOVER completada (2026-04-23)
- Hallazgos: 4 contradicciones críticas, 7 claims sin fuente, 5 lagunas críticas
- Calibración epistémica global: 0.71 (PARCIALMENTE CALIBRADO)
- Próximo: Phase 3 DIAGNOSE (root cause analysis)

---

## Tech Stack — IACT-docs

### Documentación
- **Sphinx:** v8.2.3 (core)
- **Tema:** Furo 2025.9.25
- **Parsers:** MyST (Markdown + reStructuredText)
- **Language:** Spanish (es)

### Python Stack
- **Runtime:** Python 3.11+
- **Dependencies:** 86 paquetes en requirements.txt
- **Key packages:** Babel, Jinja2, Pygments, PyYAML, requests

### Sphinx Extensions (16 activas)
1. sphinx.ext.intersphinx — Referências cruzadas
2. sphinx.ext.todo — Tareas pendientes
3. sphinx.ext.coverage — Cobertura de documentación
4. sphinx.ext.mathjax — Matemáticas
5. sphinx.ext.autodoc — Documentación desde docstrings
6. sphinx.ext.autosummary — Resúmenes automáticos
7. sphinx.ext.viewcode — Enlaces a código fuente
8. sphinx.ext.napoleon — Soporte Google/NumPy docstrings
9. sphinx_autodoc_typehints — Type hints en docs
10. sphinx_design — Componentes de diseño
11. sphinx_copybutton — Botones copiar código
12. sphinx_tabs.tabs — Pestañas tabuladas
13. sphinx_toolbox.collapse — Elementos colapsables
14. notfound.extension — Página 404 personalizada
15. myst_parser — Parser MyST
16. sphinx-prompt — Prompts de consola

### UML & Diagramming
- No actualmente integrado
- Considerado: sphinx-uml, sphinxcontrib-plantuml

---

## Framework Infrastructure — THYROX (heredado)

Este proyecto usa el framework THYROX para gestión de work packages y metodología.

### 28 Agentes Nativos (Framework agents)

Disponibles pero no todos usados en IACT-docs:
- `agentic-reasoning` — Razonamiento profundo multi-paso
- `agentic-validator` — Validación contra guidelines
- `ba-coordinator`, `bpa-coordinator`, `cp-coordinator`, `dmaic-coordinator`, `lean-coordinator`, `pdca-coordinator`, `pm-coordinator`, `pps-coordinator`, `rm-coordinator`, `rup-coordinator`, `sp-coordinator`, `thyrox-coordinator` — Coordinadores de metodologías
- `deep-dive` — Análisis profundo exhaustivo
- `deep-review` — Análisis de cobertura entre fases
- `diagrama-ishikawa` — Análisis de causa raíz
- `mysql-expert`, `nodejs-expert`, `postgresql-expert`, `react-expert`, `webpack-expert` — Tech-experts (NO usados en IACT-docs)
- `pattern-harvester` — Extrae patrones recurrentes
- `skill-generator` — Genera skills para tecnologías
- `task-executor` — Ejecuta tareas atómicas
- `task-planner` — Descompone trabajo en tareas
- `task-synthesizer` — Sintetiza resultados paralelos
- `tech-detector` — Detecta stack tecnológico

**Para IACT-docs:** Primariamente usados `task-planner`, `deep-dive`, `agentic-reasoning` en Phase 1 DISCOVER.

### 11 Metodologías Soportadas (Available but not used)

El framework THYROX soporta:
- PDCA, DMAIC, RUP, RM, PMBOK, BABOK, Lean, PPS, SP, CP, BPA

**Para IACT-docs:** Actualmente usando solo el ciclo THYROX base (12 stages). Las metodologías adicionales están disponibles pero no son necesarias para este proyecto.

### Scripts de Gestión (Framework infrastructure)

Ubicación: `.claude/scripts/thyrox/`

- `session-start.sh` — Inicialización de sesión (hook)
- `validate-session-close.sh` — Validación de cierre de WP
- `validate-phase-readiness.sh` — Validación de readiness por fase
- `update-state.sh` — Regeneración de estado
- `lint-agents.py` — Validación de formato de agentes

**Para IACT-docs:** Se heredan estos scripts del framework. Son necesarios para que Phase 1→3→5→6→8→10→11 funcione correctamente.

---

## Deuda Técnica y Próximos Pasos

Ver `.thyrox/context/technical-debt.md` para lista detallada de TDs.

**Alta prioridad:**
- TD-001: Limpiar git history (información sensible)
- TD-006: Implementar CI/CD pipeline
- TD-007: Plan remediación Phase 3 DIAGNOSE

**Documentación necesaria:**
- TD-002: ADR sobre información sensible
- TD-004: Estructura de directorios
- TD-005: Validación de extensiones Sphinx

---

## Métricas del Proyecto

| Métrica | Valor | Nota |
|---------|-------|------|
| Versión | 1.0.0 | En desarrollo |
| Extensiones Sphinx | 16 | 14 funcionales, 2 comentadas |
| Dependencias Python | 86 | En requirements.txt |
| TDs abiertos | 7 | IACT-docs specific |
| Fases completadas | Phase 1 DISCOVER | Próxima: Phase 3 DIAGNOSE |
| Calibración epistémica | 0.71 | PARCIALMENTE CALIBRADO |

---

**Ubicación:** `.thyrox/context/project-state.md`  
**Alcance:** Proyecto IACT-docs (feature/project-setup branch)  
**Última calibración:** 2026-04-23
