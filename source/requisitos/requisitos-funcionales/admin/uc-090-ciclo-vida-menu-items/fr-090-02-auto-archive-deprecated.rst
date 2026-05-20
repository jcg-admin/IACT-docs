.. meta::
 :artefacto: FR-090.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/admin
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-090-02:

============================================================
FR-090.02: Auto-archivo de MenuItems DEPRECATED tras 90 dias
============================================================

1. Identificacion
-----------------

* **ID:** FR-090.02
* **UC origen:** UC-090 (UC_ADM_05) — FA-04
* **Modulo:** MOD_Admin
* **Tipo:** Tarea programada
* **Actor:** Sistema (job scheduler)

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE archivar automaticamente los
MenuItems que llevan mas de ``AUTO_ARCHIVE_DAYS=90`` dias en
estado ``DEPRECATED``, transicionandolos a ``ARCHIVED`` sin
intervencion humana.

**Comportamiento implementado:**

* ``MenuLifecycleService.AUTO_ARCHIVE_DAYS = 90``.
* ``MenuLifecycleService.auto_archive_menu_items()`` (helper):

  - Selecciona ``MenuItem.objects.filter(status='DEPRECATED',
    deprecated_at__lte=now - timedelta(days=90))``.
  - Para cada item ejecuta ``transition(item, 'ARCHIVED')``.

* Ejecucion automatica: depende del scheduler del proyecto.
  No esta en CNST-013 (no Celery) — se ejecuta via APScheduler
  o cron interno.

3. Criterios de aceptacion
--------------------------

* CA-01: item en DEPRECATED con
  ``deprecated_at < now - 90 dias`` -> auto-transicion a
  ARCHIVED.
* CA-02: item en DEPRECATED con
  ``deprecated_at > now - 90 dias`` -> permanece en DEPRECATED.
* CA-03: ejecucion es idempotente — re-correr no duplica
  archivados.

4. Trazabilidad
---------------

* **Codigo:** ``apps/access/services/menu_lifecycle_service.py
  auto_archive_menu_items()``.
* **Constante:** ``AUTO_ARCHIVE_DAYS = 90``.
