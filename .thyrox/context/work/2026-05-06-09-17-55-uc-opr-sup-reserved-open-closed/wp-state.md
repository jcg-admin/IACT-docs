```yml
project: IACT-docs
work_package: 2026-05-06-09-17-55-uc-opr-sup-reserved-open-closed
created_at: 2026-05-06 09:17:55
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (Stages 1, 5, 6, 8, 10, 11)
target: Marcar UCs MOD_Operator (UC_OPR_01..10) y MOD_Supervision (UC_SUP_01..03) como reservados open-closed (out-of-scope para release v5.6.0) en ambos arboles del corpus — requisitos/casos-uso/ y arquitectura-tecnica/use-case-view/. La documentacion se preserva como extension point; los indices y banners declaran el status.
predecessor_wp: 2026-05-06-09-02-26-rbac-v5-6-0-corpus-alignment (closed B-1..B-6, bumped 30+ files to v5.6.0)
trigger: directiva del ejecutor "abrir un nuevo wp para actualizar source/arquitectura-tecnica/* y source/requisitos/*" + framing v5.6.0 declara OPR/SUP como reservados pero indices aun los marcan "estado: Vigente".
```

# WP — UC_OPR + UC_SUP como Reservados Open-Closed

## Trigger

El WP predecesor `rbac-v5-6-0-corpus-alignment` reclasifico
MOD_Operator (10 fn) y MOD_Supervision (3 fn) como reservados
open-closed: declarados en el catalogo pero out-of-scope para
v5.6.0. Sin embargo:

- Los `index.rst` de ambos modulos en `requisitos/casos-uso/{operator,
  supervision}/` y `arquitectura-tecnica/use-case-view/{operator,
  supervision}/` aun declaran `:estado: Vigente`.
- Los UC_OPR_01..10 y UC_SUP_01..03 individuales (13 directorios)
  carecen de banner de status reservado.
- No hay nota visible para el lector indicando que estos UCs son
  extension points para una release futura.

## Decisiones de framing (auto-tomadas)

1. **Status frontmatter:** introducir el valor `:estado: Reservado`
   (out-of-scope, open-closed). 13 archivos `Vigente` → `Reservado`
   en operator/ y supervision/. NO inventar un valor — usar
   `Reservado` que es estandar y entendible (vs `OutOfScope` o
   `OpenClosed`).
2. **Banner inline:** agregar en el `index.rst` de cada modulo un
   bloque `.. note::` o `.. warning::` debajo del titulo principal
   declarando:
   - Que el modulo es reservado open-closed para v5.6.0.
   - Que la documentacion se preserva como extension point.
   - Que los UCs no son implementables en esta release.
   - Referencia al WP de framing y al catalogo.
3. **NO eliminar contenido:** preservar UCs y diagramas — son
   extension points. Solo agregar status visible.
4. **NO tocar MOD_Admin:** sus UCs (UC_ADM_01..03) son in-scope
   en v5.6.0; quedan como `Vigente`.

## Inventario de archivos a actualizar

### Zona A — `source/requisitos/casos-uso/operator/` (11 archivos)

- `index.rst` (banner + status)
- `uc-opr-01/index.rst` ... `uc-opr-10/index.rst` (10 archivos —
  status frontmatter)

### Zona B — `source/requisitos/casos-uso/supervision/` (4 archivos)

- `index.rst` (banner + status)
- `uc-sup-01/index.rst`, `uc-sup-02/index.rst`,
  `uc-sup-03/index.rst` (3 archivos)

### Zona C — `source/arquitectura-tecnica/use-case-view/operator/`
(N archivos por descubrir)

- `index.rst` (banner + status)
- archivos hijos si los hay

### Zona D — `source/arquitectura-tecnica/use-case-view/supervision/`
(N archivos por descubrir)

- `index.rst` (banner + status)
- archivos hijos si los hay

## Plan de batches

| Batch | Zona | Effort estimado |
|---|---|---|
| **B-1** | Zona A — operator/ requisitos (11 archivos) | ~25 min |
| **B-2** | Zona B — supervision/ requisitos (4 archivos) | ~15 min |
| **B-3** | Zonas C+D — use-case-view operator/+supervision/ | ~25 min (depende de N hijos) |

Total: **~1.5h wall-clock** + builds entre batches.

## Restricciones

- Strict build (`-W`) tras cada batch.
- Tim Pope commits.
- NO eliminar UC content; solo agregar status + banner.
- NO tocar UC_ADM (in-scope).

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Banner muy largo rompe estructura RST de toctree | Banner antes del titulo o despues del subtitulo, separado con blank lines |
| R-02 | `:estado: Reservado` no esta en STD-008 — convencion nueva | Documentar valor introducido en changelog del WP; valor auto-explicativo |
| R-03 | Cross-references a UC_OPR/UC_SUP desde otros docs pueden seguir asumiendo "Vigente" | Mas alla del scope de este WP — solo banner; verificacion de refs es WP separado |
| R-04 | Build strict puede fallar si banner usa una directive desconocida | Usar `.. note::` o `.. warning::` (ambas estandar Sphinx) |

## Stopping points

- **SP-01** (gate humano): aprobado en blanket por el ejecutor
  ("ya no necesitas el gate humano").
- **SP-02** (gate tecnico per-batch): build strict 0 warnings.
- **SP-03** (cierre): pendiente del ejecutor (I-011).
