```yml
created_at: 2026-05-06 19:39:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 1 — DISCOVER (research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
query_id: Q2
tier: 1 (oficial)
```

# Q2 — Bootstrap de Groups predefinidos via data migration

## Query ejecutado

```
Django data migration create permission groups bootstrap
```

`allowed_domains=["docs.djangoproject.com"]`

## Hallazgos verbatim (Tier 1)

### Patrón canónico — `RunPython` en data migration

> "RunPython is generally the operation you would use to create
> data migrations, run custom data updates and alterations, and
> anything else you need access to an ORM and/or Python code
> for."

### Workflow oficial Django para grupos predefinidos

1. **Crear migración vacía:**
   ```bash
   python manage.py makemigrations --empty yourapp \
       --name create_permission_groups
   ```

2. **Implementar función con RunPython:**
   ```python
   from django.db import migrations

   def create_groups(apps, schema_editor):
       Group = apps.get_model('auth', 'Group')
       Permission = apps.get_model('auth', 'Permission')

       group, created = Group.objects.get_or_create(name='Your Group Name')
       group.permissions.set(Permission.objects.filter(...))

   class Migration(migrations.Migration):
       dependencies = [
           ('yourapp', '0001_previous_migration'),
       ]
       operations = [
           migrations.RunPython(create_groups),
       ]
   ```

3. **Ejecutar:** `python manage.py migrate` corre la migración y
   crea los grupos automáticamente.

### Uso de `apps.get_model()` (importante)

> "The Permission model is rarely accessed directly... migrations
> que usan `apps.get_model('auth', 'Group')` aseguran que se
> obtiene la versión histórica del modelo en el punto de la
> migración, no la versión actual del código."

**Implicaciones para IACT:**

- El proyecto IACT puede bootstrap los 12 grupos AGR-001..012
  con una sola data migration usando `RunPython`.
- El management command `initialize_permissions` mencionado en
  `arquitectura-tecnica/rbac/modelo-rbac-iact/implementacion.rst`
  es **una alternativa** pero no la canónica per docs Django —
  Django prefiere migrations para datos seed.

## Sources

- [Migrations | Django documentation](https://docs.djangoproject.com/en/5.0/topics/migrations/)
- [Migration Operations | Django documentation](https://docs.djangoproject.com/en/5.0/ref/migration-operations/)
- [How to create database migrations | Django documentation](https://docs.djangoproject.com/en/4.2/howto/writing-migrations/)
- [How to provide initial data for models](https://docs.djangoproject.com/en/6.0/howto/initial-data/)

## Veredicto preliminar Q2

El patrón **canónico Django** para bootstrap de grupos
predefinidos es **data migration con `RunPython`**, no fixtures
ni management commands. Esto es compatible con `auth.Group`
nativo y con un modelo custom como `AccessGroup`.

IACT-docs declara `python manage.py initialize_permissions` como
mecanismo de bootstrap, pero docs Django sugiere que migrations
son la forma idiomatica.
