CNST-005: Seguridad Django REST Framework
=========================================

:ID: CNST-005
:Versión: 1.0.0
:Fecha: 2025-12-17
:Estado: Vigente
:Clasificación: CRÍTICO - NO NEGOCIABLE
:Origen: Mejores prácticas de seguridad

----

Propósito
---------

Este documento establece los estándares de seguridad obligatorios para todas las APIs REST del Sistema IACT - IVR Analytics & Customer Tracking, usando Django REST Framework (DRF).

Contexto
--------

Origen de la Restricción
~~~~~~~~~~~~~~~~~~~~~~~~

Estándares de seguridad requeridos para proteger el sistema IACT y los datos del cliente. Todas las APIs deben implementar autenticación, autorización y validación adecuadas.

Justificación
~~~~~~~~~~~~~

- Proteger datos sensibles del cliente
- Prevenir accesos no autorizados
- Cumplir con políticas de seguridad corporativas
- Minimizar superficie de ataque
- Garantizar trazabilidad de acciones

Aplicable a
~~~~~~~~~~~

- Todas las APIs REST del sistema
- Todos los ViewSets y APIViews
- Serializers y validaciones
- Middlewares de seguridad
- Todas las fases del ciclo de vida

Autenticación
-------------

Configuración Obligatoria
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/config/settings/base.py
   
   REST_FRAMEWORK = {
       # Autenticación: JWT obligatorio
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ],
       
       # Permisos: Autenticado por defecto
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
       
       # Throttling: Límites de requests
       'DEFAULT_THROTTLE_CLASSES': [
           'rest_framework.throttling.AnonRateThrottle',
           'rest_framework.throttling.UserRateThrottle',
       ],
       'DEFAULT_THROTTLE_RATES': {
           'anon': '20/hour',      # No autenticados
           'user': '1000/hour',    # Autenticados
       },
       
       # Paginación obligatoria
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 50,
       
       # Parsers permitidos
       'DEFAULT_PARSER_CLASSES': [
           'rest_framework.parsers.JSONParser',
       ],
       
       # Renderers
       'DEFAULT_RENDERER_CLASSES': [
           'rest_framework.renderers.JSONRenderer',
       ],
       
       # Manejo de excepciones
       'EXCEPTION_HANDLER': 'apps.common.exceptions.custom_exception_handler',
       
       # Formato de fechas
       'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
       'DATE_FORMAT': '%Y-%m-%d',
   }

Configuración JWT
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/config/settings/base.py
   
   from datetime import timedelta
   import os
   
   SIMPLE_JWT = {
       # Tiempos de vida
       'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
       'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
       
       # Rotación de tokens
       'ROTATE_REFRESH_TOKENS': True,
       'BLACKLIST_AFTER_ROTATION': True,
       
       # Algoritmo
       'ALGORITHM': 'HS256',
       'SIGNING_KEY': os.environ.get('JWT_SECRET_KEY'),
       
       # Headers
       'AUTH_HEADER_TYPES': ('Bearer',),
       'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
       
       # Claims
       'USER_ID_FIELD': 'id',
       'USER_ID_CLAIM': 'user_id',
       
       # Validaciones
       'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
       'TOKEN_TYPE_CLAIM': 'token_type',
   }
   
   # App de blacklist
   INSTALLED_APPS = [
       # ...
       'rest_framework_simplejwt.token_blacklist',
   ]

Autorización (Permisos)
-----------------------

Permisos Base
~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/permissions.py
   
   from rest_framework import permissions
   
   class IsActiveUser(permissions.BasePermission):
       """
       Verificar que el usuario esté activo.
       
       Uso:
           permission_classes = [IsAuthenticated, IsActiveUser]
       """
       
       message = 'Usuario inactivo'
       
       def has_permission(self, request, view):
           return request.user and request.user.is_active


   class IsAdminUser(permissions.BasePermission):
       """
       Verificar que el usuario sea administrador (staff).
       
       Uso en vistas administrativas.
       """
       
       message = 'Se requieren permisos de administrador'
       
       def has_permission(self, request, view):
           return (
               request.user and 
               request.user.is_authenticated and 
               request.user.is_staff
           )


   class IsOwnerOrAdmin(permissions.BasePermission):
       """
       Permitir acceso al dueño del recurso o a administradores.
       
       El modelo debe tener campo 'user' o 'owner' o 'created_by'.
       """
       
       message = 'No tiene permiso para este recurso'
       
       def has_object_permission(self, request, view, obj):
           # Admin siempre tiene acceso
           if request.user.is_staff:
               return True
           
           # Verificar propiedad
           owner_fields = ['user', 'owner', 'created_by', 'recipient']
           
           for field in owner_fields:
               if hasattr(obj, field):
                   owner = getattr(obj, field)
                   if owner == request.user:
                       return True
           
           return False

Permisos Basados en Roles (RBAC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/permissions.py
   
   class HasRole(permissions.BasePermission):
       """
       Verificar que usuario tenga rol específico.
       
       Uso:
           class MyView(APIView):
               permission_classes = [IsAuthenticated, HasRole]
               required_roles = ['R004', 'R005']  # REPORTS_VIEWER, REPORTS_EXPORTER
       """
       
       message = 'No tiene el rol requerido'
       
       def has_permission(self, request, view):
           if not request.user.is_authenticated:
               return False
           
           required_roles = getattr(view, 'required_roles', [])
           
           if not required_roles:
               return True
           
           # Obtener roles del usuario
           user_roles = request.user.roles.filter(
               is_active=True
           ).values_list('role_id', flat=True)
           
           # Verificar si tiene al menos uno de los roles requeridos
           return any(role in user_roles for role in required_roles)


   class IsReportsViewer(permissions.BasePermission):
       """
       Permiso para ver reportes.
       
       Roles permitidos: R004 (REPORTS_VIEWER), R005 (REPORTS_EXPORTER),
       R007 (REPORTS_ADVANCED_CREATOR), R015 (SYSTEM_ADMIN)
       """
       
       message = 'No tiene permiso para ver reportes'
       ALLOWED_ROLES = ['R004', 'R005', 'R007', 'R015']
       
       def has_permission(self, request, view):
           if not request.user.is_authenticated:
               return False
           
           if request.user.is_staff:
               return True
           
           user_roles = request.user.roles.filter(
               is_active=True
           ).values_list('role_id', flat=True)
           
           return any(role in user_roles for role in self.ALLOWED_ROLES)


   class IsDataAnalyst(permissions.BasePermission):
       """
       Permiso para análisis avanzado de datos.
       
       Roles permitidos: R010 (DATA_ANALYST), R015 (SYSTEM_ADMIN)
       """
       
       message = 'No tiene permiso de analista de datos'
       ALLOWED_ROLES = ['R010', 'R015']
       
       def has_permission(self, request, view):
           if not request.user.is_authenticated:
               return False
           
           if request.user.is_staff:
               return True
           
           user_roles = request.user.roles.filter(
               is_active=True
           ).values_list('role_id', flat=True)
           
           return any(role in user_roles for role in self.ALLOWED_ROLES)


   class IsAlertsManager(permissions.BasePermission):
       """
       Permiso para gestionar alertas.
       
       Roles permitidos: R012 (ALERTS_CONFIGURATOR), R013 (ALERTS_EVENTS_MANAGER),
       R014 (ALERTS_TEMPLATES_MANAGER), R015 (SYSTEM_ADMIN)
       """
       
       message = 'No tiene permiso para gestionar alertas'
       ALLOWED_ROLES = ['R012', 'R013', 'R014', 'R015']
       
       def has_permission(self, request, view):
           if not request.user.is_authenticated:
               return False
           
           if request.user.is_staff:
               return True
           
           user_roles = request.user.roles.filter(
               is_active=True
           ).values_list('role_id', flat=True)
           
           return any(role in user_roles for role in self.ALLOWED_ROLES)


   class CanManageUsers(permissions.BasePermission):
       """
       Permiso para gestionar usuarios.
       
       Roles permitidos: R001 (USERS_FULL_MANAGER), R002 (USERS_PARTIAL_MANAGER),
       R015 (SYSTEM_ADMIN)
       """
       
       message = 'No tiene permiso para gestionar usuarios'
       ALLOWED_ROLES = ['R001', 'R002', 'R015']
       
       def has_permission(self, request, view):
           if not request.user.is_authenticated:
               return False
           
           user_roles = request.user.roles.filter(
               is_active=True
           ).values_list('role_id', flat=True)
           
           return any(role in user_roles for role in self.ALLOWED_ROLES)

Throttling (Rate Limiting)
--------------------------

Throttles Personalizados
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/throttling.py
   
   from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
   
   class LoginRateThrottle(AnonRateThrottle):
       """
       Throttle para endpoint de login.
       
       Previene ataques de fuerza bruta.
       Límite: 5 intentos por minuto por IP.
       """
       
       rate = '5/minute'
       scope = 'login'


   class ReportGenerationThrottle(UserRateThrottle):
       """
       Throttle para generación de reportes.
       
       Reportes son costosos, limitar frecuencia.
       Límite: 10 reportes por hora.
       """
       
       rate = '10/hour'
       scope = 'reports'


   class ExportThrottle(UserRateThrottle):
       """
       Throttle para exportación de datos.
       
       Exportaciones son costosas, limitar frecuencia.
       Límite: 5 exportaciones por hora.
       """
       
       rate = '5/hour'
       scope = 'exports'


   class ETLTriggerThrottle(UserRateThrottle):
       """
       Throttle para trigger manual de ETL.
       
       Prevenir abuso del ETL manual.
       Límite: 1 por hora.
       """
       
       rate = '1/hour'
       scope = 'etl_trigger'

Configuración de Throttles
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/config/settings/base.py
   
   REST_FRAMEWORK = {
       # ... otras configuraciones ...
       
       'DEFAULT_THROTTLE_RATES': {
           'anon': '20/hour',
           'user': '1000/hour',
           'login': '5/minute',
           'reports': '10/hour',
           'exports': '5/hour',
           'etl_trigger': '1/hour',
       },
   }

Validación de Datos
-------------------

Serializers con Validación
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/reports/serializers.py
   
   from rest_framework import serializers
   from django.utils import timezone
   from datetime import timedelta
   
   class DateRangeSerializer(serializers.Serializer):
       """
       Serializer para validar rangos de fechas.
       
       Validaciones:
       - start_date requerido
       - end_date requerido
       - end_date >= start_date
       - Rango máximo: 90 días
       - No fechas futuras
       """
       
       start_date = serializers.DateField(required=True)
       end_date = serializers.DateField(required=True)
       
       def validate_start_date(self, value):
           """Validar fecha inicio."""
           if value > timezone.now().date():
               raise serializers.ValidationError(
                   'La fecha de inicio no puede ser futura'
               )
           return value
       
       def validate_end_date(self, value):
           """Validar fecha fin."""
           if value > timezone.now().date():
               raise serializers.ValidationError(
                   'La fecha de fin no puede ser futura'
               )
           return value
       
       def validate(self, data):
           """Validaciones cruzadas."""
           start = data.get('start_date')
           end = data.get('end_date')
           
           if start and end:
               if end < start:
                   raise serializers.ValidationError({
                       'end_date': 'Fecha fin debe ser mayor o igual a fecha inicio'
                   })
               
               # Máximo 90 días
               max_range = timedelta(days=90)
               if (end - start) > max_range:
                   raise serializers.ValidationError({
                       'date_range': 'El rango máximo es de 90 días'
                   })
           
           return data


   class ReportRequestSerializer(serializers.Serializer):
       """
       Serializer para solicitud de reporte.
       
       Validaciones completas para generación de reportes.
       """
       
       report_type = serializers.ChoiceField(
           choices=[
               ('calls_summary', 'Resumen de Llamadas'),
               ('queue_performance', 'Rendimiento por Cola'),
               ('hourly_distribution', 'Distribución Horaria'),
           ]
       )
       start_date = serializers.DateField()
       end_date = serializers.DateField()
       queue_ids = serializers.ListField(
           child=serializers.IntegerField(min_value=1),
           required=False,
           max_length=50
       )
       format = serializers.ChoiceField(
           choices=['json', 'csv', 'excel'],
           default='json'
       )
       
       def validate_queue_ids(self, value):
           """Validar que las colas existan."""
           if value:
               from apps.analytics.models import CallMetric
               
               existing_queues = CallMetric.objects.filter(
                   queue_id__in=value
               ).values_list('queue_id', flat=True).distinct()
               
               invalid = set(value) - set(existing_queues)
               if invalid:
                   raise serializers.ValidationError(
                       f'Colas no encontradas: {list(invalid)}'
                   )
           
           return value
       
       def validate(self, data):
           """Validaciones cruzadas."""
           start = data.get('start_date')
           end = data.get('end_date')
           
           if end < start:
               raise serializers.ValidationError({
                   'end_date': 'Debe ser mayor o igual a fecha inicio'
               })
           
           if (end - start).days > 90:
               raise serializers.ValidationError({
                   'date_range': 'Rango máximo: 90 días'
               })
           
           return data

Manejo de Excepciones
---------------------

Handler Personalizado
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/exceptions.py
   
   from rest_framework.views import exception_handler
   from rest_framework.response import Response
   from rest_framework import status
   from django.core.exceptions import PermissionDenied
   from django.http import Http404
   import logging
   
   logger = logging.getLogger('api')
   
   def custom_exception_handler(exc, context):
       """
       Handler personalizado de excepciones DRF.
       
       Estandariza formato de errores y registra en log.
       """
       # Llamar al handler por defecto primero
       response = exception_handler(exc, context)
       
       # Obtener información del request
       request = context.get('request')
       view = context.get('view')
       
       if response is not None:
           # Estandarizar formato de error
           error_data = {
               'error': True,
               'status_code': response.status_code,
               'message': _get_error_message(exc, response),
               'detail': response.data if isinstance(response.data, dict) else {'detail': response.data}
           }
           
           response.data = error_data
           
           # Log de errores 4xx y 5xx
           if response.status_code >= 400:
               logger.warning(
                   f'API Error: {response.status_code} - '
                   f'User={getattr(request.user, "username", "anonymous")} - '
                   f'Path={request.path} - '
                   f'Message={error_data["message"]}'
               )
       
       else:
           # Excepciones no manejadas por DRF
           logger.error(
               f'Unhandled Exception: {type(exc).__name__} - {str(exc)}',
               exc_info=True
           )
           
           response = Response(
               {
                   'error': True,
                   'status_code': 500,
                   'message': 'Error interno del servidor',
                   'detail': {}
               },
               status=status.HTTP_500_INTERNAL_SERVER_ERROR
           )
       
       return response


   def _get_error_message(exc, response):
       """Obtener mensaje de error legible."""
       status_messages = {
           400: 'Solicitud inválida',
           401: 'No autenticado',
           403: 'Permiso denegado',
           404: 'Recurso no encontrado',
           405: 'Método no permitido',
           429: 'Demasiadas solicitudes',
           500: 'Error interno del servidor',
       }
       
       return status_messages.get(
           response.status_code,
           str(exc) if str(exc) else 'Error desconocido'
       )

Paginación
----------

Paginador Estándar
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/pagination.py
   
   from rest_framework.pagination import PageNumberPagination
   from rest_framework.response import Response
   
   class StandardPagination(PageNumberPagination):
       """
       Paginación estándar para APIs IACT.
       
       - page_size: 50 por defecto
       - max_page_size: 200 máximo
       - Incluye metadata útil en respuesta
       """
       
       page_size = 50
       page_size_query_param = 'page_size'
       max_page_size = 200
       page_query_param = 'page'
       
       def get_paginated_response(self, data):
           return Response({
               'pagination': {
                   'count': self.page.paginator.count,
                   'total_pages': self.page.paginator.num_pages,
                   'current_page': self.page.number,
                   'page_size': self.get_page_size(self.request),
                   'has_next': self.page.has_next(),
                   'has_previous': self.page.has_previous(),
               },
               'links': {
                   'next': self.get_next_link(),
                   'previous': self.get_previous_link(),
               },
               'results': data
           })


   class LargePagination(PageNumberPagination):
       """
       Paginación para resultados grandes (exportaciones).
       
       Permite hasta 1000 registros por página para exportaciones.
       """
       
       page_size = 100
       page_size_query_param = 'page_size'
       max_page_size = 1000

Ejemplo de Vista Completa
-------------------------

Vista con Todas las Protecciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/reports/views.py
   
   from rest_framework import viewsets, status
   from rest_framework.decorators import action
   from rest_framework.response import Response
   from rest_framework.permissions import IsAuthenticated
   from apps.common.permissions import IsReportsViewer, IsDataAnalyst
   from apps.common.throttling import ReportGenerationThrottle, ExportThrottle
   from apps.common.pagination import StandardPagination
   from apps.common.audit import UserActionLog
   from apps.reports.serializers import ReportRequestSerializer
   from apps.analytics.models import CallMetric
   
   class ReportViewSet(viewsets.ViewSet):
       """
       ViewSet para generación de reportes.
       
       Seguridad implementada:
       - Autenticación JWT obligatoria
       - Permisos basados en roles (RBAC)
       - Throttling por endpoint
       - Validación de datos
       - Auditoría de acciones
       """
       
       permission_classes = [IsAuthenticated, IsReportsViewer]
       pagination_class = StandardPagination
       
       def get_throttles(self):
           """Throttles específicos por acción."""
           if self.action == 'generate':
               return [ReportGenerationThrottle()]
           elif self.action == 'export':
               return [ExportThrottle()]
           return super().get_throttles()
       
       def list(self, request):
           """
           Listar reportes disponibles.
           
           GET /api/v1/reports/
           """
           reports = [
               {
                   'id': 'calls_summary',
                   'name': 'Resumen de Llamadas',
                   'description': 'Totales y promedios por período'
               },
               {
                   'id': 'queue_performance',
                   'name': 'Rendimiento por Cola',
                   'description': 'Métricas desglosadas por cola'
               },
               {
                   'id': 'hourly_distribution',
                   'name': 'Distribución Horaria',
                   'description': 'Volumen de llamadas por hora'
               },
           ]
           
           return Response({'reports': reports})
       
       @action(detail=False, methods=['post'])
       def generate(self, request):
           """
           Generar reporte.
           
           POST /api/v1/reports/generate/
           
           Body:
               {
                   "report_type": "calls_summary",
                   "start_date": "2025-01-01",
                   "end_date": "2025-01-31",
                   "queue_ids": [1, 2, 3],
                   "format": "json"
               }
           """
           # Validar datos
           serializer = ReportRequestSerializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           data = serializer.validated_data
           
           # Generar reporte
           report_data = self._generate_report(data)
           
           # Auditoría
           UserActionLog.record(
               user_id=request.user.id,
               action='REPORT_GENERATE',
               resource=f"report:{data['report_type']}",
               result='SUCCESS',
               details={
                   'start_date': str(data['start_date']),
                   'end_date': str(data['end_date']),
                   'format': data['format']
               }
           )
           
           return Response({
               'report_type': data['report_type'],
               'generated_at': timezone.now().isoformat(),
               'data': report_data
           })
       
       @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsDataAnalyst])
       def export(self, request):
           """
           Exportar datos (requiere rol DATA_ANALYST).
           
           POST /api/v1/reports/export/
           """
           serializer = ReportRequestSerializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           data = serializer.validated_data
           
           # Solo analistas pueden exportar
           # (ya validado por permission_classes)
           
           # Generar exportación
           export_data = self._generate_export(data)
           
           # Auditoría
           UserActionLog.record(
               user_id=request.user.id,
               action='DATA_EXPORT',
               resource=f"export:{data['report_type']}",
               result='SUCCESS'
           )
           
           return Response(export_data)
       
       def _generate_report(self, data):
           """Generar datos del reporte."""
           queryset = CallMetric.objects.filter(
               metric_date__range=[data['start_date'], data['end_date']]
           )
           
           if data.get('queue_ids'):
               queryset = queryset.filter(queue_id__in=data['queue_ids'])
           
           # Agregar según tipo de reporte
           if data['report_type'] == 'calls_summary':
               from django.db.models import Sum, Avg
               
               return queryset.aggregate(
                   total_calls=Sum('total_calls'),
                   completed=Sum('completed_calls'),
                   abandoned=Sum('abandoned_calls'),
                   avg_duration=Avg('avg_duration'),
                   avg_wait=Avg('avg_wait_time')
               )
           
           # ... otros tipos de reporte
           return {}
       
       def _generate_export(self, data):
           """Generar exportación de datos."""
           # Implementación de exportación
           return {'status': 'export_generated'}

Validación en Desarrollo
------------------------

Pre-commit Checklist
~~~~~~~~~~~~~~~~~~~~

Antes de hacer commit, verificar:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - Todas las vistas tienen ``permission_classes``
   * - [ ]
     - No existe ``AllowAny`` excepto en login/registro
   * - [ ]
     - Serializers validan todos los inputs
   * - [ ]
     - Throttling configurado en endpoints sensibles
   * - [ ]
     - Paginación en endpoints que retornan listas

Code Review Checklist
~~~~~~~~~~~~~~~~~~~~~

Durante code review, rechazar si:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - Vista sin autenticación (excepto login)
   * - [ ]
     - Datos de request usados sin validar
   * - [ ]
     - Queries sin límites (paginación)
   * - [ ]
     - Permisos no verificados para acción

Script de Validación
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # scripts/validate_api_security.sh
   
   echo "Validando seguridad de APIs..."
   
   ERRORS=0
   
   # Buscar AllowAny fuera de auth
   ALLOW_ANY=$(grep -r "AllowAny" api/apps/ --include="*.py" | grep -v "auth\|login\|register" | wc -l)
   if [ $ALLOW_ANY -gt 0 ]; then
       echo "WARNING: $ALLOW_ANY usos de AllowAny fuera de auth"
   fi
   
   # Buscar vistas sin permission_classes
   NO_PERMS=$(grep -r "class.*APIView\|class.*ViewSet" api/apps/ --include="*.py" -A 5 | grep -v "permission_classes" | grep "class.*View" | wc -l)
   if [ $NO_PERMS -gt 0 ]; then
       echo "WARNING: Posibles vistas sin permission_classes"
   fi
   
   # Verificar que JWT está configurado
   if ! grep -q "JWTAuthentication" api/config/settings/base.py; then
       echo "ERROR: JWT no configurado"
       ERRORS=$((ERRORS + 1))
   fi
   
   if [ $ERRORS -eq 0 ]; then
       echo "OK: Configuración de seguridad básica correcta"
       exit 0
   else
       echo "FALLO: $ERRORS errores de seguridad encontrados"
       exit 1
   fi

Referencias
-----------

Documentos Relacionados
~~~~~~~~~~~~~~~~~~~~~~~

- CNST-002: Gestión de Sesiones en Base de Datos
- CNST-009: Logging y Auditoría Inmutable
- Modelo RBAC IACT v4.0 (18 roles funcionales)

Implementación de Referencia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``api/config/settings/base.py`` - Configuración DRF
- ``api/apps/common/permissions.py`` - Permisos personalizados
- ``api/apps/common/throttling.py`` - Throttles
- ``api/apps/common/pagination.py`` - Paginadores
- ``api/apps/common/exceptions.py`` - Handler de excepciones

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
     - Versión inicial con permisos RBAC
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

**Fin del Documento CNST-005**
