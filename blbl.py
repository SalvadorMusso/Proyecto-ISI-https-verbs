from wsgiref.simple_server import make_server

def app(environ, start_response):
    status = "200 OK"
    headers = [("Content-Type","text/plain")]
    start_response(status,headers)
    return[b"Hola"]

with make_server("",9292,app) as server:
    print("Listening on http://localhost:9292")
    server.serve_forever()