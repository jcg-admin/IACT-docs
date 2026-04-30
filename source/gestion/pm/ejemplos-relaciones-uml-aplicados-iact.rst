.. meta::
 :artefacto: EJEMPLOS_RELACIONES_UML_IACT
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
Relaciones UML aplicadas al dominio IACT (PlantUML)
==================================================================

.. note::

 Compañero del :doc:`/gestion/pm/plan-documentacion-uc-con-uml`.
 Muestra los **6 tipos de relaciones UML + multiplicidad**
 aplicados al **dominio real del proyecto IACT** — call center
 IVR + analytics + supervisión ETL + RBAC granular.

 Sirve como **referencia de precedente** para los autores que
 generen los 13 documentos del plan.

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 Para la teoría genérica ver
 :doc:`/base-cognitiva/_uml/uml-04-uso-relaciones`
 (Schmuller Hora 4).

----

1. Por qué necesitamos relaciones
=================================

Las clases por sí solas son incompletas. El poder de UML está
en cómo se conectan.

**6 tipos de relaciones UML:**

1. **Asociación** — conexión conceptual (tiene, usa, relaciona).
2. **Herencia** — especialización (*es un tipo de*).
3. **Composición** — parte fuerte (el todo contiene las
   partes).
4. **Agregación** — parte débil (el todo agrupa partes).
5. **Dependencia** — uso (una clase usa otra).
6. **Realización** — implementación de interfaz.

----

2. Asociación
=============

**Definición:** conexión conceptual entre dos clases. Elementos:
línea + nombre + dirección + roles + multiplicidad.

2.1 Usuario consulta Reporte (UC_RPT)
-------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario {
     - id : Integer
     - email : String
     + login()
     + consultarReporte()
   }

   class Reporte {
     - id : Integer
     - tipo : Enum
     + generar()
   }

   Usuario "1" --> "0..*" Reporte : consulta

   note right of Usuario
     Asociación:
     un Usuario consulta muchos Reportes;
     un Reporte es consultado por 1 Usuario
     (en una sesión).
   end note
   @enduml

2.2 Roles en asociación — relación empleador-empleado
-----------------------------------------------------

Un caso de roles aplicado a IACT: la relación entre
``Supervisor`` (rol *aprobador*) y ``Operador`` (rol
*ejecutor*) en la asignación de funciones (UC_ACC_01):

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   Usuario "1\n<<aprobador>>" -- "0..*\n<<ejecutor>>" Usuario : asigna_funciones
   note right of Usuario
     Roles en la asignación
     de funciones:
       - aprobador  (supervisor)
       - ejecutor   (operador o
                    admin de acceso)
   end note
   @enduml

2.3 Asociación bidireccional
----------------------------

A veces la relación funciona en ambas direcciones:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Operador
   class Supervisor
   Operador "1..*" -- "1..*" Supervisor : asesorado_por
   Supervisor "1..*" -- "1..*" Operador : asesora_a
   note right of Operador
     Bidireccional: un operador
     puede ser asesorado por varios
     supervisores y viceversa.
   end note
   @enduml

2.4 Asociaciones principales del proyecto IACT
----------------------------------------------

::

 Usuario       → posee     → Sesion          (1 : 0..1)
 Usuario       → tiene     → SegmentoDatos   (1 : 1)
 Usuario       → asignado  → Grupo            (* : *)
 Grupo         → contiene  → Funcion          (* : *)
 Reporte       → agrega    → Llamada          (* : 0..*)
 EjecucionETL  → carga     → Llamada          (* : 1..*)
 Alerta        → notifica  → Usuario          (* : 0..*)
 Usuario       → genera    → EventoAuditoria  (1 : 0..*)

----

3. Multiplicidad
================

3.1 Tabla de multiplicidades
----------------------------

.. list-table::
 :widths: 18 32 50
 :header-rows: 1

 * - Notación
   - Significado
   - Ejemplo IACT
 * - ``1``
   - Exactamente uno
   - Usuario tiene 1 SegmentoDatos
 * - ``0..1``
   - Ninguno o uno (opcional)
   - Usuario posee 0 ó 1 Sesion (CNST_002)
 * - ``1..*``
   - Uno o más
   - EjecucionETL carga 1..* Llamadas
 * - ``0..*`` ó ``*``
   - Cero o más
   - Reporte agrega 0..* Llamadas
 * - ``2..5``
   - Entre 2 y 5
   - Alerta tiene 2..5 Suscriptores mínimos
 * - ``3, 5``
   - Exactamente 3 ó 5
   - (raro en IACT, ejemplo conceptual)

3.2 Multiplicidades canónicas IACT
----------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   class Sesion
   class SegmentoDatos
   class Grupo
   class Funcion
   class Llamada
   class Reporte
   class EjecucionETL
   class ErrorETL
   class Alerta
   class Suscripcion

   Usuario "1" -- "0..1" Sesion           : posee
   Usuario "1" -- "1"   SegmentoDatos     : restringido
   Usuario "*" -- "*"   Grupo             : asignado
   Grupo   "*" -- "*"   Funcion           : contiene
   Reporte "1" -- "0..*" Llamada          : agrega
   EjecucionETL "1" -- "0..*" ErrorETL    : compose
   EjecucionETL "1" -- "1..*" Llamada     : carga
   Alerta "1" -- "0..*" Suscripcion       : tiene
   Suscripcion "0..*" -- "1" Usuario      : pertenece

   note right of Usuario
     - Usuario:Sesion = 1:0..1 (CNST_002 sesión única)
     - Usuario:SegmentoDatos = 1:1 (BR_012)
     - Reporte:Llamada = 1:0..* (filtro CNST_008)
     - EjecucionETL:Llamada = 1:1..*
     - Alerta:Suscriptor = 1:0..*
   end note
   @enduml

----

4. Asociaciones calificadas
===========================

**Problema:** una asociación 1:* requiere buscar un objeto
específico entre muchos.

**Solución:** un **calificador** (pequeño rectángulo) identifica
la búsqueda → convierte 1:* en 1:1.

4.1 Búsqueda de Llamada por id
------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Reporte
   class Llamada
   Reporte "1" -[#black]- "(id)" Llamada : busca
   note right of Llamada
     Calificador `id` reduce
     1:* a 1:1 en runtime.
     Se usa en UC_RPT_03 al
     consultar el detalle de
     una llamada específica.
   end note
   @enduml

4.2 Búsqueda de Reporte por nombre programado
---------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   class Reporte
   Usuario "1" -[#black]- "(nombre)" Reporte : recupera_programado
   note right of Reporte
     UC_RPT_08 — el usuario
     recupera el reporte programado
     por su nombre (único en
     su contexto de usuario).
   end note
   @enduml

4.3 Otros calificadores en IACT
-------------------------------

::

 Usuario   → [funcion_codigo]    → Funcion        (UC_PERM_07)
 Catalogo  → [agr_id]            → Grupo (AGR-NN) (UC_ACC_04)
 Pipeline  → [fecha]             → EjecucionETL   (UC_PIP_03)
 Auditoria → [evento_id]         → EventoAuditoria (UC_AUD_01)

----

5. Asociaciones reflexivas
==========================

Una clase se relaciona consigo misma.

5.1 Cadena de mando — Usuario supervisa Usuario
-----------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   Usuario "1\n<<supervisor>>" -- "0..*\n<<supervisado>>" Usuario : supervisa
   note right of Usuario
     Reflexiva:
       - un Supervisor supervisa
         0..* Operadores;
       - un Operador es supervisado
         por 1 Usuario.
     Roles distintos en la misma
     clase Usuario.
   end note
   @enduml

5.2 Función compuesta — Funcion → Funcion
-----------------------------------------

Algunas funciones del catálogo RBAC se componen de otras
(macro-funciones que implican varias atómicas):

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Funcion
   Funcion "0..*" -- "0..*" Funcion : implica
   note right of Funcion
     Reflexiva en el catálogo
     de 42 funciones (CNST_029):
       p.ej. ``manage_users``
       implica view_users +
       create_users +
       modify_users +
       delete_users.
   end note
   @enduml

----

6. Herencia (generalización)
============================

**Definición:** una subclase **es un tipo de** la superclase.
Símbolo: triángulo vacío apuntando a la superclase.

6.1 Jerarquía de Usuario en IACT
--------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario {
     - id : Integer
     - email : String
     - password_hash : String
     + login()
     + logout()
   }

   class Operador {
     + verDashboard()
     + verAlertasActivas()
   }

   class Supervisor {
     - centros : List<Integer>
     + verReportesHistoricos()
     + reconocerAlerta()
   }

   class AdminAcceso {
     + asignarFunciones()
     + revocarFunciones()
   }

   class AdminPipeline {
     + supervisarETL()
     + solicitarReintento()
   }

   class Auditor {
     + consultarAuditoria()
     + generarReporteCompliance()
   }

   Usuario <|-- Operador
   Usuario <|-- Supervisor
   Usuario <|-- AdminAcceso
   Usuario <|-- AdminPipeline
   Usuario <|-- Auditor
   note right of Usuario
     Cada rol "es un tipo de"
     Usuario. Todos heredan
     login(), logout().
   end note
   @enduml

6.2 Herencia multinivel — Reporte
---------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Reporte {
     - id : Integer
     - tipo : Enum
     + generar()
   }

   class ReporteOperativo {
     - segmento : SegmentoDatos
   }

   class ReporteRealTime {
     - ttl_seg : Integer
   }

   class ReporteHistorico {
     - rango_max : Integer
   }

   class ReporteAgentes
   class ReporteColas
   class ReporteCampanias

   Reporte <|-- ReporteOperativo
   ReporteOperativo <|-- ReporteRealTime
   ReporteOperativo <|-- ReporteHistorico
   ReporteHistorico <|-- ReporteAgentes
   ReporteHistorico <|-- ReporteColas
   ReporteHistorico <|-- ReporteCampanias
   note right of ReporteHistorico
     Multinivel:
       ReporteAgentes "es un tipo de"
       ReporteHistorico que a su vez
       "es un tipo de" ReporteOperativo
       que es Reporte.
   end note
   @enduml

6.3 Descubrimiento de la herencia
---------------------------------

**Preguntas para identificar herencia:**

1. ¿Tienen atributos comunes? (Operador, Supervisor, Admin →
   email, password, segmento).
2. ¿Tienen operaciones comunes? (todos pueden ``login()``,
   ``logout()``).
3. ¿Puedo decir *"es un tipo de"*? (Operador es un tipo de
   Usuario ✓; Operador tiene un Reporte ✗ — sería asociación).

6.4 Otras jerarquías canónicas IACT
-----------------------------------

::

 Usuario          → Operador / Supervisor / AdminAcceso
                    / AdminPipeline / Auditor
 Reporte          → ReporteRealTime / ReporteHistorico /
                    ReporteAgentes / ReporteColas /
                    ReporteCampanias
 Alerta           → AlertaUmbral / AlertaTendencia /
                    AlertaPipeline (severidades INFO /
                    WARNING / CRITICAL)
 EventoAuditoria  → AuditoriaAcceso / AuditoriaPermiso /
                    AuditoriaCambioAcceso (todas inmutables
                    per CNST_025)
 EjecucionETL     → EjecucionExitosa / EjecucionConErrores /
                    EjecucionReintentada

----

7. Composición vs agregación
============================

**Diferencia clave:**

::

 AGREGACIÓN (◇)  : las partes pueden existir sin el todo
 COMPOSICIÓN (●)  : las partes NO pueden existir sin el todo

7.1 Agregación — Grupo agrega Funciones
---------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Grupo
   class Funcion
   Grupo "1" o-- "0..*" Funcion : contiene
   note right of Funcion
     Agregación:
     si el Grupo se elimina,
     la Funcion sigue existiendo
     en el catálogo de 42 funciones
     (CNST_029) y puede pertenecer
     a otros grupos.
   end note
   @enduml

7.2 Composición — EjecucionETL compone Errores
----------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class EjecucionETL
   class ErrorETL
   class FilaCargada
   EjecucionETL "1" *-- "0..*" ErrorETL    : compone
   EjecucionETL "1" *-- "0..*" FilaCargada : compone
   note right of EjecucionETL
     Composición:
     si la EjecucionETL se purga,
     sus ErrorETL y FilaCargada
     pierden sentido — dependen
     completamente de la ejecución.
   end note
   @enduml

7.3 Casos prácticos en IACT
---------------------------

**Agregación:**

- ``Grupo`` ◇ ``Funcion`` — funciones existen en el catálogo
  general aunque el grupo se borre.
- ``Suscripcion`` ◇ ``Alerta`` — la alerta sigue activa
  aunque un suscriptor se desuscriba (UC_ALR_05).
- ``Centro`` ◇ ``Operador`` — los operadores pueden
  reasignarse a otro centro.

**Composición:**

- ``EjecucionETL`` ● ``ErrorETL`` — los errores no tienen
  sentido fuera de la ejecución que los generó.
- ``Reporte`` ● ``FilaResultado`` — las filas son resultado
  específico del reporte.
- ``EventoAuditoria`` ● ``DetalleAuditoria`` — los detalles
  inmutables se atan al evento (CNST_025).
- ``Sesion`` ● ``Token`` — los tokens caducan con la sesión
  (CNST_002).

7.4 Pregunta decisiva
---------------------

  *"Si el TODO desaparece, ¿las PARTES siguen teniendo
  sentido?"*

::

 SÍ → Agregación  (◇ rombo abierto)
 NO → Composición (● rombo relleno)

----

8. Restricciones en asociaciones
================================

8.1 Restricción ``{ordered}`` — UC_AUTH_01 throttling
-----------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class AuthService
   class IntentoLogin
   AuthService "1" -- "0..*" IntentoLogin : procesa
   note right of IntentoLogin
     {ordered}
     Los intentos se procesan en
     orden de llegada (FIFO);
     CNST_011 aplica throttling
     5 intentos / 5 min por IP.
   end note
   @enduml

8.2 Restricción ``{xor}`` — Permiso vía grupo o excepcional
-----------------------------------------------------------

Un usuario obtiene permiso a una función **vía un grupo asignado
o vía un permiso excepcional**, no ambos a la vez para la misma
función:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   class Grupo
   class PermisoExcepcional

   Usuario --> Grupo : asignado_a
   Usuario --> PermisoExcepcional : tiene
   note "{xor} para una misma\nfunción atómica" as N
   Grupo .. N
   PermisoExcepcional .. N
   @enduml

----

9. Clases de asociación
=======================

Una **clase de asociación** describe una relación que tiene
propiedades propias (atributos / operaciones).

9.1 Suscripcion entre Usuario y Alerta (UC_ALR_05)
--------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   class Alerta

   class Suscripcion {
     - fecha_inscripcion : DateTime
     - canal : Enum
     - severidad_minima : Enum
     - silenciada_hasta : DateTime
     + actualizar(canal, severidad)
     + silenciar(hasta)
   }

   Usuario "0..*" -- "0..*" Alerta : suscrito_a
   (Usuario, Alerta) .. Suscripcion
   note right of Suscripcion
     Atributos propios de la
     suscripción: fecha, canal
     (sólo buzón interno per
     CNST_001), severidad mínima
     y silenciamiento temporal.
   end note
   @enduml

9.2 Asignacion entre Usuario y Funcion (UC_ACC_01)
--------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Usuario
   class Funcion

   class Asignacion {
     - fecha_inicio : DateTime
     - fecha_fin : DateTime
     - aprobador : Usuario
     - es_temporal : Boolean
     - justificacion : String
     + revocar()
     + extender(nueva_fecha)
   }

   Usuario "0..*" -- "0..*" Funcion : asignado
   (Usuario, Funcion) .. Asignacion
   note right of Asignacion
     Cuando es_temporal = true,
     CNST_031 obliga
     fecha_fin ≤ fecha_inicio + 6
     meses y justificación con
     ≥ 20 caracteres.
   end note
   @enduml

----

10. Dependencias
================

**Definición:** una clase **usa** a otra. Símbolo: línea
discontinua con flecha hacia la clase usada.

10.1 SecRules usa Funcion (UC_PERM_07)
--------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class SecRules {
     + verificarPermiso(usuario : Usuario, funcion : Funcion) : Boolean
   }
   class Usuario
   class Funcion

   SecRules ..> Usuario : <<usa>>
   SecRules ..> Funcion : <<usa>>
   note right of SecRules
     Dependencia: SecRules usa
     Usuario y Funcion como
     parámetros — no las contiene
     ni las hereda.
   end note
   @enduml

10.2 Reporte usa Filtro (UC_RPT_09)
-----------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Reporte {
     + generar(filtros : Filtro) : Reporte
   }
   class Filtro

   Reporte ..> Filtro : <<usa>>
   note right of Reporte
     Reporte recibe Filtro como
     parámetro de generar(). Es
     dependencia, no composición:
     el Filtro existe
     independientemente del
     Reporte.
   end note
   @enduml

----

11. Resumen — tabla de relaciones
=================================

.. list-table::
 :widths: 20 14 22 44
 :header-rows: 1

 * - Relación
   - Símbolo
   - Frase clave
   - Ejemplo IACT
 * - **Asociación**
   - ``--``
   - tiene / usa
   - Usuario consulta Reporte
 * - **Herencia**
   - ``<|--``
   - es un tipo de
   - Operador es un Usuario
 * - **Composición**
   - ``*--``
   - compone (fuerte)
   - EjecucionETL compone ErrorETL
 * - **Agregación**
   - ``o--``
   - contiene (débil)
   - Grupo contiene Funciones
 * - **Dependencia**
   - ``..>``
   - usa
   - SecRules usa Funcion
 * - **Realización**
   - ``..|>``
   - implementa
   - StripeAdapter implementa
     IPasarelaPago (no aplica
     directamente a IACT — sin
     Stripe)

----

12. Aplicación a UCs específicos del catálogo IACT
==================================================

**UC_RPT_01 (Ver Dashboard)**
::

 Asociación   : Dashboard 1:* Reporte (contiene)
 Asociación   : Reporte 0..*:1 SegmentoDatos (filtra por)
 Herencia     : ReporteRealTime is-a ReporteOperativo is-a Reporte
 Dependencia  : Dashboard ..> Filtro (usa)

**UC_PIP_01 (Supervisar ETL)**
::

 Asociación   : SupervisorETL 1:0..* EjecucionETL (monitorea)
 Composición  : EjecucionETL *-- 0..* ErrorETL (compone)
 Composición  : EjecucionETL *-- 1..* FilaCargada (compone)
 Dependencia  : SupervisorETL ..> Scheduler (usa)

**UC_PERM_07 (Verificar Permiso)**
::

 Dependencia  : SecRules ..> Usuario (usa)
 Dependencia  : SecRules ..> Funcion (usa)
 Asociación   : Usuario *:* Grupo (asignado)
 Asociación   : Grupo  *:* Funcion (contiene)
 ClaseAsoc    : Asignacion describe Usuario--Funcion
                (con CNST_031 si es_temporal)

**UC_ALR_05 (Gestionar Suscripciones)**
::

 ClaseAsoc    : Suscripcion describe Usuario--Alerta
 Asociación   : Suscripcion 0..*:1 Usuario
 Asociación   : Suscripcion 0..*:1 Alerta
 Restricción  : canal en {buzon_interno} per CNST_001

**UC_AUD_01 (Consultar Auditoría)**
::

 Asociación   : Auditor 1:0..* EventoAuditoria (consulta)
 Composición  : EventoAuditoria *-- 0..* DetalleAuditoria
 Restricción  : EventoAuditoria es append-only (CNST_025)

----

13. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``ba-requirements-analysis`` (BABOK — RADD)
 * - **Origen del documento**
   - Reescrito de "GUÍA-RELACIONES-UML-TIPOS-Y-MULTIPLICIDAD"
     (cheat-sheet aplicado interno con dominio ecommerce),
     **reorientado al dominio real IACT** (call center IVR +
     analytics + RBAC + ETL).
 * - **Teoría genérica**
   - :doc:`/base-cognitiva/_uml/uml-04-uso-relaciones`
     (Schmuller Hora 4)
 * - **Cheat-sheet de los 9 diagramas**
   - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama`
 * - **Modelo RBAC vigente**
   - :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact`
 * - **Catálogo modular del dominio IACT**
   - :doc:`/gestion/evidencia/arquitectura-modular/analisis-catalogo-modular-iact`
 * - **Ejemplos hermanos aplicados a IACT**
   - :doc:`ejemplos-uml-aplicados-iact`,
     :doc:`ejemplos-oop-aplicados-iact`,
     :doc:`ejemplos-analisis-dominio-aplicados-iact`
 * - **Plan de documentación**
   - :doc:`plan-documentacion-uc-con-uml`
 * - **Plantilla canónica de UC**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Restricciones citadas**
   - CNST_001 (no email, sólo buzón interno),
     CNST_002 (sesión única),
     CNST_011 (throttling 5/5min),
     CNST_025 (auditoría inmutable),
     CNST_029 (catálogo de 42 funciones),
     CNST_031 (permisos temporales ≤ 6 meses),
     BR_012 (segmento único).
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
