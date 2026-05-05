```yml
created_at: 2026-05-05 08:29:30
updated_at: 2026-05-05 08:29:30
project: IACT-docs
work_package: 2026-05-05-08-28-07-use-case-view-uml07-conformance-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Decisions Log — Use Case View UML-07 Conformance

## D-01 — Actor = ROL, no permiso RBAC

**Contexto:** ``use-case-view/uc-*.rst`` actualmente usa
codenames RBAC (``view_dashboard``, ``assign_functions``)
como nodos ``actor`` de los diagramas. Esto contradice
las dos fuentes canónicas:

- ``uml-07/representacion-de-un-modelo-de-caso-de-uso.rst``:
  *"Un actor es quien inicia un caso de uso"*.
- ``_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel.rst``:
  los actores IACT canónicos son ``Operador``,
  ``Supervisor``, ``Admin Acceso``, ``Admin Pipeline``,
  ``Auditor``, ``Sistema/Scheduler``, ``IVR Conmutador``.

**Decisión:** los actores en ``use-case-view/`` son
**roles** (``Operator``, ``Supervisor``, ``UserAdmin``,
``AccessAdmin``, ``Auditor``, ``PipelineAdmin``,
``SystemAdmin``, ``Caller``, ``Scheduler``,
``IvrSwitch``). Los codenames RBAC se documentan en
**notas del diagrama** o en la prosa del archivo,
nunca como actor.

## D-02 — Inglés obligatorio (CNST-033 §2)

Los nombres de actores son código (identificadores en
PlantUML) — aplican CNST-033 §2 ("CODIGO: Ingles. No hay
excepciones."). Los ejemplos del corpus
``_metodologia-aplicacion`` usan castellano
(``Operador``, ``Auditor``, ``Supervisor``) por estar
en archivos didácticos del libro UML, NO porque sea la
convención del sistema. Aplicar inglés en
``use-case-view/`` (que SÍ es código del sistema).

**Justificación adicional:** el corpus
``_metodologia-aplicacion`` está marcado como
**material de referencia/aprendizaje**, no como
canónico de implementación. CNST-033 prevalece.

## D-03 — Jerarquía de generalización entre actores

**Cita literal uml-07/comprension-de-los-usuarios.rst:**

  > Sería conveniente mostrar a los usuarios en una
  > **jerarquía de generalización**.

**Decisión:** mostrar la jerarquía
``User <|-- Operator <|-- Supervisor <|-- ...`` en el
diagrama de cada módulo cuando agregue clarity. Mínimo:
mostrar herencia en ``uc-auth.rst`` (User → roles
autenticados) y en módulos donde el rol heredado importa.

## D-04 — Codenames RBAC como anotación

Los codenames RBAC requeridos por cada UC se documentan
en **nota PlantUML al lado del módulo**, agrupados:

.. code-block:: text

   note right of MOD_Reports
     Codenames RBAC:
       VER_DASHBOARD_IVR: view_dashboard
       EXPORTAR_REPORTE:  export_csv | export_pdf | export_excel
       PROGRAMAR_REPORTE: schedule_report
   end note

Esto preserva la trazabilidad RBAC sin contaminar el
modelo de actores.

## D-05 — Estados de User (autenticado / anónimo)

``uc-auth.rst`` tiene actualmente ``UsuarioAnonimo`` y
``user_autenticado`` como actores separados. Per uml-07,
son **estados** del actor User, no roles distintos.

**Decisión:** modelar ambos como actores con
estereotipo:

.. code-block:: text

   actor "User\n<<unauthenticated>>" as UnauthUser
   actor "User\n<<authenticated>>"   as AuthUser
   UnauthUser <|-- AuthUser

## D-06 — Loop de re-escritura

Los 13 archivos se re-escriben uno a uno, en un único
commit por archivo (por trazabilidad granular) o en
batches por módulo relacionado. Cada archivo:

1. Mantiene el rectángulo ``rectangle "MOD_X"``.
2. Sustituye actores RBAC por roles canónicos (D-01).
3. Agrega nota con codenames RBAC (D-04).
4. Aplica generalización entre actores cuando aplique
   (D-03).
5. Mantiene relaciones ``<<include>>`` y ``<<extend>>``
   correctas.
6. Pre-render para validar.

## D-07 — Bounded scope: solo use-case-view/

Este WP NO toca:

- ``source/requisitos/casos-uso/uc-*/diagramas-uml/uc-*.rst``
  (UC individuales con su propio diagrama; son
  consumidores de los actores canónicos pero su
  rediseño es un WP futuro).
- ``source/arquitectura-tecnica/system-view/`` (otros
  tipos de diagrama).
- ``source/requisitos/_metodologia-aplicacion/`` (es la
  fuente canónica, intocable).

Mantener scope acotado: solo los 13 archivos de
``arquitectura-tecnica/use-case-view/uc-*.rst``.
