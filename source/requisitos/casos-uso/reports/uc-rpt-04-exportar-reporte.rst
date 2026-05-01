.. meta::
 :artefacto: UC_RPT_04
 :tipo: Caso de Uso
 :dominio: requisitos
 :subdominio: reports
 :estado: Aprobado
 :version: 5.0.0
 :fecha_creacion: 2026-01-06
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno
 :normativa: CNST_008, CNST_019, CNST_020, CNST_025

============================
UC_RPT_04: Exportar Reporte
============================

.. note::

 **Consolidado v5.0.0 (Larman):** este UC unifica las antiguas
 ``uc-rpt-04 Exportar CSV``, ``uc-rpt-05 Exportar Excel`` y
 ``uc-rpt-06 Exportar PDF`` en un solo caso de uso "Exportar
 Reporte" con flujos alternativos por formato. Los archivos
 anteriores fueron eliminados (preservados en git history).

 Larman: "Un UC por tipo de operación, NO por formato".

 A nivel RBAC se mantienen las 3 funciones separadas
 (RPT-004/005/006) para SoD por formato. Ver decision D-07
 (WP rbac-modelo-conceptual-cleanup).

1. Resumen
----------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_RPT_04
 * - **Nombre**
   - Exportar Reporte (multi-formato)
 * - **Actor Principal**
   - AGR-004: data_exporter_group
 * - **Modulo**
   - MOD_Reports
 * - **Funciones RBAC**
   - RPT-004 ``export_csv`` (FA-CSV) | RPT-005 ``export_excel`` (FA-Excel) | RPT-006 ``export_pdf`` (FA-PDF) — el sistema valida la función correspondiente al formato seleccionado
 * - **Prioridad**
   - Alta
 * - **Complejidad**
   - Media
 * - **BReq Origen**
   - BRQ-RPT-004

2. Descripcion
--------------

Este caso de uso permite exportar el reporte que el usuario está
viendo actualmente al formato seleccionado (CSV / Excel / PDF).
La exportación respeta CNST-019 (procesamiento asíncrono sobre
umbral) y CNST-020 (throttling anti-abuse por recursos del
sistema).

**Caracteristicas principales:**

- Tres formatos soportados: CSV, Excel, PDF.
- Validación de función RBAC específica al formato (SoD).
- Procesamiento asíncrono cuando excede umbral (CNST-019).
- Throttling anti-abuse por recursos (CNST-020): concurrent
  jobs por usuario, daily quota total, tamaño máximo del
  artefacto generado.
- Filtrado automático por perfil del usuario (AGR) (CNST-008).
- Registro obligatorio en auditoría (CNST-025).
- Notificación de finalización vía buzón interno (CNST-002)
  para exportaciones asíncronas.

**Anti-patrón Larman evitado:**

La versión anterior fragmentaba en 3 UCs por formato
(uc-rpt-04 CSV, uc-rpt-05 Excel, uc-rpt-06 PDF). Larman declara
explícitamente que esto es incorrecto: "Un UC por tipo de
operación, NO por formato. Correcto: UC-601 Generar Reporte
OSHA — puede exportar PDF/Excel/Word. Incorrecto: UC-601a en
PDF, UC-601b en Excel, UC-601c en Word".

3. Diagrama de Caso de Uso
--------------------------

.. uml::
 :caption: Diagrama de Caso de Uso - UC_RPT_04 consolidado

 @startuml
 left to right direction
 actor "AGR-004\ndata_exporter_group" as USER
 actor "Sistema" as SYS

 rectangle "MOD_Reports" {
 usecase "UC_RPT_04\nExportar Reporte" as UC04
 usecase "Validar\nThrottling" as TH
 usecase "Encolar\nJob async" as JOB
 usecase "Generar\nCSV" as CSV
 usecase "Generar\nExcel" as XLSX
 usecase "Generar\nPDF" as PDF
 usecase "Notificar\nBuzon" as NOT
 usecase "Registrar\nAuditoria" as AUD
 }

 USER --> UC04
 UC04 --> TH : include
 UC04 --> JOB : extend [si > umbral CNST-019]
 UC04 ..> CSV : extend [FA-CSV]
 UC04 ..> XLSX : extend [FA-Excel]
 UC04 ..> PDF : extend [FA-PDF]
 UC04 --> AUD : include
 JOB --> NOT
 SYS --> AUD
 @enduml

4. Contexto de Ejecucion
------------------------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Precondición
 * - PRE-01
   - Usuario tiene sesión activa.
 * - PRE-02
   - Usuario tiene asignada al menos UNA de las funciones
     RPT-004/005/006 (la requerida según formato seleccionado).
 * - PRE-03
   - Existe un reporte cargado/filtrado en pantalla con datos
     a exportar.
 * - PRE-04
   - Usuario NO ha excedido throttling vigente (CNST-020).

4.2 Trigger
^^^^^^^^^^^

El usuario hace clic en "Exportar" desde la vista de reporte y
selecciona un formato.

4.3 Postcondiciones (Éxito)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 90
 :header-rows: 1

 * - ID
   - Postcondición
 * - POST-01
   - Si síncrono: usuario recibe descarga del archivo.
 * - POST-02
   - Si asíncrono: usuario recibe ``job_id`` (HTTP 202) y
     posteriormente notificación en buzón con archivo final.
 * - POST-03
   - Acción registrada en auditoría (CNST-025) con: usuario,
     formato, registros, filtros aplicados, modo (sync/async),
     duración total.

5. Flujo Normal (camino feliz)
------------------------------

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Acción
 * - 1
   - Usuario
   - Tiene un reporte filtrado a la vista.
 * - 2
   - Usuario
   - Hace clic en "Exportar" y selecciona formato (CSV / Excel / PDF).
 * - 3
   - Sistema
   - Valida función RBAC correspondiente al formato (RPT-004/005/006).
 * - 4
   - Sistema
   - Aplica filtro de agrupador (CNST-008).
 * - 5
   - Sistema
   - Calcula tamaño estimado de la exportación.
 * - 6
   - Sistema
   - Valida throttling CNST-020 (concurrent + daily quota usuario).
 * - 7
   - Sistema
   - Si registros > umbral CNST-019 → encola job asíncrono y retorna 202 + ``job_id``. Si no → procesa síncronamente.
 * - 8
   - Sistema
   - Genera el artefacto en el formato solicitado (ver flujos alternativos).
 * - 9
   - Sistema
   - Registra acción en auditoría (CNST-025).
 * - 10
   - Sistema
   - Síncrono: retorna archivo. Asíncrono: notifica buzón interno (CNST-002).

6. Flujos Alternativos
----------------------

6.1 FA-CSV: Generar CSV
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Acción
 * - 8a
   - Sistema
   - Valida función RPT-004 ``export_csv``.
 * - 8b
   - Sistema
   - Genera archivo CSV con encoding UTF-8 + BOM.
 * - 8c
   - Sistema
   - Aplana estructura de datos a columnas tabulares.

6.2 FA-Excel: Generar Excel (XLSX)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Acción
 * - 8a
   - Sistema
   - Valida función RPT-005 ``export_excel``.
 * - 8b
   - Sistema
   - Genera archivo Excel (XLSX) con hojas según secciones del reporte.
 * - 8c
   - Sistema
   - Aplica formato condicional y headers de columna.

6.3 FA-PDF: Generar PDF
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 10 20 70
 :header-rows: 1

 * - Paso
   - Actor
   - Acción
 * - 8a
   - Sistema
   - Valida función RPT-006 ``export_pdf``.
 * - 8b
   - Sistema
   - Renderiza el reporte en PDF con layout de página.
 * - 8c
   - Sistema
   - Incluye encabezado con metadatos (fecha, usuario, filtros).

7. Excepciones
--------------

7.1 EX-01: Sin Permiso para el Formato Seleccionado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Paso de origen**
   - 3
 * - **Condición**
   - Usuario no tiene la función RBAC requerida (RPT-004/005/006)
     para el formato seleccionado, aunque sí tenga otros formatos.
 * - **Acción Sistema**
   - Rechaza la exportación con mensaje sugiriendo formatos
     habilitados.
 * - **Mensaje Usuario**
   - "No tiene permiso para exportar a {formato}. Formatos
     disponibles para usted: {lista}."
 * - **Código Error**
   - RPT-040

7.2 EX-02: Throttling Excedido
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Paso de origen**
   - 6
 * - **Condición**
   - Usuario excedió concurrent jobs o daily quota declarado
     en settings (CNST-020).
 * - **Acción Sistema**
   - Rechaza la exportación con HTTP 429.
 * - **Mensaje Usuario**
   - "Demasiados exports activos / Quota diaria excedida. Intente más tarde."
 * - **Código Error**
   - RPT-041

7.3 EX-03: Artefacto Excede Tamaño Máximo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Paso de origen**
   - 8
 * - **Condición**
   - El artefacto generado excede el tamaño máximo declarado en
     settings (CNST-020 — UX, archivos demasiado grandes
     inmanejables).
 * - **Acción Sistema**
   - Rechaza con sugerencia de aplicar más filtros o dividir.
 * - **Mensaje Usuario**
   - "El archivo generado excede el tamaño máximo. Aplique más
     filtros o solicite la exportación en partes."
 * - **Código Error**
   - RPT-042

8. Diagrama de Secuencia
------------------------

.. uml::
 :caption: Diagrama de Secuencia - UC_RPT_04 consolidado

 @startuml
 actor "Usuario" as U
 participant "Frontend" as FE
 participant "ReportController" as RC
 participant "ExportService" as ES
 participant "Throttle" as TH
 queue "AsyncQueue" as Q
 participant "Worker" as W
 participant "InternalMessage" as IM
 participant "UserActionLog" as UAL
 database "DB" as DB

 U -> FE: Click Exportar (formato)
 FE -> RC: POST /api/reports/export\n{format, filters}
 RC -> RC: verify_function(RPT-004/005/006 según formato)
 RC -> ES: prepare_export(filters, format, user)
 ES -> DB: SELECT COUNT(*) FROM ...
 DB --> ES: count
 ES -> TH: check_throttle(user, format)
 alt throttle excedido
 TH --> RC: ThrottleException
 RC --> FE: 429 Too Many Requests
 FE --> U: Error mensaje quota
 end
 alt count > umbral CNST-019
 ES -> Q: enqueue_export_job
 RC --> FE: 202 Accepted + {job_id}
 FE --> U: "Job encolado"
 Q -> W: process_job(format)
 W -> DB: SELECT data
 W -> W: generate_artifact(format)
 W -> IM: notify(user, file)
 W -> UAL: record(EXPORT, format, count)
 IM --> U: Notificación buzón con archivo
 else count <= umbral
 ES -> ES: generate_artifact(format)
 ES -> UAL: record(EXPORT, format, count)
 ES --> RC: file
 RC --> FE: 200 OK + file
 FE --> U: Descarga archivo
 end
 @enduml

9. Reglas de Negocio
--------------------

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - ID
   - Regla
   - Descripción
 * - BR-RPT-40
   - Validación RBAC por formato
   - El sistema valida la función específica al formato (RPT-004 CSV / RPT-005 Excel / RPT-006 PDF) — Larman + SoD
 * - BR-RPT-41
   - Procesamiento async sobre umbral
   - Aplicar CNST-019: si count > umbral, encolar job asíncrono
 * - BR-RPT-42
   - Throttling por recursos
   - Aplicar CNST-020: concurrent + daily quota; tamaño máximo
 * - BR-RPT-43
   - Auditoría obligatoria
   - Toda exportación registrada en CNST-025 con metadatos completos
 * - BR-RPT-44
   - Notificación async
   - Si async, notificar finalización vía buzón interno (CNST-002)

10. Restricciones de Arquitectura
---------------------------------

.. list-table::
 :widths: 15 25 60
 :header-rows: 1

 * - CNST
   - Nombre
   - Aplicación en este UC
 * - CNST_008
   - Agrupadores (AGR)
   - Filtro automático por perfil del usuario (AGR)
 * - CNST_019
   - Async sobre umbral
   - Encolar job si registros > umbral declarado
 * - CNST_020
   - Throttling recursos
   - Concurrent + daily quota; tamaño máximo del artefacto
 * - CNST_025
   - Auditoría
   - Registro obligatorio de cada export

11. Trazabilidad
----------------

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **BReq Origen**
   - BRQ-RPT-004 (consolidado: incluye antiguos BRQ-RPT-005/006)
 * - **Restricciones**
   - CNST_008 (Ventana ETL), CNST-019 v3.0.0 (cola asíncrona abstracta),
     CNST-020 v3.0.0 (throttling abstracto por recursos),
     BR-011 v2.0.0 (límites delegados a CNST), CNST_025 (auditoría)
 * - **UC Relacionados**
   - uc-rpt-01 (Dashboard), uc-rpt-03 (Históricos), uc-rpt-15/16/17 (tipos de reporte específicos)
 * - **UCs eliminados al consolidar**
   - uc-rpt-05 Exportar Excel, uc-rpt-06 Exportar PDF (preservados en git history)
 * - **Clase de Dominio**
   - ``ExportJob`` (primaria), ``Report``, ``AuditEvent`` (per :doc:`/arquitectura-tecnica/modelo-dominio-iact` v1.0.0)
 * - **Funciones RBAC backing**
   - RPT-004 ``export_csv`` | RPT-005 ``export_excel`` | RPT-006 ``export_pdf`` (validación según formato)

12. Historial de Cambios
------------------------

.. list-table::
 :widths: 12 15 25 48
 :header-rows: 1

 * - Versión
   - Fecha
   - Autor
   - Cambios
 * - 4.0.0
   - 2026-01-06
   - Equipo IACT
   - Versión inicial (solo CSV)
 * - 5.0.0
   - 2026-04-30
   - NestorMonroy
   - **Consolidación Larman:** unifica uc-rpt-04 CSV + uc-rpt-05
     Excel + uc-rpt-06 PDF en un solo UC con flujos alternativos
     por formato. RBAC mantiene 3 funciones (RPT-004/005/006)
     para SoD. Alineación con CNST-019/020 v3.0.0 (recursos del
     sistema en lugar de límites por formato). Decision D-07 (WP
     rbac-modelo-conceptual-cleanup).
