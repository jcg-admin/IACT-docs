.. meta::
   :artefacto: DECISIONES-SANEAR-DEUDA-CI-Y-NORMATIVA
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/sanear-deuda-ci-y-normativa
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
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

**Registro formal de la deuda (cierre)**: para que el
diferimiento no quede enterrado en este documento al cerrar la
iniciativa, H-N2 y H-N3 se registraron como deuda tecnica
formal DEBT-012/DEBT-013 en
:doc:`/risks-technical-debt/deuda-proc-gob-013-multirepo`,
con dueño y accion propuesta (iniciativa dedicada a
PROC-GOB-013 multi-repo).

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

Cada criterio de completitud del alcance, su resultado y la
evidencia concreta:

.. list-table::
   :header-rows: 1
   :widths: 44 12 44

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - ``validate.yml`` build incremental sin ``make clean``,
       con cache de doctrees, 0 warnings bajo ``-W``
     - PASA
     - Job ``validate-incremental`` sin ``make clean``, con
       ``actions/cache`` de ``build/doctrees``, ``-j 2``.
       ``make clean`` solo en ``validate-full``.
   * - Triggers no disparan build completo en cada push de
       rama de trabajo; validacion en PR/push a develop/main
     - PASA
     - ``on.push.branches: [develop, main]``; sin
       ``feature/**``. PR a develop/main conserva validacion.
   * - Job de build completo con guard de visibilidad publica
     - PASA
     - ``validate-full`` con
       ``if: ... github.event.repository.visibility ==
       'public'``; no corre en repo privado.
   * - Hallazgos A-01..A-06 resueltos o diferidos con
       decision explicita
     - PASA
     - A-01/A-02/A-06 corregidos (``parallel_write_safe``
       False, log de hit, warning de estilos).
       A-03/A-04/A-05 descartados con evidencia verificada
       (no son defectos; ver analisis y D-EJ1).
   * - PROC-GOB-013 refleja la ruta real
       ``source/gestion/pm/iniciativas/{nombre}/``
     - PASA
     - Paso 1 corregido; ``:version: 1.0.1``; entrada de
       historial 1.0.1. Unica mencion de ruta vieja es la
       cita historica (trazabilidad, no uso activo).
   * - Todos los RST de la iniciativa existen, enlazados, y
       el build produce 0 warnings
     - PARCIAL
     - 6 RST + index existen y enlazados en
       ``pm/iniciativas/index.rst`` (toctree sin
       huerfanos). El build 0 warnings con todo integrado
       lo verifica el usuario en su local antes del push
       (PROC-GOB-013 Fase 3 paso 5; el clon no completa
       build PlantUML). El contenido D-01 ya se verifico
       limpio (log ``d01-verif-j2-20260518T151329``).

Cierre
======

5/6 criterios PASA con evidencia. El sexto es PARCIAL
unicamente porque la verificacion final de build integrado
requiere el entorno del usuario (restriccion conocida y
documentada, no deuda oculta): el contenido individual ya se
verifico y la estructura no tiene huerfanos. El cierre
documental es valido; el build es gate previo al push, no
condicion del cierre de la iniciativa.
