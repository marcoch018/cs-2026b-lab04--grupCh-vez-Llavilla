# ADR-002: Autenticación delegada al proveedor de identidad del correo institucional

- Estado: Aceptado
- Fecha: 2026-10-03
- Decisores: Grupo XX (integrantes del laboratorio)

## Contexto
Solo deben ingresar estudiantes y bibliotecarios de la UNSA (RF-06). El atributo crítico es la seguridad (QA-01), se manejan datos personales de estudiantes (R-04, Ley 29733) y la restricción R-05 exige acceso con el correo institucional. Con 2 developers y 1 mes (R-01, R-02) no conviene construir ni custodiar contraseñas propias.

## Alternativas consideradas
1. Cuentas propias con usuario y contraseña almacenadas en BiblioUNSA: control total, pero el equipo custodia credenciales, debe implementar recuperación y bloqueos, y duplica cuentas.
2. Inicio de sesión delegado (OpenID Connect) al proveedor del correo institucional, validando el dominio del correo: sin contraseñas propias y reutiliza las cuentas existentes.

## Decisión
Usaremos inicio de sesión delegado con OpenID Connect al proveedor de identidad del correo institucional y aceptaremos solo correos del dominio institucional. El rol (estudiante o bibliotecario) se asigna en BiblioUNSA. Supuesto a confirmar con la oficina de TI de la UNSA: que el correo institucional ofrece OIDC (p. ej. sobre Google Workspace). La autenticación quedará detrás de una interfaz del módulo Autenticación para poder cambiar de proveedor sin afectar otros módulos.

## Consecuencias
- Positivas: no se almacenan contraseñas; cumple QA-01 con un único punto de control; menos código que mantener y menor riesgo en datos personales.
- Negativas / riesgos: dependencia del proveedor externo (si cae, nadie inicia sesión; se mitiga con sesiones de duración limitada); si el proveedor no ofreciera OIDC, habrá que cambiar el adaptador, lo que afectaría el plazo.
