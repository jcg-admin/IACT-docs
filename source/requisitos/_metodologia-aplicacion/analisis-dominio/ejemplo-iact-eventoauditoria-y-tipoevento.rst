Ejemplo IACT — ``EventoAuditoria`` y ``TipoEvento``
---------------------------------------------------

Aplicado al cluster de auditoría de IACT
(CNST_025): cada ``EventoAuditoria`` pertenece a
exactamente un ``TipoEvento`` (acceso, cambio
RBAC, ejecución ETL, denegado por separacion, etc.); un mismo
``TipoEvento`` puede aparecer en muchos eventos.

.. uml::

   @startuml
   title IACT — ERD snapshot: AuditEvent + EventType

   entity EventType {
     * type_id : int <<PK>>
     --
     * name : varchar(50)
     description : varchar(200)
   }

   entity AuditEvent {
     * event_id : bigint <<PK>>
     --
     * user_id : int <<FK>>
     * type_id : int <<FK>>
     * timestamp : datetime
     * function_id : varchar(100)
     payload_json : text
     source_ip : varchar(45)
   }

   EventType ||--o{ AuditEvent : classifies
   @enduml

Lectura: cada evento tiene **exactamente un**
tipo (``||`` del lado de ``TipoEvento``); cada
tipo puede aparecer en **cero o más** eventos
(``o{`` del lado de ``EventoAuditoria``).

Cardinalidad bidireccional
~~~~~~~~~~~~~~~~~~~~~~~~~~

La sintaxis se puede invertir sin cambiar el
significado:

.. code-block:: text

   ' Equivalentes:
   TipoEvento ||--o{ EventoAuditoria : clasifica
   EventoAuditoria }o--|| TipoEvento : pertenece a

La preferencia IACT: **leer de izquierda a
derecha** con la entidad "padre" o "lookup" a la
izquierda. Resulta más natural en español:
``TipoEvento clasifica eventos``.

Política IACT para relaciones en ERD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Toda relación tiene cardinalidad explícita** —
   ningún ``--`` sin marcas.
2. **Toda relación tiene etiqueta** que describe
   el sentido (``clasifica``, ``pertenece a``,
   ``audita``, ``contiene``).
3. **Padre / lookup a la izquierda** — facilita la
   lectura.
4. **No usar ERD para modelar dominio** — para
   eso, diagrama de clases UML con notación
   numérica (§ 16.5).
5. **Snapshot con fecha** en el frontmatter del
   documento que contiene el ERD.

Próximas subsecciones
~~~~~~~~~~~~~~~~~~~~~

- Tipos de dato y restricciones de columna
  (NOT NULL, UNIQUE, DEFAULT).
- Atributos de identificación (PK, FK, índices).
- Schemas canónicos IACT consolidados:
  cluster RBAC, ``audit_log``, agregados de
  ``bd_analytics``.
