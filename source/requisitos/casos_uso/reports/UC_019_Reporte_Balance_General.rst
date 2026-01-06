.. meta::
   :artefacto: UC_019
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-019:

==============================================================================
UC-019: Generar Reporte Balance General
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
     - UC-019
   * - **Nombre**
     - Generar Reporte Balance General
   * - **Actor Primario**
     - Contador / Gerente Financiero
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Reports
   * - **Complejidad**
     - Alta
   * - **Prioridad**
     - Critica
   * - **BReq Origen**
     - BReq-002: Generacion de Reportes

----

2. Descripcion
--------------

Genera el Balance General (Estado de Situacion Financiera) mostrando
Activos, Pasivos y Patrimonio a una fecha de corte. Presenta estructura
jerarquica de cuentas con subtotales por categoria y totales que cumplen
la ecuacion contable: Activo = Pasivo + Patrimonio.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-019 Balance General
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
   actor "Gerente\nFinanciero" as GER
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Reports" {
       usecase "UC-019:\nBalance\nGeneral" as UC019
       usecase "Seleccionar\nFecha Corte" as SFC
       usecase "Seleccionar\nNivel Detalle" as SND
       usecase "Comparar\nPeriodos" as CP
       usecase "Exportar" as EX
   }

   CNT --> UC019
   GER --> UC019
   UC019 ..> SFC : <<include>>
   UC019 ..> SND : <<include>>
   UC019 ..> CP : <<extends>>
   UC019 ..> EX : <<extends>>
   UC019 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion RPT-003 (Generar Balance General)
2. Usuario tiene segmentos asignados (centros de costo)
3. Existe cierre contable para el periodo o datos provisionales

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Reportes > Balance General".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Balance General generado con estructura correcta
2. Ecuacion contable verificada (Activo = Pasivo + Patrimonio)
3. Evento REPORT_GENERATED registrado (BR_008)
4. Solo muestra datos de centros del usuario (BR_009)

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
     - Accede a Balance General
     -
   * - 2
     -
     - Verifica permiso RPT-003
   * - 3
     -
     - Obtiene segmentos del usuario
   * - 4
     -
     - Muestra formulario con opciones
   * - 5
     - Selecciona fecha de corte
     -
   * - 6
     - Selecciona nivel de detalle
     -
   * - 7
     - Presiona "Generar Balance"
     -
   * - 8
     -
     - Calcula saldos de cuentas de Activo
   * - 9
     -
     - Calcula saldos de cuentas de Pasivo
   * - 10
     -
     - Calcula saldos de Patrimonio
   * - 11
     -
     - Verifica ecuacion contable
   * - 12
     -
     - Estructura jerarquicamente por categoria
   * - 13
     -
     - Muestra Balance General
   * - 14
     -
     - Registra REPORT_GENERATED (BR_008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-019 Balance General
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Contador" as U
   participant "Frontend" as FE #E3F2FD
   participant "ReportController" as RC #E8F5E9
   participant "BalanceService" as BS #E8F5E9
   participant "AccountService" as AS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Balance General
   FE -> RC: 2. GET /api/reports/balance/options
   activate RC
   RC --> FE: 3. {fechas, niveles}
   deactivate RC

   FE --> U: 4. Formulario de opciones

   U -> FE: 5. Selecciona fecha y nivel
   U -> FE: 6. Generar Balance
   FE -> RC: 7. POST /api/reports/balance\n{fechaCorte, nivel, segments}
   activate RC

   RC -> BS: 8. generateBalance(fecha, nivel, segments)
   activate BS

   BS -> AS: 9. getAccountsByType('ACTIVO')
   AS -> DB: SELECT * FROM cuentas\nWHERE tipo='ACTIVO'
   AS --> BS: [cuentasActivo]

   BS -> DB: 10. SELECT cuenta, SUM(debito-credito) as saldo\nFROM movimientos\nWHERE fecha <= fechaCorte\nAND centro_costo IN (segments)\nAND cuenta IN (activos)\nGROUP BY cuenta
   DB --> BS: [saldosActivo]

   BS -> AS: 11. getAccountsByType('PASIVO')
   BS -> DB: 12. Query saldos pasivo
   DB --> BS: [saldosPasivo]

   BS -> AS: 13. getAccountsByType('PATRIMONIO')
   BS -> DB: 14. Query saldos patrimonio
   DB --> BS: [saldosPatrimonio]

   BS -> BS: 15. validateEquation()
   note right: Activo = Pasivo + Patrimonio

   BS -> BS: 16. buildHierarchy(nivel)
   note right: Estructura por\ncategorias y subcuentas

   BS -> AUD: 17. logEvent(REPORT_GENERATED,\n{type: 'BALANCE_GENERAL'})
   AUD -> DB: INSERT audit_log

   BS --> RC: 18. {activo, pasivo, patrimonio, totals}
   deactivate BS

   RC --> FE: 19. 200 OK {balance}
   deactivate RC

   FE --> U: 20. Muestra Balance General estructurado
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Comparar con Periodo Anterior
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 5 del flujo normal

**Condicion:** Usuario activa "Comparar con periodo anterior"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 5.1
     - Usuario activa checkbox "Comparativo"
   * - 5.2
     - Selecciona fecha de periodo anterior
   * - 5.3
     - Sistema genera balance para ambas fechas
   * - 5.4
     - Muestra variacion absoluta y porcentual

**Retorno:** Paso 13 con columnas comparativas

7.2 FA-2: Descuadre en Ecuacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 11 del flujo normal

**Condicion:** Activo != Pasivo + Patrimonio

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 11.1
     - Sistema detecta diferencia
   * - 11.2
     - Muestra advertencia con monto de diferencia
   * - 11.3
     - Sugiere revision de cuentas de ajuste
   * - 11.4
     - Genera reporte con marca de "provisional"

**Retorno:** Paso 12 con advertencia visible

----

8. Excepciones
--------------

8.1 EX-1: Sin Datos para Fecha
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** No hay movimientos hasta la fecha de corte

**Mensaje:** "No hay datos contables para la fecha seleccionada"

8.2 EX-2: Fecha Futura
^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Fecha de corte es posterior a hoy

**Mensaje:** "La fecha de corte no puede ser futura"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-019 Balance General
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
   :Accede a Balance General;
   :Verificar permiso RPT-003;

   if (Tiene permiso?) then (si)
       :Obtener segmentos usuario;
       :Mostrar opciones;
       :Usuario selecciona fecha corte;
       :Usuario selecciona nivel detalle;

       if (Comparativo?) then (si)
           :Seleccionar fecha anterior;
       else (no)
       endif

       fork
           :Calcular saldos ACTIVO;
       fork again
           :Calcular saldos PASIVO;
       fork again
           :Calcular saldos PATRIMONIO;
       end fork

       :Verificar ecuacion contable;

       if (Activo = Pasivo + Patrimonio?) then (si)
           #C8E6C9:Ecuacion verificada;
       else (no)
           #FFE0B2:Advertencia: descuadre;
           :Marcar como provisional;
       endif

       :Estructurar jerarquicamente;
       :Mostrar Balance General;
       #C8E6C9:Registrar auditoria (BR_008);

       if (Exportar?) then (si)
           fork
               :Exportar Excel;
           fork again
               :Exportar PDF;
           end fork
       else (no)
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
     - Aplicacion en este UC
   * - BR_008
     - Auditoria
     - Generacion de balance registrada
   * - BR_009
     - Segmentacion
     - Solo datos de centros asignados al usuario
   * - BR_011
     - Ecuacion Contable
     - Activo debe ser igual a Pasivo + Patrimonio

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-019.01
     - Sistema DEBE verificar permiso RPT-003
   * - FR-019.02
     - Sistema DEBE aplicar segmentacion (BR_009)
   * - FR-019.03
     - Sistema DEBE permitir seleccionar fecha de corte
   * - FR-019.04
     - Sistema DEBE calcular saldos de Activo
   * - FR-019.05
     - Sistema DEBE calcular saldos de Pasivo
   * - FR-019.06
     - Sistema DEBE calcular saldos de Patrimonio
   * - FR-019.07
     - Sistema DEBE verificar ecuacion contable
   * - FR-019.08
     - Sistema DEBE estructurar por niveles jerarquicos
   * - FR-019.09
     - Sistema DEBE permitir comparativo con periodo anterior
   * - FR-019.10
     - Sistema DEBE exportar a Excel y PDF
   * - FR-019.11
     - Sistema DEBE registrar en auditoria (BR_008)

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-002: Generacion de Reportes
   * - **BR Aplicables**
     - BR_008, BR_009, BR_011
   * - **FR Derivados**
     - FR-019.01 a FR-019.11 (11 requerimientos)
   * - **UC Relacionados**
     - UC-020 (Estado Resultados), UC-023 (Comparativo)
   * - **Funcion RBAC**
     - RPT-003: Generar Balance General

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
     - Version con PlantUML embebido. 3 diagramas completos.