```yml
created_at: 2026-05-05 08:08:00
project: IACT-docs
work_package: 2026-05-05-08-03-31-rbac-vocabulary-cnst-033-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Análisis de naming — MenuIvrReportService

## Pregunta

¿``IvrNavigationReportService`` o
``MenuNavigationReportService``? ¿Por qué?

## Criterios aplicables

### 1. CNST-033 §8.2 — Tabla de transformaciones

Cita literal:

::

   etl / estado_etl    →  pipeline      (sin acronimo)
   sod                 →  separation    (sin acronimo)

La regla castiga el uso de acrónimos **técnicos** que
ocultan el concepto de dominio:

- ``ETL`` (Extract-Transform-Load) → ``pipeline`` —
  ``ETL`` es una técnica de implementación; ``pipeline``
  es el concepto de dominio (proceso por etapas).
- ``SoD`` (Segregation of Duties) → ``separation`` —
  ``SoD`` es jerga de governance; ``separation`` es el
  concepto.

**Patrón de la regla:** reemplazar acrónimo técnico por
sustantivo del dominio.

### 2. ¿Qué es IVR?

Consulta a ``source/base-cognitiva/glosario.rst``:

::

   **IVR**
     Interactive Voice Response. Sistema de respuesta de voz
     interactiva usado para enrutar llamadas entrantes y guiar al
     cliente. **Es el dominio del cual IACT extrae métricas.**

Y el glosario lista IVR junto a KPI como **término del
dominio**, no como jerga técnica.

Además ``Y`` en el acrónimo ``IACT`` (el nombre del
producto) significa ``IVR Analytics & Customer Tracking``.
**El producto se llama por la palabra IVR.**

### 3. Conflicto de naming con la clase ``Menu``

El domain-model ya tiene una clase ``Menu``
(``source/arquitectura-tecnica/domain-model/menu.rst``)
que representa el **menú de navegación RBAC del frontend**:
``Menu > Domain > Section > Action``. NO es el árbol del
IVR — es el menú de la aplicación web.

Si se llama ``MenuNavigationReportService``, el lector
inmediatamente piensa "reporte de navegación del menú"
y se pregunta "¿el menú de la app web o el del IVR?". Hay
**colisión semántica directa** con la clase ``Menu`` de
RBAC.

## Análisis comparativo

### Opción A: ``MenuNavigationReportService``

Pros:

- Cumple §8.2 strict (sin acrónimo).
- "Navigation" es sustantivo de dominio.

Contras:

- **Colisiona** con la clase ``Menu`` de RBAC. Sin contexto,
  el lector no sabe a qué menú refiere.
- Esconde el dominio: "menu" es genérico (cualquier UI
  tiene menús). Lo que se mide aquí es **callers que
  navegan por prompts de voz**, no clicks en una sidebar.
- Pierde información: no comunica que estamos midiendo un
  flujo conversacional telefónico.

### Opción B: ``IvrNavigationReportService``

Pros:

- "IVR" está definido en el glosario canónico como
  **término del dominio** ("Es el dominio del cual IACT
  extrae métricas").
- El producto mismo (``IACT`` = IVR Analytics &
  Customer Tracking) usa "IVR" en su definición.
- Sin colisión con ``Menu`` (clase RBAC).
- Comunica con precisión: el reporte mide **navegación
  por el sistema IVR**.

Contras:

- Lectura strict de §8.2 podría interpretarse como
  prohibición de cualquier acrónimo, incluyendo IVR.

### Opción C: ``VoiceMenuReportService``

Pros:

- Sin acrónimo + sin colisión con ``Menu`` RBAC.
- "Voice" comunica que es telefónico.

Contras:

- No es el término que usa el proyecto. El glosario y los
  BReqs usan ``IVR``, no ``voice menu``.
- Inventar un sinónimo crea drift terminológico vs el
  resto del corpus documental.

### Opción D: ``CallNavigationReportService``

Contras:

- "Call" + "Navigation" no es preciso — la llamada
  navega por el IVR, pero "call navigation" suena a
  enrutamiento de la llamada (qué cola toma), no a
  selecciones de menú IVR.

## Decisión recomendada

**Opción B: ``IvrNavigationReportService``.**

Razonamiento:

1. **§8.2 NO aplica a IVR**. La regla apunta a acrónimos
   técnicos que ocultan dominio (``ETL``, ``SoD``). IVR
   es lo opuesto: es un acrónimo **canonizado** por el
   glosario del proyecto como término de dominio. La
   palabra IVR ES la palabra de dominio. No hay un
   sustantivo no-acrónimo que la reemplace sin perder
   precisión.

2. **Coherencia con el corpus existente**: ``BREQ-007``
   se llama ``integracion-ivr-operacional``. El producto
   se define como "IVR Analytics". Renombrar a "Menu"
   o "VoiceMenu" en el domain-model rompe el vocabulario
   compartido con el resto de la documentación.

3. **Disambiguación con ``Menu`` RBAC**: imprescindible.
   Un lector que ve dos clases ``Menu`` y
   ``MenuNavigationReportService`` no puede deducir cuál
   menú está en juego. Con ``Ivr`` el dominio queda
   explícito sin lectura cruzada.

4. **Principio Clean Code (Robert C. Martin, *Clean
   Code* cap. 2)**: "Use intention-revealing names". El
   nombre debe revelar la intención sin requerir
   contexto adicional. ``IvrNavigationReportService``
   revela la intención; ``MenuNavigationReportService``
   requiere preguntar "¿qué menú?".

5. **Casing**: ``Ivr`` (no ``IVR``) en PascalCase. CNST-033
   y la convención Python PEP-8 indican PascalCase para
   clases; los acrónimos embebidos en PascalCase se
   capitalizan solo la primera letra (``XmlParser``, no
   ``XMLParser``). El producto canónico de Python usa
   ``Ivr`` para evitar lectura tipo "I-V-R" como tres
   palabras separadas.

## Decisión propuesta para registro formal

``D-XX — Naming MenuIvrReportService → IvrNavigationReportService``

CNST-033 §8.2 no se aplica a IVR porque:

- el glosario canónico (``base-cognitiva/glosario.rst``)
  declara IVR como **término del dominio**;
- el producto se define como "IVR Analytics &
  Customer Tracking";
- el corpus existente (BReqs, BRs, normativa) usa "IVR"
  consistentemente;
- no existe sinónimo no-acrónimo que preserve precisión.

Casing: ``Ivr`` (PascalCase con primera letra mayúscula
únicamente, alineado con PEP-8 para acrónimos embebidos).

**Patrón Clean Code respetado:** sin sufijos de patrón
(``Facade``, ``Singleton``). El sufijo ``Service``
**se mantiene** porque es la convención de la capa
aplicación del modelo (todos los XxxReportService) — no
es un patrón GoF, es un eponym de stratification (Eric
Evans, DDD).

## Antecedente del archivo

Renombrado del archivo: ``menu-ivr-report-service.rst``
→ ``ivr-navigation-report-service.rst``.

Naming kebab-case del nombre de clase respeta
convención del proyecto (CNST-033 §3.5 establece
``snake_case`` para SQL pero el filesystem RST sigue
kebab-case por convención local — ver
``.claude/rules/convention-naming.md``).
