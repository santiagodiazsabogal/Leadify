# Reporte gerencial

**Fecha de corte:** 20 de noviembre de 2026
**Periodo:** Sprint 1 a Sprint 4 (agosto a noviembre de 2026)
**Para:** seguimiento del proyecto — lectura sin contexto técnico previo
**Reporte anterior:** 23 de octubre de 2026. Los cambios desde entonces se
resumen en [Qué cambió desde el 23 de octubre](#qué-cambió-desde-el-23-de-octubre).

---

## Resumen ejecutivo

Leadify es un formulario que recomienda vivienda en Bogotá D.C. La persona
elige primero si quiere **comprar** o **arrendar**:

- **Compra:** un modelo de *machine learning* (Nearest Neighbors,
  colaborativo + contenido) ordena 96 proyectos reales de cuatro
  constructoras según el perfil de quien responde, si puede pagarlos y qué tan
  cerca quedan del barrio donde quiere vivir, medido en kilómetros reales.
- **Arriendo:** recomienda sobre un catálogo de 93 inmuebles publicados
  (30 viviendas, 32 oficinas y 31 bodegas), según la zona, el presupuesto y
  las preferencias.

Al final, la persona puede pedir que **Manuela**, una agente de voz con IA, la
llame para calificar su interés y agendar con un asesor. Las constructoras e
inmobiliarias tienen además **cuentas propias** para entrar a Leadify.

**Estado actual (verificado el 20 de noviembre):**

- Formulario en producción: <https://leadify-kappa.vercel.app> responde. Abre
  directamente en el registro, sin pantallas previas.
- Motor de recomendación (compra y arriendo): desplegado en Render, responde
  en menos de un segundo con el servicio activo.
- Llamada automática (Dapta/Manuela): conectada. En la regresión del 17/11 se
  probó con llamada simulada, sin marcar a ningún número.
- Calidad del código: el análisis de SonarCloud pasa su umbral de calidad, con
  **0 problemas abiertos** y 82 cerrados.
- Pruebas: de los 15 casos del plan de pruebas, **11 pasan, 3 fallan y 1 no se
  pudo ejecutar** (regresión del 17/11).
- **Problema principal: la base de datos de producción está caída.** El
  proyecto de Supabase donde se guardan los leads está pausado y su dirección
  ya no responde. Mientras siga así, el formulario funciona pero **no guarda
  leads ni deja recuperar resultados anteriores**.
- **Pendiente en producción:** el login de empresas y la identificación de
  leads por teléfono y correo están en el código y probados en local, pero el
  servicio desplegado en Render todavía no expone las rutas de cuentas y la
  migración de la base no se ha aplicado.

---

## Qué cambió desde el 23 de octubre

| Tema | 23 de octubre | 20 de noviembre |
|---|---|---|
| Historias cerradas | 10 de 15 | 10 de 15 (sin cambio) |
| Commits en `main` | 101 | 116 (+15, sin contar este reporte) |
| Calidad del código | Sin análisis | SonarCloud: umbral aprobado, 0 problemas abiertos |
| Plan de pruebas | Sin plan | 15 casos en Azure DevOps, con regresión |
| Deuda técnica | Sin registro | 12 ítems, 165 h estimadas para pagarla |
| Base de datos de producción | Activa (reactivada el 20/10) | **Pausada otra vez** |
| Protección de `main` | Desactivada | Desactivada |
| Verificación automática en GitHub | Retirada | Se agregó el 17/11 y se retiró el mismo día |

El trabajo de las últimas cuatro semanas fue de **calidad, no de funciones
nuevas**: limpiar los avisos de SonarCloud (3 de noviembre), registrar la
deuda técnica (10 de noviembre) y escribir y ejecutar el plan de pruebas
(17 de noviembre).

---

## Medidas usadas

| Medida | Cómo se obtiene | Para qué sirve |
|---|---|---|
| Historias cerradas / planeadas por sprint | Issues de GitHub y su milestone | Avance de cada sprint |
| Puntos de historia (estimado) | Planning poker del equipo (carpeta `estimación/`) | Esfuerzo esperado de cada historia |
| Talla de la historia (estimado) | Etiquetas `XS`, `M` y `L` en el issue | Esfuerzo esperado en el Sprint 4 |
| Fecha estimada de una historia | Fecha de fin del sprint (milestone) | Plazo comprometido |
| Fecha real de una historia | Fecha de cierre del issue en GitHub | Plazo cumplido |
| Desviación en días | Fecha real − fecha estimada | Atraso (+) o adelanto (−) |
| Commits por semana en `main` | Historial de Git, sin merges | Actividad del equipo en el código |
| Casos de prueba que pasan | Plan de pruebas en Azure DevOps | Cumplimiento de los criterios de aceptación |
| Pruebas automáticas que pasan | Pruebas del login, del backend y de humo | Estabilidad del sistema |
| Problemas y umbral de calidad | SonarCloud | Salud del código |
| Deuda técnica (principal, en horas) | Registro de deuda técnica | Trabajo pendiente para dejar el código sano |
| Tiempo de respuesta del modelo | Medido contra el servicio en producción | Experiencia de quien usa el formulario |

**Lo que no se midió:** las horas reales de trabajo. El equipo estimó en
puntos pero no registró horas, así que el esfuerzo real se aproxima con la
actividad en el repositorio (más abajo). Registrar horas por historia queda
como acción para la siguiente entrega.

---

## Estado de avance de las historias

| HU | Historia | Sprint | Responsable | Estimación | Estado |
|---|---|---|---|---|---|
| HU-001 | Definición de preguntas | — | — | 1 punto | Cerrada |
| HU-002 | Diseño del cuestionario visual | Sprint 1 | Carlos Figueroa | 2 puntos | Cerrada |
| HU-003 | Diseño de la landing gamificada | Sprint 1 | Juan Diego Ortiz | 3 puntos | Cerrada |
| HU-004 | Integración de la landing gamificada | — | — | 3 puntos | Cerrada |
| HU-005 | Construcción del perfil de vivienda ideal | Sprint 1 | Sara Cuervo | 5 puntos | Cerrada |
| HU-006 | Implementación del clustering de viviendas | Sprint 2 | Carlos Figueroa | sin estimar | Cerrada |
| HU-007 | Cálculo del porcentaje de match | Sprint 2 | Santiago Díaz | sin estimar | Cerrada |
| HU-008 | Implementación de llamada automática | Sprint 3 | Santiago Díaz | sin estimar | Cerrada |
| HU-009 | Clasificación de intención de compra | Sprint 3 | Carlos Figueroa | sin estimar | Cerrada |
| HU-010 | Pruebas de integración del flujo completo | Sprint 3 | Sara Cuervo | sin estimar | **Abierta** — el caso CP-010 pasa; falta cerrar el issue con la evidencia |
| HU-011 | Despliegue y documentación del sistema | Sprint 3 | Juan Diego Ortiz | sin estimar | Cerrada |
| HU-012 | Login de empresas (crear cuenta y entrar) | Sprint 4 | Santiago Díaz | L | **Abierta** — código listo y probado en local; falta desplegarlo |
| HU-013 | Recorrido de arriendo en el formulario | Sprint 4 | Santiago Díaz | L | **Abierta** — en producción, falta validación del Product Owner |
| HU-014 | Leads identificados por teléfono y correo | Sprint 4 | Santiago Díaz | M | **Abierta** — falta aplicar la migración y reactivar la base |
| HU-015 | Entrada directa al formulario e identidad de Leadify | Sprint 4 | Santiago Díaz | XS | **Abierta** — en producción, falta validación del Product Owner |

### Avance por sprint

| Sprint | Historias | Cerradas | Fin del sprint |
|---|---|---:|---|
| Sprint 1 | HU-002, HU-003, HU-005 | 3 / 3 (100 %) | 29-ago-2026 |
| Sprint 2 | HU-006, HU-007 | 2 / 2 (100 %) | 05-sep-2026 |
| Sprint 3 | HU-008 a HU-011 | 3 / 4 (75 %) | 12-sep-2026 |
| Sprint 4 | HU-012 a HU-015 | 0 / 4 (0 %) | sin fecha |
| Sin sprint | HU-001, HU-004 | 2 / 2 (100 %) | — |
| **Total** | **15 historias** | **10 / 15 (67 %)** | |

Los números de avance **no cambiaron desde el 23 de octubre**: ninguna
historia se cerró en las últimas cuatro semanas. En el Sprint 4 el trabajo
está hecho y en el repositorio, pero ninguna historia está cerrada: dos
dependen de poner en marcha la base de producción y las cuatro esperan la
validación del Product Owner.

---

## Estimado frente a real

### Tiempos

![Fecha estimada frente a fecha real de cierre, por historia](../Gráficas/estimado-vs-real-historias.png)

| HU | Sprint | Estimado (fin del sprint) | Real (cierre en GitHub) | Desviación |
|---|---|---|---|---:|
| HU-002, HU-003, HU-005 | Sprint 1 | 29-ago-2026 | 25-ago-2026 | −4 días |
| HU-006, HU-007 | Sprint 2 | 05-sep-2026 | 21-sep-2026 | +16 días |
| HU-008, HU-009, HU-011 | Sprint 3 | 12-sep-2026 | 21-sep-2026 | +9 días |
| HU-010 | Sprint 3 | 12-sep-2026 | sigue abierta | +69 días al corte |

- El **Sprint 1 se cumplió antes de lo previsto**. Los Sprints 2 y 3 se
  cerraron con 9 a 16 días de atraso.
- Las ocho historias cerradas que tenían fecha se desviaron, en promedio,
  **+5,9 días** respecto a lo planeado.
- **HU-010 lleva 69 días de atraso** (eran 41 el 23 de octubre) solo porque su
  issue sigue abierto: su caso de prueba CP-010 pasa desde el 27 de octubre.
  Cerrarla es un trámite, no trabajo pendiente.
- **Cuidado al leer las fechas reales:** siete historias se cerraron el mismo
  día, el 21 de septiembre. Esa fecha es la de la actualización del tablero,
  no necesariamente la de terminación: el trabajo de varias estaba listo
  antes.
- HU-001 y HU-004 no tienen sprint asignado, y el Sprint 4 todavía no tiene
  fecha de fin, así que no se pueden comparar contra un plazo.

### Esfuerzo

| Historia | Puntos estimados | Resultado |
|---|---:|---|
| HU-001 | 1 | Cerrada el 21-sep, sin sprint |
| HU-002 | 2 | Cerrada dentro del Sprint 1 |
| HU-003 | 3 | Cerrada dentro del Sprint 1 |
| HU-004 | 3 | Cerrada el 21-sep, sin sprint |
| HU-005 | 5 | Cerrada dentro del Sprint 1 |
| **Total** | **14** | **10 puntos entregados dentro del Sprint 1** |

- De los 14 puntos estimados en planning poker, **10 se entregaron dentro del
  Sprint 1**. Los otros 4 (HU-001 y HU-004) se cerraron después, sin sprint
  asignado. HU-005 fue la de mayor dispersión al estimar (votos de 3 a 8) y se
  dejó en 5 puntos tras aclarar su alcance (Daily 1).
- **HU-006 a HU-011 nunca se estimaron en puntos.** Las del Sprint 4 se
  estimaron por talla: dos L, una M y una XS.
- Como no hay horas registradas, la medida de esfuerzo real disponible es la
  actividad en el código:

![Commits por semana en main](../Gráficas/commits-por-semana.png)

- Hay **116 commits** en `main`. El esfuerzo se concentró en tres semanas:
  la del 14 de septiembre (37 commits), la del 21 de septiembre (26) y la del
  19 de octubre (24).
- Desde el 23 de octubre la actividad bajó: **12 commits en tres semanas**
  (3 entre el 2 y el 8 de noviembre, 3 entre el 9 y el 15, y 6 entre el 16 y
  el 20), todos de calidad y documentación, no de funciones.
- Entre el 10 de agosto y el 6 de septiembre no hubo commits, aunque el
  Sprint 1 se cerró en ese periodo: ese trabajo fue de diseño y
  documentación, que no siempre pasa por el repositorio.

---

## Calidad y pruebas

Es lo nuevo desde el reporte anterior.

### Plan de pruebas

Se escribió un caso de prueba por historia (HU-001 a HU-015). El resultado
esperado sale del criterio de aceptación de cada historia, no del
comportamiento actual del programa. Todo está registrado en Azure DevOps y el
detalle en [Pruebas/Plan-de-Pruebas.md](Pruebas/Plan-de-Pruebas.md).

| Ejecución | Pasan | Fallan | Bloqueado |
|---|---:|---:|---:|
| 27 de octubre | 11 | 4 | 0 |
| 17 de noviembre (regresión) | 11 | 3 | 1 |

La regresión se hizo porque el 3 de noviembre la limpieza de SonarCloud tocó
código de producción (validación de correos, redirección del login y armado de
la petición al modelo). **Ningún caso que pasaba antes dejó de pasar.**

| Bug | Problema | Estado |
|---|---|---|
| 78 | Las respuestas del formulario se pierden al recargar la página | Abierto |
| 79 | 3 de los 96 proyectos quedan sin grupo en el clustering | Abierto |
| 80 | La clasificación de intención de compra tiene 2 categorías en vez de 3 | Abierto |
| 81 | Falta la función `buscar_resultados` en la base de producción | Abierto, y la base está pausada |

El caso CP-014 (leads por teléfono y correo) pasó de **fallar a bloqueado**:
no se pudo ejecutar porque la base de producción estaba pausada.

### SonarCloud

| Medida | Valor |
|---|---|
| Umbral de calidad | **Aprobado** |
| Problemas abiertos | **0** |
| Problemas de seguridad abiertos | 0, calificación A |
| Problemas cerrados en total | 82 (corregidos o descartados como falsos positivos) |
| Problemas de seguridad cerrados en los últimos 30 días | 30 |
| Duplicación de código | 17,3 % |
| Cobertura de pruebas | Sin datos todavía |
| Tamaño analizado | unas 150.000 líneas |

La duplicación y la falta de cobertura son lo que sigue pendiente de esta
medición. Las capturas están en [Capturas-SonarCloud/](Capturas-SonarCloud/).

### Deuda técnica

El [registro de deuda técnica](Registro-de-Deuda-Tecnica-Leadify.pdf) del
10 de noviembre lista **12 ítems y estima 165 horas** para pagarlos. Los de
mayor interés:

- El motor de recomendación no tiene pruebas unitarias, solo una prueba de
  humo (24 h).
- El frontend está concentrado en archivos de más de 2.000 líneas (40 h).
- Funciones demasiado largas en el motor (20 h).

---

## Qué se puede medir hoy

Cifras verificadas contra el sistema, no estimadas:

| Métrica | Valor |
|---|---|
| Proyectos en el catálogo de compra | 96, de 4 constructoras |
| Inmuebles en el catálogo de arriendo | 93 (30 viviendas, 32 oficinas, 31 bodegas) |
| Proyectos recomendados por consulta de compra | 18 |
| Sectores del grafo de cercanía (barrios) | 1.164, con distancia real en km |
| Tiempo de respuesta del modelo (servicio activo) | ~1 segundo |
| Tiempo de respuesta (servicio dormido, primera consulta del día) | 30–60 segundos |
| Casos del plan de pruebas que pasan (17/11) | 11 de 15 |
| Tablas de leads en producción | No verificable: el proyecto de Supabase está pausado |
| Pruebas automáticas del login (frontend, 17/11) | 27, todas pasan |
| Pruebas del backend (login, arriendo y llamada, 17/11) | 9, todas pasan, más la prueba de humo del motor |
| Verificaciones del repositorio (`Script/`, 17/11) | Las dos que se corrieron en la regresión (catálogo y enlaces) pasan; se corren a mano |
| Problemas abiertos en SonarCloud | 0 |

---

## Uso de GitHub

**Issues:** las 15 historias, cada una con descripción, criterios de
aceptación, etiquetas de tipo y prioridad, y responsable.

![Issues del repositorio](Capturas-GitHub/issues.png)

**Milestones:** un milestone por sprint, del Sprint 1 al Sprint 4.

![Milestones del repositorio](Capturas-GitHub/milestones.png)

**Ramas:** `main`, `develop`, una rama por historia de usuario y
`login-y-arriendo` para el trabajo del Sprint 4.

![Ramas del repositorio](Capturas-GitHub/ramas.png)

**Commits:** el historial de `main`.

![Commits de main](Capturas-GitHub/commits.png)

> Las cuatro capturas son del corte del 23 de octubre y no se volvieron a
> tomar. Los números de arriba (116 commits, issues, milestones) sí están al
> día.

---

## Problemas encontrados y cómo se resolvieron

Ningún proyecto de este tamaño llega sin tropiezos. Estos son los que
tuvimos, cómo se resolvieron, y cuáles siguen abiertos:

### Resueltos

**Pérdida accidental de historial de código (dos veces).** Un `force-push`
de un integrante sobrescribió sin querer 81 commits del repositorio
compartido —incluida la verificación automática, la guía de usuario, las
capturas del formulario y parte del trabajo del modelo—. Se recuperó **sin
perder el trabajo de nadie**, combinando las dos historias en vez de forzar
una encima de la otra. No volvió a pasar desde entonces.

**El motor de recomendación no estaba conectado en producción.** El
formulario llevaba un tiempo calculando resultados con un motor de reglas
local, aproximado, en vez de con el modelo real. Se encontró la causa (el
archivo de despliegue estaba en la carpeta equivocada para que Render lo
leyera) y quedó corregido y verificado con datos reales.

**La llamada apuntaba al backend de otro proyecto.** Se creó un flujo de Dapta
propio de Leadify y el endpoint `POST /api/llamar` pasó a vivir en el backend
de Leadify (Daily 10).

**Créditos agotados en el servicio de llamadas (Dapta).** Durante las
pruebas se acabó el saldo gratuito. Se creó una cuenta y un flujo nuevos, se
reconectaron las credenciales, y se confirmó que la llamada se dispara
correctamente de extremo a extremo.

**Las rutas del motor dependían de la estructura vieja del repositorio.** Se
centralizaron en `Model/rutas.py`, para cambiarlas en un solo lugar
(Daily 6).

**Render no permite enviar correos en el plan gratuito.** Eso descartaba la
confirmación de correo al crear una cuenta. Se decidió que las cuentas de
empresa queden activas al crearlas, sin confirmación ni revisión manual
(Daily 11).

**Los leads se identificaban por cédula.** El formulario dejó de pedirla y
ahora identifica a cada persona por teléfono y correo. Los registros
anteriores no se podían pasar a la llave nueva sin adivinar, porque un mismo
teléfono aparecía con varias cédulas, así que la migración los archiva en un
esquema cerrado en vez de borrarlos (Daily 12).

**Avisos de calidad del código en SonarCloud.** El análisis encontró
problemas como rutas por consola sin validar, expresiones regulares con
solapamiento, una redirección del login sin límite de origen y datos de la
petición en el registro. La limpieza del 3 de noviembre (tres commits) cerró
los últimos y hoy el umbral de calidad está aprobado, con 0 problemas abiertos
y 82 cerrados en total. Como la limpieza tocó código de producción, se repitió
el plan de pruebas completo y no rompió nada.

### Abiertos — requieren una decisión o una acción del equipo

**La base de datos de producción está pausada.** El plan gratuito de Supabase
pausa el proyecto tras una semana sin uso, y es **la segunda vez**: ya había
pasado en octubre y se reactivó el 20 de octubre. Hoy la dirección
del proyecto ni siquiera se resuelve. Mientras siga así, no se guardan leads
ni se recuperan resultados. **Acción:** reactivar el proyecto, y decidir si se
agenda una consulta periódica para que no se pause o se pasa a un plan que no
lo haga. Es lo más urgente antes de cualquier demostración.

**Falta activar el Sprint 4 en producción.** Hay que aplicar las migraciones
de `Database/migraciones/` en Supabase y configurar `DATABASE_URL` en Render.
Además, el servicio de Render desplegado hoy no expone las rutas de cuentas
(`/api/cuentas` y `/api/sesion`): corre una versión anterior a la del
repositorio y hay que volver a desplegarlo. Hasta entonces no se pueden crear
cuentas.

**Cuatro bugs abiertos del plan de pruebas** (78 a 81, tabla de arriba):
recargar la página pierde las respuestas, tres proyectos quedan sin grupo en
el clustering, la intención de compra solo tiene dos categorías en vez de tres
y falta una función en la base de producción.

**El formulario en local escribe en la base de producción.** La configuración
usa la misma URL de Supabase en `localhost` que en producción. Cuando la base
vuelva a estar activa, cada prueba local guardaría leads de prueba entre los
reales. Conviene separar un entorno de pruebas.

**La protección de la rama principal está desactivada.** Tras el incidente
del `force-push` se activó una protección que lo habría evitado; luego se
desactivó a pedido del equipo. Sigue desactivada hoy, así que `main` puede
volver a sobrescribirse sin darse cuenta y se pueden subir cambios sin
revisión. **Recomendación:** reactivarla antes de la entrega final.

**No hay verificación automática en GitHub.** El 17 de noviembre se agregó un
flujo que corría las pruebas con cobertura y el análisis de SonarCloud, y se
retiró ese mismo día. Hoy las pruebas y las comprobaciones
de `Script/` se corren a mano, y por eso SonarCloud todavía no tiene datos de
cobertura.

**Las ramas de cada historia no tienen commits propios.** Existe una rama por
historia, pero todas apuntan al mismo commit y van 55 commits detrás de
`main`; el trabajo se hizo directamente en `main` y en `login-y-arriendo`.

**No hay recuperación de contraseña.** Sin envío de correos, quien olvide su
contraseña no puede recuperarla por su cuenta. Está asumido por la limitación
del plan gratuito de Render.

**El plan gratuito del servicio de recomendación se "duerme".** Tras 15
minutos sin uso, la primera consulta del día tarda entre 30 y 60 segundos en
responder — no es un error, es la condición del plan sin costo. El sistema
ya tiene una red de seguridad (cae a un motor local aproximado si el
servicio no responde a tiempo), pero para una demostración en vivo conviene
despertarlo un par de minutos antes.

**El catálogo de arriendo depende del formato de Fincaraíz.** Si el portal
cambia sus páginas, el scraper deja de funcionar. El catálogo generado queda
versionado en el repositorio como respaldo (Daily 14).

**Deuda técnica por pagar.** 12 ítems y unas 165 horas, además de una
duplicación de código del 17,3 % y la ausencia de pruebas unitarias del motor
(ver [Calidad y pruebas](#calidad-y-pruebas)).

**El desglose de lenguajes de GitHub no refleja el código real.** Hoy GitHub
muestra solo PL/pgSQL y Python, aunque el repositorio también tiene
JavaScript, TypeScript y CSS. Es un problema cosmético tras las reescrituras
de historial; no afecta el funcionamiento de nada.

---

## Pendiente para la siguiente entrega

- Reactivar el proyecto de Supabase y evitar que se vuelva a pausar
- Aplicar las migraciones de la base, configurar `DATABASE_URL` y volver a
  desplegar el servicio de Render con las rutas de cuentas
- Corregir los bugs 78 a 81 y repetir los casos CP-004, CP-006, CP-009 y
  CP-014
- Validar con el Product Owner y cerrar HU-012 a HU-015
- Cerrar formalmente HU-010 con la evidencia de las pruebas ya realizadas
- Poner fecha de fin al Sprint 4 y asignar sprint a HU-001 y HU-004
- Estimar en puntos las historias que no lo están y registrar horas reales
- Reactivar la protección de la rama `main` y decidir si se vuelve a poner la
  verificación automática en GitHub
- Separar el entorno de pruebas del de producción en la configuración del
  formulario
- Retomar las capturas de GitHub y las gráficas en cada corte
- Organigrama visual del equipo
