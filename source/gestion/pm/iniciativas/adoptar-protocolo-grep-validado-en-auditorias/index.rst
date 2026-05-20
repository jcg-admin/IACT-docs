.. meta::
   :artefacto: INICIATIVA-ADOPTAR-PROTOCOLO-GREP-VALIDADO-EN-AUDITORIAS
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:55:43
   :ultimo_cambio: 2026-05-19T20:55:43
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-adoptar-protocolo-grep-validado-en-auditorias:

==============================================================
Iniciativa: Adoptar Protocolo Grep-Validado en Auditorias
==============================================================

Meta-iniciativa metodologica que codifica la leccion epistemica
extraida de **dos falsos claims** producidos por grep ciego en
auditorias previas de la sesion 2026-05-19:

1. ``UC_RPT_05/06 sin implementacion`` — invalidado por
   ``implementar-uc-rpt-05-06-programacion-reportes`` (asuncion
   de mapping lineal).
2. ``58/103 FRs sin TST ref`` — invalidado por
   ``declarar-tst-ref-en-58-frs-sin-marcar`` (asuncion de case).

Ambos eran claims SPECULATIVE disfrazados de PROVEN: el grep
"probaba" 0 hits, pero la regex era defectuosa.

**Entregable doble:**

1. ``.claude/rules/grep-validated-audit.md`` — regla cargada
   automaticamente en cada sesion. Codifica el protocolo,
   anti-patrones y checklist pre-publicacion.
2. Esta iniciativa con su deep-analysis — narrativa para
   contexto historico.

.. toctree::
   :maxdepth: 1

   deep-analisis-adoptar-protocolo-grep-validado-en-auditorias
