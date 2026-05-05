```yml
created_at: 2026-05-02 06:30:00
project: IACT-docs
work_package: 2026-05-02-05-22-01-arq-mod-plantuml-diagrams
phase: Phase 10 — EXECUTE
author: NestorMonroy
status: Cerrado
```

# Changelog — arq-mod-plantuml-diagrams

## Added

- `arq-mod-001-auth.rst` — Sección 9: diagrama PlantUML de secuencia (flujo login)
- `arq-mod-001-auth.rst` — Sección 11: diagrama PlantUML de componentes (dependencias módulo)
- `arq-mod-002-user-identity.rst` — Sección 9: diagrama PlantUML de estado (ciclo de vida usuario, BR-009)
- `arq-mod-003-rbac-core.rst` — Sección 9: diagrama PlantUML de actividad (precedencia permisos)
- `arq-mod-003-rbac-core.rst` — Sección 10: diagrama PlantUML de actividad (verificación SoD)
- `arq-mod-004-etl-monitoring.rst` — Sección 9: diagrama PlantUML de secuencia con Actor Tiempo (ventana ETL)
- `arq-mod-005-vis-reports.rst` — Sección 4: diagrama PlantUML de actividad (flujo de acceso/exportación)
- `arq-mod-006-alerts.rst` — Sección 11 (nueva): diagrama PlantUML de estado (ciclo de vida alerta, CNST-001)
- `arq-mod-007-audit.rst` — Sección 11 (nueva): diagrama PlantUML de secuencia (emisión evento auditoría)
- `arq-mod-008-sys-logs.rst` — Sección 13 (nueva): diagrama PlantUML de actividad (ciclo health check)

## Changed

- `arq-mod-006-alerts.rst` — "11. Historial" renumerado a "12. Historial de Cambios"
- `arq-mod-007-audit.rst` — Secciones 11-12 renumeradas a 12-13 tras inserción
- `arq-mod-008-sys-logs.rst` — "13. Historial" renumerado a "14. Historial de Cambios"

## Decisiones de Diseño

**D-01: Actor Tiempo en diagramas UML**

El Actor Tiempo (UML-06) dispara eventos periódicos asincrónicos en el sistema.
En diagramas de secuencia se declara como `actor "Tiempo\n(...)" as T`.
En diagramas de actividad, se embebe la referencia en el primer paso de actividad
porque la sintaxis de `actor` no es válida en activity diagrams de PlantUML.

**D-02: Diagramas de estado para ciclos de vida**

Se eligieron state diagrams (no activity diagrams) para modelar BR-009 (soft delete)
y el ciclo de alertas porque el patrón es de estados nombrados con transiciones
condicionadas — más legible que un activity diagram para estos casos.

**D-03: Limitación de sintaxis PlantUML en activity diagrams**

`note "..." as N` (floating note syntax) no está soportada en activity diagrams
de sphinxcontrib-plantuml 0.26. Se usó el texto del paso de actividad para
incluir referencias contextuales (Actor Tiempo, restricciones).

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a `main` con bump de versión.
Entrada candidata: "Add PlantUML behavioral diagrams to all 8 architecture modules"
