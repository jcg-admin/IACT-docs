CNST-002: Gestión de Sesiones en Base de Datos
===============================================

:ID: CNST-002
:Versión: 1.1.0
:Fecha: 2026-01-03
:Estado: VIGENTE
:Clasificación: CRÍTICO - NO NEGOCIABLE
:Origen: Restricción del cliente

----

Propósito
---------

Este documento establece la prohibición de uso de Redis o sistemas de caché en memoria para gestión de sesiones en el Sistema IACT - IVR Analytics & Customer Tracking, y define el mecanismo obligatorio de sesiones en base de datos MySQL con política de sesión única por usuario.

Contexto
--------

Origen de la Restricción
~~~~~~~~~~~~~~~~~~~~~~~~

Restricción de infraestructura impuesta por el cliente. El cliente NO provee ni permite la instalación de servicios Redis, Memcached u otros sistemas de caché en memoria en su infraestructura.

Justificación del Cliente
~~~~~~~~~~~~~~~~~~~~~~~~~

- Simplificación de infraestructura (menos servicios que mantener)
- Reducción de puntos de fallo
- Auditoría de sesiones en base de datos relacional
- Control centralizado de sesiones activas
- Política de seguridad: una sesión por usuario

Aplicable a
~~~~~~~~~~~

- Sistema IACT completo
- Autenticación y autorización
- Gestión de sesiones de usuario
- Tokens de acceso y refresh
- Todas las fases del ciclo de vida (desarrollo, QA, producción)

Restricciones
-------------

Prohibiciones Absolutas
~~~~~~~~~~~~~~~~~~~~~~~

Servicios de Caché Prohibidos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PROHIBIDO bajo cualquier circunstancia:

- Redis
- Memcached
- AWS ElastiCache
- Azure Cache for Redis
- Cualquier servicio de caché en memoria externa

Librerías Prohibidas
^^^^^^^^^^^^^^^^^^^^

Librerías de caché en código Python:

- ``redis`` / ``redis-py``
- ``django-redis``
- ``pymemcache``
- ``python-memcached``
- ``django-cache-machine``

Configuraciones Prohibidas
^^^^^^^^^^^^^^^^^^^^^^^^^^

NO se permite en settings:

.. code-block:: python

   # PROHIBIDO - No usar Redis
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }

   # PROHIBIDO - No usar Memcached
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
           'LOCATION': '127.0.0.1:11211',
       }
   }

   # PROHIBIDO - No usar sesiones en Redis
   SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

Consecuencias de Violación
~~~~~~~~~~~~~~~~~~~~~~~~~~

Consecuencias de violación de esta restricción:

- Rechazo inmediato en code review
- Fallo en deployment (servicio no disponible en infraestructura)
- Incidente de seguridad categoría Alta
- Re-trabajo completo del módulo afectado

Mecanismo Obligatorio
---------------------

Sesiones en Base de Datos
~~~~~~~~~~~~~~~~~~~~~~~~~

OBLIGATORIO: Usar django.contrib.sessions con backend de base de datos.

Configuración Django
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # api/config/settings/base.py

   # Sesiones en base de datos (OBLIGATORIO - CNST-002)
   SESSION_ENGINE = 'django.contrib.sessions.backends.db'

   # Timeout de sesión: 15 minutos de inactividad
   SESSION_COOKIE_AGE = 900  # 15 minutos en segundos

   # Sesión expira al cerrar navegador
   SESSION_EXPIRE_AT_BROWSER_CLOSE = True

   # Cookie segura (solo HTTPS en producción)
   SESSION_COOKIE_SECURE = True  # En producción

   # Cookie HTTPOnly (no accesible desde JavaScript)
   SESSION_COOKIE_HTTPONLY = True

   # SameSite para prevenir CSRF
   SESSION_COOKIE_SAMESITE = 'Lax'

   # Nombre de cookie único para IACT
   SESSION_COOKIE_NAME = 'iact_sessionid'

   # Guardar sesión en cada request (actualiza last_activity)
   SESSION_SAVE_EVERY_REQUEST = True

Política de Sesión Única
~~~~~~~~~~~~~~~~~~~~~~~~

OBLIGATORIO: Solo una sesión activa por usuario.

Al iniciar sesión, el sistema debe:

1. Verificar si existe sesión activa para el usuario
2. Si existe, invalidar la sesión anterior
3. Crear nueva sesión
4. Notificar al usuario si se cerró sesión en otro dispositivo

Modelo de Sesión Extendido
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/users/models.py

   from django.db import models
   from django.contrib.auth import get_user_model
   from django.contrib.sessions.models import Session
   from django.utils import timezone

   User = get_user_model()

   class UserSession(models.Model):
       """
       Extensión de sesión para política de sesión única.

       Vincula sesiones Django con usuarios para:
       - Implementar sesión única por usuario
       - Auditar sesiones activas
       - Permitir cierre remoto de sesiones

       CNST-002: Obligatorio para control de sesiones.
       """

       user = models.ForeignKey(
           User,
           on_delete=models.CASCADE,
           related_name='sessions'
       )
       session = models.OneToOneField(
           Session,
           on_delete=models.CASCADE,
           related_name='user_session'
       )
       ip_address = models.GenericIPAddressField()
       user_agent = models.CharField(max_length=255)
       created_at = models.DateTimeField(auto_now_add=True)
       last_activity = models.DateTimeField(auto_now=True)

       class Meta:
           db_table = 'user_sessions'
           ordering = ['-last_activity']
           indexes = [
               models.Index(fields=['user', 'created_at']),
               models.Index(fields=['last_activity']),
           ]

       def __str__(self):
           return f"{self.user.username} - {self.ip_address}"

       def is_active(self):
           """Verificar si la sesión está activa."""
           return self.session.expire_date > timezone.now()

       @classmethod
       def get_active_sessions(cls, user):
           """Obtener sesiones activas de un usuario."""
           now = timezone.now()
           return cls.objects.filter(
               user=user,
               session__expire_date__gt=now
           ).select_related('session')

Implementación de Sesión Única
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/users/services.py

   from django.contrib.sessions.models import Session
   from apps.users.models import UserSession
   from apps.common.notifications import notify

   def enforce_single_session(user, new_session_key, ip_address, user_agent):
       """
       Implementar política de sesión única.

       Args:
           user: Usuario que inicia sesión
           new_session_key: Clave de la nueva sesión
           ip_address: IP del usuario
           user_agent: User agent del navegador

       Returns:
           UserSession creado
       """
       # Obtener sesiones activas existentes
       active_sessions = UserSession.get_active_sessions(user)

       # Invalidar sesiones anteriores
       if active_sessions.exists():
           for user_session in active_sessions:
               # Eliminar sesión de BD
               user_session.session.delete()
               user_session.delete()

           # Notificar al usuario
           notify(
               recipient=user,
               subject='Sesión cerrada en otro dispositivo',
               body='Tu sesión anterior fue cerrada porque iniciaste '
                    'sesión desde otro dispositivo.',
               priority='NORMAL'
           )

       # Crear nueva sesión
       session = Session.objects.get(session_key=new_session_key)
       user_session = UserSession.objects.create(
           user=user,
           session=session,
           ip_address=ip_address,
           user_agent=user_agent
       )

       return user_session

Vista de Login con Sesión Única
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/users/views.py

   from rest_framework.views import APIView
   from rest_framework.response import Response
   from rest_framework import status
   from django.contrib.auth import authenticate, login
   from apps.users.services import enforce_single_session

   class LoginView(APIView):
       """
       Login con sesión única obligatoria.

       Implementa CNST-002: Sesión única por usuario.
       """

       def post(self, request):
           username = request.data.get('username')
           password = request.data.get('password')

           user = authenticate(username=username, password=password)

           if user is None:
               return Response({
                   'error': 'Credenciales inválidas'
               }, status=status.HTTP_401_UNAUTHORIZED)

           if not user.is_active:
               return Response({
                   'error': 'Usuario inactivo'
               }, status=status.HTTP_403_FORBIDDEN)

           # Crear sesión Django
           login(request, user)

           # Implementar sesión única
           ip_address = request.META.get('REMOTE_ADDR')
           user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

           user_session = enforce_single_session(
               user=user,
               new_session_key=request.session.session_key,
               ip_address=ip_address,
               user_agent=user_agent
           )

           return Response({
               'message': 'Login exitoso',
               'user': {
                   'id': user.id,
                   'username': user.username,
                   'email': user.email
               },
               'session': {
                   'created_at': user_session.created_at.isoformat(),
                   'ip_address': user_session.ip_address
               }
           }, status=status.HTTP_200_OK)

Casos de Uso Afectados
----------------------

UC-001: Iniciar Sesión
~~~~~~~~~~~~~~~~~~~~~~

Flujo Principal
^^^^^^^^^^^^^^^

1. Usuario ingresa credenciales
2. Sistema autentica usuario
3. **Sistema verifica sesiones activas existentes** (CNST-002)
4. **Sistema invalida sesión anterior si existe** (CNST-002)
5. Sistema crea nueva sesión en base de datos MySQL
6. Sistema registra UserSession con IP y User-Agent
7. Sistema retorna sesión activa

UC-002: Cerrar Sesión
~~~~~~~~~~~~~~~~~~~~~

Flujo Principal
^^^^^^^^^^^^^^^

1. Usuario solicita cerrar sesión
2. Sistema elimina registro de Session (django_session)
3. Sistema elimina registro de UserSession
4. Sistema invalida cookie de sesión
5. Sistema retorna confirmación

UC-004: Validar Sesión
~~~~~~~~~~~~~~~~~~~~~~

Flujo Principal
^^^^^^^^^^^^^^^

1. Usuario hace request autenticado
2. Sistema valida cookie de sesión
3. **Sistema consulta Session en base de datos MySQL** (CNST-002)
4. Sistema verifica expire_date
5. Si sesión válida, sistema procesa request
6. Si sesión expirada, sistema retorna 401 Unauthorized

Gestión de Sesiones Expiradas
-----------------------------

Comando de Limpieza
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/users/management/commands/clearsessions.py

   from django.core.management.base import BaseCommand
   from django.contrib.sessions.models import Session
   from django.utils import timezone
   from apps.users.models import UserSession

   class Command(BaseCommand):
       help = 'Eliminar sesiones expiradas de la base de datos'

       def handle(self, *args, **options):
           now = timezone.now()

           # Eliminar sesiones Django expiradas
           expired_sessions = Session.objects.filter(expire_date__lt=now)
           count_sessions = expired_sessions.count()
           expired_sessions.delete()

           # Eliminar UserSessions huérfanos
           orphan_user_sessions = UserSession.objects.filter(
               session__isnull=True
           )
           count_user_sessions = orphan_user_sessions.count()
           orphan_user_sessions.delete()

           self.stdout.write(
               self.style.SUCCESS(
                   f'Eliminadas {count_sessions} sesiones expiradas y '
                   f'{count_user_sessions} user sessions huérfanos'
               )
           )

Cron Job
^^^^^^^^

.. code-block:: bash

   # Ejecutar diariamente a las 03:00
   0 3 * * * cd /opt/iact && /opt/iact/venv/bin/python api/manage.py clearsessions

Middleware de Actualización de Actividad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/middleware.py

   from django.utils import timezone
   from apps.users.models import UserSession

   class UpdateSessionActivityMiddleware:
       """
       Actualizar last_activity en cada request.

       CNST-002: Mantener registro de última actividad en BD.
       """

       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           if request.user.is_authenticated and request.session.session_key:
               try:
                   user_session = UserSession.objects.get(
                       session__session_key=request.session.session_key
                   )
                   # Django ya actualiza last_activity con auto_now=True
                   # Pero explícitamente guardamos para estar seguros
                   user_session.save(update_fields=['last_activity'])
               except UserSession.DoesNotExist:
                   pass

           return self.get_response(request)

Dashboard de Sesiones Activas
-----------------------------

Vista de Administración
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/users/views.py

   from rest_framework.views import APIView
   from rest_framework.response import Response
   from rest_framework.permissions import IsAdminUser
   from apps.users.models import UserSession
   from django.utils import timezone

   class ActiveSessionsView(APIView):
       """
       Lista sesiones activas en el sistema.

       Requiere función: administra_sistema (RBAC v5.1.1)
       """

       permission_classes = [IsAdminUser]

       def get(self, request):
           now = timezone.now()

           active_sessions = UserSession.objects.filter(
               session__expire_date__gt=now
           ).select_related('user', 'session').order_by('-last_activity')

           data = []
           for user_session in active_sessions:
               data.append({
                   'user': user_session.user.username,
                   'ip_address': user_session.ip_address,
                   'user_agent': user_session.user_agent,
                   'created_at': user_session.created_at.isoformat(),
                   'last_activity': user_session.last_activity.isoformat(),
                   'expires_at': user_session.session.expire_date.isoformat()
               })

           return Response({
               'total_active': len(data),
               'sessions': data
           })

Validación en Desarrollo
------------------------

Pre-commit Checklist
~~~~~~~~~~~~~~~~~~~~

Antes de hacer commit, verificar:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - NO existe ``import redis``
   * - [ ]
     - NO existe ``redis`` en requirements.txt
   * - [ ]
     - NO existe configuración de Redis en settings
   * - [ ]
     - ``SESSION_ENGINE`` es ``'django.contrib.sessions.backends.db'``
   * - [ ]
     - Existe migración para tabla ``user_sessions``

Code Review Checklist
~~~~~~~~~~~~~~~~~~~~~

Durante code review, rechazar si:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - Se intenta usar Redis o Memcached
   * - [ ]
     - Se importan librerías de caché
   * - [ ]
     - SESSION_ENGINE no es 'db'
   * - [ ]
     - No se implementa sesión única

Validación Automatizada
~~~~~~~~~~~~~~~~~~~~~~~

Script de Validación
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   #!/bin/bash
   # scripts/validate_no_redis.sh

   echo "Validando que no existan referencias a Redis/Memcached..."

   ERRORS=0

   # Buscar imports prohibidos
   if grep -r "import redis" api/apps/; then
       echo "ERROR: Encontrado 'import redis'"
       ERRORS=$((ERRORS + 1))
   fi

   if grep -r "redis\|memcached" requirements.txt; then
       echo "ERROR: Encontrado Redis/Memcached en requirements"
       ERRORS=$((ERRORS + 1))
   fi

   # Verificar SESSION_ENGINE
   if ! grep -r "SESSION_ENGINE.*db" api/config/settings/; then
       echo "ERROR: SESSION_ENGINE no configurado para BD"
       ERRORS=$((ERRORS + 1))
   fi

   if [ $ERRORS -eq 0 ]; then
       echo "OK: No se encontraron referencias a caché prohibida"
       exit 0
   else
       echo "FALLO: $ERRORS violaciones de CNST-002 encontradas"
       exit 1
   fi

Excepciones
-----------

**NO EXISTEN EXCEPCIONES**

Esta restricción NO tiene excepciones.

La infraestructura del cliente no provee Redis ni Memcached.

Cualquier intento de usar caché en memoria fallará en deployment.

Alternativas Evaluadas y Rechazadas
-----------------------------------

Alternativa 1: Redis Interno
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Propuesta:** Instalar Redis en infraestructura del cliente.

**Rechazada porque:**

- Cliente explícitamente NO permite servicios adicionales
- Política de simplificación de infraestructura
- Overhead de mantenimiento inaceptable

Alternativa 2: Caché en Memoria Local
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Propuesta:** Usar django.core.cache.backends.locmem.

**Rechazada porque:**

- No persiste entre workers de Gunicorn
- Sesiones se perderían al reiniciar servidor
- No cumple con requerimiento de auditoría

Alternativa 3: Sesiones en Archivos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Propuesta:** Usar django.contrib.sessions.backends.file.

**Rechazada porque:**

- Problemas de concurrencia en alta carga
- Dificulta auditoría y consulta de sesiones
- Base de datos es más robusta

Referencias
-----------

Documentos Relacionados
~~~~~~~~~~~~~~~~~~~~~~~

- UC-001: Iniciar Sesión
- UC-002: Cerrar Sesión
- UC-004: Validar Sesión
- Modelo RBAC IACT v5.1.1

Implementación de Referencia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``api/apps/users/models.py`` - UserSession
- ``api/apps/users/services.py`` - enforce_single_session()
- ``api/apps/users/views.py`` - LoginView

Historial de Cambios
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 50 20

   * - Versión
     - Fecha
     - Cambios
     - Autor
   * - 1.1.0
     - 2026-01-03
     - Actualización a RBAC v5.1.1
     - Equipo IACT
   * - 1.0.0
     - 2025-12-17
     - Versión inicial completa con Clean Code
     - Equipo IACT

Aprobaciones
------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Rol
     - Nombre
     - Firma / Fecha
   * - Cliente (Sponsor)
     - [Nombre]
     - [Pendiente]
   * - Tech Lead
     - [Nombre]
     - [Pendiente]
   * - Infrastructure Lead
     - [Nombre]
     - [Pendiente]

----

**Fin del Documento CNST-002**