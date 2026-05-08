```yml
project: IACT-docs
work_package: 2026-05-08-01-41-12-sprint1-filenames-and-factory
created_at: 2026-05-08 01:41:12
current_phase: Phase 10 — EXECUTE
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (10 filenames + 1 Factory + ~50-80 cross-refs)
target: Sprint 1 del roadmap del audit clean-code-naming. Combina WP-A (10 filenames con `sod` en el nombre) + WP-H (`ReporteFactory` rename) en un solo WP por low-risk + sin pre-requisitos. WP-F (Serializer/ViewSet/View) NO se incluye — espera a confirmar que `backend/conventions.rst` v2.0.0 este mergeado a main para evitar race contra v1.0.0.
predecessor_wp: 2026-05-08-01-18-37-naming-rules-resolution (cerrado, 4 decisiones aplicadas)
trigger: directiva del ejecutor "Procede con Sprint 1 en paralelo: WP-A + WP-H"
```

# WP — Sprint 1 (filenames sod + ReporteFactory)

## Trigger

Tras cerrar WP `naming-rules-resolution` con D1-D4
aplicadas, el ejecutor autorizo Sprint 1 en paralelo:

- **WP-A:** 10 filenames con `sod` en el nombre.
- **WP-H:** `ReporteFactory` (caso puntual de Factory
  prohibido).

Pre-requisitos cumplidos:

- D1 ya alineo `backend/conventions.rst` con CLEAN_CODE.
- D4 ya documento excepcion RBAC.
- Audit (`clean-code-naming-audit`) identifico todos los
  archivos.

## Restriccion explicita del ejecutor

> "Antes de abrir WP-F (Serializer/ViewSet/View) que ahora
> esta desbloqueado por D1, confirmar que
> `backend/conventions.rst` v2.0.0 ya esta mergeado en la
> rama principal."

WP-F **NO** se incluye en este WP. Sprint 2 y 3 quedan
diferidos.

## WP-H — `ReporteFactory` rename

### Verificacion previa requerida

Segun el ejecutor:

> "El nombre correcto depende del rol que cumple la clase:
> si construye reportes para entrega, ``ReporteAssembler``;
> si los genera desde datos crudos, ``ReporteGenerator``.
> Verificar el codigo antes de commitear el rename."

Procedimiento:

1. Leer `source/requisitos/_metodologia-aplicacion/patrones-diseno/factory-reportefactory.rst`.
2. Determinar si la clase construye reportes para entrega
   o los genera desde datos crudos.
3. Aplicar `ReporteAssembler` o `ReporteGenerator` segun
   corresponda.

### Cambios derivados

- Posible rename del filename
  (`factory-reportefactory.rst` viola §5 + §1.2).

## WP-A — Filenames con `sod` (10 archivos)

Segun lista del audit C2:

| Filename actual | Renombre propuesto |
|---|---|
| `requisitos/reglas-negocio/br-007-separacion-funciones-sod.rst` | `br-007-separacion-de-funciones.rst` |
| `requisitos/reglas-negocio/rbac/sod.rst` | `rbac/separacion-de-deberes.rst` |
| `arquitectura-tecnica/design-view/act-sod-check.rst` | `act-validacion-separacion.rst` |
| `normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod.rst` | `cnst-030-reglas-de-separacion-de-funciones.rst` |
| `requisitos/requisitos-funcionales/access/uc-010.../fr-010-02-validar-sod-antes-asignar.rst` | `fr-010-02-validar-separacion-antes-asignar.rst` |
| `normativa/gobernanza/raci-rbac/raci-sod.rst` | `raci-separacion-de-deberes.rst` |
| `arquitectura-tecnica/modulos/rbac-core/diagramas/evaluacion-conflicto-sod.rst` | `evaluacion-conflicto-separacion.rst` |
| `casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-estados-sod-rule.rst` | `diagrama-de-estados-separation-rule.rst` |
| `casos-uso/access/uc-acc-01/diagramas-uml/diagrama-de-sod-validation.rst` | `diagrama-de-validacion-separacion.rst` |
| `casos-uso/access/uc-acc-05/diagramas-uml/diagrama-de-estados-sodrule.rst` | `diagrama-de-estados-separation-rule.rst` |

### Cambios derivados (por archivo)

Para cada rename:

1. `git mv` del archivo.
2. Buscar y actualizar cross-refs `:doc:` que apuntan al
   path viejo.
3. Actualizar toctrees que listen el archivo viejo.
4. Actualizar `:ref:` anchors si los hay.

### Restriccion

NO modificar contenido **interno** de los archivos en este
WP — solo rename + ajuste de cross-refs / toctrees /
anchors. La narrativa interna SoD/sod queda para WP-B y
WP-C de Sprint 2.

## Output esperado

Por archivo: 1 commit Tim Pope con el rename + sus refs
derivadas.

Total estimado: ~12-15 commits.

## Stopping points

- **SP-01 (humano):** revisar antes de cierre.

## Refs

- WP `naming-rules-resolution` (cerrado, D1-D4 aplicadas).
- WP `clean-code-naming-audit` (cerrado, audit-only).
- CLEAN_CODE_NAMING_PRINCIPLES §1.2, §5, §8.2.
- backend/conventions.rst v2.0.0 (D1).
- STD-010 v1.1.0 (D2 + D4).
