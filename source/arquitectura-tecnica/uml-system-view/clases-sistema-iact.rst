.. meta::
 :artefacto: AT_UML_SISTEMA_04_CLASES
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_clases:

=================================
Sistema IACT — Diagrama de Clases
=================================

4. Diagrama de Clases
======================

Los actores (grupos RBAC) acceden a los recursos del sistema
a traves de sus clases de servicio. ``SistemaIACT`` centraliza
la autenticacion y carga de funciones RBAC. ``ServicioReportes``
encapsula las llamadas ``cursor.callproc(sp_rpt_*)``. La
composicion entre ``SistemaIACT`` y ``AuditoriaAcceso`` garantiza
que toda accion quede registrada en ``audit_log``.

.. uml::
 :caption: Figura 5 — Diagrama de clases del Sistema IACT

 @startuml

 class SistemaIACT {
   +username: str
   +password: str
   +rbac_functions: list
   +receiveCredentials(): void
   +checkCredentials(): bool
   +loadRBACFunctions(): list
 }

 class SegmentResolver {
   +DID_MAP: dict
   +segments_for(user_id: int): list
 }

 class ServicioReportes {
   +trimestre: str
   +segmentos: list
   +callproc(sp_name, params): list
   +centros_transferencia(trimestre): list
   +llamadas_abandonadas(trimestre): list
   +menu_redirigidos(trimestre): list
   +clientes(trimestre): list
   +centros_xsegmento(trimestre): list
   +menu_centro(trimestre): list
   +cMENU_ERROR(trimestre): list
 }

 class ETLEjecucion {
   +tabla_origen: str
   +trimestre: str
   +estado: EstadoEnum
   +iniciado_en: datetime
   +finalizado_en: datetime
   +registros_base: int
   +disparar(): void
   +reintentar(): void
 }

 class DisparadorETL {
   +trimestre: str
   +ejecutado_por: str
   +receiveData(): void
   +sendToETL(): void
 }

 class ReporteLlamadasAbandonadas {
   +trimestre: str
   +segmento: str
   +total_abandonadas: int
   +tasa_abandono: float
   +receiveInput(): void
   +getReport(): void
 }

 class ReporteTransferencias {
   +trimestre: str
   +segmento: str
   +total_transferencias: int
   +receiveInput(): void
   +getReport(): void
 }

 class AuditoriaAcceso {
   +user_id: int
   +accion: str
   +timestamp: datetime
   +ip_origen: str
   +receiveData(): void
   +addToAuditLog(): void
 }

 class CancelEjecucionETL {
   +removeFromETLQueue(): void
 }

 class ReintentoETL {
   +editEjecucion(): void
 }

 enum EstadoEnum {
   en_ejecucion
   exitoso
   fallido
 }

 SistemaIACT --> SegmentResolver : usa
 SistemaIACT --> ServicioReportes : invoca
 SistemaIACT --> ETLEjecucion : gestiona
 DisparadorETL --> ETLEjecucion : crea
 ReporteLlamadasAbandonadas --> ServicioReportes
 ReporteTransferencias --> ServicioReportes
 AuditoriaAcceso *-- SistemaIACT
 ReintentoETL --> ETLEjecucion
 CancelEjecucionETL --> ETLEjecucion
 ETLEjecucion --> EstadoEnum

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
