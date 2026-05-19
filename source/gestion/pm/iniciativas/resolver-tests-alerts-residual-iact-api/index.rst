.. meta::
   :artefacto: INICIATIVA-RESOLVER-TESTS-ALERTS-RESIDUAL-IACT-API
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:25:00
   :ultimo_cambio: 2026-05-19T21:25:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-resolver-tests-alerts-residual-iact-api:

==============================================================
Iniciativa: Resolver Tests Alerts Residual IACT-api
==============================================================

P1 del plan maestro #2. Cierra las 8 fallas residuales del
bucket alerts (test_viewsets 2, test_models 4,
test_services 1, test_scheduler 1).

**Resultado:** 7 fallas resueltas + 1 declarada deuda
explicita (skipTest). ``apps/alerts/`` pasa de 31/39 a
**38/38 + 1 skipped**. Full suite global pasa de 12 a 4
failed, **99.71% pass rate** (1392/1397).

7 causas raiz distintas:

* self-detection en grep de imports prohibidos
* 2 cambios en __str__ no reflejados en tests (Message,
  AlertConfiguration)
* unique_together removido sin actualizar test
* 2 string-case mismatches "maximo" vs "Máximo"
* URL hyphen vs underscore en @action
* Response serializer con write_only field no marcado

Cambio de codigo productivo:

* ``apps/alerts/serializers/message_serializers.py``
  recipient_ids agregado ``write_only=True`` para evitar
  AttributeError al serializar response post-save.

Commit IACT-api ``469b52e``.

.. toctree::
   :maxdepth: 1

   tareas-y-progreso-resolver-tests-alerts-residual-iact-api
