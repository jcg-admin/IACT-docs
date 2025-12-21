CNST-006: Antipatrones de Arquitectura Prohibidos
=================================================

:ID: CNST-006
:Versión: 1.0.0
:Fecha: 2025-12-17
:Estado: Vigente
:Clasificación: CRÍTICO - NO NEGOCIABLE
:Origen: Estándares de calidad de código

----

Propósito
---------

Este documento establece los antipatrones de arquitectura y diseño prohibidos en el Sistema IACT - IVR Analytics & Customer Tracking, con ejemplos de código incorrecto y correcto para cada caso.

Contexto
--------

Origen de la Restricción
~~~~~~~~~~~~~~~~~~~~~~~~

Estándares de calidad de código requeridos para mantener un sistema mantenible, escalable y libre de deuda técnica. El código debe seguir principios SOLID y Clean Code.

Justificación
~~~~~~~~~~~~~

- Facilitar mantenimiento a largo plazo
- Reducir deuda técnica
- Mejorar legibilidad del código
- Facilitar testing y debugging
- Permitir onboarding rápido de nuevos desarrolladores

Aplicable a
~~~~~~~~~~~

- Todo el código Python del backend
- Código JavaScript/TypeScript del frontend
- Configuraciones y scripts
- Todas las fases del ciclo de vida

Antipatrones Prohibidos
-----------------------

Antipatrón 1: God Class (Clase Dios)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Una clase que hace demasiadas cosas, tiene demasiadas responsabilidades o conoce demasiado sobre otras partes del sistema.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Clase con más de 500 líneas
- Más de 10 métodos públicos
- Nombre genérico: Manager, Handler, Processor, Service
- Múltiples responsabilidades no relacionadas

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - God Class
   class SystemManager:
       """Esta clase hace TODO - antipatrón."""
       
       def __init__(self):
           self.db = Database()
           self.cache = Cache()
           self.logger = Logger()
           self.emailer = Emailer()  # Violación CNST-001
       
       def authenticate_user(self, username, password):
           # Autenticación
           pass
       
       def generate_report(self, params):
           # Generación de reportes
           pass
       
       def run_etl(self):
           # Proceso ETL
           pass
       
       def send_notification(self, user, message):
           # Notificaciones
           pass
       
       def backup_database(self):
           # Backups
           pass
       
       def validate_permissions(self, user, resource):
           # Permisos
           pass
       
       # ... 50 métodos más ...

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Responsabilidad única por clase
   
   class AuthenticationService:
       """Maneja solo autenticación."""
       
       def authenticate(self, username, password):
           pass
       
       def validate_token(self, token):
           pass
   
   
   class ReportGenerator:
       """Genera reportes."""
       
       def generate(self, report_type, params):
           pass
       
       def export_to_csv(self, data):
           pass
   
   
   class ETLPipeline:
       """Ejecuta proceso ETL."""
       
       def run(self, start_date, end_date):
           pass
   
   
   class NotificationSender:
       """Envía notificaciones internas (CNST-001)."""
       
       def send(self, recipient, subject, body):
           from apps.common.models import InternalMessage
           InternalMessage.objects.create(
               recipient=recipient,
               subject=subject,
               body=body
           )

Antipatrón 2: Spaghetti Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Código con flujo de control enredado, difícil de seguir, con múltiples niveles de anidación y sin estructura clara.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Más de 3 niveles de anidación (if dentro de if dentro de if)
- Funciones de más de 50 líneas
- Múltiples returns dispersos
- Lógica mezclada sin separación

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Spaghetti Code
   def process_call_data(data):
       if data:
           if 'calls' in data:
               for call in data['calls']:
                   if call.get('valid'):
                       if call.get('duration') > 0:
                           if call.get('queue_id'):
                               queue = get_queue(call['queue_id'])
                               if queue:
                                   if queue.is_active:
                                       metric = CallMetric()
                                       metric.queue_id = call['queue_id']
                                       metric.duration = call['duration']
                                       if call.get('outcome') == 'COMPLETED':
                                           metric.completed = True
                                       else:
                                           if call.get('outcome') == 'ABANDONED':
                                               metric.abandoned = True
                                           else:
                                               metric.other = True
                                       metric.save()
                                       return True
       return False

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Código limpio con early returns y funciones pequeñas
   
   def process_call_data(data):
       """Procesar datos de llamadas."""
       if not data or 'calls' not in data:
           return False
       
       processed = False
       for call in data['calls']:
           if _process_single_call(call):
               processed = True
       
       return processed
   
   
   def _process_single_call(call):
       """Procesar una llamada individual."""
       if not _is_valid_call(call):
           return False
       
       queue = _get_active_queue(call['queue_id'])
       if not queue:
           return False
       
       metric = _create_metric(call)
       metric.save()
       return True
   
   
   def _is_valid_call(call):
       """Validar datos de llamada."""
       return (
           call.get('valid') and
           call.get('duration', 0) > 0 and
           call.get('queue_id')
       )
   
   
   def _get_active_queue(queue_id):
       """Obtener cola activa."""
       queue = get_queue(queue_id)
       return queue if queue and queue.is_active else None
   
   
   def _create_metric(call):
       """Crear métrica desde llamada."""
       metric = CallMetric(
           queue_id=call['queue_id'],
           duration=call['duration']
       )
       
       outcome = call.get('outcome', '')
       metric.completed = (outcome == 'COMPLETED')
       metric.abandoned = (outcome == 'ABANDONED')
       metric.other = (outcome not in ['COMPLETED', 'ABANDONED'])
       
       return metric

Antipatrón 3: Copy-Paste Programming
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Duplicación de código en múltiples lugares en vez de extraer funcionalidad común.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Bloques de código idénticos o casi idénticos
- Misma lógica en múltiples archivos
- Correcciones que deben hacerse en múltiples lugares

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Código duplicado
   
   # En views/reports.py
   class ReportView(APIView):
       def get(self, request):
           user = request.user
           if not user.is_authenticated:
               return Response({'error': 'No autenticado'}, status=401)
           if not user.is_active:
               return Response({'error': 'Usuario inactivo'}, status=403)
           # ... lógica del reporte
   
   # En views/analytics.py (MISMO CÓDIGO)
   class AnalyticsView(APIView):
       def get(self, request):
           user = request.user
           if not user.is_authenticated:
               return Response({'error': 'No autenticado'}, status=401)
           if not user.is_active:
               return Response({'error': 'Usuario inactivo'}, status=403)
           # ... lógica de analytics
   
   # En views/exports.py (MISMO CÓDIGO otra vez)
   class ExportView(APIView):
       def get(self, request):
           user = request.user
           if not user.is_authenticated:
               return Response({'error': 'No autenticado'}, status=401)
           if not user.is_active:
               return Response({'error': 'Usuario inactivo'}, status=403)
           # ... lógica de exportación

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Extraer a permisos reutilizables
   
   # En common/permissions.py
   from rest_framework import permissions
   
   class IsActiveUser(permissions.BasePermission):
       """Permiso reutilizable: usuario activo."""
       
       message = 'Usuario inactivo'
       
       def has_permission(self, request, view):
           return (
               request.user and
               request.user.is_authenticated and
               request.user.is_active
           )
   
   
   # En views/reports.py
   class ReportView(APIView):
       permission_classes = [IsActiveUser]
       
       def get(self, request):
           # Solo lógica del reporte
           pass
   
   
   # En views/analytics.py
   class AnalyticsView(APIView):
       permission_classes = [IsActiveUser]
       
       def get(self, request):
           # Solo lógica de analytics
           pass
   
   
   # En views/exports.py
   class ExportView(APIView):
       permission_classes = [IsActiveUser]
       
       def get(self, request):
           # Solo lógica de exportación
           pass

Antipatrón 4: Magic Numbers/Strings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Uso de valores literales sin explicación en el código, haciendo difícil entender su propósito.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Números sin contexto: ``if status == 1``
- Strings repetidos: ``if role == 'admin'``
- Valores de configuración hardcoded

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Magic numbers y strings
   
   def check_permissions(user, action):
       if user.role == 1:  # ¿Qué es 1?
           return True
       if user.role == 2 and action in ['read', 'list']:  # ¿Qué es 2?
           return True
       if user.login_attempts > 5:  # ¿Por qué 5?
           lock_user(user)
       return False
   
   def get_metrics(days=30):  # ¿Por qué 30?
       timeout = 300  # ¿300 qué?
       max_records = 10000  # ¿Por qué este límite?
       # ...

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Constantes con nombres descriptivos
   
   # En common/constants.py
   class UserRole:
       """Roles de usuario (ver modelo RBAC)."""
       ADMIN = 'R015'  # SYSTEM_ADMIN
       ANALYST = 'R010'  # DATA_ANALYST
       VIEWER = 'R004'  # REPORTS_VIEWER
   
   
   class SecurityLimits:
       """Límites de seguridad."""
       MAX_LOGIN_ATTEMPTS = 5
       LOCKOUT_DURATION_MINUTES = 30
   
   
   class QueryLimits:
       """Límites de consultas."""
       DEFAULT_DAYS_RANGE = 30
       MAX_DAYS_RANGE = 90
       QUERY_TIMEOUT_SECONDS = 300
       MAX_EXPORT_RECORDS = 10000
   
   
   # Uso correcto
   from common.constants import UserRole, SecurityLimits, QueryLimits
   
   def check_permissions(user, action):
       if user.role == UserRole.ADMIN:
           return True
       
       if user.role == UserRole.VIEWER and action in ['read', 'list']:
           return True
       
       if user.login_attempts > SecurityLimits.MAX_LOGIN_ATTEMPTS:
           lock_user(user)
       
       return False
   
   
   def get_metrics(days=QueryLimits.DEFAULT_DAYS_RANGE):
       timeout = QueryLimits.QUERY_TIMEOUT_SECONDS
       max_records = QueryLimits.MAX_EXPORT_RECORDS
       # ...

Antipatrón 5: Hardcoded Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Valores de configuración (URLs, credenciales, paths) escritos directamente en el código.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- URLs hardcoded
- Credenciales en código
- Paths absolutos
- Configuraciones específicas de ambiente

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Configuración hardcoded
   
   import mysql.connector
   
   def connect_to_ivr():
       return mysql.connector.connect(
           host='192.168.1.100',
           user='ivr_user',
           password='secretpassword123',  # NUNCA hacer esto
           database='ivr_production'
       )
   
   def get_api_url():
       return 'https://api.cliente.com/v1'
   
   LOG_PATH = '/var/log/iact/app.log'

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Configuración desde variables de entorno
   
   # En config/settings/base.py
   import os
   from decouple import config
   
   DATABASES = {
       'ivr_readonly': {
           'ENGINE': 'django.db.backends.mysql',
           'HOST': config('DB_IVR_HOST'),
           'USER': config('DB_IVR_USER'),
           'PASSWORD': config('DB_IVR_PASSWORD'),
           'NAME': config('DB_IVR_NAME'),
       }
   }
   
   API_BASE_URL = config('API_BASE_URL', default='http://localhost:8000')
   LOG_PATH = config('LOG_PATH', default='/var/log/iact/app.log')
   
   
   # En .env (NO commitear)
   DB_IVR_HOST=192.168.1.100
   DB_IVR_USER=ivr_user
   DB_IVR_PASSWORD=secretpassword123
   DB_IVR_NAME=ivr_production
   API_BASE_URL=https://api.cliente.com/v1
   LOG_PATH=/var/log/iact/app.log
   
   
   # En .env.example (SÍ commitear)
   DB_IVR_HOST=<HOST>
   DB_IVR_USER=<USER>
   DB_IVR_PASSWORD=<PASSWORD>
   DB_IVR_NAME=<DATABASE>
   API_BASE_URL=<URL>
   LOG_PATH=<PATH>

Antipatrón 6: Premature Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Optimizar código antes de que sea necesario, añadiendo complejidad innecesaria sin beneficio medible.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Caché complejo para datos poco accedidos
- Estructuras de datos complejas para casos simples
- Código difícil de leer "por rendimiento"

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Optimización prematura
   
   class MetricsCache:
       """Caché complejo innecesario para pocos datos."""
       
       _instance = None
       _cache = {}
       _timestamps = {}
       _hit_count = {}
       _miss_count = {}
       _lock = threading.Lock()
       
       def __new__(cls):
           if cls._instance is None:
               cls._instance = super().__new__(cls)
           return cls._instance
       
       def get(self, key, ttl=300):
           with self._lock:
               if key in self._cache:
                   if time.time() - self._timestamps[key] < ttl:
                       self._hit_count[key] = self._hit_count.get(key, 0) + 1
                       return self._cache[key]
               self._miss_count[key] = self._miss_count.get(key, 0) + 1
               return None
       
       # ... 100 líneas más de complejidad

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Simple hasta que se demuestre necesidad
   
   def get_daily_metrics(date):
       """Obtener métricas del día (sin caché innecesario)."""
       return CallMetric.objects.filter(metric_date=date).aggregate(
           total=Sum('total_calls'),
           completed=Sum('completed_calls'),
           abandoned=Sum('abandoned_calls')
       )
   
   # Si después se demuestra que necesita caché,
   # usar el sistema de caché de Django (simple)
   
   from django.core.cache import cache
   
   def get_daily_metrics_cached(date):
       """Métricas con caché simple (solo si es necesario)."""
       cache_key = f'metrics_{date}'
       
       result = cache.get(cache_key)
       if result is None:
           result = CallMetric.objects.filter(metric_date=date).aggregate(
               total=Sum('total_calls'),
               completed=Sum('completed_calls'),
               abandoned=Sum('abandoned_calls')
           )
           cache.set(cache_key, result, timeout=3600)
       
       return result

Antipatrón 7: Callback Hell / Pyramid of Doom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Múltiples niveles de callbacks anidados que hacen el código difícil de leer y mantener.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Callbacks dentro de callbacks
- Indentación excesiva
- Difícil seguir flujo de ejecución

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Callback hell
   
   def process_data(data, callback):
       def on_validate(is_valid):
           if is_valid:
               def on_transform(transformed):
                   def on_save(saved):
                       if saved:
                           def on_notify(notified):
                               callback(True)
                           notify_completion(on_notify)
                       else:
                           callback(False)
                   save_data(transformed, on_save)
               transform_data(data, on_transform)
           else:
               callback(False)
       validate_data(data, on_validate)

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Flujo lineal y claro
   
   def process_data(data):
       """Procesar datos con flujo claro."""
       if not validate_data(data):
           return False
       
       transformed = transform_data(data)
       
       if not save_data(transformed):
           return False
       
       notify_completion()
       return True
   
   
   # O con excepciones para control de flujo
   
   class ProcessingError(Exception):
       pass
   
   
   def process_data(data):
       """Procesar datos con manejo de errores."""
       try:
           validated = validate_data(data)
           transformed = transform_data(validated)
           saved = save_data(transformed)
           notify_completion(saved)
           return True
       except ProcessingError as e:
           logger.error(f'Error procesando datos: {e}')
           return False

Antipatrón 8: Feature Envy
~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Un método que usa más datos o métodos de otra clase que de la suya propia.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Múltiples llamadas a métodos de otro objeto
- Acceso constante a atributos de otra clase
- La lógica pertenece más a la otra clase

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Feature Envy
   
   class ReportGenerator:
       def calculate_queue_stats(self, queue):
           # Esta lógica debería estar en Queue o QueueStats
           total_calls = queue.get_total_calls()
           completed = queue.get_completed_calls()
           abandoned = queue.get_abandoned_calls()
           
           completion_rate = completed / total_calls if total_calls else 0
           abandon_rate = abandoned / total_calls if total_calls else 0
           
           avg_duration = queue.get_avg_duration()
           avg_wait = queue.get_avg_wait_time()
           
           service_level = queue.get_service_level()
           
           return {
               'completion_rate': completion_rate,
               'abandon_rate': abandon_rate,
               'avg_duration': avg_duration,
               'avg_wait': avg_wait,
               'service_level': service_level
           }

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - La lógica está donde pertenece
   
   class QueueStatistics:
       """Estadísticas de una cola."""
       
       def __init__(self, queue_id, start_date, end_date):
           self.queue_id = queue_id
           self.metrics = self._load_metrics(start_date, end_date)
       
       def _load_metrics(self, start_date, end_date):
           return CallMetric.objects.filter(
               queue_id=self.queue_id,
               metric_date__range=[start_date, end_date]
           ).aggregate(
               total=Sum('total_calls'),
               completed=Sum('completed_calls'),
               abandoned=Sum('abandoned_calls'),
               avg_duration=Avg('avg_duration'),
               avg_wait=Avg('avg_wait_time')
           )
       
       @property
       def completion_rate(self):
           total = self.metrics['total'] or 0
           completed = self.metrics['completed'] or 0
           return completed / total if total else 0
       
       @property
       def abandon_rate(self):
           total = self.metrics['total'] or 0
           abandoned = self.metrics['abandoned'] or 0
           return abandoned / total if total else 0
       
       def to_dict(self):
           return {
               'completion_rate': self.completion_rate,
               'abandon_rate': self.abandon_rate,
               'avg_duration': self.metrics['avg_duration'],
               'avg_wait': self.metrics['avg_wait']
           }
   
   
   class ReportGenerator:
       def get_queue_stats(self, queue_id, start_date, end_date):
           stats = QueueStatistics(queue_id, start_date, end_date)
           return stats.to_dict()

Antipatrón 9: Primitive Obsession
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Usar tipos primitivos (strings, ints) donde objetos de dominio serían más apropiados.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Strings que representan conceptos complejos
- Validaciones repetidas del mismo tipo de dato
- Múltiples parámetros relacionados

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Primitive Obsession
   
   def create_report(
       start_year, start_month, start_day,
       end_year, end_month, end_day,
       queue_ids_str,  # "1,2,3"
       format_type     # "csv" o "excel"
   ):
       # Validar fechas manualmente cada vez
       if start_month < 1 or start_month > 12:
           raise ValueError('Mes inválido')
       
       # Parsear queue_ids manualmente
       queue_ids = [int(x) for x in queue_ids_str.split(',')]
       
       # Validar formato manualmente
       if format_type not in ['csv', 'excel', 'pdf']:
           raise ValueError('Formato inválido')
       
       # ...

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Objetos de dominio
   
   from dataclasses import dataclass
   from datetime import date
   from enum import Enum
   from typing import List
   
   class ExportFormat(Enum):
       CSV = 'csv'
       EXCEL = 'excel'
       PDF = 'pdf'
   
   
   @dataclass
   class DateRange:
       """Rango de fechas validado."""
       
       start: date
       end: date
       
       def __post_init__(self):
           if self.end < self.start:
               raise ValueError('Fecha fin debe ser >= fecha inicio')
           
           if (self.end - self.start).days > 90:
               raise ValueError('Rango máximo: 90 días')
       
       @classmethod
       def last_n_days(cls, days: int):
           end = date.today()
           start = end - timedelta(days=days)
           return cls(start=start, end=end)
   
   
   @dataclass
   class ReportRequest:
       """Solicitud de reporte validada."""
       
       date_range: DateRange
       queue_ids: List[int]
       format: ExportFormat
       
       def __post_init__(self):
           if not self.queue_ids:
               raise ValueError('Debe especificar al menos una cola')
           
           if len(self.queue_ids) > 50:
               raise ValueError('Máximo 50 colas por reporte')
   
   
   # Uso limpio
   def create_report(request: ReportRequest):
       """Crear reporte con datos validados."""
       # request ya está validado por el dataclass
       metrics = CallMetric.objects.filter(
           queue_id__in=request.queue_ids,
           metric_date__range=[request.date_range.start, request.date_range.end]
       )
       # ...

Antipatrón 10: Shotgun Surgery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descripción
^^^^^^^^^^^

Un cambio requiere modificaciones en muchos lugares diferentes del código.

Señales de Alerta
^^^^^^^^^^^^^^^^^

- Cambiar un campo requiere modificar 10+ archivos
- Lógica relacionada dispersa en todo el proyecto
- Difícil saber todos los lugares afectados por un cambio

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PROHIBIDO - Lógica dispersa
   
   # En models.py
   class User(models.Model):
       role_code = models.CharField(max_length=10)
   
   # En views.py
   def can_view_reports(user):
       return user.role_code in ['R004', 'R005', 'R007', 'R015']
   
   # En api/views.py (duplicado)
   def check_report_access(user):
       return user.role_code in ['R004', 'R005', 'R007', 'R015']
   
   # En templates/base.html
   # {% if user.role_code in 'R004,R005,R007,R015' %}
   
   # En serializers.py
   def validate_user(user):
       if user.role_code not in ['R004', 'R005', 'R007', 'R015']:
           raise ValidationError('Sin permisos')
   
   # Agregar un nuevo rol requiere cambiar TODOS estos lugares

Código CORRECTO
^^^^^^^^^^^^^^^

.. code-block:: python

   # CORRECTO - Lógica centralizada
   
   # En common/permissions.py (UN solo lugar)
   
   class RolePermissions:
       """Permisos centralizados por rol."""
       
       REPORT_VIEWERS = ['R004', 'R005', 'R007', 'R015']
       DATA_ANALYSTS = ['R010', 'R015']
       USER_MANAGERS = ['R001', 'R002', 'R015']
       ALERT_MANAGERS = ['R012', 'R013', 'R014', 'R015']
       
       @classmethod
       def can_view_reports(cls, user):
           return cls._has_any_role(user, cls.REPORT_VIEWERS)
       
       @classmethod
       def can_analyze_data(cls, user):
           return cls._has_any_role(user, cls.DATA_ANALYSTS)
       
       @classmethod
       def can_manage_users(cls, user):
           return cls._has_any_role(user, cls.USER_MANAGERS)
       
       @classmethod
       def _has_any_role(cls, user, allowed_roles):
           if not user or not user.is_authenticated:
               return False
           if user.is_staff:
               return True
           
           user_roles = user.roles.filter(
               is_active=True
           ).values_list('role_id', flat=True)
           
           return any(role in user_roles for role in allowed_roles)
   
   
   # Uso en cualquier parte del sistema
   from common.permissions import RolePermissions
   
   # En views.py
   if RolePermissions.can_view_reports(request.user):
       # ...
   
   # En serializers.py
   if not RolePermissions.can_view_reports(user):
       raise ValidationError('Sin permisos')
   
   # Agregar nuevo rol: cambiar SOLO RolePermissions

Validación en Desarrollo
------------------------

Pre-commit Checklist
~~~~~~~~~~~~~~~~~~~~

Antes de hacer commit, verificar:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - Ninguna clase supera 300 líneas
   * - [ ]
     - Ninguna función supera 30 líneas
   * - [ ]
     - No hay más de 3 niveles de anidación
   * - [ ]
     - No hay código duplicado (DRY)
   * - [ ]
     - No hay magic numbers/strings
   * - [ ]
     - Configuración en variables de entorno

Code Review Checklist
~~~~~~~~~~~~~~~~~~~~~

Durante code review, rechazar si:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - Se detecta God Class
   * - [ ]
     - Código spaghetti con anidación excesiva
   * - [ ]
     - Código duplicado sin extraer
   * - [ ]
     - Credenciales o URLs hardcoded
   * - [ ]
     - Optimizaciones sin justificación medible

Script de Validación
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # scripts/validate_code_quality.sh
   
   echo "Validando calidad de código..."
   
   ERRORS=0
   
   # Verificar archivos muy largos (posible God Class)
   LONG_FILES=$(find api/apps -name "*.py" -exec wc -l {} \; | awk '$1 > 500 {print $2}')
   if [ -n "$LONG_FILES" ]; then
       echo "WARNING: Archivos con más de 500 líneas:"
       echo "$LONG_FILES"
   fi
   
   # Buscar credenciales hardcoded
   if grep -r "password\s*=\s*['\"]" api/apps/ --include="*.py" | grep -v "password=None\|password=''\|get_password"; then
       echo "ERROR: Posibles passwords hardcoded"
       ERRORS=$((ERRORS + 1))
   fi
   
   # Buscar magic numbers en condiciones
   if grep -rE "if.*==\s*[0-9]{2,}" api/apps/ --include="*.py" | grep -v "status_code\|HTTP_"; then
       echo "WARNING: Posibles magic numbers en condiciones"
   fi
   
   # Ejecutar flake8
   flake8 api/apps/ --max-line-length=100 --max-complexity=10
   
   if [ $ERRORS -eq 0 ]; then
       echo "OK: Validación de calidad pasada"
       exit 0
   else
       echo "FALLO: $ERRORS errores de calidad encontrados"
       exit 1
   fi

Referencias
-----------

Documentos Relacionados
~~~~~~~~~~~~~~~~~~~~~~~

- CNST-005: Seguridad Django REST Framework
- CNST-009: Logging y Auditoría Inmutable
- Modelo RBAC IACT v4.0

Implementación de Referencia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``api/apps/common/permissions.py`` - Permisos centralizados
- ``api/apps/common/constants.py`` - Constantes del sistema
- ``api/config/settings/`` - Configuración por ambiente

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
     - Versión inicial con 10 antipatrones
     - Equipo IACT

Aprobaciones
------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Rol
     - Nombre
     - Firma / Fecha
   * - Tech Lead
     - [Nombre]
     - [Pendiente]
   * - Code Quality Lead
     - [Nombre]
     - [Pendiente]

----

**Fin del Documento CNST-006**
