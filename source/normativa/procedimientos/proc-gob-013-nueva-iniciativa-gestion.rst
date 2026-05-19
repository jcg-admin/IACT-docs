.. meta::
   :artefacto: PROC-GOB-013
   :tipo: Procedimiento
   :dominio: normativa
   :subdominio: procedimientos
   :estado: Aprobado
   :version: 1.0.1
   :fecha_creacion: 2026-05-16T23:01:11
   :ultimo_cambio: 2026-05-18T18:21:29
   :autor: NestorMonroy
   :clasificacion: Interno

.. _proc-gob-013-nueva-iniciativa-gestion:

================================================================
Procedimiento: Crear una Nueva Iniciativa en source/gestion/
================================================================

.. note::

   Procedimiento obligatorio que describe **como crear y gestionar
   una iniciativa de documentacion** bajo ``source/gestion/``.

   Aplica cada vez que se identifica un conjunto de trabajo nuevo
   que requiere analisis, planificacion y seguimiento formal.

   Todo archivo producido en ``source/`` es exclusivamente ``.rst``.
   Los artefactos operativos generados por los skills
   (``.md`` en ``.thyrox/context/work/``) no entran en ``source/``.

----

Principio Rector
================

Antes de crear cualquier archivo en ``source/gestion/``, se lee
el estado real de ``source/*``. El analisis determina que documentos
necesita la iniciativa — no una plantilla fija.

Los skills en ``.claude/skills/`` son las herramientas operativas
que el ejecutor activa durante cada fase. Son el **como** construir.
Los archivos RST en ``source/gestion/`` son el **que** queda.
Ambas capas coexisten sin mezclarse.

----

.. admonition:: Verificacion de cambios declarados

   Cualquier ejecutor — persona o herramienta — puede declarar
   un cambio en texto y aplicarlo solo parcialmente o no aplicarlo.
   En sesiones largas esto se acumula sin que nadie lo detecte.

   **Regla del ejecutor:**
   Antes de declarar "listo" o presentar un archivo, verificar
   que cada cambio declarado en esa respuesta esta efectivamente
   en el archivo. Si son varios puntos, revisarlos uno por uno
   y mostrar la evidencia concreta.

   **Regla del revisor:**
   Cuando alguien declare "lo agrego", "lo incluyo", "lo documento",
   pedir el fragmento exacto del archivo donde quedo antes de
   continuar. Si no puede mostrarlo, el cambio no fue aplicado.

   **Frase de verificacion:** "muestrame el fragmento exacto donde quedo"

----

Tipos de iniciativa
===================

Antes de iniciar, clasificar la iniciativa en una de dos categorias:

**Iniciativa documental**
  Produce o mejora archivos RST en ``source/``. El trabajo es
  principalmente de analisis, escritura y validacion Sphinx.
  Usa el flujo ``workflow-*`` de ``.claude/skills/``.

**Iniciativa de proyecto**
  Tiene alcance, presupuesto, equipo y entregables formales.
  Requiere Project Charter y seguimiento PMBOK.
  Usa el flujo ``pm-*`` de ``.claude/skills/``.

La mayoria de iniciativas en ``source/gestion/`` son documentales.
El flujo PMBOK aplica cuando la iniciativa afecta multiples
repositorios, tiene dependencias externas o requiere autorizacion
formal de un sponsor.

----

Fase 1 — Leer antes de crear
=============================

**Skill activo:** ``.claude/skills/workflow-discover``

Antes de abrir ningun archivo nuevo, se leen los artefactos de
``source/*`` relevantes para la iniciativa. El objetivo es entender:

- Que existe actualmente y en que estado esta
- Que informacion ya esta documentada y puede referenciarse
- Que informacion no existe en ningun lado y hay que crear
- Que problemas estructurales existen que no estaban en el
  diagnostico inicial

Esta lectura se hace con la herramienta ``view``, no con comandos
shell. La herramienta ``bash_tool`` se reserva para busquedas de
patrones, conteos y compilacion del build.

La lectura no termina hasta que se puede responder con precision:
*que produce esta iniciativa y cual es su criterio de completitud?*

Para iniciativas de proyecto, activar adicionalmente
``.claude/skills/pm-initiating`` para desarrollar el Project Charter
antes de pasar a la Fase 2.

----

Fase 2 — Decidir la estructura de la iniciativa
=================================================

**Skills activos (documental):** ``.claude/skills/workflow-scope``

**Skills activos (proyecto):** ``.claude/skills/pm-planning``

Con el analisis hecho, se decide que documentos RST necesita
la iniciativa. Los documentos que han resultado utiles son:

**Alcance** (siempre presente)
  Que es la iniciativa, por que existe, cual es su criterio de
  completitud verificable y que queda explicitamente fuera de alcance.
  Si durante la lectura se tomaron decisiones de contenido no obvias
  (por ejemplo, referenciar en lugar de duplicar), se registran aqui.

**Analisis** (siempre presente)
  El diagnostico concreto: que falta, por que falta, que impacto
  tiene. Incluye la priorizacion MoSCoW y cualquier caso especial
  descubierto durante la lectura. El nombre del archivo describe
  que se analizo, no el tipo de documento.

**Tareas** (siempre presente)
  Las tareas T-NNN atomicas con su DAG de dependencias y la tabla
  de cobertura analisis hacia tarea. Cada tarea toca exactamente un
  archivo en ``source/*``.

**Progreso** (siempre presente)
  Lista de tareas con estado (pendiente / completada / bloqueada)
  y el conteo actual. Se actualiza despues de cada tarea ejecutada,
  antes del commit.

**Decisiones** (siempre presente — obligatorio en el cierre)
  Registro de las decisiones de diseno tomadas durante la ejecucion,
  los hallazgos que surgieron al trabajar y la verificacion
  post-ejecucion con evidencia.

**Documentos adicionales** (si el analisis lo justifica)
  Si la iniciativa es compleja y necesita registrar comparativas o
  contexto adicional, se anaden con nombres autoexplicativos.

----

Por que el documento de Decisiones es el mas importante
---------------------------------------------------------

Las tareas dicen **que** se hizo. El documento de decisiones
registra **por que** se hizo asi.

Sin ese registro, el proyecto pierde en tres dimensiones:

**Trazabilidad de criterio.**
Cuando un desarrollador futuro vea una decision de diseno en
``source/``, necesita entender si fue un error o una decision
intencional. Sin el documento de decisiones, no hay forma de
saberlo sin reconstruir el razonamiento desde cero.

**Transferencia de conocimiento tacito.**
Durante la ejecucion de una iniciativa se acumulan decenas de
micro-decisiones que el ejecutor considera obvias en el momento
pero que no lo son para nadie mas. En este proyecto — donde las
sesiones son discontinuas — ese contexto se pierde incluso para
el mismo ejecutor en la siguiente sesion.

**Aprendizaje del proceso.**
Los hallazgos de ejecucion son oportunidades de mejorar el
procedimiento y los criterios de las iniciativas futuras.
Si no se documentan, el equipo los repite.

----

Fase 3 — Crear la estructura en source/gestion/
=================================================

**Skill activo:** ``.claude/skills/sphinx`` (para validacion del build)

El directorio de la iniciativa se nombra con un verbo en infinitivo
seguido del objeto de trabajo, en kebab-lowercase per STD-007.
Describe que se hace, no una etapa metodologica.

Ejemplo correcto: ``integrar-infrastructure-source``

Ejemplo incorrecto: ``wp-infra-fase1``

El orden de creacion es:

1. Crear el directorio
   ``source/gestion/pm/iniciativas/{nombre-iniciativa}/``
2. Crear los documentos RST decididos en la Fase 2
3. Crear el ``index.rst`` del directorio que los enlaza en el toctree
4. Enlazar el ``index.rst`` de la iniciativa en
   ``source/gestion/index.rst``
5. Compilar el build y verificar 0 warnings antes de commitear

El commit de estructura es independiente del commit de ejecucion.

.. note::

   **Timestamps ISO 8601 con hora real.** Al rellenar cualquier campo
   ``<YYYY-MM-DDTHH:MM:SS>`` en los documentos, obtener el valor real
   con::

      date -u +"%Y-%m-%dT%H:%M:%S"

   Nunca escribir ``T00:00:00`` como placeholder.

----

Fase 4 — Ejecutar las tareas
==============================

**Skills activos (documental):**
``.claude/skills/workflow-implement`` +
``.claude/skills/sphinx``

**Skills activos (proyecto):**
``.claude/skills/pm-executing`` (en paralelo con
``.claude/skills/pm-monitoring``) +
``.claude/skills/sphinx``

Cada tarea sigue estos pasos en orden. No se salta ninguno.

**Paso 1 — Leer el artefacto fuente**
  Antes de modificar cualquier archivo en ``source/*``, se lee su
  estado actual con ``view``. Esto aplica incluso si el archivo se
  acaba de crear.

**Paso 2 — Leer el patron de referencia si existe**
  Si la tarea sigue un patron ya establecido, se lee ese patron
  antes de escribir. Los patrones canonicos viven en
  :doc:`/normativa/estandares/plantillas/index`.

**Paso 3 — Decidir el enfoque**
  - Si el artefacto tiene estructura real que vale conservar:
    ``str_replace`` en la seccion problematica.
  - Si el artefacto esta tan incompleto que no hay nada que salvar:
    ``create_file`` o reescritura total.
  - Si el artefacto tiene secciones buenas y secciones ausentes:
    ``str_replace`` para lo que esta mal, adiciones para lo que falta.

**Paso 4 — Aplicar el cambio**
  Un cambio por tarea. Si durante la ejecucion se descubre un
  problema adicional no previsto, se registra como tarea nueva
  en el documento de tareas antes de ejecutarlo.

**Paso 5 — Verificar el resultado**
  Leer el archivo modificado con ``view`` para confirmar que el
  cambio quedo como se esperaba.

**Paso 6 — Actualizar el progreso y compilar**
  Marcar la tarea como completada en ``progreso-{nombre}.rst`` y
  actualizar el conteo. Compilar Sphinx y confirmar 0 warnings.

**Paso 7 — Commitear**
  Un commit por tarea completada. El mensaje identifica la tarea
  (``T-NNN``) y describe el cambio de forma concreta.
  Ver convencion en :doc:`/gestion/git-workflow`.

----

Fase 5 — Cerrar la iniciativa
==============================

**Skills activos (documental):**
``.claude/skills/workflow-track`` +
``.claude/skills/workflow-standardize``

**Skills activos (proyecto):**
``.claude/skills/pm-closing``

La iniciativa esta completa cuando todas las tareas ejecutables
estan marcadas como completadas y el criterio de completitud
definido en el alcance es verificablemente verdadero.

El cierre tiene pasos obligatorios en este orden:

**Paso 1 — Actualizar el progreso**
  Marcar todas las tareas como completadas en
  ``tareas-{nombre}.rst`` y actualizar el historial.
  Actualizar ``progreso-{nombre}.rst``:

  - Estado: ``COMPLETADA``
  - Fecha de inicio y fecha de cierre reales
  - Historial de versiones con la entrada de cierre

**Paso 2 — Actualizar el index de la iniciativa**
  Cambiar el ``estado`` en el meta del ``index.rst`` de
  ``Pendiente`` a ``COMPLETADA``.

**Paso 3 — Crear el documento de Decisiones** *(obligatorio)*
  Crear ``decisiones-{nombre}.rst`` con las secciones:

  - **Decisiones de diseno** — cada decision no obvia tomada, con
    su justificacion y su alternativa descartada.
  - **Hallazgos durante la ejecucion** — problemas encontrados al
    ejecutar que no estaban en el plan. Cada hallazgo indica si fue
    resuelto en esta iniciativa o en cual se resolvera.
  - **Verificacion post-ejecucion** — tabla con cada criterio del
    alcance, el resultado (PASA/FALLA) y la evidencia concreta.

  Registrar el archivo en el toctree del ``index.rst``.

**Paso 4 — Registrar deuda tecnica nueva**
  Si durante la ejecucion se descubrieron problemas fuera del
  alcance, registrarlos en
  :doc:`/risks-technical-debt/deuda-tecnica-rebuild` si aplican
  al rebuild, o crear un nuevo artefacto en
  ``source/risks-technical-debt/`` si son deuda nueva.

**Paso 5 — Build limpio**
  Compilar Sphinx y confirmar 0 warnings y 0 errores.

**Paso 6 — Commit de cierre**
  Un commit que incluya todos los archivos de cierre. El mensaje
  indica el estado final (``N/N completadas``) y referencia el
  documento de decisiones.

.. admonition:: Senal de que una iniciativa NO esta cerrada

   Una iniciativa NO esta cerrada aunque todas las tareas esten
   marcadas como completadas si:

   - El ``index.rst`` dice ``estado: Pendiente``
   - El progreso tiene ``Inicio: COMPLETADA`` en lugar de una fecha
   - No existe el archivo ``decisiones-{nombre}.rst``
   - El documento de decisiones no tiene seccion de verificacion
     post-ejecucion con evidencia

----

Verificacion antes de abrir una iniciativa
===========================================

Antes de crear el directorio de la iniciativa, responder:

1. ¿Se leyo el estado actual de ``source/*`` antes de decidir la estructura?
2. ¿El nombre del directorio describe que se hace (verbo + objeto),
   en kebab-lowercase, no una etapa?
3. ¿Cada nombre de archivo es autoexplicativo fuera de su directorio?
4. ¿El criterio de completitud en el alcance es verificable sin ambiguedad?
5. ¿Cada tarea toca exactamente un archivo?
6. ¿La tabla de cobertura cubre todos los gaps del analisis?
7. ¿El tipo de iniciativa esta clasificado (documental o proyecto)?
8. ¿Los skills correspondientes al tipo estan identificados?

Si alguna respuesta es no, se resuelve antes de crear el directorio.

Verificacion antes de declarar una iniciativa cerrada
=======================================================

Antes de hacer el commit de cierre, responder:

1. ¿El ``index.rst`` tiene ``estado: COMPLETADA``?
2. ¿El ``progreso-{nombre}.rst`` tiene fechas reales de inicio y
   cierre, y el historial actualizado?
3. ¿El ``tareas-{nombre}.rst`` tiene el historial actualizado?
4. ¿Existe el archivo ``decisiones-{nombre}.rst``?
5. ¿El documento de decisiones tiene al menos una decision documentada
   por cada artefacto no trivial modificado?
6. ¿El documento de decisiones tiene la seccion de verificacion
   post-ejecucion con evidencia concreta?
7. ¿Todos los hallazgos de ejecucion estan registrados, indicando
   si fueron resueltos en esta iniciativa o en cual se resolvera?
8. ¿El build de Sphinx produce 0 warnings y 0 errores?

Si alguna respuesta es no, no se hace el commit de cierre.

----

Trazabilidad
============

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Skills documentales**
     - ``workflow-discover`` · ``workflow-scope`` ·
       ``workflow-implement`` · ``workflow-track`` ·
       ``workflow-standardize`` · ``sphinx``
   * - **Skills de proyecto**
     - ``pm-initiating`` · ``pm-planning`` · ``pm-executing`` ·
       ``pm-monitoring`` · ``pm-closing``
   * - **Procedimientos relacionados**
     - :doc:`proc-gob-009-auditoria-documental` ·
       :doc:`proc-gob-011-gestion-cambios` ·
       :doc:`proc-doc-013-validacion-sphinx`
   * - **Dominio de salida**
     - ``source/gestion/`` (exclusivamente ``.rst``)

----

Historial
---------

.. list-table::
   :widths: 15 20 65
   :header-rows: 1

   * - Version
     - Fecha
     - Cambio
   * - 1.0.0
     - 2026-05-16T23:01:11
     - Version inicial para IACT-docs. Adaptada de
       ``PROC-GESTION-001 v4.0.0`` (otro proyecto).
       Adaptaciones principales: clasificacion de iniciativas en
       documental vs proyecto; conexion explicita con
       ``.claude/skills/pm-*`` y ``workflow-*``; restriccion
       ``source/*`` exclusivamente RST; trazabilidad hacia
       ``risks-technical-debt`` y ``gestion/git-workflow``;
       eliminacion de referencias cruzadas inexistentes en este
       repositorio.
   * - 1.0.1
     - 2026-05-18T18:21:29
     - Correccion de ruta (hallazgo H-N1, iniciativa
       ``sanear-deuda-ci-y-normativa``): el paso 1 del orden de
       creacion decia ``source/gestion/{nombre-iniciativa}/``
       cuando la realidad de facto y el propio
       ``iniciativas/index.rst`` usan
       ``source/gestion/pm/iniciativas/{nombre-iniciativa}/``.
       Se alinea el texto con la realidad. El soporte
       multi-repositorio (H-N2, H-N3) queda fuera de alcance y
       se difiere a una iniciativa dedicada.
