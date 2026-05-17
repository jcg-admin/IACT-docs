```yml
project: IACT-docs
work_package: 2026-05-05-21-56-47-functional-decomposition-antipattern-audit
created_at: 2026-05-05 21:56:47
updated_at: 2026-05-05 21:56:47
current_phase: Phase 1 — DISCOVER
author: NestorMonroy
```

# Risk Register — Functional Decomposition Antipattern Audit

| ID | Riesgo | Prob | Impacto | Estado | Mitigacion | Owner |
|----|--------|------|---------|--------|------------|-------|
| R-01 | Falsos positivos por sufijos sospechosos (Validator, Generator, Resolver) que son patterns legitimos | A | M | Identificado | Aplicar C-5 (declara ser pattern) antes de C-1 (heuristica nombre). Si declara pattern y respeta spec, es OK. | Claude |
| R-02 | Antipatron tiene matices culturales (ingles vs espanol) — Brown habla de codigo, no de docs | M | B | Identificado | Adaptar heuristica a IACT: nombres ingles para identifiers tecnicos (STD-008), espanol para descripciones | Claude |
| R-03 | Audit puede revelar que muchos archivos del predecesor caen en antipatron | M | A | Identificado | Documentar hallazgo honesto. NO esconder. WP separado de remediacion. | NestorMonroy |
| R-04 | William Brown (1998) — algunas heuristicas estan datadas (e.g. static excessive era marker en Java de los 90s) | M | M | Identificado | Adaptar al contexto Python/Django moderno donde dataclasses + utility modules son legitimos | Claude |
| R-05 | C-5 (declara ser pattern) puede ser circular: archivos auto-declaran como Repository pero realmente son single-method functions | M | A | Identificado | Verificar que cumplan SPEC del pattern: Repository requiere ≥3 metodos CRUD/finder; Strategy requiere interfaz polimorfica; Service requiere ≥2 operaciones de dominio | Claude |
| R-06 | Audit subjetivo: dos auditores podrian discrepar en mismo archivo | M | M | Identificado | Documentar evidencia textual citando lineas del PlantUML. Veredicto reproducible. | Claude |
| R-07 | Profundidad ambigua: ¿C-2 single-method aplica solo a clases o tambien a metodos? | B | B | Identificado | Definir en SP-01 con ejecutor. Default: solo clases. | NestorMonroy |
| R-08 | Sin ground truth definitivo. Brown no pone umbrales numericos exactos | A | M | Aceptado | Documentar la interpretacion adoptada como parte del audit. Reproducible para auditorias futuras. | Claude |
| R-09 | El antipatron tipicamente se detecta en CODIGO no en DOCS. Auditar diagrams es indirecto | A | M | Aceptado | Audit de diagramas es la mejor proxy disponible. Si el codigo del backend esta disponible despues, segundo audit. | Claude |
| R-10 | Auditor (Claude) tiene sesgo: produjo los 16 nuevos en WP previo. Audit no es independiente | A | M | Identificado | Aplicar criterios objetivos C-1..C-5 sin revisar autoria. Si el resultado es "todo OK", revisar especialmente para confirmar no es self-validation | Claude / NestorMonroy |

## Notas

- **R-10 es critico**: si el mismo auditor audita su propio trabajo del WP
  predecesor, hay sesgo. Mitigacion: aplicar criterios sin lookups de autor;
  veredicto debe basarse SOLO en lo que esta en el archivo.
- **R-01 + R-05** se mitigan juntos: el sufijo (-Repo, -Validator) sugiere
  pattern, pero hay que verificar que el archivo realmente cumpla la spec
  del pattern declarado.
- **R-03 es politicamente sensitivo**: el audit puede aceptar hallazgos que
  son uncomfortable (e.g. "AuthorizationGuard solo tiene un metodo check()").
  Mitigacion: el audit es ETAPA 1; remediacion es WP separado.
