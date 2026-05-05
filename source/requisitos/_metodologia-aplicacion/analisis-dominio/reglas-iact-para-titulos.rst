Reglas IACT para títulos
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Todo diagrama publicado** en este cajón debe
   tener título — un diagrama sin título es ambiguo
   fuera del contexto inmediato del párrafo que lo
   introduce.
2. **El título debe ser informativo del alcance**:
   "Modelo de dominio IACT" es genérico; "Modelo de
   dominio IACT — cluster RBAC" es específico.
3. **Convención de nombre**: ``[propósito] — [alcance]``.
   Ejemplos:

   - ``Diagrama de clases — entidad Llamada``
   - ``Diagrama de secuencias — UC_RPT_04 export``
   - ``Diagrama de despliegue — vm-iact``
4. **Sin emojis**, sin caracteres decorativos —
   coherencia con la convención general del repositorio.
5. **Coincidencia con el caption del bloque RST** — si
   el bloque ``.. uml::`` está bajo un encabezado
   "Ejemplo IACT — UC_RPT_04", el título del diagrama
   debe ser coherente con ese encabezado.
