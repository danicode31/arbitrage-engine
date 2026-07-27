# Motor de Arbitraje

El Arbitrage Engine es el núcleo del proyecto.

Su responsabilidad es analizar cotizaciones provenientes de distintos mercados y detectar oportunidades de arbitraje.

Actualmente el motor implementa una estrategia denominada:

- CrossMarketArbitrageStrategy

## Flujo

```text
MarketQuotes

↓

Agrupar por símbolo

↓

Comparar mercados

↓

Comprar en menor ASK

↓

Vender en mayor BID

↓

Calcular spread

↓

Generar ArbitrageOpportunity
```

## Resultado

Cada oportunidad contiene:

- símbolo
- mercado comprador
- mercado vendedor
- precio de compra
- precio de venta
- spread bruto
- spread neto
- ganancia estimada
- fecha de detección

Actualmente el spread neto es igual al spread bruto.

En próximos sprints se incorporarán:

- comisiones
- impuestos
- costos de transferencia
- tipo de cambio
- ratios CEDEAR
- slippage
- profundidad del libro