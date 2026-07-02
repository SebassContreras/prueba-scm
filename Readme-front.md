# PRUEBA TÉCNICA

### Hora inicio: 9:40 — Hora fin: 10:55

## Enfoque general

He intentado no instalar dependencias nuevas. Si esto fuera a producción, yo habría usado axios para tener más control de las peticiones a la API, y también TanStack Query para manejar caché, reintentos y estado de carga de una forma más eficiente.

También separé la lógica de la configuración de API para que no quede anclada a un módulo concreto. Así, si luego cambiamos de librería HTTP, el cambio se hace en un solo sitio.

## Estructura que usé

Organicé el frontend por responsabilidad:

- features: aquí va la lógica por módulo (auth e items), junto con sus types y services.
- pages: aquí están las pantallas (login e items), que actúan como punto de entrada de cada feature.
- api: cliente HTTP común y manejo de cabeceras/autorización.
- common: tipos compartidos (por ejemplo filtros y shape de errores).

Yo suelo trabajar así porque si mañana nacen más pantallas o más endpoints de un módulo, todo queda agrupado en su misma feature y es más fácil escalar.

## Cosas que sí están implementadas

- Autenticación por token con guardado en localStorage (access_token y refresh_token).
- En cada petición autenticada se manda el token en Authorization desde api/http.
- Si la API devuelve 401, se intenta refrescar el token automáticamente y se reintenta la petición.
- Si no se puede refrescar, se cierra sesión y la pantalla protegida deja de ser accesible.
- En App.vue el flujo está simple: si no hay sesión, se muestra login; si hay sesión, se muestra items.

## Sobre items y filtros

En items dejé búsqueda con filtros básicos (estado y warehouse_id) y actualización de estado por fila.

También hay manejo de mensajes de error para mostrar feedback al usuario, y protección para fechas inválidas para que no reviente la tabla.

## Diseño

No toqué diseño. Me enfoqué en lógica, estructura y flujo de autenticación.

## Qué mejoraría con más tiempo

- Añadir router y layout principal (menú/base) para escalar más páginas.
- Meter gestión de caché y reintentos con TanStack Query.
- Unificar manejo de errores con componentes reutilizables.
- Mejorar accesibilidad y estilos base.

Muchas gracias.
