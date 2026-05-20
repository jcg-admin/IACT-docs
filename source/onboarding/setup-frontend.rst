.. meta::
   :artefacto: SETUP-FRONTEND
   :tipo: Guia
   :dominio: onboarding
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

   Origen: ``/home/user/IACT-ui/docs/SETUP.md``. Portado a IACT-docs en
   iniciativa ``integrar-docs-internos-multi-repo`` (2026-05-19).
   La fuente original permanece en el repo como historico.



Setup Guide
===========

Complete guide to set up IACT locally for development.

Prerequisites
-------------

- Node.js 16+ (recommend 18 LTS)
- npm 8+ or yarn 3+
- Git
- A code editor (VS Code recommended)

Installation
------------

1. Clone Repository
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/your-org/iact.git
   cd iact

2. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   npm install

3. Start Development Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   npm start

Open `http://localhost:3000 <http://localhost:3000>`_ to view in browser.

Available Scripts
-----------------

Development
~~~~~~~~~~~

.. code-block:: bash

   npm start           # Start development server
   npm test            # Run tests in watch mode
   npm test -- --coverage  # Run tests with coverage

Build
~~~~~

.. code-block:: bash

   npm run build       # Build for production
   npm run build:analyze  # Analyze bundle size

Code Quality
~~~~~~~~~~~~

.. code-block:: bash

   npm run lint        # Run ESLint
   npm run format      # Format code with Prettier

Project Structure
-----------------

.. code-block:: text

   iact/
   ├── docs/                    # Documentation
   ├── src/
   │   ├── components/          # Reusable components
   │   ├── layouts/             # Layout components
   │   ├── pages/               # Page components
   │   ├── redux/               # Redux store and slices
   │   ├── router/              # Route configuration
   │   ├── hooks/               # Custom hooks
   │   ├── styles/              # Global styles
   │   ├── App.jsx              # Root component
   │   └── index.js             # Entry point
   ├── __tests__/               # Test files
   ├── package.json
   ├── webpack.config.js
   └── jest.config.js

Configuration Files
-------------------

webpack.config.js
~~~~~~~~~~~~~~~~~

Webpack bundler configuration with:
- CSS Modules support
- Babel transpilation
- Development/production modes

jest.config.js
~~~~~~~~~~~~~~

Jest testing configuration with:
- jsdom test environment
- CSS module mocking

jsconfig.json
~~~~~~~~~~~~~

Path aliases for clean imports:

.. code-block:: javascript

   @components  → src/components
   @layouts     → src/layouts
   @pages       → src/pages
   @hooks       → src/hooks
   @redux       → src/redux
   @router      → src/router
   @styles      → src/styles
   @utils       → src/utils

Environment Setup
-----------------

Create ``.env`` file in project root:

.. code-block:: text

   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_USE_MOCKS=true

Troubleshooting
---------------

Port 3000 already in use
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Use different port
   PORT=3001 npm start

Node modules issues
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clear cache and reinstall
   rm -rf node_modules package-lock.json
   npm install

Tests failing
~~~~~~~~~~~~~

.. code-block:: bash

   # Clear Jest cache
   npm test -- --clearCache

See `Troubleshooting Guide <./TROUBLESHOOTING.md>`_ for more issues.

----

Next: `Architecture Overview <./ARCHITECTURE.md>`_

