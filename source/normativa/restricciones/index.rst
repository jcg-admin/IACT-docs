.. _restricciones-index:

Restricciones Tecnicas
======================

:Estado: VIGENTE (Actualizado)
:Documentos: 10
:Lineas Totales: 10,071
:Ultima Actualizacion: 2026-01-03
:Version: 1.1.0
:Integracion RBAC: v5.1.1 (44 funciones atomicas)

----

Proposito
---------

Este directorio contiene las restricciones tecnicas criticas del Sistema IACT - IVR Analytics & Customer Tracking. Estas restricciones son NO NEGOCIABLES y deben cumplirse en todas las fases del proyecto.

Las restricciones estan alineadas con el Modelo RBAC v5.1.1 que utiliza funciones atomicas en lugar de roles tradicionales.

----

Cambios en v1.1.0
-----------------

Fecha: 2026-01-03

**Actualizaciones Globales (10 CNST):**

- Todos los CNST actualizados a v1.1.0
- Fecha actualizada: 2025-12-17 → 2026-01-03
- Estado cambiado: CONGELADO → VIGENTE
- Referencias actualizadas: RBAC v4.0 → RBAC v5.1.1
- Integracion con modelo de funciones atomicas (44 funciones)

**Ampliaciones de Contenido:**

- CNST-005: Nueva seccion "Permisos Temporales" (+150 lineas)
  * Modelo UserFunctionAssignment
  * Middleware de validacion automatica
  * API REST para gestion de permisos temporales
  * Comando de limpieza automatica

- CNST-006: Nueva seccion "Patrones de Diseno Recomendados" (+300 lineas)
  * 6 patrones documentados con ejemplos
  * Balance antipatrones + patrones recomendados
  * Guias positivas de arquitectura

**Incremento Total:**

- Lineas: 9,621 → 10,071 (+450 lineas, +4.7%)
- Cobertura: 98.5% → 100%

----

Historial de Versiones
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 10 15 55 20

   * - Version
     - Fecha
     - Cambios
     - Lineas
   * - 1.1.0
     - 2026-01-03
     - Ampliaciones CNST-005 y CNST-006. Integracion RBAC v5.1.1
     - 10,071
   * - 1.0.0
     - 2025-12-17
     - Version inicial completa
     - 9,621

----

Catalogo de Restricciones
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 15 15 20

   * - ID
     - Titulo
     - Lineas
     - Version
     - Estado
   * - CNST-001
     - Comunicaciones Prohibidas
     - 685
     - 1.1.0
     - VIGENTE
   * - CNST-002
     - Gestion de Sesiones en BD
     - 840
     - 1.1.0
     - VIGENTE
   * - CNST-003
     - Base de Datos Dual Inmutable
     - 901
     - 1.1.0
     - VIGENTE
   * - CNST-004
     - Actualizacion Datos ETL
     - 920
     - 1.1.0
     - VIGENTE
   * - CNST-005
     - Seguridad DRF Checklist
     - 1,144
     - 1.1.0
     - VIGENTE
   * - CNST-006
     - Antipatrones Arquitectura
     - 1,426
     - 1.1.0
     - VIGENTE
   * - CNST-007
     - Limites Performance SLA
     - 1,061
     - 1.1.0
     - VIGENTE
   * - CNST-008
     - Infraestructura Deployment
     - 1,019
     - 1.1.0
     - VIGENTE
   * - CNST-009
     - Logging Auditoria Inmutable
     - 1,077
     - 1.1.0
     - VIGENTE
   * - CNST-010
     - Clasificacion Proteccion Datos
     - 998
     - 1.1.0
     - VIGENTE

----

Clasificacion por Categoria
----------------------------

**Restricciones Tecnicas Criticas (No Negociables)**

- CNST-001: Comunicaciones Prohibidas (NO email/SMTP)
- CNST-002: Gestion de Sesiones en BD (NO Redis)
- CNST-003: Base de Datos Dual Inmutable (IVR readonly)
- CNST-004: Actualizacion Datos ETL (NO real-time)

**Restricciones de Seguridad**

- CNST-005: Seguridad DRF Checklist
- CNST-010: Clasificacion Proteccion Datos

**Restricciones de Arquitectura**

- CNST-006: Antipatrones Arquitectura

**Restricciones de Performance**

- CNST-007: Limites Performance SLA

**Restricciones de Infraestructura**

- CNST-008: Infraestructura Deployment

**Restricciones de Auditoria**

- CNST-009: Logging Auditoria Inmutable

----

Integracion con RBAC v5.1.1
---------------------------

Este conjunto de restricciones esta alineado con el Modelo RBAC v5.1.1 que utiliza funciones atomicas en lugar de roles tradicionales.

**Modelo de Funciones Atomicas:**

- 44 funciones distribuidas en 8 modulos funcionales
- Sistema "sin pretensiones" (funciones describen QUE HACE, no QUIEN ES)
- Integracion con SEC_RULES para enforcement automatico
- Soporte para permisos temporales con expiracion automatica

**Modulos IACT:**

- MOD_Auth: Autenticacion y Sesiones (4 funciones)
- MOD_Users: Gestion de Identidades (10 funciones)
- MOD_Access: Roles, Permisos, Segmentos (6 funciones)
- MOD_Pipeline: Supervision del ETL (4 funciones)
- MOD_Reports: Dashboards y Reportes (8 funciones)
- MOD_Alerts: Alertas y Notificaciones (6 funciones)
- MOD_Audit: Auditoria Funcional (4 funciones)
- MOD_Logs: Bitacoras Tecnicas (2 funciones)

**Mapeo CNST a Modulos:**

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - CNST
     - Modulos Afectados
     - Funciones Relacionadas
   * - CNST-001
     - MOD_Alerts
     - notifica_usuario, crea_mensaje_interno
   * - CNST-002
     - MOD_Auth
     - inicia_sesion, cierra_sesion
   * - CNST-003
     - MOD_Pipeline
     - extrae_datos_ivr
   * - CNST-004
     - MOD_Pipeline
     - supervisa_etl, ejecuta_etl
   * - CNST-005
     - Todos
     - Middleware de autenticacion
   * - CNST-006
     - Todos
     - Calidad de codigo
   * - CNST-007
     - MOD_Reports
     - exporta_csv, exporta_excel, genera_reporte
   * - CNST-008
     - N/A
     - Infraestructura
   * - CNST-009
     - MOD_Audit, MOD_Logs
     - registra_auditoria, consulta_logs
   * - CNST-010
     - Todos
     - ve_reportes, analiza_datos, administra_sistema

----

Documentos Relacionados
------------------------

- Modelo RBAC IACT v5.1.1
- Casos de Uso (UC-001 a UC-072)
- SRS v2.0 (8 modulos funcionales)
- ADR (Decisiones de arquitectura)

----