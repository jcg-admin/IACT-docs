```yml
created_at: 2026-05-02 05:22:01
project: IACT-docs
work_package: 2026-05-02-05-22-01-arq-mod-plantuml-diagrams
phase: Phase 10 — EXECUTE
author: NestorMonroy
status: Completado
```

# Task Plan — PlantUML diagrams para módulos arquitectónicos

## Principio

Reemplazar/agregar diagramas PlantUML (`.. uml::`) en los 8 módulos
arquitectónicos. El diagrama describe **comportamiento observable**
(actores, flujos, estados) — nunca tecnología concreta.

Tipo de diagrama según contexto (UML-06..UML-12):
- **Flujo de operación entre módulos**: diagrama de secuencias (UML-09)
- **Ciclo de vida de un objeto**: diagrama de estados (UML-08)
- **Proceso con decisiones/bifurcaciones**: diagrama de actividades (UML-11)
- **Actor Tiempo**: representado explícitamente donde hay eventos programados

---

## T-001 — arq-mod-001-auth.rst

Reemplazar sección 9 "Flujo de Autenticacion" (ASCII art → secuencia UML-09):
- [x] Participantes: Interfaz, ServicioAuth, RepositorioUsuarios
- [x] Flujo principal: POST /login → validar → crear sesión → 200 + token
- [x] Actor Tiempo implícito en timeout (anotación en diagrama)
- [x] Reemplazar sección 11 "Diagrama de Contexto" (ASCII art → componentes)

## T-002 — arq-mod-002-user-identity.rst

Reemplazar sección 9 "Estados del Usuario" (ASCII art → estados UML-08):
- [x] Estados: PENDIENTE_CONFIGURACION, ACTIVO, INACTIVO, BLOQUEADO
- [x] Transiciones con condiciones en español
- [x] Punto inicial → PENDIENTE_CONFIGURACION
- [x] Punto final desde INACTIVO/BLOQUEADO (soft delete)

## T-003 — arq-mod-003-rbac-core.rst

Reemplazar sección 9 "Precedencia de Permisos" y 10 "Reglas SoD":
- [x] Diagrama de actividades para el flujo de precedencia (3 niveles)
- [x] Diagrama de actividades para la evaluación SoD

## T-004 — arq-mod-004-etl-monitoring.rst

Reemplazar sección 9 "Flujo ETL" (ASCII art → actividades UML-11):
- [x] Actor Tiempo (ventana programada CNST-006/008)
- [x] Flujo: BD operativa → ETL → BD analítica
- [x] Punto de supervisión del módulo (solo lectura)

## T-005 — arq-mod-005-vis-reports.rst

Reemplazar sección 4 "Flujo de Acceso" (ASCII art → actividades UML-11):
- [x] Flujo: usuario entra → consulta RBAC → aplica segmentos → muestra interfaz
- [x] Bifurcación: permiso 'view' vs 'export'
- [x] Validación de límites diarios (CNST_007)

## T-006 — arq-mod-006-alerts.rst

Agregar diagrama de ciclo de vida de alerta (nuevo, UML-08 o UML-11):
- [x] Diagrama de estados: PENDIENTE → ACTIVA → RECONOCIDA → RESUELTA
- [x] Transición especial para alertas de suscripción (CNST_001: buzón interno)

## T-007 — arq-mod-007-audit.rst

Agregar diagrama de emisión de evento de auditoría (nuevo, UML-09):
- [x] Secuencia: ServicioOrigen → MiddlewareAudit → RepositorioAudit
- [x] Inserción post-commit en transacción separada

## T-008 — arq-mod-008-sys-logs.rst

Agregar diagrama de health check (nuevo, UML-11):
- [x] Flujo del health check: recolectar métricas → evaluar umbrales → generar snapshot
- [x] Bifurcación: umbral OK vs umbral violado → alerta

---

## T-009 — Build y validación

- [x] `.venv/bin/sphinx-build -b html source build/html`
- [x] 0 warnings — build succeeded

## T-010 — Commit y push

- [x] Commit consolidado (T-001..T-008)
- [x] Push a `feature/arquitectura-tecnica-content`
