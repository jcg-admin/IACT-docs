```yml
created_at: 2026-05-04 19:43:57
project: THYROX
work_package: 2026-05-04-19-43-57-unexpected-unindent-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# R-06 — Unexpected Unindent (docutils)

## Origen

Build post-R-04 clean (PROVEN — WP `2026-05-04-19-05-53-title-overlines-fix/logs/build-after-fix-2026-05-04T193147.txt`):
82 advertencias `Explicit markup ends without a blank line; unexpected unindent. [docutils]`
en 29 archivos.

## Causa raíz

RST requiere una línea en blanco entre el cierre de un bloque de directiva
(`.. note::`, `.. code-block::`, etc.) y el siguiente párrafo/sección al nivel
raíz. Sin esa línea en blanco, docutils interpreta el contenido siguiente como
parte del bloque de la directiva pero con indentación incorrecta.

Patrón uniforme en todos los archivos afectados:

```rst
.. note::

 Texto de la nota en una o varias líneas
 con indentación consistente.
Siguiente párrafo o sección    ← línea N (warned) — sin blank line antes
```

**Fix:** insertar `\n` antes de la línea N en cada instancia.

## Inventario — 82 instancias en 29 archivos

| Archivo | Instancias |
|---------|-----------|
| `arquitectura-tecnica/modulos/alerts/componentes.rst` | 1 |
| `arquitectura-tecnica/modulos/audit/componentes.rst` | 2 |
| `arquitectura-tecnica/modulos/auth/componentes.rst` | 2 |
| `arquitectura-tecnica/modulos/etl-monitoring/componentes.rst` | 2 |
| `arquitectura-tecnica/modulos/rbac-core/componentes.rst` | 1 |
| `arquitectura-tecnica/modulos/sys-logs/componentes.rst` | 2 |
| `arquitectura-tecnica/modulos/user-identity/componentes.rst` | 1 |
| `arquitectura-tecnica/modulos/vis-reports/componentes.rst` | 1 |
| `arquitectura-tecnica/rbac/modelo-rbac-iact/implementacion.rst` | 14 |
| `arquitectura-tecnica/rbac/modelo-rbac-iact/resumen.rst` | 1 |
| `databases/modelo-dual.rst` | 1 |
| `requisitos/_metodologia-aplicacion/patrones-diseno/adapter-ldapuseradapter.rst` | 1 |
| `requisitos/_metodologia-aplicacion/patrones-diseno/observer-auditlog-como-observer-de-eventos.rst` | 1 |
| `requisitos/_metodologia-aplicacion/patrones-diseno/singleton-configuracionalertas.rst` | 1 |
| `requisitos/_metodologia-aplicacion/patrones-diseno/strategy-formato-de-exportacion.rst` | 1 |
| `requisitos/casos-uso/auth/uc-auth-01/implementacion-tecnica.rst` | 3 |
| `requisitos/casos-uso/auth/uc-auth-02/implementacion-tecnica.rst` | 7 |
| `requisitos/casos-uso/auth/uc-auth-03/implementacion-tecnica.rst` | 6 |
| `requisitos/casos-uso/auth/uc-auth-04/implementacion-tecnica.rst` | 6 |
| `requisitos/casos-uso/auth/uc-auth-05/implementacion-tecnica.rst` | 9 |
| `requisitos/casos-uso/permissions/uc-perm-07/datos-involucrados.rst` | 3 |
| `requisitos/reglas-negocio/br-013-username-unico.rst` | 2 |
| `requisitos/reglas-negocio/br-015-bloqueo-intentos-fallidos.rst` | 1 |
| `requisitos/reglas-negocio/br-016-tasa-abandono.rst` | 1 |
| `requisitos/reglas-negocio/br-017-tiempo-promedio-espera.rst` | 2 |
| `requisitos/reglas-negocio/br-018-indice-eficiencia.rst` | 2 |
| `requisitos/reglas-negocio/br-019-retencion-2-anios.rst` | 3 |
| `requisitos/reglas-negocio/br-020-clasificacion-datos.rst` | 3 |
| `requisitos/reglas-negocio/rbac/catalogo-funciones.rst` | 2 |
| **Total** | **82** |

## Completitud de la lista (INFERRED)

La lista proviene del build parcial del log R-04 (16% al final del log).
Sin embargo, las advertencias docutils aparecen durante la fase de lectura
de Sphinx, que precede a la escritura. La última advertencia de este tipo
está en la línea 3521 del log; a partir de ahí no hay más advertencias
`unexpected unindent` aunque el build continúe escribiendo. Conclusión:
la lista de 29 archivos es completa.

## Decisión

Insertar línea en blanco antes de cada línea warned. El script verifica
que la línea anterior no sea ya en blanco (evita dobles blancos).

## Build logs

- `logs/build-after-fix-*.txt` — build post-fix: esperado 0 unexpected unindent warnings
