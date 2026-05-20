.. meta::
   :artefacto: DECISIONES-EVOLUCIONAR-PROC-GOB-013-MULTIREPO
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/evolucionar-proc-gob-013-multirepo
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:26:25
   :ultimo_cambio: 2026-05-19T18:26:25
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-evolucionar-proc-gob-013-multirepo:

==========================================================
Decisiones: Evolucionar PROC-GOB-013 a Multi-Repo
==========================================================

Decisiones de diseno
=====================

D1 — Anadir el campo a la seccion "Meta-modelo" en lugar de inline en cada Fase
--------------------------------------------------------------------------------

PROC-GOB-013 v1.0.1 no tenia una seccion canonica que
enumerase los campos del bloque ``.. meta::``. La opcion
considerada era anadir notas inline en Fase 2 ("el index debe
declarar :repo_objetivo:") y Fase 3 ("recordar
:repo_objetivo: en el index"). Se descarto: dispersa la
definicion, complica futuras adiciones de campos y obliga al
lector a recorrer el procedimiento para reconstruir el
contrato.

Decision tomada: una unica seccion "Meta-modelo de la
iniciativa" justo despues de "Tipos de iniciativa" y antes de
"Fase 1". Tabla canonica de 11 campos con obligatoriedad
explicita. Permite cualquier adicion futura sin tocar las
fases.

D2 — Documentar compatibilidad prospectiva, no retroactiva
-----------------------------------------------------------

Considerado: anadir tarea T-extra que reescribiera el meta de
las iniciativas previas (``ampliar-devops-runbooks``,
``crear-infrastructure-skeleton``,
``integrar-contenido-rescatado``, ``resolver-ramas-pendientes``,
``sanear-deuda-ci-y-normativa``) para validar contra el nuevo
modelo formal. Se descarto: las iniciativas previas ya
declaran ``:repo_objetivo: IACT-docs`` de facto desde
``sanear-deuda-ci-y-normativa`` (D5 de esa iniciativa). El
mejoramiento retroactivo es trabajo de auditoria documental,
no de evolucion normativa.

Decision tomada: PROC-GOB-013 v2.0.0 introduce el campo con
efecto **prospectivo**. Iniciativas previas quedan validas.
Las iniciativas activas en el momento del bump actualizan su
meta en el siguiente commit que las toque. La regla queda
documentada en la propia seccion Meta-modelo (parrafo
"Compatibilidad con iniciativas previas").

D3 — La documentacion vive siempre en IACT-docs, la ejecucion en el repo objetivo
-----------------------------------------------------------------------------------

Modelo considerado A: replicar
``source/gestion/pm/iniciativas/`` en cada repo (IACT-api,
IACT-db, etc.) cuando ``:repo_objetivo:`` apunta a ellos. Se
descarto: fragmenta la trazabilidad documental, requiere build
Sphinx en cada repo, multiplica costos.

Modelo considerado B: copiar el RST de la iniciativa al repo
objetivo despues del cierre. Se descarto: introduce
duplicacion versionada con riesgo de drift.

Decision tomada (Modelo C): la documentacion de TODA
iniciativa transversal vive en IACT-docs. Lo que cambia segun
``:repo_objetivo:`` es **donde se ejecutan y commitean** las
tareas (codigo, configuracion, scripts). El progreso de la
iniciativa referencia los commits del repo objetivo por hash.
Esta iniciativa estrena el patron: T-004 vive en repo IACT
(commit ``ebbca996``), referenciado desde la tabla de
``progreso-evolucionar-proc-gob-013-multirepo.rst``.

D4 — Skills abiertos por repo, no listados como obligatorios
--------------------------------------------------------------

Considerado: enumerar skills concretos por repo objetivo
(p.ej. ``workflow-api-discover``, ``workflow-db-discover``)
como obligatorios. Se descarto: ningun repo tiene aun skills
propios en ``.claude/skills/`` distintos de los documentales;
imponerlos seria especular sobre futuros artefactos
inexistentes.

Decision tomada: la seccion Trazabilidad describe una regla
de "cuando existan en ``.claude/skills/`` de ese repo o del
orquestador IACT, sustituyen al conjunto ``workflow-*``
documental". Mientras no existan, se aplica el conjunto
documental con ejecucion fisica en el repo objetivo. Asi se
formaliza la generalizacion sin crear deuda de skills
fantasmas.

D5 — La integracion de .claude/ se incluye como T-004 de esta iniciativa
--------------------------------------------------------------------------

Considerado: tratar la copia de ``.claude/`` de IACT-docs al
repo IACT como iniciativa independiente. Se descarto: la
copia es un cambio trivial (un commit), pero estrena el
patron multi-repo con evidencia ejecutable. Convertirlo en
iniciativa separada introduce overhead de gobernanza sin
beneficio.

Decision tomada: ``.claude/`` integrado al repo IACT como
T-004 con su propio commit en ese repo (``ebbca996``).
Demuestra ``:repo_objetivo: multiple`` con evidencia real:
una misma iniciativa, dos repos tocados, trazabilidad por
hash en el progreso.

Hallazgos durante la ejecucion
================================

H-E1 — Inconsistencia en source/gestion/pm/iniciativas/index.rst
------------------------------------------------------------------

Las cinco iniciativas registradas tienen meta
``:estado: COMPLETADA`` pero tres aparecen bajo "Iniciativas
activas" en el toctree:

* ``integrar-contenido-rescatado``
* ``resolver-ramas-pendientes``
* ``sanear-deuda-ci-y-normativa``

Es deuda documental existente, descubierta al leer el index
durante la Fase 1 de esta iniciativa. **No se resuelve en
esta iniciativa** por estar fuera de alcance (la iniciativa
trata el meta-modelo de PROC-GOB-013, no el saneamiento del
index). Se difiere a una iniciativa nueva
``sanear-clasificacion-iniciativas-index`` o se absorbe en
una auditoria documental existente; queda registrado aqui
para no perderse.

H-E2 — PROC-GOB-014 no tiene cross-ref reciproca desde PROC-GOB-013
---------------------------------------------------------------------

Resuelto en T-001: PROC-GOB-013 v2.0.0 anade fila
"PROC-GOB-014 (estructura vertical por submodulo,
complementario al eje multi-repo de este procedimiento)" en
la seccion Trazabilidad. La cross-ref en direccion contraria
(PROC-GOB-014 referencia a PROC-GOB-013) ya existia en
PROC-GOB-014 v1.0.0 ("Procedimiento padre").

H-E3 — La iniciativa transversal debe ser referenciada desde el index del submodulo afectado
----------------------------------------------------------------------------------------------

PROC-GOB-014 indica: "Toda iniciativa transversal registrada
en ``source/gestion/pm/iniciativas/`` que tenga impacto en
un submodulo debe aparecer linkada desde el ``index.rst`` de
ese submodulo, en la seccion Iniciativas activas".

Esta iniciativa (``:repo_objetivo: multiple``) impacta a
IACT (orquestador, T-004) y a IACT-docs (T-001..T-003). El
index del submodulo ``docs/`` deberia listarla. **No se
resuelve en esta iniciativa** por estar fuera de alcance
explicito (alcance limita los archivos a tocar). Se registra
como hallazgo y se difiere a una iniciativa de saneamiento o
a la primera iniciativa que abra el submodulo correspondiente.

H-E4 — CWD persistente entre Bash calls causa commits en el repo equivocado
-----------------------------------------------------------------------------

Durante la ejecucion se observo que el ``cd`` en una llamada
Bash persiste en llamadas siguientes (cambia el working
directory de la sesion). Esto causo un intento de commit en
el repo equivocado, detectado por "nothing added to commit".
Mitigacion: cada commit/push se hizo con ``cd`` explicito al
repo correcto en la misma llamada.

No es un hallazgo de la iniciativa per se, sino del entorno
de ejecucion. Se documenta como leccion para futuras
iniciativas multi-repo: nunca asumir el CWD, declararlo
explicitamente en cada llamada.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 35 12 53

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - PROC-GOB-013 v2.0.0 declara :repo_objetivo:
       obligatorio en el meta-modelo
     - PASA
     - ``source/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion.rst``
       seccion "Meta-modelo de la iniciativa", fila
       ``repo_objetivo`` con obligatoriedad "Obligatorio".
       Commit ``428fd278``.
   * - Dominio enumerado del campo: IACT, IACT-api,
       IACT-db, IACT-docs, IACT-ui, multiple
     - PASA
     - Idem; columna "Semantica y dominio" de la fila
       ``repo_objetivo`` lista los seis valores.
   * - Ruta de iniciativa generalizada por repo
     - PASA
     - PROC-GOB-013 Fase 3 paso 1 reescrito: "la
       documentacion vive siempre en IACT-docs ...
       artefactos producidos por la ejecucion se
       commitean en el repo objetivo". Commit
       ``428fd278``.
   * - Cross-ref a PROC-GOB-014 anadida
     - PASA
     - PROC-GOB-013 seccion Trazabilidad, fila
       Procedimientos relacionados incluye
       ``proc-gob-014-gestion-por-submodulo``. Commit
       ``428fd278``.
   * - Bump 1.0.1 -> 2.0.0 con entrada de historial
     - PASA
     - Meta del archivo: ``:version: 2.0.0``. Tabla
       Historial: fila ``2.0.0`` con descripcion
       completa del cambio. Commit ``428fd278``.
   * - DEBT-012 y DEBT-013 marcadas Resueltas
     - PASA
     - ``source/risks-technical-debt/deuda-proc-gob-013-multirepo.rst``:
       meta ``:estado: Resuelta``, ambas filas con tag
       "Resuelta por iniciativa
       evolucionar-proc-gob-013-multirepo". Seccion
       Resolucion documenta los cinco cambios. Commit
       ``bd4fcb57``.
   * - .claude/ replicado en repo IACT
     - PASA
     - Commit ``ebbca996`` en rama
       ``feature/evolucionar-proc-gob-013-multirepo``
       de IACT: 100+ archivos en
       ``.claude/{rules,skills,agents,commands,hooks,references,scripts}/``
       mas ``CLAUDE.md``, ``ARCHITECTURE.md``,
       ``settings.json``.
   * - Esta iniciativa cumple el nuevo meta-modelo
     - PASA
     - Todos los artefactos (index, alcance, analisis,
       tareas, progreso, decisiones) declaran
       ``:repo_objetivo: multiple``. Es la primera del
       sistema con este valor.
   * - Build dummy 0 warnings tras el cierre
     - PASA
     - ``sphinx-build -b dummy`` completa con
       ``build succeeded`` tras T-001 y T-002. Ultima
       ejecucion previa a este documento sin warnings.

Deuda nueva registrada
========================

* H-E1: clasificacion incorrecta de iniciativas en
  ``source/gestion/pm/iniciativas/index.rst`` (3 cerradas
  bajo "Iniciativas activas"). Se evaluara registrarlo como
  deuda DEBT-014 o absorberlo en una iniciativa de
  auditoria documental proxima.
* H-E3: iniciativas transversales no se reflejan en el
  index del submodulo afectado (regla de PROC-GOB-014).
  Esta iniciativa misma carece de entrada en el index del
  submodulo ``docs/``. Se difiere a la primera iniciativa
  que toque el submodulo ``docs/`` o a una iniciativa de
  saneamiento.

Conclusion
==========

La iniciativa cumplio su criterio de completitud. PROC-GOB-013
v2.0.0 esta vigente y formaliza el meta-modelo multi-repo de
iniciativa que el sistema IACT necesitaba. La deuda diferida
DEBT-012/DEBT-013 esta cerrada y trazada al cambio que la
resolvio. La iniciativa misma demuestra ``:repo_objetivo:
multiple`` con evidencia ejecutable cross-repo.
