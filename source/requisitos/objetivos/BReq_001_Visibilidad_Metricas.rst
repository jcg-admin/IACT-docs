.. meta::
   :artefacto: BReq_001
   :tipo: Business Requirement
   :dominio: requisitos
   :subdominio: objetivos
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2026-01-06
   :ultimo_cambio: 2026-01-06
   :autor: Equipo IACT
   :clasificacion: Interno

.. _breq-001:

==============================================================================
BReq_001: Objetivos de Negocio IACT
==============================================================================

.. contents:: Contenido
   :local:
   :depth: 2

----

1. Proposito
------------

Este documento define los Business Requirements (BReq) del proyecto IACT -
IVR Analytics & Customer Tracking. Los BReq representan los objetivos de
alto nivel que justifican la existencia del sistema.

1.1 Alcance
^^^^^^^^^^^

- Define 5 objetivos de negocio medibles
- Establece metricas de exito cuantificables
- Documenta trazabilidad hacia BR (influencia) y UC (generacion)
- Sirve como base para validar el exito del proyecto

1.2 Relacion con META_04
^^^^^^^^^^^^^^^^^^^^^^^^

META_04 describe el CONTEXTO del proyecto (stakeholders, sistemas, ambiente).
Este documento define los OBJETIVOS (metas medibles del negocio).

::

   META_04: "Donde opera IACT?" -> Contexto
   BReq:    "Por que existe IACT?" -> Objetivos

----

2. Vision del Proyecto
----------------------

2.1 Enunciado de Vision
^^^^^^^^^^^^^^^^^^^^^^^

IACT proporciona a los supervisores y analistas del call center una
plataforma de analitica que transforma datos operacionales del IVR en
informacion accionable, permitiendo decisiones basadas en evidencia y
reduciendo el tiempo de respuesta ante incidentes.

2.2 Problema de Negocio
^^^^^^^^^^^^^^^^^^^^^^^

Actualmente, los datos del sistema IVR estan disponibles pero no son
facilmente accesibles ni analizables. Los supervisores carecen de
visibilidad en tiempo real sobre metricas clave como:

- Tasa de abandono de llamadas
- Tiempo promedio de espera
- Carga por centro de atencion
- Tendencias y anomalias

2.3 Solucion Propuesta
^^^^^^^^^^^^^^^^^^^^^^

IACT extrae datos del IVR mediante proceso ETL nocturno, los transforma
en metricas accionables, y los presenta en dashboards y reportes accesibles
segun el perfil de cada usuario.

----

3. Business Requirements
------------------------

3.1 BReq-001: Visibilidad de Metricas IVR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Enunciado Formal**

El sistema DEBE proporcionar visibilidad en tiempo casi-real de las
metricas operacionales del IVR, permitiendo a los supervisores monitorear
el estado del call center.

**Metrica de Exito**

::

   Dashboard actualizado automaticamente cada 5 minutos
   Latencia maxima de datos: D+1 (dia siguiente al operacional)
   100% de metricas clave disponibles en dashboard

**Justificacion**

Sin visibilidad de metricas, los supervisores operan "a ciegas" y no
pueden detectar problemas hasta que escalan significativamente.

**BR que Influyen**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - BR
     - Nombre
     - Como Influye
   * - BR_002
     - ETL Batch Nocturno
     - Define cuando se actualizan los datos (D+1)
   * - BR_016
     - Tasa de Abandono
     - Define calculo de metrica clave
   * - BR_017
     - Tiempo Promedio Espera
     - Define calculo de metrica clave

**UC que Genera**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - UC
     - Nombre
     - Relacion
   * - UC-025
     - Visualizar Dashboard Operativo
     - Vista principal de metricas
   * - UC-026
     - Ver KPIs en Tiempo Real
     - Indicadores actualizados
   * - UC-027
     - Analizar Tendencias
     - Graficos historicos
   * - UC-028
     - Comparar Periodos
     - Analisis comparativo
   * - UC-029
     - Filtrar por Centro
     - Segmentacion de datos
   * - UC-030
     - Exportar Vista Dashboard
     - Compartir estado
   * - UC-050
     - Supervisar Estado ETL
     - Monitoreo del proceso
   * - UC-051
     - Consultar Errores ETL
     - Diagnostico de problemas
   * - UC-052
     - Consultar Disponibilidad Datos
     - Verificar actualizacion
   * - UC-053
     - Reiniciar Proceso ETL
     - Recuperacion manual

----

3.2 BReq-002: Reduccion de Tiempo de Respuesta a Incidentes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Enunciado Formal**

El sistema DEBE reducir el tiempo de deteccion y respuesta a incidentes
operacionales mediante alertas proactivas basadas en umbrales configurables.

**Metrica de Exito**

::

   Reduccion >= 40% en tiempo de respuesta vs linea base
   Linea base: Tiempo promedio actual sin sistema de alertas
   Medicion: Tiempo desde ocurrencia hasta primera accion correctiva

**Justificacion**

La deteccion tardia de problemas (alta tasa de abandono, colas saturadas)
resulta en perdida de clientes y deterioro del servicio.

**BR que Influyen**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - BR
     - Nombre
     - Como Influye
   * - BR_014
     - Alerta por Umbral
     - Define mecanismo de deteccion automatica

**UC que Genera**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - UC
     - Nombre
     - Relacion
   * - UC-036
     - Crear Alerta por Umbral
     - Configuracion de deteccion
   * - UC-037
     - Recibir Notificacion Alerta
     - Comunicacion al usuario
   * - UC-038
     - Consultar Historial Alertas
     - Registro de eventos
   * - UC-039
     - Modificar Configuracion Alerta
     - Ajuste de umbrales
   * - UC-040
     - Gestionar Destinatarios Alerta
     - Distribucion de notificaciones


----

3.3 BReq-003: Decisiones Informadas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Enunciado Formal**

El sistema DEBE proporcionar reportes y analisis que permitan a los
tomadores de decision basar sus acciones en datos concretos y actualizados.

**Metrica de Exito**

::

   100% de decisiones operacionales documentadas con datos de soporte
   Reportes disponibles en formatos exportables (CSV, Excel, PDF)
   Tiempo de generacion de reporte: < 30 segundos

**Justificacion**

Decisiones basadas en intuicion o datos desactualizados resultan en
asignacion ineficiente de recursos y oportunidades perdidas.

**BR que Influyen**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - BR
     - Nombre
     - Como Influye
   * - BR_011
     - Limites de Exportacion
     - Define volumenes maximos exportables
   * - BR_012
     - Segmentacion Usuario-Centro
     - Define alcance de datos por usuario
   * - BR_020
     - Rango Temporal Reportes
     - Define ventana maxima de consulta

**UC que Genera**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - UC
     - Nombre
     - Relacion
   * - UC-017
     - Generar Reporte Predefinido
     - Reportes estandar
   * - UC-018
     - Crear Reporte Personalizado
     - Reportes ad-hoc
   * - UC-019
     - Programar Reporte Automatico
     - Generacion periodica
   * - UC-020
     - Filtrar Reportes por Fecha
     - Seleccion temporal
   * - UC-021
     - Filtrar Reportes por Centro
     - Seleccion geografica
   * - UC-022
     - Exportar Reporte CSV
     - Formato tabular
   * - UC-023
     - Exportar Reporte Excel
     - Formato enriquecido
   * - UC-024
     - Exportar Reporte PDF
     - Formato presentacion

----

3.4 BReq-004: Cumplimiento de Seguridad
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Enunciado Formal**

El sistema DEBE garantizar que solo usuarios autorizados accedan a los
datos y funcionalidades segun sus permisos asignados, cumpliendo con
politicas de seguridad organizacionales.

**Metrica de Exito**

::

   0 accesos no autorizados detectados
   100% de accesos registrados en auditoria
   Cumplimiento RBAC NIST verificable
   0 violaciones de SoD

**Justificacion**

Datos del call center incluyen informacion sensible de operaciones.
Acceso no autorizado representa riesgo regulatorio y de negocio.

**BR que Influyen**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - BR
     - Nombre
     - Como Influye
   * - BR_004
     - Comunicaciones Internas Only
     - Limita canales de notificacion
   * - BR_005
     - Sesion Unica por Usuario
     - Previene acceso concurrente
   * - BR_006
     - RBAC Flat NIST
     - Define modelo de permisos
   * - BR_007
     - Separacion Funciones SoD
     - Previene conflictos de interes
   * - BR_008
     - Auditoria de Accesos
     - Registra toda actividad
   * - BR_009
     - Bajas Logicas
     - Preserva trazabilidad
   * - BR_010
     - Auditoria Inmutable
     - Protege evidencia
   * - BR_013
     - Username Unico
     - Garantiza identificacion
   * - BR_015
     - Bloqueo Intentos Fallidos
     - Previene fuerza bruta
   * - BR_018
     - Retencion de Logs
     - Cumple retencion legal
   * - BR_019
     - Clasificacion de Datos
     - Define niveles de proteccion

**UC que Genera**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - UC
     - Nombre
     - Relacion
   * - UC-001
     - Iniciar Sesion
     - Autenticacion
   * - UC-002
     - Cerrar Sesion
     - Terminacion segura
   * - UC-003
     - Recuperar Password
     - Restablecimiento seguro
   * - UC-004
     - Cambiar Password Propio
     - Gestion credenciales
   * - UC-005
     - Gestionar Sesiones Activas
     - Control de acceso
   * - UC-010
     - Asignar Funciones a Usuario
     - Permisos
   * - UC-011
     - Revocar Funciones a Usuario
     - Desautorizacion
   * - UC-041
     - Asignar Segmento de Datos
     - Alcance de datos
   * - UC-042
     - Revocar Segmento de Datos
     - Restriccion
   * - UC-043
     - Configurar Restricciones SoD
     - Segregacion
   * - UC-044
     - Consultar Permisos Efectivos
     - Verificacion
   * - UC-045
     - Gestionar Catalogo Agrupadores
     - Administracion RBAC
   * - UC-046
     - Gestionar Catalogo Funciones
     - Administracion RBAC
   * - UC-047
     - Auditar Cambios de Permisos
     - Trazabilidad
   * - UC-060
     - Registrar Evento Auditoria
     - Logging
   * - UC-061
     - Consultar Log Auditoria
     - Revision
   * - UC-062
     - Generar Reporte Auditoria
     - Evidencia
   * - UC-063
     - Exportar Auditoria
     - Archivo
   * - UC-070
     - Consultar Logs Sistema
     - Diagnostico
   * - UC-071
     - Filtrar Logs por Criterio
     - Busqueda
   * - UC-072
     - Exportar Logs Sistema
     - Archivo tecnico
   * - UC-073
     - Configurar Retencion Logs
     - Politica

----

3.5 BReq-005: Integridad de Datos Operacionales
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Enunciado Formal**

El sistema DEBE garantizar que los datos operacionales del IVR permanezcan
inalterados, accediendo a la base de datos IVR exclusivamente en modo
lectura.

**Metrica de Exito**

::

   0 operaciones de escritura en base IVR
   100% de accesos via Database Router validado
   Verificacion continua mediante logs de BD

**Justificacion**

La base IVR es un sistema legacy critico que alimenta multiples aplicaciones.
Cualquier modificacion accidental comprometeria operaciones del call center
y otros sistemas dependientes.

**BR que Influyen**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - BR
     - Nombre
     - Como Influye
   * - BR_001
     - Fuente Operacional Inmutable
     - Define restriccion de solo lectura

**UC que Genera**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - UC
     - Nombre
     - Relacion
   * - UC-050
     - Supervisar Estado ETL
     - Monitoreo extraccion (solo lectura)
   * - UC-051
     - Consultar Errores ETL
     - Diagnostico sin modificar origen
   * - UC-052
     - Consultar Disponibilidad Datos
     - Verificar sin alterar
   * - UC-053
     - Reiniciar Proceso ETL
     - Re-extraccion (solo lectura)

----

4. Matriz de Trazabilidad
-------------------------

4.1 Trazabilidad BReq -> UC (Generacion)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   BReq-001 (Visibilidad)    --genera--> UC-025 a UC-030 (Dashboard)
                                         UC-050 a UC-053 (Pipeline)
                                         Total: 10 UC

   BReq-002 (Incidentes)     --genera--> UC-036 a UC-040 (Alertas)
                                         Total: 5 UC

   BReq-003 (Decisiones)     --genera--> UC-017 a UC-024 (Reportes)
                                         Total: 8 UC

   BReq-004 (Cumplimiento)   --genera--> UC-001 a UC-005 (Auth)
                                         UC-010, UC-011, UC-041-047 (Access)
                                         UC-060 a UC-063 (Audit)
                                         UC-070 a UC-073 (Logs)
                                         Total: 22 UC

   BReq-005 (Integridad)     --genera--> UC-050 a UC-053 (Pipeline)
                                         Total: 4 UC (compartidos con BReq-001)

4.2 Trazabilidad BR -> BReq (Influencia)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Business Rule
     - BReq Influenciados
   * - BR_001 Fuente Operacional Inmutable
     - BReq-005
   * - BR_002 ETL Batch Nocturno
     - BReq-001
   * - BR_003 Usuario Inactivo 90 Dias
     - BReq-004
   * - BR_004 Comunicaciones Internas Only
     - BReq-004
   * - BR_005 Sesion Unica por Usuario
     - BReq-004
   * - BR_006 RBAC Flat NIST
     - BReq-004
   * - BR_007 Separacion Funciones SoD
     - BReq-004
   * - BR_008 Auditoria de Accesos
     - BReq-004
   * - BR_009 Bajas Logicas
     - BReq-004
   * - BR_010 Auditoria Inmutable
     - BReq-004
   * - BR_011 Limites de Exportacion
     - BReq-003
   * - BR_012 Segmentacion Usuario-Centro
     - BReq-003
   * - BR_013 Username Unico
     - BReq-004
   * - BR_014 Alerta por Umbral
     - BReq-002
   * - BR_015 Bloqueo Intentos Fallidos
     - BReq-004
   * - BR_016 Tasa de Abandono
     - BReq-001
   * - BR_017 Tiempo Promedio Espera
     - BReq-001
   * - BR_018 Retencion de Logs
     - BReq-004
   * - BR_019 Clasificacion de Datos
     - BReq-004
   * - BR_020 Rango Temporal Reportes
     - BReq-003

4.3 Resumen de Cobertura
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Metrica
     - Valor
     - Total
     - Cobertura
   * - BReq con UC
     - 5
     - 5
     - 100%
   * - BR con BReq
     - 20
     - 20
     - 100%
   * - UC generados
     - 49
     - 49
     - 100%

----

5. Criterios de Exito del Proyecto
----------------------------------

5.1 KPIs Agregados
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - KPI
     - Meta
     - Frecuencia Medicion
   * - Disponibilidad Dashboard
     - >= 99.5%
     - Mensual
   * - Reduccion Tiempo Incidentes
     - >= 40%
     - Trimestral
   * - Decisiones con Datos
     - 100%
     - Mensual
   * - Incidentes Seguridad
     - 0
     - Continua
   * - Escrituras en IVR
     - 0
     - Continua

5.2 Criterios de Aceptacion del Proyecto
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El proyecto IACT se considera exitoso cuando:

1. Dashboard operativo disponible con metricas actualizadas D+1
2. Sistema de alertas funcional con al menos 5 umbrales configurados
3. Reportes exportables en 3 formatos (CSV, Excel, PDF)
4. Modelo RBAC implementado con 44 funciones y 10 agrupadores
5. Auditoria completa de todos los accesos
6. Cero escrituras detectadas en base IVR

----

6. Referencias
--------------

Documentos Relacionados
^^^^^^^^^^^^^^^^^^^^^^^

- **FND_05**: Jerarquia de 4 Niveles - Define estructura BR -> BReq -> UC -> FR
- **META_04**: Contexto del Proyecto - Describe ambiente operacional
- **reglas_negocio/**: 20 BR documentadas que influyen en estos BReq
- **MODELO_RBAC_IACT_v5.1.1**: Modelo de control de acceso
- **CNST_001 a CNST_010**: Restricciones tecnicas que originan las BR

Fuentes de Requisitos
^^^^^^^^^^^^^^^^^^^^^

- Entrevistas con supervisores de call center
- Analisis de sistema IVR legacy
- Politicas de seguridad organizacionales
- CNST del cliente (restricciones no negociables)

----

7. Historial de Cambios
-----------------------

.. list-table::
   :widths: 15 15 20 50
   :header-rows: 1

   * - Version
     - Fecha
     - Autor
     - Descripcion del Cambio
   * - 1.0.0
     - 2026-01-06
     - Equipo IACT
     - Version inicial con 5 BReq documentados

----