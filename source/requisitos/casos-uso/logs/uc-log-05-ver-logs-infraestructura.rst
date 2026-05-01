.. meta::
 :artefacto: UC_LOG_05
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno
 :normativa: CNST_024, CNST_025

============================================
UC_LOG_05: Ver Logs de Infraestructura
============================================

.. note::

 Caso de uso nuevo en v5.4.0. Cubre logs de infraestructura
 (timeouts, up/down, network, conectividad BD), conceptualmente
 distintos de los logs de aplicación (uc-log-01) y los logs de
 ETL (uc-log-02). Función dedicada LOG-005 ``view_infrastructure_logs``
 — split SRP del antiguo LOG-001 genérico.

 Trazabilidad: ARQ-MOD-008 alcance § 2.1 "logs de infraestructura
 (up/down, timeouts)". Decision D-05 (WP rbac-modelo-conceptual-cleanup).

1. Resumen
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_LOG_05
 * - **Nombre**
   - Ver Logs de Infraestructura
 * - **Actor Principal**
   - AGR-010: ``system_admin_group`` (sysadmin)
 * - **Modulo**
   - MOD_Logs
 * - **Funcion RBAC**
   - LOG-005 ``view_infrastructure_logs`` (NUEVA v5.4.0 — SRP)
 * - **Prioridad**
   - Alta
 * - **Complejidad**
   - Baja
 * - **BReq Origen**
   - BRQ-LOG-005

2. Descripcion
--------------

Este caso de uso permite al sysadmin consultar los logs de
infraestructura del sistema IACT: eventos de red, timeouts,
estados up/down de servicios externos (BD IVR, BD Analytics,
buzón interno), errores de conectividad, restarts, eventos del
runtime del servidor.

**Características principales:**

- Logs específicos de la capa de infraestructura.
- Filtrado por componente (network, db, runtime).
- Filtrado por severidad (INFO/WARN/ERROR/CRITICAL).
- Filtrado por rango de tiempo.
- Formato JSON estructurado (CNST_024).
- NO cubre errores de aplicación (eso es uc-log-01).
- NO cubre logs ETL (eso es uc-log-02).

3. Diagrama de Caso de Uso
--------------------------

.. uml::
 :caption: Diagrama de Caso de Uso - UC_LOG_05

 @startuml
 left to right direction
 actor "AGR-010\nsystem_admin_group" as USER

 rectangle "MOD_Logs" {
 usecase "UC_LOG_05\nVer Logs Infra" as UC05
 usecase "Filtrar por\nComponente" as COMP
 usecase "Filtrar por\nSeveridad" as SEV
 usecase "Filtrar por\nRango temporal" as TS
 }

 USER --> UC05
 UC05 --> COMP : extend
 UC05 --> SEV : extend
 UC05 --> TS : include
 @enduml

4. Contexto de Ejecucion
------------------------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Precondicion
 * - PRE-01
   - Usuario tiene sesión activa con función LOG-005.
 * - PRE-02
   - Sistema de logging de infraestructura está operativo.

4.2 Trigger
^^^^^^^^^^^

El sysadmin accede al visor de logs de infraestructura.

4.3 Postcondiciones
^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Postcondicion
 * - POST-01
   - Se muestran logs de infraestructura filtrados según criterios.

5. Flujo Normal
---------------

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Acción
 * - 1
   - Usuario
   - Accede al visor de logs de infraestructura.
 * - 2
   - Sistema
   - Valida función LOG-005.
 * - 3
   - Sistema
   - Recupera logs de infra del rango temporal por defecto (última hora).
 * - 4
   - Sistema
   - Aplica filtros opcionales (componente, severidad).
 * - 5
   - Sistema
   - Renderiza con resaltado de sintaxis JSON.

6. Excepciones
--------------

6.1 EX-01: Sin Permiso LOG-005
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Paso de origen**
   - 2
 * - **Condición**
   - Usuario no tiene función LOG-005.
 * - **Acción Sistema**
   - Rechaza acceso.
 * - **Mensaje Usuario**
   - "No tiene permisos para ver logs de infraestructura."
 * - **Código Error**
   - LOG-050

7. Reglas de Negocio
--------------------

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Regla
   - Descripción
 * - BR-LOG-50
   - Solo sysadmin
   - Por defecto solo AGR-010 ``system_admin_group`` y AGR-008 ``auditor_group`` tienen LOG-005
 * - BR-LOG-51
   - JSON estructurado
   - Mantiene formato CNST-024
 * - BR-LOG-52
   - Sin PII
   - Logs de infra no contienen PII (CNST-026)

8. Restricciones de Arquitectura
--------------------------------

.. list-table::
 :widths: 15 25 60
 :header-rows: 1

 * - CNST
   - Nombre
   - Aplicación
 * - CNST_024
   - Logs JSON
   - Mantener formato JSON estructurado
 * - CNST_025
   - Auditoría
   - Acceso a logs queda registrado
 * - CNST_026
   - Sin PII
   - Validar antes de mostrar

9. Trazabilidad
---------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **BReq Origen**
   - BRQ-LOG-005
 * - **Funcion RBAC**
   - LOG-005 ``view_infrastructure_logs`` (NUEVA v5.4.0)
 * - **UC Relacionados**
   - uc-log-01 (app logs), uc-log-02 (ETL logs), uc-log-06 (health), uc-log-07 (métricas)
 * - **Clase de Dominio**
   - ``InfrastructureLog`` (primaria) (per :doc:`/arquitectura-tecnica/modelo-dominio-iact` v1.0.0)

10. Historial de Cambios
------------------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-04-30
   - Versión inicial. Caso de uso nuevo en v5.4.0 — split SRP de LOG-001 genérico, cubre el alcance "logs de infraestructura" declarado en ARQ-MOD-008. Decision D-05 (WP rbac-modelo-conceptual-cleanup).
