.. meta::
   :artefacto: UC_030
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/reports
   :modulo: MOD_Reports
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-030:

==============================================================================
UC-030: Exportar Dashboard
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
     - UC-030
   * - **Nombre**
     - Exportar Dashboard
   * - **Actor Primario**
     - Usuario autenticado
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Reports
   * - **Complejidad**
     - Baja
   * - **Prioridad**
     - Baja
   * - **BReq Origen**
     - BReq-003: Visualizacion de Indicadores

----

2. Descripcion
--------------

Permite exportar el dashboard actual a formato PDF o imagen (PNG) para
uso en presentaciones, reportes ejecutivos o archivo. Captura todos
los widgets visibles con sus graficos y datos actuales.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-030 Exportar Dashboard
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

   actor "Usuario" as USR

   rectangle "MOD_Reports" {
       usecase "UC-030:\nExportar\nDashboard" as UC030
       usecase "Exportar\nPDF" as EP
       usecase "Exportar\nImagen" as EI
       usecase "Programar\nEnvio" as PE
   }

   USR --> UC030
   UC030 ..> EP : <<extends>>
   UC030 ..> EI : <<extends>>
   UC030 ..> PE : <<extends>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene funcion DSH-005 (Exportar Dashboard)
2. Dashboard renderizado con datos

4.2 Trigger
^^^^^^^^^^^

Usuario hace clic en "Exportar" en cualquier dashboard.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Archivo generado y descargado
2. Evento DASHBOARD_EXPORTED registrado

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
     - Hace clic en "Exportar"
     -
   * - 2
     -
     - Verifica permiso DSH-005
   * - 3
     -
     - Muestra opciones de formato
   * - 4
     - Selecciona formato (PDF/PNG)
     -
   * - 5
     - (Opcional) Configura opciones
     -
   * - 6
     - Presiona "Exportar"
     -
   * - 7
     -
     - Captura estado actual del dashboard
   * - 8
     -
     - Genera archivo en formato seleccionado
   * - 9
     -
     - Registra en auditoria
   * - 10
     -
     - Inicia descarga del archivo

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-030 Exportar Dashboard
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   actor "Usuario" as U
   participant "Frontend" as FE #E3F2FD
   participant "DashboardController" as DC #E8F5E9
   participant "ExportService" as ES #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Clic "Exportar"
   FE --> U: 2. Muestra opciones

   U -> FE: 3. Selecciona PDF
   U -> FE: 4. Clic "Exportar"

   FE -> FE: 5. Captura DOM del dashboard
   note right: html2canvas\no similar

   FE -> DC: 6. POST /api/dashboard/export\n{format: 'PDF', image: base64}
   activate DC

   DC -> ES: 7. generatePDF(imageData)
   activate ES
   ES -> ES: 8. Crear documento PDF
   ES -> ES: 9. Insertar imagen
   ES -> ES: 10. Agregar metadata\n(fecha, usuario)
   ES --> DC: {pdfBuffer}
   deactivate ES

   DC -> AUD: 11. logEvent(DASHBOARD_EXPORTED)
   AUD -> DB: INSERT audit_log

   DC --> FE: 12. Binary PDF
   deactivate DC

   FE --> U: 13. Descarga archivo.pdf
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Exportar como Imagen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario selecciona PNG

Sistema genera imagen PNG directamente sin convertir a PDF.

7.2 FA-2: Programar Envio por Email
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario activa "Enviar por email"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 7.2.1
     - Usuario ingresa destinatarios
   * - 7.2.2
     - Usuario configura frecuencia (unica/recurrente)
   * - 7.2.3
     - Sistema programa envio
   * - 7.2.4
     - Sistema genera y envia en horario configurado

----

8. Excepciones
--------------

8.1 EX-1: Dashboard Vacio
^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "No hay datos para exportar en el dashboard"

8.2 EX-2: Error de Generacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Mensaje:** "Error al generar el archivo. Intente nuevamente."

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-030 Exportar Dashboard
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Clic "Exportar";
   :Verificar permiso DSH-005;
   :Mostrar opciones;
   :Usuario selecciona formato;

   if (Enviar por email?) then (si)
       :Configurar destinatarios;
       :Configurar frecuencia;
       :Programar envio;
   else (no)
   endif

   :Capturar dashboard;

   if (Formato PDF?) then (si)
       :Generar PDF;
       :Agregar metadata;
   else (PNG)
       :Generar imagen;
   endif

   #C8E6C9:Registrar auditoria;
   :Descargar archivo;
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
     - Exportacion registrada con formato y destino

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-030.01
     - Verificar permiso DSH-005
   * - FR-030.02
     - Capturar estado actual del dashboard
   * - FR-030.03
     - Exportar a formato PDF
   * - FR-030.04
     - Exportar a formato PNG
   * - FR-030.05
     - Incluir metadata (fecha, usuario, periodo)
   * - FR-030.06
     - Permitir envio por email
   * - FR-030.07
     - Permitir programar envio recurrente
   * - FR-030.08
     - Registrar exportacion en auditoria

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-003
   * - **BR Aplicables**
     - BR_008
   * - **FR Derivados**
     - FR-030.01 a FR-030.08
   * - **Funcion RBAC**
     - DSH-005

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