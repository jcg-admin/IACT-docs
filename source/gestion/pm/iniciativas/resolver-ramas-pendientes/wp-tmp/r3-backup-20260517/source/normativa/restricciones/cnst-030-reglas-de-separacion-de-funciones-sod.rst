.. meta::
 :artefacto: CNST_030
 :tipo: Restriccion
 :dominio: normativa
 :subdominio: restricciones
 :estado: Vigente
 :version: 3.0.0
 :fecha_creacion: 2025-12-17
 :ultimo_cambio: 2026-05-13
 :autor: NestorMonroy
 :clasificacion: Critico

.. _cnst-030:

===============================================
CNST-030: Reglas de Separacion de Funciones SoD
===============================================

Resumen Ejecutivo
-----------------

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **ID**
   - CNST_030
 * - **Categoria**
   - RBAC
 * - **Tipo (TXM_01)**
   - Tecnica
 * - **Criticidad**
   - Critico
 * - **Negociable**
   - No
 * - **Estado**
   - Vigente

1. Definicion
-------------

1.1 Enunciado
^^^^^^^^^^^^^


Las reglas de SoD (Separation of Duties) DEBEN declararse atomicamente
y enforzarse en tiempo de asignacion. La asignacion de un grupo que
crea conflicto SoD con otro grupo del usuario DEBE rechazarse con
error explicito.

1.2 Justificacion
^^^^^^^^^^^^^^^^^


SoD previene fraude y errores por concentracion de poder. Las reglas
SoD textuales (no atomicas) son ineficaces porque dependen del
revisor humano.

1.3 Origen
^^^^^^^^^^

- **Fuente:** Compliance + prevencion de fraude
- **Documento:** MODELO_RBAC_IACT:524-603
- **Fecha:** 2025-01-01

2. Especificacion Tecnica
-------------------------

2.1 Descripcion Detallada
^^^^^^^^^^^^^^^^^^^^^^^^^


- Modelo ``SeparationRule`` con campos ``functions_set_a``, ``functions_set_b``,
  ``description``, ``state`` (ENABLED/DISABLED). ``db_table = 'access_separation_rule'``.
- Validacion en ``DutySeparationValidator.validate(user, new_function_codes)``
  invocado desde ``FunctionAssignView`` y ``AGRAssignView`` (capa API).
  Ver nota de implementacion en §5.1.
- Reporte periodico de violaciones existentes (sanity check).

**Catalogo de las 3 reglas SoD vigentes (modelo v5.4.0):**

.. list-table::
 :widths: 15 30 25 20 10
 :header-rows: 1

 * - ID
   - Nombre (ingles)
   - Grupo A
   - Grupo B
   - CNST
 * - SOD-001
   - pipeline_audit_separation
   - Pipeline (PIP-001..004): view_pipeline_status,
     view_pipeline_errors, view_data_availability,
     request_pipeline_retry
   - Audit (AUD-001..004): view_audit_log, search_audit_log,
     export_audit_log, generate_compliance_report
   - CNST_030
 * - SOD-002
   - user_audit_separation
   - Gestion Users criticas (4 funciones): create_users,
     delete_users, list_users, unblock_users
   - Audit parcial (3 funciones): view_audit_log,
     search_audit_log, export_audit_log
   - CNST_030
 * - SOD-003
   - access_audit_separation
   - Gestion Acceso (3 funciones): assign_functions,
     revoke_functions, manage_separation_rules
   - Audit (2 funciones): view_audit_log, search_audit_log
   - CNST_030

**Razon de cada regla:**

- **SOD-001:** quien opera el ETL no debe auditarlo (independencia
  operador/auditor).
- **SOD-002:** quien gestiona usuarios no debe auditar sus propias
  acciones de gestion.
- **SOD-003:** quien gestiona acceso no debe auditar cambios de
  permisos que el mismo aplico.

**Aplicabilidad a custom groups (decision D-RBAC-7):**

Las 3 reglas SoD aplican TANTO a system groups (AGR-001..010) como a
**custom groups** creados via UC_PERM_05. La validacion runtime
verifica las funciones contenidas en cualquier grupo, sin distincion
de origen (predefinido o creable). Esto previene que admin tech
cree un custom group que combine funciones prohibidas por SoD.

2.2 Parametros
^^^^^^^^^^^^^^

Ver subseccion 2.1.

2.3 Tecnologias Involucradas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Modelo ``SeparationRule`` (``apps.access.models``)
- ``DutySeparationValidator`` (``apps.access.function_assign_view``)
- Reporte periodico de violaciones

3. Impacto en Sistema
---------------------

3.1 Modulos Afectados
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Modulo
   - Impacto
 * - MOD_Access
   - Implementa ``SeparationRule`` + ``DutySeparationValidator``

3.2 Casos de Uso Afectados
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - UC
   - Impacto
 * - UC_004
   - Asignar Rol — valida SoD
 * - UC_005
   - Auditoria de violaciones SoD

3.3 Lo que NO se puede hacer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Asignar grupos en conflicto SoD a un mismo usuario
- Hacer permisos temporales que violen SoD
- Bypassear la validacion en codigo

4. Business Rules Derivadas
---------------------------

Sin BRs especificas mapeadas a esta CNST en la base cognitiva actual.
El catalogo BR_NNN del dominio IACT esta pendiente de elaborar en
el WP de requisitos (deuda diferida).

5. Implementacion
-----------------

5.1 Codigo de Referencia
^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: python

 # apps/access/function_assign_view.py
 # BR-007: validar SoD antes de asignar funciones (UC_ACC_01 CA-05/06)

 class DutySeparationValidator:
     @staticmethod
     def validate(user, new_function_codes: list[str]) -> list[dict]:
         """
         Evalua SoD contra el conjunto efectivo de funciones:
         actuales del usuario + nuevas a asignar.

         Retorna lista de violaciones [{rule_id, rule_code, conflict_pair}].
         Lista vacia = sin violaciones, asignacion puede proceder.
         """
         from apps.access.models import SeparationRule, UserFunctionAssignment
         violations = []
         current_codes = set(
             UserFunctionAssignment.objects.filter(user=user, state='ACTIVE')
             .values_list('function__code', flat=True)
         )
         all_codes = current_codes | set(new_function_codes)

         for rule in SeparationRule.objects.filter(state='ENABLED'):
             codes_set_a    = set(rule.functions_set_a.values_list('code', flat=True))
             codes_set_b    = set(rule.functions_set_b.values_list('code', flat=True))
             user_has_set_a = bool(all_codes & codes_set_a)
             user_has_set_b = bool(all_codes & codes_set_b)
             if user_has_set_a and user_has_set_b:
                 violations.append({
                     'rule_id':       rule.pk,
                     'rule_code':     rule.code,
                     'conflict_pair': [list(codes_set_a), list(codes_set_b)],
                 })
         return violations

 # Invocacion en FunctionAssignView (UC_ACC_01) y AGRAssignView (UC_ACC_04):
 violations = DutySeparationValidator.validate(target_user, new_function_codes)
 if violations:
     return Response({'sod_violations': violations}, status=400)

.. note::

 **Nivel de enforcement — capa API (no DB).**

 La validacion se realiza en la capa DRF, no mediante un signal Django.
 Esto significa que los endpoints canonicos ``POST /api/access/users/{id}/functions/assign/``
 y ``POST /api/access/users/{id}/agr/`` enforzan SoD en toda asignacion
 que pase por el API. Las escrituras directas a la base de datos (p.ej.
 via Django admin o scripts de migracion) no estan cubiertas por este
 mecanismo. Los scripts de seed de datos (``create_separation_rules``,
 ``create_access_groups``) son responsables de respetar SoD
 al definir los conjuntos de funciones de cada regla.

5.2 Validacion de Cumplimiento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ver seccion 5.1 (codigo de referencia es la validacion ejecutable).


6. Excepciones
--------------

6.1 Excepciones Permitidas
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Excepciones SoD requieren ADR + aprobacion explicita del Compliance Officer

6.2 Proceso de Excepcion
^^^^^^^^^^^^^^^^^^^^^^^^

Solicitud formal con justificacion de negocio + analisis de riesgo + aprobacion Compliance Officer + vigencia acotada.

El protocolo formal de waiver de CNSTs esta pendiente de elaborar en
el WP de gobernanza (`PROC_Excepciones_CNST` — ver
(referencia interna) § W-4).

7. Verificacion
---------------

7.1 Criterios de Cumplimiento
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El cumplimiento se verifica via los snippets de la seccion 5.

7.2 Metodo de Verificacion
^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Tipo:** Automatico
- **Frecuencia:** Continuo + reporte semanal
- **Herramienta:** Tests de integracion en ``test_separation_rule_validate.py``
  (endpoint ``POST /api/access/separation-rules/validate``) + reporte SQL
  de violaciones existentes

8. Trazabilidad
---------------

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **CNSTs relacionadas**
   - :doc:`cnst-029-rbac-modelo-plano`, :doc:`cnst-031-permisos-temporales-maximo-6-meses`
 * - **BR derivadas**
   - Pendiente WP requisitos
 * - **UCs afectados**
   - UC_004, UC_005
 * - **MODs afectados**
   - MOD_Access
 * - **ADRs relacionados**
   - Pendiente WP arquitectura tecnica

9. Historial de Cambios
-----------------------

.. list-table::
 :widths: 12 15 25 48
 :header-rows: 1

 * - Version
   - Fecha
   - Autor
   - Cambios
 * - 1.0.0
   - 2025-12-17
   - NestorMonroy
   - Version inicial (consolidada del backup canonico)
 * - 2.0.0
   - 2026-04-28
   - NestorMonroy
   - Descomposicion SRP (un concern por archivo) + enriquecimiento estructura completa TPL_CNST (9 secciones)
 * - 3.0.0
   - 2026-05-13
   - NestorMonroy
   - Alineacion con implementacion real v5.4.0 (FASE 5 DT-STD008-001).
     SoDRule → SeparationRule. group_a/group_b/rationale → functions_set_a/b/description.
     UserGroup → UserAccessGroup (eliminado — enforcement no es via signal).
     Signal pre_save eliminado — mecanismo real es DutySeparationValidator
     invocado desde FunctionAssignView y AGRAssignView (capa API).
     Nota arquitectonica añadida en §5.1 sobre nivel de enforcement (API, no DB).
     Catalogo SoD: modelo v5.2.1 → v5.4.0.
     SOD-003 Grupo A: manage_sod → manage_separation_rules.

