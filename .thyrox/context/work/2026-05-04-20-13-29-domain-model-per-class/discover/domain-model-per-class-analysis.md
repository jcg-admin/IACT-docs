```yml
created_at: 2026-05-04 20:13:29
project: THYROX
work_package: 2026-05-04-20-13-29-domain-model-per-class
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Domain Model per-class — Análisis DISCOVER

## Solicitud del ejecutor

`source/arquitectura-tecnica/modulos/user-identity/diagramas/clases-modulo-identidad.rst`
contiene 3 clases (`User`, `Session`, `AuditEvent`) en un único diagrama combinado.
El ejecutor señaló que cada clase debería tener su propio archivo en
`source/arquitectura-tecnica/domain-model/`.

## Hallazgo principal (PROVEN)

**Los 3 archivos ya existen.** `domain-model/` tiene 27 archivos (1 por clase,
26 clases + 1 overview), organizados en 8 bounded contexts. Los 3 afectados:

| Clase | Archivo | Versión | BC |
|-------|---------|---------|-----|
| User | `domain-model/user.rst` | 1.1.0 | Auth |
| Session | `domain-model/session.rst` | 1.0.0 | Auth |
| AuditEvent | `domain-model/audit-event.rst` | 1.0.0 | Audit |

**Archivos a crear: 0.**

## Diferencias entre la fuente actual y domain-model (PROVEN)

### User — clases-modulo-identidad.rst vs domain-model/user.rst

| Aspecto | clases-modulo-identidad | domain-model/user.rst |
|---------|------------------------|-----------------------|
| Atributos | 6 (sin full_name, primary_access_group_id) | 8 (completo) |
| Métodos | 3 (create, deactivate, modify) | 5 (+view, +recover_password) |
| Notas CNST | Ninguna | CNST-002, CNST-003 en Session |
| Relaciones | User→Session, User→AuditEvent | User→Session, User→InternalMailbox |
| Formato | `+attr: Type` (sin espacios) | `+ attr : Type` (con espacios) |

### Session — diferencias

| Aspecto | clases-modulo-identidad | domain-model/session.rst |
|---------|------------------------|-----------------------|
| Atributos | 5 (sin last_activity_at, client_info) | 7 (completo) |
| Métodos | 2 (open, close) | 4 (+close_all, +view_own_sessions) |
| Permisos | Ninguno | Stereotipos `<<admin: ...>>` en métodos |

### AuditEvent — diferencias

| Aspecto | clases-modulo-identidad | domain-model/audit-event.rst |
|---------|------------------------|-----------------------|
| Atributos | 4 (sin actor_user_id, target_entity_*) | 7 (completo) |
| EventType enum | No presente | 10 valores completos |
| Métodos | 2 (record, search) | 5 (+view, +export, +generate_compliance_report) |
| Permisos | Ninguno | Stereotipos de permisos en métodos |

## Valor único de clases-modulo-identidad.rst (INFERRED)

El archivo tiene valor arquitectónico que los archivos individuales NO replican:

1. **Diagrama de relaciones inter-clase**: muestra `User "1" *-- "0..*" Session`
   y `User "1" --> "0..*" AuditEvent : genera` en un solo diagrama. Ningún archivo
   individual de domain-model muestra la relación User→AuditEvent.

2. **Scope de módulo**: enmarcado bajo `modulos/user-identity/` — perspectiva
   de implementación del módulo, no del dominio global.

## Gap: sin cross-references

`clases-modulo-identidad.rst` no tiene `.. seealso::` apuntando a los archivos
canónicos de `domain-model/`. Un lector que lee el diagrama del módulo no sabe
que `domain-model/user.rst` es la fuente de verdad.

## Decisión recomendada

| Opción | Descripción | Recomendación |
|--------|-------------|---------------|
| A | Eliminar `clases-modulo-identidad.rst` y reemplazar con referencias | ❌ Pierde el diagrama de relaciones inter-clase único |
| B | Actualizar el diagrama en `clases-modulo-identidad.rst` con los atributos canónicos + agregar seealso | ✅ Mantiene valor, sincroniza con domain-model |
| C | Mantener tal cual, solo agregar seealso | ⚠ Deja atributos desactualizados vs domain-model |

**Opción B recomendada**: actualizar el diagrama combinado con los atributos
completos de domain-model (que son la fuente canónica) + agregar `seealso`
a los 3 archivos domain-model. El diagrama combinado sigue siendo válido como
vista de módulo.

## Inventario de cambios (Opción B)

### clases-modulo-identidad.rst

1. Actualizar diagrama `@startuml`:
   - `User`: +full_name, +primary_access_group_id, +view(), +recover_password()
   - `Session`: +last_activity_at, +client_info, +close_all(), +view_own_sessions()
   - `AuditEvent`: +actor_user_id, +target_entity_type, +target_entity_id, enum EventType completo, +view(), +export(), +generate_compliance_report()
   - Agregar `InternalMailbox` con su relación a User
2. Agregar sección `.. seealso::` con los 3 archivos canónicos:
   ```
   :doc:`/arquitectura-tecnica/domain-model/user`
   :doc:`/arquitectura-tecnica/domain-model/session`
   :doc:`/arquitectura-tecnica/domain-model/audit-event`
   ```
3. Actualizar `:version:` en meta de 1.0.0 → 1.1.0

### domain-model/*.rst — sin cambios

Los archivos individuales son la fuente canónica — ya tienen el contenido
correcto. No se modifican.

## Conclusión

**0 archivos nuevos a crear.** El trabajo es:
- 1 archivo a actualizar: `clases-modulo-identidad.rst`
- Sincronizar su diagrama con los atributos canónicos de domain-model
- Agregar cross-references

¿Aprobás la Opción B?
