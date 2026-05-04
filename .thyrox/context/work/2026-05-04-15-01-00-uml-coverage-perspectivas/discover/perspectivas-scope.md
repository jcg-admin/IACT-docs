```yml
created_at: 2026-05-04 15:02:00
project: THYROX
work_package: 2026-05-04-15-01-00-uml-coverage-perspectivas
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# WP-4: uml-coverage-perspectivas — Scope

## Problema

`perspectivas-arquitectonicas.rst` define el grid perspectiva × vista para IACT
(Security, Regulation, Availability, Performance, Evolution × 6 vistas) y prescribe
"aplicar perspectivas a vistas" para validar calidad. No existe ningún documento de
perspectiva en `arquitectura-tecnica/`.

## Prescripción base-cognitiva

- `perspectivas-arquitectonicas.rst`: "Aplicar perspectivas a vistas para analizar y
  validar sus cualidades y para impulsar la toma de decisiones arquitectónicas adicionales"
- Resultado esperado: Insights, Mejoras, Artefactos (modelos de valor duradero)
- Las perspectivas NO son vistas separadas — son análisis transversales sobre las vistas existentes

## Alcance del WP

1. **Crear `arquitectura-tecnica/perspectivas/index.rst`** — índice de perspectivas aplicadas
2. **Crear un documento por perspectiva** (solo las de relevancia ALTA para IACT):
   - `perspectiva-security.rst` — Security perspective: RBAC enforcement, JWT, control de acceso a datos IVR, distribución de credenciales
   - `perspectiva-regulation.rst` — Regulation perspective: auditoría regulatoria, trazabilidad de acciones ciudadanas, CNST-029..033
   - `perspectiva-availability.rst` — Availability & Resilience: pipeline ETL failure isolation (P-04), redundancia, recovery procedures
3. **No crear perspectivas de baja relevancia**: Performance y Evolution se documentan con
   una nota de cobertura (parcialmente cubiertas en implementation-view/ y design-view/)
4. **Actualizar `arquitectura-tecnica/index.rst`** si existe referencia a perspectivas

## Criterios de aceptación

- [ ] 3 documentos de perspectiva creados (Security, Regulation, Availability)
- [ ] Cada documento referencia explícitamente qué vistas afecta y cómo
- [ ] Referencias cruzadas a `perspectivas-arquitectonicas.rst`
- [ ] Build verde sin warnings nuevos

## Prioridad

MEDIA — ejecutar después de WP-1 (context-view) y WP-3 (housekeeping).
