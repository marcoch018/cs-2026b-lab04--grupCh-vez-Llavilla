# Bitácora de uso de IA — BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 03/10 | Claude | Prompt 1 adaptado: 3 alternativas de estilo para BiblioUNSA con 1 mes, 2 developers y un VPS | Monolito en capas, monolito modular y microservicios; recomendó el monolito modular | Se contrastó cada alternativa con R-01, R-02 y R-03; microservicios exige varios despliegues, BD y broker, que no caben en 1 mes ni en un VPS | Aceptada |
| 2 | 03/10 | Claude | Prompt 2 (abogado del diablo) sobre el monolito modular | 5 riesgos: erosión de límites, punto único de falla, dependencia de la API académica, datos personales, picos de inicio de semestre | Se revisó que cada riesgo tuviera mitigación aplicable al presupuesto; se incorporaron import-linter, respaldos y el adaptador con reintentos (ADR-001 y ADR-003) | Aceptada |
| 3 | 03/10 | Claude | Proponer criterios, pesos y puntajes de la matriz derivados de drivers.md | 6 criterios con pesos 25/20/20/15/10/10 y puntajes 1–5 | Los pesos suman 100 %; los totales se recalcularon con `matriz.py` (3,60 / 4,15 / 2,85); cada peso cita un driver | Aceptada |
| 4 | 03/10 | Claude | Redactar ADR-002 de autenticación con correo institucional | Asumió que el correo institucional funciona sobre OIDC (p. ej. Google Workspace) y que basta "conectarlo" | Ese dato no está en el caso ni en R-05: es un supuesto no verificado. Se agregó el supuesto explícito en el ADR y se aisló la autenticación tras una interfaz para poder cambiar de proveedor | Corregida |
| 5 | 03/10 | Claude | Generar el código Mermaid de la arquitectura elegida a partir de la matriz | Diagrama con 2 actores, 6 módulos, PostgreSQL y 3 servicios externos | Revisión línea por línea y trazabilidad módulo → requisito (Autenticación→RF-06, Catálogo→RF-01/07, Reservas→RF-02, Préstamos→RF-03, Multas→RF-04, Notificaciones→RF-08, adaptador académico→RF-05); validación de sintaxis en mermaid.live | Aceptada |
| 6 | 03/10 | Claude | Generar `despliegue.py` con Python Diagrams | Script con usuarios, Nginx, Django, Celery, Redis, PostgreSQL, monitoreo y 3 servicios externos | Se ejecutó el script y se comprobó que la imagen incluye usuarios, servidor, aplicación, BD, servicios externos y monitoreo con conexiones etiquetadas | Aceptada |
| 7 | 03/10 | Claude | Generar `alternativa.puml` de la segunda mejor alternativa (capas) con nota de 3 a 5 líneas | Diagrama de componentes en capas con nota que cita el puntaje | Se renderizó con PlantUML; se corrigió que la nota citara el puntaje real de la matriz (3,60 frente a 4,15) y los puntajes por criterio | Corregida |

> Los prompts completos están en el anexo. Nunca se incluyeron datos personales ni información confidencial en un prompt.

## Anexo: prompts

### Prompt 1 — Generación de alternativas (adaptado)
```text
Actúa como arquitecto de software senior con experiencia en sistemas universitarios.
Contexto: plataforma "BiblioUNSA" para el préstamo y reserva de libros de las bibliotecas de la UNSA.
Actores: estudiante, bibliotecario y sistema académico. Funcionalidades: catálogo en línea, reserva de libros,
préstamo con carné QR, control de multas, validación de matrícula vigente. El acceso es con el correo
institucional y el sistema académico se consulta solo mediante API, sin acceso directo a su base de datos.
Restricciones: MVP en producción en 1 mes, equipo de 2 developers con experiencia en Python/Django,
presupuesto bajo (un VPS), cumplimiento de la Ley 29733.
Tarea: propón 3 alternativas de estilo arquitectónico. Para cada una indica fortalezas, debilidades,
riesgos y qué atributos de calidad favorece o penaliza.
Formato: tabla comparativa en Markdown y, al final, tu recomendación justificada.
No inventes APIs ni capacidades de servicios; si no estás seguro, indícalo.
```

### Prompt 2 — Crítica adversarial
```text
Ahora actúa como "abogado del diablo". Critica duramente la alternativa que recomendaste: ¿qué supuestos
no se cumplen con nuestras restricciones?, ¿qué podría fallar en producción?, ¿qué costo oculto tiene?
Enumera los 5 riesgos más graves y, para cada uno, una táctica arquitectónica de mitigación.
```
Resumen de la respuesta: (1) erosión de límites entre módulos → interfaces públicas e import-linter en la CI; (2) punto único de falla → healthchecks, reinicio automático y respaldos diarios de PostgreSQL; (3) dependencia de la API académica → adaptador con timeout, caché y reintentos; (4) datos personales (Ley 29733) → minimizar datos, HTTPS, roles y registro de accesos; (5) picos de inicio de semestre en un solo VPS → caché, paginación e índices, y extraer Catálogo si hace falta.

### Prompt 3 — Criterios y pesos
```text
Con los drivers de drivers.md (RF-01..RF-08, QA-01..QA-04, R-01..R-06) propón mínimo 5 criterios para
comparar las 3 alternativas, con pesos que sumen 100 % y la justificación de cada peso citando un driver.
Puntúa de 1 a 5 y explica cada puntaje en una línea.
```

### Prompt 4 — ADR de autenticación
```text
Redacta un borrador de ADR (plantilla 000-plantilla.md) para la autenticación con el correo institucional
de la UNSA. Cita los IDs de drivers.md, compara mínimo 2 alternativas e indica consecuencias positivas y
negativas. Si asumes algo que no está en el caso, márcalo explícitamente como supuesto.
```

### Prompt 5 — Diagrama Mermaid
```text
A partir de matriz-decision.md, escribe el diagrama Mermaid (flowchart TB) de la alternativa elegida con
mínimo 2 actores, todos los módulos, el almacenamiento de datos, mínimo 1 servicio externo y la dirección
de las dependencias. Usa subgraph para el monolito modular.
```

### Prompt 6 — Vista de despliegue
```text
Escribe un script de Python Diagrams (despliegue.py) con usuarios, proxy, aplicación, base de datos, caché/cola,
servicios externos y monitoreo, usando Cluster para el servidor y Edge(label=...) en las conexiones.
Guarda la imagen en img/.
```

### Prompt 7 — Alternativa descartada
```text
Diagrama en PlantUML la segunda mejor alternativa de la matriz (monolito en capas) como diagrama de
componentes, con una nota de 3 a 5 líneas que explique por qué se descartó citando su puntaje.
```
