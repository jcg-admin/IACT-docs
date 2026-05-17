```yml
created_at: 2026-05-04 02:11:54
project: IACT-docs
work_package: 2026-05-04-02-11-54-uml-alias-naming-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# UML Alias Naming — Discovery Analysis

## Problema

Los diagramas PlantUML del proyecto usan aliases de una o dos letras
(`as U`, `as AE`, `as SR`, `as RVG`) que hacen ilegibles las flechas
de mensajes. Cuando alguien lee `USR -> AE : 1: POST /api/auth/login()`,
no puede entender qué son `USR` ni `AE` sin buscar la declaración.

## Referencia canónica — base-cognitiva/_uml/

El material de referencia en `source/base-cognitiva/_uml/` muestra:

```plantuml
' PATRÓN CORRECTO del libro de referencia:
participant ":GUI"          as GUI
participant ":SistemaOp"    as SO
participant ":CPU"          as CPU
participant ":TarjetaVideo" as TV
participant ":Monitor"      as MON

GUI ->> SO  : notificarTecla   ← SE ENTIENDE
SO  ->> CPU : notificarTecla   ← SE ENTIENDE
```

El patrón: el alias es el nombre de la entidad (igual o abreviatura
reconocible de varias letras). `SO` = SistemaOp, `TV` = TarjetaVideo
— se entiende. `AE` = AuthEndpoint — NO se entiende.

## Regla derivada

**Alias auto-documentado:** al leer solo la flecha del diagrama
(`X -> Y : mensaje`), debe entenderse quiénes son X e Y sin buscar
la declaración.

**Criterios:**
1. Mínimo 3 caracteres en el alias
2. El alias refleja el rol/nombre del participante de forma evidente
3. Alias preferidos: nombre completo en CamelCase o snake_case
4. Abreviaturas aceptables solo si son reconocibles en contexto

## Inventario de violaciones

### diagramas-uml-sistema.rst

| Violación | Corrección |
|-----------|------------|
| `as RVG` | `as view_reports` |
| `as QSG` | `as view_pipeline_status` |
| `as PAG` | `as request_pipeline_retry` |
| `as UAG` | `as assign_functions` |
| `as AUG` | `as view_audit_log` |
| `as SCH` | `as APScheduler` |
| `as USR` (actor) | `as view_reports` |
| `as AE` | `as AuthEndpoint` |
| `as DE` | `as DashboardEndpoint` |
| `as SR` | `as SegmentResolver` |
| `as SRP` | `as ServicioReportes` |
| `as FAIL` | `as AutenticacionFallida` (ya descriptivo) |
| `as USR` (object) | `as UserRBAC` |

### UC diagramas-uml.rst files

Patrones comunes a corregir en todos los UC:
- `as U`, `as F`, `as A`, `as B` — ilegibles
- `as AUD`, `as ADM` — aceptables si contexto claro, idealmente expandir

### DesignView files (ya correctos)
Los archivos de DesignView recién actualizados usan `as Actor`,
`as Iface`, `as SvcNode`, `as Store` — estos son aceptables (3+ chars,
descriptivos en contexto).

## Alcance

1. `diagramas-uml-sistema.rst` — 14 secciones, múltiples diagramas
2. `diagramas-uc-por-modulo.rst` — diagramas UC por módulo
3. `requisitos/casos-uso/**/diagramas-uml.rst` — ~80 UCs
4. `arquitectura-tecnica/*/diagramas.rst` — módulos arquitectónicos

## Prioridad

| Documento | Impacto visual | Prioridad |
|-----------|---------------|-----------|
| `diagramas-uml-sistema.rst` | Alto (documento principal) | Alta |
| `diagramas-uc-por-modulo.rst` | Medio | Media |
| UC `diagramas-uml.rst` | Medio (80 archivos) | Media |
| módulos `diagramas.rst` | Bajo | Baja |
