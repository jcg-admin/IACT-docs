
.. meta::
   :artefacto: UC_047
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-047:

==============================================================================
UC-047: Auditar Cambios de Permisos
==============================================================================

.. contents:: Contenido
   :local:
   :depth: 2

----

1. Resumen
----------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **ID**
     - UC-047
   * - **Nombre**
     - Auditar Cambios de Permisos
   * - **Actor Primario**
     - Auditor / Administrador de Seguridad
   * - **Actores Secundarios**
     - Ninguno
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite consultar el historial de cambios en permisos del sistema: asignaciones,
revocaciones, cambios en agrupadores y funciones. Soporta filtros por fecha,
usuario, tipo de accion y exportacion para auditorias externas.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-047 Auditar Permisos
   :align: center
   :scale: 90%

   @startuml
   left to right direction
   skinparam actorStyle awesome
   skinparam backgroundColor #FAFAFA
   skinparam usecase {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
   }

   actor "Auditor" as AUD
   actor "Admin\nSeguridad" as ADM

   rectangle "MOD_Access" {
       usecase "UC-047:\nAuditar\nPermisos" as UC047
       usecase "Filtrar por\nFecha" as FF
       usecase "Filtrar por\nUsuario" as FU
       usecase "Filtrar por\nAccion" as FA
       usecase "Exportar\nReporte" as ER
   }

   AUD --> UC047
   ADM --> UC047
   UC047 ..> FF : <<include>>
   UC047 ..> FU : <<include>>
   UC047 ..> FA : <<include>>
   UC047 ..> ER : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion ACC-009 (Auditar Permisos) o AUD-002 (Consultar Auditoria)
2. Existen registros de auditoria de permisos

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Auditoria de Permisos" en modulo de seguridad.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Registros de auditoria mostrados segun filtros
2. Opcionalmente exportados a PDF/Excel

----

5. Flujo Normal
---------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Accede a Auditoria de Permisos
     -
   * - 2
     -
     - Verifica permiso ACC-009 o AUD-002
   * - 3
     -
     - Muestra ultimos 100 registros
   * - 4
     - (Opcional) Aplica filtro de fechas
     -
   * - 5
     - (Opcional) Filtra por usuario
     -
   * - 6
     - (Opcional) Filtra por tipo de accion
     -
   * - 7
     -
     - Actualiza resultados segun filtros
   * - 8
     - (Opcional) Exporta a PDF/Excel
     -
   * - 9
     -
     - Genera archivo con datos filtrados

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-047 Auditar Permisos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Auditor" as AUD
   participant "Frontend" as FE #E3F2FD
   participant "AuditController" as AC #E8F5E9
   participant "AuditService" as AS #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   AUD -> FE: 1. Accede a Auditoria Permisos
   FE -> AC: 2. GET /api/audit/permissions\n?limit=100
   activate AC

   AC -> AS: 3. getPermissionAudit(filters)
   activate AS

   AS -> DB: 4. SELECT * FROM audit_log\nWHERE action IN (\n'FUNCTIONS_ASSIGNED',\n'FUNCTIONS_REVOKED',\n'SEGMENTS_ASSIGNED', ...)\nORDER BY timestamp DESC
   DB --> AS: [auditRecords]

   AS --> AC: 5. {records, total}
   deactivate AS

   AC --> FE: 6. 200 OK {audit}
   deactivate AC

   FE --> AUD: 7. Tabla de auditoria
   note right: Columnas: Fecha, Usuario,\nAccion, Admin, Detalles

   AUD -> FE: 8. Aplica filtros
   FE -> AC: 9. GET /api/audit/permissions\n?from=&to=&user=&action=

   AC --> FE: 10. Resultados filtrados

   AUD -> FE: 11. Clic "Exportar PDF"
   FE -> AC: 12. GET /api/audit/permissions/export\n?format=pdf&filters=...
   activate AC

   AC -> AS: 13. generateReport(filters, 'pdf')
   AS --> AC: {pdfBytes}

   AC --> FE: 14. 200 OK (binary/pdf)
   deactivate AC

   FE --> AUD: 15. Descarga archivo PDF
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Sin Resultados
^^^^^^^^^^^^^^^^^^^^^^^^

Si no hay registros que coincidan con filtros, muestra mensaje informativo.

7.2 FA-2: Exportar a Excel
^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar a PDF pero genera archivo .xlsx con todos los campos.

----

8. Excepciones
--------------

8.1 EX-1: Sin Permiso
^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No tiene permisos para acceder a auditoria de permisos"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-047 Auditar Permisos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam activity {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
   }

   start

   :Accede a Auditoria Permisos;

   :Verificar permiso;

   if (Tiene ACC-009 o AUD-002?) then (si)

       :Cargar ultimos 100 registros;
       :Mostrar tabla;

       while (Usuario interactua?) is (si)

           split
               :Filtrar por fecha;
           split again
               :Filtrar por usuario;
           split again
               :Filtrar por accion;
           split again
               :Exportar PDF/Excel;
               :Generar archivo;
               :Descargar;
           end split

           :Actualizar resultados;

       endwhile (no)

       stop

   else (no)
       #FFCDD2:403 Forbidden;
       stop
   endif

   @enduml

----

10. Reglas de Negocio
---------------------

.. list-table::
   :widths: 12 25 63
   :header-rows: 1

   * - BR
     - Nombre
     - Aplicacion
   * - BR_008
     - Auditoria de Accesos
     - Este UC consulta los registros generados por BR_008

----

11. Tipos de Eventos Auditados
------------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Evento
     - Descripcion
   * - FUNCTIONS_ASSIGNED
     - Funciones asignadas a usuario
   * - FUNCTIONS_REVOKED
     - Funciones revocadas a usuario
   * - SEGMENTS_ASSIGNED
     - Segmentos asignados a usuario
   * - SEGMENTS_REVOKED
     - Segmentos revocados a usuario
   * - SOD_RULE_CREATED
     - Regla SoD creada
   * - SOD_RULE_DELETED
     - Regla SoD eliminada
   * - GROUPER_CREATED
     - Agrupador creado
   * - GROUPER_MODIFIED
     - Agrupador modificado
   * - FUNCTION_CREATED
     - Funcion creada
   * - FUNCTION_MODIFIED
     - Funcion modificada

----

12. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-047.01
     - Verificar permiso ACC-009 o AUD-002
   * - FR-047.02
     - Mostrar ultimos 100 registros por defecto
   * - FR-047.03
     - Permitir filtro por rango de fechas
   * - FR-047.04
     - Permitir filtro por usuario afectado
   * - FR-047.05
     - Permitir filtro por tipo de accion
   * - FR-047.06
     - Permitir filtro por administrador que realizo
   * - FR-047.07
     - Exportar a PDF con formato de auditoria
   * - FR-047.08
     - Exportar a Excel con todos los campos
   * - FR-047.09
     - Paginar resultados (100 por pagina)

----

13. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_008 (Auditoria de Accesos)
   * - **FR Derivados**
     - FR-047.01 a FR-047.09 (9 requerimientos)
   * - **UC Relacionados**
     - UC-010, UC-011, UC-041-046 (generan eventos)
   * - **Funciones RBAC**
     - ACC-009: Auditar Permisos, AUD-002: Consultar Auditoria

----

14. Historial de Cambios
------------------------

.. list-table::
   :widths: 12 12 76
   :header-rows: 1

   * - Version
     - Fecha
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Version con PlantUML embebido (Sphinx)