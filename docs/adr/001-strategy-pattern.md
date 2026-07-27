# ADR-001

## Contexto

El motor de arbitraje deberá soportar múltiples algoritmos.

No es conveniente acoplar toda la lógica a una única clase.

## Decisión

Se adopta el patrón Strategy.

Cada algoritmo implementará BaseStrategy.

## Consecuencias

Ventajas

- Fácil agregar estrategias.
- Tests independientes.
- Bajo acoplamiento.
- Escalable.

Desventajas

- Mayor cantidad de clases.
- Más estructura inicial.