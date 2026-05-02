```yml
project: IACT-docs
work_package: 2026-05-02-05-22-01-arq-mod-plantuml-diagrams
created_at: 2026-05-02 05:22:01
current_phase: Phase 8 — PLAN EXECUTION
status: Activo
author: NestorMonroy
flow: thyrox
methodology_step: thyrox:execute
predecessor_wp: 2026-05-02-04-58-38-arq-tecnica-abstraccion
branch: feature/arquitectura-tecnica-content
```

# WP — Diagramas PlantUML para módulos arquitectónicos

## Motivo

Los módulos en `source/arquitectura-tecnica/modulos/` describen
comportamiento mediante diagramas ASCII art (`.. code-block:: text`).
Esto viola la convención del proyecto (ADR-GOB-006, UML-06..UML-12):
los diagramas deben ser PlantUML (`.. uml::`).

Además, los módulos 006, 007 y 008 no tienen ningún diagrama.

## Principios guía (base-cognitiva/_uml)

- **UML-06**: cada UC se inicia por persona, sistema, hardware o
  **tiempo** — el actor "Tiempo" debe aparecer donde corresponda.
- **UML-08**: diagrama de estados para ciclo de vida de objetos.
- **UML-09**: diagrama de secuencias para interacciones entre objetos.
- **UML-11**: diagrama de actividades para flujos de proceso.
- **UML-12**: diagramas de componentes para estructura física.

## Convención de diagramas del proyecto

```rst
.. uml::
 :caption: Descripción en español — sin tecnología concreta.

 @startuml

 ' contenido PlantUML
 @enduml
```

## Alcance

| Módulo | Acción | Tipo UML |
|--------|--------|----------|
| arq-mod-001-auth | Reemplazar ASCII art flujo login + contexto | Secuencia + Contexto |
| arq-mod-002-user-identity | Reemplazar ASCII art estados usuario | Estado (UML-08) |
| arq-mod-003-rbac-core | Reemplazar ASCII art precedencia + SoD | Actividad (UML-11) |
| arq-mod-004-etl-monitoring | Reemplazar ASCII art flujo ETL | Actividad + Actor Tiempo |
| arq-mod-005-vis-reports | Reemplazar ASCII art flujo acceso | Actividad (UML-11) |
| arq-mod-006-alerts | Agregar diagrama ciclo de vida alerta | Actividad (UML-11) |
| arq-mod-007-audit | Agregar diagrama emisión evento auditoría | Secuencia (UML-09) |
| arq-mod-008-sys-logs | Agregar diagrama health check | Actividad (UML-11) |

## Tareas

Ver `plan-execution/arq-mod-plantuml-diagrams-task-plan.md`
