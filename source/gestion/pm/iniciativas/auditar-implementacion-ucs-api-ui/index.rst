.. meta::
   :artefacto: INICIATIVA-AUDITAR-IMPLEMENTACION-UCS-API-UI
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: Completada
   :version: 1.0.0
   :fecha_creacion: 2026-07-03T22:15:30
   :ultimo_cambio: 2026-07-03T22:15:30
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-auditar-implementacion-ucs-api-ui:

==============================================================
Iniciativa: Auditar Implementacion UCs en api y ui
==============================================================

Audita que los **88 UCs** declarados en
``source/requisitos/requisitos-funcionales/`` esten
implementados en ``IACT-api`` e ``IACT-ui``. Es la re-ejecucion
completa de la auditoria de cobertura sobre el corpus actual de
docs (la corrida previa, 2026-05-19, cubrio 75 UCs; desde
entonces se agregaron uc-078..091 y se retiro uc-047).

Es una **iniciativa de investigacion (no de implementacion)** —
read-only sobre IACT-api e IACT-ui. Aplica el protocolo
:doc:`grep-validado </gestion/pm/iniciativas/adoptar-protocolo-grep-validado-en-auditorias/index>`:
mapping textual (no lineal), markers compuestos y rangos
expandidos, e inspeccion de buckets negativos antes de publicar
cualquier "sin implementar".

Resultado ejecutivo: **70/70 UCs in-scope implementados en api
y 69/69 aplicables en ui — 0 gaps docs → codigo**. Los
hallazgos reales son de conformidad de markers y deuda
documental inversa (markers en codigo sin UC docs). Ver
hallazgos F-01..F-07 en el deep-analisis.

.. toctree::
   :maxdepth: 1

   alcance-auditar-implementacion-ucs-api-ui
   deep-analisis-auditar-implementacion-ucs-api-ui
   matriz-implementacion-uc-api-ui
   tareas-y-progreso-auditar-implementacion-ucs-api-ui
