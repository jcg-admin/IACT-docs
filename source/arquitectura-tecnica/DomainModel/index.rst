.. meta::
 :artefacto: INDEX_AT_UC_DOMAINMODEL
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-uc-domainmodel-index:

===========================
Domain Model — Vista Logica
===========================

Entidades del dominio y relaciones por UC. Diagrama de clases (conceptual) + estados.

Cubre los 80 UCs del sistema IACT en 12 modulos.

MOD_Auth — Autenticacion (5 UCs)
--------------------------------

.. toctree::
 :maxdepth: 1

 iniciar-sesion-domain-model

 iniciar-sesion-estado
 cerrar-sesion-domain-model

 cerrar-sesion-estado
 recuperar-contrasena-domain-model

 recuperar-contrasena-estado
 cambiar-contrasena-domain-model

 cambiar-contrasena-estado
 gestionar-sesiones-domain-model

 gestionar-sesiones-estado


MOD_Users — Gestion Usuarios (4 UCs)
------------------------------------

.. toctree::
 :maxdepth: 1

 crear-usuario-domain-model

 crear-usuario-estado
 consultar-usuarios-domain-model

 consultar-usuarios-estado
 modificar-usuario-domain-model

 modificar-usuario-estado
 eliminar-usuario-domain-model

 eliminar-usuario-estado


MOD_Access — Control Acceso (7 UCs)
-----------------------------------

.. toctree::
 :maxdepth: 1

 asignar-funciones-domain-model

 asignar-funciones-estado
 revocar-funciones-domain-model

 revocar-funciones-estado
 consultar-permisos-efectivos-domain-model

 consultar-permisos-efectivos-estado
 asignar-agrupador-domain-model

 asignar-agrupador-estado
 gestionar-reglas-sod-domain-model

 gestionar-reglas-sod-estado
 permiso-temporal-domain-model

 permiso-temporal-estado
 auditar-cambios-acceso-domain-model

 auditar-cambios-acceso-estado


MOD_Permissions — Gestion RBAC (10 UCs)
---------------------------------------

.. toctree::
 :maxdepth: 1

 asignar-grupo-usuario-domain-model

 asignar-grupo-usuario-estado
 revocar-grupo-usuario-domain-model

 revocar-grupo-usuario-estado
 conceder-permiso-excepcional-domain-model

 conceder-permiso-excepcional-estado
 revocar-permiso-excepcional-domain-model

 revocar-permiso-excepcional-estado
 crear-grupo-permisos-domain-model

 crear-grupo-permisos-estado
 asignar-funciones-grupo-domain-model

 asignar-funciones-grupo-estado
 verificar-permiso-usuario-domain-model

 verificar-permiso-usuario-estado
 generar-menu-dinamico-domain-model

 generar-menu-dinamico-estado
 auditar-acceso-domain-model

 auditar-acceso-estado
 consultar-auditoria-permisos-domain-model

 consultar-auditoria-permisos-estado


MOD_Reports — Reporteria (16 UCs)
---------------------------------

.. toctree::
 :maxdepth: 1

 resolver-segmento-domain-model

 resolver-segmento-estado
 ver-dashboard-domain-model

 ver-dashboard-estado
 ver-metricas-tiempo-real-domain-model

 ver-metricas-tiempo-real-estado
 ver-reportes-historicos-domain-model

 ver-reportes-historicos-estado
 exportar-reporte-domain-model

 exportar-reporte-estado
 programar-reporte-domain-model

 programar-reporte-estado
 ver-reportes-programados-domain-model

 ver-reportes-programados-estado
 configurar-filtros-domain-model

 configurar-filtros-estado
 guardar-vista-domain-model

 guardar-vista-estado
 compartir-reporte-domain-model

 compartir-reporte-estado
 reporte-agentes-domain-model

 reporte-agentes-estado
 reporte-colas-domain-model

 reporte-colas-estado
 reporte-campanas-domain-model

 reporte-campanas-estado
 reporte-transferencias-domain-model

 reporte-transferencias-estado
 reporte-menus-ivr-domain-model

 reporte-menus-ivr-estado
 reporte-clientes-unicos-domain-model

 reporte-clientes-unicos-estado


MOD_Alerts — Alertas (5 UCs)
----------------------------

.. toctree::
 :maxdepth: 1

 configurar-umbrales-alertas-domain-model

 configurar-umbrales-alertas-estado
 ver-alertas-activas-domain-model

 ver-alertas-activas-estado
 reconocer-alerta-domain-model

 reconocer-alerta-estado
 ver-historial-alertas-domain-model

 ver-historial-alertas-estado
 gestionar-suscripciones-domain-model

 gestionar-suscripciones-estado


MOD_Pipeline — Supervision ETL (4 UCs)
--------------------------------------

.. toctree::
 :maxdepth: 1

 supervisar-etl-domain-model

 supervisar-etl-estado
 consultar-errores-etl-domain-model

 consultar-errores-etl-estado
 consultar-disponibilidad-datos-domain-model

 consultar-disponibilidad-datos-estado
 solicitar-reintento-pipeline-domain-model

 solicitar-reintento-pipeline-estado


MOD_Audit — Auditoria (4 UCs)
-----------------------------

.. toctree::
 :maxdepth: 1

 consultar-auditoria-general-domain-model

 consultar-auditoria-general-estado
 buscar-auditoria-domain-model

 buscar-auditoria-estado
 exportar-auditoria-domain-model

 exportar-auditoria-estado
 generar-reporte-compliance-domain-model

 generar-reporte-compliance-estado


MOD_Logs — Bitacoras (7 UCs)
----------------------------

.. toctree::
 :maxdepth: 1

 consultar-logs-sistema-domain-model

 consultar-logs-sistema-estado
 consultar-logs-etl-domain-model

 consultar-logs-etl-estado
 buscar-logs-domain-model

 buscar-logs-estado
 exportar-logs-domain-model

 exportar-logs-estado
 ver-logs-infraestructura-domain-model

 ver-logs-infraestructura-estado
 ver-estado-sistema-domain-model

 ver-estado-sistema-estado
 ver-metricas-tecnicas-domain-model

 ver-metricas-tecnicas-estado


MOD_Operator — Operacion Agente (10 UCs)
----------------------------------------

.. toctree::
 :maxdepth: 1

 cambiar-estado-agente-domain-model

 cambiar-estado-agente-estado
 atender-llamada-entrante-domain-model

 atender-llamada-entrante-estado
 realizar-llamada-saliente-domain-model

 realizar-llamada-saliente-estado
 hold-unhold-llamada-domain-model

 hold-unhold-llamada-estado
 transferir-llamada-domain-model

 transferir-llamada-estado
 ingresar-disposition-domain-model

 ingresar-disposition-estado
 solicitar-break-pausa-domain-model

 solicitar-break-pausa-estado
 ver-propio-dashboard-domain-model

 ver-propio-dashboard-estado
 ver-historial-llamadas-propio-domain-model

 ver-historial-llamadas-propio-estado
 recibir-notificacion-supervisor-domain-model

 recibir-notificacion-supervisor-estado


MOD_Supervision — Supervision Tiempo Real (3 UCs)
-------------------------------------------------

.. toctree::
 :maxdepth: 1

 monitorear-llamada-domain-model

 monitorear-llamada-estado
 barge-in-llamada-domain-model

 barge-in-llamada-estado
 mensaje-broadcast-equipo-domain-model

 mensaje-broadcast-equipo-estado


MOD_Caller — Llamante Externo (5 UCs)
-------------------------------------

.. toctree::
 :maxdepth: 1

 iniciar-llamada-call-center-domain-model

 iniciar-llamada-call-center-estado
 navegar-ivr-domain-model

 navegar-ivr-estado
 esperar-cola-domain-model

 esperar-cola-estado
 solicitar-callback-domain-model

 solicitar-callback-estado
 calificar-atencion-post-call-domain-model

 calificar-atencion-post-call-estado

