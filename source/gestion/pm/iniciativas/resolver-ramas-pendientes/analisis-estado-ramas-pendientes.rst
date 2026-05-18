.. meta::
   :artefacto: ANALISIS-ESTADO-RAMAS-PENDIENTES
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/resolver-ramas-pendientes
   :repo_objetivo: IACT-docs
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T18:46:00
   :ultimo_cambio: 2026-05-18T18:46:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _analisis-estado-ramas-pendientes:

==================================================
Analisis: Estado de las Ramas Pendientes
==================================================

Proposito
=========

Tras la integracion de los PR #22, #23, #24 y la creacion de la
iniciativa ``sanear-deuda-ci-y-normativa``, quedan ramas en el
remoto sin resolver. Este analisis las clasifica con datos
verificados para decidir, por rama: integrar, descartar o
archivar.

Las refs ``pr/N/head`` y ``pr/N/merge`` son refs internas de
GitHub (no ramas reales del repositorio) y quedan fuera de
alcance: se limpian solas o las gestiona GitHub.

Inventario verificado (vs ``origin/develop`` fe5f47d5)
=======================================================

.. list-table::
   :header-rows: 1
   :widths: 30 8 10 14 38

   * - Rama
     - ahead
     - en develop
     - source/ unicos
     - Naturaleza
   * - ``claude/review-project-config-V8Fg5``
     - 15
     - NO
     - 46
     - Nomenclatura ANTIGUA (``UC_ACC_01``,
       ``casos_uso/``, ``META_01``). Pre-migracion de naming.
   * - ``feature/arquitectura-tecnica-content``
     - 8
     - NO
     - 18
     - Nomenclatura ACTUAL (``casos-uso/``,
       ``uc-sup-01/``). Contenido tecnico de casos de uso.
   * - ``integration/backup-20260517_021658``
     - 1
     - NO
     - 109
     - Port-delta de backup; relacionado con PR #20 ya
       integrado.
   * - ``integration/feature/restore-devops-infra-pm-docs-20260518T022500``
     - 0
     - SI
     - 0
     - No aporta commits. Su contenido ya esta en develop.
   * - ``integration/fix/d01-cero-warnings-toctree-lexer-20260518T022500``
     - 1
     - NO
     - 3
     - Los 3 archivos D-01. Su contenido ya esta absorbido
       en la rama de la iniciativa ``sanear-deuda-ci-y-normativa``.

Diagnostico por rama
====================

R1 — ``claude/review-project-config-V8Fg5``
--------------------------------------------

15 commits, 46 archivos ``source/`` unicos, 9 archivos
``.thyrox/`` (scratch de trabajo, no contenido del producto).
**Hallazgo critico**: usa nomenclatura anterior a la migracion de
naming del proyecto (``UC_ACC_01_Asignar_Funciones.rst``,
``casos_uso/`` con guion bajo, ``META_01_``, ``GOB_05_``). El
proyecto actual usa kebab-lowercase. Integrar tal cual
reintroduciria la nomenclatura vieja: seria deuda, no
resolucion. Behind 1420: la rama es muy antigua.

Requiere decision de contenido: determinar si los 46 ``source/``
ya fueron migrados/reescritos con nomenclatura nueva en develop
(en cuyo caso la rama es obsoleta) o si hay contenido unico no
recuperado (en cuyo caso se rescata reescribiendo con
nomenclatura actual, no fusionando la rama).

R2 — ``feature/arquitectura-tecnica-content``
----------------------------------------------

8 commits, 18 ``source/`` unicos, 7 ``.thyrox/``. Nomenclatura
ACTUAL (``casos-uso/``, ``uc-sup-01/`` con la estructura de
12 partes). Es un track independiente de contenido tecnico de
casos de uso (UC-SUP-01 a spec completa, analisis IVR de
pipeline). Contenido sustantivo y con nomenclatura correcta:
candidato a integracion real, no a descarte.

R3 — ``integration/backup-20260517_021658``
--------------------------------------------

1 commit (``bc112cfd``), 109 ``source/``. Es un port-delta de
backup. Develop ya integro un port-delta equivalente via PR #20
(merge ``22a9c66f``, commit ``313d6452``). Requiere verificar si
los 109 archivos son los mismos ya integrados (rama obsoleta) o
si hay delta no portado (rescate selectivo).

R4 — ``integration/feature/restore-devops-infra-pm-docs-20260518T022500``
--------------------------------------------------------------------------

ahead=0 vs develop. No aporta ningun commit; su contenido ya
esta integro en develop (via PR #20). No tiene valor. Candidata
a borrado directo, sin riesgo de perdida.

R5 — ``integration/fix/d01-cero-warnings-toctree-lexer-20260518T022500``
------------------------------------------------------------------------

1 commit, 3 archivos D-01. Su contenido (W1/W2/W3) ya esta
absorbido en el commit de cierre D-01 de la rama
``integration/iniciativa/sanear-deuda-ci-y-normativa``.
Verificado limpio con build ``-W -j 2``. Una vez esa iniciativa
se integre a develop, esta rama queda redundante. Candidata a
borrado tras confirmar la integracion.

Priorizacion MoSCoW
====================

**Must**
  * Borrar R4 (ahead=0, no aporta, sin riesgo).
  * Verificar R3 contra PR #20 ya integrado (obsoleta vs delta
    real).
  * Verificar R1: cuanto de sus 46 ``source/`` ya esta en
    develop con nomenclatura nueva.

**Should**
  * Resolver R2: integrar el contenido tecnico (nomenclatura
    ya correcta) por la via que corresponda.
  * Borrar R5 tras confirmar que la iniciativa
    ``sanear-deuda-ci-y-normativa`` se integro.

**Could**
  * Rescate selectivo de contenido unico de R1 reescrito con
    nomenclatura actual (si el analisis detecta contenido no
    recuperado).

**Won't (esta iniciativa)**
  * Fusionar R1 tal cual: reintroduciria nomenclatura obsoleta.
  * Tocar refs ``pr/N/*`` (gestionadas por GitHub).

Caso especial
=============

R1 y R3 ilustran un patron recurrente del proyecto: una rama
"atrasada" con ``git diff`` que muestra muchos archivos no
significa que aporte ese contenido; suele estar **behind**
respecto a trabajo ya integrado por otra via. La verificacion
correcta es comparar contra ``merge-base`` y revisar si el
contenido ya existe en develop con la nomenclatura vigente, no
asumir por el conteo de ``git diff`` bidireccional.
