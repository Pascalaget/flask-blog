from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

#local sever for images and movies
def M(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    web_dir = os.path.join(os.path.dirname(__file__), 'C:')
    os.chdir(web_dir)
    server_address = ('127.0.0.1', 8000)
    httpd = server_class(server_address, handler_class)
    print(server_address)
    httpd.serve_forever()
