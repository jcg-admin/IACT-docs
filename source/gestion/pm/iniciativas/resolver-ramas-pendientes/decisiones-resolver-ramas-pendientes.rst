.. meta::
   :artefacto: DECISIONES-RESOLVER-RAMAS-PENDIENTES
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-ramas-pendientes
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:46:00
   :ultimo_cambio: 2026-05-18T21:37:24
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-resolver-ramas-pendientes:

==================================================
Decisiones: Resolver Ramas Pendientes
==================================================

Decisiones de diseno
====================

D1 — wp-tmp/ como repositorio de paso pasajero
-----------------------------------------------

El contenido con valor no integrado se rescata a
``source/gestion/pm/iniciativas/resolver-ramas-pendientes/wp-tmp/``.
Es pasajero: queda en git log y en los documentos de la
iniciativa, pero NO se integra a develop ni al build. No
requiere ``exclude_patterns`` en ``conf.py`` porque la rama de
iniciativa no llega a develop hasta una decision consciente
posterior. Finalidad: preservar todo lo cambiado para poder
borrar las ramas sin perder trabajo, y analizar la integracion
despues sin presion.

D2 — Rama limpia desde develop
-------------------------------

La iniciativa va en rama propia desde ``origin/develop``,
independiente de ``sanear-deuda-ci-y-normativa``. Razon: son
trabajos sin relacion funcional; ramas independientes evitan
PRs gigantes y dependencias fragiles. Riesgo asumido: ambas
tocan ``pm/iniciativas/index.rst`` (cruce trivial al integrar,
se resuelve actualizando con develop).

D3 — Verificacion por hash, no por git diff
--------------------------------------------

``git diff --name-only A...B`` sobre una rama ``behind`` infla
el conteo de "unicos". Toda decision de rescate se baso en
comparar hash de objeto git por archivo. Caso R1: de 9
``.thyrox/`` "unicos", 7 identicos a develop, 1 mas viejo, solo
1 nuevo real. Aplicado igual en R2 y R3.

D4 — Rescatar todo lo cambiado de R3 (estrategia de
preservacion)
----------------------------------------------------------------

Decision del usuario: para R3, en vez de decidir archivo por
archivo que integrar, se copia TODO lo cambiado (79 archivos)
a ``wp-tmp/`` con estructura de directorios. Asi la rama se
borra sin riesgo y el analisis de integracion se hace despues
sobre el material preservado. Los 34 identicos y ``ROADMAP.md``
NO se copiaron (mismo hash que develop = ruido que dificultaria
el analisis).

D5 — Resolucion del conflicto en pm/iniciativas/index.rst
----------------------------------------------------------

Las iniciativas ``sanear-deuda-ci-y-normativa`` y
``resolver-ramas-pendientes`` modifican ambas el toctree de
"Iniciativas activas" en ``pm/iniciativas/index.rst``, cada una
listando solo su propia entrada (salieron de develop por
separado). Al integrar ambas a develop habra **conflicto de
merge** en ese archivo.

**Resolucion (opcion B, decision del usuario)**: al resolver
el conflicto se conservan **AMBAS** entradas en el toctree de
activas::

   .. toctree::
      :maxdepth: 1

      sanear-deuda-ci-y-normativa/index
      resolver-ramas-pendientes/index

NO descartar ninguna. Descartar una dejaria su iniciativa como
documento huerfano (warning de Sphinx). Se descarto la opcion A
(que cada rama listara ambas) por acoplar el orden de
integracion y arriesgar un toctree roto si una rama se integra
sin la otra.

D6 — Analisis de integracion wp-tmp incorporado al alcance
-----------------------------------------------------------

Decision del usuario (2026-05-18): el analisis de **como**
integrar ``wp-tmp/`` a ``source/`` pasa a ser parte de esta
iniciativa (documento ``analisis-integracion-wp-tmp``). El
Alcance se corrigio en consecuencia (era contradictorio
declararlo out-of-scope mientras se ejecutaba). La **ejecucion**
de la integracion archivo por archivo sigue siendo trabajo
planificado a partir de ese analisis, con verificacion de build
por paso, no integracion en bloque.

Hallazgos surgidos durante la ejecucion
========================================

H-EJ1 — ``.thyrox/`` no es scratch
-----------------------------------

El analisis inicial caracterizo ``.thyrox/`` como "scratch de
trabajo, no contenido del producto". **Incorrecto**: esta
versionado en develop (3548 archivos), no esta en
``.gitignore``, contiene ADRs y analisis con valor. Se corrigio
el documento de analisis. Leccion: no caracterizar por la
etiqueta sin verificar contra el repo.

H-EJ2 — R3 es patron inverso al esperado
------------------------------------------

Se predijo que R3 (behind 705) tendria versiones viejas. Los
datos lo refutaron: los 68 que difieren tienen R3 MAS reciente
(port-delta del 17-mayo). La posicion ``behind`` no determina
si una rama aporta; solo la verificacion de contenido lo
determina.

H-EJ3 — modelo-rbac-iact.rst de R3 es vigente
----------------------------------------------

Riesgo evaluado: que el modelo RBAC de R3 usara v5.2.1 FK
binario (deprecado). Verificado: ``:version: 5.4.0`` M2M
vigente; las menciones a v5.2.1/v5.3.0 son changelog
historico, no uso activo (misma distincion aplicada en
H-N1 de la otra iniciativa). Riesgo descartado.

H-EJ4 — R3 no duplica PR #20
-----------------------------

Riesgo evaluado: que R3 fuera duplicado del PR #20 (mismo
backup). Verificado: los archivos nuevos de R3
(``modelo-rbac-iact.rst``, ``cnst-030``) estan AUSENTES en
develop; PR #20 no los integro. R3 aporta delta complementario
real.

Verificacion post-ejecucion con evidencia
==========================================

Cada criterio de completitud del alcance, su resultado y la
evidencia concreta:

.. list-table::
   :header-rows: 1
   :widths: 44 12 44

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - Cada rama R1..R5 con resolucion documentada con
       evidencia
     - PASA
     - ``analisis-estado-ramas-pendientes`` +
       ``analisis-rescate-thyrox-r1`` +
       ``analisis-profundo-r2`` + ``analisis-profundo-r3``;
       tabla de resoluciones en ``tareas-*``.
   * - Contenido con valor de R1/R2/R3 preservado en
       ``wp-tmp/`` verificado por hash
     - PASA
     - 94 archivos en ``wp-tmp/``, hash de objeto git
       identico al origen (R1: 1, R2: 12, R3: 79, +
       PROCEDENCIA por subdir).
   * - Estructura PROC-GOB-013 completa (5 docs + index) y
       enlazada en ``pm/iniciativas/index.rst``
     - PASA
     - 9 .rst (5 obligatorios + 4 analisis +
       analisis-integracion); index toctree sin huerfanos;
       enlace en ``pm/iniciativas/index.rst`` (T-008,
       commit ``4e583b7a``).
   * - Build 0 warnings de la rama
     - PENDIENTE
     - Lo verifica el usuario en su local antes del push
       (PROC-GOB-013 Fase 3 paso 5). El clon de trabajo no
       completa el build PlantUML. No bloquea el cierre
       documental; es gate previo al push.

Deuda registrada al cierre
==========================

La ejecucion de la integracion de ``wp-tmp/`` a ``source/``
NO se realizo (decision D6: el analisis si, la ejecucion no).
Para no dejar deuda oculta, se registro formalmente como
:doc:`/risks-technical-debt/deuda-integracion-wp-tmp`
(DEBT-008..011), con el analisis de como abordarla ya
disponible como insumo. El cierre de esta iniciativa es
limpio: cumplio su alcance real (resolver y preservar las
ramas) y la deuda pendiente quedo con dueño y trazable, no
silenciada.
