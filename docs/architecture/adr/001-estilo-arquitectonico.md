# ADR-001: Adoptar un monolito modular para el MVP de BiblioUNSA

- Estado: Aceptado
- Fecha: 2026-10-03
- Decisores: Grupo XX (integrantes del laboratorio)

## Contexto
El MVP debe estar en producción en 1 mes (R-01) con 2 developers que dominan Python/Django (R-02) y un solo VPS de bajo costo (R-03). El atributo crítico es la seguridad (QA-01, R-04, R-05) y la integración con el sistema académico debe hacerse solo por API (QA-02, R-06). Además, las reglas de préstamo, multas y la API académica pueden cambiar, por lo que importa la modificabilidad (RF-04, RF-05).

## Alternativas consideradas
1. Monolito en capas (3,60): rápido y simple, pero las integraciones y reglas quedarían mezcladas entre capas y los cambios se propagarían.
2. Microservicios (2,85): máxima independencia, pero exige varios despliegues, bases de datos y un broker que el equipo no puede operar en 1 mes ni con el presupuesto de R-03.
3. Monolito modular (4,15): elegido. Ver `docs/architecture/matriz-decision.md`.

## Decisión
Usaremos un monolito modular en Django con 6 módulos (Autenticación, Catálogo, Reservas, Préstamos, Multas, Notificaciones). Los módulos se comunican solo mediante interfaces públicas (servicios de aplicación) y cada uno tiene su propio esquema en PostgreSQL. Las integraciones externas (sistema académico, identidad, correo) se implementan como adaptadores (puertos y adaptadores).

## Consecuencias
- Positivas: un solo despliegue, bajo costo y entrega en 1 mes; las integraciones quedan aisladas y probables; los módulos pueden extraerse como servicios si la carga lo exige.
- Negativas / riesgos: el equipo debe respetar los límites entre módulos (se usará import-linter en la CI); una falla grave afecta a todo el sistema, por lo que se requiere monitoreo y respaldos.
