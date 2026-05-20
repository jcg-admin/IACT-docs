.. meta::
   :artefacto: INICIATIVA-ACLARAR-UC-047-RESOLVER-SEGMENTO
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:35:00
   :ultimo_cambio: 2026-05-19T20:35:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-aclarar-uc-047-resolver-segmento:

==============================================================
Iniciativa: Aclarar uc-047 (Resolver Segmento Usuario)
==============================================================

.. admonition:: Resolucion: uc-047 OUT del scope
   :class: important

   Resuelve el unico gap ambiguo identificado en
   ``verificar-mapping-docs-codigo-todos-los-dominios``.
   Conclusion: ``uc-047-resolver-segmento-usuario`` **no es
   un UC user-facing** sino un **UC de inclusion**
   (``UC_INC_RPT_01``, prefijo ``INC`` = inclusion). El
   sponsor confirma que el "segmento de usuario" queda
   fuera del scope (conceptualmente ligado al routing
   caller/operator declarados OUT en el scope original).

   **Efecto en la cobertura agregada:**

   * Antes: 56-57 / 57 in-scope con marker (98-100%).
   * Despues: **57 - 1 = 56 in-scope**, todos con
     implementacion verificable = **100% cobertura
     in-scope api**.

.. toctree::
   :maxdepth: 1

   deep-analisis-aclarar-uc-047-resolver-segmento
