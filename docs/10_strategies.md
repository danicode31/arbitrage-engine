# Estrategias

Todas las estrategias implementan el contrato BaseStrategy.

```python
detect(
    quotes: list[MarketQuote]
) -> list[ArbitrageOpportunity]
```

Cada estrategia debe ser completamente independiente.

## Estrategias implementadas

### CrossMarketArbitrageStrategy

Objetivo:

Buscar diferencias de precio del mismo activo entre distintos mercados.

Algoritmo:

1. Agrupar por símbolo.
2. Buscar el menor ASK.
3. Buscar el mayor BID.
4. Calcular spread.
5. Crear oportunidad.

## Estrategias futuras

### CedearStrategy

Comparar:

CEDEAR ↔ Acción USA

considerando

- ratio
- CCL

---

### BondStrategy

Bonos duales.

---

### OptionParityStrategy

Calls
Puts
Activo

---

### CryptoExchangeStrategy

Binance

Bybit

Kraken

OKX

---

### StatisticalArbitrage

Pairs Trading.

Cointegración.

Z-Score.