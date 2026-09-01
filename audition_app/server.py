import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from data_store import load_auditions, add_audition
from notifier import generate_daily_briefing_text, generate_kakaotalk_carousel_payload

PORT = 8080
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class AuditionHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/api/auditions":
            auditions = load_auditions()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(auditions, ensure_ascii=False).encode("utf-8"))
            return
            
        elif parsed.path == "/api/summary/daily":
            summary = generate_daily_briefing_text()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(summary.encode("utf-8"))
            return
            
        elif parsed.path == "/api/kakaotalk/carousel":
            payload = generate_kakaotalk_carousel_payload()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
            return

        # Serve static index.html or other static files
        if parsed.path == "/" or parsed.path == "/index.html":
            file_path = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        return super().do_GET()

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), AuditionHandler)
    print(f"Audition App server running on http://localhost:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
