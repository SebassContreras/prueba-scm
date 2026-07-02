# PRUEBA TÉCNICA

### Hora inicio: 21:30 — Hora fin: 23:00

## Inicio

Es verdad que empecé tal vez a las 21:00 a descargar el código.
En empezar realmente con el desarrollo creo que empecé a las 21:30.

## Refactor

Una de las decisiones antes de empezar a implementar la lógica especificada en la prueba fue refactorizar las vistas.
Sé que no es algo muy relevante, pero vengo de Django y las cosas se hacen un poco distintas.
Por eso, para ubicarme mejor en los puntos a atacar, organicé la app para entender el punto de entrada y cómo funcionan los endpoints.

## Separación por carpetas

Parte de la refactorización fue entender qué capa se involucra y a cuál no debía prestarle atención.
Primero hice una carpeta de servicios y otra de rutas (de hecho, `schemas.py` debería estar en una carpeta, y `models.py` también).
Decidí no hacerlo por razones de tiempo.

## Decisiones de diseño

Hice el schema correspondiente de esta manera porque cubre todas las necesidades de filtros posibles, tanto si solo agregamos uno como si encadenamos más. Además, al agregar la posibilidad de `values`, añadimos la capa de filtrar por muchos a la vez.

En `apply_filters`, cambiamos el simple string —que era la principal vulnerabilidad— a una lista tipada de `Filter`. Esto hace que `apply_filters` pueda ser reutilizada en otros endpoints.

Tener todo con Pydantic permite tipar la estructura para refinar los datos que entran, y que si llega a llegar algo que no debería, dé error.

**Decisión de `operators` como diccionario y lambda:** esto hace que podamos comparar sus keys fácilmente y dar error si no es válida. También nos permite añadir fácilmente cualquier otro operador o removerlo sin tener que tocar lógica extra.

Cambié cosas de `apply_filters` porque me faltaron añadir validaciones. Entre ellas, qué tipo de operador acepta qué tipo de dato, para no hacer `operador in` con `value: "algo"` en lugar de `values: [1, 2, 3]`. No sé si es necesario, pero mientras escribía me surgieron estas dudas.

El máximo de filtros lo decidí según el máximo de campos en el modelo. Pero escribiendo esto también me doy cuenta de que puedo llegar a necesitar más, porque puedo repetir operadores como `>` y `<` para agregar rangos de fechas.

El máximo de rows es complicado de definir. Decidí 500 por decir algo, pero en cambio yo intentaría aplicar paginación y limitar a 50 registros únicamente, y hacer auto-fetch con el scroll.

Creo que no me dejo nada. ¡Muchas gracias!
