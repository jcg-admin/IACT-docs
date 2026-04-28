.. meta::
   :artefacto: Index_Estandares
   :tipo: Indice
   :dominio: normativa
   :subdominio: estandares
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-07
   :ultimo_cambio: 2026-04-28
   :autor: Equipo IACT
   :clasificacion: Interno

.. _estandares:

==========
Estándares
==========

Propósito
=========

Este subdominio define los **estándares del proyecto IACT** que
gobiernan documentación, código, naming y procedimientos.
Establece formatos, notaciones, plantillas reutilizables y
convenciones de estilo.

Contenido
=========

Los estándares cubren:

- Documentación: prohibición de emojis, lenguaje profesional
  obligatorio, frases prohibidas con alternativas.
- Naming: convenciones de archivos, directorios, identificadores
  técnicos.
- Versionado: SemVer 2.0.0 en metadata, no en filenames.
- Plantillas reutilizables: moldes para UCs, BRs, FRs, NFRs,
  ADRs, restricciones, etc.

.. note::

   **Política de numeración STD:** la secuencia STD_001..STD_007
   refleja el orden histórico de creación de estándares en el
   proyecto. Los huecos STD_003, STD_004, STD_005 están
   **reservados** para estándares futuros sobre temas
   identificados pero aún no formalizados (formato RST,
   metadata obligatoria, gobernanza de cambios). No se
   renumeran los estándares existentes para mantener
   inmutabilidad de IDs ya citados.

   Los STDs sin numeración (``STD_Naming_Identificadores``,
   ``STD_Profesional_Documentacion``) usan nombre descriptivo
   directamente — son estándares transversales sin secuencia
   estricta.

.. toctree::
   :maxdepth: 1
   :caption: Estándares (STDs)

   STD_001_Estandares_Documentacion_Sin_Emojis
   STD_002_Nomenclatura_Proyecto
   STD_006_Versionado_Semantico
   STD_007_Convencion_Naming
   STD_Naming_Identificadores
   STD_Profesional_Documentacion

.. toctree::
   :maxdepth: 2
   :caption: Plantillas

   plantillas/index

.. toctree::
   :maxdepth: 1
   :caption: Guías técnicas

   guia-estilo
   estandares-codigo
   shell-scripting-guide
