"""HTTP boundary for Astra Cloud; no external web framework required."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .service import AstraCloudService


def make_handler(service: AstraCloudService):
    class Handler(BaseHTTPRequestHandler):
        def _json(self, status: int, payload: dict) -> None:
            raw = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_POST(self):  # noqa: N802
            if self.path != "/v1/tasks":
                self._json(404, {"error": "not_found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                task = json.loads(self.rfile.read(length).decode("utf-8"))
                record = service.submit(task)
            except ValueError as exc:
                self._json(400, {"error": str(exc)})
                return
            except Exception:
                self._json(500, {"error": "internal_error"})
                return
            self._json(202, _public(record))

        def do_GET(self):  # noqa: N802
            prefix = "/v1/tasks/"
            if not self.path.startswith(prefix):
                self._json(404, {"error": "not_found"})
                return
            record = service.get(self.path[len(prefix):])
            if record is None:
                self._json(404, {"error": "task_not_found"})
                return
            self._json(200, _public(record))

        def log_message(self, *_args):
            return

    return Handler


def serve(service: AstraCloudService, host: str = "127.0.0.1", port: int = 8787) -> None:
    ThreadingHTTPServer((host, port), make_handler(service)).serve_forever()


def _public(record) -> dict:
    return {
        "task_id": record.task_id, "request_id": record.request_id, "state": record.state.value,
        "agent_id": record.agent_id, "output": record.output, "error_code": record.error_code,
        "artifacts": list(record.artifacts), "audit_refs": list(record.audit_refs),
    }
