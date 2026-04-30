.. meta::
 :artefacto: EJEMPLOS_AGREG_INTERFACES_IACT
 :tipo: Guia
 :dominio: gestion
 :subdominio: pm
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==================================================================
Agregación, composición, interfaces y realización — IACT
==================================================================

.. note::

 Compañero del :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`.
 Muestra los 5 conceptos de **Hora 5 de Schmuller**
 (agregación, composición, interfaces, realización,
 visibilidad y ámbito) aplicados al **dominio real del
 proyecto IACT** — call center IVR + analytics + ETL + RBAC.

 Sirve como **referencia de precedente** para los autores que
 generen los 13 documentos del plan.

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 Para la teoría genérica ver
 :doc:`/base-cognitiva/_uml/uml-05-agregacion-composicion-interfaces`
 (Schmuller Hora 5).

----

1. El camino al modelo completo
===============================

  La meta final es crear una **idea estática** de un sistema,
  con todas las conexiones entre las clases que lo conforman.

En esta hora completamos el modelo UML con:

- **Agregación** y **composición** (partes y todo).
- **Interfaces** (contratos de comportamiento).
- **Realizaciones** (implementación de interfaces).
- **Visibilidad** (acceso público / protegido / privado).
- **Ámbito** (instancia vs compartido / *archivador*).

----

2. Agregación (rombo vacío)
===========================

**Definición:** un *todo* se compone de *partes*, pero las
partes pueden existir **independientemente**.

**Característica clave:** un componente puede pertenecer a
**múltiples todos**.

**Símbolo:** rombo VACÍO (``o--``) en el lado del todo.

2.1 Funcion ◇ Grupo (catálogo RBAC IACT)
----------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Grupo {
     - id : Integer
     - nombre : String
   }
   class Funcion {
     - codigo : String
     - descripcion : String
   }

   Grupo "*" o-- "*" Funcion : contiene
   note right of Funcion
     Una función (capacidad atómica) PUEDE
     existir sin pertenecer a ningún grupo;
     pertenece a múltiples grupos
     simultáneamente (predefinidos
     AGR-001..010 y/o creados via
     UC_PERM_05). Si un grupo se elimina,
     las funciones siguen vivas en el
     catálogo de 42 funciones (CNST_029).
   end note
   @enduml

2.2 Otras agregaciones canónicas IACT
-------------------------------------

::

 Centro          ◇  Operador           — operadores reasignables
 Campania        ◇  Operador           — operadores compartidos
 Suscripcion     ◇  Alerta             — la alerta sigue activa
                                         si un suscriptor se va
                                         (UC_ALR_05)
 SegmentoDatos   ◇  Reporte            — el segmento puede usarse
                                         por múltiples reportes

2.3 Restricción OR en agregación
--------------------------------

A veces la agregación tiene un patrón *"uno u otro"*. En IACT,
una **alerta crítica** notifica por canal de máxima visibilidad,
elegido entre dos opciones del buzón interno (sin email per
CNST_001):

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class AlertaCritica
   class CanalUrgente
   class CanalPrioritario
   class TipoEntregaImmediata

   AlertaCritica o-- CanalUrgente
   AlertaCritica o-- CanalPrioritario
   AlertaCritica o-- TipoEntregaImmediata

   note "{xor}\nCanalUrgente OR CanalPrioritario\n(no ambos)" as N
   CanalUrgente .. N
   CanalPrioritario .. N
   @enduml

----

3. Composición (rombo relleno)
==============================

**Definición:** un *todo* se compone de *partes*, pero las
partes **NO pueden existir sin el todo**.

**Característica clave:** un componente pertenece a **un solo
todo** (relación de pertenencia exclusiva).

**Símbolo:** rombo RELLENO (``*--``) en el lado del todo.

**Vida útil:** cuando el todo muere, las partes también mueren.

3.1 EjecucionETL ● ErrorETL (UC_PIP)
------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class EjecucionETL {
     - id : Integer
     - fecha_inicio : DateTime
     - fecha_fin : DateTime
     - estado : Enum
     + cargarDesdeIVR()
   }

   class ErrorETL {
     - codigo : String
     - mensaje : String
     - tabla : String
     - timestamp : DateTime
   }

   class FilaCargada {
     - tabla : String
     - id_origen : Integer
     - timestamp : DateTime
   }

   EjecucionETL "1" *-- "0..*" ErrorETL    : compone
   EjecucionETL "1" *-- "0..*" FilaCargada : compone

   note right of EjecucionETL
     Composición:
       si la EjecucionETL se purga
       (UC_PIP), sus ErrorETL y
       FilaCargada se eliminan
       en cascada. No tienen
       sentido fuera de la
       ejecución que los generó.
   end note
   @enduml

3.2 Otras composiciones canónicas IACT
--------------------------------------

::

 Reporte          ●  FilaResultado      — filas atadas al reporte
                                          que las generó
 Sesion           ●  Token              — los tokens expiran con
                                          la sesión (CNST_002)
 EventoAuditoria  ●  DetalleAuditoria   — detalle inmutable
                                          atado al evento
                                          (CNST_025)
 Alerta           ●  HistorialAlerta    — historial muere con
                                          la alerta

3.3 Diferencia visual agregación vs composición
-----------------------------------------------

::

 AGREGACIÓN (◇)                COMPOSICIÓN (●)
 ──────────────────────────────────────────────────────
 Partes independientes         Partes dependientes
 Componente ∈ múltiples todos  Componente ∈ un solo todo
 No obligatoria la existencia  Obligatoria la existencia
 Ejemplo: Funcion en Grupo     Ejemplo: ErrorETL en EjecucionETL

  **Pregunta decisiva:**
  *"Si el todo desaparece, ¿la parte sigue teniendo sentido?"*
  - Sí → agregación.
  - No → composición.

----

4. Diagramas de contexto
========================

Un **diagrama de contexto** es un *zoom* sobre una parte del
sistema.

4.1 Contexto de composición — EjecucionETL
------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   package "EjecucionETL (composición)" {
     class Scheduler
     class FilaCargada
     class ErrorETL
     class EstadoEjecucion

     Scheduler --> EstadoEjecucion : dispara
     EstadoEjecucion --> FilaCargada : produce
     EstadoEjecucion --> ErrorETL    : registra
   }
   note right of EstadoEjecucion
     Diagrama de contexto:
     muestra cómo se relacionan
     los componentes DENTRO de
     una EjecucionETL.
   end note
   @enduml

4.2 Contexto de sistema — IACT completo
---------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   package "IACT (contexto del sistema)" {
     class Usuario
     class Sesion
     class Reporte
     class Metrica
     class Alerta
     class Suscripcion
     class EjecucionETL
     class EventoAuditoria
     class IVR
     class BuzonInterno

     Usuario --> Sesion         : abre
     Usuario --> Reporte        : consulta
     Reporte --> Metrica        : agrega
     Alerta  --> Suscripcion    : notifica
     Suscripcion --> Usuario    : pertenece
     EjecucionETL --> IVR       : lee (read-only)
     Alerta --> BuzonInterno    : notifica via (CNST_001)
     Usuario --> EventoAuditoria : genera
   }

   cloud "Stripe / SendGrid" as Externos
   note right of Externos
     NO aplica a IACT —
     sin pasarela de pago,
     sin email externo.
   end note
   @enduml

----

5. Interfaces y realizaciones
=============================

**Definición:** una **interfaz** es un conjunto de operaciones
públicas que una clase presenta a otras.

**Interfaz ≠ clase:**

- **Clase** — tiene atributos y operaciones (estructura
  completa).
- **Interfaz** — sólo tiene operaciones públicas (contrato de
  comportamiento).

**Realización:** cuando una clase implementa una interfaz.

**Símbolo:** línea discontinua con triángulo vacío (``..|>``).

5.1 ``IExportable`` — UC_RPT_04, UC_AUD_03, UC_LOG_04
-----------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   interface IExportable <<interface>> {
     + exportar(formato : Enum) : Archivo
     + estimarFilas() : Integer
     + obtenerSizeMB() : Decimal
   }

   class Reporte {
     - tipo : Enum
     - filtros : Filtro
     + exportar(formato : Enum) : Archivo
     + estimarFilas() : Integer
     + obtenerSizeMB() : Decimal
   }

   class EventoAuditoria {
     - rango : Rango
     + exportar(formato : Enum) : Archivo
     + estimarFilas() : Integer
     + obtenerSizeMB() : Decimal
   }

   class LogSistema {
     - rango : Rango
     - servicio : String
     + exportar(formato : Enum) : Archivo
     + estimarFilas() : Integer
     + obtenerSizeMB() : Decimal
   }

   Reporte ..|> IExportable
   EventoAuditoria ..|> IExportable
   LogSistema ..|> IExportable

   note right of IExportable
     Contrato común para tres tipos
     de export en IACT:
       UC_RPT_04 (Reporte)
       UC_AUD_03 (Auditoría)
       UC_LOG_04 (Logs)
     Throttling distinto por formato
     per CNST_019/020.
   end note
   @enduml

5.2 ``INotificable`` — UC_ALR_02 / UC_ALR_05
--------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   interface INotificable <<interface>> {
     + entregar(usuario : Usuario, mensaje : Mensaje) : Boolean
     + obtenerEstado() : EstadoEntrega
   }

   class BuzonInterno {
     + entregar(usuario, mensaje) : Boolean
     + obtenerEstado() : EstadoEntrega
   }

   class NotificacionPush {
     + entregar(usuario, mensaje) : Boolean
     + obtenerEstado() : EstadoEntrega
   }

   BuzonInterno ..|> INotificable
   NotificacionPush ..|> INotificable

   note right of INotificable
     CNST_001 prohíbe email →
     IACT NO implementa NotificacionEmail.
     Las únicas implementaciones válidas son
     buzón interno y notificación push interna.
   end note
   @enduml

5.3 ``ISegmentable`` — filtrado por segmento (BR_012)
-----------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   interface ISegmentable <<interface>> {
     + aplicarFiltroSegmento(s : SegmentoDatos)
     + perteneceA(s : SegmentoDatos) : Boolean
   }

   class Llamada
   class Reporte
   class Alerta
   class EventoAuditoria

   Llamada ..|> ISegmentable
   Reporte ..|> ISegmentable
   Alerta ..|> ISegmentable
   EventoAuditoria ..|> ISegmentable

   note right of ISegmentable
     Toda entidad consultada por
     un usuario operativo debe
     filtrarse por su segmento
     (BR_012). El contrato lo
     uniforma.
   end note
   @enduml

5.4 Beneficios de usar interfaces
---------------------------------

::

 SIN INTERFACES:
   - Código duplicado en múltiples clases
   - Difícil de mantener
   - Acoplamiento alto

 CON INTERFACES:
   - Un solo lugar para definir el contrato
   - Reutilización de código
   - Bajo acoplamiento
   - Fácil agregar nuevas implementaciones

----

6. Visibilidad — ``+ # -``
==========================

La **visibilidad** controla quién puede acceder a atributos y
operaciones.

.. list-table::
 :widths: 12 18 30 40
 :header-rows: 1

 * - Símbolo
   - Nivel
   - Acceso
   - Uso típico en IACT
 * - ``+``
   - Público
   - Cualquier clase
   - Interfaz expuesta a otros UCs
 * - ``#``
   - Protegido
   - Sólo subclases
   - Implementación heredada por subtipos
 * - ``-``
   - Privado
   - Sólo la clase
   - Detalles internos (segmentación, hash,
     SQL crudo)

6.1 Ejemplo — clase ``Reporte``
-------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Reporte {
     - segmento_aplicado : SegmentoDatos
     - cache_ttl : Integer
     - sql_crudo : String
     # registrarConsulta()
     # invalidarCache()
     + generar(filtros : Filtro)
     + exportar(formato : Enum)
     + getResultados()
   }
   note right of Reporte
     Visibilidad:
       + generar / exportar / getResultados
         → interfaz pública del UC_RPT
       # registrarConsulta / invalidarCache
         → heredable por subtipos
         (ReporteHistorico, ReporteAgentes...)
       - segmento_aplicado / cache_ttl /
         sql_crudo → detalles internos
         (segmentación BR_012, SLA CNST_017)
   end note
   @enduml

6.2 Visibilidad en interfaces
-----------------------------

  En las **interfaces** todas las operaciones son
  **públicas (+)** — el propósito es que otras clases las
  implementen y usen.

----

7. Ámbito — instancia vs archivador
===================================

El **ámbito** determina si un atributo o operación es:

- **Instancia** — cada objeto tiene su propio valor (común).
- **Archivador** (estático) — todos los objetos comparten un
  valor (raro). Notación: subrayado.

7.1 Configuración de SLAs del sistema (CNST_017)
------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class ConfiguracionSLA {
     {static} - sla_max_seg : Integer = 10
     {static} - retencion_max_anios : Integer = 2
     {static} - export_csv_max : Integer = 100000
     {static} - export_excel_max : Integer = 50000
     {static} - export_pdf_max : Integer = 10000
     {static} - throttling_intentos_login : Integer = 5
     {static} - throttling_ventana_min : Integer = 5
     {static} + getSlaMaxSeg() : Integer
     {static} + getExportLimit(formato : Enum) : Integer
   }
   note right of ConfiguracionSLA
     Todos los atributos son
     **archivador** (subrayados):
     una sola configuración
     compartida por todo el
     sistema. Refleja:
       CNST_017 (SLA)
       CNST_015 (retención 2 años)
       CNST_019/020 (export)
       CNST_011 (throttling)
   end note
   @enduml

7.2 Catálogo de funciones — instancia compartida
------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Funcion {
     - codigo : String
     - descripcion : String
     - modulo : String
     {static} - TOTAL : Integer = 42
     {static} + listarTodas() : List<Funcion>
     {static} + buscarPorCodigo(c : String) : Funcion
   }
   note right of Funcion
     - codigo / descripcion / modulo
       → instancia (cada Funcion es única)
     - TOTAL = 42 (CNST_029)
       → archivador (compartido por todas
         las instancias)
     - listarTodas / buscarPorCodigo
       → archivador (operaciones de catálogo)
   end note
   @enduml

----

8. Modelo completo IACT — integración
=====================================

8.1 Paso 1 — agregación + composición
-------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Grupo
   class Funcion
   class EjecucionETL
   class ErrorETL

   Grupo "*" o-- "*" Funcion           : agregación
   EjecucionETL "1" *-- "0..*" ErrorETL : composición

   note right of Funcion
     Agregación: Funcion sobrevive
     al borrado de Grupo.
   end note
   note right of ErrorETL
     Composición: ErrorETL muere
     con la EjecucionETL.
   end note
   @enduml

8.2 Paso 2 — interfaces + visibilidad
-------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   interface IExportable <<interface>> {
     + exportar(formato)
   }
   class Reporte {
     - sql_crudo : String
     # registrarConsulta()
     + exportar(formato)
   }
   class LogSistema {
     - servicio : String
     + exportar(formato)
   }
   Reporte ..|> IExportable
   LogSistema ..|> IExportable
   @enduml

8.3 Paso 3 — diagrama de contexto integrado
-------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   skinparam packageStyle rectangle

   package "IACT — sistema completo" {
     package "Catálogo RBAC" {
       class Funcion
       class Grupo
       Grupo "*" o-- "*" Funcion
     }

     package "Pipeline ETL" {
       class EjecucionETL
       class ErrorETL
       EjecucionETL "1" *-- "0..*" ErrorETL
     }

     package "Reportes" {
       interface IExportable <<interface>>
       class Reporte
       class FilaResultado
       Reporte ..|> IExportable
       Reporte "1" *-- "0..*" FilaResultado
     }

     package "Auditoría" {
       class EventoAuditoria
       class DetalleAuditoria
       EventoAuditoria ..|> IExportable
       EventoAuditoria "1" *-- "0..*" DetalleAuditoria
     }

     package "Alertas" {
       interface INotificable <<interface>>
       class Alerta
       class BuzonInterno
       Alerta -- BuzonInterno : usa
       BuzonInterno ..|> INotificable
     }
   }

   note bottom
     ◇ agregación (Grupo–Funcion)
     ● composición (Reporte–FilaResultado,
       EjecucionETL–ErrorETL,
       EventoAuditoria–DetalleAuditoria)
     ..|> realización (IExportable,
                      INotificable)
   end note
   @enduml

----

9. Resumen — los 5 conceptos
============================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   skinparam packageStyle rectangle
   rectangle "Modelo UML completo (IACT)" as M {
     rectangle "1. AGREGACIÓN ◇\nGrupo ↔ Funcion\nCentro ↔ Operador"               as A
     rectangle "2. COMPOSICIÓN ●\nEjecucionETL ↔ ErrorETL\nReporte ↔ Fila"          as C
     rectangle "3. INTERFACES\nIExportable, INotificable,\nISegmentable"            as I
     rectangle "4. VISIBILIDAD\n+ público / # protegido / − privado"                as V
     rectangle "5. ÁMBITO\nInstancia vs archivador\n(ConfiguracionSLA = static)"    as S
   }
   @enduml

----

10. Aplicación a UCs específicos del catálogo IACT
==================================================

**UC_RPT_04 (Exportar reporte):**

::

 Interfaz       : Reporte ..|> IExportable
 Composición    : Reporte ●─ FilaResultado
 Visibilidad    : -sql_crudo (privado), +exportar (público)
 Ámbito         : ConfiguracionSLA (archivador) define
                  límites CNST_019/020 por formato

**UC_PIP_02 (Consultar errores ETL):**

::

 Composición    : EjecucionETL ●─ ErrorETL
                  (errores no existen sin ejecución)
 Visibilidad    : +obtenerErrores (público),
                  -conexion_ivr (privada)

**UC_PERM_06 (Asignar funciones a grupo):**

::

 Agregación     : Grupo ◇─ Funcion
                  (función sobrevive al grupo)
 Composición    : —
 Restricción    : SoD validada en runtime per CNST_030

**UC_ALR_05 (Gestionar suscripciones):**

::

 Interfaz       : BuzonInterno ..|> INotificable
 Restricción    : sin email per CNST_001 (no hay
                  NotificacionEmail implementando la interfaz)

**UC_AUD_03 (Exportar auditoría):**

::

 Interfaz       : EventoAuditoria ..|> IExportable
 Composición    : EventoAuditoria ●─ DetalleAuditoria
 Restricción    : append-only per CNST_025
                  (no hay método borrar() en la interfaz)

----

11. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``ba-requirements-analysis`` (BABOK — RADD)
 * - **Origen del documento**
   - Reescrito de "GUÍA-AGREGACION-COMPOSICION-INTERFACES-
     REALIZACION" (cheat-sheet aplicado interno con dominio
     ecommerce), **reorientado al dominio real IACT**.
 * - **Teoría genérica**
   - :doc:`/base-cognitiva/_uml/uml-05-agregacion-composicion-interfaces`
     (Schmuller Hora 5)
 * - **Cheat-sheet de los 9 diagramas**
   - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama`
 * - **Modelo RBAC vigente**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact`
 * - **Catálogo modular del dominio IACT**
   - :doc:`/gestion/evidencia/arquitectura-modular/analisis-catalogo-modular-iact`
 * - **Ejemplos hermanos aplicados a IACT**
   - :doc:`diagramas-uml`,
     :doc:`orientacion-objetos`,
     :doc:`analisis-dominio`,
     :doc:`relaciones-uml`
 * - **Plan de documentación**
   - :doc:`plan-documentacion-uc`
 * - **Plantilla canónica de UC**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Restricciones citadas**
   - CNST_001 (no email),
     CNST_002 (sesión única),
     CNST_011 (throttling 5/5min),
     CNST_015 (retención 2 años),
     CNST_017 (SLA tiempos),
     CNST_019/020 (export async + throttling),
     CNST_025 (auditoría inmutable),
     CNST_029 (catálogo de 42 funciones),
     CNST_030 (SoD),
     BR_012 (segmento único).
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
