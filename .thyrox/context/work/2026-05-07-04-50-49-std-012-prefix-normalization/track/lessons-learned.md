```yml
created_at: 2026-05-07 07:35:00
project: IACT-docs
work_package: 2026-05-07-04-50-49-std-012-prefix-normalization
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Lessons Learned — STD-012 v1.1.0 Prefix Normalization

> Aprendizajes generalizables del WP. Aplicables a futuras
> reformas masivas del corpus.

## L-1: Inventario antes de actuar

**Trigger:** El primer estimado del WP fue 144 renames + 49
deletes = 193 operaciones. La auditoria scope-correction
detecto que 70 archivos eran out-of-scope (caller/operator/
supervision). Reduccion final: 31 deletes + 92 renames =
123 operaciones in-scope (36% reduccion).

**Aprendizaje:**

Antes de arrancar Phase 7 de un WP de cleanup masivo,
ejecutar Phase 1 DISCOVER con inventario exhaustivo y
clasificacion del scope. Quien valida el scope NO puede
ser el mismo que ejecuta — el ejecutor humano detecto la
exclusion de OPR/SUP/CLI que el agente habia incluido por
defecto.

**Aplicacion:** patron a replicar en cleanups normativos
futuros — siempre presentar inventario al ejecutor antes
de Phase 7.

## L-2: Backup-then-recreate vs simple rename

**Trigger:** El plan inicial era `git mv` (rename simple).
El ejecutor pidio explicitamente "copies los que vas a
eliminar a este wp, y que los elimines, no solo que los
renombres, esto con la finalidad de volver hacerlo desde
cero uno x uno, y si tienes duda de que tenian puedas
consultarlos en el wp".

**Aprendizaje:**

Backup-then-recreate (vs rename simple):

- Pro: deja trazable lo eliminado en backup/ del WP, sin
  necesidad de revisar git log.
- Pro: incentiva recrear con normas actuales (STD-010,
  STD-011, RBAC v5.6.x) en lugar de preservar contenido
  legacy.
- Con: ~5x mas trabajo que rename simple.
- Con: riesgo de introducir errores nuevos al recrear.

Aplicable cuando: (a) el contenido legacy probablemente
viola normas actuales, (b) se quiere oportunidad explicita
de actualizar contenido, (c) la deuda tecnica acumulada
justifica el esfuerzo extra.

**Aplicacion:** opcion estandar para WPs de cleanup
post-deuda-tecnica importante.

## L-3: STD-012 §7.3 — excepcion explicita para auxiliares

**Trigger:** Detectados 2 archivos sin diagrama UML
(``notas-sobre-los-diagramas.rst``, ``tail-sse.rst``). El
plan inicial era renombrarlos por consistencia, pero serian
nombres incorrectos (``diagrama-de-notas-...`` cuando no es
un diagrama).

**Aprendizaje:**

STD-012 v1.1.0 §7.3 formaliza la excepcion: el prefijo
``diagrama-de-`` aplica solo a archivos que contienen
``@startuml`` o ``.. uml::``. Verificacion via grep antes
de aplicar normas masivas.

**Aplicacion:** integrar al checklist de cualquier rename
masivo: verificar que el archivo cae bajo el dominio de la
norma antes de actuar.

## L-4: Race conditions en sphinx-build paralelo

**Trigger:** Build con ``make clean`` mostro 4 warnings
PlantUML. Build incremental subsiguiente EXIT=0 sin
warnings. Diagnosticado como race conditions de PlantUML
processing concurrente con ``-j auto`` (4 procesos
sphinx-build simultaneos).

**Aprendizaje:**

PlantUML cache + processing paralelo puede generar
warnings transitorias en el primer build clean. Para
verificacion deterministica:

::

   make clean
   sphinx-build -W -j 1 -b html source build/html

El ``-j 1`` (serial) elimina race conditions a costa de
tiempo de build (3x mas lento, pero deterministico).

**Aplicacion:** para audits finales pre-cierre, usar -j 1.
Para builds intermedios durante desarrollo, -j auto OK.

## L-5: Cluster-by-cluster batching reduce overhead de commits

**Trigger:** Plan inicial era commit por archivo (193
commits). Plan revisado fue commit por cluster (12 clusters
+ 2 normativos = 14 commits).

**Aprendizaje:**

Cluster-by-cluster es el sweet spot:

- Granularidad suficiente para audit por cluster.
- Pocos commits para revisar en code review.
- Atomico por cluster — un cluster queda consistente en
  un commit.
- Permite pausar el WP entre clusters sin estado
  intermedio inconsistente.

**Aplicacion:** patron a replicar en cualquier cleanup
masivo de UCs. Granularidad NO archivo, NO WP completo,
SI cluster.

## L-6: Out-of-scope state vs Reservado

**Trigger:** OPR (10) y SUP (3) ya estaban como
``Reservado``. CLI (5) estaba como ``Vigente`` pero el
ejecutor confirmo que es out-of-scope del proyecto.

**Aprendizaje:**

Diferencia semantica:

- ``Reservado``: capability declarada en catalogo pero no
  implementada en este release; planificada para futuro.
- ``Fuera del scope``: capability/UC declarada pero NO
  se implementa; decision firme de exclusion.

El nuevo estado ``Fuera del scope`` se introdujo para CLI
+ se aplico a OPR/SUP por consistencia. El cluster
operator tenia textualmente ``out-of-scope`` en el warning,
ahora alineado con el estado metadata.

**Aplicacion:** considerar formalizar ``Fuera del scope``
como valor enum oficial en STD-007 (sigue siendo informal).

## L-7: PlantUML — actividad multilinea sin ; al final

**Trigger:** Sphinx fallo con "Syntax Error 4" al primer
intento de procesar diagramas-de-actividad recreados.
Causa: actividades multilinea sin ``;`` al final (ej:
``:Invoker emite GET /api/v1/audit/\n   con filtros + cursor;``).

**Aprendizaje:**

PlantUML activity diagrams requieren cada paso en una
sola linea terminada con ``;``. Multilinea con
continuacion no funciona.

**Aplicacion:** template para diagramas de actividad
recreados:

::

   :Step description en una sola linea con ; al final;
   :Otro step;

NO:

::

   :Step description
      multilinea sin ;
      con espacios al inicio;

## L-8: Cross-refs verbatim contra archivos reales

**Trigger:** 4 cross-refs rotos detectados durante el WP:
``cnst-030-sod-conjuntos-disjuntos`` (real:
``cnst-030-reglas-de-separacion-de-funciones-sod``),
``br-007-separacion-deberes`` (real:
``br-007-separacion-funciones-sod``),
``br-009-baja-logica`` (real: ``br-009-bajas-logicas``),
``br-018-pii-anonimizacion`` (real: ``br-020-clasificacion-datos``).

**Aprendizaje:**

Antes de generar contenido nuevo con ``:doc:`` refs,
verificar el path real:

::

   ls source/normativa/restricciones/cnst-030*.rst
   ls source/requisitos/reglas-negocio/br-00[79]*.rst

Sphinx strict (-W) detecta los refs rotos y aborta el
build, asi que se cachan eventualmente — pero genera
ciclos de fix que se evitan verificando upfront.

**Aplicacion:** integrar al protocolo de creacion de
diagramas/notas con ``:doc:`` refs.

## L-9: STD-010 vocabulario canonico aplicado masivamente

**Trigger:** El recreate masivo dio oportunidad de aplicar
vocabulario STD-010 a 93 archivos: "Servicio de
Aplicacion" (no Endpoint), "Servicio de Cache" (no Redis),
"Procesador Asincrono" (no Celery), "Almacen de Datos"
(no PostgreSQL), "InternalMailbox", "ExportWorker".

**Aprendizaje:**

Cada cleanup masivo de UCs es una oportunidad para
aplicar STD-010. El proceso:

1. Leer legacy (probable que tenga tecnologia concreta).
2. Identificar terminos prohibidos (grep contra lista
   STD-010 §3).
3. Sustituir por canonicos al recrear.
4. Tecnologia concreta (Redis, Celery) va solo en
   ``implementacion-tecnica.rst`` o ``arquitectura-tecnica/``.

**Aplicacion:** integrar STD-010 audit como primer paso
del recreate de cualquier diagrama.

## L-10: Backup en WP folder vs git history

**Trigger:** El ejecutor pidio backup en el WP aunque git
log preserva todo.

**Aprendizaje:**

Beneficios del backup explicito:

- Acceso directo sin necesidad de comandos git.
- Visible en file tree del WP — descubrible.
- Util durante el recreate (consultar legacy mientras
  se escribe el nuevo).
- Documenta explicitamente lo que se elimino.

Costo: ~3500 lineas adicionales en el commit de backup,
pero git compresion lo absorbe.

**Aplicacion:** estandar para cualquier WP de cleanup
masivo donde hay riesgo de perder contexto al borrar.

## Refs

- WP de origen: este documento.
- Predecesor:
  ``2026-05-07-04-08-13-use-case-view-analysis``
  (G-CU-06 escindido a este WP).
- STD-010 v1.0.0, STD-011 v1.0.0, STD-012 v1.0.0/v1.1.0.
- BR-009 (baja logica), BR-007 (SoD).
- ADR-BACK-008/009/010 (referenciados en multiples
  diagramas recreados).
