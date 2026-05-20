.. meta::
   :artefacto: DEPLOYMENT-FRONTEND
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

   Origen: ``/home/user/IACT-ui/docs/DEPLOYMENT.md``. Portado a IACT-docs en
   iniciativa ``integrar-docs-internos-multi-repo`` (2026-05-19).
   La fuente original permanece en el repo como historico.



Deployment Guide
================

Guide for deploying to production.

Build for Production
--------------------

.. code-block:: bash

   npm run build

Creates ``dist/`` folder with optimized build.

Environment Variables
---------------------

Create ``.env.production``:

.. code-block:: text

   REACT_APP_API_URL=https://api.prod.example.com
   REACT_APP_USE_MOCKS=false

Deployment Options
------------------

1. Vercel
~~~~~~~~~

.. code-block:: bash

   npm install -g vercel
   vercel

2. Netlify
~~~~~~~~~~

.. code-block:: bash

   npm run build
   # Drag and drop dist/ folder to Netlify

3. Docker
~~~~~~~~~

Create ``Dockerfile``:

.. code-block:: dockerfile

   FROM node:18
   WORKDIR /app
   COPY . .
   RUN npm install && npm run build
   EXPOSE 3000
   CMD ["npm", "start"]

4. AWS S3 + CloudFront
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   npm run build
   aws s3 sync dist/ s3://my-bucket

Pre-Deployment Checklist
------------------------

- [ ] All tests passing
- [ ] No console errors
- [ ] Production environment variables set
- [ ] API endpoints configured
- [ ] Performance optimized
- [ ] Security headers configured
- [ ] Analytics configured
- [ ] Error monitoring configured

Performance Optimization
------------------------

- Enable gzip compression
- Cache static assets
- CDN for images
- Code splitting enabled
- Minification enabled

Monitoring
----------

- Set up error tracking (Sentry)
- Set up analytics (GA)
- Set up performance monitoring
- Configure alerts

----

See `Setup Guide <./SETUP.md>`_ for more details.

