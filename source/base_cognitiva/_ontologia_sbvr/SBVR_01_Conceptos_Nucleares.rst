.. meta::
   :artefacto: SBVR_01
   :tipo: Ontologia
   :dominio: base_cognitiva
   :subdominio: _ontologia_sbvr
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2025-12-18
   :ultimo_cambio: 2025-12-18
   :autor: Business Analyst Lead
   :clasificacion: Interno

.. _sbvr_01_conceptos_nucleares:

==========================================================
SBVR_01 · Conceptos Nucleares
==========================================================

.. contents:: Contenido
   :local:
   :depth: 2

------------------------------------------------------------
1. Propósito
------------------------------------------------------------

Este documento define los conceptos fundamentales del dominio IACT utilizando
la notación SBVR (Semantics of Business Vocabulary and Business Rules).
Constituye el vocabulario base para toda regla de negocio del sistema.

------------------------------------------------------------
2. Notación SBVR Utilizada
------------------------------------------------------------

Cada concepto se documenta con la siguiente estructura:

- **Término:** Nombre del concepto (sustantivo o frase nominal)
- **Definición:** Significado preciso en el contexto IACT
- **Sinónimos:** Términos alternativos aceptados
- **Tipo:** Clasificación (Entidad, Actor, Objeto, Evento, Estado)
- **Relaciones:** Conexiones con otros conceptos (fact types)

Convenciones tipográficas:

- ``término`` — concepto definido en este vocabulario
- *cursiva* — término técnico externo
- **negrita** — énfasis

------------------------------------------------------------
3. Conceptos de Actores
------------------------------------------------------------

3.1. Usuario
^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Usuario
   * - **Definición**
     - Persona autenticada que interactúa con el ``Sistema IACT`` a través
       de una interfaz de usuario. Cada Usuario tiene uno o más ``Rol Funcional``,
       un ``Perfil`` y pertenece a un ``Segmento de Datos``.
   * - **Sinónimos**
     - Usuario del Sistema
   * - **Tipo**
     - Actor
   * - **Relaciones**
     - | ``Usuario`` tiene uno o más ``Rol Funcional``
       | ``Usuario`` tiene ``Perfil``
       | ``Usuario`` pertenece a ``Segmento de Datos``
       | ``Usuario`` inicia ``Sesión``

3.2. Cliente
^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Cliente
   * - **Definición**
     - Persona externa que interactúa con el ``Sistema IVR`` del cual IACT
       recolecta y analiza datos. No interactúa directamente con el Sistema IACT.
   * - **Sinónimos**
     - Llamante, Cliente Final
   * - **Tipo**
     - Actor Externo
   * - **Relaciones**
     - | ``Cliente`` realiza ``Llamada``
       | ``Cliente`` interactúa con ``Menú IVR``
       | ``Cliente`` genera ``Evento IVR``

------------------------------------------------------------
4. Conceptos RBAC
------------------------------------------------------------

4.1. Rol Funcional
^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Rol Funcional
   * - **Definición**
     - Conjunto nombrado de permisos que representa una capacidad técnica
       del sistema. Un ``Usuario`` puede tener múltiples roles funcionales
       simultáneamente. Los permisos se acumulan (operación UNION).
   * - **Sinónimos**
     - Rol, Rol RBAC
   * - **Tipo**
     - Objeto
   * - **Nota**
     - El sistema define 18 roles funcionales organizados en 6 categorías:
       Gestión de Usuarios, Reportes, Visualización, Análisis, Alertas,
       Administración.
   * - **Relaciones**
     - | ``Rol Funcional`` otorga ``Permiso``
       | ``Usuario`` tiene ``Rol Funcional``

4.2. Perfil
^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Perfil
   * - **Definición**
     - Configuración predefinida que determina módulos disponibles y límites
       operativos para un ``Usuario``. Existen 4 perfiles base: BÁSICO,
       ANALISTA, ADMINISTRADOR_SEGMENTO, ADMINISTRADOR.
   * - **Sinónimos**
     - Perfil de Usuario, Perfil de Módulos
   * - **Tipo**
     - Objeto
   * - **Relaciones**
     - | ``Usuario`` tiene ``Perfil``
       | ``Perfil`` habilita ``Módulo``
       | ``Perfil`` define límites operativos

4.3. Segmento de Datos
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Segmento de Datos
   * - **Definición**
     - Partición lógica de datos que restringe el alcance de información
       visible para un ``Usuario``. Cada usuario pertenece a exactamente
       un segmento.
   * - **Sinónimos**
     - Segmento, Data Segment
   * - **Tipo**
     - Objeto
   * - **Valores**
     - | OP: DATOS_OPERATIVOS (operación del IVR)
       | FI: DATOS_FINANCIEROS (costos y facturación)
       | TE: DATOS_TECNICOS (infraestructura y rendimiento)
       | SU: DATOS_SUPERVISION (supervisión y control)
       | CA: DATOS_CALIDAD (métricas de calidad)
       | GE: DATOS_CONSOLIDADOS (datos agregados)
   * - **Relaciones**
     - | ``Usuario`` pertenece a ``Segmento de Datos``
       | ``Segmento de Datos`` filtra ``Métrica``
       | ``Segmento de Datos`` filtra ``Reporte``

4.4. Permiso
^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Permiso
   * - **Definición**
     - Autorización atómica para ejecutar una acción específica en el sistema.
       Los permisos se asignan a través de ``Rol Funcional`` o directamente
       al ``Usuario`` (con fecha de expiración).
   * - **Sinónimos**
     - Permission, Autorización
   * - **Tipo**
     - Objeto
   * - **Formato**
     - ``recurso.accion[.modificador]`` (ej: reports.view.basic)
   * - **Relaciones**
     - | ``Rol Funcional`` otorga ``Permiso``
       | ``Permiso`` autoriza acción sobre recurso

------------------------------------------------------------
5. Conceptos del Sistema
------------------------------------------------------------

5.1. Sistema IACT
^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Sistema IACT
   * - **Definición**
     - Plataforma de software que captura, procesa y presenta métricas
       de interacción entre ``Cliente`` y sistemas IVR.
   * - **Sinónimos**
     - IACT, Sistema, Plataforma IACT
   * - **Tipo**
     - Sistema
   * - **Relaciones**
     - | ``Sistema IACT`` recibe ``Evento IVR``
       | ``Sistema IACT`` almacena ``Métrica``
       | ``Sistema IACT`` presenta ``Dashboard``

5.2. Sistema IVR
^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Sistema IVR
   * - **Definición**
     - Sistema externo de respuesta de voz interactiva que atiende
       llamadas de ``Cliente`` y genera eventos capturados por IACT.
   * - **Sinónimos**
     - IVR, Plataforma IVR, Sistema de Voz
   * - **Tipo**
     - Sistema Externo
   * - **Relaciones**
     - | ``Sistema IVR`` recibe ``Llamada``
       | ``Sistema IVR`` genera ``Evento IVR``
       | ``Sistema IVR`` contiene ``Menú IVR``

------------------------------------------------------------
6. Conceptos de Negocio
------------------------------------------------------------

6.1. Llamada
^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Llamada
   * - **Definición**
     - Interacción telefónica iniciada por un ``Cliente`` hacia el
       ``Sistema IVR``, con inicio y fin definidos.
   * - **Sinónimos**
     - Llamada Telefónica, Interacción
   * - **Tipo**
     - Evento
   * - **Relaciones**
     - | ``Llamada`` es iniciada por ``Cliente``
       | ``Llamada`` es atendida por ``Sistema IVR``
       | ``Llamada`` tiene ``Duración``
       | ``Llamada`` genera múltiples ``Evento IVR``

6.2. Evento IVR
^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Evento IVR
   * - **Definición**
     - Acción discreta ocurrida durante una ``Llamada``, registrada con
       timestamp y atributos específicos.
   * - **Sinónimos**
     - Evento, Acción IVR
   * - **Tipo**
     - Evento
   * - **Relaciones**
     - | ``Evento IVR`` pertenece a ``Llamada``
       | ``Evento IVR`` tiene ``Tipo de Evento``
       | ``Evento IVR`` tiene ``Timestamp``
       | ``Evento IVR`` genera ``Métrica``

6.3. Menú IVR
^^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Menú IVR
   * - **Definición**
     - Nodo de navegación en el ``Sistema IVR`` que presenta opciones
       al ``Cliente`` y captura su selección.
   * - **Sinónimos**
     - Menú, Opción IVR, Nodo IVR
   * - **Tipo**
     - Objeto
   * - **Relaciones**
     - | ``Menú IVR`` pertenece a ``Sistema IVR``
       | ``Menú IVR`` tiene ``Opciones``
       | ``Cliente`` navega ``Menú IVR``

6.4. Métrica
^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Métrica
   * - **Definición**
     - Valor cuantitativo derivado de uno o más ``Evento IVR``,
       calculado y almacenado para análisis.
   * - **Sinónimos**
     - Indicador, KPI, Medición
   * - **Tipo**
     - Objeto
   * - **Relaciones**
     - | ``Métrica`` se deriva de ``Evento IVR``
       | ``Métrica`` se presenta en ``Dashboard``
       | ``Métrica`` se incluye en ``Reporte``

------------------------------------------------------------
7. Conceptos de Presentación
------------------------------------------------------------

7.1. Dashboard
^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Dashboard
   * - **Definición**
     - Interfaz visual que presenta ``Métrica`` de forma agregada
       y actualizada, permitiendo monitoreo en tiempo real.
   * - **Sinónimos**
     - Tablero, Panel de Control
   * - **Tipo**
     - Objeto
   * - **Relaciones**
     - | ``Dashboard`` muestra ``Métrica``
       | ``Usuario`` visualiza ``Dashboard``
       | ``Dashboard`` contiene ``Widget``

7.2. Reporte
^^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Reporte
   * - **Definición**
     - Documento generado bajo demanda que presenta ``Métrica``
       para un período y criterios específicos.
   * - **Sinónimos**
     - Informe, Report
   * - **Tipo**
     - Objeto
   * - **Relaciones**
     - | ``Reporte`` contiene ``Métrica``
       | ``Usuario`` genera ``Reporte``
       | ``Reporte`` tiene ``Formato`` (PDF, Excel, CSV)

------------------------------------------------------------
8. Conceptos de Seguridad
------------------------------------------------------------

8.1. Sesión
^^^^^^^^^^^

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Término**
     - Sesión
   * - **Definición**
     - Período de interacción autenticada de un ``Usuario`` con el
       ``Sistema IACT``, delimitado por login y logout.
   * - **Sinónimos**
     - Sesión de Usuario
   * - **Tipo**
     - Evento
   * - **Relaciones**
     - | ``Usuario`` inicia ``Sesión``
       | ``Sesión`` tiene ``Duración``
       | ``Sesión`` registra ``Acción de Usuario``

------------------------------------------------------------
9. Diagrama de Relaciones
------------------------------------------------------------

::

   ┌─────────────┐         ┌─────────────┐
   │   Cliente   │────────▶│   Llamada   │
   └─────────────┘ realiza └──────┬──────┘
                                  │ genera
                                  ▼
   ┌─────────────┐         ┌─────────────┐
   │ Sistema IVR │◀────────│  Evento IVR │
   └─────────────┘ origina └──────┬──────┘
                                  │ deriva
                                  ▼
   ┌─────────────┐         ┌─────────────┐
   │   Usuario   │────────▶│   Métrica   │
   └──────┬──────┘ analiza └──────┬──────┘
          │                       │ presenta
          │ visualiza             ▼
          │                ┌─────────────┐
          └───────────────▶│  Dashboard  │
                           └─────────────┘

------------------------------------------------------------
10. Referencias
------------------------------------------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Documento
     - Referencia
   * - Tipos de Regla de Negocio
     - :doc:`SBVR_02_Tipos_Regla_Negocio`
   * - Vocabulario Controlado
     - :doc:`SBVR_03_Vocabulario_Controlado`
   * - Modelo RBAC
     - Modelo_RBAC_Completo_Sistema_IACT_v_0_0_1
   * - Glosario IACT
     - :doc:`/base_cognitiva/glosario/IACT_Glossary_v1_0_0`
   * - Especificación SBVR
     - SBVR 1.5 (OMG, 2019)

------------------------------------------------------------
Historial de Cambios
------------------------------------------------------------

.. list-table::
   :widths: 15 15 20 50
   :header-rows: 1

   * - Versión
     - Fecha
     - Autor
     - Cambios
   * - 1.0.0
     - 2025-12-18
     - BA Lead
     - Versión inicial con conceptos nucleares del dominio IACT

----

**Trazabilidad:** Vocabulario base para toda regla de negocio en
requisitos/reglas_negocio/. Ver :doc:`/trazabilidad/matrices/RTM_Master`.