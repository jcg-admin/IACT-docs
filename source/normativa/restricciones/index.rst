.. _restricciones-index:

==============================================================================
Restricciones del Sistema
==============================================================================

:Dominio: arquitectura_tecnica
:Subdominio: restricciones
:Estado: CONGELADO
:Documentos: 10
:Lineas Totales: 9,621
:Ultima Actualizacion: 2025-12-17

Descripcion General
-------------------

Este subdominio contiene las **restricciones tecnicas impuestas** al sistema
IACT Dashboard Analytics. Las restricciones son limitaciones externas que
provienen del cliente, la infraestructura existente o politicas organizacionales.

.. important::

   **CNST = Restriccion IMPUESTA (externa)**
   
   A diferencia de los estandares (STD) que son metodologias adoptadas
   internamente, las restricciones son imposiciones que el equipo de
   desarrollo DEBE cumplir sin negociacion.

Diferencia CNST vs STD
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Tipo
     - Naturaleza
     - Ejemplo
   * - CNST
     - Imposicion externa del cliente
     - "NO usar email para notificaciones"
   * - STD
     - Metodologia adoptada internamente
     - "Usar Clean Code naming"

Catalogo de Restricciones
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 10 35 15 40

   * - ID
     - Titulo
     - Lineas
     - Descripcion
   * - CNST-001
     - :ref:`cnst-001`
     - 685
     - Prohibicion de comunicaciones externas (email, SMS, WhatsApp)
   * - CNST-002
     - :ref:`cnst-002`
     - 840
     - Gestion de sesiones unicas y tokens JWT
   * - CNST-003
     - :ref:`cnst-003`
     - 901
     - Arquitectura dual de base de datos MySQL/PostgreSQL
   * - CNST-004
     - :ref:`cnst-004`
     - 920
     - Actualizacion de datos solo via ETL nocturno
   * - CNST-005
     - :ref:`cnst-005`
     - 994
     - Checklist de seguridad Django REST Framework
   * - CNST-006
     - :ref:`cnst-006`
     - 1,126
     - Antipatrones de arquitectura prohibidos
   * - CNST-007
     - :ref:`cnst-007`
     - 1,061
     - Limites de rendimiento y SLAs
   * - CNST-008
     - :ref:`cnst-008`
     - 1,019
     - Infraestructura y modelo de deployment
   * - CNST-009
     - :ref:`cnst-009`
     - 1,077
     - Logging y auditoria inmutable
   * - CNST-010
     - :ref:`cnst-010`
     - 998
     - Clasificacion y proteccion de datos

Organizacion por Categoria
--------------------------

Comunicaciones y Sesiones
^^^^^^^^^^^^^^^^^^^^^^^^^

Restricciones relacionadas con la interaccion usuario-sistema.

- :ref:`cnst-001` - Comunicaciones Prohibidas
- :ref:`cnst-002` - Gestion de Sesiones

Base de Datos y ETL
^^^^^^^^^^^^^^^^^^^

Restricciones sobre el manejo de datos y sincronizacion.

- :ref:`cnst-003` - Base de Datos Dual Inmutable
- :ref:`cnst-004` - Actualizacion via ETL

Seguridad y Acceso
^^^^^^^^^^^^^^^^^^

Restricciones de seguridad, autenticacion y autorizacion.

- :ref:`cnst-005` - Seguridad DRF
- :ref:`cnst-010` - Clasificacion de Datos

Arquitectura y Rendimiento
^^^^^^^^^^^^^^^^^^^^^^^^^^

Restricciones sobre diseno y limites operacionales.

- :ref:`cnst-006` - Antipatrones Prohibidos
- :ref:`cnst-007` - Limites Performance/SLA

Infraestructura y Operaciones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Restricciones sobre deployment y operacion del sistema.

- :ref:`cnst-008` - Infraestructura Deployment
- :ref:`cnst-009` - Logging Auditoria

Matriz de Impacto por Componente
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 10 10 10 10 10

   * - CNST
     - API
     - UI
     - ETL
     - BD
     - Infra
   * - CNST-001
     - X
     - X
     - 
     - 
     - 
   * - CNST-002
     - X
     - X
     - 
     - X
     - 
   * - CNST-003
     - X
     - 
     - X
     - X
     - 
   * - CNST-004
     - 
     - 
     - X
     - X
     - 
   * - CNST-005
     - X
     - 
     - 
     - 
     - 
   * - CNST-006
     - X
     - X
     - X
     - X
     - 
   * - CNST-007
     - X
     - X
     - X
     - X
     - 
   * - CNST-008
     - X
     - X
     - 
     - 
     - X
   * - CNST-009
     - X
     - 
     - X
     - X
     - 
   * - CNST-010
     - X
     - X
     - X
     - X
     - 

Integracion con RBAC v4.0
-------------------------

Todas las restricciones consideran los 18 roles funcionales del sistema:

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Rol
     - Codigo
     - CNSTs Aplicables
   * - R001
     - SUPER_ADMIN
     - Todos (acceso completo)
   * - R003
     - DASHBOARD_VIEWER
     - CNST-001, 002, 007, 010(C1-C2)
   * - R004
     - REPORTS_VIEWER
     - CNST-001, 002, 007, 010(C1-C2)
   * - R005
     - REPORTS_EXPORTER
     - CNST-001, 002, 007, 010(C1-C2)
   * - R010
     - DATA_ANALYST
     - CNST-001, 002, 003, 007, 010(C1-C3)
   * - R011
     - ETL_OPERATOR
     - CNST-003, 004, 009
   * - R015
     - SYSTEM_ADMIN
     - Todos excepto CNST-003 escritura MySQL
   * - R016
     - AUDIT_VIEWER
     - CNST-009, 010

Dependencias entre Restricciones
--------------------------------

.. code-block:: text

   CNST-003 (BD Dual)
       |
       +---> CNST-004 (ETL) - Requiere arquitectura dual
       |
       +---> CNST-009 (Audit) - Logs en PostgreSQL
   
   CNST-005 (Seguridad DRF)
       |
       +---> CNST-002 (Sesiones) - JWT authentication
       |
       +---> CNST-010 (Datos) - Permisos por clasificacion
   
   CNST-008 (Infra)
       |
       +---> CNST-007 (SLA) - Limites por capacidad servidor
       |
       +---> CNST-009 (Audit) - Rotacion logs por espacio

Resumen de Implementacion
-------------------------

Modelos Django Definidos
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # CNST-001
   class InternalMessage(models.Model)
   class SecurityQuestion(models.Model)
   
   # CNST-002
   class UserSession(models.Model)
   
   # CNST-003
   class IVRCallDetail(models.Model)      # MySQL (lectura)
   class DailyCallMetrics(models.Model)   # PostgreSQL
   
   # CNST-004
   class ETLExecution(models.Model)
   
   # CNST-009
   class UserActionLog(models.Model)
   class APIAccessLog(models.Model)
   
   # CNST-010
   class DataClassification(models.Model)

Servicios y Middleware
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # CNST-001
   def notify_admins(subject, message)
   def notify_user(user_id, message)
   
   # CNST-002
   class SingleSessionMiddleware
   def validate_jwt_token(token)
   
   # CNST-003
   class IVRReadOnlyRouter
   class IVRDataExtractor
   
   # CNST-004
   class ETLPipeline
   class ETLScheduler
   
   # CNST-009
   class AuditLogMiddleware
   def log_user_action(user, action, details)

Permisos DRF
^^^^^^^^^^^^

.. code-block:: python

   # CNST-005
   class IsAuthenticated
   class HasRole(role_id)
   class RBACPermission
   
   # CNST-010
   class CanAccessRestrictedData      # C3
   class CanAccessConfidentialData    # C4
   @requires_classification(level)

Verificacion de Cumplimiento
----------------------------

Script de validacion disponible en cada documento CNST:

.. code-block:: bash

   # Verificar cumplimiento de todas las restricciones
   python manage.py check_constraints --all
   
   # Verificar restriccion especifica
   python manage.py check_constraints --cnst=001

Referencias
-----------

Documentos Relacionados
^^^^^^^^^^^^^^^^^^^^^^^

- :ref:`std-003` - Clean Code Naming (nombres usados en CNST)
- :ref:`std-004` - Nomenclatura Proyecto (paths api/ui)
- :ref:`std-001` - Suite Calidad (Bandit en CNST-005)
- :ref:`adr-001` - Stack Django + React
- :ref:`adr-002` - BD Dual MySQL + PostgreSQL

Metodologia
^^^^^^^^^^^

Las restricciones fueron documentadas siguiendo:

- Formato RST para Sphinx
- Sin emojis ni simbolos visuales
- Sin referencias a estandares externos (OWASP, NIST, ISO)
- Justificacion tecnica (no legal/regulatoria)
- Integracion con RBAC v4.0
- Ejemplos de codigo Clean Code

Historial de Versiones
----------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Version
     - Fecha
     - Cambios
   * - 1.0.0
     - 2025-12-17
     - Version inicial con 10 documentos CNST

Indice de Documentos
--------------------

.. toctree::
   :maxdepth: 1
   :caption: Restricciones

   CNST_001_Comunicaciones_Prohibidas
   CNST_002_Gestion_Sesiones_BD
   CNST_003_Base_Datos_Dual_Inmutable
   CNST_004_Actualizacion_Datos_ETL
   CNST_005_Seguridad_DRF_Checklist
   CNST_006_Antipatrones_Arquitectura
   CNST_007_Limites_Performance_SLA
   CNST_008_Infraestructura_Deployment
   CNST_009_Logging_Auditoria_Inmutable
   CNST_010_Clasificacion_Proteccion_Datos
