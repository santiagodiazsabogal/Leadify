# Daily 12 — Jueves 15 de octubre de 2026

**Equipo:** Leadify · **Curso:** Fundamentos de Software · **Duración:** 15 min
**Asistentes:** Diego Ortiz, Carlos Figueroa, Santiago Díaz, Sara Cuervo

## Temas tratados
- **Diseño del login de empresas.** Una cuenta equivale a una empresa (constructora o inmobiliaria). Lo maneja el backend de FastAPI, sin Supabase Auth, y las cuentas viven en Postgres.
- **Esquema `acceso` aparte,** con tres tablas: `cuentas`, `sesiones` e `intentos`. La API pública de Supabase no lo expone: solo entra el backend, por conexión directa.
- **Seguridad:**
  - Contraseña con scrypt y sal propia por cuenta.
  - Sesión con cookie `HttpOnly`, `Secure` y `SameSite=Lax`; en la base solo se guarda el SHA-256 del token.
  - "Recordarme" dura 30 días; sin él, la sesión vence al cerrar el navegador o a las 12 horas.
  - Tope de 5 fallos por correo cada 15 minutos y de 20 registros por IP por hora.
  - Los mensajes de error no revelan si un correo existe.
- **Las cuentas nacen activas,** sin confirmación de correo ni revisión, y no hay recuperación de contraseña por correo.
- **Cambio en la identificación de los leads:** pasan de cédula a **teléfono + correo**. El teléfono es la llave y el correo actúa como segundo factor: se fija la primera vez y nunca se sobreescribe, para que nadie reclame el teléfono de otra persona.
- Los datos guardados por cédula **no se borran**: se mueven a un esquema cerrado, `archivo_cedula`.

## Por integrante
- **Diego:** revisa las variables de entorno necesarias (`DATABASE_URL`) y cómo documentarlas en el README.
- **Carlos:** revisa los criterios de aceptación del login contra el diseño.
- **Santiago:** escribe las migraciones de las cuentas y de los leads por teléfono y correo.
- **Sara:** valida que el cambio de cédula a teléfono y correo no rompa el flujo de "volver y ver mis resultados".

## Impedimentos
- Pasar las filas viejas a la llave nueva no se puede hacer sin adivinar: un mismo teléfono aparece con varias cédulas. Por eso se archivan.

## Acuerdos
- Mantener la misma política de seguridad: tablas cerradas y acceso solo por funciones del servidor.
- Las migraciones se numeran por fecha y se aplican en orden.

# Evidencia
<img width="704" height="1524" alt="Daily5" src="https://github.com/user-attachments/assets/7f9138b2-a386-4e7b-9a5d-48e39e2302c9" />
