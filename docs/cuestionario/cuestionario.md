# Cuestionario — Laboratorio 04 (BiblioUNSA)

**1. ¿Por qué una decisión arquitectónica es "costosa de cambiar"? Ejemplo.**
Porque condiciona la estructura de todo el sistema: cambiarla obliga a reescribir código, datos, pruebas y despliegue. En BiblioUNSA, elegir monolito modular con un esquema de PostgreSQL por módulo (ADR-001) define cómo se organizan el código y los datos. Pasar luego a microservicios o a otra base de datos implicaría separar esquemas, crear APIs entre módulos y operar varios despliegues. En cambio, elegir el nombre de una variable es barato de cambiar y no es arquitectura.

**2. Requisito funcional vs. atributo de calidad. ¿Por qué los atributos influyen más en la arquitectura?**
Un requisito funcional dice *qué* hace el sistema (RF-02: reservar un libro). Un atributo de calidad dice *qué tan bien* lo hace (seguridad, interoperabilidad, disponibilidad, rendimiento). Casi cualquier arquitectura puede ofrecer las mismas funciones, pero los atributos condicionan la estructura: la seguridad y la interoperabilidad de BiblioUNSA llevaron a aislar la autenticación y la API académica en módulos y adaptadores (ADR-002 y ADR-003).

**3. Reescribir "el sistema debe ser seguro" como escenario de seis partes.**
| Parte | Valor |
|---|---|
| Fuente | Persona con un correo no institucional (p. ej. @gmail.com) |
| Estímulo | Intenta iniciar sesión y reservar un libro |
| Entorno | Operación normal |
| Artefacto | Módulo Autenticación (API) |
| Respuesta | Rechaza el acceso, no crea sesión y registra el intento |
| Medida | 100 % de 50 intentos de prueba rechazados; 0 sesiones creadas; registro en ≤ 1 s |

**4. Monolito modular vs. microservicios (costo, modificabilidad, complejidad operativa) y cuándo migrar.**
El monolito modular tiene costo bajo (un VPS y una BD), buena modificabilidad si se respetan los límites entre módulos y operación simple. Los microservicios tienen costo alto (varios servicios, BD y broker), la mayor modificabilidad e independencia de despliegue, y una complejidad operativa elevada (red, datos distribuidos, monitoreo). Conviene migrar cuando un módulo necesite escalar de forma independiente, cuando varios equipos choquen al desplegar el mismo monolito o cuando una falla en un módulo afecte demasiado al resto, y siempre que exista capacidad de operar el sistema distribuido. En BiblioUNSA, el módulo Catálogo sería el primer candidato si la carga de consulta lo exigiera.

**5. Ventajas de Diagram as Code frente a PowerPoint (mínimo 3).**
(a) Se versiona en Git junto al código y muestra diferencias línea por línea. (b) Se revisa en un Pull Request como cualquier archivo. (c) Se regenera automáticamente (por ejemplo, con una GitHub Action), evitando imágenes desactualizadas. (d) Es texto, por lo que una IA puede generarlo y corregirlo con facilidad. (e) Estandariza estilos sin dibujar a mano.

**6. Elementos de un ADR y por qué registrar las alternativas descartadas.**
Título, estado, fecha, decisores, contexto (drivers que motivan la decisión), alternativas consideradas, decisión y consecuencias positivas y negativas. Registrar lo descartado evita reabrir la misma discusión, muestra que la decisión fue analizada y permite revisarla si cambian las condiciones (por ejemplo, el presupuesto o el tamaño del equipo).

**7. Caso en que la IA generó una propuesta incorrecta o sesgada. ¿Cómo se detectó?**
Al redactar el ADR-002, la IA asumió que el correo institucional de la UNSA ofrece inicio de sesión estándar (OIDC, p. ej. Google Workspace), un dato que no estaba en el caso. Se detectó al contrastar el borrador con los drivers (R-05 solo exige acceso con correo institucional) y preguntarnos qué evidencia respaldaba ese dato. Se corrigió marcándolo como supuesto a confirmar con la oficina de TI y aislando la autenticación tras una interfaz. (Ver bitácora, entrada 4.)

**8. Riesgos éticos y de confidencialidad al usar IA para diseñar la arquitectura de un sistema real.**
Enviar información confidencial (credenciales, datos personales de estudiantes, detalles internos de seguridad o de la API académica) a un servicio externo; incumplir la Ley 29733 de protección de datos personales; depender de salidas con datos inventados o sesgadas hacia arquitecturas de moda; atribuir a la IA decisiones que debe asumir el equipo; y posibles problemas de propiedad intelectual o licencias en lo generado. Mitigaciones: no incluir datos personales ni secretos en los prompts, anonimizar el contexto, verificar toda salida y registrar el uso en la bitácora.
