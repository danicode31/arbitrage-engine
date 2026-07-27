# Arquitectura

El proyecto sigue una arquitectura por capas inspirada en Clean Architecture, donde cada componente tiene una única responsabilidad.

```text
                    +----------------------+
                    |    Collectors        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   MarketPipeline     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Repositories       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      DuckDB          |
                    +----------------------+

                               |

                    +----------------------+
                    | Arbitrage Engine     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |     Strategies       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Opportunities        |
                    +----------------------+
```

## Principios

- Responsabilidad única.
- Bajo acoplamiento.
- Alta cohesión.
- Inyección de dependencias.
- Componentes fácilmente testeables.
- Separación entre infraestructura y lógica de negocio.