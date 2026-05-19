.. meta::
   :artefacto: INICIATIVA-SEPARAR-UCS-INCLUSION-DE-USER-FACING
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T22:00:00
   :ultimo_cambio: 2026-05-19T22:00:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-separar-ucs-inclusion-de-user-facing:

==============================================================
Iniciativa: Separar UCs Inclusion de User-Facing
==============================================================

P3 del plan maestro #13. Reorganiza estructuralmente los UCs
de inclusion (``UC_INC_*`` per Larman) en subdirectorio
``inclusion/`` dentro de su dominio, para evitar la
confusion detectada en
``aclarar-uc-047-resolver-segmento`` y
``adoptar-protocolo-grep-validado-en-auditorias``.

Cambios aplicados
==================

* Movido (via ``git mv`` para preservar historial):
  ``source/requisitos/requisitos-funcionales/reports/uc-047-resolver-segmento-usuario``
  → ``source/requisitos/requisitos-funcionales/reports/inclusion/uc-047-resolver-segmento-usuario``.
* Nuevo archivo
  ``source/requisitos/requisitos-funcionales/reports/inclusion/index.rst``
  declara la subseccion "UCs de inclusion" con su
  toctree y nota explicativa.
* ``reports/index.rst`` separa el toctree principal
  (user-facing 15 UCs) de la subseccion de inclusion
  (1 UC: uc-047) via toctree con
  ``:caption: UCs de inclusion``.

Resultado:

* Sphinx build limpio (0 warnings).
* La estructura visual distingue user-facing vs
  inclusion sin renombrar el directorio uc-047 (preserva
  identificador).
* Cualquier UC_INC futuro va al subdirectorio
  ``inclusion/`` de su dominio respectivo.

Convencion formalizada (ad-hoc por ahora)
============================================

* **UCs user-facing**: viven directamente en
  ``requisitos-funcionales/{dominio}/uc-NNN-*/``.
* **UCs de inclusion**: viven en
  ``requisitos-funcionales/{dominio}/inclusion/uc-NNN-*/``.
* Markers en codigo: user-facing usan
  ``UC_<DOM>_<NN>``; inclusion usan
  ``UC_INC_<DOM>_<NN>``.

Formalizar en proc-gob-013 v2.1.0 o nuevo
``proc-gob-015-ucs-inclusion`` queda como **iniciativa
candidata hermana** ``formalizar-convencion-inclusion-en-proc-gob``
cuando el sponsor decida prioridad. Por ahora la convencion
queda **documentada en este index** y aplicada a uc-047
como ejemplo unico.

Aplicabilidad
==============

Solo uc-047 esta afectado (verificado por
``enumerar-otros-ucs-inclusion``: 1 UC_INC en todo el
sistema). Si aparecen mas UCs_INC en el futuro, se
aplican a su ``{dominio}/inclusion/`` correspondiente.

.. toctree::
   :maxdepth: 1

   tareas-y-progreso-separar-ucs-inclusion-de-user-facing
