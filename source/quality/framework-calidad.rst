.. meta::
 :artefacto: QA_002
 :tipo: Framework
 :dominio: quality
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Medio

============================
Framework de Calidad
============================

Pipeline de validacion automatizada del sistema IACT.

1. Stack
========

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Tipo
   - Herramientas
 * - Linters Python
   - ruff, mypy
 * - Linters JS/TS
   - ESLint, Prettier
 * - Tests Python
   - pytest + pytest-django + factory-boy
 * - Tests JS
   - Jest + Testing Library
 * - Coverage
   - coverage.py + Codecov
 * - Security
   - Bandit (Python), npm audit (JS)
 * - CI/CD
   - GitHub Actions / GitLab CI
 * - Sphinx build
   - sphinx-build con ``-W`` en CI (CNST: build limpio)

2. Pipeline CI
==============

.. code-block:: text

 PR submitted
 ↓
 Linters → fail-fast si format/style violations
 ↓
 Unit tests → coverage >= 80%
 ↓
 Integration tests → DB en docker
 ↓
 E2E tests (solo en main)
 ↓
 Sphinx build con -W (validar docs)
 ↓
 Security scan
 ↓
 Merge / Deploy

3. Verificacion de cumplimiento de CNSTs
=========================================

El framework de calidad verifica automaticamente cumplimiento de
restricciones canonicas:

- :doc:`/normativa/restricciones/CNST_009_Autenticacion_DRF_Obligatoria`
  → tests verifican ``permission_classes`` declaradas
- :doc:`/normativa/restricciones/CNST_011_Throttling_Obligatorio_en_Endpoints_Publicos`
  → tests verifican rate limits
- :doc:`/normativa/restricciones/CNST_026_PII_Prohibida_en_Logs_y_Auditoria`
  → linter de logs sanitiza PII
- :doc:`/normativa/restricciones/CNST_032_Menu_Dinamico_Obligatorio`
  → E2E test verifica `obtener_menu_usuario`
- :doc:`/normativa/restricciones/CNST_033_Vocabulario_Unificado_RBAC`
  → linter custom rechaza "Capacidad" en codigo nuevo
