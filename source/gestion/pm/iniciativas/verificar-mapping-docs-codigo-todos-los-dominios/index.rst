.. meta::
   :artefacto: INICIATIVA-VERIFICAR-MAPPING-DOCS-CODIGO-TODOS-LOS-DOMINIOS
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:29:37
   :ultimo_cambio: 2026-05-19T20:29:37
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-verificar-mapping-docs-codigo-todos-los-dominios:

==============================================================
Iniciativa: Verificar Mapping Docs <-> Codigo (12 dominios)
==============================================================

Iniciativa de investigacion derivada de
``implementar-uc-rpt-05-06`` (que descubrio el bug de mapping
lineal asumido). Esta iniciativa verifica el mapping para los
**12 dominios** del sistema y produce la tabla maestra
``uc-docs <-> UC_<DOM>_<NN>-codigo`` con discrepancias
identificadas.

Resultado: el deep-analysis original de
``auditar-cobertura-uc-implementacion`` subreporto cobertura
porque (a) asumio mapping lineal y (b) no detecto markers
cross-dominio. La cobertura **real** in-scope api es
**~98% (56/57 UCs)**; la unica brecha residual estricta es
``uc-047-resolver-segmento-usuario`` sin marker directo
(posiblemente cubierto por UC_RPT_17 sin marker explicito).

.. toctree::
   :maxdepth: 1

   deep-analisis-verificar-mapping-docs-codigo-todos-los-dominios
