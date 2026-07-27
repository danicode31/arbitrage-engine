# Collectors

## MockCollector

Genera datos simulados.

## YahooCollector

Obtiene datos desde Yahoo Finance.

## IOLCollector

Obtiene datos desde InvertirOnline.

## PolygonCollector

Obtiene datos desde Polygon.io.

# Collectors

Los collectors obtienen cotizaciones y las normalizan como objetos `MarketQuote`.

## Contrato común

Todos implementan:

- `connect()`
- `disconnect()`
- `get_quotes()`
- `is_connected`

## BaseCollector

Clase abstracta que define el contrato común.

## MockCollector

Genera cotizaciones simuladas para desarrollo y pruebas.

Activos actuales:

- GGAL
- YPFD
- PAMP
- TXAR
- AL30

El collector exige conexión antes de entregar cotizaciones.