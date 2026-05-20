.. meta::
   :artefacto: INICIATIVA-SANEAR-DEUDA-RUNTIME-MULTIREPO
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T19:07:37
   :ultimo_cambio: 2026-05-19T19:12:52
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-sanear-deuda-runtime-multirepo:

==============================================================
Iniciativa: Sanear Deuda Runtime Multi-Repo
==============================================================

Cierra cuatro deudas registradas en iniciativas previas
mediante cambios reales de codigo y configuracion en tres
repos del sistema (IACT, IACT-api, IACT-ui). Tambien
re-ejecuta la suite pytest sin filtros para cuantificar la
brecha real entre los 1397 tests colectados y los 223 que la
iniciativa hermana ``habilitar-pytest-iact-api`` valido con
``-m unit``.

Tiene ``:repo_objetivo: multiple`` (IACT-api + IACT-ui +
IACT). La documentacion vive en IACT-docs por D3 Modelo C
de PROC-GOB-013 v2.0.0.

.. toctree::
   :maxdepth: 1

   alcance-sanear-deuda-runtime-multirepo
   tareas-y-progreso-sanear-deuda-runtime-multirepo
   decisiones-sanear-deuda-runtime-multirepo
