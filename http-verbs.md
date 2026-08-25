# Tarea: Construir un Servidor HTTP con WSGI en python que implemente Verbos HTTP (GET, POST, PATCH y DELETE)

## Objetivo

Construir tu propio servidor web en Python usando `wsgiref.simple_server`, tal como hicimos en clase con `server.py`, pero administrando una colección de recursos y demostrando que manejás con claridad los verbos HTTP **GET**, **POST**, **PATCH** y **DELETE**.

> En clase vimos un `GET /` que respondía `200 OK` y un `POST /users` que respondía `201 Created`. Ahora se pide utilizar los cuatro verbos principales `GET`, `POST`, `PATCH`, `DELETE`. 

## 1. Repaso de Conceptos: ¿qué diferencia hay entre los verbos?

Aquí la semántica de cada verbo:

| Verbo | Función | Es seguro? | Es idempotente? | Cuerpo (body)? | Respuestas típicas |
|---|---|---|---|---|---|
| **GET** | Leer/obtener recursos. **Nunca** debe modificar el estado del servidor. | Sí | Sí | No (solo consulta) | `200 OK`, `404 Not Found` |
| **POST** | Crear un **nuevo** recurso. Cada llamada genera un recurso distinto. | No | No | Sí (JSON) | `201 Created` |
| **PATCH** | Modificar **parcialmente** un recurso existente (solo los campos que mando). | No | Sí | Sí (JSON) | `200 OK`, `404 Not Found` |
| **DELETE** | Eliminar un recurso existente. | No | Sí | Normalmente no | `200 OK` / `204 No Content`, `404 Not Found` |

Recordá:

- **Idempotente**: ejecutarlo muchas veces produce el mismo resultado (ej.: borrar un recurso ya borrado sigue "estando borrado"). `POST` **no** es idempotente: dos `POST` iguales crean dos recursos.

## 2. Consigna

Implementá un servidor que administre una lista de **tareas** en memoria (una lista o diccionario en Python, no hace falta persistir en disco). El servidor debe soportar:

| Ruta y verbo | Comportamiento |
|---|---|
| `GET /tasks` | Devuelve todas las tareas. `200 OK` |
| `GET /tasks/{id}` | Devuelve una tarea por id. `200 OK` o `404 Not Found` si no existe |
| `POST /tasks` | Crea una nueva tarea con el cuerpo JSON recibido y le asigna un id. `201 Created` |
| `PATCH /tasks/{id}` | Modifica **solo los campos** enviados en el cuerpo JSON. `200 OK` o `404 Not Found` |
| `DELETE /tasks/{id}` | Elimina la tarea con ese id. `200 OK` / `204 No Content` o `404 Not Found` |
| Cualquier otra combinación | `404 Not Found` (o `405 Method Not Allowed` si la ruta existe pero el verbo no) |

### Requisitos obligatorios

1. **Sin frameworks.** Usá solo `wsgiref.simple_server`, como en el ejemplo de clase. Nada de Flask todavía (eso viene en talleres posteriores).
2. **Cuerpos en JSON.** Tanto para recibir (`json.loads`) como para responder (`json.dumps`), y siempre con el header `Content-Type: application/json`.
3. **Códigos de estado correctos.** Cada verbo tiene que devolver el código que corresponde según la tabla.
4. **`PATCH` parcial.** No debe reemplazar la tarea entera: si el cuerpo solo trae `{"done": true}`, solo se cambia `done` y el resto de los campos se conservan.

### Criterios de evaluación

- Se entiende y se aplica correctamente la **diferencia semántica entre los cuatro verbos** (no usar `GET` para crear ni `POST` para leer, etc.).
- La implementación funciona y responde con los códigos de estado correctos.
- `PATCH` es parcial (modifica solo lo enviado).
- El código es legible, ordenado y no repite lógica de forma innecesaria.
- Se entrega evidencia de prueba (puntos 3 y 4 siguientes).

## 3. Cómo probar (entrega la evidencia)

Levantá tu servidor y probá cada verbo. Tenés dos opciones:

**Automático (recomendado):** corré el script `demo-verbos-http.sh`, que ejecuta todos los `curl`, verifica los códigos de estado y el contenido de cada respuesta, y marca cada prueba con `PASS` o `FAIL`.

```bash
uv run python server.py     # terminal 1
./demo-verbos-http.sh       # terminal 2
```

Al final imprime un resumen y termina con código de error si alguna prueba falló. Guardá esa salida (por ejemplo en `evidencia.txt`) y entregala junto con el código.

**Manual:** también podés probar cada verbo a mano con `curl` como hicimos en clase:

```bash
# Ver todas las tareas (GET)
curl http://localhost:9292/tasks

# Crear una tarea (POST)
curl -X POST http://localhost:9292/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudiar HTTP", "done": false}'

# Ver una tarea por id (GET)
curl http://localhost:9292/tasks/1

# Modificar solo un campo (PATCH)
curl -X PATCH http://localhost:9292/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Eliminar una tarea (DELETE)
curl -X DELETE http://localhost:9292/tasks/1

# Caso de error: ver una tarea inexistente (GET → 404)
curl -i http://localhost:9292/tasks/999
```

Probalos en este orden y mostrá que después del `DELETE`, el `GET /tasks/1` devuelve `404`.

## 4. Entrega

- Un único archivo Python (p. ej. `server.py`) que se ejecute con `uv run python server.py` y quede escuchando en `http://localhost:9292`.
- **Extras:** en el README, una breve explicación con tus palabras de la diferencia entre `GET`, `POST`, `PATCH` y `DELETE`, y por qué `POST` no es idempotente

