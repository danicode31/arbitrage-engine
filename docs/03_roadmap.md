# Roadmap

## Sprint 0 - Fundación

- [x] Repositorio GitHub
- [x] Rama `main`
- [x] Rama `develop`
- [x] Entorno virtual
- [x] Configuración inicial
- [x] Ruff
- [x] Black
- [x] MyPy
- [x] Pytest
- [x] Pre-commit

## Sprint 1 - Dominio

- [x] Configuración con Pydantic
- [x] Logger
- [x] Modelo `MarketQuote`
- [x] Validaciones de precios
- [x] Tests del modelo

## Sprint 2 - Ingesta y persistencia

- [x] `BaseCollector`
- [x] `MockCollector`
- [x] Estado de conexión
- [x] Cotizaciones simuladas
- [x] DuckDB
- [x] Tabla `market_quotes`
- [x] `MarketQuoteRepository`
- [x] Persistencia por lote
- [x] Tests de base de datos
- [x] Tests del repositorio

## Sprint 3 - Pipeline

- [ ] Crear `MarketPipeline`
- [ ] Separar lógica de `main.py`
- [ ] Ejecutar collector y persistencia
- [ ] Manejo centralizado de errores
- [ ] Métricas de ejecución

## Sprint 4

### Motor de arbitraje

- [x] ArbitrageOpportunity
- [x] ArbitrageEngine
- [x] BaseStrategy
- [x] CrossMarketArbitrageStrategy
- [x] Tests del motor
- [x] Tests de estrategia

Pendiente:

- [ ] Costos
- [ ] Comisiones
- [ ] Rentabilidad %
- [ ] Configuración por mercado
- [ ] Alertas