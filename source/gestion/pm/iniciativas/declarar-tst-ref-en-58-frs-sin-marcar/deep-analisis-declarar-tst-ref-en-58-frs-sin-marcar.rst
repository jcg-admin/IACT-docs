.. meta::
   :artefacto: DEEP-ANALISIS-DECLARAR-TST-REF-EN-58-FRS-SIN-MARCAR
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/declarar-tst-ref-en-58-frs-sin-marcar
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:46:37
   :ultimo_cambio: 2026-05-19T20:46:37
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deep-analisis-declarar-tst-ref-en-58-frs-sin-marcar:

==============================================================
Deep-Analisis: TST refs en FRs (recalibracion del claim)
==============================================================

Origen del claim
==================

``auditar-conformidad-fr-tests-aceptacion`` reporto:

   "58 / 103 (56.3%) FRs sin ninguna declaracion de test
   esperado."

Comando que produjo el numero:

.. code-block:: bash

   cat /tmp/fr-all.txt | xargs grep -L "TST-FR" | wc -l
   # => 58

El flag ``-L`` lista archivos que NO contienen el patron.
El patron ``TST-FR`` es **case-sensitive**.

Verificacion (Fase 1 DISCOVER)
================================

Al inspeccionar uno de los archivos del listado "sin TST"
(``logs/uc-064-ver-estado-sistema/fr-064-01-consultar-estado-sistema.rst``,
linea 92):

::

   * - **TEST**
     - TST-fr-064-01 (pendiente)

**Notar:** ``TST-fr-`` (lowercase ``f``) — no
``TST-FR-`` (uppercase ``F``). El grep case-sensitive lo
filtra como ausente.

Re-ejecucion con case-insensitive:

.. code-block:: bash

   cat /tmp/fr-all.txt | xargs grep -iL "TST-fr\\|TST-FR" \\
     | wc -l
   # => 0

   cat /tmp/fr-all.txt | xargs grep -iE "TST-(fr|FR)-" \\
     | wc -l
   # => 103

**Resultado verificado:** los 103 FRs **declaran** un
TST ref. Ninguno carece de declaracion.

----

Distribucion de convenciones
==============================

Las dos formas coexisten particionadas estrictamente
por dominio:

.. list-table::
   :header-rows: 1
   :widths: 30 18 18 34

   * - Convencion
     - FRs
     - Dominios
     - Forma
   * - Uppercase + punto
     - 45
     - auth, users, access
     - ``TST-FR-NNN.NN``
   * - Lowercase + guion
     - 58
     - permissions, reports,
       logs, alerts, pipeline,
       audit
     - ``TST-fr-NNN-NN``

Particion por dominio sugiere que la convencion se
aplico en ciclos distintos: tres dominios temprano con
una convencion, seis dominios posteriores con otra. No
hay mezcla dentro de un dominio.

----

Implicaciones
===============

I-1 — La cobertura conformidad sigue siendo 0% trazable
---------------------------------------------------------

El descubrimiento NO afecta la conclusion principal de
``auditar-conformidad-fr-tests-aceptacion``: **0/103
FRs referenciados en codigo api**. La trazabilidad
codigo->FR es nula bajo cualquier convencion.

Lo que cambia: los 103 FRs declaran su TST ref
esperado; el codigo nunca aplico la convencion.

I-2 — La iniciativa anterior necesita actualizacion
-----------------------------------------------------

``auditar-conformidad-fr-tests-aceptacion`` afirmaba:

* "58/103 (56.3%) FRs sin ninguna declaracion de test
  esperado" — **falso**, son 0.
* "45/103 (43.7%) FRs declaran TST-FR-NNN.NN como
  pendiente" — incompleto, son 45 con UPPERCASE + 58
  con lowercase = **103 (100%)** declaran.

Compromiso de correccion: bump
``auditar-conformidad-fr-tests-aceptacion/deep-analisis-*``
a v1.1.0 con admonicion CORRECCION similar a la aplicada
a la auditoria original. **Pendiente de ejecutarse**
(scope acotado de esta iniciativa: solo registrar el
descubrimiento; la actualizacion del documento previo
se hace en commit posterior).

I-3 — Inconsistencia de naming es deuda metodologica menor
------------------------------------------------------------

Las dos convenciones son **funcionalmente equivalentes**
(misma semantica, distinta sintaxis). No bloquean nada
porque:

* Ningun tooling automatico depende del naming TST
  todavia (no hay grep de tests por TST ref).
* Para humanos, ambas formas son legibles.
* Para grep manual, basta usar case-insensitive.

Pero es deuda real si se quiere automatizar (R-1 de
``auditar-conformidad-fr-tests-aceptacion`` propone
``@pytest.mark.tst_fr("FR-001.02")``). Si se elige el
formato uppercase+punto, los 58 FRs de la otra convencion
quedan fuera del marco hasta normalizar.

----

Decision
==========

D1 — No normalizar en esta iniciativa
---------------------------------------

Considerado: ejecutar un ``sed`` masivo que normalice
los 58 FRs lowercase a uppercase+punto (o viceversa).

**Descartado:** la decision de cual convencion es
canonica es del sponsor, no del agente. Sin esa
decision, una normalizacion arbitraria introduce
trabajo reversible si despues se elige la otra
convencion.

Decision tomada: **registrar la dualidad como deuda
metodologica** y abrir iniciativa hermana
``normalizar-convencion-tst-ref-fr`` para que el
sponsor decida.

D2 — Actualizar auditar-conformidad-fr-tests-aceptacion
---------------------------------------------------------

El claim "58 FRs sin TST ref" en
``auditar-conformidad-fr-tests-aceptacion`` esta
ahora invalidado. Compromiso: agregar admonicion
CORRECCION v1.1.0 al deep-analisis de esa iniciativa
en el commit que cierra esta.

Patron similar al aplicado en
``implementar-uc-rpt-05-06-programacion-reportes`` que
invalido el claim "UC_RPT_05/06 sin implementacion" en
``auditar-cobertura-uc-implementacion``.

----

Hallazgos
==========

H-E1 — Grep case-sensitive como bug metodologico repetido
-----------------------------------------------------------

Es la **segunda vez** en la sesion que un claim de
auditoria queda invalidado por una asuncion implicita en
grep:

1. ``implementar-uc-rpt-05-06``: asuncion de linearidad
   en mapping de numeracion.
2. Esta iniciativa: asuncion de case en patron de
   marker.

Lecion epistemica: **los grep son utiles pero
producen claims SPECULATIVE cuando las suposiciones
sobre el patron no estan validadas con muestras
explicitas del corpus**. Toda auditoria por grep debe:

* Inspeccionar al menos un archivo del bucket
  "negativo" antes de afirmar ausencia.
* Validar la regex con el corpus real, no con
  expectativa.
* Reportar conteos con la regex exacta usada para que
  el lector pueda reproducir.

Iniciativa candidata
``adoptar-protocolo-grep-validado-en-auditorias``
formaliza este principio.

H-E2 — Particion limpia por dominio sugiere drift temporal
------------------------------------------------------------

Que las 45 + 58 se separen sin mezcla por dominio
sugiere dos ciclos de redaccion. Hipotesis: convencion
uppercase+punto se aplico a los 3 dominios "core"
(auth/users/access) primero; convencion lowercase+guion
emergio despues para los otros 6 dominios.

Sin commit history para verificar (`git log` de los
RST mostraria fechas de creacion), queda como
inferencia. Validar es trivial pero fuera del scope
estricto.

----

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 38 12 50

   * - Criterio
     - Resultado
     - Evidencia
   * - Verificar el claim de 58 sin TST ref
     - FALSO
     - case-insensitive grep retorna 0 archivos sin
       TST ref; los 103 declaran.
   * - Confirmar la dualidad de convenciones
     - PASA
     - 45 uppercase + 58 lowercase = 103.
       Particion limpia por dominio.
   * - Decision: no normalizar arbitrariamente
     - PASA
     - D1 documentada. Iniciativa hermana
       registrada.
   * - Compromiso actualizar audit previo
     - Pendiente
     - D2 documentada. Ejecucion en commit posterior.

----

Conclusion
===========

* Los 103 FRs in-scope **declaran TST ref**, todos
  marcados pendiente.
* La "brecha de 58" reportada fue **artefacto de grep
  case-sensitive** sobre dos convenciones de naming
  coexistentes.
* La trazabilidad codigo->FR sigue siendo **0%** —
  esto NO cambia con el descubrimiento.
* Deuda real identificada: **inconsistencia de
  naming** TST refs (dual convention, sin normalizacion).
* La iniciativa cierra **discovery**: cero RST tocados,
  cero edits aplicados. Su valor es la calibracion
  correcta del estado real.

Iniciativas candidatas derivadas:

1. ``normalizar-convencion-tst-ref-fr`` — sponsor
   decide convencion canonica, sed masivo normaliza
   los 103 FRs.
2. ``adoptar-protocolo-grep-validado-en-auditorias`` —
   meta-iniciativa metodologica para evitar falso-
   negativo por grep ciego.
3. Las 4 iniciativas ya registradas en
   ``auditar-conformidad-fr-tests-aceptacion`` (R-1..
   R-5) siguen vigentes — solo cambia el numerador
   base (de 45 a 103 con TST ref declarado).
