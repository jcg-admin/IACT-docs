.. meta::
   :artefacto: INICIATIVA-ENUMERAR-OTROS-UCS-INCLUSION
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:55:00
   :ultimo_cambio: 2026-05-19T21:55:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-enumerar-otros-ucs-inclusion:

==============================================================
Iniciativa: Enumerar Otros UCs Inclusion
==============================================================

P2 del plan maestro #14. Derivada del descubrimiento en
``aclarar-uc-047-resolver-segmento``: el prefijo
``UC_INC_*`` denota UCs de inclusion (Larman) — operaciones
invocadas por otros UCs como paso, no por actor directo.

Pregunta: ¿hay otros UCs ``UC_INC_*`` ademas de
``UC_INC_RPT_01`` (uc-047) que la auditoria original pudo
haber contado como user-facing por error?

Resultado: NO
==============

Aplicando el protocolo
``grep-validated-audit.md`` (case-insensitive, regex amplio,
muestra de ambos buckets):

.. code-block:: bash

   # Docs
   grep -rohE "UC_INC_[A-Z]+_[0-9]+" \\
     /home/user/IACT-docs/source/requisitos/ \\
     2>/dev/null | sort -u

Output:

::

   UC_INC_RPT_01

.. code-block:: bash

   # IACT-api
   grep -rohE "UC_INC_[A-Z]+_[0-9]+" \\
     /home/user/IACT-api/callcentersite/apps/ \\
     2>/dev/null | sort -u
   # (vacio — 0 ocurrencias)

   # IACT-ui
   grep -rohE "UC_INC_[A-Z]+_[0-9]+" \\
     /home/user/IACT-ui/src/ \\
     2>/dev/null | sort -u
   # (vacio — 0 ocurrencias)

**El unico UC de inclusion en todo el sistema es
``UC_INC_RPT_01``** (uc-047-resolver-segmento-usuario,
declarado OUT del scope por el sponsor en
``aclarar-uc-047-resolver-segmento``).

Implicaciones
===============

* La cobertura agregada **no cambia**: sigue 56 in-scope
  + uc-047 OUT = 57 declarados in
  ``requisitos-funcionales/``, ahora 61 tras
  documentar-ucs-implementados-no-declarados.
* La iniciativa hermana
  ``separar-ucs-inclusion-de-user-facing`` (plan #13)
  tiene **trabajo minimo**: solo afecta a uc-047 (un
  archivo). Puede degradarse a un edit puntual en lugar
  de iniciativa estructural.

Iniciativa hermana derivada
=============================

* ``separar-ucs-inclusion-de-user-facing`` puede
  reducirse a:

  1. Mover uc-047-resolver-segmento-usuario/ a
     ``reports/inclusion/uc-047-resolver-segmento-usuario/``
     o renombrar a ``reports/uc-inc-047-*``.
  2. Actualizar toctree padre.
  3. Documentar convencion en proc-gob-015 (o nota en
     proc-gob-013).
