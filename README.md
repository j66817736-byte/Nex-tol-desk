# Nex-tol Desk

Panel modular de control para observar áreas, ejecutar flujos de diagnóstico y explicar resultados mediante causa, proceso y efecto. La lógica de aplicación vive aquí; la base de datos personal se mantiene externa y no se incluye en este repositorio.

## Estado

Primera base funcional: servidor local en Python estándar, catálogo de módulos y un flujo demostrativo de diagnóstico. Los trabajos de esta versión se guardan solo en memoria y desaparecen al apagar el servidor. No conecta ni modifica bases de datos reales.

## Ejecutar

Requiere Python 3.10 o posterior; no necesita instalar dependencias.

```bash
python -m control.server
```

Abre <http://127.0.0.1:8000>. Para cambiar el puerto:

```bash
PORT=8080 python -m control.server
```

El servidor escucha solo en `127.0.0.1` por defecto. No lo expongas a internet sin autenticación, autorización, HTTPS y una revisión de seguridad.

## Qué incluye

- Panel web adaptable con estado del control y catálogo de módulos.
- API JSON: `GET /api/health`, `GET /api/modules`, `GET /api/jobs` y `POST /api/jobs`.
- Flujo de diagnóstico de demostración: validar, clasificar, analizar causa y efecto, y emitir un informe.
- Separación entre catálogo, orquestación, servidor HTTP y presentación.
- Puerto de arquitectura para conectar una base externa más adelante, sin almacenar aquí información personal.

## Estructura

```text
control/       lógica del catálogo, trabajos y servidor
web/           panel estático
 tests/        pruebas automatizadas
 docs/          arquitectura y siguientes pasos
```

Consulta [`docs/architecture.md`](docs/architecture.md) para el flujo, las decisiones y las limitaciones.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

## Referencias técnicas

`dotintent/flutter-nfc-reader` sirve como ejemplo de separación entre una interfaz común y adaptadores específicos de plataforma. `j66817736-byte/synthesizer` sirve como referencia de interfaces intercambiables para proveedores y evaluación de flujos RAG. Se usan como referencias de diseño; este proyecto no copia ni incorpora sus bases de datos o código fuente.

## Seguridad y datos

No introduzcas secretos, credenciales ni datos personales en los ejemplos. La base personal queda deliberadamente fuera del repositorio. Antes de conectar una fuente real, define autenticación, permisos mínimos, validación, auditoría, retención y copias de seguridad.
