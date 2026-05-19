.. meta::
   :artefacto: INICIATIVA-HABILITAR-JEST-IACT-UI
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-ui
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:52:11
   :ultimo_cambio: 2026-05-19T18:52:11
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-habilitar-jest-iact-ui:

==============================================================
Iniciativa: Habilitar jest en IACT-ui
==============================================================

Completa la cadena ``db -> api -> ui`` al dejar el eslabon
``ui`` runnable: ``npm test`` ejecuta la suite Jest completa
con 0 fallas. Habilita validar cambios futuros en el frontend
contra esta base de pruebas (React 18 + Redux Toolkit +
Webpack 5).

Patron Modelo C-runtime (PROC-GOB-013 v2.0.0 D3) con
``:repo_objetivo: IACT-ui``: documentacion en IACT-docs,
ejecucion en IACT-ui. Sin commits en IACT-ui porque el trabajo
es runtime puro (``npm install`` reconstruye
``node_modules/``, ``npm test`` ejecuta la suite).

.. toctree::
   :maxdepth: 1

   alcance-habilitar-jest-iact-ui
   tareas-y-progreso-habilitar-jest-iact-ui
   decisiones-habilitar-jest-iact-ui
