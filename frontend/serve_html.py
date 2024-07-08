import http.server
import socketserver
import os

PORT = 5500
DIRECTORY = "./src"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'Index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

os.chdir(DIRECTORY)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    print("Go to http://localhost:5500")
    httpd.serve_forever()
