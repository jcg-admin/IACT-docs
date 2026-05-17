Primer ERD IACT — entidad ``EventoAuditoria``
---------------------------------------------

Como ejemplo introductorio, la primera entidad
canónica de IACT que merece un ERD es
``EventoAuditoria`` (CNST_025 — append-only).

.. uml::

   @startuml
   title IACT — ERD snapshot: AuditEvent

   entity AuditEvent {
     * event_id : bigint <<PK>>
     --
     * user_id : int <<FK>>
     * timestamp : datetime
     * event_type : varchar(50)
     * function_id : varchar(100)
     payload_json : text
     source_ip : varchar(45)
   }
   @enduml

Lectura del ERD:

- ``evento_id`` es la PK — autoincremental, no
  reusable (CNST_025 immutable).
- ``usuario_id`` es FK al catálogo RBAC.
- Campos obligatorios marcados con ``*``.
- ``payload_json`` es opcional — solo aparece
  cuando el evento lo amerita.

En las subsecciones siguientes se agregarán
relaciones, claves foráneas y un schema más
completo del cluster RBAC.

Política IACT — ERD
~~~~~~~~~~~~~~~~~~~

1. **ERD como snapshot, no como referencia
   permanente** — la fuente de verdad son las
   migraciones Django.
2. **Marcar fecha y contexto** del snapshot
   (``status: Snapshot YYYY-MM-DD`` en el
   frontmatter del documento o el ADR).
3. **Diseñar el ERD después de la arquitectura**,
   no antes — la arquitectura define qué entidades
   viven dónde.
4. **Iterar** — si el ERD revela un problema
   estructural en la arquitectura, volver al
   Container view y revisar.
5. **No mantener un ERD del enterprise** —
   herramientas como MySQL Workbench pueden
   generar uno automático desde el schema vivo
   cuando se necesite.

Próximas subsecciones
~~~~~~~~~~~~~~~~~~~~~

- Relaciones entre entidades (1:1, 1:N, N:M).
- Cardinalidad y opcionalidad en notación
  PlantUML.
- Schemas IACT canónicos:
  ``audit_log``, catálogo RBAC, ``bd_analytics``.
