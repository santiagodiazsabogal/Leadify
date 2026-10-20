# Daily 15 — Martes 20 de octubre de 2026

**Equipo:** Leadify · **Curso:** Fundamentos de Software · **Duración:** 15 min
**Asistentes:** Diego Ortiz, Carlos Figueroa, Santiago Díaz, Sara Cuervo

## Temas tratados
- **Entró la integración completa:**
  - Login de empresas conectado al backend: `POST /api/cuentas` para registrarse y `POST`, `GET` y `DELETE` sobre `/api/sesion` para entrar, consultar y cerrar sesión. Pantallas en `/acceso/` y `/inicio/`.
  - Formulario con **dos recorridos: compra o arriendo** (vivienda, oficina o bodega), cada uno con su catálogo y su endpoint.
  - Leads identificados por **teléfono y correo**, con las migraciones aplicadas y los datos por cédula archivados.
- **Decisión de producto:** se probó una landing que ofrecía "entrar al formulario" o "iniciar sesión", y se retiró el mismo día. La raíz del sitio abre directamente el formulario, sin landing ni pantalla de bienvenida. Con eso se fueron la landing, sus imágenes y la tabla de solicitudes de demo.
- **Identidad visual:** el logo pasa a ser la palabra Leadify con el punto coral, en el login, el formulario y el favicon.
- La base de datos quedó con el esquema `acceso` (cuentas, sesiones e intentos) y las tablas de leads por teléfono y correo.

## Por integrante
- **Diego:** actualiza el README con las rutas `/acceso/` e `/inicio/` y las variables de entorno nuevas.
- **Carlos:** cierra en el tablero las historias de login, arriendo y leads por teléfono.
- **Santiago:** integró el login y el arriendo, aplicó las migraciones y simplificó la entrada.
- **Sara:** prueba de punta a punta los dos recorridos y valida que la raíz abra el formulario.

## Impedimentos
- Sin confirmación de correo ni recuperación de contraseña, quien olvide la clave no puede recuperarla. Está asumido por la limitación del plan gratuito de Render.
- Siguen abiertos: la protección de `main` y el cierre formal de HU-010.

## Acuerdos
- Reactivar la protección de `main` antes de la entrega final.
- Consolidar la evidencia de pruebas de integración en HU-010 y cerrarla.
- Despertar el servicio de Render antes de la demostración.

# Evidencia

<img width="739" height="1600" alt="655205999-b47db590-e8d1-4424-9906-1bcd04d2cf0f" src="https://github.com/user-attachments/assets/83590021-88b3-42f2-b1ba-6f45d4ffd578" />

