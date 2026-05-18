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

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Item
     - Evidencia
   * - Rescates wp-tmp/
     - 94 archivos, hash verificado identico al origen
       (R1: 1, R2: 12, R3: 79, + PROCEDENCIA por subdir).
   * - Push limpio
     - Rama remota con 5 commits; los mode-change/deleted
       (ruido tar->Windows) NUNCA se commitearon ni
       subieron (verificado contra remoto).
   * - Integridad de ramas
     - R1..R5 con resolucion documentada; ninguna se borra
       sin su contenido preservado o verificado redundante.
   * - Estructura PROC-GOB-013
     - 5 documentos + index; pendiente solo el enlace en
       ``pm/iniciativas/index.rst`` (T-008).
   * - Build de la rama
     - Pendiente: lo verifica el usuario antes del push
       (Fase 3 paso 5). El clon no completa build PlantUML.
