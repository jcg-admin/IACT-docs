.. meta::
   :artefacto: UC_024
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-024:

==============================================================================
UC-024: Generar Reporte Presupuesto vs Real
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
     - UC-024
   * - **Nombre**
     - Generar Reporte Presupuesto vs Real
   * - **Actor Primario**
     - Controller / Gerente Financiero
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Reports
   * - **Complejidad**
     - Alta
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-002: Generacion de Reportes

----

2. Descripcion
--------------

Genera reporte comparativo entre el presupuesto aprobado y la ejecucion
real, mostrando desviaciones por cuenta y centro de costo. Calcula
porcentaje de ejecucion y variaciones para control presupuestario.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-024 Presupuesto vs Real
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

   actor "Controller" as CTR
   actor "Gerente\nFinanciero" as GER

   rectangle "MOD_Reports" {
       usecase "UC-024:\nPresupuesto\nvs Real" as UC024
       usecase "Seleccionar\nPeriodo" as SP
       usecase "Ver %\nEjecucion" as VE
       usecase "Alertar\nDesviaciones" as AD
       usecase "Exportar" as EX
   }

   CTR --> UC024
   GER --> UC024
   UC024 ..> SP : <<include>>
   UC024 ..> VE : <<include>>
   UC024 ..> AD : <<extends>>
   UC024 ..> EX : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion RPT-008 (Presupuesto vs Real)
2. Existe presupuesto cargado para el periodo
3. Usuario tiene segmentos asignados

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Reportes > Presupuesto vs Real".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Reporte generado con comparativo
2. Desviaciones significativas resaltadas con semaforo
3. Evento REPORT_GENERATED registrado

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
     - Accede a Presupuesto vs Real
     -
   * - 2
     -
     - Verifica permiso RPT-008
   * - 3
     -
     - Carga centros de costo del usuario
   * - 4
     - Selecciona periodo
     -
   * - 5
     - Presiona "Generar Reporte"
     -
   * - 6
     -
     - Obtiene presupuesto del periodo
   * - 7
     -
     - Obtiene ejecucion real
   * - 8
     -
     - Calcula desviaciones y % ejecucion
   * - 9
     -
     - Aplica semaforos de alerta
   * - 10
     -
     - Muestra reporte
   * - 11
     -
     - Registra en auditoria

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-024 Presupuesto vs Real
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   actor "Controller" as U
   participant "Frontend" as FE #E3F2FD
   participant "ReportController" as RC #E8F5E9
   participant "BudgetService" as BS #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede al reporte
   FE -> RC: 2. GET /api/reports/budget/options
   RC --> FE: 3. {periodos, centros}
   FE --> U: 4. Formulario

   U -> FE: 5. Selecciona y genera
   FE -> RC: 6. POST /api/reports/budget
   activate RC

   RC -> BS: 7. compareBudget(params)
   activate BS

   BS -> DB: 8. SELECT FROM presupuesto
   DB --> BS: [presupuesto]

   BS -> DB: 9. SELECT FROM movimientos
   DB --> BS: [ejecutado]

   BS -> BS: 10. calcularDesviaciones()
   note right: Semaforo:\nVerde <5%\nAmarillo 5-15%\nRojo >15%

   BS --> RC: 11. {comparison, alerts}
   deactivate BS

   RC --> FE: 12. 200 OK
   deactivate RC
   FE --> U: 13. Tabla con semaforos
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Sin Presupuesto
^^^^^^^^^^^^^^^^^^^^^^^^^

Muestra mensaje y solo datos reales disponibles.

7.2 FA-2: Proyeccion Anual
^^^^^^^^^^^^^^^^^^^^^^^^^^

Calcula proyeccion anual basado en ejecucion actual.

----

8. Excepciones
--------------

8.1 EX-1: Presupuesto No Cargado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay presupuesto aprobado para el periodo"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-024 Presupuesto vs Real
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso RPT-008;
   :Seleccionar periodo;
   :Obtener presupuesto;

   if (Existe presupuesto?) then (si)
       :Obtener ejecucion real;
       :Calcular desviaciones;

       while (Por cada cuenta) is (siguiente)
           if (Desviacion < 5%?) then (si)
               #C8E6C9:VERDE;
           elseif (Desviacion < 15%?) then (si)
               #FFF9C4:AMARILLO;
           else (>15%)
               #FFCDD2:ROJO;
           endif
       endwhile (fin)

       :Mostrar reporte;
       #C8E6C9:Registrar auditoria;
   else (no)
       #FFE0B2:Sin presupuesto;
   endif
   stop
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
     - Generacion registrada
   * - BR_009
     - Segmentacion
     - Solo centros del usuario
   * - BR_016
     - Semaforo
     - Verde <5%, Amarillo 5-15%, Rojo >15%

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-024.01
     - Verificar permiso RPT-008
   * - FR-024.02
     - Aplicar segmentacion (BR_009)
   * - FR-024.03
     - Obtener presupuesto aprobado
   * - FR-024.04
     - Obtener ejecucion real
   * - FR-024.05
     - Calcular desviacion absoluta y porcentual
   * - FR-024.06
     - Aplicar semaforo de desviacion
   * - FR-024.07
     - Calcular proyeccion anual
   * - FR-024.08
     - Exportar a Excel y PDF

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-002
   * - **BR Aplicables**
     - BR_008, BR_009, BR_016
   * - **FR Derivados**
     - FR-024.01 a FR-024.08
   * - **Funcion RBAC**
     - RPT-008

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
     - Version con PlantUML embebido. 3 diagramas.