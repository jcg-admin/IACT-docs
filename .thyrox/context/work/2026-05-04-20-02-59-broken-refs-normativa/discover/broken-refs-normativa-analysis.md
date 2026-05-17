```yml
created_at: 2026-05-04 20:03:00
project: THYROX
work_package: 2026-05-04-20-02-59-broken-refs-normativa
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# R-07 — Broken refs en normativa/estandares

## Origen

Build log `b75ert8rr`: 2 warnings `unknown document` en archivos de normativa:

```
normativa/estandares/metodologia-analisis-dominio-ucs.rst:32:
  WARNING: unknown document: '/requisitos/_metodologia-aplicacion/analisis-dominio'
normativa/estandares/metodologia-oop-para-ucs.rst:36:
  WARNING: unknown document: '/requisitos/_metodologia-aplicacion/orientacion-objetos'
```

## Causa raíz

Ambas refs `:doc:` apuntan a rutas de directorio sin sufijo `/index`. Sphinx no
resuelve directorios — requiere el path exacto al archivo `.rst`, que en ambos
casos es `{directorio}/index.rst` (PROVEN: `ls` confirmó existencia).

Patrón uniforme:
```rst
:doc:`/requisitos/_metodologia-aplicacion/analisis-dominio`     ← broken
:doc:`/requisitos/_metodologia-aplicacion/analisis-dominio/index`  ← correcto
```

## Inventario — 2 instancias en 2 archivos

| Archivo | Línea | Ref original | Target verificado |
|---------|-------|-------------|------------------|
| `normativa/estandares/metodologia-analisis-dominio-ucs.rst` | 33 | `.../analisis-dominio` | `.../analisis-dominio/index.rst` ✓ |
| `normativa/estandares/metodologia-oop-para-ucs.rst` | 37 | `.../orientacion-objetos` | `.../orientacion-objetos/index.rst` ✓ |

## Fix aplicado

Agregado sufijo `/index` a cada ref con `str.replace(old + '\`', new + '\`')` para
evitar reemplazar ocurrencias parciales en rutas más largas.

## Build logs

- `logs/build-after-fix-2026-05-04T200310.txt` — build post-fix: `build succeeded.`
  sin warnings en los archivos modificados.
