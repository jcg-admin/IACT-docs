.. meta::
 :artefacto: INDEX_AT_UC_DESIGNVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-uc-designview-index:

=============================
Design View — Vista de Diseno
=============================

Clases con detalle de diseno, secuencias, colaboracion. Como el sistema resuelve el UC tecnicamente.

Cubre los 80 UCs del sistema IACT en 12 modulos.

MOD_Auth — Autenticacion (5 UCs)
--------------------------------

.. toctree::
 :maxdepth: 1

 iniciar-sesion-secuencia

 iniciar-sesion-comunicacion
 cerrar-sesion-secuencia

 cerrar-sesion-comunicacion
 recuperar-contrasena-secuencia

 recuperar-contrasena-comunicacion
 cambiar-contrasena-secuencia

 cambiar-contrasena-comunicacion
 gestionar-sesiones-secuencia

 gestionar-sesiones-comunicacion


MOD_Users — Gestion Usuarios (4 UCs)
------------------------------------

.. toctree::
 :maxdepth: 1

 crear-usuario-secuencia

 crear-usuario-comunicacion
 consultar-usuarios-secuencia

 consultar-usuarios-comunicacion
 modificar-usuario-secuencia

 modificar-usuario-comunicacion
 eliminar-usuario-secuencia

 eliminar-usuario-comunicacion


MOD_Access — Control Acceso (7 UCs)
-----------------------------------

.. toctree::
 :maxdepth: 1

 asignar-funciones-secuencia

 asignar-funciones-comunicacion
 revocar-funciones-secuencia

 revocar-funciones-comunicacion
 consultar-permisos-efectivos-secuencia

 consultar-permisos-efectivos-comunicacion
 asignar-agrupador-secuencia

 asignar-agrupador-comunicacion
 gestionar-reglas-sod-secuencia

 gestionar-reglas-sod-comunicacion
 permiso-temporal-secuencia

 permiso-temporal-comunicacion
 auditar-cambios-acceso-secuencia

 auditar-cambios-acceso-comunicacion


MOD_Permissions — Gestion RBAC (10 UCs)
---------------------------------------

.. toctree::
 :maxdepth: 1

 asignar-grupo-usuario-secuencia

 asignar-grupo-usuario-comunicacion
 revocar-grupo-usuario-secuencia

 revocar-grupo-usuario-comunicacion
 conceder-permiso-excepcional-secuencia

 conceder-permiso-excepcional-comunicacion
 revocar-permiso-excepcional-secuencia

 revocar-permiso-excepcional-comunicacion
 crear-grupo-permisos-secuencia

 crear-grupo-permisos-comunicacion
 asignar-funciones-grupo-secuencia

 asignar-funciones-grupo-comunicacion
 verificar-permiso-usuario-secuencia

 verificar-permiso-usuario-comunicacion
 generar-menu-dinamico-secuencia

 generar-menu-dinamico-comunicacion
 auditar-acceso-secuencia

 auditar-acceso-comunicacion
 consultar-auditoria-permisos-secuencia

 consultar-auditoria-permisos-comunicacion


MOD_Reports — Reporteria (16 UCs)
---------------------------------

.. toctree::
 :maxdepth: 1

 resolver-segmento-secuencia

 resolver-segmento-comunicacion
 ver-dashboard-secuencia

 ver-dashboard-comunicacion
 ver-metricas-tiempo-real-secuencia

 ver-metricas-tiempo-real-comunicacion
 ver-reportes-historicos-secuencia

 ver-reportes-historicos-comunicacion
 exportar-reporte-secuencia

 exportar-reporte-comunicacion
 programar-reporte-secuencia

 programar-reporte-comunicacion
 ver-reportes-programados-secuencia

 ver-reportes-programados-comunicacion
 configurar-filtros-secuencia

 configurar-filtros-comunicacion
 guardar-vista-secuencia

 guardar-vista-comunicacion
 compartir-reporte-secuencia

 compartir-reporte-comunicacion
 reporte-agentes-secuencia

 reporte-agentes-comunicacion
 reporte-colas-secuencia

 reporte-colas-comunicacion
 reporte-campanas-secuencia

 reporte-campanas-comunicacion
 reporte-transferencias-secuencia

 reporte-transferencias-comunicacion
 reporte-menus-ivr-secuencia

 reporte-menus-ivr-comunicacion
 reporte-clientes-unicos-secuencia

 reporte-clientes-unicos-comunicacion


MOD_Alerts — Alertas (5 UCs)
----------------------------

.. toctree::
 :maxdepth: 1

 configurar-umbrales-alertas-secuencia

 configurar-umbrales-alertas-comunicacion
 ver-alertas-activas-secuencia

 ver-alertas-activas-comunicacion
 reconocer-alerta-secuencia

 reconocer-alerta-comunicacion
 ver-historial-alertas-secuencia

 ver-historial-alertas-comunicacion
 gestionar-suscripciones-secuencia

 gestionar-suscripciones-comunicacion


MOD_Pipeline — Supervision ETL (4 UCs)
--------------------------------------

.. toctree::
 :maxdepth: 1

 supervisar-etl-secuencia

 supervisar-etl-comunicacion
 consultar-errores-etl-secuencia

 consultar-errores-etl-comunicacion
 consultar-disponibilidad-datos-secuencia

 consultar-disponibilidad-datos-comunicacion
 solicitar-reintento-pipeline-secuencia

 solicitar-reintento-pipeline-comunicacion


MOD_Audit — Auditoria (4 UCs)
-----------------------------

.. toctree::
 :maxdepth: 1

 consultar-auditoria-general-secuencia

 consultar-auditoria-general-comunicacion
 buscar-auditoria-secuencia

 buscar-auditoria-comunicacion
 exportar-auditoria-secuencia

 exportar-auditoria-comunicacion
 generar-reporte-compliance-secuencia

 generar-reporte-compliance-comunicacion


MOD_Logs — Bitacoras (7 UCs)
----------------------------

.. toctree::
 :maxdepth: 1

 consultar-logs-sistema-secuencia

 consultar-logs-sistema-comunicacion
 consultar-logs-etl-secuencia

 consultar-logs-etl-comunicacion
 buscar-logs-secuencia

 buscar-logs-comunicacion
 exportar-logs-secuencia

 exportar-logs-comunicacion
 ver-logs-infraestructura-secuencia

 ver-logs-infraestructura-comunicacion
 ver-estado-sistema-secuencia

 ver-estado-sistema-comunicacion
 ver-metricas-tecnicas-secuencia

 ver-metricas-tecnicas-comunicacion


MOD_Operator — Operacion Agente (10 UCs)
----------------------------------------

.. toctree::
 :maxdepth: 1

 cambiar-estado-agente-secuencia

 cambiar-estado-agente-comunicacion
 atender-llamada-entrante-secuencia

 atender-llamada-entrante-comunicacion
 realizar-llamada-saliente-secuencia

 realizar-llamada-saliente-comunicacion
 hold-unhold-llamada-secuencia

 hold-unhold-llamada-comunicacion
 transferir-llamada-secuencia

 transferir-llamada-comunicacion
 ingresar-disposition-secuencia

 ingresar-disposition-comunicacion
 solicitar-break-pausa-secuencia

 solicitar-break-pausa-comunicacion
 ver-propio-dashboard-secuencia

 ver-propio-dashboard-comunicacion
 ver-historial-llamadas-propio-secuencia

 ver-historial-llamadas-propio-comunicacion
 recibir-notificacion-supervisor-secuencia

 recibir-notificacion-supervisor-comunicacion


MOD_Supervision — Supervision Tiempo Real (3 UCs)
-------------------------------------------------

.. toctree::
 :maxdepth: 1

 monitorear-llamada-secuencia

 monitorear-llamada-comunicacion
 barge-in-llamada-secuencia

 barge-in-llamada-comunicacion
 mensaje-broadcast-equipo-secuencia

 mensaje-broadcast-equipo-comunicacion


MOD_Caller — Llamante Externo (5 UCs)
-------------------------------------

.. toctree::
 :maxdepth: 1

 iniciar-llamada-call-center-secuencia

 iniciar-llamada-call-center-comunicacion
 navegar-ivr-secuencia

 navegar-ivr-comunicacion
 esperar-cola-secuencia

 esperar-cola-comunicacion
 solicitar-callback-secuencia

 solicitar-callback-comunicacion
 calificar-atencion-post-call-secuencia

 calificar-atencion-post-call-comunicacion

