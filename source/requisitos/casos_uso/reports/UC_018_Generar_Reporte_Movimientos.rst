.. meta::
   :artefacto: UC_018
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-018:

==============================================================================
UC-018: Generar Reporte de Movimientos
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
     - UC-018
   * - **Nombre**
     - Generar Reporte de Movimientos
   * - **Actor Primario**
     - Analista Contable
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

Genera reporte detallado de movimientos contables mostrando cada transaccion
con fecha, numero de documento, cuenta, descripcion, debito, credito y saldo
acumulado. Permite filtros por periodo, cuenta, centro de costo y tipo de
movimiento. Aplica segmentacion segun centros asignados al usuario (BR_009).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-018 Reporte Movimientos
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
       usecase "UC-018:\nReporte\nMovimientos" as UC018
       usecase "Filtrar\nPeriodo" as FP
       usecase "Filtrar\nCuenta" as FC
       usecase "Filtrar\nTipo" as FT
       usecase "Exportar\nExcel/PDF" as EX
       usecase "Aplicar\nSegmentacion" as AS
   }

   ANA --> UC018
   GER --> UC018
   UC018 ..> FP : <<include>>
   UC018 ..> FC : <<include>>
   UC018 ..> FT : <<include>>
   UC018 ..> AS : <<include>>
   UC018 ..> EX : <<extends>>
   UC018 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion RPT-002 (Generar Reporte Movimientos)
2. Usuario tiene segmentos asignados (centros de costo)
3. Existen movimientos contables en el sistema

4.2 Trigger
^^^^^^^^^^^

Usuario accede a "Reportes > Movimientos Contables".

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Reporte generado con movimientos filtrados
2. Saldo acumulado calculado correctamente
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
     - Accede a Reporte de Movimientos
     - 
   * - 2
     - 
     - Verifica permiso RPT-002
   * - 3
     - 
     - Obtiene segmentos del usuario
   * - 4
     - 
     - Carga opciones de filtros
   * - 5
     - 
     - Muestra formulario de filtros
   * - 6
     - Selecciona periodo (fecha desde/hasta)
     - 
   * - 7
     - (Opcional) Selecciona cuenta especifica
     - 
   * - 8
     - (Opcional) Selecciona tipo movimiento
     - 
   * - 9
     - Presiona "Generar Reporte"
     - 
   * - 10
     - 
     - Ejecuta query con segmentacion
   * - 11
     - 
     - Calcula saldo acumulado por linea
   * - 12
     - 
     - Muestra reporte paginado
   * - 13
     - 
     - Registra REPORT_GENERATED (BR_008)
   * - 14
     - (Opcional) Exporta a Excel/PDF
     - 

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-018 Reporte Movimientos
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

   U -> FE: 1. Accede a Reporte Movimientos
   FE -> RC: 2. GET /api/reports/movimientos/filters
   activate RC
   
   RC -> SS: 3. getUserSegments(userId)
   SS -> DB: SELECT segment_id FROM user_segments
   SS --> RC: [segments]
   
   RC -> DB: 4. SELECT DISTINCT cuenta FROM movimientos
   DB --> RC: [cuentas]
   
   RC --> FE: 5. {periodos, cuentas, tipos, segments}
   deactivate RC
   
   FE --> U: 6. Formulario de filtros

   U -> FE: 7. Configura filtros y genera
   FE -> RC: 8. POST /api/reports/movimientos\n{fechaDesde, fechaHasta, cuenta, tipo}
   activate RC

   RC -> RS: 9. generateMovimientos(filters, segments)
   activate RS

   RS -> DB: 10. SELECT fecha, documento, cuenta,\ndescripcion, debito, credito\nFROM movimientos\nWHERE fecha BETWEEN ? AND ?\nAND centro_costo IN (segments)\nORDER BY fecha, id
   note right: BR_009:\nSegmentacion aplicada
   DB --> RS: [movimientos]

   RS -> RS: 11. calculateRunningBalance()
   note right: Calcula saldo\nacumulado por linea

   RS -> AUD: 12. logEvent(REPORT_GENERATED,\n{type: 'MOVIMIENTOS', filters})
   AUD -> DB: INSERT audit_log

   RS --> RC: 13. {movimientos, totals, count}
   deactivate RS

   RC --> FE: 14. 200 OK {report}
   deactivate RC

   FE --> U: 15. Tabla de movimientos paginada

   opt Exportar
       U -> FE: 16. Clic "Exportar Excel"
       FE -> RC: 17. GET /api/reports/movimientos/export\n?format=xlsx&filters=...
       RC -> RS: generateExcel(data)
       RS --> RC: {file}
       RC --> FE: 18. Binary file
       FE --> U: 19. Descarga archivo
   end
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Sin Movimientos para Filtros
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 10 del flujo normal

**Condicion:** No hay movimientos que cumplan los filtros

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 10.1
     - Sistema detecta resultado vacio
   * - 10.2
     - Muestra mensaje "Sin movimientos para los filtros seleccionados"
   * - 10.3
     - Sugiere ampliar rango de fechas

**Retorno:** Usuario puede modificar filtros

7.2 FA-2: Exportar a PDF
^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 14 del flujo normal

**Condicion:** Usuario selecciona formato PDF

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 14.1
     - Usuario selecciona "Exportar PDF"
   * - 14.2
     - Sistema genera PDF con formato formal
   * - 14.3
     - Incluye encabezado con empresa y fecha
   * - 14.4
     - Descarga archivo PDF

**Retorno:** Fin del caso de uso

7.3 FA-3: Muchos Registros
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Resultado excede 10,000 registros

**Accion:** Sistema muestra advertencia y sugiere exportar directamente

----

8. Excepciones
--------------

8.1 EX-1: Sin Segmentos Asignados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario no tiene centros de costo asignados

**Accion del Sistema:** Retorna error

**Mensaje al Usuario:** "No tiene centros de costo asignados. Contacte al administrador."

8.2 EX-2: Rango de Fechas Invalido
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Fecha desde mayor que fecha hasta

**Accion del Sistema:** Retorna error de validacion

**Mensaje al Usuario:** "La fecha inicial no puede ser mayor a la fecha final"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-018 Reporte Movimientos
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
   :Accede a Reporte Movimientos;
   :Verificar permiso RPT-002;
   
   if (Tiene permiso?) then (si)
       :Obtener segmentos usuario;
       
       if (Tiene segmentos?) then (si)
           :Cargar opciones filtros;
           :Mostrar formulario;
           :Usuario configura filtros;
           
           :Validar fechas;
           
           if (Fechas validas?) then (si)
               :Ejecutar query con segmentacion\n(BR_009);
               
               if (Hay resultados?) then (si)
                   
                   if (Mas de 10,000?) then (si)
                       #FFE0B2:Advertencia: muchos registros;
                       :Sugerir exportar;
                   else (no)
                   endif
                   
                   :Calcular saldo acumulado;
                   :Mostrar reporte paginado;
                   #C8E6C9:Registrar auditoria (BR_008);
                   
                   if (Exportar?) then (si)
                       fork
                           :Exportar Excel;
                       fork again
                           :Exportar PDF;
                       end fork
                       :Descargar archivo;
                   else (no)
                   endif
                   
               else (no)
                   #FFE0B2:Sin datos para filtros;
               endif
           else (no)
               #FFCDD2:Error: fechas invalidas;
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
     - Aplicacion en este UC
   * - BR_008
     - Auditoria
     - Generacion de reporte registrada con filtros usados
   * - BR_009
     - Segmentacion
     - Solo muestra movimientos de centros asignados al usuario

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-018.01
     - Sistema DEBE verificar permiso RPT-002
   * - FR-018.02
     - Sistema DEBE aplicar segmentacion por centro de costo (BR_009)
   * - FR-018.03
     - Sistema DEBE permitir filtrar por rango de fechas
   * - FR-018.04
     - Sistema DEBE permitir filtrar por cuenta contable
   * - FR-018.05
     - Sistema DEBE permitir filtrar por tipo de movimiento
   * - FR-018.06
     - Sistema DEBE mostrar: fecha, documento, cuenta, descripcion, debito, credito
   * - FR-018.07
     - Sistema DEBE calcular y mostrar saldo acumulado por linea
   * - FR-018.08
     - Sistema DEBE paginar resultados (50 por pagina)
   * - FR-018.09
     - Sistema DEBE exportar a Excel con formato
   * - FR-018.10
     - Sistema DEBE exportar a PDF con encabezado formal
   * - FR-018.11
     - Sistema DEBE registrar generacion en auditoria (BR_008)

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-002: Generacion de Reportes
   * - **BR Aplicables**
     - BR_008 (Auditoria), BR_009 (Segmentacion)
   * - **FR Derivados**
     - FR-018.01 a FR-018.11 (11 requerimientos)
   * - **UC Relacionados**
     - UC-017 (Saldos), UC-022 (Analisis Cuentas)
   * - **Funcion RBAC**
     - RPT-002: Generar Reporte Movimientos

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
     - Version con PlantUML embebido (Sphinx). 3 diagramas completos.
