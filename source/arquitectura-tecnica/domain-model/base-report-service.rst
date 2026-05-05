.. meta::
 :artefacto: AT_DM_CLASS_BASE_REPORT_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_base_report_service:

=================
BaseReportService
=================

**Clase abstracta** raíz de todos los servicios de reporte
del bounded context Reports. Define el contrato común y el
**template-method** ``apply_segment_filter`` que
materializa CNST-008 (filtrado por segmento) antes de
delegar la consulta a la subclase concreta.

.. uml::
 :caption: BaseReportService — clase abstracta con
           template-method y herencia generalizada de los
           6 servicios de reporte concretos.

 @startuml

 abstract class BaseReportService {
   # stat_repo : StatRepo
   # kpi_calculator : KPICalculator
   # segment_resolver : SegmentResolver
   --
   + {abstract} get(invoker : User, period : Period, \
                    filters : Filters) : Report
   # apply_segment_filter(filters : Filters, \
                          segment : Segment) : Filters
   # resolve_segment(invoker : User) : Segment
 }

 class AgentReportService
 class AbandonoReportService
 class ClientesReportService
 class MenuIvrReportService
 class TransferenciasReportService

 BaseReportService <|-- AgentReportService
 BaseReportService <|-- AbandonoReportService
 BaseReportService <|-- ClientesReportService
 BaseReportService <|-- MenuIvrReportService
 BaseReportService <|-- TransferenciasReportService

 note right of BaseReportService
   Clase abstracta — no instanciable.
   apply_segment_filter es template-method:
   las subclases NO lo redefinen, solo
   implementan get(...) usando el filtro
   ya saneado.
 end note

 @enduml

Atributos protegidos
====================

- ``stat_repo : StatRepo`` — repositorio de lectura
  específico por subclase (``AgentDailyStatRepo``,
  ``QueueDailyStatRepo``, ``CallerDailyStatRepo``, etc.).
  Inyectado vía constructor.
- ``kpi_calculator : KPICalculator`` — calculadora de KPIs
  derivados, **componente puro y compartido** (composición
  fuerte ``*--``).
- ``segment_resolver : SegmentResolver`` — resolución de
  segmento del invoker (CNST-008). Servicio externo
  (agregación ``o--``).

Operaciones
===========

- ``get(invoker, period, filters)`` — **abstracto**. Cada
  subclase implementa la consulta especializada.
- ``apply_segment_filter(filters, segment)`` —
  **template-method**: aplica el segmento a los filtros
  antes de pasarlos al repo. Idéntico en las 6 subclases.
- ``resolve_segment(invoker)`` — delega al
  ``SegmentResolver``. Helper protegido.

Patrón aplicado
===============

**Template Method** (Gamma et al., GoF):

1. La clase abstracta define el esqueleto del algoritmo
   (``apply_segment_filter`` → consulta).
2. Las subclases solo proveen ``get(...)`` con la consulta
   y agregación específicas.
3. El comportamiento de seguridad (CNST-008) está
   garantizado en la base, no en las hojas — **defensa en
   profundidad**.

Trazabilidad a UCs
==================

- Esta clase no tiene UC propio — es el contrato común.
- Subclases concretas (5):
  :doc:`agent-report-service`,
  :doc:`abandono-report-service`,
  :doc:`clientes-report-service`,
  :doc:`menu-ivr-report-service`,
  :doc:`transferencias-report-service`.

.. note::

   ``ScheduledReportListService`` NO hereda de
   ``BaseReportService`` — es un servicio CRUD de
   metadata de reportes programados, no un agregador
   de stats. Carece de ``stat_repo``,
   ``kpi_calculator`` y ``segment_resolver``. Ver D-13
   en el WP ``arq-tecnica-uml-rigor-pass``.

Restricciones aplicables
========================

- **CNST-008** — filtrado por segmento garantizado en la
  base (defensa en profundidad).
- **Liskov Substitution** — donde se espera
  ``BaseReportService`` cualquier subclase encaja.

Relaciones
==========

- **Generalización** (``<|--``): 6 subclases concretas
  heredan atributos protegidos y el template-method.
- **Composición** con ``KPICalculator`` (heredada).
- **Agregación** con ``StatRepo`` y ``SegmentResolver``
  (heredada).
