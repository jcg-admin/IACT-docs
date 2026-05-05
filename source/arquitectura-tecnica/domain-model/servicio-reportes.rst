.. meta::
 :artefacto: AT_DM_CLASS_SERVICIO_REPORTES
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

.. _dm_class_servicio_reportes:

================
ServicioReportes
================

**Facade legada** que expone los cuatro reportes operativos
(abandono, menú IVR, clientes, transferencias) bajo una
interfaz unificada. Es un agregador de los servicios
especializados — no contiene lógica de negocio propia.

.. note::

   El nombre en castellano (``ServicioReportes``) se mantiene
   por compatibilidad con la API legada del sistema. Los
   nuevos servicios usan inglés (STD-008). Esta facade
   delega a los ``XxxReportService`` modernos y se considera
   *deprecated* para clientes nuevos — usar los servicios
   especializados directamente.

.. uml::
 :caption: ServicioReportes — facade que agrega los cuatro
           reportes operativos del IVR.

 @startuml

 class ServicioReportes {
   - abandono_service : AbandonoReportService
   - menu_ivr_service : MenuIvrReportService
   - clientes_service : ClientesReportService
   - transferencias_service : TransferenciasReportService
   --
   + llamadas_abandonadas(invoker : User, period : Period) : AbandonReport
   + menu_redirigidos(invoker : User, period : Period) : MenuIvrReport
   + clientes(invoker : User, period : Period) : ClientesReport
   + centros_transferencia(invoker : User, period : Period) : TransferenciasReport
 }

 class AbandonoReportService
 class MenuIvrReportService
 class ClientesReportService
 class TransferenciasReportService

 ServicioReportes "1" o-- "1" AbandonoReportService : delegates
 ServicioReportes "1" o-- "1" MenuIvrReportService : delegates
 ServicioReportes "1" o-- "1" ClientesReportService : delegates
 ServicioReportes "1" o-- "1" TransferenciasReportService : delegates

 note right of ServicioReportes
   Facade legada (deprecated para
   clientes nuevos). Agrega y delega
   a los XxxReportService modernos.
   Nombre en castellano por API legacy.
 end note

 @enduml

Trazabilidad a UCs
==================

Cubre cuatro reportes operativos del cluster ``uc-rpt-*`` vía
delegación a los servicios especializados.

Relaciones
==========

- Agregación con los cuatro ``XxxReportService`` modernos.
- No tiene composición ni dependencias propias — es un
  facade puro.

Decisión de naming
==================

El nombre y métodos en castellano son una **excepción
documentada** a STD-008 (English identifiers). Se mantiene
por compatibilidad de API. Los servicios delegados usan
inglés en sus identificadores internos. Ver decisión D-XX
en el WP ``2026-05-05-06-41-02-arq-tecnica-uml-deepening``.
