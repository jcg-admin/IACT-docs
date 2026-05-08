```yml
project: IACT-docs
work_package: 2026-05-08-03-38-01-tdd5-std010-scope-clarification
created_at: 2026-05-08 03:38:01
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeño (3 exenciones normativas + bump version STD-010 → v1.2.0)
target: TD-D5 — ampliar STD-010 §2 con clausula §2.5 que exenta tres categorias adicionales identificadas como diferidas en WP-G: identity files, landing page arquitectonica, testing files. Es trabajo normativo: no hay renames, no hay cambios en archivos de contenido, no hay dependencias con otras ramas.
predecessor_wp: 2026-05-08-03-18-31-wpf-serializer-viewset-view (cerrado)
trigger: directiva del ejecutor "Si. Abre TD-D5 ahora."
```

# TD-D5 — STD-010 §2.5 scope clarification

## Origen del WP

WP-G `2026-05-08-03-08-21-wpg-std010-cleanup` aplico STD-010 §3
vocabulario canonico a los archivos claramente in-scope (~36
ediciones en rbac-historia, fundamentos, _uml, admin/rbac).
Identifico tres categorias de archivos donde aplicar STD-010
genera **circularidad semantica** (el archivo declara la
identidad/stack del proyecto; abstraerlo elimina la informacion
que el archivo existe para comunicar):

1. **Identity files** — `base-cognitiva/_metadata/meta-01` y
   `meta-05` (12 refs).
2. **Landing page arquitectonica** — `source/index.rst` seccion
   intro y stack (5 refs).
3. **Testing files tecnicos** — `casos-uso/**/testing.rst` (4
   refs en uc-auth-01 y uc-auth-02 tras WP-F).

Total cubierto por TD-D5: **21 refs**.

## Tres exenciones a agregar en STD-010 §2.5

### §2.5.1 Identity files — declaracion del stack del proyecto

Archivos cuyo proposito es **declarar la identidad tecnologica
del proyecto** (que tecnologias se usan como Backend, Frontend,
BD, Cache, Mensajeria, etc.). Aplicar STD-010 a estos archivos
genera circularidad — el archivo existe precisamente para nombrar
el stack.

```text
✓ EXENTO: "Backend: Django REST Framework (Python 3.11+)"
✗ ABSURDO: "Backend: el Framework de Aplicacion"
```

Archivos exentos:

- `source/base-cognitiva/_metadata/meta-01-identidad-proyecto.rst`
- `source/base-cognitiva/_metadata/meta-05-estructura-documental.rst`

Criterio: cualquier archivo cuyo proposito documental sea
**identidad del proyecto** (no narrativa de requisitos, no
diseño operacional, no analisis de proceso).

### §2.5.2 Landing page arquitectonica

`source/index.rst` raiz (la pagina de aterrizaje del repo) ya
tenia tratamiento "por contenido" en §2.2. Esta clausula
clarifica que la **seccion de presentacion arquitectonica**
(parrafos de bienvenida que contextualizan el sistema con su
stack para nuevos lectores) opera bajo el mismo criterio que
identity files — declarar el stack es el proposito, no
abstraerlo.

Aplica a:

- `source/index.rst` parrafos introductorios y bullet lists de
  stack tecnologico.

NO aplica a:

- `source/index.rst` toctree y navegacion (ya en §2.2).
- Cualquier prosa de requisitos o decisiones que no sea
  introduccion arquitectonica.

### §2.5.3 Testing files — paralelo de §5.1

`casos-uso/**/testing.rst` documenta infraestructura de tests:
configuracion de fixtures, factory_boy, pytest, coverage tools.
Es analogo a `implementacion-tecnica.rst` (§5.1 ya exento) pero
no estaba listado en la tabla §2.1.

Esta clausula clarifica que `testing.rst` es **explicitamente
exento por la misma razon que `implementacion-tecnica.rst`** —
el archivo es tecnico por proposito documental.

Archivos exentos:

- `source/requisitos/casos-uso/**/testing.rst`

## Refs no cubiertas por TD-D5 (out of scope)

Para transparencia: WP-G reporto ~288 refs diferidas totales.
TD-D5 cubre 21 (3 categorias arriba). Las restantes ~267 refs
viven en categorias NO incluidas en el alcance literal del
ejecutor para este WP:

| Categoria | Refs | Estado tras TD-D5 |
|---|---|---|
| Identity files (meta-01, meta-05) | 12 | ✅ EXENTO §2.5.1 |
| Landing arquitectonica (index.rst) | 5 | ✅ EXENTO §2.5.2 |
| Testing files | 4 | ✅ EXENTO §2.5.3 |
| `normativa/procedimientos/**` | ~155 | ⚠ Pendiente — no incluido en directiva |
| `normativa/gobernanza/adr-*` | ~50 | ⚠ Pendiente |
| `normativa/estandares/plantillas/**` | ~19 | ⚠ Pendiente |
| `gestion/evidencia/arquitectura-modular/**` | ~6 | ⚠ Pendiente |

Esto se documenta como observacion: el ejecutor especifico solo
3 exenciones; las 230 refs en procedimientos/ADRs/plantillas/
arquitectura-modular tendrian que abordarse con una decision
ulterior si se considera que generan los mismos falsos
positivos (probablemente si — un ADR backend que documenta
"Redis prohibido" necesita decir "Redis", igual que un identity
file). Esa decision es del ejecutor, no de este WP.

## Output esperado

- `STD-010 v1.1.0 → v1.2.0` (MINOR: amplia ambito).
- Nuevas secciones §2.5.1, §2.5.2, §2.5.3.
- Tabla §2.1 actualizada con filas de "No — exenta (§2.5)".
- Historial v1.2.0 en §8.
- 21 refs movidas a estado "exento normativamente".

## Stopping points

- **SP-01:** revisar redaccion antes de bump version.
- **SP-02:** decision opcional sobre extender §2.5 a
  procedimientos/ADRs/plantillas (nuevo WP).

## Refs

- WP-G `2026-05-08-03-08-21-wpg-std010-cleanup` (origen del
  diferimiento).
- STD-010 v1.1.0 §2.1, §2.2, §2.3, §2.4, §5.1.
