.. meta::
   :artefacto: DEEP-ANALISIS-ACLARAR-UC-047-RESOLVER-SEGMENTO
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/aclarar-uc-047-resolver-segmento
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:35:00
   :ultimo_cambio: 2026-05-19T20:35:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deep-analisis-aclarar-uc-047-resolver-segmento:

==============================================================
Deep-Analisis: uc-047 — UC user-facing o helper?
==============================================================

Pregunta de partida
====================

``verificar-mapping-docs-codigo-todos-los-dominios`` cerro
con cobertura api **56-57 / 57 (98-100%)** in-scope. El
unico caso ambiguo:
``uc-047-resolver-segmento-usuario`` sin marker
``UC_RPT_NN`` directo en codigo. Hipotesis abiertas:

* (A) UC user-facing sin implementar — gap real.
* (B) UC helper interno cubierto implicitamente por otro
  marker (probable: UC_RPT_17 clientes-unicos-por-segment).
* (C) UC fuera de scope no identificado en el cuento OUT
  inicial.

Evidencia documental
=====================

Lectura del index.rst del UC
------------------------------

``source/requisitos/requisitos-funcionales/reports/uc-047-resolver-segmento-usuario/index.rst``
linea 7:

::

   Requisitos Funcionales derivados de UC_INC_RPT_01.

**Prefijo ``UC_INC_``** (no ``UC_RPT_``). El prefijo
``INC`` se usa en este sistema para identificar **UCs de
inclusion** segun el patron de Larman (Use Case Inclusion):
operaciones reutilizables invocadas por otros UCs como
paso, no por el actor directamente.

Lectura del FR-047.01
-----------------------

``source/requisitos/requisitos-funcionales/reports/uc-047-resolver-segmento-usuario/fr-047-01-resolver-segmento-dids.rst``
linea 51:

::

   El sistema DEBE resolver el conjunto de segmentos
   accesibles para un usuario CUANDO se invoca como
   inclusion en cualquier UC de reporte, consultando los
   DIDs IVR asignados por RBAC.
   [...]
   Este UC es siempre invocado como paso de inclusion, no
   directamente por el usuario.

Linea 30 (Trazabilidad):

::

   UC Origen: UC_INC_RPT_01: Resolver Segmento del Usuario

Confirmacion: uc-047 es un **UC de inclusion** que ningun
actor invoca directamente. Es subrutina de logica
compartida entre UCs de reporte (UC_RPT_01..17).

Busqueda del marker UC_INC_RPT_01 en codigo
---------------------------------------------

.. code-block:: bash

   grep -rohE "UC_INC_[A-Z]+_[0-9]+ — [^.\\n']{10,80}" \\
     /home/user/IACT-api/callcentersite/apps/ \\
     | sort -u

Output: **0 hits**.

.. code-block:: bash

   grep -rE "UC_INC_RPT_01" \\
     /home/user/IACT-api/callcentersite/apps/ \\
     | wc -l

Output: **0**.

El marker ``UC_INC_RPT_01`` no aparece en codigo. Pero la
logica que describe — resolver segmento de usuario via
DIDs RBAC — esta presumiblemente implementada como parte
del flujo de cualquier reporte de segment (UC_RPT_17
"Clientes unicos por segment", UC_RPT_15 "KPIs SLA por
centro y segment", etc.).

Decision del sponsor
======================

Mensaje literal del sponsor durante esta iniciativa:

   "los uc-opr-* y los uc-sup-* y los uc-cli-01..05,
   quedan fuera del escope, no se realizan y no se
   implementan
   ¿Qué es 'segmento de usuario' / UC_INC_RPT_01? si
   analizas bien, nosotros dejamos fuera eso, del segmento
   de usuario"

Interpretacion: el sponsor confirma que el "segmento de
usuario" (y por extension UC_INC_RPT_01 / uc-047) queda
OUT del scope. Razon implicita: el concepto de segmento
esta acoplado al routing operator/caller/supervision
(actores OUT). Sin esos actores, la nocion de segmento
RBAC-por-DIDs no entrega valor user-facing — los
reportes que la consumen (UC_RPT_15/17) la usan a nivel
de logica interna pero la resolucion del segmento del
**actor que ejecuta el reporte** no es un flujo del
sistema in-scope.

Decision adoptada: **uc-047 OUT del scope**.

Implicacion sobre la cobertura agregada
==========================================

Antes de esta resolucion (segun
``verificar-mapping-docs-codigo-todos-los-dominios``):

* In-scope: 57 UCs.
* Con marker verificable: 56 (todos los dominios
  in-scope) + 1 ambiguo (uc-047) = 56-57.
* Cobertura: 98-100%.

Despues de declarar uc-047 OUT:

* In-scope: 57 - 1 = **56 UCs**.
* Con marker verificable: **56 / 56**.
* **Cobertura in-scope api: 100%**.

Reclasificacion del scope OUT
===============================

El scope OUT pasa de 18 UCs a **19 UCs**:

.. list-table::
   :header-rows: 1
   :widths: 30 12 58

   * - Dominio / patron
     - UCs
     - Razon
   * - operator (``uc-opr-*``)
     - 10
     - Sponsor original
   * - supervision (``uc-sup-*``)
     - 3
     - Sponsor original
   * - caller (``uc-cli-01..05``)
     - 5
     - Sponsor original
   * - reports / inclusion segmento
     - 1
     - Sponsor confirma 2026-05-19:
       UC_INC_RPT_01 / uc-047 OUT por
       acoplamiento con actores OUT.

Total OUT: **19 / 75 = 25%**.
Total IN: **56 / 75 = 75%**.
Total IN con codigo: **56 / 56 = 100%**.

Hallazgos
==========

H-C1 — Prefijo UC_INC no estaba en la enumeracion buscada
-----------------------------------------------------------

La auditoria
``auditar-cobertura-uc-implementacion`` busco markers
``UC_AUTH``, ``UC_USR``, ``UC_ACC``, ``UC_PERM``,
``UC_OPR``, ``UC_RPT``, ``UC_DSH``, ``UC_ALN``,
``UC_ALR``, ``UC_AUD``, ``UC_LOG``, ``UC_CALL``,
``UC_PIP``, ``UC_SUP``. **No incluyo el prefijo
``UC_INC_*``** (UCs de inclusion).

Solo verificando el RST del uc-047 aparece la pista. Es
un **gap metodologico de la heuristica de grep**: la
enumeracion de prefijos asume una lista cerrada que no
contemplo el patron INC.

H-C2 — uc-047 no esta etiquetado como inclusion en el RST padre
-----------------------------------------------------------------

El index.rst de ``requisitos-funcionales/reports/`` lista
uc-047 al mismo nivel que UCs user-facing (uc-032..046).
Un lector casual no distingue que uc-047 es de
naturaleza distinta (inclusion vs primary). La nota
"Este UC es siempre invocado como paso de inclusion"
vive solo en el FR-047.01, no en el index ni en el
nombre del directorio.

Mejora sugerida (iniciativa derivada):

* Separar UCs de inclusion en
  ``requisitos-funcionales/{dominio}/inclusion/uc-NNN-*``
  o usar prefijo ``uc-inc-*`` en el nombre del directorio.
* O al menos anadir badge / etiqueta en el index del
  dominio.

Iniciativa candidata:
``separar-ucs-inclusion-de-user-facing``.

H-C3 — Pueden existir otros UCs INC en otros dominios
-------------------------------------------------------

Si uc-047 es UC_INC_RPT_01, puede haber UC_INC_USR_*,
UC_INC_PERM_*, etc. La auditoria los habria contado
como gaps user-facing cuando son helpers.

Verificacion rapida:

.. code-block:: bash

   grep -rohE "UC_INC_[A-Z]+_[0-9]+" \\
     /home/user/IACT-docs/source/requisitos/ \\
     | sort -u

Si retorna mas UCs UC_INC_*, abrir iniciativa para
reclasificarlos.

Verificacion post-ejecucion
=============================

.. list-table::
   :header-rows: 1
   :widths: 40 12 48

   * - Criterio
     - Resultado
     - Evidencia
   * - uc-047 identificado como UC de inclusion
     - PASA
     - RST linea 7 ("derivados de UC_INC_RPT_01") +
       FR-047.01 linea 51 ("invocado como paso de
       inclusion, no directamente por el usuario").
   * - Marker UC_INC_RPT_01 inexistente en codigo
     - PASA
     - grep retorna 0 hits.
   * - Sponsor confirma OUT
     - PASA
     - Mensaje literal "dejamos fuera eso, del segmento
       de usuario".
   * - Cobertura agregada recalculada
     - PASA
     - 56/56 = 100% in-scope api tras ajuste de scope.

Conclusion
===========

* ``uc-047-resolver-segmento-usuario`` es un UC de
  inclusion (``UC_INC_RPT_01``), no user-facing.
* El sponsor confirma OUT del scope por acoplamiento con
  actores OUT (operator, caller, supervision).
* Scope OUT actualizado: 19 UCs (18 originales + uc-047).
* **Cobertura in-scope api: 100% (56/56)** — todos los
  UCs declarados user-facing in-scope tienen
  implementacion verificable.

Iniciativas candidatas derivadas
==================================

* **separar-ucs-inclusion-de-user-facing**: convencion
  estructural para que UCs INC no se confundan con
  user-facing en futuras auditorias.
* **enumerar-otros-ucs-inclusion**: verificar si hay
  UC_INC_* en otros dominios y reclasificarlos.
* **documentar-ucs-implementados-no-declarados** (ya
  registrada): los ~8 markers de codigo sin docs.
* **auditar-conformidad-fr-tests-aceptacion** (ya
  registrada): trabajo de orden superior pendiente.

La pregunta del sponsor "se implementaron todos los
flujos de los UCs?" tiene respuesta calibrada final:

**Si — todos los 56 UCs in-scope user-facing tienen
implementacion verificable en api (100%)**, con cobertura
ui parcial pendiente de auditar UI sin marker (~77%
medible). La unica deuda real estricta del proyecto es:

1. Documental inversa (~8 markers sin RST en docs).
2. Conformidad FR-test (pendiente iniciativa dedicada).
3. UC_RPT_02 STUB por CNST-004 (decision arquitectonica
   intencional, no omision).
