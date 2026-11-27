import http.server,functools
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self,p):
        if p.startswith('/_r/'): return '/home/claude/reels/'+p[4:].split('?')[0]
        return super().translate_path(p)
    def end_headers(self): self.send_header('Cache-Control','no-store');super().end_headers()
    def log_message(self,*a):pass
http.server.ThreadingHTTPServer(('127.0.0.1',8772),functools.partial(H,directory='/home/claude/banderin/site')).serve_forever()
