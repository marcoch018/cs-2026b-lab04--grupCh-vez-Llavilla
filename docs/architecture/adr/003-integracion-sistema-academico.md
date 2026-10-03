# ADR-003: Integrar el sistema académico mediante un adaptador con reintento asíncrono

- Estado: Aceptado
- Fecha: 2026-10-03
- Decisores: Grupo XX (integrantes del laboratorio)

## Contexto
Antes de reservar o prestar hay que validar la matrícula vigente en el sistema académico (RF-05). La restricción R-06 permite consultarlo solo por API, sin acceso a su base de datos, y QA-02 exige verificarlo. Además, QA-03 pide que una caída del sistema académico no impida consultar el catálogo ni pierda reservas. El equipo es pequeño (R-02) y usa un solo VPS (R-03).

## Alternativas consideradas
1. Llamada síncrona directa desde Reservas y Préstamos al sistema académico: simple, pero una caída bloquea las reservas y el código de integración queda disperso.
2. Adaptador único (puerto y adaptador) que consulta la API, guarda en caché el resultado por un tiempo corto y, si hay timeout, registra la reserva como "pendiente de validación" y la reintenta con una cola de tareas (Celery + Redis).

## Decisión
Usaremos un adaptador único para el sistema académico, con timeout de 5 s, caché corta de la matrícula y reintentos cada 10 minutos mediante tareas asíncronas. Ningún otro módulo conoce la API académica. No se creará ninguna conexión a su base de datos.

## Consecuencias
- Positivas: cumple QA-02 y QA-03 (0 reservas perdidas, catálogo siempre disponible); si la API cambia solo se modifica el adaptador; se puede simular en pruebas.
- Negativas / riesgos: añade Redis y un worker al despliegue; una reserva puede quedar pendiente (consistencia eventual) y la caché puede mostrar una matrícula desactualizada durante unos minutos.
