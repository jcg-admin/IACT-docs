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

Relación **"es-un" verdadera** con expansión de
comportamiento.

- Mantiene el comportamiento base del padre.
- Añade características específicas.
- No elimina funcionalidades.
- Respeta el contrato original (LSP).

Beneficios: jerarquías naturales, mantenimiento más
sencillo, reusabilidad, extensiones seguras.

**Cuándo usarla**: cuando exista relación clara de
subtipo, la especialización sea natural y no viole LSP.

**Mejores prácticas**: implementar todas las operaciones,
mantener cohesión, respetar propósito original, seguir
principios SOLID.

**Regla principal**: si una clase hija no puede cumplir
completamente con el contrato de su padre, la herencia
no es apropiada.

Ejemplo IACT correcto:

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

Cada subclase **mantiene** ``generar()`` y ``exportar()`` y
**añade** su lógica específica de cálculo. Ningún subtipo
rompe el contrato del padre.

14.2 Herencia por extensión con transformación (con cuidado)
------------------------------------------------------------

Modifica el concepto fundamental mientras mantiene la
estructura técnica.

- Va más allá de "es-un": transforma el concepto.
- Mantiene estructura técnica del padre.
- Puede confundir a desarrolladores que esperan
  comportamiento heredado intacto.
- Complica el modelo de dominio si no se justifica.

**Usar con precaución**: solo cuando la transformación es
natural y tiene sentido en el dominio.

**Mejores prácticas**: documentar el cambio conceptual,
asegurar coherencia, justificar la necesidad
explícitamente en un ADR.

Ejemplo IACT donde puede aparecer:

- ``ReporteAuditoria`` que hereda de ``Reporte`` pero
  cambia la semántica de "exportar" para producir un
  paquete firmado en lugar de un archivo plano. La forma
  técnica es la misma; el concepto cambia. Justificarlo
  en ADR del subdominio antes de adoptarlo.

14.3 Herencia por construcción (evitar)
---------------------------------------

Uso **incorrecto** de herencia solo para reutilizar código,
sin relación jerárquica verdadera.

- Se usa solo para reutilizar código.
- No existe relación "es-un".
- Busca atajos para acceder a funcionalidad.

Consecuencias: relaciones artificiales, acoplamiento
innecesario, violación de LSP, mantenimiento difícil.

**Evitar siempre.**

Ejemplo incorrecto en IACT:

- ``Reporte`` que hereda de ``UtilsArchivo`` solo para
  reutilizar ``escribir_csv``. Un reporte **no es** una
  utilidad de archivo: la herencia miente sobre el
  dominio.

**Solución**: composición o inyección. Pasar un
``EscritorCSV`` al ``Reporte`` como dependencia, o
delegar la operación a un servicio.

14.4 Herencia por limitación (evitar)
-------------------------------------

La clase hija **no implementa o restringe** operaciones
heredadas.

- No cumple el contrato del padre.
- Restringe operaciones heredadas.
- Rompe expectativas de comportamiento.

Consecuencias: violación de LSP, inconsistencias, código
frágil, reusabilidad reducida.

Señales de advertencia:

- Métodos que lanzan ``NotImplementedError`` para
  desactivar operaciones del padre.
- Implementaciones vacías (``pass``) en métodos heredados.
- Comentarios "esto no aplica para este subtipo".

**Evitar.** Indica que la jerarquía está mal modelada.

Ejemplo incorrecto en IACT:

- ``ReporteSoloLectura`` heredando de ``Reporte`` y
  lanzando excepción en ``exportar()``. Si no se puede
  exportar, no es un ``Reporte`` en el sentido del
  contrato — modelar como interfaz separada
  ``ReporteVisualizable`` y dejar ``Reporte`` solo para
  los que sí soportan ``exportar()``.

**Solución**: reevaluar jerarquía, usar **interfaces
específicas** o **composición**, crear abstracciones
mejor delimitadas.

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

16. Trazabilidad
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
