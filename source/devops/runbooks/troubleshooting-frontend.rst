.. meta::
   :artefacto: TROUBLESHOOTING-FRONTEND
   :tipo: Documentacion operativa
   :dominio: devops
   :subdominio: frontend
   :repo_origen: IACT-ui
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19
   :ultimo_cambio: 2026-05-19
   :autor: NestorMonroy
   :clasificacion: Interno

.. admonition:: Documento portado desde repo IACT-ui
   :class: note

   Origen: ``/home/user/IACT-ui/docs/TROUBLESHOOTING.md``. Portado a IACT-docs en
   iniciativa ``integrar-docs-internos-multi-repo`` (2026-05-19).
   La fuente original permanece en el repo como historico.



Troubleshooting Guide
=====================

Common issues and solutions.

Port 3000 Already in Use
------------------------

.. code-block:: bash

   PORT=3001 npm start

Dependencies Issues
-------------------

.. code-block:: bash

   rm -rf node_modules package-lock.json
   npm install

Tests Failing
-------------

.. code-block:: bash

   npm test -- --clearCache
   npm test

Styles Not Loading
------------------

- Check CSS Modules import syntax
- Verify ``.module.scss`` extension
- Check webpack config

Components Not Rendering
------------------------

- Check barrel export (index.jsx)
- Verify import paths
- Check console for errors

Redux State Not Updating
------------------------

- Check action dispatch
- Verify reducer implementation
- Check middleware config

Build Errors
------------

.. code-block:: bash

   npm run build
   # Check error messages
   # Usually: missing dependencies or syntax errors

Performance Issues
------------------

- Check Network tab in DevTools
- Look for large assets
- Enable code splitting
- Check for console warnings

----

See `Setup Guide <./SETUP.md>`_ for more help.

