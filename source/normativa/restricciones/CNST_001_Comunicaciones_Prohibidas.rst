CNST-001: Comunicaciones Prohibidas
====================================

:ID: CNST-001
:Versión: 1.1.0
:Fecha: 2026-01-03
:Estado: VIGENTE
:Clasificación: CRÍTICO - NO NEGOCIABLE
:Origen: Restricción del cliente

----

Propósito
---------

Este documento establece la prohibición absoluta de uso de servicios de correo electrónico (SMTP) en el Sistema IACT - IVR Analytics & Customer Tracking, y define el mecanismo obligatorio de notificaciones mediante buzón interno.

Contexto
--------

Origen de la Restricción
~~~~~~~~~~~~~~~~~~~~~~~~

Restricción de negocio impuesta por el cliente. El cliente NO permite que aplicaciones corporativas envíen correos electrónicos a través de servicios SMTP externos o internos.

Justificación del Cliente
~~~~~~~~~~~~~~~~~~~~~~~~~

- Control centralizado de comunicaciones corporativas
- Prevención de spam interno
- Auditoría de comunicaciones
- Cumplimiento de políticas de seguridad de información

Aplicable a
~~~~~~~~~~~

- Sistema IACT completo
- Todos los módulos y componentes
- Todos los casos de uso que requieran notificar usuarios
- Todas las fases del ciclo de vida (desarrollo, QA, producción)

Restricciones
-------------

Prohibiciones Absolutas
~~~~~~~~~~~~~~~~~~~~~~~

Servicios de Correo Electrónico
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PROHIBIDO bajo cualquier circunstancia:

- SMTP (Simple Mail Transfer Protocol)
- SendGrid
- Mailgun
- Amazon SES (Simple Email Service)
- Twilio SendGrid
- Mailchimp Transactional
- Postmark
- SparkPost
- Cualquier otro servicio de email

Librerías Prohibidas
^^^^^^^^^^^^^^^^^^^^

Librerías de email en código Python:

- ``smtplib`` (Python estándar)
- ``django.core.mail``
- ``email.mime`` (para construir emails)
- ``aiosmtplib`` (async SMTP)

Funcionalidades Prohibidas
^^^^^^^^^^^^^^^^^^^^^^^^^^

NO se permite:

- Envío de correos electrónicos
- Templates de email (.html, .txt para emails)
- Recuperación de contraseña por email
- Notificaciones por email
- Alertas por email
- Confirmaciones por email
- Reportes por email
- Invitaciones por email

Consecuencias de Violación
~~~~~~~~~~~~~~~~~~~~~~~~~~

Consecuencias de violación de esta restricción:

- Rechazo inmediato en code review
- Rollback de deployment si se detecta en producción
- Incidente de seguridad categoría Alta
- Re-trabajo completo del módulo afectado

Mecanismo Obligatorio
~~~~~~~~~~~~~~~~~~~~~

OBLIGATORIO: Buzón Interno (InternalMessage)

Todas las notificaciones se realizan mediante el modelo ``InternalMessage``, almacenado en base de datos y accesible desde la interfaz web.

Implementación
--------------

Recuperación de Contraseña sin Email
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En lugar de enviar emails para recuperación de contraseña, se usan preguntas de seguridad.

Modelo SecurityQuestion
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # api/apps/users/models.py

   from django.db import models
   from django.contrib.auth import get_user_model
   from django.utils import timezone
   import hashlib

   User = get_user_model()

   class SecurityQuestion(models.Model):
       """
       Preguntas de seguridad para recuperación de contraseña.

       CNST-001: NO se permite recuperación por email.
       """

       user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_questions')
       question = models.CharField(max_length=255)
       answer_hash = models.CharField(max_length=128)
       created_at = models.DateTimeField(auto_now_add=True)

       class Meta:
           db_table = 'security_questions'

       def set_answer(self, answer):
           """Hash de respuesta con salt del usuario."""
           salt = f"{self.user.id}_{self.question}"
           self.answer_hash = hashlib.sha256(f"{salt}_{answer}".encode()).hexdigest()

       def check_answer(self, answer):
           """Verificar respuesta."""
           salt = f"{self.user.id}_{self.question}"
           return self.answer_hash == hashlib.sha256(f"{salt}_{answer}".encode()).hexdigest()

Validación de Respuestas
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def validate_security_answers(user, answers):
       """
       Validar respuestas de seguridad del usuario.

       Args:
           user: Usuario que intenta recuperar contraseña
           answers: Lista de tuplas (question_id, answer)

       Returns:
           bool: True si todas las respuestas son correctas
       """
       questions = user.security_questions.all()

       if len(answers) < 3:
           return False

       for question_id, answer in answers:
           try:
               question = questions.get(id=question_id)
               if not question.check_answer(answer):
                   return False
           except SecurityQuestion.DoesNotExist:
               return False

       return True

Código INCORRECTO
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # ❌ PROHIBIDO - Envío de email
   from django.core.mail import send_mail

   def reset_password_email(user):
       send_mail(
           subject='Recuperar contraseña',
           message='Link: https://...',
           from_email='noreply@iact.com',
           recipient_list=[user.email],
       )

Sistema de Notificaciones Internas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modelo InternalMessage
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # api/apps/common/models.py

   from django.db import models
   from django.contrib.auth import get_user_model
   from django.utils import timezone

   User = get_user_model()

   class InternalMessage(models.Model):
       """
       Buzón interno de mensajes del sistema IACT.

       CNST-001: Reemplaza completamente el email.
       UC-037: Recibir Notificación Interna.
       """

       PRIORITY_CHOICES = [
           ('LOW', 'Baja'),
           ('NORMAL', 'Normal'),
           ('HIGH', 'Alta'),
           ('CRITICAL', 'Crítica'),
       ]

       recipient = models.ForeignKey(
           User,
           on_delete=models.CASCADE,
           related_name='messages_received'
       )

       sender = models.ForeignKey(
           User,
           on_delete=models.SET_NULL,
           null=True,
           blank=True,
           related_name='messages_sent'
       )

       subject = models.CharField(max_length=255)
       body = models.TextField()
       priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='NORMAL')

       is_read = models.BooleanField(default=False)
       read_at = models.DateTimeField(null=True, blank=True)

       is_archived = models.BooleanField(default=False)
       archived_at = models.DateTimeField(null=True, blank=True)

       created_at = models.DateTimeField(auto_now_add=True)

       class Meta:
           db_table = 'internal_messages'
           ordering = ['-created_at']
           indexes = [
               models.Index(fields=['recipient', '-created_at']),
               models.Index(fields=['recipient', 'is_read']),
           ]

       def __str__(self):
           return f"{self.subject} - {self.recipient.username}"

       def mark_as_read(self):
           """Marcar mensaje como leído."""
           if not self.is_read:
               self.is_read = True
               self.read_at = timezone.now()
               self.save()

       def archive(self):
           """Archivar mensaje."""
           if not self.is_archived:
               self.is_archived = True
               self.archived_at = timezone.now()
               self.save()

       @classmethod
       def unread_count(cls, user):
           """Contar mensajes no leídos."""
           return cls.objects.filter(
               recipient=user,
               is_read=False,
               is_archived=False
           ).count()

Función de Notificación
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # api/apps/common/notifications.py

   from apps.common.models import InternalMessage

   def notify(recipient, subject, body, sender=None, priority='NORMAL'):
       """
       Enviar notificación mediante buzón interno.

       CNST-001: NO se permite email bajo ninguna circunstancia.

       Args:
           recipient: Usuario destinatario
           subject: Asunto del mensaje
           body: Cuerpo del mensaje
           sender: Usuario remitente (opcional)
           priority: Prioridad (LOW, NORMAL, HIGH, CRITICAL)

       Returns:
           InternalMessage creado
       """
       message = InternalMessage.objects.create(
           recipient=recipient,
           sender=sender,
           subject=subject,
           body=body,
           priority=priority
       )

       return message

Notificar a Administradores
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def notify_admins(subject, body, priority='HIGH'):
       """
       Notificar a todos los administradores del sistema.

       CNST-001: Usa buzón interno, NO email.

       Args:
           subject: Asunto
           body: Contenido
           priority: Prioridad (por defecto HIGH)
       """
       from django.contrib.auth import get_user_model

       User = get_user_model()

       admins = User.objects.filter(is_staff=True, is_active=True)

       for admin in admins:
           notify(
               recipient=admin,
               subject=subject,
               body=body,
               priority=priority
           )

Notificar por Función RBAC
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def notify_by_function(function_code, subject, body, priority='NORMAL'):
       """
       Notificar a usuarios con una función específica (RBAC v5.1.1).

       CNST-001: Notificación por buzón interno.
       Compatible con RBAC v5.1.1: funciones atómicas.

       Args:
           function_code: Código de función atómica (ej: 'administra_sistema')
           subject: Asunto
           body: Contenido
           priority: Prioridad

       Example:
           notify_by_function(
               function_code='ve_reportes',
               subject='Nuevo reporte disponible',
               body='El reporte mensual está listo.'
           )
       """
       from apps.access.models import UserFunctionAssignment

       # Obtener usuarios con la función específica
       assignments = UserFunctionAssignment.objects.filter(
           function_code=function_code,
           is_active=True
       ).select_related('user')

       for assignment in assignments:
           if assignment.user.is_active:
               notify(
                   recipient=assignment.user,
                   subject=subject,
                   body=body,
                   priority=priority
               )

Ejemplo de Uso Completo
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Ejemplo: Notificar cuando se genera un reporte

   from apps.common.notifications import notify_by_function

   def on_report_generated(report):
       """
       Notificar a usuarios con capacidad de ver reportes.

       RBAC v5.1.1: función 've_reportes' (MOD_Reports - RPT-001)
       """
       notify_by_function(
           function_code='ve_reportes',
           subject=f'Reporte {report.name} generado',
           body=f'''
           El reporte {report.name} ha sido generado exitosamente.

           Período: {report.start_date} - {report.end_date}
           Registros: {report.record_count}

           Accede al sistema para visualizarlo.
           ''',
           priority='NORMAL'
       )

Integración con Casos de Uso
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UC-003: Recuperar Contraseña
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # api/apps/users/views.py

   def password_recovery(request):
       """
       Recuperación de contraseña con preguntas de seguridad.

       CNST-001: NO email. UC-003.
       """
       username = request.POST.get('username')
       answers = request.POST.get('answers')

       user = User.objects.get(username=username)

       if validate_security_answers(user, answers):
           # Generar contraseña temporal
           temp_password = generate_temp_password()
           user.set_password(temp_password)
           user.save()

           # Notificar por buzón interno
           notify(
               recipient=user,
               subject='Contraseña temporal generada',
               body=f'Tu contraseña temporal es: {temp_password}\n\nCámbiala al iniciar sesión.',
               priority='HIGH'
           )

           return {'success': True}

       return {'success': False, 'error': 'Respuestas incorrectas'}

UC-037: Recibir Notificación
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # api/apps/common/views.py

   class InternalMessageViewSet(viewsets.ModelViewSet):
       """
       API para gestión de mensajes internos.

       CNST-001: Buzón interno obligatorio.
       UC-037: Recibir Notificación.
       """

       serializer_class = InternalMessageSerializer
       permission_classes = [IsAuthenticated]

       def get_queryset(self):
           """Solo mensajes del usuario actual."""
           return InternalMessage.objects.filter(
               recipient=self.request.user,
               is_archived=False
           )

       @action(detail=True, methods=['post'])
       def mark_read(self, request, pk=None):
           """Marcar como leído."""
           message = self.get_object()
           message.mark_as_read()
           return Response({'status': 'read'})

       @action(detail=False, methods=['get'])
       def unread_count(self, request):
           """Contar no leídos."""
           count = InternalMessage.unread_count(request.user)
           return Response({'unread': count})

Validación Automatizada
~~~~~~~~~~~~~~~~~~~~~~~~

Script de Validación
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # scripts/validate_cnst_001.py

   import os
   import re
   import sys

   def validate_no_email_usage(project_dir):
       """
       Validar que no se use email en el código.

       CNST-001: Prohibición absoluta de SMTP.
       """
       violations = []

       # Patrones prohibidos
       patterns = [
           r'from django\.core\.mail import',
           r'import smtplib',
           r'send_mail\(',
           r'EmailMessage\(',
           r'@.*\.com',  # Posible email address
       ]

       for root, dirs, files in os.walk(project_dir):
           # Ignorar venv, node_modules, etc.
           dirs[:] = [d for d in dirs if d not in ['venv', 'node_modules', '.git']]

           for file in files:
               if file.endswith('.py'):
                   filepath = os.path.join(root, file)

                   with open(filepath, 'r', encoding='utf-8') as f:
                       content = f.read()

                       for pattern in patterns:
                           if re.search(pattern, content):
                               violations.append({
                                   'file': filepath,
                                   'pattern': pattern,
                               })

       return violations

   if __name__ == '__main__':
       violations = validate_no_email_usage('.')

       if violations:
           print("❌ CNST-001 VIOLATIONS FOUND:")
           for v in violations:
               print(f"  {v['file']}: {v['pattern']}")
           sys.exit(1)
       else:
           print("✅ CNST-001: No email usage detected")
           sys.exit(0)

Aprobaciones
------------

Este documento ha sido revisado y aprobado por:

- Arquitecto de Software
- Tech Lead
- Product Owner
- Cliente (Restricción de negocio)

Referencias
-----------

Casos de Uso Relacionados
~~~~~~~~~~~~~~~~~~~~~~~~~~

- UC-003: Recuperar Contraseña
- UC-037: Recibir Notificación Interna

Restricciones Relacionadas
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- CNST-004: Actualización de Datos mediante ETL (no real-time)

Modelo RBAC IACT
~~~~~~~~~~~~~~~~

- Modelo RBAC IACT v5.1.1 (44 funciones atómicas, 8 módulos)
- Función ``administra_sistema``: Gestión completa del sistema
- Función ``ve_reportes``: Visualización de reportes (MOD_Reports)
- MOD_Alerts: Módulo de alertas y notificaciones

Historial de Cambios
---------------------

.. list-table::
   :header-rows: 1
   :widths: 10 15 50 25

   * - Versión
     - Fecha
     - Cambios
     - Autor
   * - 1.0.0
     - 2025-12-17
     - Versión inicial
     - Equipo IACT
   * - 1.1.0
     - 2026-01-03
     - Actualización a RBAC v5.1.1. Función notify_by_function() con funciones atómicas
     - Equipo IACT