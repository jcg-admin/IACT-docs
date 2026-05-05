.. meta::
 :artefacto: AT_DM_CLASS_MENU_IVR_REPORT_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_menu_ivr_report_service:

====================
MenuIvrReportService
====================

Servicio de reporte de **navegación del IVR**: cuenta
selecciones por opción de menú, tasa de fall-through (no
selección), profundidad media de navegación y opciones más
abandonadas.

Útil para detectar opciones mal diseñadas u oscurecidas en
el árbol IVR. Aplica filtros de segmento (CNST-008).

.. uml::
 :caption: Clase MenuIvrReportService — reporte de
           navegación del IVR.

 @startuml

 abstract class BaseReportService

 class MenuIvrReportService {
   --
   + get(invoker : User, period : Period, \
         filters : MenuFilters) : MenuIvrReport
   + by_option(invoker : User, period : Period) : List<MenuOptionStats>
   + drop_off_curve(invoker : User, period : Period) : DropOffCurve
 }

 BaseReportService <|-- MenuIvrReportService

 class MenuIvrReport {
   + period : Period
   + total_entries : Integer
   + total_completions : Integer
   + fall_through_rate : Double
   + average_depth : Double
   + by_option : Map<MenuOptionId, Integer>
 }

 class MenuOptionStats {
   + option_id : UUID
   + option_label : String
   + selections : Integer
   + drop_off_rate : Double
 }

 class DropOffCurve {
   + buckets : List<Bucket>
 }

 class MenuDailyStatRepo

 MenuIvrReportService "1" o-- "1" MenuDailyStatRepo : reads
 MenuIvrReportService "1" ..> "1" MenuIvrReport : <<returns>>
 MenuIvrReportService "1" ..> "0..*" MenuOptionStats : <<returns>>
 MenuIvrReportService "1" ..> "0..1" DropOffCurve : <<returns>>

 note bottom of MenuIvrReport
   by_option : {ordered}
 end note

 note right of MenuIvrReportService
   Hereda apply_segment_filter de
   BaseReportService. drop_off_curve
   agrupa por nivel del árbol IVR.
 end note

 @enduml

Trazabilidad a UCs
==================

Reporte derivado del cluster ``uc-rpt-*``. Insumo para
optimización del árbol IVR.

Relaciones
==========

- Agregación con ``MenuDailyStatRepo`` y
  ``SegmentResolver``.
- Composición con ``KPICalculator``.
- Devuelve DTOs especializados.
