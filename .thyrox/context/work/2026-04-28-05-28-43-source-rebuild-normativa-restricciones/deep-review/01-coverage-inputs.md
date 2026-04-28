```yml
created_at: 2026-04-28 06:15:00
project: IACT-docs
work_package: 2026-04-28-05-28-43-source-rebuild-normativa-restricciones
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Deep-Review de cobertura de inputs — normativa/restricciones

**Alcance:** comparar inputs (backup canónico, FASE 02 divergente, doc maestro,
ACTUALIZACION_DEL_ARBOL, CNST_05 v2.0.0 standalone) contra `source/normativa/restricciones/`.

## Cobertura buena

1. **Backup canónico → rebuild (11 archivos):** los 10 CNST_001…CNST_010 están
   presentes con contenido equivalente (diff solo en bloque `.. meta::` añadido y
   cross-refs). CNST_012 backup → CNST_011 rebuild conforme D-CNST-1. Sin pérdida
   sustantiva.
2. **Renumeración 012→011 correcta:** título, label `_cnst-011` y tuplas
   `'CNST-011'` actualizadas; gap cerrado (D-CNST-4).
3. **Ampliaciones v1.1.0 preservadas:** "Permisos Temporales" en CNST_005
   (UserFunctionAssignment, ExpiredPermissionsMiddleware, expire_permissions, API)
   y "Patrones Recomendados" en CNST_006 (Service Layer, Strategy) verificados por
   grep — alineados con ACTUALIZACION_DEL_ARBOL.
4. **Descarte CNST_05 v2.0.0 justificado:** documenta restricción de proceso de
   creación iterativa, no del sistema IACT (D-CNST-3).
5. **Index con meta-bloque y agrupación por dominio:** los 11 toctree entries y la
   sección "Estructura por dominio" cubren los 11 CNST.

## Gaps detectados

### G-1 — FASE 02 base_cognitiva (8 archivos divergentes) no fusionada [BAJA]
Los `.rst` en `FASE 02/base_cognitiva/...` reordenan el catálogo (RBAC=CNST_005,
Reportes=CNST_006) y suman ~12k líneas. Rebuild conserva numeración backup.
Justificado por D-CNST-1. Pérdida real: narrativa NIST-RBAC expandida (44 funciones,
10 agrupadores, 5 segmentos) — parcialmente cubierta en rebuild CNST_011.

### G-2 — Sección "8. Desarrollo" del doc maestro sin CNST propio [MEDIA]
Doc maestro lista "8.1 Coding Standards" y "8.2 Git/CI/CD"; no tienen CNST_NNN en
rebuild ni backup. D-CNST-2 verificó huérfanas contra backup, no contra doc
maestro. Contenido normativo legítimo ausente.

### G-3 — Sección "11. Checklist Pre/Post-Deploy" sin artefacto [BAJA]
Checklist consolidado del doc maestro no expuesto en rebuild. Contenido operativo;
puede vivir en `procedimientos/`.

### G-4 — Sección "12. Glosario de Restricciones" no migrada [BAJA]
Doc maestro cierra con glosario; ausente en rebuild y backup. Puede consolidarse a
nivel proyecto.

### G-5 — Index pierde trazabilidad histórica [BAJA]
Backup index documentaba `Lineas Totales: 10,993`, `Integracion RBAC: v5.1.1` y
sección "Cambios en v1.1.0". Rebuild los omite (reemplazados por meta + narrativa).
No es contenido normativo, pero sí historial.

### G-6 — Cross-ref `:ref:`br-006`` reemplazada por texto plano [BAJA]
En CNST_011 L27, rebuild convirtió `:ref:`br-006`` a texto ("BR-006 (regla de
negocio pendiente de WP requisitos)"). Rompe link futuro.

## Recomendación final

**Avanzar al gate** con dos hallazgos de seguimiento:

- **F-restricciones-1 (MEDIA):** evaluar si "Coding Standards" y "Git/CI/CD"
  merecen CNST_012/013 o pertenecen a `estandares/`.
- **F-restricciones-2 (BAJA):** restaurar `:ref:`br-006`` cuando WP requisitos cree
  el target.

Decisiones D-CNST-1..5 cubren todos los gaps ALTA. Cobertura efectiva del backup:
100% (11/11 CNST + index). Sin pérdida normativa crítica.
