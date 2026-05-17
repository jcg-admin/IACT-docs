23.5 Aplicación a IACT
----------------------

Reglas concretas para este proyecto (alineadas con
``.claude/rules/`` y la convención del repositorio):

- **Python (Django apps)**: ``black`` con línea de 79-88
  caracteres; ``ruff`` para detección de violaciones.
  Sin alineación manual con tabuladores.
- **JavaScript/React**: ``prettier`` con configuración
  fijada en el repositorio.
- **RST (esta documentación)**: indentación con espacios
  consistente; no mezclar tabs y espacios en directivas
  ``.. uml::`` o ``.. code-block::``.
- **PlantUML embebido**: línea ≤ 80 caracteres;
  alineación de operadores ``-->`` ``..>`` por
  legibilidad sin recurrir a tabuladores manuales.
- **Importaciones Python ordenadas** (``isort``):
  estándar → terceros → locales, con línea en blanco
  entre grupos.
- **Atributos antes que métodos** en cada modelo Django
  o servicio.

Anti-patrones IACT específicos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Funciones de ``services.py`` ordenadas alfabéticamente
  en lugar de por dependencias — dificulta la lectura
  top-down. Reordenar.
- Líneas largas con encadenamientos del estilo train
  wreck (ver § 21.2): además de violar Demeter, suelen
  forzar líneas > 100 caracteres.
- Variables declaradas al inicio del método y usadas 50
  líneas después — dispersa el contexto y dificulta el
  seguimiento.
- Tabuladores para alinear ``=`` en bloques de
  asignación — fragilidad ante refactor.
