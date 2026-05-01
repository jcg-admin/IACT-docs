.. meta::
 :artefacto: UC_RPT_11
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: reports
 :estado: Aprobado
 :version: 4.0.0
 :fecha_creacion: 2026-01-06
 :autor: Equipo IACT
 :clasificacion: Interno
 :normativa: CNST_001, CNST_008, CNST_025

============================
UC_RPT_11: Compartir Reporte
============================

1. Resumen
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_RPT_11
 * - **Nombre**
   - Compartir Reporte
 * - **Actor Principal**
   - AGR-003: agr_supervisor
 * - **Modulo**
   - MOD_Reports
 * - **Funcion RBAC**
   - RPT-011: ``share_report`` (RESTAURADA en modelo v5.3.0)
 * - **Prioridad**
   - Media
 * - **Complejidad**
   - Media
 * - **BReq Origen**
   - BRQ-RPT-011

2. Descripcion
--------------

Permite compartir un reporte generado con otros usuarios del mismo
agrupador (AGR). La notificacion se envia via InternalMessage (CNST_001).

**Restriccion CNST_001:** Notificaciones SOLO via InternalMessage.

3. Diagrama de Caso de Uso
--------------------------

.. uml::
 :caption: Diagrama de Caso de Uso - UC_RPT_11

 @startuml
 left to right direction
 actor "AGR-003\nagr_supervisor" as USER
 rectangle "MOD_Reports" {
 usecase "UC_RPT_11\nCompartir Reporte" as UC11
 usecase "Notificar via\nInternalMessage" as NOT
 }
 USER --> UC11
 UC11 --> NOT : include
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
   - Usuario tiene funcion RPT-011
 * - PRE-02
   - Existe un reporte para compartir
 * - PRE-03
   - Destinatarios del mismo agrupador (AGR)

4.2 Trigger
^^^^^^^^^^^

Usuario hace clic en Compartir desde un reporte.

4.3 Postcondiciones
^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Postcondicion
 * - POST-01
   - Reporte compartido con destinatarios
 * - POST-02
   - Notificacion enviada via InternalMessage

5. Flujo Normal (Camino Feliz)
------------------------------

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Accion
 * - 1
   - Usuario
   - Hace clic en Compartir
 * - 2
   - Sistema
   - Valida RPT-011
 * - 3
   - Sistema
   - Muestra usuarios del agrupador
 * - 4
   - Usuario
   - Selecciona destinatarios
 * - 5
   - Usuario
   - Opcionalmente agrega mensaje
 * - 6
   - Sistema
   - Valida destinatarios del agrupador (AGR)
 * - 7
   - Sistema
   - Envia notificacion via InternalMessage
 * - 8
   - Sistema
   - Registra en auditoria

6. Diagrama de Secuencia
------------------------

.. uml::
 :caption: Diagrama de Secuencia - UC_RPT_11

 @startuml
 actor "Usuario" as U
 participant "Frontend" as FE
 participant "ShareController" as SC
 participant "ShareService" as SS
 participant "InternalMessage" as IM
 participant "UserActionLog" as UAL
 database "Analytics" as DB

 U -> FE: Compartir reporte
 FE -> SC: POST /api/reports/share
 SC -> SC: verify_function(RPT-011)
 SC -> SS: share_report(report, destinatarios)
 SS -> SS: validate_same_segment
 note right: CNST_008
 SS -> IM: notify(destinatarios, report_link)
 note right: CNST_001
 SS -> UAL: record(REPORT_SHARE)
 note right: CNST_025
 UAL -> DB: INSERT audit
 SS --> SC: shared
 SC --> FE: 200 OK
 FE --> U: Reporte compartido
 @enduml

7. Flujos Alternos
------------------

7.1 FA-01: Compartir con Mensaje
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Accion
 * - 5a
   - Usuario
   - Ingresa mensaje personalizado
 * - 7a
   - Sistema
   - Incluye mensaje en notificacion

8. Excepciones
--------------

8.1 EX-01: Destinatario Otro Agrupador
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Condicion**
   - Destinatario de agrupador diferente
 * - **Mensaje**
   - Solo puede compartir con usuarios del mismo agrupador (AGR)
 * - **Codigo Error**
   - RPT-100

9. Diagrama de Actividad
------------------------

.. uml::
 :caption: Diagrama de Actividad - UC_RPT_11

 @startuml
 start
 if (Tiene RPT-011?) then (no)
 stop
 else (si)
 endif
 :Seleccionar destinatarios;
 if (Mismo agrupador?) then (no)
 :Error agrupador;
 stop
 else (si)
 endif
 :Enviar via InternalMessage;
 note right: CNST_001
 :Registrar auditoria;
 stop
 @enduml

10. Reglas de Negocio
---------------------

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Regla
   - Descripcion
 * - BR-RPT-100
   - Mismo Agrupador (AGR)
   - Solo usuarios del mismo agrupador (AGR)
 * - BR-RPT-101
   - Notificacion
   - Via InternalMessage unicamente

11. Restricciones de Arquitectura
---------------------------------

.. list-table::
 :widths: 15 25 60
 :header-rows: 1

 * - CNST
   - Nombre
   - Aplicacion
 * - CNST_001
   - Comunicacion Interna
   - Solo InternalMessage
 * - CNST_008
   - Agrupadores (AGR)
   - Mismo agrupador (AGR)
 * - CNST_025
   - Auditoria
   - Registro REPORT_SHARE

12. Requisitos Funcionales Derivados
------------------------------------

.. list-table::
 :widths: 15 40 45
 :header-rows: 1

 * - ID
   - Requisito
   - Criterio de Aceptacion
 * - FR-RPT-100
   - Compartir reportes
   - Notificacion enviada
 * - FR-RPT-101
   - Validar agrupador (AGR)
   - Solo mismo agrupador (AGR)

13. Trazabilidad
----------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **BReq Origen**
   - BRQ-RPT-011
 * - **Restricciones**
   - CNST_001, CNST_008, CNST_025
 * - **UC Relacionados**
   - UC_RPT_01 (Dashboard), UC_RPT_03 (Historicos), UC_RPT_04 (Exportar)
 * - **Clase de Dominio**
   - ``Report`` (primaria, operacion share), ``InternalMailbox``, ``AuditEvent`` (per :doc:`/arquitectura-tecnica/modelo-dominio-iact` v1.0.0)
 * - **Actor Principal**
   - AGR-003: agr_supervisor
 * - **Funcion RBAC**
   - RPT-011: ``share_report`` (RESTAURADA en modelo v5.3.0)

14. Historial de Cambios
------------------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Version
   - Fecha
   - Cambios
 * - 4.0.0
   - 2026-01-06
   - Version inicial v4.0