```yml
created_at: 2026-05-06 19:45:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 1 — DISCOVER (research)
author: NestorMonroy
status: Aprobado
version: 1.0.0
query_id: Q7
tier: 2 (paquetes y comunidad — Django no tiene SoD nativo)
```

# Q7 — RBAC con Separation of Duties (SoD) en Django

## Query ejecutado

```
Django RBAC separation of duties SoD implementation pattern
```

## Hallazgos verbatim

### Django **no provee SoD nativo**

Django auth (Group + Permission) provee únicamente la unión de
permisos. No hay enforcement built-in de constraints "el usuario
no puede tener simultáneamente perm A y perm B".

### Paquetes terceros documentados

**`django-rbac` (PyPI):**

> "RBAC enables the conditions for the implementation of what is
> called the Separation of Duties (SoD), so typically applications
> or projects using django-rbac will set mechanisms to delegate
> creating new permissions to owners."

`django-rbac` provee mecanismo de delegation pero el enforcement
SoD sigue siendo responsabilidad de la aplicación.

**`django-prbac` (Dimagi):**

GitHub: https://github.com/dimagi/django-prbac — implementación
parametrizada de RBAC con soporte para reglas más complejas.

### Fundamento teórico (Purdue paper)

> "Separation of Duty (SoD) is widely considered to be a
> fundamental principle in computer security, and a Static SoD
> (SSoD) policy states that in order to have all permissions
> necessary to complete a sensitive task, the cooperation of at
> least a certain number of users is required."

> "In RBAC, permissions are associated with roles, and users are
> granted membership in appropriate roles, thereby acquiring the
> roles' permissions, and **RBAC uses mutual exclusion
> constraints to implement SoD policies**."

### Implementación canónica en Django (sin paquete tercero)

> "In Django, you can implement RBAC using the built-in Group
> model and Permission system, and by creating groups with
> predefined permissions and assigning users to these groups,
> you can easily control access to different parts of your
> application."

Para SoD: el equipo debe implementar custom validation:

1. Modelo `SeparationRule` con par de Groups (o sets de
   Permissions) mutuamente exclusivos.
2. Signal `pre_save` o validación en form/serializer que
   verifica antes de asignar Group a User: "¿este Group
   conflicta con algún Group ya asignado?".
3. Custom backend opcional que rechaza assignments
   conflictivos.

## Veredicto preliminar Q7

IACT-docs implementa **SoD via modelo `FunctionSeparationRule`**
con 3 reglas (SOD-001/002/003). Esto **NO es nativo Django** y
**NO existe paquete tercero canónico ampliamente adoptado** —
es invención justificada del proyecto.

**El patrón IACT (FunctionSeparationRule) está bien fundamentado
teóricamente** (paper Purdue, NIST RBAC). Es legitimo y
necesario si el dominio requiere SoD.

**Recomendación:** mantener el modelo `FunctionSeparationRule`
con justificación explícita en ADR (no es Django idiomatic
porque Django no provee SoD; este es un dominio donde IACT debe
ser custom).

## Sources

- [django-rbac · PyPI](https://pypi.org/project/django-rbac/)
- [Django RBAC: Full Implementation Guide (Permit.io)](https://www.permit.io/blog/how-to-implement-role-based-access-control-rbac-into-a-django-application)
- [On Mutually-Exclusive Roles and Separation of Duty (Purdue)](https://www.cs.purdue.edu/homes/ninghui/papers/sod-j.pdf)
- [django-prbac on GitHub (Dimagi)](https://github.com/dimagi/django-prbac)
- [Django-DRF-Custom-Roles-and-Permissions-RBAC (boxabhi)](https://github.com/boxabhi/Django-DRF-Custom-Roles-and-Permissions-Role-Based-Access-Control-RBAC-with-Django-Rest-Framework)
