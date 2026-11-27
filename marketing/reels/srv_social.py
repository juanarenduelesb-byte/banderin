import http.server,functools
# Igual que srv.py, pero /vendor/supabase.js devuelve el Supabase de demostración (datos de ejemplo) para grabar Social.
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self,p):
        q=p.split('?')[0]
        if q.startswith('/_r/'): return '/home/claude/reels/'+q[4:]
        if q=='/vendor/supabase.js': return '/home/claude/reels/demosb.js'
        return super().translate_path(p)
    def end_headers(self): self.send_header('Cache-Control','no-store');super().end_headers()
    def log_message(self,*a):pass
http.server.ThreadingHTTPServer(('127.0.0.1',8772),functools.partial(H,directory='/home/claude/banderin/site')).serve_forever()
