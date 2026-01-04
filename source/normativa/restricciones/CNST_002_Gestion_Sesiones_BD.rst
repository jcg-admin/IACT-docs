CNST-002: Gestión de Sesiones en Base de Datos
===============================================

:ID: CNST-002
:Versión: 1.0.0
:Fecha: 2025-12-17
:Estado: Vigente
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
           indexes = [
               models.Index(fields=['user', 'created_at']),
               models.Index(fields=['session']),
           ]

       def __str__(self):
           return f"{self.user.username} - {self.ip_address}"

       @classmethod
       def create_session(cls, user, session_key, request):
           """
           Crear sesión única para usuario.

           Invalida sesiones previas del mismo usuario.

           Args:
               user: Usuario autenticado
               session_key: Key de sesión Django
               request: HTTP request (para IP y User-Agent)

           Returns:
               UserSession creada
           """
           # Invalidar sesiones previas del usuario
           cls.invalidate_user_sessions(user)

           # Obtener sesión Django
           session = Session.objects.get(session_key=session_key)

           # Crear nueva UserSession
           return cls.objects.create(
               user=user,
               session=session,
               ip_address=cls._get_client_ip(request),
               user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
           )

       @classmethod
       def invalidate_user_sessions(cls, user):
           """
           Invalidar todas las sesiones de un usuario.

           Args:
               user: Usuario cuyas sesiones se invalidarán
           """
           user_sessions = cls.objects.filter(user=user)

           for user_session in user_sessions:
               # Eliminar sesión Django
               try:
                   user_session.session.delete()
               except Session.DoesNotExist:
                   pass

           # Eliminar registros UserSession
           user_sessions.delete()

       @classmethod
       def get_active_session(cls, user):
           """
           Obtener sesión activa del usuario.

           Args:
               user: Usuario

           Returns:
               UserSession o None
           """
           return cls.objects.filter(user=user).first()

       @staticmethod
       def _get_client_ip(request):
           """Obtener IP del cliente."""
           x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
           if x_forwarded_for:
               return x_forwarded_for.split(',')[0].strip()
           return request.META.get('REMOTE_ADDR')

Middleware de Sesión Única
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/middleware.py

   from django.contrib.auth import logout
   from django.utils import timezone
   from apps.users.models import UserSession

   class SingleSessionMiddleware:
       """
       Middleware que garantiza una sola sesión activa por usuario.

       Funcionalidad:
       - Verifica que la sesión actual sea válida
       - Actualiza timestamp de última actividad
       - Cierra sesión si fue invalidada desde otro dispositivo

       CNST-002: Obligatorio para política de sesión única.
       """

       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           if request.user.is_authenticated:
               self._validate_session(request)

           response = self.get_response(request)
           return response

       def _validate_session(self, request):
           """Validar que la sesión sea la activa del usuario."""
           session_key = request.session.session_key

           if not session_key:
               return

           # Verificar si existe UserSession para esta sesión
           try:
               user_session = UserSession.objects.select_related('session').get(
                   session__session_key=session_key,
                   user=request.user
               )
               # Actualizar última actividad
               user_session.last_activity = timezone.now()
               user_session.save(update_fields=['last_activity'])

           except UserSession.DoesNotExist:
               # Sesión no registrada o invalidada, cerrar sesión
               logout(request)


   class SessionTimeoutMiddleware:
       """
       Middleware para timeout de sesión por inactividad.

       Cierra sesión si han pasado más de 15 minutos
       desde la última actividad.

       CNST-002: Timeout de 15 minutos obligatorio.
       """

       TIMEOUT_SECONDS = 900  # 15 minutos

       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           if request.user.is_authenticated:
               self._check_timeout(request)

           response = self.get_response(request)
           return response

       def _check_timeout(self, request):
           """Verificar timeout de sesión."""
           last_activity = request.session.get('last_activity')

           if last_activity:
               from datetime import datetime
               last = datetime.fromisoformat(last_activity)
               elapsed = (timezone.now() - last).total_seconds()

               if elapsed > self.TIMEOUT_SECONDS:
                   logout(request)
                   return

           # Actualizar última actividad
           request.session['last_activity'] = timezone.now().isoformat()

Configuración de Middlewares
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/config/settings/base.py

   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',

       # Middlewares de sesión IACT (CNST-002)
       'apps.common.middleware.SingleSessionMiddleware',
       'apps.common.middleware.SessionTimeoutMiddleware',

       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

Autenticación con JWT
---------------------

Configuración SimpleJWT
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/config/settings/base.py

   from datetime import timedelta
   import os

   SIMPLE_JWT = {
       # Access token: 15 minutos (igual que sesión)
       'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),

       # Refresh token: 7 días
       'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

       # Rotar refresh token en cada uso
       'ROTATE_REFRESH_TOKENS': True,

       # Blacklist de tokens rotados
       'BLACKLIST_AFTER_ROTATION': True,

       # Algoritmo de firma
       'ALGORITHM': 'HS256',

       # Clave secreta desde variable de entorno
       'SIGNING_KEY': os.environ.get('JWT_SECRET_KEY'),

       # Tipo de header
       'AUTH_HEADER_TYPES': ('Bearer',),
       'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

       # Claims del token
       'USER_ID_FIELD': 'id',
       'USER_ID_CLAIM': 'user_id',
   }

   # Incluir app de blacklist
   INSTALLED_APPS = [
       # ... otras apps ...
       'rest_framework_simplejwt.token_blacklist',
   ]

View de Login con Sesión Única
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/users/views.py

   from rest_framework import status
   from rest_framework.views import APIView
   from rest_framework.response import Response
   from rest_framework.permissions import AllowAny
   from rest_framework_simplejwt.tokens import RefreshToken
   from django.contrib.auth import authenticate
   from apps.users.models import UserSession
   from apps.common.audit import UserActionLog

   class LoginView(APIView):
       """
       Vista de login con política de sesión única.

       CNST-002: Implementa sesión única por usuario.
       Al hacer login, invalida sesiones previas.
       """

       permission_classes = [AllowAny]

       def post(self, request):
           username = request.data.get('username')
           password = request.data.get('password')

           if not username or not password:
               return Response(
                   {'error': 'Username y password requeridos'},
                   status=status.HTTP_400_BAD_REQUEST
               )

           # Autenticar usuario
           user = authenticate(username=username, password=password)

           if not user:
               # Auditoría de intento fallido
               UserActionLog.login(
                   user_id=0,
                   success=False,
                   ip=self._get_client_ip(request)
               )
               return Response(
                   {'error': 'Credenciales inválidas'},
                   status=status.HTTP_401_UNAUTHORIZED
               )

           if not user.is_active:
               return Response(
                   {'error': 'Usuario inactivo'},
                   status=status.HTTP_403_FORBIDDEN
               )

           # Verificar sesión existente
           existing_session = UserSession.get_active_session(user)
           session_replaced = existing_session is not None

           # Invalidar sesiones previas (sesión única)
           UserSession.invalidate_user_sessions(user)

           # Generar tokens JWT
           refresh = RefreshToken.for_user(user)

           # Crear sesión Django y registrar UserSession
           request.session.create()
           UserSession.create_session(
               user=user,
               session_key=request.session.session_key,
               request=request
           )

           # Auditoría de login exitoso
           UserActionLog.login(
               user_id=user.id,
               success=True,
               ip=self._get_client_ip(request)
           )

           response_data = {
               'access': str(refresh.access_token),
               'refresh': str(refresh),
               'user': {
                   'id': user.id,
                   'username': user.username,
                   'email': user.email,
               }
           }

           # Informar si se reemplazó sesión
           if session_replaced:
               response_data['message'] = 'Sesión anterior cerrada'

           return Response(response_data, status=status.HTTP_200_OK)

       def _get_client_ip(self, request):
           """Obtener IP del cliente."""
           x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
           if x_forwarded_for:
               return x_forwarded_for.split(',')[0].strip()
           return request.META.get('REMOTE_ADDR')


   class LogoutView(APIView):
       """
       Vista de logout.

       Invalida sesión y blacklistea tokens JWT.
       """

       def post(self, request):
           try:
               # Blacklistear refresh token
               refresh_token = request.data.get('refresh')
               if refresh_token:
                   token = RefreshToken(refresh_token)
                   token.blacklist()

               # Invalidar sesión
               if request.user.is_authenticated:
                   UserSession.invalidate_user_sessions(request.user)

                   # Auditoría
                   UserActionLog.logout(user_id=request.user.id)

               return Response(
                   {'message': 'Logout exitoso'},
                   status=status.HTTP_200_OK
               )

           except Exception:
               return Response(
                   {'message': 'Logout exitoso'},
                   status=status.HTTP_200_OK
               )

Limpieza de Sesiones
--------------------

Comando de Limpieza
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/management/commands/cleanup_sessions.py

   from django.core.management.base import BaseCommand
   from django.contrib.sessions.models import Session
   from django.utils import timezone
   from apps.users.models import UserSession
   import logging

   logger = logging.getLogger(__name__)

   class Command(BaseCommand):
       help = 'Limpiar sesiones expiradas de la base de datos'

       def add_arguments(self, parser):
           parser.add_argument(
               '--dry-run',
               action='store_true',
               help='Mostrar qué se eliminaría sin hacerlo'
           )

       def handle(self, *args, **options):
           dry_run = options['dry_run']

           if dry_run:
               self.stdout.write('Modo DRY-RUN: No se eliminarán datos')

           # Sesiones Django expiradas
           expired_sessions = Session.objects.filter(
               expire_date__lt=timezone.now()
           )
           expired_count = expired_sessions.count()

           # UserSessions huérfanas
           orphan_user_sessions = UserSession.objects.filter(
               session__isnull=True
           )
           orphan_count = orphan_user_sessions.count()

           self.stdout.write(f'Sesiones expiradas: {expired_count}')
           self.stdout.write(f'UserSessions huérfanas: {orphan_count}')

           if not dry_run:
               # Eliminar sesiones expiradas
               expired_sessions.delete()
               logger.info(f'Eliminadas {expired_count} sesiones expiradas')

               # Eliminar UserSessions huérfanas
               orphan_user_sessions.delete()
               logger.info(f'Eliminadas {orphan_count} UserSessions huérfanas')

               self.stdout.write(
                   self.style.SUCCESS('Limpieza completada')
               )
           else:
               self.stdout.write('DRY-RUN: No se eliminó nada')

Cron Job de Limpieza
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Ejecutar cada hora para limpiar sesiones expiradas
   0 * * * * cd /opt/iact && /opt/iact/venv/bin/python api/manage.py cleanup_sessions >> /opt/iact/logs/sessions.log 2>&1

Validación en Desarrollo
------------------------

Pre-commit Checklist
~~~~~~~~~~~~~~~~~~~~

Antes de hacer commit, verificar:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - NO existe ``import redis`` o ``from redis``
   * - [ ]
     - NO existe configuración de Redis en settings
   * - [ ]
     - NO existe ``SESSION_ENGINE = '...cache'``
   * - [ ]
     - SÍ existe ``SESSION_ENGINE = 'django.contrib.sessions.backends.db'``
   * - [ ]
     - SÍ existe ``SESSION_COOKIE_AGE = 900``

Code Review Checklist
~~~~~~~~~~~~~~~~~~~~~

Durante code review, rechazar si:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - Se intenta usar Redis o Memcached
   * - [ ]
     - Se configura caché en memoria
   * - [ ]
     - Se permite más de una sesión por usuario
   * - [ ]
     - No se implementa timeout de 15 minutos

Script de Validación
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # scripts/validate_no_redis.sh

   echo "Validando que no existan referencias a Redis..."

   ERRORS=0

   # Buscar imports de Redis
   if grep -r "import redis\|from redis" api/apps/; then
       echo "ERROR: Encontrado import de redis"
       ERRORS=$((ERRORS + 1))
   fi

   # Buscar configuración de Redis en settings
   if grep -r "RedisCache\|redis://" api/config/settings/; then
       echo "ERROR: Encontrada configuración de Redis"
       ERRORS=$((ERRORS + 1))
   fi

   # Verificar SESSION_ENGINE correcto
   if ! grep -q "SESSION_ENGINE.*db" api/config/settings/base.py; then
       echo "ERROR: SESSION_ENGINE no está configurado para BD"
       ERRORS=$((ERRORS + 1))
   fi

   if [ $ERRORS -eq 0 ]; then
       echo "OK: No se encontraron referencias a Redis"
       exit 0
   else
       echo "FALLO: $ERRORS violaciones de CNST-002 encontradas"
       exit 1
   fi

Excepciones
-----------

**NO EXISTEN EXCEPCIONES**

Esta restricción NO tiene excepciones.

Ningún módulo, componente o funcionalidad puede usar Redis, Memcached u otros sistemas de caché en memoria.

Si surge un requerimiento de caché, debe implementarse usando:

- Base de datos (para sesiones)
- Caché de Django en BD: ``django.core.cache.backends.db.DatabaseCache``
- Caché local en memoria del proceso (sin persistencia externa)

Alternativas Evaluadas y Rechazadas
-----------------------------------

Alternativa 1: Redis Interno del Cliente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Propuesta:** Solicitar instalación de Redis en infraestructura del cliente.

**Rechazada porque:**

- Cliente explícitamente indicó que no provee Redis
- Política de infraestructura simplificada
- No quieren servicios adicionales que mantener

Alternativa 2: Memcached
~~~~~~~~~~~~~~~~~~~~~~~~

**Propuesta:** Usar Memcached en lugar de Redis.

**Rechazada porque:**

- Misma limitación de infraestructura
- Cliente no provee ningún servicio de caché en memoria
- Preferencia por solución en BD existente

Alternativa 3: Sesiones en Archivos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Propuesta:** Usar SESSION_ENGINE = 'django.contrib.sessions.backends.file'

**Rechazada porque:**

- No escala en múltiples servidores
- Problemas de permisos en filesystem
- Más difícil de auditar
- BD es más confiable

Referencias
-----------

Documentos Relacionados
~~~~~~~~~~~~~~~~~~~~~~~

- RESTRICCIONES_COMPLETAS_DEL_SISTEMA_IACT.md
- CNST-005: Seguridad DRF Checklist
- CNST-009: Logging y Auditoría Inmutable

Implementación de Referencia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``api/config/settings/base.py`` - Configuración de sesiones
- ``api/apps/users/models.py`` - Modelo UserSession
- ``api/apps/common/middleware.py`` - Middlewares de sesión
- ``api/apps/users/views.py`` - LoginView, LogoutView

Historial de Cambios
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 50 20

   * - Versión
     - Fecha
     - Cambios
     - Autor
   * - 1.0.0
     - 2025-12-17
     - Versión inicial, sin referencias externas
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
   * - Security Officer
     - [Nombre]
     - [Pendiente]

----

**Fin del Documento CNST-002**