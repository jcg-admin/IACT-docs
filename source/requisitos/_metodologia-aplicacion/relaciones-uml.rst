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

 Compañero del :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`.
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

13. Comparativa por contexto — el contexto manda
=================================================

La distinción entre tipos de relaciones (asociación,
agregación, composición, dependencia) **no siempre es
clara**. El factor más determinante es el **contexto** en
el que viven los objetos: el contexto define visibilidad,
temporalidad y versatilidad de la colaboración. Un análisis
cuidadoso y consistente evita problemas en la práctica.

Ejemplo Paciente–Médico
-----------------------

- **Contexto urgencias**: la interacción es temporal y
  específica → **dependencia / uso** es suficiente. Un
  médico atiende a un paciente en un episodio puntual y
  no mantiene seguimiento.
- **Contexto atención primaria**: hay seguimiento
  continuo y acceso al historial → **asociación**
  refleja mejor la realidad: la relación persiste, el
  médico tiene un vínculo durable con el paciente.

El mismo par de clases admite **dos relaciones
diferentes** según el contexto. Modelar las dos a la vez
casi siempre indica que hay realmente dos sistemas
distintos.

Ejemplo Motor–Coche
-------------------

- **Contexto taller mecánico**: el motor puede ser
  reemplazado o modificado de forma independiente →
  **asociación** o **agregación** (el motor existe sin
  el coche, se intercambia entre coches).
- **Contexto gestión administrativa vehicular**: el
  motor es parte integral del vehículo y determina
  características fiscales → **composición** (vida
  ligada al coche, no se "reemplaza" en sentido
  administrativo).

Aplicación a IACT
-----------------

.. list-table::
 :widths: 22 35 43
 :header-rows: 1

 * - Par de clases
   - Contexto
   - Relación recomendada
 * - ``Reporte`` ↔ ``Filtro``
   - El filtro se compone para una consulta puntual.
   - Dependencia / uso (no se persiste el filtro).
 * - ``Reporte`` ↔ ``ConfiguracionExport``
   - La configuración pertenece a la tarea de export.
   - Composición (vive y muere con la tarea).
 * - ``EjecucionETL`` ↔ ``ErrorETL``
   - Errores son parte indivisible de la ejecución.
   - Composición.
 * - ``EjecucionETL`` ↔ ``VentanaETL``
   - Una ventana puede contener varias ejecuciones; la
     ventana sigue existiendo si la ejecución falla.
   - Asociación.
 * - ``Usuario`` ↔ ``Grupo``
   - Asignación cambiante; un usuario puede pertenecer
     a varios grupos.
   - Asociación N:M con clase intermedia
     ``Asignacion``.
 * - ``Sesion`` ↔ ``Usuario``
   - La sesión existe por el usuario y caduca con él
     (CNST_002).
   - Composición o agregación fuerte según se permita
     reabrir la sesión sin recrear el ``Usuario``.

Cita canónica — Rumbaugh
------------------------

   *La decisión de utilizar una agregación es discutible
   y suele ser arbitraria. Con frecuencia, no resulta
   evidente que una asociación deba ser modelada en
   forma de agregación. En gran parte, este tipo de
   incertidumbre es típico del modelado; este requiere
   un juicio bien formado y hay pocas reglas
   inamovibles. La experiencia demuestra que si uno
   piensa cuidadosamente e intenta ser congruente, la
   distinción imprecisa entre asociación ordinaria y
   agregación no da lugar a problemas en la práctica.*
   — Rumbaugh, 1991.

No hay solución única — hay trade-offs
--------------------------------------

Cuando se decide cómo relacionar diferentes partes del
sistema, no existe una respuesta universalmente
"perfecta". Cada elección compromete factores que
compiten entre sí:

- **Costo** de desarrollo y mantenimiento.
- **Legibilidad** del código.
- **Eficiencia** de la solución.
- **Modularidad** del diseño.

Reglas IACT para decidir
------------------------

1. Empezar por el **contexto del UC**, no por la
   intuición sobre la pareja de clases.
2. Si el mismo par admite **dos relaciones distintas**
   en dos UCs, modelar separadamente — probablemente son
   dos clases diferentes con el mismo nombre.
3. **Ser consistente** dentro del mismo cluster (ver § 11
   de :doc:`agregacion-interfaces`).
4. En caso de duda **agregación vs asociación**, elegir
   asociación: es más laxa y se puede endurecer después
   sin romper consumidores.
5. Documentar la decisión en un ADR del subdominio si la
   relación es central al cluster.

----

14. Comparativa de tipos de herencia
====================================

No toda herencia es válida. Existen al menos cuatro
formas conceptuales de aplicarla, dos legítimas y dos a
evitar. Esta sección las clasifica con criterio LSP
(Liskov Substitution Principle) y aplica el contraste a
IACT.

14.1 Herencia por especialización (recomendada)
-----------------------------------------------

La **herencia por especialización** (*inheritance by
specialization*) representa una relación **"es un tipo
de"** donde una clase descendiente hereda el comportamiento
**completo** de su clase base pero lo **expande o
modifica** para un propósito más específico.

En esta relación, la clase descendiente debe implementar
**absolutamente todas** las operaciones definidas en la
clase base — no puede omitir ninguna — y la complementa
con características adicionales o modificaciones
especializadas.

Tres principios esenciales
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Implementación obligatoria de todas las operaciones**
   de la clase base, asegurando que no se omita ninguna
   funcionalidad.
2. **Capacidad de añadir nuevas características** que
   enriquecen la funcionalidad básica sin alterar el
   contrato.
3. **Posibilidad de redefinir ciertos comportamientos**
   para adaptarlos a necesidades más específicas, siempre
   respetando la sustitución de Liskov.

Características que la distinguen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Mantiene el comportamiento base del padre.
- Añade características específicas.
- No elimina ni restringe funcionalidades.
- Respeta el contrato original (LSP).

Beneficios: jerarquías naturales, mantenimiento más
sencillo, reusabilidad, extensiones seguras.

Obligaciones del subtipo
~~~~~~~~~~~~~~~~~~~~~~~~

- Implementar **todas** las operaciones base.
- No puede omitir comportamientos.
- Mantiene la **coherencia** del modelo.
- Preserva la **sustitución de Liskov**.

Aspectos clave del diseño
~~~~~~~~~~~~~~~~~~~~~~~~~

- La especialización debe **tener sentido en el dominio**.
- Los cambios son **incrementales y compatibles**.
- Se mantiene la **cohesión** del modelo.
- Las modificaciones respetan el **propósito original**.

**Cuándo usarla**: cuando exista relación clara de
subtipo, la especialización sea natural en el contexto, se
necesite comportamiento adicional específico y no se viole
LSP.

**Mejores prácticas**: implementar todas las operaciones,
mantener cohesión, respetar propósito original, seguir
principios SOLID.

**Regla principal**: si una clase hija no puede cumplir
completamente con el contrato de su padre, la herencia
no es apropiada.

Ejemplo canónico — figuras geométricas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   abstract class Figura {
     - color : String
     - posicionX : int
     - posicionY : int
     + calcularArea()
     + calcularPerimetro()
     + dibujar()
     + mover()
   }

   class Circulo {
     - radio : double
     + calcularArea()
     + calcularPerimetro()
     + dibujar()
     + mover()
   }

   class Rectangulo {
     - base : double
     - altura : double
     + calcularArea()
     + calcularPerimetro()
     + dibujar()
     + mover()
   }

   Figura <|-- Circulo
   Figura <|-- Rectangulo

   note left of Figura : Clase base
   note right of Circulo : Especializacion completa
   note right of Rectangulo : Especializacion completa
   @enduml

``Circulo`` y ``Rectangulo`` **implementan todas** las
operaciones de ``Figura`` (``calcularArea``,
``calcularPerimetro``, ``dibujar``, ``mover``); ninguna
queda sin implementar ni se desactiva. La especialización
añade los atributos propios (``radio``; ``base``,
``altura``) sin romper el contrato.

Ejemplo aplicado a IACT
~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   abstract class Reporte {
     + generar()
     + exportar(formato)
   }
   class ReporteVolumen
   class ReporteAbandono
   class ReporteSoDCompliance
   Reporte <|-- ReporteVolumen
   Reporte <|-- ReporteAbandono
   Reporte <|-- ReporteSoDCompliance
   @enduml

Cada subclase **mantiene** ``generar()`` y ``exportar()``
y **añade** su lógica específica de cálculo. Ningún
subtipo rompe el contrato del padre.

Por qué es buena práctica
~~~~~~~~~~~~~~~~~~~~~~~~~

La herencia por especialización es uno de los usos más
correctos y naturales de la herencia porque:

- Mantiene la **integridad del modelo**.
- Es **intuitiva y fácil de entender**.
- Sigue los principios **SOLID**.
- Facilita el **polimorfismo seguro** — cualquier
  consumidor de ``Figura`` o ``Reporte`` puede operar
  sobre cualquier subtipo sin saber cuál es.

14.2 Herencia por extensión con transformación (con cuidado)
------------------------------------------------------------

La **herencia por extensión con transformación
conceptual** (*inheritance by extension with conceptual
transformation*) representa un caso donde la clase
derivada **no solo hereda** atributos y comportamientos de
su clase base, sino que **modifica el concepto fundamental**
que representa.

La relación deja de ser "es un tipo de" y pasa a ser
**"se transforma en"**: la clase derivada introduce un
cambio significativo en el propósito o la interpretación
del objeto, mientras mantiene la estructura heredada.

Naturaleza transformativa
~~~~~~~~~~~~~~~~~~~~~~~~~

- Va **más allá** de "es-un".
- Representa una **evolución o transformación** del
  concepto original.
- **Mantiene estructura** técnica heredada pero **cambia
  el significado** fundamental.

Aspectos clave
~~~~~~~~~~~~~~

- La clase hija modifica la **interpretación conceptual**.
- **Conserva la estructura técnica** heredada.
- Introduce nuevos comportamientos que **alteran el
  propósito**.
- Representa una **metamorfosis** del concepto original.

Riesgos asociados
~~~~~~~~~~~~~~~~~

- Puede **confundir** a otros desarrolladores.
- Dificulta el **mantenimiento** del código.
- Puede **violar expectativas** del sistema.
- **Complica** la comprensión del modelo de dominio.

Ejemplo canónico — ``Documento`` → ``ContratoCorporativo``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una clase base ``Documento`` que se transforma en
``ContratoCorporativo``: ya no solo es un documento que
**almacena información**, sino que se convierte en un
**instrumento legal** que ejecuta y valida acciones
corporativas. El concepto fundamental cambia de
"almacenamiento de información" a "instrumento legal
ejecutable".

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Documento {
     - contenido : String
     - titulo : String
     + editar()
     + mostrar()
   }

   class ContratoCorporativo {
     - firmantes : List
     - estado_legal : String
     + ejecutar()
     + validar()
     + revocar()
   }

   Documento <|-- ContratoCorporativo
   note right of ContratoCorporativo
     Mantiene estructura de Documento,
     pero el concepto se transforma:
     "almacena informacion" se convierte
     en "instrumento legal ejecutable".
     Requiere ADR explicito.
   end note
   @enduml

Cuándo es apropiada
~~~~~~~~~~~~~~~~~~~

- El cambio conceptual es parte **natural** del dominio.
- La transformación mantiene cierta **coherencia** con el
  concepto original.
- Existe una **justificación clara** del negocio.
- La relación transformativa es **intuitiva** para el
  experto del dominio.

Consideraciones de diseño
~~~~~~~~~~~~~~~~~~~~~~~~~

- **Evaluar si la transformación es realmente necesaria**.
- **Documentar claramente** el cambio conceptual en un ADR.
- Asegurar que la transformación tiene sentido en el
  dominio.
- Mantener la **coherencia** del sistema.

Cuándo aparece en IACT
~~~~~~~~~~~~~~~~~~~~~~

Casos posibles, todos requieren ADR del subdominio antes
de adoptarlos:

- ``Reporte`` → ``ReporteAuditoria`` con paquete firmado.
  Mantiene la estructura de un ``Reporte`` (genera,
  exporta) pero el concepto se transforma: pasa de
  "consulta operativa" a "evidencia auditable
  certificada".
- ``EventoAuditoria`` → ``EventoLegal`` para auditorías
  externas regulatorias. Mantiene la estructura del
  evento pero gana semántica de prueba legal — el cambio
  obliga a revisar CNST_025 (immutable) en términos
  legales, no solo operativos.
- ``Sesion`` → ``SesionDelegada``. Estructura de sesión
  preservada, pero el concepto se transforma: pasa de
  "usuario autenticado" a "usuario actuando en nombre de
  otro" (raro en IACT por CNST_002, pero documentado
  aquí como ejemplo de transformación discutible).

Advertencia
~~~~~~~~~~~

Debe utilizarse con **precaución**: una transformación
conceptual demasiado radical podría indicar que la
herencia **no es la mejor estrategia** para ese caso. La
clave es asegurar que la transformación es una **evolución
natural y lógica** del concepto base, no una desviación
arbitraria que comprometa la integridad del diseño. Ante
duda, **componer** (ver § 15) o aplicar un patrón
(:doc:`patrones-diseno`).

14.3 Herencia por construcción (evitar)
---------------------------------------

La **herencia por construcción** (*inheritance by
construction*) es un error de diseño que ocurre cuando se
usa la herencia entre clases **únicamente para reutilizar
código y funcionalidad**, sin que exista una relación
jerárquica verdadera entre ellas.

Las dos relaciones legítimas en OOP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **"Es-un" (IS-A)** — justifica la herencia. Un
  ``ReporteVolumen`` *es-un* ``Reporte``.
- **"Tiene-un" (HAS-A)** — indica composición. Un
  ``Reporte`` *tiene-un* ``EscritorCSV``.

La herencia por construcción **viola estos principios** al
crear una relación "es-un" artificial solo para acceder a
cierta funcionalidad. El resultado es lo que en diseño se
llama **acoplamiento impropio** (*improper coupling*).

Por qué es incorrecta
~~~~~~~~~~~~~~~~~~~~~

1. **Motivo erróneo**: se usa herencia solo para reutilizar
   código; no existe verdadera relación jerárquica; se
   busca un "atajo" para acceder a funcionalidad existente.
2. **Consecuencias negativas**: relaciones artificiales
   entre clases, acoplamiento innecesariamente alto,
   violación del **Liskov Substitution Principle**,
   mantenimiento más difícil.

Excepción parcial — C++
~~~~~~~~~~~~~~~~~~~~~~~

La única excepción parcial existe en C++ a través de la
**herencia privada**, que puede usarse como una forma de
implementación de composición. Aún así, la composición
directa suele ser una mejor opción. En lenguajes que no
tienen ese mecanismo (Python, Java, JavaScript, TypeScript,
C#, etc.), la herencia por construcción debe **evitarse
completamente**.

IACT usa Python/Django (ver ADR_DEVOPS_001) — la excepción
**no aplica**. Toda aparición de herencia por construcción
en este proyecto es un defecto.

Ejemplo canónico — ``Documento`` y ``BaseDeDatos``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando una clase ``Documento`` hereda de ``BaseDeDatos``
solo para obtener métodos de persistencia, hay herencia por
construcción. Un documento **no es-una** base de datos —
es una violación semántica clara.

Diseño incorrecto (herencia por construcción):

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Diseno incorrecto — herencia por construccion

   class BaseDeDatos {
     + guardar()
     + cargar()
     + eliminar()
   }

   class Documento {
     - contenido : String
     - titulo : String
     + editarContenido()
     + mostrarDocumento()
   }

   Documento --|> BaseDeDatos
   note right of Documento
     Documento NO es-una BaseDeDatos.
     La herencia miente sobre el dominio.
   end note
   @enduml

Diseño correcto (composición):

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Diseno correcto — composicion

   class BaseDeDatos {
     + guardar()
     + cargar()
     + eliminar()
   }

   class DocumentoCorrecto {
     - contenido : String
     - titulo : String
     - persistencia : BaseDeDatos
     + editarContenido()
     + mostrarDocumento()
     + guardarDocumento()
   }

   DocumentoCorrecto o-- BaseDeDatos : tiene-un
   note right of DocumentoCorrecto
     DocumentoCorrecto tiene-un
     BaseDeDatos como componente
     (composicion).
   end note
   @enduml

Ejemplo aplicado a IACT
~~~~~~~~~~~~~~~~~~~~~~~

- **Incorrecto**: ``Reporte`` heredando de ``UtilsArchivo``
  solo para reutilizar ``escribir_csv``. Un ``Reporte``
  **no es-una** utilidad de archivo.
- **Correcto**: ``Reporte`` componiendo un
  ``EscritorCSV`` (Strategy, ver
  :doc:`patrones-diseno`) — el reporte *tiene-un*
  escritor que puede intercambiarse en runtime.

Otros casos típicos en IACT donde aparecería el
antipatrón:

- ``EjecucionETL`` heredando de ``LoggerBase`` para usar
  ``log_info``/``log_error``. Una ejecución no es un
  logger; el logger se inyecta.
- ``Reporte`` heredando de ``HttpResponseHelper`` para
  servir el archivo. Un reporte no es una respuesta HTTP;
  la vista compone ambas.
- ``EvaluadorAlertas`` heredando de ``CronJobBase``
  porque el scheduler invoca ``run()``. La cron task se
  modela como composición o adapter, no por herencia.

Solución
~~~~~~~~

1. Usar **composición** en lugar de herencia.
2. **Inyectar** la dependencia (constructor o factory).
3. **Delegar** la funcionalidad requerida al objeto
   compuesto.

Regla principal
~~~~~~~~~~~~~~~

Usa herencia **solo cuando existe una verdadera relación
"es-un"**; en cualquier otro caso, composición.

14.4 Herencia por limitación (evitar)
-------------------------------------

La **herencia por limitación** (*restriction inheritance*)
ocurre cuando una clase hija hereda de una clase padre
pero **no implementa o restringe** algunas de las
operaciones heredadas. Es una **violación grave** del
*Liskov Substitution Principle* (LSP): los objetos de la
clase base deben poder ser reemplazados por objetos de
sus clases derivadas sin afectar la corrección del
programa.

Cuando una hija limita o no implementa funcionalidades del
padre, este principio se rompe.

Violación del contrato
~~~~~~~~~~~~~~~~~~~~~~

- La clase hija **no cumple el contrato completo** del
  padre.
- Restringe o no implementa ciertas operaciones
  heredadas.
- Rompe las expectativas de comportamiento.

Consecuencias técnicas
~~~~~~~~~~~~~~~~~~~~~~

1. **Imposibilidad de sustituir** objetos de la clase base
   por objetos de la derivada de manera segura.
2. **Violación de Design by Contract**: precondiciones,
   postcondiciones e invariantes del padre dejan de ser
   confiables en la hija.
3. **Jerarquías frágiles** y propensas a errores.
4. **Reducción significativa de la reusabilidad** del
   código.

Por qué imposibilita el polimorfismo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El polimorfismo requiere poder tratar **cualquier objeto
de una clase derivada como si fuera de su clase base**.
Cuando se limitan operaciones en la hija, esto deja de
ser cierto: el código cliente debe **conocer las
limitaciones específicas** de cada subtipo, perdiendo el
beneficio del despacho dinámico.

Síntomas comunes
~~~~~~~~~~~~~~~~

- Métodos heredados que lanzan ``NotImplementedError`` o
  excepciones para desactivar operaciones del padre.
- Implementaciones vacías (``pass``).
- Comentarios "no soportado", "no implementado", "esto
  no aplica para este subtipo".
- Comportamientos inesperados o silenciosos en la clase
  hija.

Ejemplo canónico — ``Ave`` con ``Pinguino``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una clase base ``Ave`` con el método ``volar()``. Si
``Pinguino`` hereda de ``Ave`` pero no puede implementar
``volar()`` apropiadamente, hay herencia por limitación —
el pingüino limita una capacidad que se supone debería
tener por ser un ``Ave``.

Diseño incorrecto:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Diseno incorrecto — herencia por limitacion

   class Ave {
     # nombre : String
     # peso : Double
     + volar()
     + comer()
     + getNombre()
     + getPeso()
   }

   class Pinguino {
     - velocidadNado : Double
     + volar()
     + nadar()
     + getVelocidadNado()
   }

   Ave <|-- Pinguino
   note right of Pinguino
     volar() no puede
     implementarse correctamente.
     Viola el principio LSP.
   end note
   @enduml

Diseño correcto — interfaces para separar comportamientos:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   title Diseno correcto — interfaces

   class Ave {
     # nombre : String
     # peso : Double
     + comer()
     + getNombre()
     + getPeso()
   }

   interface IAveVoladora {
     + volar()
   }

   interface IAveNadadora {
     + nadar()
   }

   class Aguila {
     - altitudMaxima : Double
     + volar()
     + getAltitudMaxima()
   }

   class Pinguino {
     - velocidadNado : Double
     + nadar()
     + getVelocidadNado()
   }

   Ave <|-- Aguila
   Ave <|-- Pinguino
   IAveVoladora <|.. Aguila
   IAveNadadora <|.. Pinguino

   note left of Ave : Comportamientos comunes
   note right of IAveVoladora : Define vuelo
   note right of IAveNadadora : Define nado
   @enduml

Lectura del diseño correcto:

- ``Ave`` queda con los comportamientos **comunes a todas
  las aves** (``comer``, atributos, getters).
- Las interfaces ``IAveVoladora`` e ``IAveNadadora``
  declaran capacidades específicas.
- ``Aguila`` hereda ``Ave`` **e implementa**
  ``IAveVoladora``.
- ``Pinguino`` hereda ``Ave`` **e implementa**
  ``IAveNadadora``.
- Cada clase implementa **solo las interfaces que tienen
  sentido** para su comportamiento natural.

Ventajas:

- Respeta LSP — ninguna clase oculta operaciones
  heredadas.
- Más flexible — agregar nuevas capacidades mediante
  interfaces.
- Más mantenible — cambios en "volar" solo afectan a
  quienes realmente lo implementan.
- Más extensible — fácil agregar aves con diferentes
  combinaciones de capacidades.

Aplicación a IACT
~~~~~~~~~~~~~~~~~

Casos típicos donde aparecería el antipatrón:

- ``ReporteSoloLectura`` heredando de ``Reporte`` y
  lanzando excepción en ``exportar()``. Si no se puede
  exportar, **no es** un ``Reporte`` en el sentido del
  contrato. Modelar como interfaces separadas:

  - ``Reporte`` (base con ``generar()``).
  - ``IExportable`` (con ``exportar(formato)``).
  - ``IConsultable`` (con ``consultar()``).

  Y dejar que ``ReporteVolumen`` implemente ambas y
  ``ReporteSoloLectura`` implemente solo ``IConsultable``.
- ``EventoAuditoriaInterno`` heredando de
  ``EventoAuditoria`` y bloqueando ``exportar_legal()``.
  Mejor: dos interfaces ``IExportableInterno`` e
  ``IExportableLegal``.
- ``UsuarioInactivo`` heredando de ``Usuario`` y
  desactivando ``iniciar_sesion()`` lanzando excepción.
  Modelarlo con un atributo de estado y composición —
  el usuario *tiene un* estado, no *es* un tipo distinto.

Soluciones generales
~~~~~~~~~~~~~~~~~~~~

- **Reevaluar la jerarquía** — probable señal de que la
  abstracción está mal trazada.
- Usar **interfaces más específicas** que separen
  capacidades.
- Usar **composición** en lugar de herencia.
- Crear **abstracciones más apropiadas** —
  frecuentemente, una jerarquía con limitación oculta dos
  conceptos que merecen abstracciones separadas.

Regla clave
~~~~~~~~~~~

**Si una clase hija no puede cumplir completamente con el
contrato de su padre, la relación de herencia no es
apropiada.** Reemplazarla por interfaces o composición
(ver § 15).

14.5 Tabla resumen
------------------

.. list-table::
 :widths: 22 22 22 17 17
 :header-rows: 1

 * - Tipo
   - Naturaleza
   - LSP
   - Recomendación
   - En IACT
 * - Especialización
   - "es-un" verdadero, expande.
   - Cumple
   - Recomendada
   - ``Reporte`` → familia ``Reporte*``
 * - Extensión con transformación
   - Cambia el concepto, mantiene estructura.
   - Frágil
   - Solo con ADR
   - ``Reporte`` → ``ReporteAuditoria`` con paquete
     firmado
 * - Construcción
   - Reutilización sin "es-un".
   - No cumple
   - Evitar
   - ``Reporte`` ← ``UtilsArchivo`` (incorrecto)
 * - Limitación
   - Restringe / desactiva.
   - No cumple
   - Evitar
   - ``Reporte`` con subclases que rompen ``exportar()``

Regla integradora IACT
----------------------

Antes de definir una herencia, responder:

1. ¿La hija **es realmente** una variante del padre, o
   solo necesita su código?
2. ¿La hija puede sustituir al padre en cualquier
   contrato del padre (LSP)?
3. Si la respuesta a 1 o 2 es "no", reemplazar la
   herencia por **composición** o **interfaces**.

Esta regla es coherente con § 12 de
:doc:`orientacion-objetos` (antipatrón Descomposición
Funcional) y con la sección de patrones
:doc:`patrones-diseno` (Adapter, Strategy, Decorator
suelen ser la respuesta cuando la herencia no encaja).

----

15. Comparativa herencia vs composición
=======================================

La § 14 fija criterios sobre **cuándo** la herencia es
válida. Esta sección plantea la pregunta complementaria:
**herencia o composición** cuando ambas son técnicamente
posibles. La respuesta corta — y la que adopta IACT por
defecto — es: **componer salvo que el "es-un" sea
inequívoco**.

15.1 Tabla comparativa
----------------------

.. list-table::
 :widths: 22 39 39
 :header-rows: 1

 * - Aspecto
   - Composición (HAS-A)
   - Herencia (IS-A)
 * - Tipo de relación
   - "tiene un" (contiene una parte).
   - "es un" (es una variante de).
 * - Definición básica
   - Un objeto contiene otros objetos.
   - Una clase deriva o extiende de otra.
 * - Naturaleza del vínculo
   - Propiedad / contenencia.
   - Especialización.
 * - Ejemplo práctico
   - Un propietario tiene un coche.
   - Un ingeniero de software es un ingeniero.
 * - Acoplamiento
   - Bajo entre componentes.
   - Alto entre clases.
 * - Flexibilidad
   - Alta: permite cambios en runtime.
   - Baja: estructura rígida y estática.
 * - Reutilización
   - Horizontal (a través de componentes).
   - Vertical (a través de la jerarquía).
 * - Cardinalidad
   - Puede contener múltiples instancias (>1).
   - Típicamente herencia simple (1 padre).
 * - Modificabilidad
   - Fácil de modificar y adaptar.
   - Cambios pueden afectar toda la jerarquía.
 * - Mantenimiento
   - Más sencillo: componentes independientes.
   - Más complejo: dependencias jerárquicas.
 * - Caso de uso ideal
   - Flexibilidad y bajo acoplamiento.
   - Relación "es-un" clara y estable.
 * - Recomendación
   - **Preferida en caso de duda.**
   - Solo cuando la relación "es-un" es inequívoca.

15.2 Aplicación a IACT
----------------------

.. list-table::
 :widths: 30 35 35
 :header-rows: 1

 * - Caso
   - Decisión
   - Por qué
 * - ``Reporte`` y los formatos de export
   - Composición — ``Reporte`` *tiene un*
     ``FormatoExport`` (Strategy, ver
     :doc:`patrones-diseno`).
   - Cambiar de CSV a XLSX no debe alterar el árbol
     de clases del reporte. Composición permite
     intercambio en runtime.
 * - ``Reporte`` y sus variantes
     (``ReporteVolumen``, ``ReporteAbandono``)
   - Herencia — *son* reportes.
   - LSP se cumple: cualquier subclase puede
     responder al contrato común
     (``generar()``, ``exportar()``).
 * - ``Sesion`` y ``Usuario``
   - Composición — la sesión *tiene un* usuario.
   - Una sesión no es una variante de usuario;
     contiene una referencia. Permite caducar
     sesión sin tocar usuario (CNST_002).
 * - ``Alerta`` y ``EvaluadorAlertas``
   - Composición — la alerta *tiene un*
     evaluador (Strategy).
   - Cambiar la regla de evaluación (umbral,
     tendencia) no debe forzar nuevas subclases de
     ``Alerta``.
 * - ``ReporteAuditoria`` con paquete firmado
   - Herencia con transformación (§ 14.2) — solo
     si hay ADR.
   - El "es-un" se sostiene en estructura técnica
     pero el concepto se transforma; evaluar si
     composición + decorador firma sería más
     claro.
 * - ``Reporte`` y utilidades de archivo
   - Composición — el reporte *usa* un escritor;
     **nunca hereda** de él.
   - Heredar de ``UtilsArchivo`` sería herencia
     por construcción (§ 14.3, evitar).
 * - ``EjecucionETL`` y ``ErrorETL``
   - Composición — la ejecución *tiene*
     errores como partes (composición fuerte).
   - Los errores no existen sin la ejecución
     (CNST_006/008); su vida está ligada.

15.3 Reglas IACT por defecto
----------------------------

1. **Composición salvo "es-un" inequívoco.** Ante duda,
   componer.
2. **Si hay duda LSP, no heredar.** Si en algún
   subtipo previsible el contrato del padre se rompe,
   pasar a composición + interfaz.
3. **Una sola jerarquía por cluster** (ver § 11 de
   :doc:`agregacion-interfaces`). Si dos jerarquías
   compiten por el mismo concepto, casi siempre conviene
   convertir una en interfaz y componer.
4. **Ningún reporte/alerta/permiso hereda de
   utilidades.** La utilidad se inyecta o se compone.
5. **La herencia se documenta en el ADR del cluster**
   cuando es central; la composición típicamente no
   requiere ADR salvo que cambie un contrato público.

15.4 Relación con patrones GoF
------------------------------

Cuando la herencia no encaja, los patrones de
:doc:`patrones-diseno` resuelven la mayoría de los casos
con composición:

- **Strategy** sustituye una jerarquía de "variantes que
  cambian un algoritmo" por composición con interfaz
  (export CSV/XLSX/JSON).
- **Decorator** evita una jerarquía explosiva de
  combinaciones (firma + cifrado + compresión) por
  composición encadenada.
- **Adapter** evita herencia "para cuadrar contratos" de
  fuentes externas (LDAP) componiendo el origen.
- **Composite** modela jerarquías de partes con
  composición + recursión, no con herencia.

----

16. Principios fundamentales de la herencia y guía de decisión
==============================================================

Las §§ 14-15 detallan los **cuatro tipos de herencia** y la
**comparativa con composición**. Esta sección consolida los
**principios fundamentales** que rigen cualquier decisión
sobre herencia y ofrece una **guía de decisión** operativa
para cada nueva clase del proyecto IACT.

16.1 Tres principios fundamentales
----------------------------------

Relación natural ("es-un")
~~~~~~~~~~~~~~~~~~~~~~~~~~

- La herencia debe utilizarse **exclusivamente** cuando
  existe una verdadera relación **"es-un" (is-a)**.
- La relación debe reflejar una **jerarquía natural del
  dominio del problema** — no una conveniencia técnica.
- Si la relación no es clara o natural, considerar la
  **composición** como alternativa (§ 15).

En IACT: ``ReporteVolumen`` *es-un* ``Reporte``,
``EventoAuditoriaAcceso`` *es-un* ``EventoAuditoria``,
``AlertaPublicada`` *es-un* ``EstadoAlerta``. Cualquier
relación que no encaje naturalmente en este molde —
"el reporte es-un escritor de archivos" — es una señal
para componer.

Principio de Sustitución de Liskov
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Comportamiento consistente.** La clase hija debe poder
**sustituir** a la clase padre en cualquier contexto sin
afectar la corrección del programa. El comportamiento de
la hija debe mantener las expectativas establecidas por el
padre. Ver detalles formales en § 18 de
:doc:`orientacion-objetos`.

**Contrato de interfaz.** La clase hija debe **respetar
todas las precondiciones y postcondiciones** definidas por
el padre (Design by Contract; ver § 21.4 de
:doc:`orientacion-objetos`). Si una hija no puede cumplir
completamente con el contrato del padre, la herencia
**no es apropiada**.

Documentación y contexto
~~~~~~~~~~~~~~~~~~~~~~~~

- La transformación conceptual entre padre e hija debe
  **tener sentido en el contexto específico** del
  problema.
- Las decisiones de diseño y las relaciones de herencia
  deben estar **claramente documentadas** — preferiblemente
  en un ADR del subdominio cuando la herencia es central
  al cluster (ver § 11 de :doc:`agregacion-interfaces`).
- El **propósito y las responsabilidades** de cada nivel
  de la jerarquía deben ser **explícitos**.

16.2 Síntesis de los cuatro tipos de herencia
---------------------------------------------

Tabla recapitulativa que enlaza con las §§ 14.1-14.4:

.. list-table::
 :widths: 22 22 26 30
 :header-rows: 1

 * - Tipo
   - Naturaleza
   - Cumple LSP
   - Recomendación IACT
 * - **Especialización** (§ 14.1)
   - "es-un" verdadera con expansión.
   - Sí.
   - **Recomendada** — el patrón canónico.
 * - **Extensión con transformación** (§ 14.2)
   - "se transforma en" — cambia concepto, mantiene
     estructura.
   - Frágil — depende del caso.
   - Solo con **ADR explícito** del subdominio.
 * - **Construcción** (§ 14.3)
   - Reutilizar código sin "es-un".
   - **No.**
   - **Evitar** — usar composición / inyección.
 * - **Limitación** (§ 14.4)
   - Restringe o desactiva operaciones heredadas.
   - **No.**
   - **Evitar** — separar interfaces o componer.

16.3 Guía de decisión operativa
-------------------------------

Antes de implementar una herencia, **responder estas tres
preguntas**:

1. ¿Existe una **verdadera relación "es-un"**?
2. ¿La clase hija **puede cumplir completamente** con el
   contrato del padre (LSP)?
3. ¿La sustitución **tiene sentido en todos los contextos
   de uso** previstos?

Si la respuesta es "**no**" a **cualquiera** de las tres:

- **Considerar composición** en lugar de herencia
  (§ 15).
- **Evaluar si la abstracción necesita rediseño** —
  posiblemente la jerarquía está mal modelada.
- **Verificar la distribución de responsabilidades** —
  posiblemente SRP se está violando (ver § 17 de
  :doc:`orientacion-objetos`).

Diagrama de decisión (texto)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   ¿La relación es "es-un" verdadera?
   ├── No  → Composición (§ 15) o interfaces (ISP)
   └── Sí
       ↓
   ¿La hija cumple LSP completamente?
   ├── No  → Composición o interfaces específicas (§ 14.4)
   └── Sí
       ↓
   ¿La sustitución tiene sentido en todos los contextos?
   ├── No  → Reevaluar abstracción + responsabilidades
   └── Sí
       ↓
   ¿El concepto de la hija difiere fundamentalmente
   del padre (transformación)?
   ├── Sí  → Herencia por extensión (§ 14.2) — requiere ADR
   └── No  → Herencia por especialización (§ 14.1) ✓ recomendada

16.4 Aplicación al proyecto IACT
--------------------------------

Validación rápida para cada herencia que se proponga en
una app Django:

.. list-table::
 :widths: 30 35 35
 :header-rows: 1

 * - Pregunta
   - Decisión correcta
   - Decisión incorrecta
 * - ``Reporte`` ← ``ReporteVolumen``
   - Especialización (§ 14.1) — es-un, cumple LSP.
   - —
 * - ``Reporte`` ← ``ReporteAuditoria`` (paquete firmado)
   - Extensión con transformación + ADR (§ 14.2).
   - Especialización implícita sin documentar el
     cambio conceptual.
 * - ``Reporte`` ← ``UtilsArchivo``
   - **Evitar** — composición ``EscritorCSV``
     (§ 14.3).
   - Herencia por construcción.
 * - ``Ave`` ← ``Pinguino`` con ``volar()`` desactivado
   - **Evitar** — separar ``IAveVoladora``,
     ``IAveNadadora`` (§ 14.4).
   - Herencia por limitación.
 * - ``Sesion`` ↔ ``Usuario``
   - **Composición** — la sesión *tiene un* usuario.
   - Heredar de ``Usuario`` para reutilizar campos.

16.5 Cierre
-----------

La herencia es la **herramienta más poderosa y más abusada**
de OOP. Aplicada con disciplina (LSP + "es-un" + contexto)
es la base del polimorfismo seguro y de patrones GoF como
Strategy, Template Method y Composite (ver
:doc:`patrones-diseno`). Aplicada por inercia o conveniencia
produce los antipatrones de § 14.3 y § 14.4 — y deuda
técnica que se solidifica como flujo de lava (§ 13 de
:doc:`orientacion-objetos`).

La regla integradora: **componer salvo que el "es-un" sea
inequívoco y la sustituibilidad LSP esté asegurada**.

----

17. Trazabilidad
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
   - :doc:`diagramas-uml`,
     :doc:`orientacion-objetos`,
     :doc:`analisis-dominio`
 * - **Plan de documentación**
   - :doc:`plan-documentacion-uc`
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
