# Plan de pruebas

**Fecha de ejecución:** 27 de octubre de 2026, sobre la versión de `main` de ese día
**Regresión:** 17 de noviembre de 2026, sobre `main` en el commit `e004620`
**Registro en Azure DevOps:** 17 de noviembre de 2026
**Curso:** Fundamentos de Ingeniería de Software · Pruebas de Software I

---

## Resumen

Se escribió un caso de prueba por cada historia de usuario (HU-001 a HU-015).
El resultado esperado de cada caso sale del criterio de aceptación de su
historia, no del comportamiento actual del programa.

**Resultado del 27/10: 11 casos pasaron y 4 fallaron, de 15.** Cada fallo
tiene un bug abierto.

**Regresión del 17/11: 11 pasan, 3 siguen fallando y 1 quedó bloqueado.** La
limpieza de SonarCloud del 3/11 no rompió ningún caso que antes pasaba. El
detalle está en [Regresión del 17/11/2026](#regresión-del-17112026).

El detalle completo de cada caso (precondiciones, pasos, datos de entrada,
resultado esperado y resultado obtenido) está en
[Casos-de-Prueba-Leadify.pdf](Casos-de-Prueba-Leadify.pdf).

## Dónde está en Azure DevOps

Todo vive en el proyecto
[`tfsker / Proyecto-Leadify`](https://dev.azure.com/tfsker/Proyecto-Leadify).
Los enlaces solo abren para los integrantes de la organización.

- **Plan de pruebas:** [Plan de pruebas - Leadify](https://dev.azure.com/tfsker/Proyecto-Leadify/_testPlans/execute?planId=61&suiteId=62)
  (plan 61), con los 15 casos y dos ejecuciones registradas: la del 27/10 y
  la regresión del 17/11.
- **Casos de prueba:** work items 12 a 26 (tipo *Test Case*), con sus pasos.
- **Historias de usuario:** work items 63 a 77. Cada historia queda
  *probada por* su caso (enlace *Tested By*).
- **Bugs:** work items 78 a 81, enlazados al caso que los encontró y a su
  historia.

## Casos y resultados

| Caso | Qué valida | Historia | Resultado | Bug |
|---|---|---|---|---|
| [CP-001](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/12) | Las preguntas del cuestionario alimentan el contrato del perfil | [HU-001](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/63) Definición de preguntas | Pasó | |
| [CP-002](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/13) | El cuestionario avanza en el orden definido | [HU-002](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/64) Diseño del cuestionario visual | Pasó | |
| [CP-003](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/14) | La interfaz mantiene la consistencia en los tamaños de pantalla | [HU-003](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/65) Diseño de la landing gamificada | Pasó | |
| [CP-004](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/15) | Las respuestas se mantienen al recargar la página | [HU-004](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/66) Integración de la landing gamificada | **Falló** | [78](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/78) |
| [CP-005](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/16) | El sistema identifica las características principales del perfil | [HU-005](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/67) Construcción del perfil de vivienda ideal | Pasó | |
| [CP-006](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/17) | Cada vivienda del catálogo queda asignada a un grupo | [HU-006](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/68) Implementación del clustering de viviendas | **Falló** | [79](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/79) |
| [CP-007](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/18) | Cada vivienda recibe un porcentaje de Match entre 0 % y 100 % | [HU-007](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/69) Cálculo del porcentaje de Match | Pasó | |
| [CP-008](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/19) | La llamada se inicia con la información del cuestionario | [HU-008](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/70) Implementación de llamada automática | Pasó | |
| [CP-009](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/20) | Se asigna una categoría de intención de compra: alta, media o baja | [HU-009](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/71) Clasificación de intención de compra | **Falló** | [80](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/80) |
| [CP-010](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/21) | El flujo de compra se completa hasta el Match y la clasificación | [HU-010](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/72) Pruebas de integración del flujo completo | Pasó | |
| [CP-011](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/22) | La aplicación está desplegada y responde en el entorno definido | [HU-011](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/73) Despliegue y documentación del sistema | Pasó | |
| [CP-012](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/23) | Crear una cuenta válida la deja activa y entra a la cuenta | [HU-012](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/74) Login de empresas (crear cuenta y entrar) | Pasó | |
| [CP-013](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/24) | Arrendar una vivienda usa presupuesto, preferencias y estilo de vida | [HU-013](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/75) Recorrido de arriendo en el formulario | Pasó | |
| [CP-014](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/25) | La base de producción identifica al lead por teléfono y correo | [HU-014](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/76) Leads identificados por teléfono y correo | **Falló** | [81](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/81) |
| [CP-015](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/26) | La raíz del sitio abre directo el registro del formulario | [HU-015](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/77) Entrada directa al formulario e identidad de Leadify | Pasó | |

## Regresión del 17/11/2026

El 3/11 entró la corrección de los avisos de SonarCloud (commits `c86a7eb`,
`65cb1e4` y `61dbaea`), que tocó la validación de correos, la redirección del
login y el armado de la petición al modelo. Por eso se repitieron los 15 casos
sobre `main` en el commit `e004620`.

| Caso | 27/10 | 17/11 | Qué se obtuvo el 17/11 |
|---|---|---|---|
| CP-001 | Pasó | Pasó | La petición lleva los seis campos del contrato, más las zonas comunes. |
| CP-002 | Pasó | Pasó | Las 8 preguntas salen en el orden definido. |
| CP-003 | Pasó | Pasó | Sin desplazamiento horizontal a 1366 px ni a 390 px, en el formulario y en el login. |
| CP-004 | Falló | **Falló** | Tras F5 vuelve a «Cuéntanos quién eres» con todo vacío. |
| CP-005 | Pasó | Pasó | El perfil devuelto coincide con lo declarado. |
| CP-006 | Falló | **Falló** | Los proyectos 83, 92 y 93 siguen sin grupo. |
| CP-007 | Pasó | Pasó | 18 proyectos por perfil, todos entre 0 % y 100 %. |
| CP-008 | Pasó | Pasó | Llamada simulada (`mock_enqueued`) con los 19 campos. |
| CP-009 | Falló | **Falló** | Siguen existiendo solo 2 categorías. |
| CP-010 | Pasó | Pasó | Match, llamada simulada y pantalla final con su clasificación. |
| CP-011 | Pasó | Pasó | Render y Vercel responden 200. |
| CP-012 | Pasó | Pasó | La cuenta se crea activa y entra a `/inicio/`. |
| CP-013 | Pasó | Pasó | 9 preguntas de arriendo y 30 inmuebles con su porcentaje. |
| CP-014 | Falló | **Bloqueado** | No se pudo ejecutar: el proyecto de Supabase de producción está pausado. |
| CP-015 | Pasó | Pasó | La raíz abre directo en «Cuéntanos quién eres». |

Las pruebas automáticas del repositorio también pasan:

| Prueba | Resultado |
|---|---|
| `npm run test:auth` (login) | 27 de 27 |
| `npm run build` | Compila |
| `python pruebas/prueba_humo.py` (motor) | Todo en orden |
| `python pruebas/prueba_acceso.py` (login, arriendo y llamada) | 9 de 9 |
| `python Script/verificar_catalogo.py` | El catálogo corresponde al código (96 proyectos) |
| `python Script/verificar_enlaces.py` | Todos los enlaces resuelven |

### Hallazgos de la regresión

- **La base de producción está pausada.** El proyecto `leadify` de Supabase
  aparece como inactivo y su dominio no resuelve. Mientras siga así, en
  producción no se guardan leads ni se pueden buscar resultados. Hay que
  reactivarlo antes de aplicar la migración del bug 81.
- **El formulario en local escribe en la base de producción.**
  [`config.js`](../../Demo/frontend/public/experiencia/js/config.js) usa la
  misma URL de Supabase en `localhost` que en producción, y el flujo llama a
  `guardar_consulta` y `marcar_interes`. En esta regresión esas llamadas se
  bloquearon en el navegador. Cuando la base vuelva a estar activa, cada
  prueba local guardaría leads de prueba en producción.

## Bugs abiertos

| Bug | Problema | Qué se obtuvo |
|---|---|---|
| [78](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/78) | Las respuestas del formulario se pierden al recargar la página | Tras recargar, el formulario vuelve a «Cuéntanos quién eres» y hay que responder de nuevo. |
| [79](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/79) | 3 de los 96 proyectos del catálogo quedan sin grupo en el clustering | 93 proyectos tienen grupo; 3 quedan con el perfil dominante vacío. |
| [80](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/80) | La clasificación de intención de compra usa 2 categorías en vez de 3 | Solo existen «Listo para asesor» y «En maduración». |
| [81](https://dev.azure.com/tfsker/Proyecto-Leadify/_workitems/edit/81) | Falta la función `buscar_resultados(p_telefono, p_correo)` en producción | Responde 404 (PGRST202): la migración `20261020120000` no está aplicada en Supabase. El 17/11, además, el proyecto de Supabase está pausado. |

## Entornos

- **Local:** frontend en `localhost:5173`, backend en `localhost:8100`, llamada
  de Dapta simulada (no se llamó a nadie). En la regresión el backend corrió
  con `ACCESO_EN_MEMORIA=1`, con cuentas que se borran al apagarlo.
- **Producción:** <https://leadify-kappa.vercel.app>,
  <https://leadify-gmqj.onrender.com> y Supabase. Solo se usó para CP-011,
  CP-014 y CP-015; en CP-014 la consulta fue de solo lectura.
