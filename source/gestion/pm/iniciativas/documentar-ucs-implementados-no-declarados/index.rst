.. meta::
   :artefacto: INICIATIVA-DOCUMENTAR-UCS-IMPLEMENTADOS-NO-DECLARADOS
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:50:00
   :ultimo_cambio: 2026-05-19T21:50:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-documentar-ucs-implementados-no-declarados:

==============================================================
Iniciativa: Documentar UCs Implementados No Declarados
==============================================================

P2 del plan maestro #9. Cierra la deuda documental inversa
identificada en
``verificar-mapping-docs-codigo-todos-los-dominios``: **5
markers UC en codigo api sin contraparte RST en docs**.

UCs documentados retroactivamente
==================================

.. list-table::
   :header-rows: 1
   :widths: 12 14 35 39

   * - UC docs
     - Marker código
     - Nombre
     - Dominio
   * - UC-078
     - UC_ACC_03
     - Consultar Permisos Efectivos del
       Usuario
     - access
   * - UC-079
     - UC_ACC_04
     - Asignar Agrupador a Usuario
     - access
   * - UC-080
     - UC_ACC_05
     - Gestionar Reglas de Separación de
       Funciones
     - access
   * - UC-081
     - UC_LOG_08
     - Ver Eventos del Pipeline Analítico
     - logs
   * - UC-082
     - UC_PIP_05
     - Gestionar Configuración del Job ETL
     - pipeline

Numeración continúa tras supervision OUT (uc-075..077). Los
RST creados son **minimum-viable**: identificación, marker
en código, especificación breve, trazabilidad con
TST-fr-NNN-XX pendiente. Los FR detallados se desarrollarán
en iniciativas hermanas si el sponsor lo prioriza.

Fuera de scope: 3 markers UI ``UC_USR_05/06/07`` sin
descripción textual en código UI. Requieren inspección del
src/ para determinar feature representada. Diferidos a
iniciativa ``alinear-numeracion-uc-api-ui`` del plan maestro
(#11).

.. toctree::
   :maxdepth: 1

   tareas-y-progreso-documentar-ucs-implementados-no-declarados
