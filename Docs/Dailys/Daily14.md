# Daily 14 — Lunes 19 de octubre de 2026

**Equipo:** Leadify · **Curso:** Fundamentos de Software · **Duración:** 15 min
**Asistentes:** Diego Ortiz, Carlos Figueroa, Santiago Díaz, Sara Cuervo

## Temas tratados
- **Catálogo de arriendo (demo).** Nuevo scraper, `scraper_arriendo.py`, sobre Fincaraíz para vivienda, oficina y bodega de Bogotá. Es demo a propósito: por defecto se detiene en 50 inmuebles entre los tres tipos (parámetro `--tope`). Lee los datos estructurados de cada página de listado: precio, dirección, coordenadas, área y fotos. El catálogo de venta no se toca.
- **Modelo de arriendo** (`Model/arriendo.py`), con la misma mecánica del de compra en lo que sí tiene sentido para un canon mensual:
  - **Cercanía** a la zona elegida en el mapa, medida en kilómetros por el grafo de barrios. Es la pieza que manda.
  - **Perfil** (solo vivienda): Nearest Neighbors sobre habitaciones, baños, parqueaderos y estrato.
  - **Presupuesto** (solo vivienda): cuánto se pasa el canon del techo del rango.
  - Oficinas y bodegas reciben solo la cercanía, porque su recorrido no pregunta más.
- **Lo que no se reutiliza, a propósito:** el componente colaborativo y la cota de precio. Dependen de un historial simulado de compras y de cuota de hipoteca, que para arriendo no existen, y fingirlos sería inventar el dato.
- Los porcentajes de compatibilidad salen de la misma regla de compra: el primero se muestra con piso de 85 % y a cada siguiente se le resta lo que lo separa del anterior.
- **Pruebas:** `prueba_acceso.py` cubre el login y el arriendo; el login del front tiene sus propias pruebas con `npm run test:auth`.

## Por integrante
- **Diego:** documenta en el README los comandos nuevos y las dependencias agregadas al backend.
- **Carlos:** revisa los casos de prueba del login y del arriendo frente a los criterios de aceptación.
- **Santiago:** implementó el scraper, el modelo de arriendo y el endpoint.
- **Sara:** valida los textos y las preguntas del recorrido de arriendo para cada tipo de inmueble.

## Impedimentos
- Fincaraíz puede cambiar el formato de sus páginas, así que el scraper depende de que la estructura se mantenga. El catálogo generado queda versionado como respaldo.

## Acuerdos
- El catálogo de arriendo se mantiene como demo de 50 inmuebles.
- Mañana: integrar todo en el formulario y la entrada de las empresas.

# Evidencia

<img width="739" height="1600" alt="655205999-b47db590-e8d1-4424-9906-1bcd04d2cf0f" src="https://github.com/user-attachments/assets/c4d9a929-476c-48a0-adde-bb1146e931c0" />

