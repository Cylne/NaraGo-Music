#!/usr/bin/env python3
"""
Rich Beats Proxy Server
- Serves static files (index.html, etc.)
- Proxies /api/* requests to https://richmusic.vercel.app
- Handles CORS automatically
"""
import http.server
import socketserver
import urllib.request
import json
import os
import threading

ORIGIN = "https://richmusic.vercel.app"
PORT = 8080
STATIC_DIR = "/root/richmusic"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "3600")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/"):
            self.handle_api()
        else:
            super().do_GET()

    def handle_api(self):
        target_url = ORIGIN + self.path
        req = urllib.request.Request(target_url, method="GET")
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read()
                self.send_response(resp.status)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", resp.headers.get("Content-Type", "application/json"))
                self.end_headers()
                self.wfile.write(content)
        except Exception as e:
            error_resp = json.dumps({"error": str(e)}).encode()
            self.send_response(500)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(error_resp)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

if __name__ == "__main__":
    os.chdir(STATIC_DIR)
    with socketserver.TCPServer(("0.0.0.0", PORT), ProxyHandler) as httpd:
        print(f"🚀 Rich Beats Proxy Server running on http://0.0.0.0:{PORT}")
        print(f"  • Static files: {STATIC_DIR}")
        print(f"  • API proxy: /api/* -> {ORIGIN}/api/*")
        httpd.serve_forever()
