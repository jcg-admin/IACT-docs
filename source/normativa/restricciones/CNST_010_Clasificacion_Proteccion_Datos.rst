CNST-010: Clasificación y Protección de Datos
=============================================

:ID: CNST-010
:Versión: 1.0.0
:Fecha: 2025-12-17
:Estado: Vigente
:Clasificación: CRÍTICO - NO NEGOCIABLE
:Origen: Políticas de seguridad del cliente

----

Propósito
---------

Este documento establece la clasificación de datos y controles de protección obligatorios para el Sistema IACT - IVR Analytics & Customer Tracking, definiendo qué datos son accesibles según el rol del usuario.

Contexto
--------

Origen de la Restricción
~~~~~~~~~~~~~~~~~~~~~~~~

Políticas de seguridad del cliente y requerimientos de privacidad de datos. Los datos del sistema deben clasificarse y protegerse según su nivel de sensibilidad.

Justificación
~~~~~~~~~~~~~

- Proteger información sensible del negocio
- Cumplir con políticas corporativas de seguridad
- Garantizar acceso basado en necesidad de conocer
- Minimizar exposición de datos sensibles
- Facilitar auditoría de acceso a datos

Aplicable a
~~~~~~~~~~~

- Todos los datos del sistema IACT
- APIs y endpoints
- Reportes y exportaciones
- Dashboard y visualizaciones
- Todas las fases del ciclo de vida

Clasificación de Datos
----------------------

Niveles de Clasificación
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Nivel
     - Nombre
     - Descripción
   * - C1
     - PÚBLICO
     - Datos que pueden ser vistos por cualquier usuario autenticado
   * - C2
     - INTERNO
     - Datos operacionales de uso general interno
   * - C3
     - RESTRINGIDO
     - Datos sensibles con acceso limitado por rol
   * - C4
     - CONFIDENCIAL
     - Datos altamente sensibles, solo administradores

Clasificación por Tipo de Dato
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Dato
     - Nivel
     - Roles con Acceso
   * - Métricas agregadas (totales diarios)
     - C1
     - Todos los usuarios autenticados
   * - Métricas por cola
     - C2
     - R004+: REPORTS_VIEWER y superiores
   * - Detalles de llamadas
     - C3
     - R010: DATA_ANALYST, R015: SYSTEM_ADMIN
   * - Configuración del sistema
     - C4
     - R015: SYSTEM_ADMIN
   * - Logs de auditoría
     - C4
     - R015: SYSTEM_ADMIN
   * - Datos de usuarios
     - C3
     - R001, R002: USER_MANAGERS, R015
   * - Reportes generados
     - C2
     - Creador del reporte + R005+

Matriz de Acceso por Rol
------------------------

Roles y Permisos de Datos
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 15 15

   * - Rol
     - C1
     - C2
     - C3
     - C4
     - Notas
   * - R003: DASHBOARD_VIEWER
     - Sí
     - No
     - No
     - No
     - Solo métricas públicas
   * - R004: REPORTS_VIEWER
     - Sí
     - Sí
     - No
     - No
     - Visualiza reportes
   * - R005: REPORTS_EXPORTER
     - Sí
     - Sí
     - No
     - No
     - Puede exportar C1-C2
   * - R010: DATA_ANALYST
     - Sí
     - Sí
     - Sí
     - No
     - Análisis avanzado
   * - R015: SYSTEM_ADMIN
     - Sí
     - Sí
     - Sí
     - Sí
     - Acceso total

Implementación de Clasificación
-------------------------------

Modelo de Clasificación
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/classification.py
   
   from enum import Enum
   from typing import List, Set
   
   class DataClassification(Enum):
       """
       Niveles de clasificación de datos CNST-010.
       """
       PUBLIC = 'C1'        # Público - todos los usuarios
       INTERNAL = 'C2'      # Interno - usuarios con rol de reportes
       RESTRICTED = 'C3'    # Restringido - analistas y admins
       CONFIDENTIAL = 'C4'  # Confidencial - solo admins
   
   
   class DataAccessControl:
       """
       Control de acceso a datos según clasificación.
       
       CNST-010: Define qué roles pueden acceder a cada nivel.
       """
       
       # Mapeo de clasificación a roles permitidos
       ACCESS_MATRIX = {
           DataClassification.PUBLIC: {
               'R003', 'R004', 'R005', 'R006', 'R007',
               'R008', 'R009', 'R010', 'R011', 'R012',
               'R013', 'R014', 'R015', 'R016', 'R017', 'R018'
           },
           DataClassification.INTERNAL: {
               'R004', 'R005', 'R006', 'R007', 'R008',
               'R009', 'R010', 'R011', 'R015', 'R016'
           },
           DataClassification.RESTRICTED: {
               'R001', 'R002', 'R010', 'R015'
           },
           DataClassification.CONFIDENTIAL: {
               'R015'
           },
       }
       
       @classmethod
       def can_access(cls, user, classification: DataClassification) -> bool:
           """
           Verificar si usuario puede acceder a datos de esta clasificación.
           
           Args:
               user: Usuario Django
               classification: Nivel de clasificación
           
           Returns:
               True si tiene acceso, False si no
           """
           if not user or not user.is_authenticated:
               return False
           
           # Superusuarios tienen acceso total
           if user.is_superuser:
               return True
           
           # Obtener roles del usuario
           user_roles = set(
               user.roles.filter(is_active=True).values_list('role_id', flat=True)
           )
           
           # Verificar si algún rol tiene acceso
           allowed_roles = cls.ACCESS_MATRIX.get(classification, set())
           
           return bool(user_roles & allowed_roles)
       
       @classmethod
       def get_max_classification(cls, user) -> DataClassification:
           """
           Obtener máximo nivel de clasificación accesible por usuario.
           
           Args:
               user: Usuario Django
           
           Returns:
               Nivel máximo de clasificación
           """
           if not user or not user.is_authenticated:
               return None
           
           if user.is_superuser:
               return DataClassification.CONFIDENTIAL
           
           user_roles = set(
               user.roles.filter(is_active=True).values_list('role_id', flat=True)
           )
           
           # Verificar de mayor a menor
           for classification in [
               DataClassification.CONFIDENTIAL,
               DataClassification.RESTRICTED,
               DataClassification.INTERNAL,
               DataClassification.PUBLIC,
           ]:
               allowed_roles = cls.ACCESS_MATRIX.get(classification, set())
               if user_roles & allowed_roles:
                   return classification
           
           return None
       
       @classmethod
       def filter_fields(cls, user, data: dict, field_classifications: dict) -> dict:
           """
           Filtrar campos de un diccionario según clasificación.
           
           Args:
               user: Usuario Django
               data: Diccionario con datos
               field_classifications: Mapeo campo -> clasificación
           
           Returns:
               Diccionario con solo campos permitidos
           """
           filtered = {}
           
           for field, value in data.items():
               classification = field_classifications.get(
                   field, DataClassification.PUBLIC
               )
               
               if cls.can_access(user, classification):
                   filtered[field] = value
           
           return filtered

Decorador de Clasificación
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/decorators.py
   
   import functools
   from rest_framework.response import Response
   from rest_framework import status
   from apps.common.classification import DataClassification, DataAccessControl
   from apps.common.models import UserActionLog
   import logging
   
   logger = logging.getLogger('security')
   
   def requires_classification(classification: DataClassification):
       """
       Decorador que restringe acceso según clasificación de datos.
       
       CNST-010: Usar en vistas que exponen datos clasificados.
       
       Args:
           classification: Nivel mínimo requerido
       
       Uso:
           @requires_classification(DataClassification.RESTRICTED)
           def get_call_details(request, call_id):
               ...
       """
       def decorator(func):
           @functools.wraps(func)
           def wrapper(request, *args, **kwargs):
               user = request.user
               
               if not DataAccessControl.can_access(user, classification):
                   # Registrar intento de acceso denegado
                   UserActionLog.record(
                       user=user,
                       action='VIEW',
                       resource=f'{request.method}:{request.path}',
                       result='DENIED',
                       ip_address=_get_client_ip(request),
                       details={
                           'required_classification': classification.value,
                           'reason': 'Clasificación insuficiente'
                       }
                   )
                   
                   logger.warning(
                       f'Acceso denegado por clasificación: '
                       f'User={user.username}, '
                       f'Path={request.path}, '
                       f'Required={classification.value}'
                   )
                   
                   return Response(
                       {
                           'error': 'Acceso denegado',
                           'message': f'Se requiere acceso a datos {classification.name}',
                           'code': 'CLASSIFICATION_DENIED'
                       },
                       status=status.HTTP_403_FORBIDDEN
                   )
               
               return func(request, *args, **kwargs)
           return wrapper
       return decorator


   def _get_client_ip(request):
       """Obtener IP del cliente."""
       x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
       if x_forwarded_for:
           return x_forwarded_for.split(',')[0].strip()
       return request.META.get('REMOTE_ADDR')

Permiso DRF de Clasificación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/permissions.py
   
   from rest_framework import permissions
   from apps.common.classification import DataClassification, DataAccessControl
   
   class RequiresDataClassification(permissions.BasePermission):
       """
       Permiso DRF basado en clasificación de datos.
       
       Uso en ViewSet:
           class CallDetailViewSet(viewsets.ReadOnlyModelViewSet):
               permission_classes = [IsAuthenticated, RequiresDataClassification]
               required_classification = DataClassification.RESTRICTED
       """
       
       def has_permission(self, request, view):
           classification = getattr(
               view, 
               'required_classification', 
               DataClassification.PUBLIC
           )
           
           return DataAccessControl.can_access(request.user, classification)
       
       def has_object_permission(self, request, view, obj):
           # Si el objeto tiene clasificación propia, usarla
           obj_classification = getattr(
               obj, 
               'classification', 
               None
           )
           
           if obj_classification:
               return DataAccessControl.can_access(
                   request.user, 
                   DataClassification(obj_classification)
               )
           
           return self.has_permission(request, view)


   class CanAccessRestrictedData(permissions.BasePermission):
       """
       Permiso para datos restringidos (C3).
       
       Roles: R001, R002, R010, R015
       """
       
       message = 'Se requiere acceso a datos restringidos'
       
       def has_permission(self, request, view):
           return DataAccessControl.can_access(
               request.user, 
               DataClassification.RESTRICTED
           )


   class CanAccessConfidentialData(permissions.BasePermission):
       """
       Permiso para datos confidenciales (C4).
       
       Roles: R015 (SYSTEM_ADMIN)
       """
       
       message = 'Se requiere acceso a datos confidenciales'
       
       def has_permission(self, request, view):
           return DataAccessControl.can_access(
               request.user, 
               DataClassification.CONFIDENTIAL
           )

Serializers con Clasificación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/analytics/serializers.py
   
   from rest_framework import serializers
   from apps.common.classification import DataClassification, DataAccessControl
   
   class MetricSerializer(serializers.Serializer):
       """
       Serializer de métricas con campos clasificados.
       
       CNST-010: Campos se filtran según rol del usuario.
       """
       
       # Clasificación de campos
       FIELD_CLASSIFICATIONS = {
           'metric_date': DataClassification.PUBLIC,
           'total_calls': DataClassification.PUBLIC,
           'completed_calls': DataClassification.INTERNAL,
           'abandoned_calls': DataClassification.INTERNAL,
           'avg_duration': DataClassification.INTERNAL,
           'avg_wait_time': DataClassification.INTERNAL,
           'queue_id': DataClassification.INTERNAL,
           'queue_name': DataClassification.INTERNAL,
           'hourly_breakdown': DataClassification.RESTRICTED,
           'performance_score': DataClassification.RESTRICTED,
       }
       
       # Campos públicos (C1)
       metric_date = serializers.DateField()
       total_calls = serializers.IntegerField()
       
       # Campos internos (C2)
       completed_calls = serializers.IntegerField(required=False)
       abandoned_calls = serializers.IntegerField(required=False)
       avg_duration = serializers.DecimalField(
           max_digits=10, decimal_places=2, required=False
       )
       avg_wait_time = serializers.DecimalField(
           max_digits=10, decimal_places=2, required=False
       )
       queue_id = serializers.IntegerField(required=False)
       queue_name = serializers.CharField(required=False)
       
       # Campos restringidos (C3)
       hourly_breakdown = serializers.JSONField(required=False)
       performance_score = serializers.DecimalField(
           max_digits=5, decimal_places=2, required=False
       )
       
       def to_representation(self, instance):
           """Filtrar campos según clasificación del usuario."""
           data = super().to_representation(instance)
           
           # Obtener usuario del contexto
           request = self.context.get('request')
           if not request or not request.user:
               # Sin usuario, solo campos públicos
               return {
                   k: v for k, v in data.items()
                   if self.FIELD_CLASSIFICATIONS.get(k) == DataClassification.PUBLIC
               }
           
           # Filtrar según acceso del usuario
           return DataAccessControl.filter_fields(
               request.user,
               data,
               self.FIELD_CLASSIFICATIONS
           )


   class UserSerializer(serializers.Serializer):
       """
       Serializer de usuario con campos clasificados.
       """
       
       FIELD_CLASSIFICATIONS = {
           'id': DataClassification.INTERNAL,
           'username': DataClassification.INTERNAL,
           'email': DataClassification.RESTRICTED,
           'is_active': DataClassification.INTERNAL,
           'roles': DataClassification.RESTRICTED,
           'last_login': DataClassification.RESTRICTED,
           'date_joined': DataClassification.RESTRICTED,
       }
       
       id = serializers.IntegerField()
       username = serializers.CharField()
       email = serializers.EmailField(required=False)
       is_active = serializers.BooleanField()
       roles = serializers.ListField(required=False)
       last_login = serializers.DateTimeField(required=False)
       date_joined = serializers.DateTimeField(required=False)
       
       def to_representation(self, instance):
           data = super().to_representation(instance)
           request = self.context.get('request')
           
           if not request or not request.user:
               return {'id': data.get('id'), 'username': data.get('username')}
           
           return DataAccessControl.filter_fields(
               request.user,
               data,
               self.FIELD_CLASSIFICATIONS
           )

Vistas con Clasificación
------------------------

Ejemplo de Vista Protegida
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/analytics/views.py
   
   from rest_framework import viewsets, status
   from rest_framework.decorators import action
   from rest_framework.response import Response
   from rest_framework.permissions import IsAuthenticated
   from apps.common.permissions import RequiresDataClassification, CanAccessRestrictedData
   from apps.common.classification import DataClassification
   from apps.common.decorators import requires_classification
   from apps.common.models import UserActionLog
   from apps.analytics.models import CallMetric
   from apps.analytics.serializers import MetricSerializer
   
   class MetricsViewSet(viewsets.ReadOnlyModelViewSet):
       """
       ViewSet de métricas con control de clasificación.
       
       - list/retrieve: C2 (INTERNAL)
       - detailed: C3 (RESTRICTED)
       """
       
       permission_classes = [IsAuthenticated, RequiresDataClassification]
       required_classification = DataClassification.INTERNAL
       serializer_class = MetricSerializer
       
       def get_queryset(self):
           return CallMetric.objects.all()
       
       def list(self, request):
           """Listar métricas (nivel INTERNAL)."""
           queryset = self.get_queryset()
           
           # Aplicar filtros
           start_date = request.query_params.get('start_date')
           end_date = request.query_params.get('end_date')
           
           if start_date:
               queryset = queryset.filter(metric_date__gte=start_date)
           if end_date:
               queryset = queryset.filter(metric_date__lte=end_date)
           
           # Paginar
           page = self.paginate_queryset(queryset)
           serializer = self.get_serializer(page, many=True)
           
           # Auditar acceso
           UserActionLog.record(
               user=request.user,
               action='VIEW',
               resource='metrics:list',
               result='SUCCESS',
               details={'count': len(page)}
           )
           
           return self.get_paginated_response(serializer.data)
       
       @action(detail=False, methods=['get'], 
               permission_classes=[IsAuthenticated, CanAccessRestrictedData])
       def detailed(self, request):
           """
           Métricas detalladas (nivel RESTRICTED).
           
           Solo accesible por R010 (DATA_ANALYST) y R015 (SYSTEM_ADMIN).
           """
           queryset = self.get_queryset()
           
           # Incluir datos detallados
           data = list(queryset.values(
               'metric_date',
               'queue_id',
               'total_calls',
               'completed_calls',
               'abandoned_calls',
               'avg_duration',
               'avg_wait_time',
           )[:1000])
           
           # Auditar
           UserActionLog.record(
               user=request.user,
               action='VIEW',
               resource='metrics:detailed',
               result='SUCCESS',
               details={
                   'classification': DataClassification.RESTRICTED.value,
                   'count': len(data)
               }
           )
           
           return Response({'metrics': data})


   class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
       """
       ViewSet de logs de auditoría (nivel CONFIDENTIAL).
       
       Solo R015 (SYSTEM_ADMIN) puede acceder.
       """
       
       permission_classes = [IsAuthenticated, RequiresDataClassification]
       required_classification = DataClassification.CONFIDENTIAL
       
       def get_queryset(self):
           from apps.common.models import UserActionLog
           return UserActionLog.objects.all()
       
       def list(self, request):
           """Listar logs de auditoría."""
           queryset = self.get_queryset().order_by('-created_at')[:500]
           
           data = [
               {
                   'id': log.id,
                   'user': log.user.username if log.user else 'Sistema',
                   'action': log.action,
                   'resource': log.resource,
                   'result': log.result,
                   'ip_address': log.ip_address,
                   'created_at': log.created_at.isoformat(),
               }
               for log in queryset
           ]
           
           return Response({'logs': data})

Protección de Exportaciones
---------------------------

Exportación con Clasificación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/exports/services.py
   
   from apps.common.classification import DataClassification, DataAccessControl
   from apps.common.models import UserActionLog
   import logging
   
   logger = logging.getLogger('exports')
   
   class ClassifiedExporter:
       """
       Exportador que respeta clasificación de datos.
       
       CNST-010: Las exportaciones solo incluyen datos
       que el usuario está autorizado a ver.
       """
       
       # Clasificación de campos exportables
       EXPORT_FIELDS = {
           'metric_date': DataClassification.PUBLIC,
           'total_calls': DataClassification.PUBLIC,
           'completed_calls': DataClassification.INTERNAL,
           'abandoned_calls': DataClassification.INTERNAL,
           'avg_duration': DataClassification.INTERNAL,
           'avg_wait_time': DataClassification.INTERNAL,
           'queue_id': DataClassification.INTERNAL,
           'completion_rate': DataClassification.RESTRICTED,
           'abandon_rate': DataClassification.RESTRICTED,
           'service_level': DataClassification.RESTRICTED,
       }
       
       def __init__(self, user):
           self.user = user
           self.max_classification = DataAccessControl.get_max_classification(user)
       
       def get_exportable_fields(self):
           """Obtener campos que el usuario puede exportar."""
           exportable = []
           
           for field, classification in self.EXPORT_FIELDS.items():
               if DataAccessControl.can_access(self.user, classification):
                   exportable.append(field)
           
           return exportable
       
       def export(self, queryset, format='csv'):
           """
           Exportar datos filtrando por clasificación.
           
           Args:
               queryset: QuerySet de datos
               format: Formato de exportación
           
           Returns:
               Path al archivo generado
           """
           allowed_fields = self.get_exportable_fields()
           
           if not allowed_fields:
               raise PermissionError('No tiene acceso a ningún campo exportable')
           
           # Filtrar datos
           data = list(queryset.values(*allowed_fields))
           
           # Auditar exportación
           UserActionLog.record(
               user=self.user,
               action='EXPORT',
               resource='metrics:export',
               result='SUCCESS',
               details={
                   'fields': allowed_fields,
                   'record_count': len(data),
                   'format': format,
                   'max_classification': self.max_classification.value
               }
           )
           
           logger.info(
               f'Exportación: User={self.user.username}, '
               f'Records={len(data)}, '
               f'Fields={len(allowed_fields)}, '
               f'MaxClassification={self.max_classification.value}'
           )
           
           # Generar archivo
           return self._generate_file(data, allowed_fields, format)
       
       def _generate_file(self, data, fields, format):
           """Generar archivo de exportación."""
           import csv
           import os
           from datetime import datetime
           from django.conf import settings
           
           export_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
           os.makedirs(export_dir, exist_ok=True)
           
           timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
           filename = f'export_{self.user.id}_{timestamp}.{format}'
           filepath = os.path.join(export_dir, filename)
           
           if format == 'csv':
               with open(filepath, 'w', newline='', encoding='utf-8') as f:
                   writer = csv.DictWriter(f, fieldnames=fields)
                   writer.writeheader()
                   writer.writerows(data)
           
           return filepath

Validación en Desarrollo
------------------------

Pre-commit Checklist
~~~~~~~~~~~~~~~~~~~~

Antes de hacer commit, verificar:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - Endpoints sensibles tienen ``RequiresDataClassification``
   * - [ ]
     - Serializers filtran campos según clasificación
   * - [ ]
     - Exportaciones respetan nivel de acceso
   * - [ ]
     - Accesos a datos C3/C4 tienen auditoría

Code Review Checklist
~~~~~~~~~~~~~~~~~~~~~

Durante code review, rechazar si:

.. list-table::
   :header-rows: 0
   :widths: 10 90

   * - [ ]
     - Endpoint expone datos sin verificar clasificación
   * - [ ]
     - Datos C3/C4 accesibles por roles no autorizados
   * - [ ]
     - Exportación incluye campos no permitidos
   * - [ ]
     - Falta auditoría en acceso a datos sensibles

Script de Validación
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # scripts/validate_data_classification.sh
   
   echo "Validando clasificación de datos..."
   
   ERRORS=0
   
   # Verificar que existe el módulo de clasificación
   if [ ! -f "api/apps/common/classification.py" ]; then
       echo "ERROR: Módulo de clasificación no encontrado"
       ERRORS=$((ERRORS + 1))
   fi
   
   # Buscar endpoints sin permisos
   if grep -r "permission_classes\s*=\s*\[\]" api/apps/ --include="*.py" | grep -v "health\|login"; then
       echo "WARNING: Endpoints sin permisos encontrados"
   fi
   
   # Verificar uso de clasificación en serializers
   if ! grep -q "FIELD_CLASSIFICATIONS" api/apps/analytics/serializers.py 2>/dev/null; then
       echo "WARNING: Serializers sin clasificación de campos"
   fi
   
   if [ $ERRORS -eq 0 ]; then
       echo "OK: Clasificación de datos configurada"
       exit 0
   else
       echo "FALLO: $ERRORS errores de clasificación encontrados"
       exit 1
   fi

Auditoría de Acceso a Datos
---------------------------

Monitoreo de Accesos
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # api/apps/common/monitoring.py
   
   from django.utils import timezone
   from datetime import timedelta
   from apps.common.models import UserActionLog
   from apps.common.notifications import notify_admins
   import logging
   
   logger = logging.getLogger('security')
   
   def check_suspicious_access():
       """
       Detectar patrones de acceso sospechosos.
       
       Alertar cuando:
       - Usuario accede a muchos recursos C3/C4 en poco tiempo
       - Múltiples intentos denegados
       - Acceso fuera de horario laboral
       """
       now = timezone.now()
       one_hour_ago = now - timedelta(hours=1)
       
       # Detectar múltiples accesos denegados
       denied_by_user = UserActionLog.objects.filter(
           result='DENIED',
           created_at__gte=one_hour_ago
       ).values('user__username').annotate(
           count=models.Count('id')
       ).filter(count__gte=5)
       
       for entry in denied_by_user:
           notify_admins(
               subject='Alerta: Múltiples accesos denegados',
               body=f"Usuario {entry['user__username']} tiene "
                    f"{entry['count']} accesos denegados en la última hora.",
               priority='HIGH'
           )
           
           logger.warning(
               f"Accesos denegados sospechosos: "
               f"User={entry['user__username']}, Count={entry['count']}"
           )
       
       # Detectar acceso excesivo a datos restringidos
       restricted_access = UserActionLog.objects.filter(
           action='VIEW',
           result='SUCCESS',
           created_at__gte=one_hour_ago,
           details__contains='RESTRICTED'
       ).values('user__username').annotate(
           count=models.Count('id')
       ).filter(count__gte=100)
       
       for entry in restricted_access:
           logger.info(
               f"Alto volumen de acceso a datos restringidos: "
               f"User={entry['user__username']}, Count={entry['count']}"
           )

Referencias
-----------

Documentos Relacionados
~~~~~~~~~~~~~~~~~~~~~~~

- CNST-005: Seguridad Django REST Framework (permisos base)
- CNST-009: Logging y Auditoría Inmutable
- Modelo RBAC IACT v4.0 (18 roles funcionales)

Implementación de Referencia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``api/apps/common/classification.py`` - Sistema de clasificación
- ``api/apps/common/permissions.py`` - Permisos de clasificación
- ``api/apps/analytics/serializers.py`` - Serializers con filtrado
- ``api/apps/exports/services.py`` - Exportación clasificada

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
     - Versión inicial alineada con RBAC v4.0
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

**Fin del Documento CNST-010**
