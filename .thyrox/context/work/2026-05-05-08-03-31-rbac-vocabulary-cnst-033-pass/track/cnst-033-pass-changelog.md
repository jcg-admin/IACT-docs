```yml
created_at: 2026-05-05 08:20:00
updated_at: 2026-05-05 08:20:00
project: IACT-docs
work_package: 2026-05-05-08-03-31-rbac-vocabulary-cnst-033-pass
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
```

# WP Changelog — RBAC Vocabulary CNST-033 Pass

## Removed

- `source/arquitectura-tecnica/domain-model/servicio-reportes.rst`
  — facade legacy en castellano (D-02). Sin lógica propia; los 5
  XxxReportService modernos son la API canónica.

## Renamed

| Antes | Después | Decisión |
|-------|---------|----------|
| `abandono-report-service.rst` / `AbandonoReportService` | `abandonment-report-service.rst` / `AbandonmentReportService` | D-03 |
| `clientes-report-service.rst` / `ClientesReportService` | `caller-report-service.rst` / `CallerReportService` | D-03 |
| `menu-ivr-report-service.rst` / `MenuIvrReportService` | `ivr-navigation-report-service.rst` / `IvrNavigationReportService` | D-03, D-04 |
| `transferencias-report-service.rst` / `TransferenciasReportService` | `transfer-report-service.rst` / `TransferReportService` | D-03 |

## Changed

- `source/arquitectura-tecnica/domain-model/index.rst` — toctree
  actualizado (4 archivos renombrados, 1 eliminado).
- `source/arquitectura-tecnica/domain-model/base-report-service.rst`
  — lista de subclases concretas con nombres en inglés.
- `source/requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/clases.rst`,
  `uc-rpt-15/...`, `uc-rpt-16/...`, `uc-rpt-17/...` — class block
  `ServicioReportes` removido + relación `XxxReportService -->
  ServicioReportes` removida + clase canónica renombrada.
- `source/requisitos/casos-uso/reports/uc-rpt-{13,15,16,17}/implementacion-tecnica.rst`
  — sección "11.4 Implementacion ServicioReportes" removida +
  bullet `- ServicioReportes` removido + métodos castellanos
  reemplazados por canónicos en inglés (D-07).
- `source/requisitos/casos-uso/reports/uc-rpt-01/diagramas-uml/diagrama-de-secuencia.rst`
  — `ServicioReportes` → `ReportingService` (rol genérico).
- `source/arquitectura-tecnica/system-view/{clases,secuencia,comunicacion}-sistema-iact.rst`
  — `ServicioReportes` → `ReportingService` (rol genérico application
  service tier).
- `source/arquitectura-tecnica/design-view/seq-reports.rst`
  — `ServicioReportes` → `ReportingService` (17 ocurrencias).
- `source/arquitectura-tecnica/modulos/vis-reports/diagramas/{componentes,secuencia}-*.rst`
  — `ServicioReportes` → `ReportingService`.
- `source/normativa/estandares/std-011-alias-diagramas-uml.rst`
  — alias `ServicioReportes` → `ReportingService`.

## Aceptado / no fixeado

- **Otros identificadores castellanos en seq-reports.rst y system-view/**
  (`InterfazReportes`, `RepositorioReport`, `AlmacenDatos`,
  `ColaProcesamiento`, `ReporteLlamadasAbandonadas`, etc.) — quedan
  fuera del scope de este WP (que ataca solo las 5 clases
  derivadas de D-11). Se registra como hallazgo para WP futuro
  `cnst-033-system-design-view-pass`.
- Catálogo `function_code` en signatures (e.g. `view_reports`,
  `export_csv`) ya está en inglés conforme CNST-033 §5 — sin
  cambios necesarios.

## Status de promoción a CHANGELOG.md raíz

Pendiente del merge a `main`. Categorías Keep a Changelog:

- **Changed**: domain-model class names AbandonoReportService,
  ClientesReportService, MenuIvrReportService,
  TransferenciasReportService renamed to English per CNST-033.
- **Removed**: ServicioReportes legacy facade (sin lógica propia).
- **Refs**: CNST-033 v2.0.0, BR-006, D-01..D-07.

## Validación

- Pre-render PlantUML en áreas impactadas: 0 errores
  (domain-model 68 ✓, uc-rpt 59 ✓, design-view 13 ✓,
  system-view 12 ✓, modulos/vis-reports 3 ✓).
- `grep -r ServicioReportes source/` → 0 matches.
- `grep -r servicio-reportes source/` → 0 matches.
