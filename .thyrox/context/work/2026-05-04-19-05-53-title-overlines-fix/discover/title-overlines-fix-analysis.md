```yml
created_at: 2026-05-04 19:05:53
project: THYROX
work_package: 2026-05-04-19-05-53-title-overlines-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# R-04 — Title Underline/Overline Too Short

## Origen

Sphinx build (PROVEN — `logs/build-clean-2026-05-04T190553.txt`) produjo 52
advertencias de tipo `Title underline too short` y `Title overline too short`.
Después de deduplicar (Sphinx procesa algunos archivos dos veces en builds
paralelos), se identificaron **31 instancias únicas** en **23 archivos**.

## Causa raíz

RST requiere que la línea de subrayado (y sobrerayado) sea **al menos tan
larga como el texto del título**. Los títulos afectados fueron creados o
editados sin ajustar el subrayado al nuevo largo, o bien el autor copió
un patrón de subrayado corto de otro título.

Patrón más frecuente: títulos con sufijo `(Base de Datos)` que extendieron
el largo del texto pero no el subrayado.

## Inventario de instancias (PROVEN)

### Overlines (7 instancias — overline + underline ambos corregidos)

| Archivo | Línea | Título | Largo título | Largo previo | Correcto |
|---------|-------|--------|-------------|-------------|---------|
| `arquitectura-tecnica/design-view/mod-supervision.rst` | 15 | Design View — MOD_Supervision: Supervision en Tiempo Real | 57 | 53 | 57 |
| `arquitectura-tecnica/domain-model/exceptional-permission.rst` | 16 | ExceptionalPermission | 21 | 19 | 21 |
| `arquitectura-tecnica/process-view/proc-dashboard-concurrencia.rst` | 15 | Process View — Concurrencia de Dashboard en Tiempo Real | 55 | 54 | 55 |
| `arquitectura-tecnica/rbac/modelo-rbac-iact/diagramas/index.rst` | 15 | Modelo RBAC IACT — Diagramas | 28 | 27 | 28 |
| `arquitectura-tecnica/use-case-view/mod-admin.rst` | 15 | MOD_Admin — Administracion del Modelo RBAC: UC por Modulo | 57 | 51 | 57 |
| `base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/metamodelo-descripcion.rst` | 15 | Meta-modelo: descripción de arquitecturas multi-viewpoint | 57 | 55 | 57 |
| `requisitos/reglas-negocio/rbac/index.rst` | 15 | RBAC — Especificacion | 21 | 20 | 21 |

### Underlines (24 instancias)

| Archivo | Línea | Título | Correcto |
|---------|-------|--------|---------|
| `arquitectura-tecnica/modulos/etl-monitoring/componentes.rst` | 31 | Acceso a Datos — etl_runs (Almacen de Datos) | 44 |
| `databases/modelo-dual.rst` | 22 | 1. Almacen de Datos 10.1.48 — IVR Fuente (solo lectura) | 55 |
| `databases/modelo-dual.rst` | 34 | 2. Almacen de Datos 10.1.48 — IVR Analitica (lectura/escritura ETL) | 67 |
| `databases/modelo-dual.rst` | 78 | 5. Routers de base de datos | 27 |
| `requisitos/casos-uso/access/uc-acc-01/actores-precondiciones.rst` | 81 | 2.2.3 BD analitica (Base de Datos) | 34 |
| `requisitos/casos-uso/access/uc-acc-01/actores-precondiciones.rst` | 100 | 2.2.5 Interfaz de Usuario | 25 |
| `requisitos/casos-uso/access/uc-acc-09/flujo-principal.rst` | 58 | PASO 8 — consultar paginado | 27 |
| `requisitos/casos-uso/auth/uc-auth-01/actores-precondiciones.rst` | 112 | 2.2.2 Base de datos analitica (Base de Datos) | 45 |
| `requisitos/casos-uso/auth/uc-auth-01/actores-precondiciones.rst` | 153 | 2.2.4 Interfaz de Usuario | 25 |
| `requisitos/casos-uso/auth/uc-auth-02/actores-precondiciones.rst` | 59 | 2.2.2 Base de datos analitica (Base de Datos) | 45 |
| `requisitos/casos-uso/auth/uc-auth-02/actores-precondiciones.rst` | 72 | 2.2.3 Interfaz de Usuario | 25 |
| `requisitos/casos-uso/auth/uc-auth-03/actores-precondiciones.rst` | 68 | 2.2.3 Base de datos analitica (Base de Datos) | 45 |
| `requisitos/casos-uso/auth/uc-auth-03/actores-precondiciones.rst` | 87 | 2.2.5 Interfaz de Usuario | 25 |
| `requisitos/casos-uso/auth/uc-auth-04/actores-precondiciones.rst` | 53 | 2.2.2 BD analitica (Base de Datos) | 34 |
| `requisitos/casos-uso/auth/uc-auth-04/actores-precondiciones.rst` | 62 | 2.2.3 Interfaz de Usuario | 25 |
| `requisitos/casos-uso/auth/uc-auth-05/actores-precondiciones.rst` | 58 | 2.2.3 BD Base de Datos | 22 |
| `requisitos/casos-uso/users/uc-usr-01/actores-precondiciones.rst` | 56 | 2.2.3 BD Base de Datos | 22 |
| `requisitos/casos-uso/users/uc-usr-01/actores-precondiciones.rst` | 69 | 2.2.5 Interfaz de Usuario | 25 |
| `requisitos/casos-uso/users/uc-usr-01/flujo-principal.rst` | 132 | PASO 9 — Hashear con algoritmo de hash | 38 |
| `requisitos/casos-uso/users/uc-usr-04/actores-precondiciones.rst` | 82 | 2.2.4 Interfaz de Usuario | 25 |
| `requisitos/reglas-negocio/br-013-username-unico.rst` | 254 | 7.1 Modelo de datos | 19 |
| `requisitos/reglas-negocio/br-015-bloqueo-intentos-fallidos.rst` | 154 | 4.1 Modelo de datos | 19 |
| `requisitos/reglas-negocio/br-017-tiempo-promedio-espera.rst` | 180 | 4.2 Modelo de datos | 19 |
| `requisitos/reglas-negocio/br-018-indice-eficiencia.rst` | 178 | 4.2 Modelo de datos | 19 |

## Decisión

**Opción elegida:** Corregir todos los subrayados/sobrerayados a la longitud
exacta del título correspondiente, usando el carácter ya presente en cada
archivo (sin cambiar la jerarquía de caracteres RST).

**Alternativa descartada:** Acortar los títulos — descartada porque los
títulos son descriptivos y correctos; el problema es solo el decorador.

## Método de corrección (PROVEN)

Script Python `fix_title_underlines.py` ejecutado en `/tmp/`:
- Para `underline`: lee título en línea N-1, calcula largo, escribe
  `char * len(titulo)` en línea N.
- Para `overline`: lee título en línea N+1, calcula largo, escribe
  `char * len(titulo)` en líneas N (overline) y N+2 (underline).

Resultado: 23 archivos modificados, 31 instancias corregidas.

## Build logs

- `logs/build-clean-2026-05-04T190553.txt` — build limpio pre-fix: 52 warnings
- `logs/build-after-fix-*.txt` — build post-fix: esperado 0 warnings
