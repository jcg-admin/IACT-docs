.. _uc-inc-rpt-01-parte-09:

=================================
Parte 9 — Criterios de aceptacion
=================================

Formato Given/When/Then para verificacion de la resolucion
de segmentos del usuario antes de cualquier consulta a la
Base Analitica IVR.

9.1 CA-01: Resolucion para usuario con un segmento
==================================================

**DADO** un usuario con ``segment_id=1`` (nacional_A) y
sin permisos extendidos,

**CUANDO** un UC_RPT_xx invoca UC_INC_RPT_01,

**ENTONCES**:

- Resultado: ``segments = [1]`` (solo nacional_A).
- Tiempo de resolucion P50 ≤ 50 ms.
- Cache hit en sesiones subsiguientes (TTL 300s).

9.2 CA-02: Resolucion para usuario con permiso global
=====================================================

**DADO** un usuario con capability
``view_all_segments`` (``is_active=True``),

**CUANDO** un UC_RPT_xx invoca UC_INC_RPT_01,

**ENTONCES**:

- Resultado: ``segments = [1, 2, 3]`` (todos los
  segmentos disponibles).
- ``es_global = true`` en la respuesta.

9.3 CA-03: Resolucion para usuario sin segmento
===============================================

**DADO** un usuario sin ``segment_id`` (NULL — caso de
super-admin sin segmento operativo),

**CUANDO** un UC_RPT_xx invoca UC_INC_RPT_01,

**ENTONCES**:

- Si tiene capability ``view_all_segments``: ``segments``
  contiene todos.
- Si NO tiene la capability: rechazo con
  ``{"error": "no_segment_assigned"}`` y log de seguridad.

9.4 CA-04: Cache hit reduce latencia
====================================

**DADO** un usuario que invoco UC_INC_RPT_01 hace 60
segundos,

**CUANDO** un nuevo UC_RPT_xx invoca UC_INC_RPT_01 para
el mismo usuario,

**ENTONCES**:

- Resultado servido desde cache.
- P50 ≤ 5 ms (vs 50 ms cache MISS).

9.5 CA-05: Invalidacion de cache tras cambio RBAC
=================================================

**DADO** un usuario con segments cacheados,

**CUANDO** un UC de RBAC modifica sus capabilities (e.g.,
UC_PERM_06 le quita ``view_all_segments``),

**ENTONCES**:

- Cache de ``segments:user:{id}`` invalidado.
- Proxima invocacion ejecuta resolucion completa contra
  el repositorio operacional.

9.6 CA-06: Falla del repositorio operacional
============================================

**DADO** el repositorio operacional inaccesible
(timeout / connection error),

**CUANDO** un UC_RPT_xx invoca UC_INC_RPT_01,

**ENTONCES**:

- UC_RPT_xx recibe error transient.
- Cache no se actualiza.
- Audit event ``SEGMENT_RESOLUTION_FAILED`` con
  ``user_id``, ``error``, ``timestamp``.

9.7 CA-07: BR-012 enforcement
=============================

**DADO** un usuario operativo (``segment_id`` con FK NOT
NULL per BR-012),

**CUANDO** UC_INC_RPT_01 resuelve sus segmentos,

**ENTONCES**:

- ``segment_id`` es **permanente** (BR-012 — no switchable
  en runtime).
- Resultado refleja exclusivamente el ``segment_id``
  asignado al usuario al momento de creacion.

9.8 CA-08: Multiples invocaciones en mismo request
==================================================

**DADO** un UC_RPT_xx que internamente invoca varios
sub-queries,

**CUANDO** cada sub-query invoca UC_INC_RPT_01,

**ENTONCES**:

- Resolucion se ejecuta una sola vez por request
  (memoizacion intra-request, ortogonal al cache de TTL).
- Subsiguientes invocaciones en el mismo request reutilizan
  el resultado en memoria.

.. seealso::

 - :doc:`/requisitos/reglas-negocio/br-012-usuario-segmento-unico`.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-14/index` —
   consumidor.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-17/index` —
   consumidor.
