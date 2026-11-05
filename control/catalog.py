"""Catalog of areas visible in the control panel.

Keep this metadata free of user records and credentials. Each module can later
be backed by an independently tested service or adapter.
"""

MODULES = [
    {"id": "mobile", "name": "Aplicaciones móviles", "status": "reference", "description": "Estructura multiplataforma; referencia NFC para distinguir interfaz común y código nativo."},
    {"id": "backend", "name": "Backend y API", "status": "foundation", "description": "Rutas, validación de entradas, servicios y respuestas observables."},
    {"id": "data", "name": "Datos externos", "status": "disconnected", "description": "Punto de conexión futuro. No se guarda ni se crea aquí la base personal."},
    {"id": "ai-rag", "name": "IA y recuperación (RAG)", "status": "reference", "description": "Flujos de recuperación/generación y evaluación; referencia de interfaces intercambiables."},
    {"id": "cloud", "name": "Cloud e infraestructura", "status": "planned", "description": "Pendiente: despliegue, configuración, observabilidad y recuperación ante fallos."},
    {"id": "security", "name": "Seguridad y privacidad", "status": "planned", "description": "Pendiente: identidad, roles, permisos mínimos, auditoría y política de datos."},
]


def get_modules() -> list[dict[str, str]]:
    """Return a copy so callers cannot mutate the canonical catalog."""
    return [module.copy() for module in MODULES]
