# Drivers arquitectónicos — BiblioUNSA

Sistema de préstamo y reserva de libros de las bibliotecas de la UNSA. Actores: estudiante, bibliotecario y sistema académico.

## 1. Requisitos funcionales clave
| ID    | Requisito                                                                  | Actor                     | Prioridad |
|-------|----------------------------------------------------------------------------|---------------------------|-----------|
| RF-01 | Consultar el catálogo en línea (búsqueda por título, autor y biblioteca)    | Estudiante                | Alta      |
| RF-02 | Reservar un libro disponible                                               | Estudiante                | Alta      |
| RF-03 | Registrar préstamo y devolución escaneando el carné QR                     | Bibliotecario             | Alta      |
| RF-04 | Calcular y controlar multas por devolución tardía                          | Bibliotecario, Estudiante | Media     |
| RF-05 | Validar matrícula vigente consultando el sistema académico (API)           | Sistema académico         | Alta      |
| RF-06 | Iniciar sesión con el correo institucional                                 | Estudiante, Bibliotecario | Alta      |
| RF-07 | Gestionar inventario del catálogo (altas, bajas, ejemplares)               | Bibliotecario             | Media     |
| RF-08 | Notificar por correo (reserva lista, vencimiento de préstamo, multa)       | Estudiante                | Media     |

## 2. Atributos de calidad (ordenados por prioridad)
1. **Seguridad** (atributo crítico) — solo personas con correo institucional acceden y se manejan datos personales de estudiantes (Ley 29733).
2. **Interoperabilidad** (compatibilidad, ISO/IEC 25010:2023) — la matrícula se valida solo mediante la API del sistema académico, sin acceso a su base de datos.
3. **Disponibilidad / fiabilidad** — una caída del sistema académico no debe impedir consultar el catálogo ni perder reservas.
4. **Eficiencia de desempeño** — la búsqueda en el catálogo debe responder bien al inicio de semestre, cuando hay más consultas.
5. **Mantenibilidad (modificabilidad)** — el sistema debe poder adaptarse si cambia la API académica o se agregan reglas de préstamo/multas.

## 3. Restricciones
| ID   | Tipo         | Restricción                                                                               |
|------|--------------|-------------------------------------------------------------------------------------------|
| R-01 | Plazo        | MVP en producción en 1 mes                                                                |
| R-02 | Equipo       | 2 developers con experiencia en Python/Django y PostgreSQL                                |
| R-03 | Presupuesto  | Un servidor (VPS) de bajo costo; cualquier servicio de pago debe justificarse             |
| R-04 | Normativa    | Ley 29733 de protección de datos personales (datos de estudiantes)                        |
| R-05 | Tecnología   | El acceso se hace con el correo institucional (no se crean cuentas propias con contraseña)|
| R-06 | Integración  | El sistema académico se consulta solo por API; prohibido acceso directo a su base de datos|

## 4. Escenarios de atributos de calidad
| ID    | Atributo        | Fuente                          | Estímulo                                   | Entorno                              | Artefacto                          | Respuesta                                                                                                  | Medida                                                                                   |
|-------|-----------------|---------------------------------|--------------------------------------------|--------------------------------------|------------------------------------|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| QA-01 | Seguridad       | Persona con correo no institucional (p. ej. @gmail.com) | Intenta iniciar sesión y reservar un libro | Operación normal                     | Módulo Autenticación (API)         | Rechaza el acceso, no crea sesión y registra el intento                                                    | 100 % de 50 intentos de prueba rechazados; 0 sesiones creadas; registro en ≤ 1 s         |
| QA-02 | Interoperabilidad | Estudiante autenticado        | Solicita una reserva                       | Operación normal                     | Adaptador del Sistema Académico    | Valida la matrícula vigente mediante la API del sistema académico, sin consultar su base de datos          | 0 conexiones directas a la BD académica; validación con p95 ≤ 2 s                        |
| QA-03 | Disponibilidad  | API del Sistema Académico       | No responde (timeout de 5 s)               | Operación normal                     | Módulo Reservas + adaptador        | El catálogo sigue disponible; la reserva queda "pendiente de validación" y se reintenta automáticamente    | 0 reservas perdidas; reintento cada ≤ 10 min; catálogo con 100 % de disponibilidad       |
| QA-04 | Rendimiento     | 500 estudiantes concurrentes (supuesto del grupo) | Buscan libros en el catálogo | Inicio de semestre, hora pico        | Módulo Catálogo (API)              | Devuelve resultados paginados (20 por página)                                                              | p95 del tiempo de respuesta ≤ 2 s                                                        |
