.. meta::
   :artefacto: DEEP-ANALISIS-ADOPTAR-PROTOCOLO-GREP-VALIDADO-EN-AUDITORIAS
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/adoptar-protocolo-grep-validado-en-auditorias
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:55:43
   :ultimo_cambio: 2026-05-19T20:55:43
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deep-analisis-adoptar-protocolo-grep-validado-en-auditorias:

==============================================================
Deep-Analisis: Protocolo Grep-Validado en Auditorias
==============================================================

Contexto y problema
=====================

En la sesion 2026-05-19, dos auditorias importantes
produjeron claims que despues fueron invalidados al
inspeccionar el corpus:

Caso 1 — UC_RPT_05/06
-----------------------

* Auditoria: ``auditar-cobertura-uc-implementacion``.
* Claim original: "UC_RPT_05 (uc-036-programar-reporte) y
  UC_RPT_06 (uc-037-ver-reportes-programados): sin marker
  en api ni ui. Posible: feature de programacion de
  reportes esta solo en docs, no implementada."
* Realidad: los UCs ``uc-036`` y ``uc-037`` **estan
  implementados** bajo markers ``UC_RPT_07`` y
  ``UC_RPT_08`` respectivamente (gap de numeracion en el
  codigo entre 04 y 07).
* Causa raiz: asuncion implicita de mapping lineal
  ``uc-NNN-decreciente <-> UC_<DOM>_NN-decreciente``.

Caso 2 — 58 FRs sin TST ref
-----------------------------

* Auditoria:
  ``auditar-conformidad-fr-tests-aceptacion``.
* Claim original: "58 / 103 (56.3%) FRs sin ninguna
  declaracion de test esperado".
* Realidad: los 103 FRs declaran TST ref; los 58 "sin"
  usan convencion ``TST-fr-NNN-NN`` (lowercase + guion)
  en lugar de ``TST-FR-NNN.NN`` (uppercase + punto).
* Causa raiz: grep case-sensitive sobre corpus con dos
  convenciones de naming coexistentes.

Patron comun
==============

Ambos casos tienen la misma forma logica:

1. La auditoria define un patron (regex o marker
   esperado).
2. Grep retorna 0 hits para algun subconjunto del corpus.
3. La auditoria concluye "el subconjunto carece del
   patron" y por extension "no tiene implementacion / no
   declara X".
4. **La conclusion es invalida**: el subconjunto SI
   tiene el concepto pero codificado bajo otra
   sintaxis/convencion que el patron de grep no contemplo.

El problema epistemico: el grep es **deductivamente
correcto** (0 hits = 0 matches del literal exacto) pero
**inductivamente engañoso** (0 matches del literal no
implica 0 instancias del concepto).

----

Tres asunciones implicitas que producen el bug
================================================

A-1 — Mapping lineal entre dos corpus
---------------------------------------

Cuando dos enumeraciones (docs ``uc-NNN`` vs codigo
``UC_<DOM>_NN``) tienen rangos del mismo tamaño,
**asumir** que ``i`` en uno corresponde a ``i`` en otro
es comun. **Es falso** cuando uno de los corpus tiene
gaps (markers retirados, reservados, renumerados).

Defensa: validar por descripcion textual del item
correspondiente, no por indice numerico.

A-2 — Uniformidad de naming en el corpus
------------------------------------------

Cuando un corpus tiene N archivos del mismo "tipo",
**asumir** que todos usan la misma convencion sintactica
es comun. **Es falso** cuando los archivos se crearon en
distintos ciclos editoriales con convenciones distintas.

Defensa: case-insensitive por default; muestrear 2-3
archivos para verificar uniformidad antes de fijar la
regex.

A-3 — El literal exacto cubre el concepto
-------------------------------------------

Cuando se busca un concepto (ej. "test de FR-001.02"),
**asumir** que un solo literal exacto (``TST-FR-001.02``)
captura todas sus instancias es comun. **Es falso** si
el concepto tiene multiples representaciones legitimas
(``TST-FR-001.02``, ``TST-fr-001-02``, ``fr_001_02_test``,
docstring con FR mencionado en prosa, etc.).

Defensa: enumerar variantes plausibles antes de fijar
la regex y ampliar con alternancia (``A|B|C``).

----

Solucion adoptada
==================

E-1 — Regla operacional en .claude/rules/
-------------------------------------------

Archivo nuevo: ``.claude/rules/grep-validated-audit.md``.

Por I-009 de ``thyrox-invariants.md``, los archivos en
``.claude/rules/`` se cargan **incondicionalmente en
cada sesion**. La regla sera leida por cualquier agente
o desarrollador que abra una sesion sobre IACT-docs y
estara disponible al iniciar cualquier auditoria.

Contenido:

* Regla principal: 4 pasos pre-publicacion.
* Anti-patrones: AP-1..AP-4 con ejemplos contrastados.
* Tabla de clasificacion PROVEN / INFERRED / SPECULATIVE
  para claims grep-derivados.
* Checklist de 6 items pre-publicacion.
* Casos historicos documentados (UC_RPT_05/06 y 58 FRs)
  con su causa raiz y fix.

E-2 — Iniciativa documental con narrativa
-------------------------------------------

Esta iniciativa (``adoptar-protocolo-grep-validado-en-auditorias``)
contiene el contexto historico, el patron logico
identificado, las tres asunciones implicitas y el
analisis epistemico. La regla en ``.claude/rules/`` es
operacional (que hacer); este deep-analysis es
explicativo (por que).

----

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 38 12 50

   * - Criterio
     - Resultado
     - Evidencia
   * - Regla ``grep-validated-audit.md`` creada
     - PASA
     - ``ls /home/user/IACT-docs/.claude/rules/``
       muestra el archivo.
   * - Regla incluye protocolo de 4 pasos
     - PASA
     - Seccion "Protocolo paso a paso" del archivo.
   * - Regla incluye 4 anti-patrones
     - PASA
     - AP-1 (0 hits sin inspeccionar), AP-2 (mapping
       lineal), AP-3 (case sin validar), AP-4
       (conteos sin reproducibilidad).
   * - Tabla de clasificacion PROVEN/INFERRED/
       SPECULATIVE para grep claims
     - PASA
     - Tabla "Clasificacion de claims por grep" en
       el archivo.
   * - Checklist pre-publicacion (6 items)
     - PASA
     - Seccion "Lista de verificacion
       pre-publicacion".
   * - Casos historicos documentados
     - PASA
     - 2026-05-19 UC_RPT_05/06 y 58 FRs con causa
       raiz y referencias a iniciativas que los
       resolvieron.
   * - Esta iniciativa documenta el patron logico
     - PASA
     - Seccion "Patron comun" + "Tres asunciones
       implicitas".

----

Hallazgos
==========

H-F1 — La sesion produjo 2 falsos claims en ~3 horas
------------------------------------------------------

Iniciativas de la sesion 2026-05-19:

* 09:xx — sesion arranca con setup multi-repo
* 18:xx — primer falso claim (UC_RPT_05/06)
* 20:35 — falso claim invalidado por iniciativa #10
* 20:46 — segundo falso claim (58 FRs)
* 20:55 — falso claim invalidado por iniciativa #14

Ratio: **2 falsos claims por sesion de ~12 horas**, en
auditorias relativamente complejas. Sin la regla, una
auditoria de orden superior tendria probabilidad
significativa de generar un tercer caso.

H-F2 — Ambos casos se descubrieron por inspeccion del archivo
---------------------------------------------------------------

En ambos casos, la invalidacion del claim ocurrio al
**abrir un archivo del bucket negativo** para verificar
otra cosa (en el caso 1, planificando la implementacion;
en el caso 2, planificando la edicion del archivo).
**Si la auditoria hubiera incluido inspeccion del
bucket negativo desde el inicio**, los falsos claims
nunca se habrian publicado.

La regla AP-1 codifica exactamente esto.

H-F3 — El costo de invalidacion es proporcional a la profundidad
------------------------------------------------------------------

Caso 1 (UC_RPT_05/06): invalidacion en 5 minutos,
porque la auditoria afecto solo a un dominio (reports)
con 16 UCs.

Caso 2 (58 FRs): invalidacion en 5 minutos, porque
afectaba 9 dominios y 103 FRs pero la causa raiz
era trivial (case-sensitive).

Hipotesis: si una auditoria con un falso claim avanza
**varias iniciativas** sin invalidacion (por ejemplo,
iniciativas de implementacion derivadas), el costo de
correccion es **catastrofico** (codigo escrito en base
a un gap inexistente).

Implicacion: validar antes de publicar es **mucho mas
barato** que invalidar despues. La regla R-1 de
``calibration-verified-numbers.md`` lo dice
explicitamente pero no contemplaba el caso grep ciego.

----

Conclusion
===========

* La regla ``.claude/rules/grep-validated-audit.md``
  queda activa para sesiones futuras (carga
  automatica).
* Esta iniciativa documenta el contexto historico,
  las tres asunciones implicitas y la verificacion
  post-ejecucion.
* La leccion epistemica se preserva tanto en formato
  operacional (que hacer) como narrativo (por que).

**Aplicacion inmediata:** las iniciativas pendientes
(``auditar-componentes-ui-sin-marker``,
``enumerar-otros-ucs-inclusion``,
``documentar-ucs-implementados-no-declarados``) deben
aplicar este protocolo desde el inicio. Cualquier
auditoria futura sin la checklist completada queda como
claim SPECULATIVE.

Iniciativas hermanas
=====================

* ``normalizar-convencion-tst-ref-fr`` — registrada en
  ``declarar-tst-ref-en-58-frs-sin-marcar``. Resuelve la
  dualidad de naming TST detectada.
* ``adoptar-protocolo-evidence-classification-en-skills``
  — meta-iniciativa hermana de mayor orden:
  formalizar el patron PROVEN / INFERRED / SPECULATIVE
  en los skills de auditoria (no solo en docs/normativa).
* ``auditar-iniciativas-previas-bajo-grep-validado`` —
  re-auditar las iniciativas cerradas en esta sesion
  para detectar cualquier claim SPECULATIVE que haya
  quedado activo. Trabajo de verificacion retrospectiva.
