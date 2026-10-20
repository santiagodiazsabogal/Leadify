# Daily 8 — Miércoles 23 de septiembre de 2026

**Equipo:** Leadify · **Curso:** Fundamentos de Software · **Duración:** 15 min
**Asistentes:** Diego Ortiz, Carlos Figueroa, Santiago Díaz, Sara Cuervo

## Temas tratados
- **Plano 3D del apartamento** en el formulario: el panel arma el apartamento a medida que la persona responde. Viene del prototipo aparte "Vivienda 3D", portado a JavaScript vanilla con three.js (escena, muros, muebles, materiales y zonificación en `js/plano3d/`).
- Es una **mejora progresiva**: el plano 2D de recortes sigue debajo y es lo que se ve si el equipo no tiene WebGL o es de gama baja.
- Se corrió un paso la tabla `ETAPAS` de `perfil.js`: estaba calibrada para otro orden de preguntas (ahora "zona" va primera) y los ambientes aparecían antes de tiempo, sin ningún error visible.
- Incidente: un `force-push` dejó `main` con 81 commits menos (CI, `.gitignore`, guía de usuario, mockups y el 3D). Se recuperó fusionando las dos historias, sin perder el trabajo de nadie.
- La verificación automática de GitHub Actions se retiró. Los cuatro scripts siguen en `Script/` para correrlos a mano.

## Por integrante
- **Diego:** confirma que sus commits (mockup, README y contributors) siguen intactos tras la recuperación.
- **Carlos:** revisa el historial de `main` y `develop` para confirmar que quedaron reconectadas.
- **Santiago:** portó el 3D y ejecutó la recuperación del historial.
- **Sara:** prueba el formulario con el plano 3D y valida que el 2D aparezca como respaldo.

## Impedimentos
- La protección de la rama `main` está desactivada, así que otro `force-push` volvería a sobrescribirla.

## Acuerdos
- Avisar en el grupo antes de hacer `force-push`.
- Reactivar la protección de `main` antes de la entrega final.
- Siguiente paso: guardar en base de datos a quien llena el formulario.

# Evidencia

<img width="698" height="357" alt="Daily8" src="https://github.com/user-attachments/assets/cb0ebfa1-1e5a-405e-9834-889188eea65e" />

