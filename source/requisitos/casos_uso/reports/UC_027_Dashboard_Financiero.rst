.. meta::
   :artefacto: UC_027
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-027:

==============================================================================
UC-027: Ver Dashboard Financiero
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
     - UC-027
   * - **Nombre**
     - Ver Dashboard Financiero
   * - **Actor Primario**
     - Gerente Financiero / Director
   * - **Actores Secundarios**
     - Ninguno
   * - **Modulo**
     - MOD_Reports
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-003: Visualizacion de Indicadores

----

2. Descripcion
--------------

Muestra dashboard con indicadores financieros clave: ratios de liquidez
(corriente, prueba acida), ratios de rentabilidad (ROA, ROE, margen neto),
ratios de endeudamiento y capital de trabajo. Incluye graficos de
tendencia y comparativo con periodos anteriores.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-027 Dashboard Financiero
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

   actor "Gerente\nFinanciero" as GER
   actor "Director" as DIR

   rectangle "MOD_Reports" {
       usecase "UC-027:\nDashboard\nFinanciero" as UC027
       usecase "Ver Ratios\nLiquidez" as VRL
       usecase "Ver Ratios\nRentabilidad" as VRR
       usecase "Ver\nEndeudamiento" as VE
       usecase "Ver\nTendencias" as VT
   }

   GER --> UC027
   DIR --> UC027
   UC027 ..> VRL : <<include>>
   UC027 ..> VRR : <<include>>
   UC027 ..> VE : <<include>>
   UC027 ..> VT : <<include>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion DSH-002 (Dashboard Financiero)
2. Usuario tiene segmentos asignados
3. Existen datos financieros calculados

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Dashboard > Financiero".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Dashboard renderizado con KPIs financieros
2. Graficos de tendencia generados
3. Comparativo con periodo anterior mostrado

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
     - Accede a Dashboard Financiero
     -
   * - 2
     -
     - Verifica permiso DSH-002
   * - 3
     -
     - Obtiene segmentos del usuario
   * - 4
     -
     - Calcula ratios de liquidez
   * - 5
     -
     - Calcula ratios de rentabilidad
   * - 6
     -
     - Calcula ratios de endeudamiento
   * - 7
     -
     - Genera datos de tendencia (12 meses)
   * - 8
     -
     - Renderiza dashboard con widgets
   * - 9
     - Visualiza indicadores
     -
   * - 10
     - (Opcional) Cambia periodo
     -
   * - 11
     -
     - Recalcula y actualiza

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-027 Dashboard Financiero
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   actor "Gerente" as U
   participant "Frontend" as FE #E3F2FD
   participant "DashboardController" as DC #E8F5E9
   participant "RatioService" as RS #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Dashboard Financiero
   FE -> DC: 2. GET /api/dashboard/financial
   activate DC

   DC -> RS: 3. calculateLiquidityRatios(segments)
   activate RS
   RS -> DB: SELECT activo_corriente, pasivo_corriente
   RS -> RS: 4. razonCorriente = AC / PC
   RS -> RS: 5. pruebaAcida = (AC - inventarios) / PC
   RS --> DC: {liquidez}
   deactivate RS

   DC -> RS: 6. calculateProfitabilityRatios(segments)
   activate RS
   RS -> DB: SELECT utilidad, activos, patrimonio
   RS -> RS: 7. ROA = utilidad / activos
   RS -> RS: 8. ROE = utilidad / patrimonio
   RS -> RS: 9. margenNeto = utilidad / ingresos
   RS --> DC: {rentabilidad}
   deactivate RS

   DC -> RS: 10. calculateDebtRatios(segments)
   activate RS
   RS -> DB: SELECT pasivo, patrimonio
   RS -> RS: 11. endeudamiento = pasivo / activo
   RS --> DC: {endeudamiento}
   deactivate RS

   DC -> RS: 12. getTrends(12 months)
   RS --> DC: {trends}

   DC --> FE: 13. {liquidez, rentabilidad,\nendeudamiento, trends}
   deactivate DC

   FE --> U: 14. Dashboard con widgets y graficos
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Drill-down en Ratio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usuario hace clic en ratio para ver detalle de calculo.

7.2 FA-2: Comparar con Industria
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usuario activa benchmark para comparar con promedios.

----

8. Excepciones
--------------

8.1 EX-1: Datos Insuficientes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay datos suficientes para calcular indicadores"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-027 Dashboard Financiero
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso DSH-002;
   :Obtener segmentos usuario;

   fork
       :Calcular Liquidez;
       note right
           Razon Corriente
           Prueba Acida
           Capital Trabajo
       end note
   fork again
       :Calcular Rentabilidad;
       note right
           ROA
           ROE
           Margen Neto
       end note
   fork again
       :Calcular Endeudamiento;
       note right
           Razon Deuda
           Cobertura Intereses
       end note
   fork again
       :Generar Tendencias;
       note right
           Ultimos 12 meses
       end note
   end fork

   :Renderizar widgets;
   :Mostrar graficos;

   while (Usuario en dashboard?) is (si)
       :Esperar interaccion;
       if (Cambia periodo?) then (si)
           :Recalcular ratios;
       else (no)
       endif
   endwhile (no)
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
   * - BR_009
     - Segmentacion
     - Solo datos de centros del usuario
   * - BR_018
     - Formulas Ratios
     - Formulas estandar de analisis financiero

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-027.01
     - Verificar permiso DSH-002
   * - FR-027.02
     - Aplicar segmentacion (BR_009)
   * - FR-027.03
     - Calcular razon corriente
   * - FR-027.04
     - Calcular prueba acida
   * - FR-027.05
     - Calcular ROA y ROE
   * - FR-027.06
     - Calcular margen neto
   * - FR-027.07
     - Calcular razon de endeudamiento
   * - FR-027.08
     - Mostrar tendencias 12 meses
   * - FR-027.09
     - Permitir drill-down en ratios

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-003
   * - **BR Aplicables**
     - BR_009, BR_018
   * - **FR Derivados**
     - FR-027.01 a FR-027.09
   * - **Funcion RBAC**
     - DSH-002

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
