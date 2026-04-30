.. meta::
 :artefacto: METODOLOGIA_UC_DIAGRAMAS_IACT
 :tipo: Guia
 :dominio: requisitos
 :subdominio: _metodologia-aplicacion
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==================================================================
Casos de uso — diagramas (modelado visual aplicado a IACT)
==================================================================

.. note::

 Compañero de :doc:`casos-uso-especificacion` (la
 especificación textual de un UC). Este documento cubre la
 **dimensión visual** — cómo crear el diagrama de casos de
 uso que acompaña a la especificación.

 Adapta la **Hora 7 de Schmuller** ("Diagramas de casos de
 uso") al dominio real del proyecto IACT (call center IVR +
 analytics + RBAC + ETL).

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 Para la teoría genérica ver
 :doc:`/base-cognitiva/_uml/uml-07-diagramas-casos-uso`
 (Schmuller Hora 7).

----

1. Comunicar requisitos visualmente
===================================

  *Los usuarios con frecuencia saben más de lo que dicen.*

**Solución:** los diagramas de casos de uso convierten el
análisis en **imágenes claras** que todos entienden.

**Objetivo:** comunicar requisitos funcionales de forma
visual y clara.

----

2. Componentes del diagrama
===========================

2.1 Símbolos básicos
--------------------

::

 ┌─────────────────────────────────────────┐
 │  LÍMITE DEL SISTEMA (rectángulo)        │
 │                                         │
 │     ◯◯◯◯◯◯                              │
 │    (Caso de uso — elipse)               │
 │        │                                │
 │        │ línea asociativa               │
 │        │                                │
 │     ╱─┼─╲                               │
 │    │     │                              │
 │    └─────┘                              │
 │  ACTOR                                  │
 │  (figura de palo)                       │
 └─────────────────────────────────────────┘

2.2 Posicionamiento
-------------------

::

 ACTOR INICIADOR        CASO DE USO        ACTOR BENEFICIARIO
 (izquierda)            (centro)           (derecha)
        │                  │                      │
        └──────────────────●─────────────────────→│
                  (puede ser el mismo)

----

3. Ejemplo visual — Máquina de gaseosas (referencia genérica)
=============================================================

Diagrama clásico de Schmuller que sirve de base conceptual:

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction
   actor Cliente
   actor "Representante\ndel proveedor" as Proveedor
   actor Recolector
   actor Tiempo

   rectangle "Máquina de Gaseosas" {
     usecase "Comprar gaseosa"      as UC1
     usecase "Reabastecer"          as UC2
     usecase "Recolectar el dinero" as UC3
   }

   Cliente    --> UC1
   Proveedor  --> UC2
   Recolector --> UC3
   Tiempo     --> UC2
   Tiempo     --> UC3
   @enduml

----

4. Ejemplo IACT — diagrama de alto nivel
========================================

Diagrama del **sistema completo IACT** mostrando los UCs
operativos clave por dominio funcional, con sus actores
internos y externos.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction

   actor Operador
   actor Supervisor
   actor "Admin\nAcceso"     as AA
   actor "Admin\nPipeline"   as AP
   actor Auditor
   actor "Sistema /\nScheduler" as Sched
   actor "IVR\nConmutador"  as IVR

   rectangle "IACT" {
     usecase "UC_AUTH_01\nIniciar sesión"     as AUTH01
     usecase "UC_RPT_01\nVer dashboard"       as RPT01
     usecase "UC_RPT_04\nExportar reporte"    as RPT04
     usecase "UC_ALR_03\nReconocer alerta"    as ALR03
     usecase "UC_ACC_01\nAsignar funciones"   as ACC01
     usecase "UC_PERM_07\nVerificar permiso"  as PERM07
     usecase "UC_PIP_01\nSupervisar ETL"      as PIP01
     usecase "UC_PIP_04\nSolicitar reintento" as PIP04
     usecase "UC_AUD_01\nConsultar auditoría" as AUD01
     usecase "UC_AUD_03\nExportar auditoría"  as AUD03
     usecase "Carga ETL\nnocturna"            as ETL
   }

   Operador   --> AUTH01
   Operador   --> RPT01
   Operador   --> RPT04
   Operador   --> ALR03

   Supervisor --> AUTH01
   Supervisor --> RPT04
   Supervisor --> ALR03

   AA         --> ACC01
   AP         --> PIP01
   AP         --> PIP04
   Auditor    --> AUD01
   Auditor    --> AUD03

   Sched      --> ETL
   IVR        <-- ETL

   RPT01      ..> PERM07 : <<include>>
   RPT04      ..> PERM07 : <<include>>
   ACC01      ..> PERM07 : <<include>>
   AUD01      ..> PERM07 : <<include>>
   PIP04      ..> PERM07 : <<include>>
   @enduml

**Lectura del diagrama:**

- Cinco actores **operativos** (Operador, Supervisor,
  AdminAcceso, AdminPipeline, Auditor) inician UCs
  específicos según su rol.
- Dos actores **sistema/externos** (Scheduler y IVR
  Conmutador) participan en la carga ETL.
- ``UC_PERM_07`` (verificar permiso) es **incluido por
  todos** los UCs operativos — es el equivalente IACT a
  *"abrir la máquina"* del ejemplo del libro.

----

5. Inclusión en diagrama (``<<include>>``)
==========================================

**Concepto:** un UC **incluye** los pasos de otro. Reutiliza
y elimina duplicación.

**Notación:** línea discontinua con flecha + estereotipo
``<<include>>``.

5.1 Ejemplo IACT — UC_RPT_04 (Exportar reporte)
-----------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction
   actor Supervisor

   rectangle "IACT" {
     usecase "UC_RPT_04\nExportar reporte"  as RPT04
     usecase "UC_RPT_03\nVer reportes\nhistóricos"   as RPT03
     usecase "UC_PERM_07\nVerificar permiso\n+ throttling\nCNST_020"            as PERM
     usecase "Aplicar filtro\nsegmento\n(BR_012,\nCNST_008)"                    as SEG
     usecase "Registrar en\nAuditLog\n(CNST_025)"                               as AUD
   }

   Supervisor --> RPT04

   RPT04 ..> PERM  : <<include>>
   RPT04 ..> RPT03 : <<include>>
   RPT04 ..> SEG   : <<include>>
   RPT04 ..> AUD   : <<include>>

   note right of RPT04
     UC_RPT_04 INCLUYE:
       - Verificar permiso del formato
         (CSV / Excel / PDF) con
         throttling diario CNST_020
       - Ver reporte histórico que se
         exporta (UC_RPT_03)
       - Aplicar filtro de segmento
         del usuario (BR_012)
       - Registrar export en
         AuditLog inmutable (CNST_025)
   end note
   @enduml

----

6. Extensión en diagrama (``<<extend>>``)
=========================================

**Concepto:** un UC **extiende** otro agregando pasos en
**puntos de extensión específicos**.

**Notación:** línea discontinua con flecha + estereotipo
``<<extend>>`` apuntando al caso base.

6.1 Ejemplo IACT — UC_RPT_03 (Ver reportes históricos) extendido
----------------------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction
   actor Supervisor

   rectangle "IACT" {
     usecase "UC_RPT_03\nVer reportes\nhistóricos\n.. extension points ..\nresultados listados\nen pantalla"   as RPT03
     usecase "UC_RPT_09\nConfigurar filtros"          as RPT09
     usecase "UC_RPT_10\nGuardar vista"               as RPT10
     usecase "UC_RPT_11\nCompartir reporte"           as RPT11
   }

   Supervisor --> RPT03

   RPT09 ..> RPT03 : <<extend>>\n(resultados listados)
   RPT10 ..> RPT03 : <<extend>>\n(resultados listados)
   RPT11 ..> RPT03 : <<extend>>\n(resultados listados)

   note right of RPT03
     Punto de extensión:
       "resultados listados en pantalla"

     UC_RPT_03 (base) puede ser
     extendido opcionalmente por:
       - UC_RPT_09 (configurar filtros)
       - UC_RPT_10 (guardar vista actual)
       - UC_RPT_11 (compartir vía link)
     Las extensiones son opcionales,
     no obligatorias.
   end note
   @enduml

----

7. Generalización en diagrama
=============================

**Concepto:** un UC **hereda** de otro. El secundario
hereda acciones del primario y agrega las propias.

**Notación:** línea continua con triángulo vacío apuntando
al caso primario.

7.1 Ejemplo IACT — UC_AUTH_01 con variante 2FA
----------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction
   actor Usuario

   rectangle "IACT" {
     usecase "UC_AUTH_01\nIniciar sesión\n(BASE)"       as A1
     usecase "UC_AUTH_01b\nIniciar sesión\ncon 2FA"     as A1B
   }

   Usuario --> A1
   Usuario --> A1B

   A1B --|> A1

   note right of A1B
     UC_AUTH_01b HEREDA de UC_AUTH_01:
       + paso adicional de verificación
         del segundo factor (TOTP / SMS
         interno) tras validar password.
     Sólo aplica a usuarios con 2FA
     habilitado en su cuenta.
   end note
   @enduml

7.2 Ejemplo IACT — UC_PIP_04 con reintento parametrizado
--------------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction
   actor "Admin\nPipeline" as AP

   rectangle "IACT" {
     usecase "UC_PIP_04\nSolicitar reintento\n(BASE)"           as P4
     usecase "UC_PIP_04b\nReintentar con\nparámetros ajustados" as P4B
   }

   AP --> P4
   AP --> P4B

   P4B --|> P4

   note right of P4B
     UC_PIP_04b HEREDA de UC_PIP_04:
       + permite ajustar la ventana
         CNST_008 (6-12h) si la
         ejecución original falló por
         timeout o conexión IVR.
   end note
   @enduml

----

8. Generalización entre actores
===============================

La generalización también aplica entre **actores** — útil
para mostrar la jerarquía de roles del proyecto.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Usuario
   actor Operador
   actor Supervisor
   actor "Admin Acceso"   as AA
   actor "Admin Pipeline" as AP
   actor Auditor

   Usuario <|-- Operador
   Usuario <|-- Supervisor
   Usuario <|-- AA
   Usuario <|-- AP
   Usuario <|-- Auditor

   note right of Usuario
     Usuario base:
       login(), logout(),
       changePassword().
     Cada rol especializado
     hereda esto + agrega
     funciones específicas.
   end note
   @enduml

----

9. Agrupamiento con paquetes
============================

Los **paquetes** organizan UCs en grupos coherentes por
dominio funcional. En IACT, cada paquete corresponde a un
módulo del catálogo modular.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction
   actor Operador
   actor Supervisor
   actor "Admin Acceso"   as AA
   actor "Admin Pipeline" as AP
   actor Auditor

   rectangle "IACT" {
     package "UC_AUTH (5 UCs)" {
       usecase "Iniciar sesión"  as A1
       usecase "Cerrar sesión"   as A2
     }

     package "UC_USR (4 UCs)" {
       usecase "CRUD usuarios" as U1
     }

     package "UC_ACC (9 UCs)" {
       usecase "Asignar funciones"   as AC1
       usecase "Gestionar SoD"       as AC5
     }

     package "UC_PERM (10 UCs)" {
       usecase "Verificar permiso"   as PE7
       usecase "Generar menú\ndinámico" as PE8
     }

     package "UC_RPT (14 UCs)" {
       usecase "Ver dashboard"       as R1
       usecase "Exportar reporte"    as R4
     }

     package "UC_ALR (5 UCs)" {
       usecase "Reconocer alerta"    as AL3
     }

     package "UC_PIP (4 UCs)" {
       usecase "Supervisar ETL"      as P1
       usecase "Solicitar reintento" as P4
     }

     package "UC_AUD (4 UCs)" {
       usecase "Consultar auditoría" as AU1
     }

     package "UC_LOG (7 UCs)" {
       usecase "Consultar logs"      as L1
     }
   }

   Operador   --> A1
   Operador   --> R1
   Supervisor --> R4
   Supervisor --> AL3
   AA         --> AC1
   AA         --> AC5
   AP         --> P1
   AP         --> P4
   Auditor    --> AU1
   @enduml

**Notación de ruta:** un UC dentro de un paquete se referencia
con ``Paquete::UC`` (ej: ``UC_RPT::Ver dashboard``).

----

10. Documentar escenarios — companion textual del diagrama
==========================================================

  El diagrama sólo muestra **qué** UCs existen y cómo se
  relacionan. La **secuencia de pasos** vive en la
  especificación textual del UC.

Ver :doc:`casos-uso-especificacion` para el template
canónico textual.

Cada UC del diagrama tiene su archivo individual en
``source/requisitos/casos-uso/<modulo>/uc-<mod>-<NN>-<desc>.rst``
con flujo, alternativas, precondiciones, postcondiciones y
casos de prueba.

----

11. Flujo completo de análisis
==============================

::

 Fase 1 — Entrevistas con el cliente
   → Diagrama de clases inicial
     (ver: metodologia-analisis-dominio-ucs)

 Fase 2 — Entrevistas con usuarios
   → Diagrama de casos de uso
     ALTO NIVEL (este documento)

 Fase 3 — Profundizar en cada UC
   → Especificación detallada
     (ver: casos-uso-especificacion)
   → Diagrama de casos de uso
     DETALLADO por paquete (este doc)

 Fase 4 — Implementación
   → Diagrama de secuencias
     (ver: diagramas-uml § 5)
   → Diagrama de clases
     (ver: diagramas-uml § 1)
   → Código

----

12. En el proyecto IACT — estructura de diagramas
=================================================

::

 1 diagrama de alto nivel
   - Sistema IACT completo
   - Todos los actores
   - UCs principales agrupados por paquete

 9 diagramas detallados (uno por paquete)
   - UC_AUTH (5 UCs)
   - UC_USR  (4 UCs)
   - UC_ACC  (9 UCs)
   - UC_PERM (10 UCs)
   - UC_RPT  (14 UCs) [crítico]
   - UC_ALR  (5 UCs)
   - UC_PIP  (4 UCs)
   - UC_AUD  (4 UCs)
   - UC_LOG  (7 UCs)

 Diagramas auxiliares en cada UC individual
   - El propio UC + sus inclusiones / extensiones
   - En la sección 4 del archivo
     uc-<mod>-<NN>-<desc>.rst per la plantilla
     :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`

  Total ≈ 10 diagramas master + 1 mini-diagrama por UC
  (97 mini-diagramas).

----

13. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skills aplicadas**
   - ``rm-elicitation`` (BABOK Hora 6 + 7 — POV usuario),
     ``rm-specification`` (modelado del UC con UML)
 * - **Origen del documento**
   - Reescrito de "GUÍA-DIAGRAMAS-CASOS-DE-USO-MODELADO"
     (Hora 7 de Schmuller, cheat-sheet aplicado interno con
     dominio ecommerce), reorientado al dominio real IACT.
 * - **Compañero textual**
   - :doc:`casos-uso-especificacion` (Hora 6)
 * - **Lección teórica**
   - :doc:`/base-cognitiva/_uml/uml-07-diagramas-casos-uso`
 * - **Cheat-sheet UML**
   - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama`
 * - **Plantilla canónica de UC**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Ejemplos hermanos**
   - :doc:`diagramas-uml`,
     :doc:`orientacion-objetos`,
     :doc:`analisis-dominio`,
     :doc:`relaciones-uml`,
     :doc:`agregacion-interfaces`
 * - **Catálogo modular del dominio**
   - :doc:`/gestion/evidencia/arquitectura-modular/analisis-catalogo-modular-iact`
 * - **Restricciones citadas**
   - CNST_001 (no email), CNST_008 (ventana ETL),
     CNST_011 (throttling), CNST_017 (SLA),
     CNST_019/020 (export), CNST_025 (auditoría),
     BR_012 (segmento).
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
