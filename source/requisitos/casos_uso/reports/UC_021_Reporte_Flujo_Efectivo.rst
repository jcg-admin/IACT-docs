.. meta::
   :artefacto: UC_021
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-021:

==============================================================================
UC-021: Generar Reporte Flujo de Efectivo
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
     - UC-021
   * - **Nombre**
     - Generar Reporte Flujo de Efectivo
   * - **Actor Primario**
     - Contador / Tesorero
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

Genera el Estado de Flujo de Efectivo mostrando movimientos de caja
clasificados en tres categorias: Actividades Operacionales, Actividades
de Inversion y Actividades de Financiamiento. Presenta efectivo inicial,
variacion neta y efectivo final del periodo.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-021 Flujo de Efectivo
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

   actor "Contador" as CNT
   actor "Tesorero" as TES
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Reports" {
       usecase "UC-021:\nFlujo de\nEfectivo" as UC021
       usecase "Seleccionar\nPeriodo" as SP
       usecase "Metodo\nDirecto/Indirecto" as MD
       usecase "Exportar" as EX
   }

   CNT --> UC021
   TES --> UC021
   UC021 ..> SP : <<include>>
   UC021 ..> MD : <<include>>
   UC021 ..> EX : <<extends>>
   UC021 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion RPT-005 (Generar Flujo de Efectivo)
2. Usuario tiene segmentos asignados
3. Existen movimientos de caja en el periodo

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Reportes > Flujo de Efectivo".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Flujo de Efectivo generado con tres secciones
2. Variacion neta reconciliada con saldo final
3. Evento REPORT_GENERATED registrado (BR_008)

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
     - Accede a Flujo de Efectivo
     -
   * - 2
     -
     - Verifica permiso RPT-005
   * - 3
     -
     - Obtiene segmentos del usuario
   * - 4
     -
     - Muestra formulario de opciones
   * - 5
     - Selecciona periodo
     -
   * - 6
     - Selecciona metodo (directo/indirecto)
     -
   * - 7
     - Presiona "Generar Flujo"
     -
   * - 8
     -
     - Obtiene saldo inicial de efectivo
   * - 9
     -
     - Calcula flujo de Actividades Operacionales
   * - 10
     -
     - Calcula flujo de Actividades de Inversion
   * - 11
     -
     - Calcula flujo de Actividades de Financiamiento
   * - 12
     -
     - Suma variacion neta del periodo
   * - 13
     -
     - Verifica saldo final = inicial + variacion
   * - 14
     -
     - Muestra Flujo de Efectivo
   * - 15
     -
     - Registra en auditoria (BR_008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-021 Flujo de Efectivo
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Tesorero" as U
   participant "Frontend" as FE #E3F2FD
   participant "ReportController" as RC #E8F5E9
   participant "CashFlowService" as CF #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Flujo de Efectivo
   FE -> RC: 2. GET /api/reports/cashflow/options
   RC --> FE: 3. {periodos, metodos}

   FE --> U: 4. Formulario

   U -> FE: 5. Genera con periodo y metodo
   FE -> RC: 6. POST /api/reports/cashflow\n{periodo, metodo, segments}
   activate RC

   RC -> CF: 7. generateCashFlow(params)
   activate CF

   CF -> DB: 8. SELECT saldo FROM cuentas_efectivo\nWHERE fecha < inicio_periodo
   DB --> CF: {saldoInicial}

   CF -> DB: 9. SELECT * FROM movimientos\nWHERE cuenta IN (operacionales)\nAND centro IN (segments)
   note right: Cobros clientes,\nPagos proveedores, etc.
   DB --> CF: [movOperacionales]

   CF -> CF: 10. flujoOperacional = SUM(movOperacionales)

   CF -> DB: 11. SELECT * FROM movimientos\nWHERE cuenta IN (inversion)
   note right: Compra/venta activos
   DB --> CF: [movInversion]

   CF -> CF: 12. flujoInversion = SUM(movInversion)

   CF -> DB: 13. SELECT * FROM movimientos\nWHERE cuenta IN (financiamiento)
   note right: Prestamos, dividendos
   DB --> CF: [movFinanciamiento]

   CF -> CF: 14. flujoFinanc = SUM(movFinanciamiento)

   CF -> CF: 15. variacionNeta = oper + inv + financ
   CF -> CF: 16. saldoFinal = saldoInicial + variacionNeta

   CF -> AUD: 17. logEvent(REPORT_GENERATED)
   AUD -> DB: INSERT audit_log

   CF --> RC: 18. {saldoInicial, operacional,\ninversion, financiamiento,\nvariacionNeta, saldoFinal}
   deactivate CF

   RC --> FE: 19. 200 OK {cashflow}
   deactivate RC

   FE --> U: 20. Muestra Flujo de Efectivo
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Metodo Indirecto
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario selecciona metodo indirecto

Parte de la Utilidad Neta y ajusta por partidas no monetarias
(depreciacion, provisiones, variacion capital de trabajo).

7.2 FA-2: Flujo Negativo
^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Variacion neta es negativa

Sistema muestra advertencia de consumo de efectivo.

----

8. Excepciones
--------------

8.1 EX-1: Sin Cuentas de Efectivo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay cuentas de efectivo configuradas en el sistema"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-021 Flujo de Efectivo
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
   :Accede a Flujo de Efectivo;
   :Verificar permiso RPT-005;

   if (Tiene permiso?) then (si)
       :Obtener segmentos;
       :Usuario selecciona periodo;
       :Usuario selecciona metodo;

       if (Metodo directo?) then (si)
           :Clasificar movimientos por tipo;
       else (indirecto)
           :Partir de Utilidad Neta;
           :Ajustar partidas no monetarias;
       endif

       :Obtener saldo inicial;

       fork
           :Calcular Flujo Operacional;
       fork again
           :Calcular Flujo Inversion;
       fork again
           :Calcular Flujo Financiamiento;
       end fork

       :Variacion = Oper + Inv + Financ;
       :Saldo Final = Inicial + Variacion;

       if (Variacion < 0?) then (si)
           #FFE0B2:Advertencia: consumo efectivo;
       else (no)
       endif

       :Mostrar Flujo de Efectivo;
       #C8E6C9:Registrar auditoria;

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
   * - BR_013
     - Flujo Efectivo
     - Variacion = Oper + Inv + Financ

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-021.01
     - Verificar permiso RPT-005
   * - FR-021.02
     - Aplicar segmentacion (BR_009)
   * - FR-021.03
     - Calcular saldo inicial de efectivo
   * - FR-021.04
     - Calcular flujo de Actividades Operacionales
   * - FR-021.05
     - Calcular flujo de Actividades de Inversion
   * - FR-021.06
     - Calcular flujo de Actividades de Financiamiento
   * - FR-021.07
     - Soportar metodo directo e indirecto
   * - FR-021.08
     - Verificar saldo final = inicial + variacion
   * - FR-021.09
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
     - BR_008, BR_009, BR_013
   * - **FR Derivados**
     - FR-021.01 a FR-021.09
   * - **Funcion RBAC**
     - RPT-005

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
