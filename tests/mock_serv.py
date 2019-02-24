import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler


class MockServerRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        with open('tests/resources/merge_requests.json', 'rb') as f:
            self.wfile.write(f.read())


with socketserver.TCPServer(('', PORT), MockServerRequestHandler) as httpd:
    print('serving at port', PORT)
    httpd.serve_forever()
