.. meta::
   :artefacto: UC_017
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-017:

==============================================================================
UC-017: Generar Reporte de Saldos por Cuenta
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
     - UC-017
   * - **Nombre**
     - Generar Reporte de Saldos por Cuenta
   * - **Actor Primario**
     - Analista Contable / Gerente
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Reports
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-002: Generacion de Reportes

----

2. Descripcion
--------------

Genera reporte de saldos contables por cuenta, mostrando saldo inicial,
movimientos debito/credito y saldo final para un periodo. Aplica
segmentacion de datos segun centros de costo del usuario (BR_009).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-017 Reporte Saldos
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

   actor "Analista\nContable" as ANA
   actor "Gerente" as GER
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Reports" {
       usecase "UC-017:\nReporte\nSaldos" as UC017
       usecase "Filtrar\nPeriodo" as FP
       usecase "Filtrar\nCuentas" as FC
       usecase "Exportar" as EX
       usecase "Aplicar\nSegmentacion" as AS
   }

   ANA --> UC017
   GER --> UC017
   UC017 ..> FP : <<include>>
   UC017 ..> FC : <<include>>
   UC017 ..> AS : <<include>>
   UC017 ..> EX : <<extends>>
   UC017 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion RPT-001 (Generar Reporte Saldos)
2. Usuario tiene segmentos asignados (centros de costo)
3. Existen datos contables para el periodo

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Reportes > Saldos por Cuenta".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Reporte generado con datos filtrados
2. Evento REPORT_GENERATED registrado (BR_008)
3. Solo muestra datos de centros del usuario (BR_009)

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
     - Accede a Reporte de Saldos
     -
   * - 2
     -
     - Verifica permiso RPT-001
   * - 3
     -
     - Obtiene segmentos del usuario
   * - 4
     -
     - Muestra formulario de filtros
   * - 5
     - Selecciona periodo (mes/año)
     -
   * - 6
     - (Opcional) Filtra por cuenta
     -
   * - 7
     - Presiona "Generar Reporte"
     -
   * - 8
     -
     - Ejecuta query con segmentacion
   * - 9
     -
     - Calcula saldos iniciales/finales
   * - 10
     -
     - Muestra reporte en pantalla
   * - 11
     -
     - Registra REPORT_GENERATED (BR_008)
   * - 12
     - (Opcional) Exporta a Excel/PDF
     -

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-017 Reporte Saldos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Analista" as U
   participant "Frontend" as FE #E3F2FD
   participant "ReportController" as RC #E8F5E9
   participant "ReportService" as RS #E8F5E9
   participant "SegmentService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Reporte Saldos
   FE -> RC: 2. GET /api/reports/saldos/filters
   activate RC

   RC -> SS: 3. getUserSegments(userId)
   SS -> DB: SELECT segment_id FROM user_segments
   SS --> RC: [segments]

   RC --> FE: 4. {periodos, cuentas, segments}
   deactivate RC

   FE --> U: 5. Formulario de filtros

   U -> FE: 6. Selecciona periodo y genera
   FE -> RC: 7. POST /api/reports/saldos\n{periodo, cuentas, formato}
   activate RC

   RC -> RS: 8. generateSaldos(filters, userSegments)
   activate RS

   RS -> DB: 9. SELECT cuenta, SUM(debito), SUM(credito)\nFROM movimientos\nWHERE periodo = ?\nAND centro_costo IN (user_segments)\nGROUP BY cuenta
   note right: BR_009:\nSegmentacion aplicada
   DB --> RS: [data]

   RS -> RS: 10. calculateBalances(data)

   RS -> AUD: 11. logEvent(REPORT_GENERATED,\n{type: 'SALDOS', filters})
   AUD -> DB: INSERT audit_log

   RS --> RC: 12. {report, totals}
   deactivate RS

   RC --> FE: 13. 200 OK {report}
   deactivate RC

   FE --> U: 14. Muestra reporte en tabla

   U -> FE: 15. Clic "Exportar Excel"
   FE -> RC: 16. GET /api/reports/saldos/export?format=xlsx
   RC --> FE: 17. Binary file
   FE --> U: 18. Descarga archivo
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Sin Datos para Periodo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** No hay movimientos en el periodo seleccionado

**Accion:** Muestra mensaje "Sin datos para el periodo seleccionado"

7.2 FA-2: Exportar a PDF
^^^^^^^^^^^^^^^^^^^^^^^^

Usuario puede exportar a PDF con formato de reporte formal.

----

8. Excepciones
--------------

8.1 EX-1: Sin Segmentos Asignados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No tiene centros de costo asignados. Contacte al administrador."

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-017 Reporte Saldos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Accede a Reporte Saldos;
   :Verificar permiso RPT-001;

   if (Tiene permiso?) then (si)
       :Obtener segmentos usuario;

       if (Tiene segmentos?) then (si)
           :Mostrar filtros;
           :Usuario selecciona periodo;
           :Ejecutar query con segmentacion\n(BR_009);

           if (Hay datos?) then (si)
               :Calcular saldos;
               :Mostrar reporte;
               #C8E6C9:Registrar auditoria;

               if (Exportar?) then (si)
                   :Generar archivo;
                   :Descargar;
               else (no)
               endif
           else (no)
               #FFE0B2:Sin datos para periodo;
           endif
       else (no)
           #FFCDD2:Error: Sin segmentos;
       endif
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
     - Auditoria
     - Generacion de reporte registrada
   * - BR_009
     - Segmentacion
     - Solo datos de centros asignados al usuario

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-017.01
     - Verificar permiso RPT-001
   * - FR-017.02
     - Aplicar segmentacion por centro de costo
   * - FR-017.03
     - Filtrar por periodo (mes/año)
   * - FR-017.04
     - Filtrar por cuenta contable
   * - FR-017.05
     - Calcular saldo inicial del periodo
   * - FR-017.06
     - Mostrar movimientos debito/credito
   * - FR-017.07
     - Calcular saldo final
   * - FR-017.08
     - Exportar a Excel
   * - FR-017.09
     - Exportar a PDF
   * - FR-017.10
     - Registrar generacion en auditoria

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-002: Generacion de Reportes
   * - **BR Aplicables**
     - BR_008, BR_009
   * - **FR Derivados**
     - FR-017.01 a FR-017.10
   * - **Funcion RBAC**
     - RPT-001: Generar Reporte Saldos

----

13. Historial de Cambios
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
