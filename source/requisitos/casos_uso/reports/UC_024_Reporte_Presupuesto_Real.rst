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
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Reports" {
       usecase "UC-024:\nPresupuesto\nvs Real" as UC024
       usecase "Seleccionar\nPeriodo" as SP
       usecase "Seleccionar\nCentro Costo" as SCC
       usecase "Ver %\nEjecucion" as VE
       usecase "Alertar\nDesviaciones" as AD
       usecase "Exportar" as EX
   }

   CTR --> UC024
   GER --> UC024
   UC024 ..> SP : <<include>>
   UC024 ..> SCC : <<include>>
   UC024 ..> VE : <<include>>
   UC024 ..> AD : <<extends>>
   UC024 ..> EX : <<extends>>
   UC024 --> SA
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
2. Desviaciones significativas resaltadas
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
     - (Opcional) Filtra por centro costo
     -
   * - 6
     - Presiona "Generar Reporte"
     -
   * - 7
     -
     - Obtiene presupuesto del periodo
   * - 8
     -
     - Obtiene ejecucion real
   * - 9
     -
     - Calcula desviaciones
   * - 10
     -
     - Calcula % de ejecucion
   * - 11
     -
     - Identifica alertas (>15% desviacion)
   * - 12
     -
     - Muestra reporte con semaforos
   * - 13
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
   skinparam sequenceMessageAlign center

   actor "Controller" as U
   participant "Frontend" as FE #E3F2FD
   participant "ReportController" as RC #E8F5E9
   participant "BudgetService" as BS #E8F5E9
   participant "AlertService" as AL #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Presupuesto vs Real
   FE -> RC: 2. GET /api/reports/budget/options
   RC --> FE: 3. {periodos, centros}

   FE --> U: 4. Formulario

   U -> FE: 5. Selecciona periodo y centro
   FE -> RC: 6. POST /api/reports/budget\n{periodo, centro}
   activate RC

   RC -> BS: 7. compareBudgetVsActual(params)
   activate BS

   BS -> DB: 8. SELECT cuenta, monto\nFROM presupuesto\nWHERE periodo = ?\nAND centro = ?
   DB --> BS: [presupuesto]

   BS -> DB: 9. SELECT cuenta, SUM(monto)\nFROM movimientos\nWHERE periodo = ?\nAND centro = ?
   DB --> BS: [ejecutado]
cat >> /mnt/user-data/outputs/casos_uso_v2/reports/UC_024_Reporte_Presupuesto_Real.rst << 'EOF'

   BS -> BS: 10. merge(presupuesto, ejecutado)

   loop Por cada cuenta
       BS -> BS: 11. desviacion = ejecutado - presupuesto
       BS -> BS: 12. pctEjecucion = ejecutado/presupuesto * 100
       BS -> BS: 13. pctDesviacion = desviacion/presupuesto * 100
   end

   BS -> AL: 14. checkAlerts(desviaciones)
   activate AL
   AL -> AL: 15. flagSignificant(>15%)
   note right: Semaforo:\nVerde <5%\nAmarillo 5-15%\nRojo >15%
   AL --> BS: [alertas]
   deactivate AL

   BS -> AUD: 16. logEvent(REPORT_GENERATED)
   AUD -> DB: INSERT audit_log

   BS --> RC: 17. {comparison, alerts, totals}
   deactivate BS

   RC --> FE: 18. 200 OK {report}
   deactivate RC

   FE --> U: 19. Tabla con semaforos de desviacion
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Desglose por Centro de Costo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario no filtra por centro especifico

Muestra resumen por centro con opcion de expandir.

7.2 FA-2: Proyeccion Anual
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario activa proyeccion

Calcula proyeccion anual basado en ejecucion actual.

7.3 FA-3: Sin Presupuesto
^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** No existe presupuesto para el periodo

**Accion:** Muestra mensaje y solo datos reales.

----

8. Excepciones
--------------

8.1 EX-1: Presupuesto No Cargado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay presupuesto aprobado para el periodo [X]"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-024 Presupuesto vs Real
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam activity {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
       DiamondBackgroundColor #FFF9C4
       DiamondBorderColor #F57C00
   }

   start
   :Accede a Presupuesto vs Real;
   :Verificar permiso RPT-008;

   if (Tiene permiso?) then (si)
       :Cargar centros disponibles;
       :Usuario selecciona periodo;
       :Usuario selecciona centro (opcional);

       :Obtener presupuesto;

       if (Existe presupuesto?) then (si)
           :Obtener ejecucion real;

           fork
               :Calcular desviaciones;
           fork again
               :Calcular % ejecucion;
           end fork

           while (Por cada cuenta) is (siguiente)
               if (Desviacion < 5%?) then (si)
                   #C8E6C9:Semaforo VERDE;
               elseif (Desviacion < 15%?) then (si)
                   #FFF9C4:Semaforo AMARILLO;
               else (no)
                   #FFCDD2:Semaforo ROJO;
               endif
           endwhile (fin)

           :Generar tabla con semaforos;
           :Mostrar totales y resumen;
           #C8E6C9:Registrar auditoria;

       else (no)
           #FFE0B2:Sin presupuesto;
           :Mostrar solo datos reales;
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
     - Generacion registrada
   * - BR_009
     - Segmentacion
     - Solo centros del usuario
   * - BR_016
     - Semaforo Presupuestal
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
     - Calcular desviacion absoluta
   * - FR-024.06
     - Calcular % de ejecucion
   * - FR-024.07
     - Aplicar semaforo de desviacion
   * - FR-024.08
     - Permitir desglose por centro
   * - FR-024.09
     - Calcular proyeccion anual
   * - FR-024.10
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
     - FR-024.01 a FR-024.10
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
