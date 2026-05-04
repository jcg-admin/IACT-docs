.. meta::
 :artefacto: INDEX_AT_UC_USECASEVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-uc-usecaseview-index:

=====================================
Use Case View — Vista de Casos de Uso
=====================================

Diagrama UC con actores RBAC, includes y extends. Une todas las demas vistas.

Cubre los 80 UCs del sistema IACT en 12 modulos.

MOD_Auth — Autenticacion (5 UCs)
--------------------------------

.. toctree::
 :maxdepth: 1

 iniciar-sesion
 cerrar-sesion
 recuperar-contrasena
 cambiar-contrasena
 gestionar-sesiones


MOD_Users — Gestion Usuarios (4 UCs)
------------------------------------

.. toctree::
 :maxdepth: 1

 crear-usuario
 consultar-usuarios
 modificar-usuario
 eliminar-usuario


MOD_Access — Control Acceso (7 UCs)
-----------------------------------

.. toctree::
 :maxdepth: 1

 asignar-funciones
 revocar-funciones
 consultar-permisos-efectivos
 asignar-agrupador
 gestionar-reglas-sod
 permiso-temporal
 auditar-cambios-acceso


MOD_Permissions — Gestion RBAC (10 UCs)
---------------------------------------

.. toctree::
 :maxdepth: 1

 asignar-grupo-usuario
 revocar-grupo-usuario
 conceder-permiso-excepcional
 revocar-permiso-excepcional
 crear-grupo-permisos
 asignar-funciones-grupo
 verificar-permiso-usuario
 generar-menu-dinamico
 auditar-acceso
 consultar-auditoria-permisos


MOD_Reports — Reporteria (16 UCs)
---------------------------------

.. toctree::
 :maxdepth: 1

 resolver-segmento
 ver-dashboard
 ver-metricas-tiempo-real
 ver-reportes-historicos
 exportar-reporte
 programar-reporte
 ver-reportes-programados
 configurar-filtros
 guardar-vista
 compartir-reporte
 reporte-agentes
 reporte-colas
 reporte-campanas
 reporte-transferencias
 reporte-menus-ivr
 reporte-clientes-unicos


MOD_Alerts — Alertas (5 UCs)
----------------------------

.. toctree::
 :maxdepth: 1

 configurar-umbrales-alertas
 ver-alertas-activas
 reconocer-alerta
 ver-historial-alertas
 gestionar-suscripciones


MOD_Pipeline — Supervision ETL (4 UCs)
--------------------------------------

.. toctree::
 :maxdepth: 1

 supervisar-etl
 consultar-errores-etl
 consultar-disponibilidad-datos
 solicitar-reintento-pipeline


MOD_Audit — Auditoria (4 UCs)
-----------------------------

.. toctree::
 :maxdepth: 1

 consultar-auditoria-general
 buscar-auditoria
 exportar-auditoria
 generar-reporte-compliance


MOD_Logs — Bitacoras (7 UCs)
----------------------------

.. toctree::
 :maxdepth: 1

 consultar-logs-sistema
 consultar-logs-etl
 buscar-logs
 exportar-logs
 ver-logs-infraestructura
 ver-estado-sistema
 ver-metricas-tecnicas


MOD_Operator — Operacion Agente (10 UCs)
----------------------------------------

.. toctree::
 :maxdepth: 1

 cambiar-estado-agente
 atender-llamada-entrante
 realizar-llamada-saliente
 hold-unhold-llamada
 transferir-llamada
 ingresar-disposition
 solicitar-break-pausa
 ver-propio-dashboard
 ver-historial-llamadas-propio
 recibir-notificacion-supervisor


MOD_Supervision — Supervision Tiempo Real (3 UCs)
-------------------------------------------------

.. toctree::
 :maxdepth: 1

 monitorear-llamada
 barge-in-llamada
 mensaje-broadcast-equipo


MOD_Caller — Llamante Externo (5 UCs)
-------------------------------------

.. toctree::
 :maxdepth: 1

 iniciar-llamada-call-center
 navegar-ivr
 esperar-cola
 solicitar-callback
 calificar-atencion-post-call

