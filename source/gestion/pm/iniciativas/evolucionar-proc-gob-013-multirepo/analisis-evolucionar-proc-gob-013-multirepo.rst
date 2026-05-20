.. meta::
   :artefacto: ANALISIS-EVOLUCIONAR-PROC-GOB-013-MULTIREPO
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/evolucionar-proc-gob-013-multirepo
   :repo_objetivo: multiple
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:18:39
   :ultimo_cambio: 2026-05-19T18:18:39
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-evolucionar-proc-gob-013-multirepo:

==========================================================
Analisis: Evolucionar PROC-GOB-013 a Multi-Repo
==========================================================

Estado actual del meta-modelo de iniciativa
==============================================

PROC-GOB-013 v1.0.1 enumera en Fase 2 los documentos
obligatorios (Alcance, Analisis, Tareas, Progreso,
Decisiones) pero **no define un meta-modelo formal de
campos** que el bloque ``.. meta::`` del ``index.rst`` deba
contener. La realidad de facto:

* Todas las iniciativas registradas usan los mismos campos
  (``artefacto``, ``tipo``, ``dominio``, ``subdominio``,
  ``estado``, ``version``, ``fecha_creacion``,
  ``ultimo_cambio``, ``autor``, ``clasificacion``).
* Desde la iniciativa ``sanear-deuda-ci-y-normativa``
  (2026-05-18) todas las iniciativas anaden
  ``:repo_objetivo: IACT-docs`` como **medida local sin
  respaldo normativo** (decision D5 de esa iniciativa).
* El procedimiento no exige ese campo y el build no falla si
  se omite.

Hallazgo H-N2 (DEBT-012) describe exactamente esta brecha:
campo no formalizado en el meta-modelo. Resolverlo es
**aditivo** sobre la realidad de facto, no rompe iniciativas
cerradas.

Estado actual de las rutas y skills declarados
================================================

PROC-GOB-013 v1.0.1 menciona rutas y skills exclusivos de
IACT-docs:

* **Ruta de iniciativa:** ``source/gestion/pm/iniciativas/{nombre}/``.
  Esta ruta solo existe en IACT-docs.
* **Skills documentales:** ``workflow-discover``,
  ``workflow-scope``, ``workflow-implement``,
  ``workflow-track``, ``workflow-standardize``, ``sphinx``.
  Son skills cargadas desde ``.claude/skills/`` de IACT-docs.
* **Skills de proyecto:** ``pm-initiating``,
  ``pm-planning``, ``pm-executing``, ``pm-monitoring``,
  ``pm-closing``.

Hallazgo H-N3 (DEBT-013) describe la asuncion implicita
mono-repo. PROC-GOB-014 (creado 2026-05-19) introduce el
encuadre de gestion por submodulo en
``source/gestion/pm/{api,db,docs,server,ui}/`` pero **no
modifica** el meta-modelo ni las rutas declaradas por
PROC-GOB-013. La generalizacion de rutas/skills es una
brecha vigente.

Gaps concretos a cerrar
========================

.. list-table::
   :header-rows: 1
   :widths: 8 50 42

   * - ID
     - Gap
     - Solucion
   * - G-01
     - PROC-GOB-013 no formaliza el meta-modelo de campos
       del ``index.rst`` de una iniciativa.
     - Anadir seccion "Meta-modelo de la iniciativa" con
       lista de campos obligatorios y opcionales.
   * - G-02
     - El campo ``:repo_objetivo:`` no esta declarado como
       obligatorio en ningun procedimiento.
     - Declararlo obligatorio en el meta-modelo, con
       dominio enumerado y semantica formal.
   * - G-03
     - La ruta ``source/gestion/pm/iniciativas/`` esta
       descrita como universal cuando solo aplica a
       iniciativas con objetivo IACT-docs.
     - Generalizar: la ruta depende del valor de
       ``:repo_objetivo:`` (regla explicita por valor).
   * - G-04
     - Los skills documentales ``workflow-*`` se asumen
       universales cuando son especificos de IACT-docs.
     - Reformular como "skills de referencia para
       IACT-docs" y prever skills paralelos para otros
       repos cuando existan.
   * - G-05
     - PROC-GOB-013 no referencia a PROC-GOB-014 (creado
       posteriormente).
     - Anadir trazabilidad: PROC-GOB-014 como
       procedimiento complementario al eje multi-repo.
   * - G-06
     - El bump previo (1.0.0 -> 1.0.1) fue PATCH
       (correccion puntual de ruta). Una evolucion del
       meta-modelo es MAJOR.
     - Bump 1.0.1 -> 2.0.0 con entrada de historial que
       documenta el cambio incompatible.

Priorizacion MoSCoW
====================

.. list-table::
   :header-rows: 1
   :widths: 15 12 73

   * - Categoria
     - Gap
     - Justificacion
   * - Must
     - G-01, G-02, G-06
     - Sin meta-modelo formal con ``:repo_objetivo:``
       obligatorio y bump MAJOR coherente, la deuda
       DEBT-012 no se cierra. Son el nucleo de la
       iniciativa.
   * - Must
     - G-03
     - Sin generalizacion de rutas, las iniciativas en
       otros repos no tienen encuadre. Cierra DEBT-013.
   * - Should
     - G-05
     - La trazabilidad a PROC-GOB-014 es coherencia
       documental: ambos procedimientos coexisten y
       deben referenciarse mutuamente.
   * - Should
     - G-04
     - Generalizar skills es coherente con G-03, pero
       no rompe iniciativas existentes si no se hace
       (los skills actuales siguen siendo validos para
       IACT-docs).
   * - Could
     - Anadir tabla de matriz "tipo de iniciativa x
       repo objetivo x skills aplicables"
     - Util pero no critico para cerrar la deuda. Se
       evalua durante la ejecucion; si la inclusion no
       complica el diff, se incluye.

Cobertura analisis -> tarea
============================

.. list-table::
   :header-rows: 1
   :widths: 10 12 30 48

   * - Gap
     - Tarea
     - Archivo
     - Cobertura
   * - G-01
     - T-001
     - ``source/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion.rst``
     - Seccion "Meta-modelo de la iniciativa" anadida.
   * - G-02
     - T-001
     - idem
     - Campo ``:repo_objetivo:`` declarado obligatorio
       con dominio enumerado.
   * - G-03
     - T-001
     - idem
     - Regla por valor de ``:repo_objetivo:`` para la
       ruta de iniciativa.
   * - G-04
     - T-001
     - idem
     - Reformulacion de skills como referencia para
       IACT-docs; nota sobre skills paralelos.
   * - G-05
     - T-001
     - idem
     - Cross-ref a PROC-GOB-014 anadida.
   * - G-06
     - T-001
     - idem
     - Bump 2.0.0 + entrada de historial.
   * - Cierre deuda
     - T-002
     - ``source/risks-technical-debt/deuda-proc-gob-013-multirepo.rst``
     - DEBT-012 y DEBT-013 marcadas Resuelta con
       referencia a esta iniciativa.
   * - Estructura
     - T-003
     - ``source/gestion/pm/iniciativas/index.rst``
     - Iniciativa enlazada como activa.
   * - Cross-repo
     - T-004
     - ``IACT/.claude/`` (repo IACT)
     - Copia funcional de ``.claude/`` de IACT-docs a
       IACT para bootstrap del orquestador; commit en
       el repo IACT.

Casos especiales descubiertos durante la lectura
=================================================

* Las cinco iniciativas listadas en
  ``source/gestion/pm/iniciativas/index.rst`` tienen meta
  ``:estado: COMPLETADA`` aunque tres aparecen bajo
  "Iniciativas activas" del toctree. Es inconsistencia
  documental existente, fuera del alcance de esta
  iniciativa. Se registrara como hallazgo H-E1 al cierre y
  se decidira si se corrige aqui o se difiere a una
  iniciativa de auditoria.
* PROC-GOB-014 ya introduce ``INDEX-PM-<MOD>`` y
  ``pm-<mod>`` para la gestion vertical por submodulo, pero
  la matriz "iniciativa transversal -> submodulo afectado"
  no esta resuelta. PROC-GOB-014 dice "se referencia desde
  el index del submodulo correspondiente"; esta iniciativa
  es transversal y debera quedar referenciada al cierre en
  el index del submodulo ``docs/`` (al menos). Se registra
  como hallazgo de ejecucion al cerrar.
