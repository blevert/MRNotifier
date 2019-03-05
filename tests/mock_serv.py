import http.server

PORT = 8000


class MockServerRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        if 'merge_requests' in self.path:
            with open('tests/resources/merge_requests.json', 'rb') as f:
                self.wfile.write(f.read())
        elif 'award_emoji' in self.path:
            with open('tests/resources/award_emoji.json', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.wfile.write(b'READY')


with http.server.ThreadingHTTPServer(('', PORT), MockServerRequestHandler) as httpd:
    print('serving at port', PORT)
    httpd.serve_forever()
