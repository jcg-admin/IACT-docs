```yml
created_at: 2026-05-02 05:32:56
project: IACT-docs
work_package: 2026-05-02-05-32-56-arq-mod-cajones
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Activo
branch: feature/arquitectura-tecnica-content
```

# WP — Reestructuración de módulos arquitectónicos en cajones

## Objetivo

Reorganizar los 8 módulos `arq-mod-*.rst` (actualmente archivos planos) en
subdirectorios por módulo, siguiendo el mismo patrón de `source/requisitos/casos-uso/`.

Cada módulo se convierte en un "cajón" con:
- `index.rst` — propósito, alcance, toctree interno
- `responsabilidades.rst` — puede/no puede hacer
- `dependencias.rst` — depende de / es requerido por
- `componentes.rst` — técnicos, modelos de datos, APIs expuestas
- `restricciones.rst` — CNSTs aplicables
- `casos-uso.rst` — UCs asociados + FRs derivados
- `diagramas.rst` — diagramas PlantUML

## Estructura objetivo

```
source/arquitectura-tecnica/modulos/
├── index.rst                  ← toctree → auth/index, user-identity/index, ...
├── auth/
│   ├── index.rst              ← ARQ_MOD_001 overview
│   ├── responsabilidades.rst
│   ├── dependencias.rst
│   ├── componentes.rst
│   ├── restricciones.rst
│   ├── casos-uso.rst
│   └── diagramas.rst
├── user-identity/
│   ├── index.rst
│   └── ...
├── rbac-core/
├── etl-monitoring/
├── vis-reports/
├── alerts/
├── audit/
└── sys-logs/
```

## Trazabilidad (Sphinx references)

Cada archivo usa `:doc:` y `:ref:` para referencias cruzadas dentro de `source/`.
Ejemplo: `:doc:`/requisitos/casos-uso/auth/index`` vincula UCs referenciados.
Los archivos en `.thyrox/`, `temp-holding/`, `source/base-cognitiva/` NO reciben
referencias.
