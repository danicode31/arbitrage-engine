# Roadmap

## Sprint 0 - Fundación

✅ Repositorio GitHub
✅ Rama `main`
✅ Rama `develop`
✅ Entorno virtual
✅ Configuración inicial
✅ Ruff
✅ Black
✅ MyPy
✅ Pytest
✅ Pre-commit

## Sprint 1 - Dominio

✅ Configuración con Pydantic
✅ Logger
✅ Modelo `MarketQuote`
✅ Validaciones de precios
✅ Tests del modelo

## Sprint 2 - Ingesta y persistencia

✅ `BaseCollector`
✅ `MockCollector`
✅ Estado de conexión
✅ Cotizaciones simuladas
✅ DuckDB
✅ Tabla `market_quotes`
✅ `MarketQuoteRepository`
✅ Persistencia por lote
✅ Tests de base de datos
✅ Tests del repositorio

## Sprint 3 - Pipeline

✅ Crear `MarketPipeline`
✅ Separar lógica de `main.py`
✅ Ejecutar collector y persistencia
✅ Manejo centralizado de errores
✅ Métricas de ejecución

## Sprint 4

### Motor de arbitraje

✅ ArbitrageOpportunity
✅ ArbitrageEngine
✅ BaseStrategy
✅ CrossMarketArbitrageStrategy
✅ Tests del motor
✅ Tests de estrategia

## Sprint 5

### Se introdujo el servicio QuoteService como responsable de centralizar
✅ Conexión al collector
✅ Obtención de cotizaciones
✅ Persistencia en el repositorio
✅ Almacenamiento del último snapshot
✅ Publicación de eventos del dominio

### EventBus
✅ publicación de eventos del dominio
✅ registro de múltiples suscriptores
✅ bajo acoplamiento entre componentes
✅ arquitectura preparada para futuros consumidores

## Sprint 6

✅ Arquitectura en capas.
✅ Repository Pattern.
✅ Collector Pattern.
✅ Strategy Pattern.
✅ Event-Driven Architecture.
✅ Dependency Injection.
✅ Composition Root.
✅ Metrics Registry.
✅ Scheduler desacoplado.
✅ QuoteService como fachada del dominio.
✅ Cobertura de pruebas para los componentes principales.
✅ Base preparada para integrar proveedores reales de datos de mercado.

## Sprint 7
Performance Metrics

## Sprint 8
Real Collector

## Sprint 9
Cost Engine

## Sprint 10
Alerts

## Sprint 11
REST API

## Sprint 12
Dashboard

## Sprint 13
Backtesting

## Sprint 14
Portfolio Optimizer