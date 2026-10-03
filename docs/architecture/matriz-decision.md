# Matriz de decisión — BiblioUNSA

## Alternativas
- **A. Monolito en capas:** una sola aplicación dividida en presentación, lógica de negocio y acceso a datos; cada capa usa solo la inferior. Un despliegue y una base de datos.
- **B. Monolito modular (con puertos y adaptadores para integraciones):** un solo despliegue dividido en módulos de dominio (Autenticación, Catálogo, Reservas, Préstamos, Multas, Notificaciones) con interfaces explícitas. Las integraciones externas (sistema académico, identidad, correo) se aíslan en adaptadores.
- **C. Microservicios:** un servicio por módulo, cada uno con su base de datos, detrás de un API Gateway y comunicados con un broker de eventos.

## Criterios y pesos (suman 100 %)
| Criterio                       | Peso | Justificación (driver relacionado)                                                                                 |
|--------------------------------|------|--------------------------------------------------------------------------------------------------------------------|
| Seguridad                      | 25 % | Atributo crítico: QA-01, R-04 (Ley 29733) y R-05 (solo correo institucional). Es el de mayor peso.                |
| Interoperabilidad              | 20 % | QA-02 y R-06: la integración con el sistema académico solo por API debe poder aislarse y verificarse.             |
| Tiempo de entrega              | 20 % | R-01: el MVP debe estar en producción en 1 mes.                                                                    |
| Costo operativo                | 15 % | R-03: un solo VPS de bajo costo.                                                                                   |
| Simplicidad operativa          | 10 % | R-02: equipo de 2 developers; cada servicio adicional es más operación y monitoreo.                                |
| Modificabilidad                | 10 % | QA-02/RF-05: la API académica o las reglas de multas pueden cambiar sin reescribir el sistema.                     |
| **Total**                      | 100 %|                                                                                                                    |

## Matriz (puntaje 1 = muy malo … 5 = excelente)
| Criterio (peso)                | A. Capas | B. Monolito modular | C. Microservicios |
|--------------------------------|----------|---------------------|-------------------|
| Seguridad (25 %)               | 3        | 4                   | 3                 |
| Interoperabilidad (20 %)       | 2        | 4                   | 4                 |
| Tiempo de entrega (20 %)       | 5        | 4                   | 2                 |
| Costo operativo (15 %)         | 5        | 5                   | 2                 |
| Simplicidad operativa (10 %)   | 5        | 4                   | 1                 |
| Modificabilidad (10 %)         | 2        | 4                   | 5                 |
| **Total ponderado**            | **3,60** | **4,15**            | **2,85**          |

Total ponderado = Σ (peso × puntaje). Ejemplo para B: 0,25×4 + 0,20×4 + 0,20×4 + 0,15×5 + 0,10×4 + 0,10×4 = 4,15.
El cálculo y el gráfico se regeneran con [`diagramas/matriz.py`](diagramas/matriz.py) (salida: `diagramas/img/matriz.png`).

### Justificación de los puntajes
| Criterio            | Razonamiento                                                                                                                                                                      |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Seguridad           | A: una sola capa de acceso, pero sin aislar la autenticación (3). B: autenticación como módulo con interfaz única y un solo punto de control (4). C: más servicios = más superficie de ataque y más secretos que gestionar (3). |
| Interoperabilidad   | A: la llamada al sistema académico queda mezclada con la lógica (2). B y C: adaptador/servicio dedicado que se puede probar y simular (4).                                         |
| Tiempo de entrega   | A: lo más rápido (5). B: requiere definir módulos e interfaces (4). C: múltiples despliegues, red y broker no caben en 1 mes con 2 developers (2).                               |
| Costo operativo     | A y B: un VPS y una BD (5). C: varios servicios, BD y broker (2).                                                                                                                  |
| Simplicidad operativa | A: un proceso (5). B: un proceso con disciplina de límites (4). C: orquestación y monitoreo distribuido (1).                                                                    |
| Modificabilidad     | A: cambios se propagan entre capas (2). B: módulos con interfaces (4). C: servicios independientes (5).                                                                           |

## Afirmación de la IA que no respetaba las restricciones
La IA asumió que el correo institucional de la UNSA funciona sobre un proveedor de identidad estándar (OIDC, p. ej. Google Workspace) y que bastaba "conectar" la autenticación. Ese dato no estaba en el caso. Se corrigió: ADR-002 deja el proveedor de identidad como **supuesto a confirmar con la oficina de TI** y aísla la autenticación detrás de una interfaz para poder cambiarla. Ver [bitácora, entrada 4](bitacora-ia.md).

## Conclusión
Elegimos **B. Monolito modular** (4,15) porque cumple el plazo de 1 mes (R-01) con 2 developers (R-02) en un solo VPS (R-03), y permite aislar la autenticación y la integración con el sistema académico en módulos/adaptadores (QA-01, QA-02, R-06). La alternativa A (3,60) queda como segunda opción y C (2,85) excede la capacidad del equipo. Ver [ADR-001](adr/001-estilo-arquitectonico.md).
