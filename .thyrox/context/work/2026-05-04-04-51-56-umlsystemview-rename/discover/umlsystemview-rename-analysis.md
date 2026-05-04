```yml
created_at: 2026-05-04 04:51:56
project: IACT-docs
work_package: 2026-05-04-04-51-56-umlsystemview-rename
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# DISCOVER — Nombres Genéricos en UMLSystemView (12 archivos)

## Problema

Los archivos en `source/arquitectura-tecnica/UMLSystemView/` tienen nombres
genéricos que describen el *tipo* de diagrama, no el *contenido*:
`casos-uso.rst`, `clases.rst`, `secuencia.rst`, `componentes.rst`, etc.

Esto viola la regla de nombres auto-descriptivos.

## Hallazgos (PROVEN)

```bash
ls source/arquitectura-tecnica/UMLSystemView/
→ actividad-autenticacion.rst     ← ya auto-descriptivo
→ actividad-flujo-principal.rst   ← ya auto-descriptivo
→ casos-uso.rst                   ← GENÉRICO
→ clases.rst                      ← GENÉRICO
→ componentes.rst                 ← GENÉRICO
→ comunicacion.rst                ← GENÉRICO
→ despliegue-multicliente.rst     ← ya auto-descriptivo
→ despliegue.rst                  ← GENÉRICO (¿de qué?)
→ index.rst                       ← OK
→ maquina-estados.rst             ← GENÉRICO (¿de qué entidad?)
→ secuencia.rst                   ← GENÉRICO
→ submaquina-etl.rst              ← ya auto-descriptivo
→ submaquina-reporte.rst          ← ya auto-descriptivo
```

Archivos genéricos: 7 (casos-uso, clases, componentes, comunicacion, despliegue, maquina-estados, secuencia)

## Decisiones tomadas

### D-001: Qué renombrar y a qué nombre

| Archivo actual | Título interno | Nombre correcto |
|----------------|----------------|-----------------|
| `casos-uso.rst` | "Sistema IACT — Diagrama de Casos de Uso" | `casos-uso-sistema-iact.rst` |
| `clases.rst` | "Sistema IACT — Diagrama de Clases" | `clases-sistema-iact.rst` |
| `componentes.rst` | (verificar heading) | `componentes-sistema-iact.rst` |
| `comunicacion.rst` | (verificar heading) | `comunicacion-sistema-iact.rst` |
| `despliegue.rst` | (verificar heading) | `despliegue-sistema-iact.rst` |
| `maquina-estados.rst` | (verificar heading) | `maquina-estados-etl.rst` o `maquina-estados-sistema.rst` |
| `secuencia.rst` | "Sistema IACT — Diagrama de Secuencia" | `secuencia-sistema-iact.rst` |

### D-002: Estrategia

- Renombrar archivos (`git mv`)
- Actualizar `UMLSystemView/index.rst` toctree
- Verificar otras referencias en el repo al nombre antiguo

### D-003: Qué NO cambiar

- `actividad-autenticacion.rst`, `actividad-flujo-principal.rst`,
  `despliegue-multicliente.rst`, `submaquina-etl.rst`, `submaquina-reporte.rst`
  ya tienen nombres auto-descriptivos — no tocar.
