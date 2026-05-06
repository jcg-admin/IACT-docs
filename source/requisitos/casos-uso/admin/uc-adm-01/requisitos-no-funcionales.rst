.. _uc-adm-01-parte-06:

==========================================
Parte 6 — Requisitos no funcionales
==========================================

- Performance: CRUD ≤ 200 ms; reload
  enforcement ≤ 2 s.
- Confiabilidad: ≥ 99.9%; operacion critica
  de configuracion del modelo RBAC.
- Seguridad: solo AGR-010. Toda operacion
  auditada con alta criticidad.
- Auditabilidad: P-39 audit reforzado;
  immutable append-only en AuditEvent.
- Consistencia: EnforcementEngine debe
  recargar antes de aceptar nuevas asignaciones.
- Trazabilidad: cada SoDRule tiene version
  e historial de cambios.
