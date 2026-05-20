.. meta::
   :artefacto: INICIATIVA-DECLARAR-TST-REF-EN-58-FRS-SIN-MARCAR
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:46:37
   :ultimo_cambio: 2026-05-19T20:46:37
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-declarar-tst-ref-en-58-frs-sin-marcar:

==============================================================
Iniciativa: Declarar TST ref en 58 FRs (resultado: discovery)
==============================================================

.. admonition:: Resolucion: el gap no existe
   :class: important

   El claim de
   ``auditar-conformidad-fr-tests-aceptacion`` que afirmaba
   "58/103 FRs sin declaracion de test esperado" resulto
   **falso negativo de grep case-sensitive**. El grep
   buscaba ``TST-FR-`` (uppercase) pero los 58 FRs usan
   ``TST-fr-NNN-NN`` (lowercase con guion). Case-insensitive
   confirma: **103/103 FRs declaran un TST ref**.

   La iniciativa pivota de "declarar lo que falta" a
   "documentar el hallazgo y la inconsistencia de naming
   real encontrada".

   Hallazgo lateral: **dos convenciones TST coexisten en
   docs**, particionadas por dominio:

   * Uppercase ``TST-FR-NNN.NN``: 45 FRs (auth 21,
     users 17, access 7).
   * Lowercase ``TST-fr-NNN-NN``: 58 FRs (permissions 22,
     reports 16, logs 7, alerts 5, pipeline 4, audit 4).

   Es deuda metodologica menor: misma semantica con dos
   sintaxis. Probablemente artefacto de redaccion en
   ciclos distintos.

.. toctree::
   :maxdepth: 1

   deep-analisis-declarar-tst-ref-en-58-frs-sin-marcar
