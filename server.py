from wsgiref.simple_server import make_server
import json

task = [{"id" : 1 , "tarea" : "comprar pan", "estado" : False} ,
        {"id" : 2 , "tarea" : "tirar la basura", "estado" : True}]

def leer_cuerpo(enviaron):
    try:
        tamaño = int(enviaron.get('CONTENT_LENGTH', 0))
    except (ValueError, TypeError):
        tamaño = 0

    if tamaño > 0:
        cuerpo_bytes = enviaron['wsgi.input'].read(tamaño)
        return json.loads(cuerpo_bytes.decode('utf-8'))
    return {}

def aplicacion(enviaron, empezar_respuesta):
    method = enviaron.get('REQUEST_METHOD')
    path = enviaron.get('PATH_INFO')

    if method == 'GET' and path == '/tasks':
        estado = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        cuerp_resp = json.dumps(task).encode('utf-8')

        empezar_respuesta(estado, headers)
        return [cuerp_resp]
    
    elif method == 'POST' and path == '/tasks':
        nuevo_item = leer_cuerpo(enviaron)
        siguiente_id = max([t["id"] for t in task], default=0) + 1 

        nuevo_item = {"id": siguiente_id, **nuevo_item}
        
        task.append(nuevo_item)

        estado = '201 Created'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        cuerp_resp = json.dumps(nuevo_item).encode('utf-8')
        empezar_respuesta(estado, headers)
        return [cuerp_resp]

    elif method == 'GET' and path.startswith('/tasks/'):
        partes = path.strip('/').split('/')
        if len(partes) == 2 and partes[1].isdigit():
            task_id = int(partes[1])
            encontrada = next((t for t in task if t["id"] == task_id), None)
            
            if encontrada:
                estado = '200 OK'
                headers = [('Content-Type', 'application/json; charset=utf-8')]
                cuerp_resp = json.dumps(encontrada).encode('utf-8')
                empezar_respuesta(estado, headers)
                return [cuerp_resp]
            else:
                estado = '404 Not Found'
                headers = [('Content-Type', 'application/json; charset=utf-8')]
                cuerp_resp = json.dumps({"error": "Tarea no encontrada"}).encode('utf-8')
                empezar_respuesta(estado, headers)
                return [cuerp_resp]

    elif method == 'PATCH' and path.startswith('/tasks/'):
        partes = path.strip('/').split('/')
        if len(partes) == 2 and partes[1].isdigit():
            task_id = int(partes[1])
            encontrada = next((t for t in task if t["id"] == task_id), None)
            
            if not encontrada:
                estado = '404 Not Found'
                headers = [('Content-Type', 'application/json; charset=utf-8')]
                cuerp_resp = json.dumps({"error": "Tarea no encontrada"}).encode('utf-8')
                empezar_respuesta(estado, headers)
                return [cuerp_resp]

            cambios = leer_cuerpo(enviaron)

            encontrada.update(cambios)
            encontrada["id"] = task_id 

            estado = '200 OK'
            headers = [('Content-Type', 'application/json; charset=utf-8')]
            cuerp_resp = json.dumps(encontrada).encode('utf-8')
            empezar_respuesta(estado, headers)
            return [cuerp_resp]

    elif method == 'DELETE' and path.startswith('/tasks/'):
        partes = path.strip('/').split('/')
        if len(partes) == 2 and partes[1].isdigit():
            task_id = int(partes[1])
            encontrada = next((t for t in task if t["id"] == task_id), None)

            if not encontrada:
                estado = '404 Not Found'
                headers = [('Content-Type', 'application/json; charset=utf-8')]
                cuerp_resp = json.dumps({"error": "Tarea no encontrada"}).encode('utf-8')
                empezar_respuesta(estado, headers)
                return [cuerp_resp]

            task.remove(encontrada)

            estado = '200 OK'
            headers = [('Content-Type', 'application/json; charset=utf-8')]
            cuerp_resp = json.dumps({
                "mensaje": f"Tarea con id {task_id} eliminada correctamente",
                "tarea": encontrada
            }).encode('utf-8')
            empezar_respuesta(estado, headers)
            return [cuerp_resp]
        
    estado = '404 Not Found'
    headers = [('Content-Type', 'application/json; charset=utf-8')]
    cuerp_resp = json.dumps({"error": "Ruta no encontrada"}).encode('utf-8')

    empezar_respuesta(estado, headers)
    return [cuerp_resp]


if __name__ == '__main__':
    with make_server('', 9292, aplicacion) as server:
        print(f"Servidor corriendo en http://localhost:{9292}/tasks")
        server.serve_forever()
