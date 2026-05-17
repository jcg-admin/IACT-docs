```yml
created_at: 2026-05-04 04:52:25
project: IACT-docs
work_package: 2026-05-04-04-52-25-metodologia-uml-split
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# DISCOVER — Múltiples Diagramas por Archivo (_metodologia y base-cognitiva)

## Problema

Dos zonas del repositorio tienen archivos con múltiples diagramas PlantUML
por archivo, violando la regla un-diagrama-por-archivo:

1. `source/requisitos/_metodologia-aplicacion/` — 15 archivos con 2-45 diagramas
2. `source/base-cognitiva/_uml/` — 14 archivos con 2-19 diagramas

## Hallazgos (PROVEN)

### _metodologia-aplicacion

```
45 diagramas-secuencias.rst
31 relaciones-uml.rst
31 analisis-dominio.rst
29 diagramas-distribucion.rst
21 diagramas-estados.rst
21 diagramas-colaboraciones.rst
20 diagramas-componentes.rst
17 agregacion-interfaces.rst
15 orientacion-objetos.rst
12 casos-uso-diagramas.rst
10 diagramas-uml.rst
7  diagramas-actividades.rst
6  patrones-diseno.rst
2  casos-uso-especificacion.rst
```

Total: 15 archivos con múltiples diagramas

### base-cognitiva/_uml

```
19 uml-02-orientacion-objetos.rst
16 uml-04-uso-relaciones.rst
15 uml-03-uso-orientacion-objetos.rst
13 uml-10-diagramas-colaboraciones.rst
12 uml-09-diagramas-secuencias.rst
12 uml-01-introduccion.rst
12 cuando-usar-cada-diagrama.rst
11 (proced-gob-006 - excluir: normativa)
7  uml-07-diagramas-casos-uso.rst
...
```

## Decisiones tomadas

### D-001: ¿Aplica la regla un-diagrama-por-archivo a estas zonas?

**SÍ** — La regla es universal para `source/arquitectura-tecnica/` y fue
extendida por el usuario a UC spec files. Aplica también a estas zonas.

**Diferencia de contexto:** Estos son archivos de guía/catálogo, no specs.
Los diagramas son *ejemplos* ilustrativos de una técnica (no especificaciones
de comportamiento del sistema). Sin embargo, la regla de naming y
un-diagrama-por-archivo aplica igualmente.

### D-002: Estrategia de split

Para archivos con muchos ejemplos (ej. `diagramas-secuencias.rst` con 45):
- Crear subdirectorio `{nombre-archivo}/` dentro de `_metodologia-aplicacion/`
- Un archivo por ejemplo con nombre auto-descriptivo del diagrama
- Crear `{nombre}/index.rst` como toctree
- Reemplazar el archivo original por el index

Para archivos con 2-3 diagramas:
- Dividir directamente en archivos hermanos en el mismo directorio

### D-003: uc-inc-rpt-01 (trabajo adicional)

`source/requisitos/casos-uso/reports/uc-inc-rpt-01/` tiene solo 7 de 12 partes.
Faltan: `flujos-alternos`, `excepciones`, `requisitos-no-funcionales`,
`datos-involucrados`, `patrones-diseno`. Esto se incluye en este WP
como tarea adicional (D).

### D-004: Prioridad

1. `_metodologia-aplicacion/` — 15 archivos (impacto en navegabilidad)
2. `base-cognitiva/_uml/` — 14 archivos
3. `uc-inc-rpt-01` completeness — 5 partes faltantes
