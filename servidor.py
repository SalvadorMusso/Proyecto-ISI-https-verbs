from wsgiref.simple_server import make_server
import json

task = [{"id" : 1 , "tarea" : "comprar pan", "estado" : False} ,
        {"id" : 2 , "tarea" : "tirar la basura", "estado" : True}]

def aplicacion(enviaron, empezar_respuesta):
    method = enviaron.get('REQUEST_METHOD')
    path = enviaron.get('PATH_INFO')

    if method == 'GET' and path == '/tasks':
        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        response_body = json.dumps(task).encode('utf-8')

        empezar_respuesta(status, headers)
        return [response_body]

    if method == 'GET' and path.startswith('/tasks/'):
        partes = path.strip('/').split('/')
        if len(partes) == 2 and partes[1].isdigit():
            task_id = int(partes[1])
            encontrada = next((t for t in task if t["id"] == task_id), None)
            
            if encontrada:
                status = '200 OK'
                headers = [('Content-Type', 'application/json; charset=utf-8')]
                response_body = json.dumps(encontrada).encode('utf-8')
                empezar_respuesta(status, headers)
                return [response_body]
            else:
                status = '404 Not Found'
                headers = [('Content-Type', 'application/json; charset=utf-8')]
                response_body = json.dumps({"error": "Tarea no encontrada"}).encode('utf-8')
                empezar_respuesta(status, headers)
                return [response_body]

    status = '404 Not Found'
    headers = [('Content-Type', 'application/json; charset=utf-8')]
    response_body = json.dumps({"error": "Ruta no encontrada"}).encode('utf-8')

    empezar_respuesta(status, headers)
    return [response_body]


if __name__ == '__main__':
    with make_server('', 9292, aplicacion) as server:
        print(f"Servidor corriendo en http://localhost:{9292}/tasks")
        server.serve_forever()
