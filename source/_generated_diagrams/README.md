# _generated_diagrams — pre-rendered PlantUML cache

SVGs pre-renderizados de los `@startuml..@enduml` del proyecto.
Generados por `scripts/prerender-plantuml.py`.

## Convención de nombres

`{sha256_16_hex}.svg` donde el hash =
`sha256(plantuml-styles.puml + "\n" + normalized_uml_block)[:16]`.

## NO editar manualmente

Los SVGs se generan idempotentemente por el script. Editarlos
manualmente causa drift con el RST source.

## Regenerar

```bash
python3 scripts/prerender-plantuml.py
```

## Cuándo invalidar

- Cambia `source/_static/plantuml-styles.puml` → todos los hashes
  cambian → re-render completo.
- Cambia un `@startuml..@enduml` block → su hash cambia → script
  renderiza el nuevo, el antiguo queda como huérfano (limpiar con
  `prerender-plantuml.py --gc`, futuro).
