.. meta::
 :artefacto: ADR-GOB-009
 :tipo: ADR
 :dominio: normativa
 :subdominio: gobernanza
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Critico

.. _adr-gob-009:

================================================================
ADR-GOB-009: RBAC Modelo Conceptual (Supersede BACK-001/004)
================================================================

**Estado:** Aprobado.

**Fecha:** 2026-04-29.

**Decisores:** NestorMonroy.

**Supersede:**

- :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`
- :doc:`/backend/adr-back-004-sistema-permisos-sin-roles-jerarquicos`

**Relacionados (no superseded):**

- :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`
  (decision de coexistencia ACC + PERM, sigue vigente)
- :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`
- :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod`
- :doc:`/normativa/restricciones/cnst-031-permisos-temporales-maximo-6-meses`
- :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`
- :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact` (modelo v5.2.1)

----

1. Contexto
===========

Tras la consolidacion del modelo RBAC IACT v5.2.1 (enero 2026)
y la decision de coexistencia ACC + PERM (ADR-GOB-008,
2026-04-29), los ADRs legacy ``ADR-BACK-001`` (grupos funcionales
sin jerarquia) y ``ADR-BACK-004`` (sistema permisos sin roles
jerarquicos) presentaban inconsistencias materiales con el corpus
normativo vigente:

- ``ADR-BACK-001`` cita "**19 funciones**" y "**130+
  capacidades**" — cifras divergentes del modelo v5.2.1 vigente
  (42 funciones + 10 grupos AGR-001..AGR-010).
- ``ADR-BACK-001/004`` usan vocabulario "**Capacidad**" que
  CNST-033 vigente PROHIBE explicitamente.
- ``ADR-BACK-001 + ADR-BACK-004`` documentan **la misma
  decision conceptual** (RBAC sin roles jerarquicos) desde dos
  angulos — son redundantes.
- ``ADR-BACK-004`` tiene una nota in-text "DOCUMENTAR MATRIZ
  RACI" inadecuada para un ADR aceptado (ver Diferido).

Este ADR consolida la decision conceptual canonica del modelo
RBAC IACT alineada al corpus vigente, **superseding ambos
legacy** sin perdida de informacion (los originales se preservan
con marcador Superseded).

----

2. Decision
===========

2.1 Modelo RBAC IACT canonico
-----------------------------

El modelo RBAC del proyecto IACT es:

1. **Plano** — sin jerarquia de roles ni herencia ABAC
   compleja. Per :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.
2. **Granular** — la unidad asignable es la **Funcion atomica**
   (1 verbo + 1 sustantivo).
3. **Catalogo cerrado** — **42 funciones atomicas** distribuidas
   en **8 modulos** funcionales (MOD_Auth, MOD_Users,
   MOD_Access, MOD_Pipeline, MOD_Reports, MOD_Alerts,
   MOD_Audit, MOD_Logs).
4. **10 grupos predefinidos** AGR-001..AGR-010 que agrupan
   funciones tipicas para perfiles operativos.
5. **Custom groups** creables por administradores tecnicos
   (D-RBAC-4) — distincion entre **system groups** (inmutables)
   y **custom groups** (creables).
6. **3 reglas SoD** declarativas (SOD-001/002/003) per
   :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod`.
7. **Permisos excepcionales temporales** con duracion maxima
   **6 meses** per
   :doc:`/normativa/restricciones/cnst-031-permisos-temporales-maximo-6-meses`.
8. **Sin etiquetas jerarquicas** organizacionales (no Admin,
   no Supervisor, no Manager, no Senior). Filosofia "Sin
   Pretensiones".

2.2 Vocabulario canonico (CNST-033)
-----------------------------------

- **"Funcion"** (docs en espanol) / **"Function"** (codigo en
  ingles) — termino canonico para la unidad atomica.
- **"FunctionGroup"** — agrupacion (system o custom).
- **"UserFunctionAssignment"** — asignacion de funciones a
  usuarios via grupos.
- **"FunctionSeparationRule"** — regla SoD entre funciones.

PROHIBIDOS: "Capacidad", "Capacity" (D-RBAC-1).

2.3 Coexistencia ACC + PERM (per ADR-GOB-008)
---------------------------------------------

El sistema mantiene dos vistas:

- **Vista funcional MOD_Access** (admin no-tech) — UC_ACC_01..09.
- **Vista tecnica MOD_Permissions** (admin tech) — UC_PERM_01..10.

Reconciliadas en codigo a traves del vocabulario unificado y la
decision de migracion ``Capacidad`` -> ``Function`` (D-RBAC-8).

----

3. Justificacion
================

3.1 Por que un solo ADR conceptual
----------------------------------

ADR-BACK-001 y ADR-BACK-004 abordan el mismo problema con
overlap significativo. Consolidar en un ADR unico:

- Elimina redundancia.
- Da una sola fuente de verdad para el modelo conceptual.
- Reduce el esfuerzo de mantener consistencia cruzada.

3.2 Por que en gobernanza (no en backend)
-----------------------------------------

El modelo conceptual RBAC es decision **transversal** del
proyecto (afecta backend, frontend, requisitos, normativa).
Ubicarlo en backend lo restringe semanticamente. Per la
convencion STD-007 v2.0.2 §4 "Ubicacion fisica de los ADRs",
los adr-gob-* viven en gobernanza. Este ADR usa el modulo
``gob`` (gobernanza) en lugar de ``back`` para reflejar su
naturaleza transversal.

3.3 Por que cifras 42/10/3 (no 19/130+/0)
-----------------------------------------

El modelo v5.2.1 (vigente, en
:doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact`) declara:

- **42 funciones** distribuidas en 8 modulos:
  Auth=4, Users=9, Access=5, Pipeline=4, Reports=8, Alerts=6,
  Audit=4, Logs=2.
- **10 grupos** AGR-001..AGR-010.
- **3 reglas SoD** SOD-001/002/003.

Las cifras "19/130+" del legacy ADR-BACK-001 corresponden a un
estado anterior de diseno (octubre-noviembre 2025) que evoluciono
mediante:

1. Modelo v4.0 "Sin Pretensiones" (~75 funciones con namespaces).
2. Consolidacion v5.0/v5.1.
3. Recalibracion v5.2.0 -> v5.2.1 (correccion de 87+ errores;
   ver :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`).

3.4 Por que vocabulario "Funcion" canonico
------------------------------------------

D-RBAC-1 documentado en ADR-GOB-008 establece:

   "Vocabulario unico 'Funcion' canonico (docs) / 'Function'
   (codigo)."

El termino "Capacidad" sugiere atributo del usuario (lo que
puede hacer). El termino "Funcion" describe **que hace** la
operacion (action). El modelo IACT define la accion atomica, no
la propiedad del actor. Ver
:doc:`/gestion/evidencia/rbac-historia/capacidades-vs-permisos-comparativo`
para el analisis comparativo completo.

----

4. Consecuencias
================

4.1 Positivas
-------------

- Single source of truth conceptual para el modelo RBAC.
- Cifras consistentes (42/10/3) en todo el corpus.
- Vocabulario unificado enforzable via CNST-033.
- Trazabilidad historica preservada (ADRs legacy con marcador
  Superseded).
- Implementabilidad correcta del sistema RBAC futuro
  garantizada (sin ambiguedad entre legacy y vigente).

4.2 Negativas mitigadas
-----------------------

- Lectores externos que conocian ADR-BACK-001/004 deben
  re-orientar a este ADR. Mitigacion: el marcador "Superseded
  by" en el legacy apunta directamente.
- Analisis y disenos pasados que asumian "19/130+" deben
  recalibrar a "42/10/3". Mitigacion: documentos historicos en
  :doc:`/gestion/evidencia/rbac-historia/index` documentan la
  evolucion.

----

5. Diferido (out-of-scope)
==========================

5.1 DEBT-RBAC-RACI
------------------

La nota in-text de ADR-BACK-004 sugeria documentar una **matriz
RACI** sobre las funciones del sistema. Esta es una propuesta
legitima pero excede el scope de este ADR conceptual.

**Diferido como DEBT-RBAC-RACI** en
:doc:`/risks-technical-debt/deuda-tecnica-rebuild` para abordar
en un WP propio cuando se priorice.

----

6. Trazabilidad historica
=========================

Documentos historicos del subsistema RBAC en
:doc:`/gestion/evidencia/rbac-historia/index`:

- :doc:`/gestion/evidencia/rbac-historia/modelo-rbac-v4-0-roles-jerarquicos-deprecado`
  — modelo v4.0 predecesor.
- :doc:`/gestion/evidencia/rbac-historia/analisis-comparativo-rbac-v4-vs-br-iact`
  — genealogia v4 -> v5.x.
- :doc:`/gestion/evidencia/rbac-historia/capacidades-vs-permisos-comparativo`
  — origen de D-RBAC-1.
- :doc:`/gestion/evidencia/rbac-historia/discrepancia-rbac-correccion-ene-2026`
  — deteccion de roles tradicionales en BR.
- :doc:`/gestion/evidencia/rbac-historia/decisiones-modulos-8-vs-9-historico`
  — debate "8 modulos".
- :doc:`/gestion/evidencia/rbac-historia/analisis-errores-modelo-rbac-v5-2-0`
  — Change Impact 87+ errores v5.2.0.
- :doc:`/gestion/evidencia/rbac-historia/gap-analysis-sistema-permisos-nov-2025`
  — Gap Analysis nov 2025.
- :doc:`/gestion/evidencia/rbac-historia/diseno-referencia-implementacion-permisos-legacy`
  — codigo Python legacy.

----

7. Spec vigente y normativa relacionada
=======================================

- :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact` (v5.2.1).
- :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.
- :doc:`/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod`.
- :doc:`/normativa/restricciones/cnst-031-permisos-temporales-maximo-6-meses`.
- :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`.
- :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`.
- :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`.
- ADR tecnico complementario: ``adr-back-006`` (estrategia de
  implementacion, supersede ADR-BACK-003) — ver
  :doc:`/backend/adr-back-006-rbac-estrategia-implementacion`.
