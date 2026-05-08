.. meta::
 :artefacto: AT_UML_SISTEMA_04_CLASES
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_clases:

=================================
Sistema IACT — Diagrama de Clases
=================================

4. Diagrama de Clases
======================

Las funciones RBAC (per P-15) acceden a los recursos del sistema
a traves de sus clases de servicio canonicas del domain-model.
``AuthorizationGuard`` centraliza la autenticacion y verificacion
de permisos. Los report services especializados (``Abandonment
ReportService``, ``TransferReportService``, etc.) encapsulan las
consultas pre-agregadas. ``AuditService`` garantiza que toda
escritura quede registrada como ``AuditEvent``.

.. note::

 v2.0.0 (2026-05-06): vocabulario alineado al domain-model
 canonico per STD-008 (identifiers en ingles) y al audit Brown
 1998. Reemplaza nombres en espanol (DisparadorETL,
 ReporteLlamadasAbandonadas, etc.) por sus equivalentes
 canonicos del domain-model.

.. uml::
 :caption: Figura 5 — Diagrama de clases del Sistema IACT.

 @startuml

 class AuthorizationGuard <<sistema>> {
   +verify(user_id, function): bool
   +loadEffectiveSet(user_id): list
 }

 class SegmentResolver <<sistema>> {
   +DID_MAP: dict
   +segments_for(user_id): list
 }

 class BaseReportService <<sistema>> {
   +period: str
   +segments: list
   +generate(): Report
 }

 class PipelineExecution {
   +source_table: str
   +period: str
   +state: PipelineState
   +started_at: datetime
   +finished_at: datetime
   +base_records: int
   +start(): void
   +retry(): void
   +cancel(): void
 }

 class AbandonmentReportService <<sistema>> {
   +by_segment(period): AbandonmentReport
 }

 class TransferReportService <<sistema>> {
   +by_segment(period): TransferReport
 }

 class AuditService <<sistema>> {
   +emit(event: AuditEvent): void
 }

 class AuditEvent {
   +event_id: UUID
   +user_id: int
   +action: str
   +timestamp: datetime
   +ip_origin: str
 }

 enum PipelineState {
   SCHEDULED
   RUNNING
   COMPLETED
   FAILED
   CANCELLED
 }

 BaseReportService <|-- AbandonmentReportService
 BaseReportService <|-- TransferReportService

 AuthorizationGuard ..> SegmentResolver : usa
 AuthorizationGuard ..> BaseReportService : verify pre-call
 AbandonmentReportService ..> PipelineExecution : lee metricas
 TransferReportService ..> PipelineExecution : lee metricas
 AuditService ..> AuditEvent : crea
 PipelineExecution ..> AuditService : on transition
 PipelineExecution --> PipelineState

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/abandonment-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/transfer-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/domain-model/audit-event`
 - :doc:`/arquitectura-tecnica/design-view/pipeline/state`
