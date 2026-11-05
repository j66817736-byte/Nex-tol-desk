# Arquitectura y flujo

## Objetivo de esta primera entrega

Crear un panel local comprobable que haga visible la estructura del control y muestre cómo una solicitud se transforma en un resultado. No crea ni incorpora la base de datos personal del usuario. La memoria de trabajos es temporal y se pierde al reiniciar.

## Recorrido de una solicitud

1. El navegador pide `/api/modules` y `/api/jobs`.
2. `control/server.py` valida la ruta y entrega JSON o archivos estáticos.
3. `control/catalog.py` ofrece metadatos de módulos; no contiene registros de usuarios.
4. Al iniciar el diagnóstico, `control/jobs.py` ejecuta pasos explícitos: validación → clasificación → análisis de causa/efecto → informe.
5. La interfaz muestra pasos y límites, sin afirmar que consultó datos externos.

## Límites deliberados

- No hay conexión a base de datos, persistencia, autenticación ni cuentas todavía.
- El flujo actual es una demostración determinista, no una IA ni un diagnóstico de sistemas reales.
- El servidor solo debe usarse localmente. Antes de una exposición remota se requieren controles de acceso, HTTPS, gestión de secretos, límites de uso y revisión de seguridad.
- El panel no debe guardar información personal por defecto. La fuente externa futura debe ser elegida y autorizada explícitamente.

## Extensión sin mezclar datos

Definir contratos pequeños para cada fuente/adaptador (por ejemplo, `list_status()` y `health_check()`), mantener la orquestación independiente del proveedor y testearlos con dobles de prueba. Los secretos se entregan por variables de entorno o un gestor de secretos; nunca se versionan. Los datos se consultan con permisos mínimos y se separa configuración de lógica.

## Referencias observadas

- El plugin Flutter NFC organiza una API Dart y adaptaciones nativas para Android/iOS; la lección útil es ocultar diferencias de plataforma tras un contrato común y documentar las capacidades que no son iguales.
- Synthesizer separa interfaces de proveedores de LLM y RAG y presenta un arnés de evaluación; la lección útil es intercambiar proveedores y medir resultados en lugar de acoplar la lógica a uno solo.
- Esas referencias guían decisiones; el código de esta primera entrega es nuevo y no importa su almacenamiento ni datos.
