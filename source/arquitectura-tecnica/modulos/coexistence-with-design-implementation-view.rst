.. meta::
 :artefacto: AT_MODULOS_COEXISTENCE_DESIGN_IMPL
 :tipo: Documento de coexistencia
 :dominio: arquitectura_tecnica
 :subdominio: modulos
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-modulos-coexistence:

=========================================================
Coexistencia con DesignView e ImplementationView
=========================================================

Este documento registra **formalmente** la decision sobre la
relacion entre el cajon ``arquitectura-tecnica/modulos/`` y los
cajones de las vistas Kruchten ``design-view/`` e
``implementation-view/``. Origen: hallazgo H-02 del WP
``process-deploy-view-rename`` (2026-05-08), validado por el WP
``dag-completion-loop``.

Conclusion
==========

**Coexistencia legitima — sin solapamiento.** Los tres cajones
documentan **dimensiones diferentes** del mismo modulo
arquitectonico, con audiencia y proposito distintos.

Tabla de responsabilidades
===========================

.. list-table::
 :widths: 22 26 26 26
 :header-rows: 1

 * - Pregunta del lector
   - ``modulos/<mod>/``
   - ``design-view/<mod>/``
   - ``implementation-view/<mod>/``
 * - Que es este modulo y por que existe?
   - **Si** — proposito, responsabilidades funcionales,
     dependencias, restricciones del modulo, KPIs.
   - No
   - No
 * - Cual es el modelo conceptual / dominio?
   - No
   - **Si** — bounded context, agregados, entidades,
     value objects, invariantes, ciclo de vida.
   - No
 * - Como esta organizado el codigo?
   - No
   - No
   - **Si** — capas (api/service/repository/orm),
     paquetes Python, interfaces de framework,
     adaptadores externos.
 * - Que diagramas UML aplican?
   - Componentes alto nivel (caja negra),
     secuencias representativas inter-modulo.
   - Clases de dominio, secuencias intra-bounded-context,
     estados de agregados.
   - Componentes fisicos (paquetes de codigo),
     secuencias capa-a-capa.

Audiencia tipica
=================

- ``modulos/<mod>/`` — **arquitecto de sistema, tech lead,
  product owner.** Lee para entender el modulo como bloque del
  sistema, sus dependencias y su ubicacion en el panorama.
- ``design-view/<mod>/`` — **diseñador de software,
  desarrollador senior.** Lee para entender el modelo de
  dominio y el comportamiento conceptual antes de implementar.
- ``implementation-view/<mod>/`` — **desarrollador
  implementador.** Lee para encontrar el codigo, los modulos
  Python, las capas y los puntos de extension.

Que NO se duplica
==================

Los tres cajones referencian el mismo modulo (``MOD_AUTH``,
``MOD_USER_IDENTITY``, etc.) pero **NO repiten el mismo
contenido**:

- Si una entidad de dominio aparece en ``design-view/``, el
  cajon ``modulos/`` NO duplica su descripcion — la
  referencia con ``:doc:``.
- Si una clase Python aparece en ``implementation-view/``, el
  cajon ``design-view/`` NO la documenta como clase Python —
  documenta su contraparte conceptual de dominio.
- Si una restriccion de negocio se documenta en ``modulos/``,
  no se repite en las vistas — se referencia.

Que SI puede aparecer en mas de un cajon
==========================================

- **Diagramas UML del mismo elemento** con vista distinta:
  por ejemplo, una secuencia inter-modulo (vista logica
  alto nivel en ``modulos/<mod>/diagramas/``) y la misma
  secuencia descompuesta capa-a-capa
  (``implementation-view/<mod>/sequence-...``). Son vistas
  complementarias, no copias.
- **Referencias cruzadas** (``:doc:``, ``:ref:``) — todos los
  cajones se referencian mutuamente para que el lector pueda
  navegar entre dimensiones.

Verificacion del principio
============================

Si en una revision se detecta contenido **identico** entre dos
cajones (mismo texto, mismo diagrama, misma tabla), eso indica
violacion de la coexistencia y debe consolidarse en uno solo
con referencia desde el otro.

Si el contenido es **distinto pero del mismo dominio**, la
coexistencia es legitima y se documenta con ``:doc:`` cruzado.

.. seealso::

 - :doc:`index` — listado de los 13 modulos arquitectonicos.
 - :doc:`/arquitectura-tecnica/design-view/index` —
   vista logica del sistema.
 - :doc:`/arquitectura-tecnica/implementation-view/index` —
   vista de implementacion del sistema.
 - WP ``process-deploy-view-rename`` (H-02) — origen del
   analisis preliminar.
 - WP ``dag-completion-loop`` — formalizacion de la decision.
