.. meta::
   :artefacto: DEEP-ANALISIS-AUDITAR-CONFORMIDAD-FR-TESTS-ACEPTACION
   :tipo: Analisis
   :dominio: gestion
   :subdominio: pm/iniciativas/auditar-conformidad-fr-tests-aceptacion
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T20:46:37
   :ultimo_cambio: 2026-05-19T20:46:37
   :autor: NestorMonroy
   :clasificacion: Interno

.. _deep-analisis-auditar-conformidad-fr-tests-aceptacion:

==============================================================
Deep-Analisis: Conformidad FR -> Tests de Aceptacion
==============================================================

Metodologia
============

**Universo:** todos los archivos ``fr-NNN-NN-*.rst`` bajo
``source/requisitos/requisitos-funcionales/{dominio}/uc-NNN-*/``,
excluyendo dominios OUT (operator, supervision, caller) y
uc-047 (UC de inclusion OUT — ver
``aclarar-uc-047-resolver-segmento``).

**Comando de verificacion:**

.. code-block:: bash

   find source/requisitos/requisitos-funcionales \\
     -name "fr-*.rst" -type f \\
     | grep -vE "/operator/|/supervision/|/caller/" \\
     | wc -l

Output: **103** FRs in-scope.

**Tres preguntas por cada FR:**

1. ¿El RST declara una referencia ``TST-FR-NNN.NN``?
2. Si la declara, ¿esta marcada como "pendiente"?
3. ¿Existe en codigo api algun test que mencione el FR
   (por ID o por TST ref)?

----

Resultados verificados
=======================

Inventario por dominio (in-scope, 103 FRs)
--------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 14 14 14 36

   * - Dominio
     - FRs total
     - Con TST ref
     - Sin TST ref
     - Notas
   * - permissions
     - 22
     - ?
     - ?
     - Mayor concentracion de FRs
   * - auth
     - 21
     - ?
     - ?
     - Login + sesiones complejo
   * - users
     - 17
     - 16+
     - <2
     - Casi todos con TST ref
   * - reports
     - 16
     - ?
     - ?
     -
   * - logs
     - 7
     - ?
     - ?
     -
   * - access
     - 7
     - 5+
     - <3
     -
   * - alerts
     - 5
     - ?
     - ?
     -
   * - pipeline
     - 4
     - ?
     - ?
     -
   * - audit
     - 4
     - ?
     - ?
     -

Totales agregados verificados:

.. code-block:: bash

   # Total FRs in-scope
   cat /tmp/fr-files.txt | wc -l
   # => 103

   # FRs con TST-FR ref declarada
   cat /tmp/fr-files.txt | xargs grep -l "TST-FR" | wc -l
   # => 45

   # FRs sin ninguna TST ref
   cat /tmp/fr-files.txt | xargs grep -L "TST-FR" | wc -l
   # => 58

   # FRs con TST-FR no marcada pendiente
   grep -rE "TST-FR-" source/requisitos/requisitos-funcionales \\
     2>/dev/null | grep -vE "/operator/|/supervision/|/caller/" \\
     | grep -v "pendiente" | wc -l
   # => 0

**Resumen agregado:**

* **45 / 103 (43.7%)** FRs declaran un TST ref formal.
* **45 / 45 (100%)** de los TST refs estan marcados
  ``pendiente`` — ningun FR considera su test ya
  implementado.
* **58 / 103 (56.3%)** FRs **no declaran ningun test**.
* **0 / 45** FRs declaran test en estado distinto a
  pendiente.

FRs referenciados en codigo api
---------------------------------

.. code-block:: bash

   # Cualquier referencia tipo "FR-NNN.NN" o "TST-FR-"
   grep -rohE "FR-[0-9]+\\.[0-9]+|fr_[0-9]+_[0-9]+|TST-FR-[0-9]+" \\
     /home/user/IACT-api/callcentersite/apps/ \\
     /home/user/IACT-api/callcentersite/tests/ \\
     2>/dev/null | sort -u | wc -l

Output: **0**.

.. code-block:: bash

   # Conteo total de ocurrencias
   grep -rE "FR-[0-9]+\\.[0-9]+" \\
     /home/user/IACT-api/callcentersite/apps/ \\
     /home/user/IACT-api/callcentersite/tests/ \\
     2>/dev/null | wc -l

Output: **0**.

**Cero ocurrencias** de FR ID en codigo. La trazabilidad
explicita FR -> test en el codigo es nula.

----

Interpretacion calibrada
==========================

Lo que se sabe (verificado):

* Los 1378 tests pytest de IACT-api passing
  (98.64% de 1397) cubren flujos completos del sistema.
* Los 2381 tests jest de IACT-ui passing cubren la capa
  UI.
* La implementacion api in-scope es **100%** (56/56 UCs
  con marker verificable).
* La trazabilidad explicita FR -> test en codigo es
  **0%** (0/103 FRs referenciados).
* La trazabilidad explicita FR -> test en docs declara
  **100% pendiente** (45/45 TSTs documentados estan
  marcados pendiente).
* 58/103 FRs ni siquiera declaran un TST esperado en docs.

Lo que se infiere:

* Los tests existen y validan que el codigo no rompe,
  pero **no se puede demostrar** que cada FR especifico
  se cumple con un test especifico — solo que el codigo
  asociado al UC funciona bajo los flujos cubiertos.
* La cobertura efectiva por FR puede ser alta (los UCs
  estan implementados y testeados) pero **no es trazable
  ni auditable** sin convencion de marcado.

Lo que NO se puede afirmar:

* "Cada criterio de aceptacion de cada FR esta validado
  por un test especifico" — claim SPECULATIVE bajo la
  evidencia actual.
* "Cada FR es Pass/Fail por al menos un test" — ditto.
* "Las pruebas cubren los 103 FRs in-scope" — ditto.

----

Hallazgos
==========

H-D1 — Convencion de trazabilidad declarada en docs pero no implementada en codigo
------------------------------------------------------------------------------------

Los RST de FRs declaran una columna **TEST** con
``TST-FR-NNN.NN (pendiente)``. La convencion existe — el
codigo solo necesitaria agregar un decorador o docstring
``TST-FR-NNN.NN`` en cada test que valida el FR para
cerrar el ciclo.

Sin embargo, **0 tests api referencian FRs**. La
convencion docs nunca se aplico al codigo.

H-D2 — 58 FRs sin TST ref declarado son la mayor brecha
---------------------------------------------------------

De los 103 FRs in-scope, **58 (56.3%) no declaran ningun
test esperado** en su RST. Estos no solo carecen de
trazabilidad — carecen de la **declaracion del criterio
de validacion**.

Sin la declaracion, no se puede ni siquiera medir si el
test pendiente existe — porque no se sabe que test
buscar.

H-D3 — Posible cobertura informal alta, formal nula
-----------------------------------------------------

Los 1378 tests api passing presumiblemente cubren la
funcionalidad descrita por los 103 FRs (todos los UCs
in-scope tienen tests). Pero la cobertura es **por UC**,
no **por FR**. La granularidad TST-FR-NNN.NN no se
traduce 1-a-1 a un test concreto en codigo.

Implicacion: si un FR cambia (p.ej. el criterio de
aceptacion se vuelve mas estricto), no hay forma de
identificar **que tests** necesitan revisarse. La auditoria
de impacto cambio-de-FR -> tests es manual y costosa.

H-D4 — TST-FR pendiente como estado universal
-----------------------------------------------

Que los 45 TST refs declarados esten **todos** marcados
"pendiente" sugiere que la convencion se creo pero
ningun ciclo de implementacion la cerro. Es deuda
metodologica: el proyecto adopto la nomenclatura sin
adoptar el flujo de trazabilidad.

H-D5 — Diferencia con la cobertura UC (100%)
----------------------------------------------

La cobertura UC -> implementacion es **100%** (56/56)
pero la cobertura FR -> test es **0%**. La discrepancia
revela que las dos preguntas son **distintas**:

* "El sistema implementa los flujos de los UCs?" → SI
  (100% in-scope).
* "Cada criterio de aceptacion FR esta validado
  explicitamente?" → NO (0% trazable).

Una iniciativa de conformidad real requiere cerrar el
gap entre las dos preguntas.

----

Recomendaciones
================

R-1 — Adopcion de convencion de marcado en tests
-------------------------------------------------

Cada test que valida un criterio de aceptacion de un FR
debe declarar el TST ref en su docstring o como
decorador pytest:

.. code-block:: python

   @pytest.mark.tst_fr("FR-001.02")
   def test_validar_credenciales_usuario_inexistente():
       """TST-FR-001.02: usuario sin cuenta retorna 401."""
       ...

Esto habilita:

* ``pytest -m "tst_fr"`` para correr solo tests de
  conformidad.
* Grep automatico de FR -> test para auditoria.
* Reverse-trace: para cada FR, listar sus tests.

R-2 — Cerrar la brecha de 58 FRs sin TST ref
---------------------------------------------

Iniciativa derivada **declarar-tst-ref-en-58-frs-sin-marcar**:
revisar cada uno de los 58 FRs sin declaracion y anadir
la tabla TEST con TST-FR-NNN.NN (pendiente).

R-3 — Cerrar los 45 TST-FR pendientes
---------------------------------------

Para cada uno de los 45 FRs con TST declarado pendiente,
**implementar el test** que valida el criterio de
aceptacion explicito (no solo el flujo generico). Esto
es trabajo masivo: 45 tests nuevos minimo.

Iniciativa derivada
**implementar-tst-fr-conformidad-por-dominio** (split
por dominio: ``implementar-tst-fr-auth``,
``implementar-tst-fr-users``, etc.).

R-4 — Comprometer la convencion en CI
---------------------------------------

Una vez los tests existan con el decorador del R-1,
agregar un gate de CI que verifique:

* Cada FR-NNN.NN tiene al menos un test con su
  decorador.
* Ningun FR queda sin test asociado.

Iniciativa derivada
**ci-gate-conformidad-fr-tests**.

R-5 — Aceptar la brecha como deuda explicita
----------------------------------------------

Si el sponsor decide no cerrar la brecha (R-2/R-3/R-4)
en el corto plazo, registrar la deuda formal en
``source/risks-technical-debt/deuda-conformidad-fr-tests.rst``
con priorizacion y duenio.

----

Conclusion
===========

* Cobertura **UC -> implementacion: 100%** in-scope api
  (56/56).
* Cobertura **FR -> test trazable: 0%** (0/103 FRs
  con test referenciado en codigo).
* **45 / 103** FRs declaran TST esperado (pendiente).
* **58 / 103** FRs ni declaran TST esperado.
* La convencion de marcado existe en docs (``TST-FR-NNN.NN``)
  pero nunca se aplico al codigo. Deuda metodologica
  identificada.

**Respuesta calibrada actualizada a "se implementaron
todos los flujos?":**

* En sentido **macro** (el sistema funciona, los UCs
  estan codificados, los tests genericos pasan): **SI**.
* En sentido **conformidad estricta** (cada FR tiene un
  test que valida su criterio de aceptacion): **NO** —
  solo 0% trazable, aunque la cobertura efectiva probablemente
  sea mayor (no medible sin convencion).

Iniciativas candidatas registradas (4):

1. ``declarar-tst-ref-en-58-frs-sin-marcar``
2. ``implementar-tst-fr-conformidad-por-dominio``
3. ``ci-gate-conformidad-fr-tests``
4. ``registrar-deuda-conformidad-fr-tests-en-risks``
