.. meta::
 :artefacto: AT_DM_PATTERN_SPECIFICATION
 :tipo: Diagrama Arquitectonico — Domain Model — Patron
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: CrossCutting
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _dm_pattern_specification:

================================
Patron Specification — Catalogo
================================

El patron **Specification** encapsula reglas de negocio que evaluan si
una entidad cumple con un criterio. En IACT se usa para validaciones
de elegibilidad, conflictos SoD, restricciones de borrado y otras
condiciones que no son responsabilidad directa de las entities ni
de los services.

Cada Specification tiene una unica operacion ``is_satisfied_by(entity)``
que retorna Boolean. Pueden combinarse con operadores logicos
(``AND``, ``OR``, ``NOT``) para construir specifications compuestos.

.. uml::
 :caption: Patron Specification — interfaz canonica + composicion.

 @startuml

 interface Specification<T> {
   + is_satisfied_by(entity : T) : Boolean
   + and(other : Specification<T>) : Specification<T>
   + or(other : Specification<T>) : Specification<T>
   + not() : Specification<T>
 }

 abstract class CompositeSpecification<T> {
   + is_satisfied_by(entity : T) : Boolean
 }

 class AndSpecification<T>
 class OrSpecification<T>
 class NotSpecification<T>

 Specification <|.. CompositeSpecification
 CompositeSpecification <|-- AndSpecification
 CompositeSpecification <|-- OrSpecification
 CompositeSpecification <|-- NotSpecification

 @enduml

Catalogo de implementaciones IACT
==================================

Las siguientes specifications viven en codigo (modulos backend) — este
documento las cataloga para trazabilidad. NO se crean archivos
``domain-model/<spec>.rst`` por cada una; se documentan agrupadas
aqui.

.. list-table::
 :widths: 30 25 45
 :header-rows: 1

 * - Specification
   - Aplica a
   - Proposito
 * - ``CriticalFunctionSpec``
   - Function
   - Identifica funciones criticas (require approval, audit reforzado)
 * - ``LastHolderSpec``
   - User
   - Detecta si User es el ultimo holder de una funcion critica
     (bloqueo de revoke)
 * - ``ActiveAssignmentSpec``
   - Assignment
   - Filtra Assignment con state=ACTIVE no expirados
 * - ``ExpiredExceptionalSpec``
   - ExceptionalPermission
   - Detecta ExceptionalPermission con expires_at < now
 * - ``SoDViolationSpec``
   - List<Function>
   - Evalua si un set de funciones viola alguna SeparationRule
     activa (CNST-005)
 * - ``ValidJWTSpec``
   - String (token)
   - Verifica token JWT firmado, no expirado, no blacklisted
 * - ``EligibleForExportSpec``
   - User + Resource
   - Verifica que el actor tiene la funcion view_audit_log /
     export_audit_log y el resource esta en su scope
 * - ``IdempotentRequestSpec``
   - Request
   - Detecta replay de POST con mismo request_id en ventana
 * - ``BoundedDateRangeSpec``
   - Period
   - Valida que date_range no excede maximo configurado
 * - ``StaleDatasetSpec``
   - Dataset
   - Detecta datasets con last_refresh > threshold

Trazabilidad a UCs
==================

Specifications consumidas por multiples UCs:

- ``SoDViolationSpec`` — UC_ACC_01, UC_ACC_04, UC_ACC_08, UC_ADM_01,
  UC_ADM_03 (toda escritura RBAC).
- ``ValidJWTSpec`` — UC_AUTH_01, UC_AUTH_05 (auth flows).
- ``LastHolderSpec`` — UC_ACC_02, UC_PERM_02 (revoke con safety).
- ``BoundedDateRangeSpec`` — UC_AUD_02, UC_LOG_03 (FTS bounded).
- ``IdempotentRequestSpec`` — UC_ACC_01, UC_ACC_08, UC_PERM_03.

Relaciones
==========

- :doc:`rule-validator` — orquestador que combina specifications.
- :doc:`function` — entity evaluada por CriticalFunctionSpec.
- :doc:`assignment` — entity evaluada por ActiveAssignmentSpec.
- :doc:`exceptional-permission` — evaluada por ExpiredExceptionalSpec.
- :doc:`separation-rule` — fuente de SoDViolationSpec.
