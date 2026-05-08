.. meta::
 :artefacto: BACK_CONVENTIONS
 :tipo: Convenciones
 :dominio: backend
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

============
Convenciones
============

Convenciones de naming, estructura y estilo para el backend
IACT (Django REST Framework). Aplica a Python, DRF y artefactos
asociados.

Naming
======

.. note::

   La autoridad normativa de naming en este proyecto es
   :doc:`/normativa/estandares/clean-code-naming-principles`.
   Esta seccion resume y aplica esa norma al contexto backend.
   Ante cualquier divergencia, prevalece el documento
   autoritativo.

Python
------

- **Modulos / paquetes:** snake_case (``users``, ``auth_module``).
- **Clases:** PascalCase, nombre de **rol en el dominio**.
  El nombre debe permanecer valido si el framework cambia
  (CLEAN_CODE §6.1). Ejemplos:
  ``UserCapabilityResolver``, ``MenuItemRepresentation``,
  ``MenuItemEndpoint``, ``FunctionAuthProvider``.
- **Funciones / metodos:** snake_case con verbo descriptivo
  (``resolve``, ``transition``, ``validate_token``).
- **Variables:** snake_case con nombre descriptivo
  (``active_user_count``, ``query_params``).
- **Constantes:** UPPER_SNAKE_CASE conceptuales
  (``CACHE_TTL_SECONDS``, no ``TTL`` solo).

Sufijos prohibidos en clases (CLEAN_CODE §6.2)
-----------------------------------------------

Los siguientes sufijos describen mecanismo tecnico del
framework, no rol en el dominio. Estan **prohibidos** en
clases de produccion y de tests:

| Sufijo prohibido | Origen | Reemplazo de dominio |
|---|---|---|
| ``Serializer`` | DRF | ``Representation`` |
| ``ViewSet`` | DRF | ``Endpoint`` |
| ``View`` (cuando viene de DRF) | DRF | ``Endpoint`` |
| ``Permission`` (cuando viene de DRF) | DRF | ``AccessPolicy`` |
| ``Backend`` (auth) | Django auth | ``AuthProvider`` |
| ``Manager`` | Django ORM | ``Query`` o ``Repository`` |
| ``Middleware`` | Django/WSGI | nombre de rol descriptivo |
| ``Factory`` | GoF | ``TestData`` (tests) o rol del dominio |
| ``Builder`` (sin interfaz fluent real) | GoF | ``Assembler`` o rol del dominio |
| ``Helper`` / ``Utils`` | generico | nombre especifico del rol |

Ejemplos correctos (DRF + clean code):

.. code-block:: python

   # El nombre describe el rol; la herencia revela el mecanismo
   class MenuItemRepresentation(serializers.ModelSerializer):
       class Meta:
           model = MenuItem
           fields = ["id", "display_label", "route_path", "status"]

   class MenuItemEndpoint(viewsets.ModelViewSet):
       queryset = MenuItem.objects.renderable()
       serializer_class = MenuItemRepresentation

   class FunctionAuthProvider(BaseBackend):
       def authenticate(self, request, **kwargs): ...

   class CapabilityAccessPolicy(BasePermission):
       def has_permission(self, request, view): ...

Convivencia con la herencia del framework
------------------------------------------

El nombre de la clase es de **dominio**. La clase base de
DRF/Django de la que hereda (``ModelSerializer``,
``ModelViewSet``, ``BasePermission``, ``BaseBackend``) es
detalle de implementacion visible solo en la definicion.
Ambas capas conviven sin que el mecanismo tecnico contamine
el nombre del concepto.

Archivos
--------

- Aplica :doc:`/normativa/estandares/std-007-convencion-naming`:
  snake_case en Python, sin tildes ni enies.
- Modulos por capa funcional: ``models.py``, ``services.py``,
  ``resolvers.py``, ``representations.py`` (no ``serializers.py``
  cuando se desea reflejar el rol en el modulo), ``endpoints.py``
  (alternativa a ``views.py``). Mantener compatibilidad si el
  proyecto ya usa nombres tradicionales — el nombre de la
  CLASE es lo critico, no el del archivo.

URLs / API
==========

- **Versionado:** prefijo ``/api/v{N}/`` en todos los endpoints.
- **Recursos en plural:** ``/api/v1/users/``, ``/api/v1/reports/``.
- **Acciones no-CRUD:** sub-recursos descriptivos
  (``/api/v1/users/{id}/activate/``).
- **Paginacion:** estandar DRF con ``page_size`` configurable.
- **Errores:** formato JSON consistente con codigo, mensaje y
  detalle. Las decisiones de formato de error son ADRs en
  :doc:`/normativa/gobernanza/index`.

Estructura de apps
==================

Por dominio funcional, alineado con los 13 modulos UC del sistema (9 RBAC activos + ADM nuevo + 2 reservados open-closed + Caller sin RBAC)
arquitectonicos:

.. code-block:: text

 backend/
   apps/
     auth/
       models.py
       serializers.py
       views.py
       urls.py
       permissions.py
     user_identity/
       ...
     rbac_core/
       ...
     etl_monitoring/
       ...
   config/
     settings/
       base.py
       dev.py
       prod.py
     urls.py
     wsgi.py

Estilo
======

- **Linter:** flake8 / ruff con configuracion compartida.
- **Formatter:** black (las reglas de estilo se delegan al
  tooling — no se documentan aqui).
- **Type hints:** obligatorios en interfaces publicas (vistas,
  serializers, servicios).
- **Imports:** orden estable (stdlib → libs externas → django →
  apps locales).

Permisos
========

- Usar el modelo RBAC canonico documentado en
  :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`.
- Las clases de permiso DRF deben mapear a las funciones (no a
  permisos legacy tabla-PERM). La migracion vocabulario
  ``Capacidad`` → ``Function`` (D-RBAC-2 + D-RBAC-8) esta
  registrada como deuda tecnica en
  :doc:`/risks-technical-debt/deuda-tecnica-rebuild` (DEBT-001).

Trazabilidad
============

- Convenciones generales: :doc:`/normativa/estandares/index`.
- Decisiones arquitectonicas backend: registrar como ADR
  en :doc:`/normativa/gobernanza/index` con prefijo
  ``ADR-BACK-`` o ``ADR-DEVOPS-`` segun aplique.
