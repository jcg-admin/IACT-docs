.. meta::
 :artefacto: AT_PROC_DASHBOARD_CONCURRENCIA
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_proc_dashboard_concurrencia:

=======================================================
Process View — Concurrencia de Dashboard en Tiempo Real
=======================================================

Patron de concurrencia para el dashboard de supervision en tiempo real:
pool de conexiones, consultas paralelas por metrica, cache de resultados
y timeouts de seguridad.

.. uml::
 :caption: Process View — concurrencia dashboard: pool, cache, consultas paralelas y timeout.

 @startuml

 actor AGR_SUPERVISOR

 participant InterfazSupervision <<frontend>>
 participant ServicioSupervision <<api>>
 participant PoolConexiones      <<connection-pool>>
 participant CacheDashboard      <<redis>>
 database    BDOperativa         <<mariadb, readonly>>
 database    AlmacenDatos        <<postgresql>>

 AGR_SUPERVISOR -> InterfazSupervision : GET /supervision/dashboard
 activate InterfazSupervision

 InterfazSupervision -> ServicioSupervision : obtenerDashboard(supervisor_id)
 activate ServicioSupervision

 ServicioSupervision -> CacheDashboard : GET dashboard:{supervisor_id}
 CacheDashboard --> ServicioSupervision : cache miss

 ServicioSupervision -> PoolConexiones : adquirir conexion (timeout:5s)
 activate PoolConexiones

 par consultas paralelas
   PoolConexiones -> BDOperativa : SELECT llamadas activas\n<<CNST-007: readonly>>
   BDOperativa --> PoolConexiones : List<Call>
 also
   PoolConexiones -> AlmacenDatos : SELECT metricas_agentes\n(ultimos 15 min)
   AlmacenDatos --> PoolConexiones : List<Metric>
 also
   PoolConexiones -> AlmacenDatos : SELECT alertas activas
   AlmacenDatos --> PoolConexiones : List<Alert>
 end

 PoolConexiones --> ServicioSupervision : datos consolidados
 deactivate PoolConexiones

 ServicioSupervision -> CacheDashboard : SET dashboard:{supervisor_id}\nTTL=30s
 CacheDashboard --> ServicioSupervision : OK

 ServicioSupervision --> InterfazSupervision : dashboard data
 deactivate ServicioSupervision

 InterfazSupervision --> AGR_SUPERVISOR : dashboard en tiempo real
 deactivate InterfazSupervision

 note over PoolConexiones
   timeout: 5s por conexion.
   Si timeout expira: 503 Service Unavailable.
   CacheDashboard TTL=30s para reducir carga.
   CNST-007: BDOperativa solo lectura.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/call`
 :doc:`/arquitectura-tecnica/domain-model/metric`
 :doc:`/arquitectura-tecnica/domain-model/alert`
 :doc:`/arquitectura-tecnica/deploy-view/standard-topology`
