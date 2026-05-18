.. meta::
   :artefacto: DECISIONES-SANEAR-DEUDA-CI-Y-NORMATIVA
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/sanear-deuda-ci-y-normativa
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:21:29
   :ultimo_cambio: 2026-05-18T18:21:29
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-sanear-deuda-ci-y-normativa:

==============================================
Decisiones: Sanear Deuda de CI y Normativa
==============================================

Decisiones de diseno
====================

D1 — Esquema de CI: incremental bloqueante + completo
------------------------------------------------------

``validate.yml`` se divide en dos jobs:

* ``validate-incremental`` (PR a develop/main, push a develop):
  sin ``make clean``, con cache de doctrees, ``-j 2``. Bloquea
  el merge si falla. Rapido: gate agil.
* ``validate-full`` (push a main, solo si el repo es publico):
  ``make clean`` + build completo limpio ``-j 2``. Garantia
  total contra la zona gris del build incremental.

Alternativas consideradas y por que se descartaron:

* "Completo bloqueante en develop y main": elimina la zona gris
  pero hace que cada merge a develop espere el build largo.
  Contradice el requisito de agilidad declarado.
* "Incremental en develop, completo solo en main": acepta una
  zona gris develop -> main. Es deuda diferida; se descarto por
  el principio de cero deuda.

**Riesgo asumido y documentado**: el job completo corre en push
a main, no en cada push a develop. Entre un merge a develop y la
llegada a main puede acumularse divergencia de la zona gris del
incremental que solo se detecta al llegar a main. Mitigacion: el
build incremental con ``-W`` captura la gran mayoria de
problemas; el completo en main es la garantia final dura. Si en
la practica la divergencia resulta frecuente, evaluar anadir el
completo no-bloqueante tambien en push a develop.

D2 — Guard de visibilidad publica auto-detectante
--------------------------------------------------

El job ``validate-full`` lleva
``if: github.ref == 'refs/heads/main' &&
github.event.repository.visibility == 'public'``. Razon: la
cuenta de GitHub Actions es gratuita y el proyecto no migrara a
premium. Si el repositorio se hiciera privado, el job pesado se
auto-desactiva sin tocar el YAML, evitando consumir cupo. No se
usa job programado (nightly) por el mismo motivo de cupo.

D3 — ``-j 2`` (no ``-j auto``, no ``-j 1``)
--------------------------------------------

``-j auto`` causa OOM (oom-killer del kernel confirmado,
``anon-rss`` ~700MB). ``-j 1`` (serial) funciona pero es el mas
lento. ``-j 2`` se verifico empiricamente: ``build succeeded``,
0 warnings, EXIT 0, sin OOM (log
``d01-verif-j2-20260518T151329``, 1289 lineas). El paralelismo
de Sphinx solo acelera la fase de escritura, parcialmente
serializada por extensiones; el coste de ``-j 2`` frente a auto
es menor que el teorico.

D4 — Correccion de PROC-GOB-013 como tarea interna
---------------------------------------------------

H-N1 (ruta) se corrige como T-001 de esta iniciativa, no como
parche previo, para mantener trazabilidad y respetar el propio
procedimiento de cambios normativos. Se bumpeo 1.0.0 -> 1.0.1
y se anadio entrada de historial.

D5 — Diferimiento de soporte multi-repo (H-N2, H-N3)
-----------------------------------------------------

El meta-modelo de iniciativa no declara repositorio objetivo y
PROC-GOB-013 asume IACT-docs implicitamente. Es un cambio
estructural que afecta a todas las iniciativas futuras del
sistema IACT (IACT-api, IACT-ui, IACT-db). Se difiere a una
iniciativa dedicada. Medida local: esta iniciativa declara
``:repo_objetivo: IACT-docs`` en el meta de todos sus
documentos. El diferimiento es alcance acotado con
justificacion, no deuda oculta.

Hallazgos surgidos durante la ejecucion
========================================

H-EJ1 — Tres hallazgos de auditoria eran falsos positivos
----------------------------------------------------------

La auditoria inicial de ``plantuml_cached.py`` marco seis
hallazgos. La verificacion contra ``scripts/prerender-plantuml.py``
y docutils antes de aplicar cambios determino que A-03, A-04 y
A-05 no son defectos:

* A-03: ``scripts/prerender-plantuml.py`` (D-08) elimina
  deliberadamente el nombre de ``@startuml`` antes de hashear.
  Excluir el argumento del hash es intencional y coordinado.
  "Corregirlo" habria desincronizado la cache de 1211 SVG y
  reintroducido el OOM.
* A-04: el offset para ``nested_parse`` de una caption de opcion
  es ambiguo en docutils; ``content_offset`` es convencion
  aceptada.
* A-05: la URI con prefijo ``/`` es patron deliberado
  documentado en el propio codigo para resolucion estilo
  ``_static``.

Leccion: verificar contra el codigo real antes de aplicar evito
introducir un bug grave (A-03) creyendo que se eliminaba deuda.
Un analisis con falsos positivos es deuda documental; se
corrigio el documento de analisis en consecuencia.

Verificacion post-ejecucion con evidencia
==========================================

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Item
     - Evidencia
   * - validate.yml
     - 0 ocurrencias ``-j auto``; 2 de ``-j 2``; ``make clean``
       solo en job completo; triggers ``[develop, main]``;
       guard de visibilidad en ``validate-full``.
   * - PROC-GOB-013
     - Paso 1 usa ruta correcta; meta ``:version: 1.0.1``;
       entrada de historial 1.0.1; unica mencion de la ruta
       vieja es la cita historica (trazabilidad correcta, no
       uso activo).
   * - plantuml_cached.py
     - ``python3 -m py_compile`` OK; ``parallel_write_safe:
       False``; ``logger.info`` de hit; dos ``logger.warning``
       de estilos; ``_diagram_hash`` sin cambios (cache
       sincronizada).
   * - D-01
     - W1=1, W2=1, W3-cron=0, linea 79 ``.. code-block:: bash``;
       build ``-W -j 2`` previo = ``build succeeded`` 0
       warnings EXIT 0.
   * - Build integrado final
     - Pendiente: se ejecuta en el local del usuario antes del
       push (PROC-GOB-013 Fase 3 paso 5). Criterio: ``build
       succeeded`` 0 warnings con todos los cambios integrados.
