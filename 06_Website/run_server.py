#!/usr/bin/env python3
"""
Simple HTTP server to test the Football Scout Tool locally
Run this script and open http://localhost:8000 in your browser
"""

import http.server
import socketserver
import os

PORT = 8080

# Change to the website directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"⚽ Football Scout Tool")
    print(f"Server running at http://localhost:{PORT}/")
    print("Press Ctrl+C to stop")
    print()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
