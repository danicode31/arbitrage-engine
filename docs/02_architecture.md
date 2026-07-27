# Arquitectura

El proyecto sigue una arquitectura por capas inspirada en Clean Architecture, donde cada componente tiene una única responsabilidad.

                  ArbitrageApplication
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
    Scheduler                           MetricsRegistry
        │
        ▼
 MarketPipeline
        │
        ▼
  QuoteService
        │
        ├───────────────┐
        │               │
        ▼               ▼
 Collector         Repository
        │               │
        └──────► DuckDB ◄──────┐
                               │
                           EventBus
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
 ArbitrageEventHandler                 MetricsEventHandler
            │
            ▼
   ArbitrageEngine
            │
            ▼
     Strategy Pattern

## Principios

- Responsabilidad única.
- Bajo acoplamiento.
- Alta cohesión.
- Inyección de dependencias.
- Componentes fácilmente testeables.
- Separación entre infraestructura y lógica de negocio.