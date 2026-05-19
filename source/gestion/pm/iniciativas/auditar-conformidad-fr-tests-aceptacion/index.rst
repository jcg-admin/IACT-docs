.. meta::
   :artefacto: INICIATIVA-AUDITAR-CONFORMIDAD-FR-TESTS-ACEPTACION
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:46:37
   :ultimo_cambio: 2026-05-19T20:46:37
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-auditar-conformidad-fr-tests-aceptacion:

==============================================================
Iniciativa: Auditar Conformidad FR -> Tests de Aceptacion
==============================================================

Trabajo de orden superior: verificar que cada FR
(``fr-NNN-NN-*.rst``) tiene al menos un test que valida
explicitamente su **criterio de aceptacion**, no solo que
toca el codigo asociado.

Resultado calibrado: la trazabilidad **explicita** FR ->
test es **0%** (0/103 FRs in-scope tienen referencia a su
TST-FR en codigo api). Los 1378 tests passing existen y
ejercitan flujos, pero ninguno declara su correspondencia
1-a-1 con un FR especifico.

Diferencia con cobertura UC -> implementacion (100% segun
``aclarar-uc-047-resolver-segmento``): la cobertura UC
mide presencia de codigo; esta auditoria mide
**trazabilidad demostrable** entre requisito y prueba.

.. toctree::
   :maxdepth: 1

   deep-analisis-auditar-conformidad-fr-tests-aceptacion
