.. meta::
   :artefacto: UC_025
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-025:

==============================================================================
UC-025: Generar Reporte Antiguedad de Saldos
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
     - UC-025
   * - **Nombre**
     - Generar Reporte Antiguedad de Saldos
   * - **Actor Primario**
     - Analista de Cartera / Tesorero
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

Genera reporte de antiguedad de saldos clasificando las cuentas por cobrar
o por pagar en rangos de tiempo: corriente (0-30 dias), 31-60 dias,
61-90 dias y mayor a 90 dias. Permite identificar cartera vencida y
gestionar cobranza o pagos.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-025 Antiguedad Saldos
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

   actor "Analista\nCartera" as ANA
   actor "Tesorero" as TES

   rectangle "MOD_Reports" {
       usecase "UC-025:\nAntiguedad\nSaldos" as UC025
       usecase "Seleccionar\nTipo" as ST
       usecase "Clasificar\npor Rangos" as CR
       usecase "Ver\nDetalle" as VD
       usecase "Exportar" as EX
   }

   ANA --> UC025
   TES --> UC025
   UC025 ..> ST : <<include>>
   UC025 ..> CR : <<include>>
   UC025 ..> VD : <<extends>>
   UC025 ..> EX : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion RPT-009 (Antiguedad Saldos)
2. Existen documentos pendientes en el sistema
3. Usuario tiene segmentos asignados

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Reportes > Antiguedad de Saldos".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Reporte generado con clasificacion por rangos
2. Totales por rango calculados
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
     - Accede a Antiguedad de Saldos
     -
   * - 2
     -
     - Verifica permiso RPT-009
   * - 3
     -
     - Muestra opciones de tipo
   * - 4
     - Selecciona tipo (CxC o CxP)
     -
   * - 5
     - Selecciona fecha de corte
     -
   * - 6
     - Presiona "Generar Reporte"
     -
   * - 7
     -
     - Obtiene documentos pendientes
   * - 8
     -
     - Calcula dias de antiguedad
   * - 9
     -
     - Clasifica en rangos
   * - 10
     -
     - Suma totales por rango
   * - 11
     -
     - Muestra reporte con matriz
   * - 12
     -
     - Registra en auditoria

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-025 Antiguedad Saldos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   actor "Analista" as U
   participant "Frontend" as FE #E3F2FD
   participant "ReportController" as RC #E8F5E9
   participant "AgingService" as AS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a Antiguedad
   FE -> RC: 2. GET /api/reports/aging/options
   RC --> FE: 3. {tipos}
   FE --> U: 4. Formulario

   U -> FE: 5. Selecciona CxC y fecha
   FE -> RC: 6. POST /api/reports/aging\n{tipo: 'CXC', fechaCorte}
   activate RC

   RC -> AS: 7. generateAging(params)
   activate AS

   AS -> DB: 8. SELECT tercero, documento,\nfecha_vencimiento, saldo\nFROM documentos_pendientes\nWHERE tipo = 'CXC'\nAND centro IN (segments)
   DB --> AS: [documentos]

   loop Por cada documento
       AS -> AS: 9. dias = fechaCorte - fecha_vencimiento

       AS -> AS: 10. clasificar(dias)
       note right: 0-30: Corriente\n31-60: Vencido 1\n61-90: Vencido 2\n>90: Vencido 3
   end

   AS -> AS: 11. sumarPorRango()
   AS -> AS: 12. sumarPorTercero()

   AS -> AUD: 13. logEvent(REPORT_GENERATED)
   AUD -> DB: INSERT audit_log

   AS --> RC: 14. {matriz, totales}
   deactivate AS

   RC --> FE: 15. 200 OK
   deactivate RC
   FE --> U: 16. Matriz de antiguedad
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Ver Detalle por Tercero
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario hace clic en un tercero

Expande mostrando todos los documentos del tercero.

7.2 FA-2: Cuentas por Pagar
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario selecciona tipo CxP

Genera antiguedad de cuentas por pagar a proveedores.

7.3 FA-3: Rangos Personalizados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario modifica rangos

Permite definir rangos diferentes (ej: 0-15, 16-30, etc).

----

8. Excepciones
--------------

8.1 EX-1: Sin Documentos Pendientes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay documentos pendientes del tipo seleccionado"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-025 Antiguedad Saldos
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Verificar permiso RPT-009;
   :Usuario selecciona tipo (CxC/CxP);
   :Usuario selecciona fecha corte;
   :Obtener documentos pendientes;

   if (Hay documentos?) then (si)
       while (Por cada documento) is (siguiente)
           :Calcular dias antiguedad;

           if (dias <= 30?) then (si)
               :Rango: Corriente;
           elseif (dias <= 60?) then (si)
               :Rango: 31-60;
           elseif (dias <= 90?) then (si)
               :Rango: 61-90;
           else (>90)
               :Rango: >90 dias;
           endif
       endwhile (fin)

       :Sumar por rango;
       :Sumar por tercero;
       :Generar matriz;
       :Mostrar reporte;
       #C8E6C9:Registrar auditoria;
   else (no)
       #FFE0B2:Sin documentos;
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
   * - BR_017
     - Rangos Antiguedad
     - 0-30, 31-60, 61-90, >90 dias

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-025.01
     - Verificar permiso RPT-009
   * - FR-025.02
     - Aplicar segmentacion (BR_009)
   * - FR-025.03
     - Permitir seleccionar CxC o CxP
   * - FR-025.04
     - Calcular dias de antiguedad
   * - FR-025.05
     - Clasificar en rangos estandar
   * - FR-025.06
     - Permitir rangos personalizados
   * - FR-025.07
     - Mostrar matriz tercero vs rangos
   * - FR-025.08
     - Permitir ver detalle por tercero
   * - FR-025.09
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
     - BR_008, BR_009, BR_017
   * - **FR Derivados**
     - FR-025.01 a FR-025.09
   * - **Funcion RBAC**
     - RPT-009

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