.. meta::
   :artefacto: INICIATIVA-AUDITAR-COBERTURA-UC-IMPLEMENTACION
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:13:49
   :ultimo_cambio: 2026-05-19T20:13:49
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-auditar-cobertura-uc-implementacion:

==============================================================
Iniciativa: Auditar Cobertura UC -> Implementacion
==============================================================

Construye la matriz de cobertura ``UC x impl x test x estado``
sobre los **75 UCs** de ``source/requisitos/requisitos-funcionales/``.
Para cada UC verifica si existe codigo en ``IACT-api/`` (view,
serializer, URL), componente en ``IACT-ui/`` (screen,
slice/redux, ruta), soporte en ``IACT-db/`` (tabla, SP), y al
menos un test que ejercite el flujo end-to-end.

Origen: respuesta a la pregunta del sponsor "se implementaron
todos los flujos de los UCs?" — la respuesta requeria una
auditoria que no se habia hecho. Esta iniciativa la produce.

Es una **iniciativa de investigacion (no de implementacion)**.
Output: dos artefactos en ``source/`` que documentan el
estado real:

* ``deep-analisis-cobertura-uc-implementacion.rst`` —
  metodologia, alcance OUT/IN, hallazgos y conclusiones.
* Matriz tabular en el mismo deep-analisis o como artefacto
  hijo si el volumen lo justifica.

.. toctree::
   :maxdepth: 1

   alcance-auditar-cobertura-uc-implementacion
   deep-analisis-cobertura-uc-implementacion
   tareas-y-progreso-auditar-cobertura-uc-implementacion
