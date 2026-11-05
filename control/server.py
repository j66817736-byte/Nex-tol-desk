"""Small, dependency-free local HTTP server for the Nex-tol Desk panel."""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from control.catalog import get_modules
from control.jobs import JobManager

ROOT = Path(__file__).resolve().parent.parent
WEB_ROOT = ROOT / "web"
JOBS = JobManager()


class ControlHandler(BaseHTTPRequestHandler):
    server_version = "NexTolDesk/0.1"

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, value: object) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        path = urlparse(self.path).path
        if path == "/api/health":
            return self._json(200, {"status": "ok", "service": "nex-tol-desk", "storage": "memory-only"})
        if path == "/api/modules":
            return self._json(200, {"modules": get_modules()})
        if path == "/api/jobs":
            return self._json(200, {"jobs": JOBS.list_jobs()})
        if path == "/" or path == "/index.html":
            return self._static("index.html")
        if path in ("/app.js", "/styles.css"):
            return self._static(path.lstrip("/"))
        return self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if urlparse(self.path).path != "/api/jobs":
            return self._json(404, {"error": "not_found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 1024:
                return self._json(413, {"error": "request_too_large"})
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "invalid_json"})
        if not isinstance(payload, dict) or payload.get("type", "diagnostic") != "diagnostic":
            return self._json(400, {"error": "unsupported_job_type"})
        return self._json(201, {"job": JOBS.run_diagnostic()})

    def _static(self, filename: str) -> None:
        path = (WEB_ROOT / filename).resolve()
        if WEB_ROOT.resolve() not in path.parents or not path.is_file():
            return self._json(404, {"error": "not_found"})
        content_type = "text/javascript; charset=utf-8" if path.suffix == ".js" else "text/css; charset=utf-8" if path.suffix == ".css" else "text/html; charset=utf-8"
        self._send(200, path.read_bytes(), content_type)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), ControlHandler)
    print(f"Nex-tol Desk disponible en http://{host}:{port} (Ctrl+C para detener)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando Nex-tol Desk...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
