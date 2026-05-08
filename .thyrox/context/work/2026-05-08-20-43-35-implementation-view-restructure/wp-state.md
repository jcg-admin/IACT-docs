```yml
project: IACT-docs
work_package: 2026-05-08-20-43-35-implementation-view-restructure
created_at: 2026-05-08 20:43:35
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeño-mediano (10 archivos a renombrar + 10 nuevos index.rst, 0 cross-refs externos)
target: Restructurar `source/arquitectura-tecnica/implementation-view/` de 13 archivos planos a directorios por modulo (10 in-scope), siguiendo la convencion ya validada en `use-case-view/` y `design-view/`. Preserva los 3 archivos out-of-scope (caller, operator, supervision) como flat con nota en index.rst.
predecessor_wp: 2026-05-08-17-51-36-design-view-restructure (cerrado)
trigger: directiva del ejecutor "abrir el WP `implementation-view-restructure` con el mismo patron ya validado"
```

# WP — Implementation-View restructure (cajas por modulo)

## Phase 1 — DISCOVER

### Estado actual de `implementation-view/` (14 archivos planos)

| Categoria | Cuenta | Archivos |
|---|---|---|
| Indice | 1 | `index.rst` v2.0.0 (44 lineas, toctree a 13 impl-*) |
| `impl-<modulo>.rst` (10 in-scope) | 10 | access, admin, alerts, audit, auth, logs, permissions, pipeline, reports, users |
| `impl-<modulo>.rst` (3 out-of-scope) | 3 | caller, operator, supervision |

Tamaño promedio: 55–70 lineas por archivo. Cada uno contiene
**1 solo diagrama de componentes** (uml-04) con capas
``<<api>>``, ``<<serializer>>``, ``<<service>>``,
``<<repository>>``, ``<<orm>>`` + database. Mucho mas simple
que design-view (que tenia 2-4 diagramas por modulo).

Estado: todos `Vigente`, version 1.0.0.

### Scope (per directiva del ejecutor + decision DesignView)

**In-scope (10 modulos a migrar):** access, admin, alerts,
audit, auth, logs, permissions, pipeline, reports, users.

**Out-of-scope (3 archivos flat preservados):** caller,
operator, supervision. Misma decision documentada en
`design-view/index.rst` v4.0.0:
- caller: externo (IVR del cliente, no se diseña ni
  implementa internamente).
- operator, supervision: deferidos a WPs futuros si/cuando
  se decida implementarlos.

**Diferencia con DesignView:** los 3 archivos
`impl-{caller,operator,supervision}.rst` SI tienen
contenido sustantivo (60-70 lineas con diagrama de
componentes). En DesignView nunca existieron, asi que el
problema no se planteo. Aqui hay 2 opciones:

- **Opcion A:** preservar los 3 como flat, NO migrar a
  cajas. Documentar en el nuevo `index.rst` que son
  out-of-scope para la estructura modular pero el
  contenido se mantiene como referencia historica.
- **Opcion B:** eliminar los 3 archivos para consistencia
  total con DesignView (que no los tiene). Riesgo: perder
  contenido sustantivo (180-210 lineas totales).

**Recomendacion:** Opcion A. Preservar contenido,
documentar scope. Coherente con la decision de DesignView
sin pérdida.

### Cross-refs entrantes (analisis)

```
Refs externas (fuera de implementation-view): 0
Refs internas (entre impl-*.rst): 0
```

**Ningun archivo impl-*.rst es referenciado via `:doc:`
desde otro lugar del corpus.** Esto es la simplificacion
maxima vs DesignView (que tenia 31 refs internos + 1
externo).

**Riesgo R-01 cero.** No hay sed cross-cluster necesario.

### Estructura objetivo

```
implementation-view/
  index.rst               (v3.0.0 — toctree a modulos + nota out-of-scope)
  access/
    index.rst             ← caja del modulo (NUEVO)
    components.rst        ← contenido de impl-access.rst (renombrado, git mv)
  admin/
    index.rst
    components.rst
  alerts/
    index.rst
    components.rst
  audit/
    index.rst
    components.rst
  auth/
    index.rst
    components.rst
  logs/
    index.rst
    components.rst
  permissions/
    index.rst
    components.rst
  pipeline/
    index.rst
    components.rst
  reports/
    index.rst
    components.rst
  users/
    index.rst
    components.rst

  impl-caller.rst         (PRESERVADO flat — out-of-scope)
  impl-operator.rst       (PRESERVADO flat — out-of-scope)
  impl-supervision.rst    (PRESERVADO flat — out-of-scope)
```

**Naming `components.rst`:** semantica del archivo unico
(diagrama uml-04 de componentes). Mas descriptivo que
mantener `impl-X.rst` dentro del modulo. Patron consistente
con `class.rst`/`sequence.rst`/`state.rst`/`activity.rst`
de DesignView (nomenclatura por tipo de diagrama UML).

### Pattern de `<modulo>/index.rst`

Validado en DesignView. 8 secciones:
1. meta block (artefacto, tipo Module Box, modulo)
2. label `.. _at_impl_mod_<modulo>:`
3. titulo "Implementation View — MOD_X"
4. intro (rol del modulo en la implementacion)
5. UML panoramico CURATED — vista mas alta de los
   componentes (subset del components.rst con foco en
   responsabilidades del modulo + dependencias inter-modulo)
6. "Lectura del diagrama"
7. "Componentes canonicos" (refs `:doc:` a domain-model
   o design-view del modulo)
8. toctree a `components.rst` + seealso

### Pattern de `<modulo>/components.rst`

Es el archivo `impl-<modulo>.rst` actual renombrado, con
sus refs internos actualizados (que son 0). Se preserva
contenido tal cual via `git mv`.

### Conteo global

| Categoria | Cuenta |
|---|---|
| `git mv` (10 archivos in-scope) | 10 |
| `<modulo>/index.rst` nuevos | 10 |
| `implementation-view/index.rst` rewrite | 1 |
| Archivos flat preservados (out-of-scope) | 3 |
| **Total cambios** | **~21 cambios** |
| **Archivos nuevos** | **10** |

### Ventajas vs DesignView

- 0 cross-refs externos (vs 1 externo en DesignView).
- 0 cross-refs internos (vs 30+ en DesignView).
- 1 diagrama por archivo (vs 2-4 en DesignView).
- Total de tasks atomicos esperados: **5 bloques** (los
  modulos en 1 bloque por simplicidad — todos tienen
  estructura idéntica), no 11 como DesignView.
- ~21 cambios totales vs ~75-85 en DesignView.

### Stopping points

- **SP-D1:** confirmar Opcion A (preservar caller/operator/
  supervision flat) vs Opcion B (eliminar para consistencia
  total).
- **SP-D2:** confirmar nombre `components.rst` (vs `impl.rst`
  preservando prefijo, o `module.rst` mas generico).
- **SP-D3:** validar pattern del module index.rst en pilot
  (access/) antes de replicar a 9.

### Pattern de pilot

Como en DesignView, ejecutar pilot en `access/` primero:
- `git mv impl-access.rst access/components.rst`
- Crear `access/index.rst` con panorama curated
- Update `implementation-view/index.rst` con seccion modulos
- Build strict EXIT=0
- Si OK, replicar a los 9 restantes en bloques

### Refs

- WP `design-view-restructure` (precedente) — pattern y
  hallazgos H-00..H-05 ya documentados.
- WP `uc-view-domain-alignment` (precedente origen del
  pattern de cajas).
- `design-view/index.rst` v4.0.0 — referencia de scope
  (caller/operator/supervision excluidos).

## Pendiente para Phase 8 PLAN

1. Confirmar SP-D1 (preservar 3 flat vs eliminar) y SP-D2
   (`components.rst` como nombre).
2. Producir task plan T-NNN: pilot access + 9 replicas +
   index v3.0.0 + build + TRACK.
3. Estimacion: 12-13 tasks atomicos vs 11 en DesignView
   (sin necesidad de cross-cluster fixes).
