# Daily 10 — Viernes 25 de septiembre de 2026

**Equipo:** Leadify · **Curso:** Fundamentos de Software · **Duración:** 15 min
**Asistentes:** Diego Ortiz, Carlos Figueroa, Santiago Díaz, Sara Cuervo

## Temas tratados
- **El motor de recomendación ya está en producción (Render).** El `render.yaml` estaba dentro de `Demo/` y Render solo lee el de la raíz del repositorio, así que el backend nunca se había desplegado y el formulario calculaba con el motor de reglas del navegador. Se movió a la raíz.
- **El formulario usa el modelo real:** `SIN_BACKEND` estaba en `true` y la función `urlDeRecomendar()` llamaba a `/recomendar` sin el prefijo `/api`. El modelo respondía 404 y la app caía al motor local en silencio, sin mostrar ningún error. Probado de punta a punta: 200 en `/api/recomendar` con 18 proyectos con fotos y direcciones reales.
- **Llamada de Manuela (Dapta):** la dirección apuntaba al backend de otro proyecto. Ahora hay un flujo propio de Leadify ("leadify---disparador-de-llamadas") y el endpoint `POST /api/llamar` vive en el backend de Leadify. Responde 200 con el payload de 19 campos; sigue en modo simulado hasta cargar las credenciales de Dapta en Render.
- **Botón de WhatsApp pausado:** sin un número real, `wa.me` abre un chat sin destinatario. Queda solo "Llamar", y el código del botón quedó comentado para reactivarlo.
- README: se agregaron Postgres/PL-pgSQL y three.js a la sección de Tecnologías.
- Se entregó el **reporte gerencial** (`Docs/Reporte-Gerencial.md`): 10 de 11 historias cerradas según el tablero, métricas del sistema en producción y los riesgos con su estado.

## Por integrante
- **Diego:** revisa que el README quede consistente con lo desplegado.
- **Carlos:** revisa el reporte gerencial frente al tablero de GitHub.
- **Santiago:** movió el despliegue, conectó el modelo, ajustó la llamada y pausó WhatsApp.
- **Sara:** valida con el reporte la historia que sigue abierta.

## Impedimentos
- El plan gratuito de Render "duerme" el servicio: tras 15 minutos sin uso, la primera consulta tarda entre 30 y 50 segundos. Hay un respaldo con el motor local.
- Faltan las credenciales de Dapta en Render para que la llamada deje de ser simulada.

## Acuerdos
- Despertar el servicio unos minutos antes de cualquier demostración en vivo.
- Pendientes: cerrar HU-010 con la evidencia de las pruebas, actualizar las fechas de sprint y reactivar la protección de `main`.

# Evidencia
<img width="704" height="1524" alt="Daily5" src="https://github.com/user-attachments/assets/3c8aa01a-2b21-436b-b2f6-0adc03bc5b7d" />

