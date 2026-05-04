```yml
created_at: 2026-05-04 07:25:32
project: IACT-docs
work_package: 2026-05-04-07-25-32-uc-numbering-conflict
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Discover — UC-043..047 Numbering Conflict

## Problema

Los números UC-043 a UC-047 están asignados simultáneamente a dos
conjuntos de casos de uso completamente distintos:

| Número | Módulo Reports (REAL — tiene archivos) | Módulo Access/SoD (PHANTOM — solo referencias) |
|--------|----------------------------------------|------------------------------------------------|
| UC-043 | `uc-043-reporte-campanas/` | Configurar SoD |
| UC-044 | `uc-044-reporte-transferencias/` | Consultar Permisos Efectivos |
| UC-045 | `uc-045-reporte-menus-ivr/` | Gestionar Catalogo de Agrupadores |
| UC-046 | `uc-046-reporte-clientes-unicos/` | Gestionar Catalogo de Funciones |
| UC-047 | `uc-047-resolver-segmento-usuario/` | Auditar Cambios de Permisos |

## Evidencia (PROVEN)

### Reports UC-043..047 — tienen archivos reales

```
source/requisitos/requisitos-funcionales/reports/
  uc-043-reporte-campanas/
    index.rst, fr-043-01-generar-reporte-campanas.rst
  uc-044-reporte-transferencias/
    index.rst, fr-044-01-generar-reporte-transferencias.rst
  uc-045-reporte-menus-ivr/  ...
  uc-046-reporte-clientes-unicos/  ...
  uc-047-resolver-segmento-usuario/  ...
```

### Access/SoD UC-043..047 — PHANTOM (solo en referencias)

No existe ningún archivo `uc-043-configurar-sod.rst` ni directorio
equivalente bajo `casos-uso/access/` ni `requisitos-funcionales/access/`.

Referencias encontradas (14 archivos, ~35 ocurrencias):
- `br-007-separacion-funciones-sod.rst` §3.2 y §5.3
- `fr-010-02-validar-sod-antes-asignar.rst`
- `fnd-03-casos-de-uso.rst` (5 ocurrencias)
- `fnd-04-trazabilidad.rst` (8 ocurrencias, incluye `.. _uc-043:` y
  `:artefacto: UC_043`)
- `fnd-05-jerarquia-4-niveles.rst` (4 ocurrencias)
- `txm-01-taxonomia-requisitos.rst`
- `rbac-core/responsabilidades.rst`
- `rbac-core/casos-uso.rst`
- `mapeo-uc.rst` (3 ocurrencias)
- `catalogo-funciones.rst` (3 ocurrencias)
- `tpl-uc-casos-de-uso.rst`

## Análisis de causa raíz

El módulo de reports fue numerado secuencialmente UC-032..047 durante
su implementación. El plan de numeración del módulo de acceso/SoD
también asignó el rango 043-047 a UCs de configuración de permisos,
posiblemente en un diseño anterior a la implementación real de reports.

Los UCs de Access/SoD nunca se implementaron como archivos — solo existen
como referencias en documentación conceptual. Los UCs de reports sí
tienen implementación completa.

## Mapa de numeración completo (PROVEN via find)

```
UC-010..011  access (assign/revoke) — REAL
UC-032..047  reports — REAL
UC-050..054  alerts — REAL
UC-055..058  audit — REAL
UC-059..065  logs — REAL
UC-066..070  caller — REAL
UC-071..074  pipeline — REAL
UC-075..077  supervision — REAL
UC-078+      LIBRE
```

## Decisión de resolución

Los UCs con archivos reales conservan sus números. Los UCs phantom de
Access/SoD se renumeran al rango libre UC-078..082:

| Antiguo | Nuevo | Nombre |
|---------|-------|--------|
| UC-043 | UC-078 | Configurar SoD |
| UC-044 | UC-079 | Consultar Permisos Efectivos |
| UC-045 | UC-080 | Gestionar Catalogo de Agrupadores |
| UC-046 | UC-081 | Gestionar Catalogo de Funciones |
| UC-047 | UC-082 | Auditar Cambios de Permisos |

**Justificación:** Los UCs de reports tienen implementación completa
(archivos FR, criterios, diagramas). Renombrarlos implicaría mover
decenas de archivos y actualizar sus FR IDs internos (FR-043.01, etc.).
Los UCs phantom de SoD solo requieren buscar y reemplazar en referencias
— cero archivos que mover.
