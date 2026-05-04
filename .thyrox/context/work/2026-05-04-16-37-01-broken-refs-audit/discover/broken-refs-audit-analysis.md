```yml
created_at: 2026-05-04 16:37:01
project: IACT-docs
work_package: 2026-05-04-16-37-01-broken-refs-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Auditoría de referencias rotas — source/

## Metodología

`make html` (modo estándar con `autosectionlabel` y `nitpicky=False`)
captura automáticamente tres tipos de broken references:

- `[ref.doc]` — `:doc:` que apunta a un documento inexistente o con
  path incorrecto.
- `[toc.not_included]` — archivo RST que existe pero no está en ningún
  toctree.
- `Title.*too short` / `duplicate label` — errores RST que impiden
  resolución correcta de anchors.

**Fuente:** PROVEN — `make html 2>&1` ejecutado en esta sesión, output
completo capturado y analizado.

---

## Resumen ejecutivo

| Categoría | Instancias | Severidad |
|-----------|-----------|----------|
| R-01: `:doc:` con path incorrecto (archivo EXISTE, path es relativo erróneo) | 10 warnings (4 targets únicos) | ALTA |
| R-02: `:doc:` a uml-NN sin path absoluto (directorio existe, ref es nombre bare) | 11 warnings (11 targets únicos) | ALTA |
| R-03: Archivos huérfanos (existen, no están en ningún toctree) | 14 archivos | MEDIA |
| R-04: Title overline/underline demasiado corto (RST syntax) | 31 instancias | MEDIA |
| R-05: Duplicate label (autosectionlabel + label manual duplicado) | 33 instancias | BAJA |

Total warnings en build: 14 (build previo). Después de los hallazgos
de ÉPICA 18 el total se mantiene en ese rango — los R-04 y R-05 son
preexistentes y no impiden la navegación.

---

## R-01 — `:doc:` con path relativo incorrecto

### Descripción

Cuatro documentos son referenciados con nombre corto (`relaciones-uml`,
`patrones-diseno`, `agregacion-interfaces`, `diagramas-uml`) desde
archivos que están en subdirectorios de `_metodologia-aplicacion/`.
Sphinx resuelve paths relativos al directorio del archivo fuente.
Desde `analisis-dominio/` o `diagramas-secuencias/`, estos nombres no
resuelven — el archivo real está un nivel arriba.

### Archivos referenciadores y targets reales

| Archivo fuente | Ref rota | Archivo real (EXISTE) | Path correcto |
|---------------|----------|----------------------|---------------|
| `requisitos/_metodologia-aplicacion/analisis-dominio/ejemplo-iact-usuario-grupo.rst:4` | `:doc:\`agregacion-interfaces\`` | `requisitos/_metodologia-aplicacion/agregacion-interfaces/index.rst` | `/requisitos/_metodologia-aplicacion/agregacion-interfaces/index` |
| `requisitos/_metodologia-aplicacion/analisis-dominio/ejemplo-iact-vinculacion-textual-recomendada.rst:21` | `:doc:\`agregacion-interfaces\`` | idem | idem |
| `requisitos/_metodologia-aplicacion/analisis-dominio/ejemplo-iact-vinculacion-textual-recomendada.rst:21` | `:doc:\`patrones-diseno\`` | `requisitos/_metodologia-aplicacion/patrones-diseno/index.rst` | `/requisitos/_metodologia-aplicacion/patrones-diseno/index` |
| `requisitos/_metodologia-aplicacion/analisis-dominio/el-equivalente-iact-rbac-y-agregaciones-canonicas.rst:4` | `:doc:\`agregacion-interfaces\`` | idem | idem |
| `requisitos/_metodologia-aplicacion/analisis-dominio/sintaxis-plantuml-minima.rst:26` | `:doc:\`relaciones-uml\`` | `requisitos/_metodologia-aplicacion/relaciones-uml/index.rst` | `/requisitos/_metodologia-aplicacion/relaciones-uml/index` |
| `requisitos/_metodologia-aplicacion/analisis-dominio/subtipos-con-etiqueta-implements.rst:4` | `:doc:\`relaciones-uml\`` | idem | idem |
| `requisitos/_metodologia-aplicacion/diagramas-secuencias/aplicacion-a-iact-exportarreportefacade.rst:4` | `:doc:\`patrones-diseno\`` | idem | idem |
| `requisitos/_metodologia-aplicacion/diagramas-secuencias/ejemplo-iact-verificacion-de-permiso-heredado.rst:4` | `:doc:\`relaciones-uml\`` | idem | idem |
| `requisitos/casos-uso/auth/uc-auth-01/implementacion-tecnica.rst:192` | `:doc:\`diagramas-uml\`` | `requisitos/_metodologia-aplicacion/diagramas-uml/index.rst` | `/requisitos/_metodologia-aplicacion/diagramas-uml/index` |
| `requisitos/casos-uso/auth/uc-auth-01/implementacion-tecnica.rst:194` | `:doc:\`patrones-diseno\`` | idem | idem |

**Fuente:** PROVEN — `grep` en archivos fuente + `find` confirmando existencia
de los targets reales.

### Corrección

Cambiar paths relativos cortos a paths absolutos desde la raíz de `source/`:

```
:doc:`agregacion-interfaces`
→ :doc:`/requisitos/_metodologia-aplicacion/agregacion-interfaces/index`

:doc:`relaciones-uml`
→ :doc:`/requisitos/_metodologia-aplicacion/relaciones-uml/index`

:doc:`patrones-diseno`
→ :doc:`/requisitos/_metodologia-aplicacion/patrones-diseno/index`

:doc:`diagramas-uml`
→ :doc:`/requisitos/_metodologia-aplicacion/diagramas-uml/index`
```

Archivos a modificar: 7 archivos, 10 ocurrencias.

---

## R-02 — `:doc:` a uml-NN con nombre bare (directorio existe)

### Descripción

Los archivos en `base-cognitiva/_uml/cuando-usar-cada-diagrama/` y en
`base-cognitiva/_uml/uml-04-uso-relaciones/` referencian los capítulos
UML con nombre corto (`uml-11-diagramas-actividades`, etc.). Esos
directorios existen con sus `index.rst` pero el path relativo es incorrecto
— se necesita subir un nivel (`../uml-NN/index`) o usar path absoluto.

### Archivos referenciadores y targets reales

| Archivo fuente | Ref rota | Directorio real (EXISTE) | Path correcto |
|---------------|----------|--------------------------|---------------|
| `cuando-usar-cada-diagrama/diagrama-de-actividades.rst:10` | `uml-11-diagramas-actividades` | `_uml/uml-11-diagramas-actividades/index.rst` | `/base-cognitiva/_uml/uml-11-diagramas-actividades/index` |
| `cuando-usar-cada-diagrama/diagrama-de-casos-de-uso.rst:14` | `uml-06-introduccion-casos-uso` | `_uml/uml-06-introduccion-casos-uso/index.rst` | `/base-cognitiva/_uml/uml-06-introduccion-casos-uso/index` |
| `cuando-usar-cada-diagrama/diagrama-de-casos-de-uso.rst:14` | `uml-07-diagramas-casos-uso` | `_uml/uml-07-diagramas-casos-uso/index.rst` | `/base-cognitiva/_uml/uml-07-diagramas-casos-uso/index` |
| `cuando-usar-cada-diagrama/diagrama-de-clases.rst:11` | `uml-03-uso-orientacion-objetos` | `_uml/uml-03-uso-orientacion-objetos/index.rst` | `/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/index` |
| `cuando-usar-cada-diagrama/diagrama-de-clases.rst:12` | `uml-04-uso-relaciones` | `_uml/uml-04-uso-relaciones/index.rst` | `/base-cognitiva/_uml/uml-04-uso-relaciones/index` |
| `cuando-usar-cada-diagrama/diagrama-de-clases.rst:13` | `uml-05-agregacion-composicion-interfaces` | `_uml/uml-05-agregacion-composicion-interfaces/index.rst` | `/base-cognitiva/_uml/uml-05-agregacion-composicion-interfaces/index` |
| `cuando-usar-cada-diagrama/diagrama-de-colaboraciones.rst:10` | `uml-10-diagramas-colaboraciones` | `_uml/uml-10-diagramas-colaboraciones/index.rst` | `/base-cognitiva/_uml/uml-10-diagramas-colaboraciones/index` |
| `cuando-usar-cada-diagrama/diagrama-de-componentes.rst:11` | `uml-12-diagramas-componentes` | `_uml/uml-12-diagramas-componentes/index.rst` | `/base-cognitiva/_uml/uml-12-diagramas-componentes/index` |
| `cuando-usar-cada-diagrama/diagrama-de-distribucion.rst:11` | `uml-13-diagramas-distribucion` | `_uml/uml-13-diagramas-distribucion/index.rst` | `/base-cognitiva/_uml/uml-13-diagramas-distribucion/index` |
| `cuando-usar-cada-diagrama/diagrama-de-estados.rst:11` | `uml-08-diagramas-estados` | `_uml/uml-08-diagramas-estados/index.rst` | `/base-cognitiva/_uml/uml-08-diagramas-estados/index` |
| `cuando-usar-cada-diagrama/diagrama-de-objetos.rst:13` | `uml-03-uso-orientacion-objetos` | `_uml/uml-03-uso-orientacion-objetos/index.rst` | `/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/index` |
| `cuando-usar-cada-diagrama/diagrama-de-secuencias.rst:12` | `uml-09-diagramas-secuencias` | `_uml/uml-09-diagramas-secuencias/index.rst` | `/base-cognitiva/_uml/uml-09-diagramas-secuencias/index` |
| `uml-04-uso-relaciones/herencia-y-generalizacion.rst:83` | `uml-03-uso-orientacion-objetos` | `_uml/uml-03-uso-orientacion-objetos/index.rst` | `/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/index` |

**Fuente:** PROVEN — `find source/base-cognitiva/_uml -name "index.rst"` +
grep en archivos fuente confirmando paths usados.

### Corrección

Reemplazar nombres bare por paths absolutos desde raíz. Patrón:

```
:doc:`uml-NN-nombre`
→ :doc:`/base-cognitiva/_uml/uml-NN-nombre/index`
```

Archivos a modificar: 9 archivos, 13 ocurrencias.

---

## R-03 — Archivos huérfanos (no en ningún toctree)

### Descripción

14 archivos `.rst` en `requisitos/_metodologia-aplicacion/` existen en el
filesystem pero Sphinx reporta que no están incluidos en ningún toctree.

Estos son los archivos **planos originales** que fueron reemplazados por
**directorios homónimos** con `index.rst` + contenido expandido. Por ejemplo:
- `relaciones-uml.rst` → reemplazado por `relaciones-uml/index.rst` (directorio)
- `patrones-diseno.rst` → reemplazado por `patrones-diseno/index.rst` (directorio)

El `index.rst` de `_metodologia-aplicacion/` referencia los directorios
(`relaciones-uml/index`, `patrones-diseno/index`) pero los archivos `.rst`
planos nunca fueron eliminados. Son ghost files.

### Lista completa

| Archivo huérfano | Estado |
|-----------------|--------|
| `requisitos/_metodologia-aplicacion/agregacion-interfaces.rst` | Ghost — reemplazado por `agregacion-interfaces/index.rst` |
| `requisitos/_metodologia-aplicacion/analisis-dominio.rst` | Ghost — reemplazado por `analisis-dominio/index.rst` |
| `requisitos/_metodologia-aplicacion/casos-uso-diagramas.rst` | Ghost — reemplazado por `casos-uso-diagramas/index.rst` |
| `requisitos/_metodologia-aplicacion/casos-uso-especificacion.rst` | Ghost — reemplazado por `casos-uso-especificacion/index.rst` |
| `requisitos/_metodologia-aplicacion/diagramas-actividades.rst` | Ghost — reemplazado por `diagramas-actividades/index.rst` |
| `requisitos/_metodologia-aplicacion/diagramas-colaboraciones.rst` | Ghost — reemplazado por `diagramas-colaboraciones/index.rst` |
| `requisitos/_metodologia-aplicacion/diagramas-componentes.rst` | Ghost — reemplazado por `diagramas-componentes/index.rst` |
| `requisitos/_metodologia-aplicacion/diagramas-distribucion.rst` | Ghost — reemplazado por `diagramas-distribucion/index.rst` |
| `requisitos/_metodologia-aplicacion/diagramas-estados.rst` | Ghost — reemplazado por `diagramas-estados/index.rst` |
| `requisitos/_metodologia-aplicacion/diagramas-secuencias.rst` | Ghost — reemplazado por `diagramas-secuencias/index.rst` |
| `requisitos/_metodologia-aplicacion/diagramas-uml.rst` | Ghost — reemplazado por `diagramas-uml/index.rst` |
| `requisitos/_metodologia-aplicacion/orientacion-objetos.rst` | Ghost — reemplazado por `orientacion-objetos/index.rst` |
| `requisitos/_metodologia-aplicacion/patrones-diseno.rst` | Ghost — reemplazado por `patrones-diseno/index.rst` |
| `requisitos/_metodologia-aplicacion/relaciones-uml.rst` | Ghost — reemplazado por `relaciones-uml/index.rst` |

**Fuente:** PROVEN — `grep "document isn't included"` del build output +
`ls source/requisitos/_metodologia-aplicacion/*.rst`.

### Corrección

`git rm` de los 14 archivos ghost. No contienen contenido canónico — ese
contenido migró a los directorios homónimos.

**Precaución:** Verificar antes de eliminar que ningún archivo en el corpus
usa `:doc:` apuntando directamente a estos archivos planos (no al index del
directorio). Si existe tal referencia, primero corregirla (es un R-01) y
luego eliminar el ghost.

---

## R-04 — Title overline/underline demasiado corto

### Descripción

31 instancias de secciones RST con subrayado o sobrelineado más corto que
el título. No impiden la navegación pero generan warnings y pueden afectar
el renderizado.

### Distribución por dominio

| Dominio | Instancias |
|---------|-----------|
| `requisitos/casos-uso/auth/` | 10 |
| `requisitos/casos-uso/users/` | 4 |
| `requisitos/casos-uso/access/` | 3 |
| `arquitectura-tecnica/design-view/` | 1 |
| `arquitectura-tecnica/domain-model/` | 1 |
| `arquitectura-tecnica/modulos/etl-monitoring/` | 1 |
| `databases/modelo-dual.rst` | 3 |
| `requisitos/reglas-negocio/` | 4 |
| `requisitos/casos-uso/auth/uc-auth-01/actores-precondiciones.rst` | 2 |
| Otros | 2 |

**Fuente:** PROVEN — `grep "Title.*too short"` del build output.

### Corrección

Para cada instancia: leer el archivo en la línea indicada, medir la longitud
exacta del título y ajustar el overline/underline al mismo largo.
Patrón de fix ya demostrado en ÉPICA 18 (F-01, F-06).

---

## R-05 — Duplicate labels (autosectionlabel)

### Descripción

33 instancias de `duplicate label` generadas por `sphinx.ext.autosectionlabel`.
Esta extensión crea automáticamente anchors para cada sección — cuando dos
secciones tienen el mismo título en documentos distintos, el anchor se duplica.

**Origen probable:** Sphinx genera anchors con el path completo del documento
+ título. Las duplicaciones ocurren principalmente en `modulos/alerts/diagramas/`
donde múltiples diagramas tienen el mismo encabezado (ej: "Componentes del
módulo de alertas" aparece en dos archivos dentro del mismo directorio).

### Impacto

- No rompe la navegación `:doc:` (que usa paths, no labels).
- Sí rompe `:ref:` que apunte a esos labels duplicados.
- Sphinx elige uno de los dos — comportamiento no determinístico.

### Corrección

Tres opciones:
- A: Renombrar las secciones para hacerlas únicas.
- B: Agregar etiquetas manuales explícitas (`.. _label-unico:`) antes de
  cada sección conflictiva y desactivar autosectionlabel para esos archivos.
- C: Deshabilitar `autosectionlabel` globalmente (breaking change si hay
  `:ref:` que dependen de él).

**Recomendación:** Opción A — renombrar secciones para que sean descriptivas
y únicas. Es la solución más limpia y no requiere configuración.

---

## Respuesta sobre el plugin de broken refs

### Situación actual de herramientas

| Herramienta | Estado | Uso |
|-------------|--------|-----|
| `make html` (modo estándar) | ✓ Disponible | Detecta `[ref.doc]` + `[toc.not_included]` — **suficiente para internal refs** |
| `SPHINX_NITPICKY=1 make html` | ✓ Disponible | Agrega detección de `:ref:` rotos e intersphinx — más estricto |
| `make linkcheck` | ✓ Disponible | Solo URLs externas — NO sirve para refs internas |
| `sphinx-lint` | ✗ No instalado | Linting estático (no Sphinx) |
| `sphinxcontrib.spelling` | ✓ Configurado en conf.py | Spell checking — no es para refs |

**Conclusión:** No se necesita instalar ningún plugin adicional. `make html`
ya detecta todas las referencias internas rotas. Para una cobertura más
completa, `SPHINX_NITPICKY=1 make html` es el comando correcto — y ya
está configurado en `conf.py` como opt-in via variable de entorno.

---

## DAG de corrección (orden recomendado)

```
R-03 (git rm 14 ghosts)
  └── precede a → R-01 (fix :doc: paths)
                    └── porque: los ghosts podrían confundir si un
                        :doc: apunta al ghost en lugar del directorio

R-01 (fix 10 :doc: refs en _metodologia-aplicacion/)
  └── paralelo con → R-02 (fix 13 :doc: refs en base-cognitiva/_uml/)

R-04 (fix 31 title overlines)
  └── paralelo con → R-01 + R-02

R-05 (fix 33 duplicate labels)
  └── último — menor impacto en navegación
```

---

## Criterios de salida

- [ ] `make html` sin ningún warning `[ref.doc]` (0 referencias `:doc:` rotas)
- [ ] `make html` sin ningún warning `[toc.not_included]` (0 huérfanos)
- [ ] `SPHINX_NITPICKY=1 make html` — 0 warnings adicionales de `:ref:` rotos
- [ ] Los 14 archivos ghost eliminados con `git rm`
- [ ] Build succeeded con ≤ warnings de `duplicate label` (R-05 puede quedar
  para WP posterior si el scope es demasiado amplio)
