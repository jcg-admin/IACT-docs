.. meta::
   :artefacto: DECISIONES-IMPLEMENTAR-UC-RPT-05-06-PROGRAMACION-REPORTES
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/implementar-uc-rpt-05-06-programacion-reportes
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:25:00
   :ultimo_cambio: 2026-05-19T20:25:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _decisiones-implementar-uc-rpt-05-06-programacion-reportes:

==============================================================
Decisiones: Implementar UC_RPT_05/06 (cancelada por discovery)
==============================================================

Decisiones de diseno
=====================

D1 — Cerrar la iniciativa sin producir codigo
-----------------------------------------------

Tras T-002 quedo claro que el scaffolding completo de
programacion de reportes ya existia: views, service, model,
serializers, URLs probablemente registradas. Implementar
codigo "nuevo" duplicaria el existente o lo reescribiria
sin justificacion.

Considerado: borrar el scaffolding existente y
reimplementar desde cero bajo los markers UC_RPT_05/06
para que el mapping fuera lineal. **Descartado:**
modificar codigo funcional con el unico objetivo de
satisfacer una numeracion teorica es anti-valor. La
implementacion existente bajo UC_RPT_07/08 es la fuente
de verdad operativa.

Decision tomada: cerrar la iniciativa COMPLETADA con
estado "discovery" — entrega es la calibracion correcta
del claim previo, no codigo.

D2 — Actualizar el deep-analysis previo
-----------------------------------------

El deep-analysis de
``auditar-cobertura-uc-implementacion`` afirmo que los
UCs uc-036/uc-037 estaban "sin implementacion en api ni
ui". Ese claim era SPECULATIVE (sin observable que lo
respaldara directamente — el grep retorno 0 hits, pero
0 hits no implica ausencia de implementacion bajo otro
marker).

Por la regla
``calibration-verified-numbers.md`` (NUNCA un numero/
afirmacion sin verificar), corresponde corregir el
deep-analysis con una nota explicita sobre el bug de
mapping y la implementacion encontrada.

Decision tomada: actualizar
``auditar-cobertura-uc-implementacion/deep-analisis-cobertura-uc-implementacion.rst``
en commit posterior con bump 1.0.0 -> 1.1.0 (MINOR
porque agrega seccion de correccion sin contradecir el
resto de la auditoria). El claim original queda en el
historial; la version nueva lo refuta con observables.

D3 — No revisitar CNST-004 en esta iniciativa
-----------------------------------------------

UC_RPT_02 (real-time metrics) es STUB por restriccion
CNST-004 (NO Channels, NO Celery, NO Redis). El sponsor
puede o no querer revisitar esa restriccion para habilitar
real-time SSE.

Considerado: cuestionar CNST-004 aqui, ya que el unico
gap real depende de esa restriccion. **Descartado:** el
alcance era implementar UC_RPT_05/06; revisitar CNST-004
es decision arquitectonica de mayor orden que requiere
sponsor + analisis costo/beneficio (que pierde el
proyecto si introduce Channels o Redis vs que gana en
funcionalidad real-time).

Decision tomada: dejar UC_RPT_02 como STUB con anota
"intencional por CNST-004". Si el sponsor quiere
revisitar, abre
``revisar-cnst-004-realtime-metrics``.

D4 — Mantener nombre original de la iniciativa
-----------------------------------------------

Considerado: renombrar a
``corregir-mapping-uc-rpt-docs-codigo`` para reflejar el
resultado discovered. **Descartado:** renombrar directorios
en RST requiere actualizar toctrees y links; rompe la
trazabilidad git si los archivos cambian de path. El
nombre original ``implementar-uc-rpt-05-06-...`` queda
con admonicion ``important`` al inicio del index explicando
que el resultado fue discovery, no implementacion.

Decision tomada: mantener nombre. La admonicion
``.. admonition:: Resultado: NO REQUIERE IMPLEMENTACION``
al tope del index hace evidente el outcome sin renombrar.

Hallazgos durante la ejecucion
================================

H-E1 — El mapping docs <-> codigo no es lineal
------------------------------------------------

Documentado en el deep-analysis. Critico: invalida una
asuncion implicita del deep-analysis previo.

H-E2 — Existe scaffolding sustancial no detectable por grep ciego
-------------------------------------------------------------------

202 lineas de view + 67 lineas de service + modelo +
serializers + URLs. El grep de marker no detecta esto
porque el marker en docstring es distinto del marker
buscado.

H-E3 — UC_RPT_02 STUB documenta CNST-004 explicitamente
---------------------------------------------------------

La decision esta documentada en codigo, no solo en
gobernanza. Es buen patron: la restriccion arquitectonica
es visible al desarrollador que toca el codigo.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 38 12 50

   * - Criterio del alcance
     - Resultado
     - Evidencia
   * - Mapping correcto documentado
     - PASA
     - Tabla completa en
       ``deep-analisis-implementar-uc-rpt-05-06-programacion-reportes``
       seccion "Mapping correcto observado".
   * - Actualizacion del deep-analysis previo
     - Pendiente
     - Por hacerse en commit posterior; alcance
       de esta iniciativa requiere registrar el
       compromiso (D2), no la ejecucion.
   * - Unico gap real identificado
     - PASA
     - ``UC_RPT_02 STUB por CNST-004`` documentado
       con evidencia textual del codigo.
   * - Iniciativa cerrada sin codigo nuevo
     - PASA
     - 0 commits en IACT-api de esta rama.

Deuda nueva registrada
========================

* **verificar-mapping-docs-codigo-todos-los-dominios**:
  los otros 11 dominios pueden tener el mismo bug
  de linearidad asumida. Verificar caso por caso.
* **documentar-stubs-en-rst-de-uc**: el RST de uc-033
  no menciona que la implementacion es STUB. Otros
  UCs pueden tener stubs no anotados en docs.
* **revisar-cnst-004-realtime-metrics**: si el sponsor
  quiere real-time real, hay que cuestionar CNST-004
  antes de implementar.

Conclusion
==========

La iniciativa cumplio su criterio de completitud sin
producir codigo. El valor entregado es:

1. Correccion calibrada de un claim SPECULATIVE del
   deep-analysis previo.
2. Mapping correcto docs <-> codigo para reports.
3. Identificacion del unico gap real (UC_RPT_02 STUB)
   con su causa raiz (CNST-004).
4. Tres iniciativas hermanas derivadas para deuda real.

Bajo el principio "no dejar deuda tecnica observable":
el claim erroneo del deep-analysis quedo como deuda
documental hasta que se actualice (compromiso de D2).
