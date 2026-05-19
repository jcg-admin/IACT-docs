.. meta::
   :artefacto: DEBT_002
   :tipo: Deuda Tecnica
   :dominio: risks-technical-debt
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T23:28:16
   :ultimo_cambio: 2026-05-18T23:28:16
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deuda-integracion-wp-tmp:

==================================================
Deuda Tecnica: Integracion de contenido wp-tmp
==================================================

Origen
======

Iniciativa ``resolver-ramas-pendientes`` (cerrada
2026-05-18). Resolvio el estado de las 5 ramas pendientes y
preservo el contenido con valor no integrado en
``source/gestion/pm/iniciativas/resolver-ramas-pendientes/wp-tmp/``.

La **ejecucion** de la integracion de ese contenido a su
ubicacion final en ``source/`` quedo fuera del alcance de
aquella iniciativa (decision documentada, D6). El analisis de
**como** integrarlo si se completo
(``analisis-integracion-wp-tmp``); esta deuda registra el
trabajo de ejecucion pendiente para que no quede invisible.

Catalogo
========

.. list-table::
   :widths: 12 18 50 20
   :header-rows: 1

   * - ID
     - Origen
     - Descripcion
     - Estado
   * - DEBT-008
     - resolver-ramas-pendientes
     - Integrar a ``source/`` los 12 archivos de R2 (spec
       UC-SUP-01: develop tiene stubs de 10-19 lineas,
       wp-tmp tiene la spec completa de 90-358). Riesgo
       BAJO: nomenclatura ya correcta, ruta existente.
       Requiere verificacion de toctree de
       ``uc-sup-01/index`` por archivo y build 0 warnings.
     - Activa
   * - DEBT-009
     - resolver-ramas-pendientes
     - Integrar los 8 archivos nuevos de R3 (incluye
       ``modelo-rbac-iact.rst`` 2897 lineas, v5.4.0 M2M
       verificado vigente; ``cnst-030-sod``; 6 diagramas
       UML). Riesgo MEDIO: cada nuevo debe enlazarse en su
       toctree o genera warning de huerfano.
     - Activa
   * - DEBT-010
     - resolver-ramas-pendientes
     - Decidir e integrar selectivamente los 68 archivos de
       R3 que difieren de develop. Riesgo ALTO: "mas
       reciente por fecha" no implica "mejor contenido";
       requiere analisis de sustancia (diff de magnitud)
       archivo por archivo ANTES de integrar. No en bloque.
     - Activa
   * - DEBT-011
     - resolver-ramas-pendientes
     - Decidir destino de ``architecture-constraints.md``
       (R1): Markdown/ingles/borrador obsoleto. No es copia
       directa (contradice politica RST-only). Opciones:
       conservar como evidencia en wp-tmp/ o reescribir
       como RST historico en espanol.
     - Activa

Insumo disponible
=================

El analisis de como abordar cada item ya esta hecho en
:doc:`/gestion/pm/iniciativas/resolver-ramas-pendientes/analisis-integracion-wp-tmp`,
con clasificacion por riesgo y estrategia de orden de
ejecucion (R2 primero por bajo riesgo, luego R3 nuevos, luego
R3 que difieren con analisis de sustancia, R1 al final). Esta
deuda no requiere re-analisis: requiere ejecucion planificada
con verificacion de build por paso.

Restriccion
===========

Toda integracion debe pasar ``sphinx-build -W -j 2`` con 0
warnings antes de commitear. El modo de fallo mas probable es
un documento anadido sin enlazar en su toctree (warning de
huerfano); el analisis de origen exige verificacion de toctree
por archivo precisamente para prevenirlo.
