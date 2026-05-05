.. _uc-adm-02-parte-06:

==========================================
Parte 6 — Requisitos no funcionales
==========================================

- Performance: CRUD ≤ 200 ms; reload
  catalog ≤ 3 s.
- Confiabilidad: ≥ 99.9%; operacion critica
  sobre el catalogo base del RBAC.
- Seguridad: solo AGR-009. Toda escritura
  auditada con alta criticidad (CNST-025).
- Trazabilidad: codename inmutable tras
  creacion; description/scope actualizables.
- Compatibilidad: desactivar no rompe
  asignaciones historicas (BR-009).
- Mantenibilidad: catalogo versionado con
  historial de activaciones/desactivaciones.
