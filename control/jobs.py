"""In-memory orchestration for a transparent cause/process/effect demo."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4


class JobManager:
    """Runs a deterministic demo flow; it does not access external data."""

    def __init__(self) -> None:
        self._jobs: list[dict[str, object]] = []
        self._lock = Lock()

    def run_diagnostic(self) -> dict[str, object]:
        steps = [
            {"name": "Validar solicitud", "result": "Entrada válida; no se recibieron datos personales."},
            {"name": "Clasificar área", "result": "Control general (ejecución demostrativa)."},
            {"name": "Analizar causa y efecto", "result": "Sin una fuente conectada no se infieren hechos externos."},
            {"name": "Emitir informe", "result": "Flujo completado; conectar una fuente requiere configuración explícita."},
        ]
        job: dict[str, object] = {
            "id": str(uuid4()),
            "type": "diagnostic",
            "status": "completed",
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "steps": steps,
            "note": "Demostración local: no lee ni persiste información del usuario.",
        }
        with self._lock:
            self._jobs.insert(0, job)
            del self._jobs[20:]
        return job.copy()

    def list_jobs(self) -> list[dict[str, object]]:
        with self._lock:
            return [job.copy() for job in self._jobs]
