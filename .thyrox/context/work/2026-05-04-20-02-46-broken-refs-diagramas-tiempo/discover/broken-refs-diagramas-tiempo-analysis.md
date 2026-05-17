```yml
created_at: 2026-05-04 20:02:46
project: THYROX
work_package: 2026-05-04-20-02-46-broken-refs-diagramas-tiempo
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Broken refs en diagramas-tiempo.rst — Análisis (R-08)

## Problema identificado

`source/requisitos/_metodologia-aplicacion/diagramas-tiempo.rst` contenía
6 referencias `:doc:` con bare names que Sphinx no puede resolver cuando
el archivo referenciado vive en un subdirectorio distinto al del documento
que contiene la referencia.

## Ubicación de las refs rotas

| Línea (original) | Ref rota | Tipo |
|---|---|---|
| 126 | `:doc:\`diagramas-secuencias\`` | bare name |
| 126 | `:doc:\`diagramas-estados\`` | bare name |
| 163 | `:doc:\`diagramas-estados\`` | bare name |
| 163 | `:doc:\`diagramas-secuencias\`` | bare name |
| 163 | `:doc:\`diagramas-colaboraciones\`` | bare name |
| 163 | `:doc:\`diagramas-actividades\`` | bare name |

## Causa raíz (PROVEN)

Sphinx resuelve bare names en `:doc:` relativos al directorio del archivo
fuente. Cuando el destino es un subdirectorio con `index.rst`, el bare
name no es suficiente: se necesita la ruta absoluta desde la raíz del
proyecto de documentación.

Verificación de existencia de targets (PROVEN — `ls` ejecutado):

- `source/requisitos/_metodologia-aplicacion/diagramas-secuencias/index.rst` — existe
- `source/requisitos/_metodologia-aplicacion/diagramas-estados/index.rst` — existe
- `source/requisitos/_metodologia-aplicacion/diagramas-colaboraciones/index.rst` — existe
- `source/requisitos/_metodologia-aplicacion/diagramas-actividades/index.rst` — existe

## Fix aplicado

Reemplazar cada bare name con la ruta absoluta:

```
:doc:`diagramas-secuencias`
→ :doc:`/requisitos/_metodologia-aplicacion/diagramas-secuencias/index`

:doc:`diagramas-estados`
→ :doc:`/requisitos/_metodologia-aplicacion/diagramas-estados/index`

:doc:`diagramas-colaboraciones`
→ :doc:`/requisitos/_metodologia-aplicacion/diagramas-colaboraciones/index`

:doc:`diagramas-actividades`
→ :doc:`/requisitos/_metodologia-aplicacion/diagramas-actividades/index`
```

Se afectaron dos ubicaciones en el archivo:

1. Sección "Limitaciones de este ejemplo" (línea ~126): 2 refs.
2. Tabla "Trazabilidad" — fila "Diagramas hermanos" (línea ~163): 4 refs.

## Resultado esperado

Build Sphinx sin warnings `unknown document` para estos targets.
