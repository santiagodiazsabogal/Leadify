# Daily 9 — Jueves 24 de septiembre de 2026

**Equipo:** Leadify · **Curso:** Fundamentos de Software · **Duración:** 15 min
**Asistentes:** Diego Ortiz, Carlos Figueroa, Santiago Díaz, Sara Cuervo

## Temas tratados
- **Los leads ya se guardan en Postgres (Supabase):** quién llenó el formulario, qué respondió, qué se le recomendó, qué proyecto le interesó y si terminó agendando cita. Tres tablas: `leads`, `consultas` e `intereses`.
- **Quien vuelve no repite las siete preguntas:** el formulario le muestra los mismos resultados que vio la primera vez. Se guarda el resultado tal cual y se restaura con la misma acción que lo pintó.
- **Seguridad sin login para el comprador:** las tablas están cerradas (no se puede leer ni una fila con la clave del navegador) y solo hay cuatro funciones del lado del servidor. La de lectura, `buscar_resultados`, exige cédula **y** teléfono: con uno solo no devuelve nada, ni siquiera confirma que exista.
- **Intención de compra:** se marca en `true` cuando Dapta devuelve `fecha_de_seguimiento`, la señal de que quedó una cita con un asesor. Pedir la llamada, por sí solo, no cuenta.
- Si la base no responde, el formulario sigue su curso y solo se pierde el guardado. Tampoco se guardan listas de recomendaciones vacías.
- `Database/` documenta el esquema real de Supabase (`01_tablas.sql` y `02_funciones.sql`), tal como está aplicado y no reescrito de memoria.

## Por integrante
- **Diego:** revisa que el README y las instrucciones de instalación mencionen la base de datos.
- **Carlos:** corrigió el formato del README de `Database/` y revisa los nombres de tablas y funciones.
- **Santiago:** implementó el guardado, la lectura de resultados anteriores y las funciones del servidor.
- **Sara:** valida que el flujo de "volver y ver mis resultados" cumpla la historia de usuario.

## Impedimentos
- Ninguno bloqueante. Falta probar el flujo completo contra el servicio desplegado.

## Acuerdos
- Los datos personales solo se leen con la doble llave (cédula y teléfono).
- Guardar es un efecto secundario: nunca puede tumbar el formulario.
- Siguiente paso: dejar el modelo real funcionando en producción.

# Evidencia

<!-- Pegar aquí la captura del daily (24 SEPT) -->
