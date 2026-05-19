.. meta::
   :artefacto: CONTRIBUIR-FRONTEND
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

   Origen: ``/home/user/IACT-ui/docs/CONTRIBUTING.md``. Portado a IACT-docs en
   iniciativa ``integrar-docs-internos-multi-repo`` (2026-05-19).
   La fuente original permanece en el repo como historico.



Contributing Guide
==================

How to contribute to IACT.

Getting Started
---------------

1. Fork the repository
2. Clone your fork
3. Create a feature branch: ``git checkout -b feature/my-feature``
4. Make your changes
5. Run tests: ``npm test``
6. Commit: ``git commit -m "feat: add my feature"``
7. Push: ``git push origin feature/my-feature``
8. Create Pull Request

Code Style
----------

- Use 2 spaces for indentation
- Use camelCase for variables
- Use PascalCase for components
- Use SCREAMING_SNAKE_CASE for constants

Testing Requirements
--------------------

- Write tests for all components
- Write tests for Redux slices
- Maintain 100% test pass rate
- Run ``npm test`` before committing

Commit Messages
---------------

Format: ``type(scope): description``

Types:
- ``feat`` - New feature
- ``fix`` - Bug fix
- ``docs`` - Documentation
- ``style`` - Code style
- ``refactor`` - Code refactoring
- ``test`` - Test files

Example:

.. code-block:: text

   feat(header): add user avatar to header

Pull Request Process
--------------------

1. Update documentation
2. Add/update tests
3. Ensure all tests pass
4. Request code review
5. Address feedback

----

Thank you for contributing!

