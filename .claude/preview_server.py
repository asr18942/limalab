import sys
import http.server
import socketserver
import mimetypes

BASE = "/Users/andreasofia/Documents/Lima Lab Website"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/":
            p = "/index.html"
        fp = BASE + p
        try:
            f = open(fp, "rb")
            data = f.read()
            f.close()
        except Exception as e:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(str(e).encode())
            return
        ctype = mimetypes.guess_type(fp)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


socketserver.TCPServer.allow_reuse_address = True
socketserver.TCPServer(("", PORT), Handler).serve_forever()
