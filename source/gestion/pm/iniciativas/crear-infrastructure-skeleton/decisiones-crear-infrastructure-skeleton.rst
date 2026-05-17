.. meta::
   :artefacto: DECISIONES-CREAR-INFRASTRUCTURE-SKELETON
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/crear-infrastructure-skeleton
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2026-05-17T00:39:49

.. _decisiones-crear-infrastructure-skeleton:

===========================================
Decisiones: Crear Infrastructure Skeleton
===========================================

1. Decisiones de diseno
========================

**D-001: Infrastructure entre Bases de Datos y Calidad en el indice raiz**

El stack de producto en source/index.rst ordena las capas tecnicas
de forma logica: frontend → backend → bases de datos → infraestructura
→ calidad. Infrastructure es la capa de hosting que sostiene al backend
y las bases de datos, por lo que su posicion entre databases y quality
es la mas coherente.

**D-002: Nota RST en ADR-001 en lugar de texto plano**

El ADR-DEVOPS-001 tenia texto de anotacion sin formato (todo en
mayusculas) que no era un elemento RST valido. Se reemplazo por un
.. note:: con referencia a los documentos que cumplen esa
documentacion pendiente. El texto original decia
"ESTO ES IMPORTANTE, SE TIENE QUE DOCUMENTAR...".

**D-003: Referencia a CNST corregida in-place**

overview.rst referencio cnst-001-no-email-sistema que no
existe. El nombre real es cnst-001-prohibicion-de-email-y-smtp.
Corregido antes del commit — 0 warnings como criterio de completitud.

2. Hallazgos durante la ejecucion
===================================

**H-001: Los nombres de CNST no siguen un patron predecible**

Tres CNSTs referenciadas en esta rama tuvieron que corregirse
porque el nombre canonico difiere del nombre semantico esperado.
Patron de riesgo: al referenciar CNSTs desde nuevos documentos,
siempre verificar con find source/normativa/restricciones -name 'cnst-NNN*'.

3. Verificacion post-ejecucion
================================

.. list-table::
   :widths: 55 15 30
   :header-rows: 1

   * - Criterio
     - Resultado
     - Evidencia
   * - source/infrastructure/index.rst existe
     - PASA
     - source/infrastructure/index.rst
   * - source/infrastructure/overview.rst existe
     - PASA
     - source/infrastructure/overview.rst
   * - source/infrastructure/conventions.rst existe
     - PASA
     - source/infrastructure/conventions.rst
   * - source/index.rst incluye infrastructure/
     - PASA
     - caption: Infraestructura en toctree raiz
   * - Build Sphinx 0 warnings 0 errors
     - PASA
     - build succeeded
