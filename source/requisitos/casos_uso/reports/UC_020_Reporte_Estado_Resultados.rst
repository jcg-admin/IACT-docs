.. meta::
   :artefacto: UC_020
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-020:

==============================================================================
UC-020: Generar Reporte Estado de Resultados
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
     - UC-020
   * - **Nombre**
     - Generar Reporte Estado de Resultados
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

Genera el Estado de Resultados (P&L - Profit and Loss) mostrando Ingresos,
Costos, Gastos y Utilidad/Perdida para un periodo. Presenta estructura
con margenes intermedios: Utilidad Bruta, Utilidad Operacional y
Utilidad Neta.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-020 Estado de Resultados
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
       usecase "UC-020:\nEstado de\nResultados" as UC020
       usecase "Seleccionar\nPeriodo" as SP
       usecase "Seleccionar\nNivel" as SN
       usecase "Comparar\nPeriodos" as CP
       usecase "Ver\nPorcentajes" as VP
       usecase "Exportar" as EX
   }

   CNT --> UC020
   GER --> UC020
   UC020 ..> SP : <<include>>
   UC020 ..> SN : <<include>>
   UC020 ..> CP : <<extends>>
   UC020 ..> VP : <<extends>>
   UC020 ..> EX : <<extends>>
   UC020 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion RPT-004 (Generar Estado de Resultados)
2. Usuario tiene segmentos asignados (centros de costo)
3. Existen movimientos de cuentas de resultado para el periodo

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Reportes > Estado de Resultados".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Estado de Resultados generado correctamente
2. Margenes calculados (Bruto, Operacional, Neto)
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
     - Accede a Estado de Resultados
     -
   * - 2
     -
     - Verifica permiso RPT-004
   * - 3
     -
     - Obtiene segmentos del usuario
   * - 4
     -
     - Muestra formulario con opciones
   * - 5
     - Selecciona periodo (mes/trimestre/año)
     -
   * - 6
     - Selecciona nivel de detalle
     -
   * - 7
     - Presiona "Generar Estado"
     -
   * - 8
     -
     - Calcula Ingresos Operacionales
   * - 9
     -
     - Calcula Costos de Venta
   * - 10
     -
     - Calcula Utilidad Bruta
   * - 11
     -
     - Calcula Gastos Operacionales
   * - 12
     -
     - Calcula Utilidad Operacional
   * - 13
     -
     - Calcula Otros Ingresos/Gastos
   * - 14
     -
     - Calcula Utilidad Neta
   * - 15
     -
     - Estructura por categorias
   * - 16
     -
     - Muestra Estado de Resultados
   * - 17
     -
     - Registra REPORT_GENERATED (BR_008)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-020 Estado de Resultados
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   actor "Contador" as U
   participant "Frontend" as FE #E3F2FD
   participant "ReportController" as RC #E8F5E9
   participant "PLService" as PL #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Estado de Resultados
   FE -> RC: 2. GET /api/reports/pl/options
   RC --> FE: 3. {periodos, niveles}

   FE --> U: 4. Formulario de opciones

   U -> FE: 5. Selecciona periodo y genera
   FE -> RC: 6. POST /api/reports/pl\n{periodo, nivel, segments}
   activate RC

   RC -> PL: 7. generatePL(periodo, nivel, segments)
   activate PL

   PL -> DB: 8. SELECT SUM(credito-debito)\nFROM movimientos\nWHERE cuenta LIKE '4%'\nAND periodo = ?\nAND centro IN (segments)
   note right: Cuentas 4xxx = Ingresos
   DB --> PL: {ingresos}

   PL -> DB: 9. SELECT SUM(debito-credito)\nWHERE cuenta LIKE '6%'
   note right: Cuentas 6xxx = Costos
   DB --> PL: {costos}

   PL -> PL: 10. utilidadBruta = ingresos - costos

   PL -> DB: 11. SELECT SUM(debito-credito)\nWHERE cuenta LIKE '5%'
   note right: Cuentas 5xxx = Gastos
   DB --> PL: {gastos}

   PL -> PL: 12. utilidadOper = utilidadBruta - gastos

   PL -> DB: 13. Query otros ingresos/gastos
   DB --> PL: {otros}

   PL -> PL: 14. utilidadNeta = utilidadOper + otros

   PL -> PL: 15. buildStructure(nivel)

   PL -> AUD: 16. logEvent(REPORT_GENERATED,\n{type: 'ESTADO_RESULTADOS'})
   AUD -> DB: INSERT audit_log

   PL --> RC: 17. {ingresos, costos, gastos,\nmargenes, utilidadNeta}
   deactivate PL

   RC --> FE: 18. 200 OK {estadoResultados}
   deactivate RC

   FE --> U: 19. Muestra Estado de Resultados
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Mostrar Porcentajes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario activa "Ver como % de Ingresos"

Muestra cada linea como porcentaje de los ingresos totales.

7.2 FA-2: Comparativo Mensual
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario selecciona comparar multiples meses

Genera columnas para cada mes con variaciones.

7.3 FA-3: Periodo con Perdida
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Utilidad Neta es negativa

Sistema muestra en rojo con indicador "(Perdida)".

----

8. Excepciones
--------------

8.1 EX-1: Sin Movimientos en Periodo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay movimientos de resultado para el periodo"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-020 Estado de Resultados
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
   :Accede a Estado de Resultados;
   :Verificar permiso RPT-004;

   if (Tiene permiso?) then (si)
       :Obtener segmentos usuario;
       :Mostrar opciones;
       :Usuario selecciona periodo;

       if (Comparativo?) then (si)
           :Seleccionar periodos a comparar;
       else (no)
       endif

       :Calcular Ingresos Operacionales;
       :Calcular Costos de Venta;
       :Utilidad Bruta = Ingresos - Costos;

       :Calcular Gastos Operacionales;
       :Utilidad Operacional = U.Bruta - Gastos;

       :Calcular Otros Ingresos/Gastos;
       :Utilidad Neta = U.Oper +/- Otros;

       if (Utilidad >= 0?) then (si)
           #C8E6C9:Mostrar Utilidad;
       else (no)
           #FFCDD2:Mostrar Perdida (rojo);
       endif

       :Estructurar por categorias;

       if (Ver porcentajes?) then (si)
           :Calcular % sobre ingresos;
       else (no)
       endif

       :Mostrar Estado de Resultados;
       #C8E6C9:Registrar auditoria (BR_008);

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
   * - BR_012
     - Estructura P&L
     - Ingresos - Costos - Gastos = Utilidad

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-020.01
     - Verificar permiso RPT-004
   * - FR-020.02
     - Aplicar segmentacion (BR_009)
   * - FR-020.03
     - Calcular Ingresos Operacionales
   * - FR-020.04
     - Calcular Costos de Venta
   * - FR-020.05
     - Calcular Utilidad Bruta
   * - FR-020.06
     - Calcular Gastos Operacionales
   * - FR-020.07
     - Calcular Utilidad Operacional
   * - FR-020.08
     - Calcular Utilidad Neta
   * - FR-020.09
     - Mostrar porcentajes sobre ingresos
   * - FR-020.10
     - Permitir comparativo de periodos
   * - FR-020.11
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
     - BR_008, BR_009, BR_012
   * - **FR Derivados**
     - FR-020.01 a FR-020.11
   * - **UC Relacionados**
     - UC-019 (Balance), UC-023 (Comparativo)
   * - **Funcion RBAC**
     - RPT-004

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