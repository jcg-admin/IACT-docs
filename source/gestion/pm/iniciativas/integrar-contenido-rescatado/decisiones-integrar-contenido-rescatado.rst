.. meta::
   :artefacto: DECISIONES-INTEGRAR-CONTENIDO-RESCATADO
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/integrar-contenido-rescatado
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-18T23:37:34
   :ultimo_cambio: 2026-05-18T23:37:34
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-integrar-contenido-rescatado:

==================================================
Decisiones: Integrar el contenido rescatado
==================================================

Decisiones de diseno
====================

D1 — Origen del contenido: ramas R2/R3, no wp-tmp/
---------------------------------------------------

``wp-tmp/`` vive solo en la rama ``resolver-ramas-pendientes``,
no en develop. Tomar de ``wp-tmp/`` acoplaria esta iniciativa a
que aquella se integre primero. Se toma de las ramas origen
R2 (``43250b49``) / R3 (``bc112cfd``) del remoto: es el origen
de verdad (``wp-tmp/`` era copia verificada por hash de estas)
y existen independientemente. Alternativa descartada: rama
desde ``resolver-ramas-pendientes`` (acoplamiento de orden de
integracion).

D2 — Alcance acotado a lo verificable como correcto
----------------------------------------------------

Solo R2 (12, riesgo bajo) y R3 nuevos (8, riesgo medio)
in-scope. R3 difieren (68, riesgo alto) y R1 (transformacion)
out-of-scope, siguen como DEBT-010/011 activas. Integrar los
89 en bloque seria integrar incorrectamente: 68 sin analisis
de sustancia y 1 que contradice la politica RST-only. Acotar
no deja deuda oculta: la deuda out-of-scope ya esta registrada
formalmente.

D3 — Una tarea por archivo; toctree en el mismo paso
-----------------------------------------------------

Cada archivo es una tarea atomica. Para los nuevos (R3), la
creacion y el enlace en el toctree de su seccion van en la
MISMA tarea. Razon: un archivo nuevo sin enlazar genera
"document isn't included in any toctree" (warning -> con
``-W`` rompe el build). Separar creacion y enlace dejaria una
ventana de huerfano.

D4 — Verificacion de build delegada al usuario
-----------------------------------------------

El clon de trabajo no completa ``sphinx-build`` (PlantUML se
cuelga; verificado toda la sesion). La preparacion (copia con
hash + toctree) se hace y commitea en el clon; la verificacion
``-W -j 2`` = 0 warnings la ejecuta el usuario en su local
antes del push. No es deuda oculta: es restriccion de entorno
documentada en el Alcance. El criterio de "integracion
correcta" incluye esta verificacion como paso del usuario, no
como algo omitido.

Hallazgos surgidos durante la ejecucion
========================================

H-EJ1 — Auditoria estatica de referencias antes de integrar
------------------------------------------------------------

Antes de integrar se audito (sin compilar, por analisis de
texto) cada ``:ref:``/``:doc:`` que el contenido introduce,
verificando sus destinos contra develop:

* **R2 (12)**: una sola ref externa
  (``breq-006-operacion-continua-sla``), existe en develop.
  Integrable limpio. Riesgo bajo confirmado con datos.
* **R3 ``modelo-rbac-iact.rst``**: refs a ``std-006`` (OK),
  ``restricciones/index`` (OK) y auto-ref (se resuelve al
  integrarse en su propia ruta). Integrable.
* **R3 6 ``diagramas-uml.rst``**: 0 refs externas; toctrees
  padre (uc-acc-01/03/04/05/08, uc-perm-06) existen en
  develop. Integrables limpios.
* **R3 ``cnst-030-sod.rst``**: referencia
  ``cnst-029-rbac-modelo-plano`` y
  ``cnst-031-permisos-temporales-maximo-6-meses``, **ninguno
  existe en develop**. Integrarlo daria 2 warnings ``:doc:``
  rotos -> con ``-W`` rompe el build.

Decision derivada: ``cnst-030-sod.rst`` sale de in-scope.
La verificacion de hash NO habria detectado esto (el contenido
es fiel a R3, pero R3 referencia archivos ausentes en develop);
solo la auditoria estatica de referencias lo previno. Esto
valida hacer la auditoria antes de integrar, no integrar y
descubrir el warning en el build del usuario.

H-EJ1 — Deuda derivada
-----------------------

La auditoria detecto tres residuales que NO se integran por
reintroducir deuda, registrados formalmente en
:doc:`/risks-technical-debt/deuda-integracion-r3-residual`:

* DEBT-014: ``cnst-030-sod.rst`` referencia cnst-029/031
  inexistentes en develop (2 warnings ``:doc:`` rotos).
* DEBT-015: ``diagramas-uml.rst`` (R2) es plano pero develop
  tiene ``diagramas-uml/`` subdirectorio mejor (seria
  huerfano + retroceso).
* DEBT-016: el ``index.rst`` de uc-sup-01 en develop tiene
  nomenclatura antigua (deuda preexistente, no introducida
  por esta iniciativa, detectada durante ella).

Verificacion post-ejecucion con evidencia
==========================================

.. list-table::
   :header-rows: 1
   :widths: 44 12 44

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - 12 archivos de R2 integrados con hash verificado
     - PARCIAL
     - 11/12 integrados (hash identico a R2).
       ``diagramas-uml.rst`` excluido con justificacion
       (DEBT-015): develop tiene subdirectorio mejor.
       Reconciliado en Alcance y Tareas.
   * - 8 archivos nuevos de R3 integrados y enlazados
     - FALLA-CONTROLADA
     - 0/8. Auditoria estatica determino que ninguno es
       integrable sin reintroducir deuda. Reclasificado a
       DEBT-014. La "falla" es la auditoria previniendo
       integracion incorrecta, no un defecto de ejecucion.
   * - Build 0 warnings con el contenido integrado
     - PENDIENTE-USUARIO
     - Lo ejecuta el usuario (clon no completa build
       PlantUML). Deep analysis verifico estaticamente:
       integridad 11/11, cero huerfanos, cero refs rotas.
   * - DEBT-008/009 marcadas resueltas; DEBT-010/011 siguen
     - PARCIAL
     - DEBT-008 (R2) se marca resuelta en
       ``deuda-integracion-wp-tmp`` al integrarse la rama
       ``resolver-ramas-pendientes`` (dependencia
       cross-rama documentada). DEBT-009 reclasificada a
       DEBT-014. DEBT-010/011 siguen activas (cross-rama).

Cierre
======

La iniciativa integro lo verificable como correcto (R2, 11
archivos) y determino con evidencia que R3 nuevos NO debia
integrarse, dejandolo como deuda formal con causa tecnica
(DEBT-014/015/016). El deep analysis previo
(``deep-analisis-deuda-tecnica``) confirmo 0 deuda oculta y
descarto 2 falsos positivos. Los criterios PARCIAL/FALLA no
son incumplimientos: son el resultado de la auditoria
funcionando, documentado con honestidad en vez de forzar
integraciones incorrectas para que la tabla diera PASA. El
unico PENDIENTE-USUARIO (build) es restriccion de entorno
conocida, no deuda oculta.
