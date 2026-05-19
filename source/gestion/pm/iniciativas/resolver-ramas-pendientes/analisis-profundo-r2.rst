.. meta::
   :artefacto: ANALISIS-PROFUNDO-R2
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-ramas-pendientes
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:46:00
   :ultimo_cambio: 2026-05-18T18:46:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-profundo-r2:

============================================================
Analisis Profundo: Rama R2 (arquitectura-tecnica-content)
============================================================

Contexto
========

R2 = ``feature/arquitectura-tecnica-content``. ahead=8,
behind=713 vs develop. 8 commits unicos sobre un work package
``pipeline-uc-deepening`` que incluye el commit ``fac2e13c``
"Expand UC_SUP_01 to full 12-part spec (benchmark quality)".

Verificacion por archivo: quien tiene la version mas reciente
===============================================================

De 18 archivos ``source/`` que ``git diff`` reporta:

.. list-table::
   :header-rows: 1
   :widths: 16 60 24

   * - Grupo
     - Archivos
     - Veredicto
   * - A (DEV mas nuevo)
     - ``caller/index.rst``, ``casos-uso/index.rst``,
       ``operator/index.rst``, ``supervision/index.rst``,
       ``uc-sup-01/index.rst``
     - develop los modifico despues (05-04..05-07) que R2
       (05-02). Son indices/toctrees. NO se rescatan:
       develop ya evoluciono mas.
   * - B (R2 mas nuevo)
     - 11 contenidos de ``uc-sup-01/`` + ``logs/index.rst``
     - R2 mas reciente. Verificacion de contenido abajo.
   * - C (nuevo en R2)
     - ``uc-sup-01/diagramas-uml.rst``
     - Ausente en develop. Unico de R2.

Verificacion de contenido del Grupo B (sustantivo vs trivial)
==============================================================

Comparacion de magnitud de diff R2 vs develop:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30

   * - Archivo (uc-sup-01/)
     - +lineas
     - -lineas
     - Veredicto
   * - ``actores-precondiciones``
     - 84
     - 12
     - SUSTANTIVO
   * - ``criterios-aceptacion``
     - 209
     - 12
     - SUSTANTIVO
   * - ``datos-involucrados``
     - 210
     - 6
     - SUSTANTIVO
   * - ``excepciones``
     - 283
     - 10
     - SUSTANTIVO
   * - ``flujo-principal``
     - 191
     - 16
     - SUSTANTIVO
   * - ``flujos-alternos``
     - 205
     - 11
     - SUSTANTIVO
   * - ``implementacion-tecnica``
     - 219
     - 6
     - SUSTANTIVO
   * - ``informacion-general``
     - 126
     - 13
     - SUSTANTIVO
   * - ``patrones-diseno``
     - 121
     - 8
     - SUSTANTIVO
   * - ``requisitos-no-funcionales``
     - 140
     - 5
     - SUSTANTIVO
   * - ``testing``
     - 353
     - 9
     - SUSTANTIVO
   * - ``logs/index.rst``
     - 1
     - 1
     - TRIVIAL

Evidencia concreta (``testing.rst``)
=====================================

* develop: 14 lineas. Stub telegrafico: "UT-01: Reason
  validator. IT-01: Silent. IT-02: Whisper. ... 100% de los 8
  CAs."
* R2: 358 lineas. Estrategia de testing completa: clasificacion
  CRITICO (impacto legal + compliance), tabla de cobertura por
  nivel (UT/IT), validacion CA-01..CA-10.

Conclusion del Grupo B: develop tiene **stubs**; R2 tiene la
**spec completa de 12 partes**. Es el trabajo del commit
``fac2e13c`` nunca integrado. Contenido valioso real, no ruido
obsoleto. Caso opuesto a R1.

Hallazgo y riesgo pendiente de verificar
=========================================

Develop modifico los indices del Grupo A el 05-07, *despues*
de R2 (05-02). Antes de declarar "R2 se integra" hay que
descartar una hipotesis: que develop ya haya integrado esta
spec por otra via (reescrita o reubicada) y que los stubs
actuales sean producto de un refactor posterior. Rescatar 11
archivos sin descartar esto arriesgaria duplicar contenido que
develop ya tenga en otra forma.

**Verificacion pendiente (siguiente paso)**: buscar en develop
si el contenido completo de UC-SUP-01 existe en otra ruta o
forma; revisar el historial de los stubs en develop (¿por que
quedaron como stub el 05-01 y los index se tocaron el 05-07?).

Recomendacion preliminar
========================

* Grupo A (5 indices): no rescatar (develop mas nuevo).
* Grupo B (11 contenidos): rescate candidato fuerte, sujeto a
  la verificacion pendiente.
* Grupo C (``diagramas-uml.rst``): rescate (unico, ausente en
  develop).
* ``logs/index.rst``: diferencia trivial (+1/-1), no priorizar.

Decision de integracion supeditada a resolver el riesgo
pendiente. No se integra a ciegas.
