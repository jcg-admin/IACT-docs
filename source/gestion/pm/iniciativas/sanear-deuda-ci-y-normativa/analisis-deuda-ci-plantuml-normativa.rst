.. meta::
   :artefacto: ANALISIS-DEUDA-CI-PLANTUML-NORMATIVA
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/sanear-deuda-ci-y-normativa
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:21:29
   :ultimo_cambio: 2026-05-18T18:21:29
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-deuda-ci-plantuml-normativa:

==================================================
Analisis: Deuda de CI, PlantUML Cache y Normativa
==================================================

Diagnostico: la cadena de deuda
================================

El hallazgo central es que el OOM de ``sphinx-build`` no tiene una
causa unica sino tres causas entrelazadas. Tratar solo una deja
las otras activas.

Causa 1 — ``-j auto`` en ``validate.yml``
------------------------------------------

``sphinx-build`` usa ``fork``: cada proceso paralelo recibe una
copia de la memoria del proceso principal. Con el volumen de
documentos del proyecto y ``-j auto`` (un worker por CPU), el pico
de memoria concurrente supera la RAM disponible. El OOM-killer del
kernel termino ``sphinx-build`` (evidencia directa: ``anon-rss``
~700MB, ``oom-kill`` en el log del kernel). No fue inferencia.

Causa 2 — ``parallel_write_safe: True`` falsamente declarado
-------------------------------------------------------------

``source/_ext/plantuml_cached.py`` declara ``parallel_write_safe:
True`` aun cuando su fallback de cache miss delega en
``sphinxcontrib.plantuml``, que lanza un proceso Java por render.
Bajo ``-j auto`` + cache miss, multiples workers lanzan JVMs
simultaneas. Es una causa raiz adicional del OOM, no un sintoma:
el flag le dice a Sphinx que puede paralelizar una escritura que
en realidad dispara JVMs.

Causa 3 — ``make clean`` fuerza rebuild completo
-------------------------------------------------

``validate.yml`` ejecuta ``make clean`` antes de ``sphinx-build``,
borrando ``build/doctrees``. Cada ejecucion de CI reprocesa los
~3000 documentos desde cero en lugar de incremental. Maximiza el
trabajo del proceso padre, agravando el pico de memoria de la
Causa 1 y haciendo el build inviable en cuenta gratuita y en
flujo agil.

Hallazgos de auditoria de ``plantuml_cached.py``
=================================================

La auditoria inicial marco seis hallazgos. La verificacion
contra ``scripts/prerender-plantuml.py`` y docutils antes de
aplicar cambios determino que solo tres son defectos reales; los
otros tres son comportamiento intencional o convencion aceptada.
Esta correccion de la propia auditoria se documenta como parte
del saneamiento (un analisis con falsos positivos es deuda
documental).

Defectos reales corregidos
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 8 12 50 30

   * - ID
     - Severidad
     - Descripcion
     - Estado
   * - A-01
     - CRITICO
     - ``parallel_write_safe: True`` con fallback que lanza JVM.
     - **Corregido**: a ``False`` + version 1.1.0. Elimina la
       causa raiz adicional del OOM (escritura serializada en
       cache miss).
   * - A-02
     - ALTO
     - Solo loguea ``miss``, nunca ``hit``.
     - **Corregido**: anadido ``logger.info`` de hit. Hit ratio
       observable; detecta degradacion de cache antes de un OOM.
   * - A-06
     - BAJO
     - Fallo/ausencia de ``plantuml-styles.puml`` retorna ``""``
       silenciosamente, alterando el hash.
     - **Corregido**: dos ``logger.warning`` (ilegible / no
       encontrado) en vez de silencio.

Hallazgos descartados tras verificacion (no son defectos)
----------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 8 40 52

   * - ID
     - Marca inicial (erronea)
     - Evidencia que lo descarta
   * - A-03
     - "Hash ignora ``self.arguments`` -> colision".
     - ``scripts/prerender-plantuml.py`` (lineas 96-106,
       decision D-08) elimina deliberadamente
       ``@startuml NOMBRE`` -> ``@startuml`` antes de hashear.
       Ambos scripts excluyen el argumento del hash a
       proposito: el nombre del diagrama no afecta el render.
       "Corregirlo" desincronizaria el hash respecto al
       prerender, invalidaria los 1211 SVG y reintroduciria el
       OOM. **No es defecto; corregirlo causaria dano.**
   * - A-04
     - "``content_offset`` incorrecto para la caption".
     - El offset para ``nested_parse`` de una caption de
       opcion es ambiguo en docutils; ``content_offset`` es
       convencion aceptada y comun. No hay offset "correcto"
       evidente. A lo sumo mejorable, no defectuoso.
   * - A-05
     - "URI hardcodeada acopla al layout".
     - El propio codigo documenta que la URI con prefijo ``/``
       es patron deliberado para resolucion estilo
       ``_static`` por Sphinx. Funciona; es diseno consciente,
       no acoplamiento accidental.

Lección de proceso: la verificacion contra el codigo real
(prerender, docutils) antes de aplicar evito introducir un bug
grave (A-03 habria roto la cache) creyendo que se eliminaba
deuda. Verificar antes de actuar es el criterio del proyecto.

Hallazgos normativos en PROC-GOB-013
=====================================

.. list-table::
   :header-rows: 1
   :widths: 8 40 52

   * - ID
     - Descripcion
     - Decision
   * - H-N1
     - Linea 203 dice ``source/gestion/{nombre}/``; la
       realidad de facto y el ``iniciativas/index.rst`` (linea
       56) usan ``source/gestion/pm/iniciativas/{nombre}/``.
     - **In-scope**: tarea de esta iniciativa.
   * - H-N2
     - El meta-modelo de iniciativa no tiene campo para
       declarar el repositorio objetivo. Se asume IACT-docs
       implicitamente.
     - **Diferido**: cambio estructural multi-repo, iniciativa
       dedicada.
   * - H-N3
     - El procedimiento esta redactado como exclusivo de
       documentacion IACT-docs; el sistema IACT es multi-repo.
     - **Diferido**: junto con H-N2.

Priorizacion MoSCoW
====================

**Must**
  * Corregir H-N1 (ruta en PROC-GOB-013).
  * Eliminar ``make clean`` de ``validate.yml`` y anadir cache de
    doctrees (Causa 3).
  * Corregir A-01 (``parallel_write_safe``) — causa raiz del OOM.
  * Acotar ``-j`` y triggers en ``validate.yml`` (Causa 1).
  * Cerrar D-01 (los 3 warnings de contenido).

**Should**
  * Corregir A-02 (loguear hit ratio) y A-06 (warning si fallan
    estilos): observabilidad para no repetir el OOM por miss
    masivo silencioso.
  * Job de build completo limpio con guard de visibilidad publica.

**Could**
  * (Ninguno pendiente: A-03/A-04/A-05 se descartaron tras
    verificacion; no son defectos, ver seccion de hallazgos
    descartados.)

**Won't (esta iniciativa)**
  * Soporte multi-repo en PROC-GOB-013 (H-N2, H-N3).
  * Cambio de ruta de diagramas a ``_static/img/`` (contradice
    D-03, pendiente de justificacion).
  * Modificar A-03/A-04/A-05: no procede, no son defectos.

Caso especial descubierto durante la lectura
=============================================

``scripts/prerender-plantuml.py`` comparte la ruta de cache con
``plantuml_cached.py`` por contrato implicito (constante duplicada
``_generated_diagrams``). Cualquier correccion de A-05 que toque
la ruta debe modificar ambos coordinadamente, o la cache se
desincroniza y reaparece el miss masivo. Por eso A-05 se clasifica
``Could`` y no ``Should``: su correccion correcta exige tocar dos
archivos con un contrato no documentado, lo que aumenta el riesgo.
