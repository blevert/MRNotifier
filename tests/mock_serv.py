import http.server

PORT = 8000


class MockServerRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        if 'award_emoji' in self.path:
            self._write_resource('award_emoji.json')
        elif 'merge_requests' in self.path:
            self._write_resource('merge_requests.json')
        else:
            self.wfile.write(b'READY')

    def _write_resource(self, resource):
        with open('tests/resources/' + resource, 'rb') as f:
            self.wfile.write(f.read())


with http.server.ThreadingHTTPServer(('', PORT), MockServerRequestHandler) as httpd:
    print('serving at port', PORT)
    httpd.serve_forever()
