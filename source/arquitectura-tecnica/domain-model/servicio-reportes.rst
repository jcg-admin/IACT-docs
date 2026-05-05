.. meta::
 :artefacto: AT_DM_CLASS_SERVICIO_REPORTES
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_servicio_reportes:

================
ServicioReportes
================

Servicio de acceso a datos operativos del sistema de llamadas para reporteria.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase ServicioReportes — stub pendiente de desarrollo.

 @startuml

 class ServicioReportes {
  + llamadas_abandonadas(trimestre) : list[dict]
  + menu_redirigidos(trimestre) : list[dict]
  + clientes(trimestre) : list[dict]
  + centros_transferencia(trimestre) : list[dict]
 }

 @enduml
