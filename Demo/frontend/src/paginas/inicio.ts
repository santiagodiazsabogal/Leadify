/* LEADIFY — /inicio/: la página después de entrar. Sin sesión → /acceso/?volver=/inicio/.
 * Las cuentas nacen aprobadas; "pendiente" o "rechazada" solo existen si alguien las cambia en la base. */

import './estilos.css';
import { proveedor, type Cuenta } from '../auth/index.ts';
import { olvidarGoogle } from '../auth/google.ts';
import { rutaDeAcceso, RUTA_ACCESO } from '../auth/sesion.ts';
import { logoHtml } from './marca.ts';
import { esc, ic, montarHerramientasDePrueba, ocupado } from './ui.ts';

const p = proveedor();
const raiz = document.getElementById('app') as HTMLElement;

const CORREO_CONTACTO = 'equipo@leadify.co';

function iniciales(usuario: string): string {
  const partes = usuario.split(/[-._]+/).filter(Boolean);
  return ((partes[0]?.[0] || '') + (partes[1]?.[0] || partes[0]?.[1] || '')).toUpperCase();
}

function pantallaTarjeta(c: Cuenta): string {
  const pendiente = c.estado === 'pendiente';
  return (
    `<div class="centrada"><header class="cabeza">${logoHtml()}</header><main class="tarjeta entra"><div class="estado">` +
    (pendiente
      ? `<div class="icono navy">${ic('reloj')}</div><h1 tabindex="-1">Tu cuenta está en revisión</h1>` +
        `<p class="sub">Escríbenos a <a href="mailto:${CORREO_CONTACTO}">${CORREO_CONTACTO}</a> desde <b>${esc(c.correo)}</b> y la activamos.</p>`
      : `<div class="icono">${ic('cerrado')}</div><h1 tabindex="-1">Tu cuenta no fue aprobada</h1>` +
        `<p class="sub">Si crees que es un error, escríbenos a <a href="mailto:${CORREO_CONTACTO}">${CORREO_CONTACTO}</a> desde <b>${esc(c.correo)}</b>.</p>`) +
    `<button class="boton secundario" type="button" id="salir">Salir</button></div></main></div>`
  );
}

function pantallaBienvenida(c: Cuenta): string {
  const tipo = c.tipo === 'constructora' ? 'Constructora' : c.tipo === 'inmobiliaria' ? 'Inmobiliaria' : 'Cuenta activa';
  return (
    `<div class="app"><header class="barra">${logoHtml(true)}` +
    `<div class="usuario"><span class="avatar" aria-hidden="true">${esc(iniciales(c.usuario))}</span><span class="nombre">${esc(c.usuario)}</span>` +
    `<button class="salir" type="button" id="salir">Salir</button></div></header>` +
    `<main class="cuerpo"><div class="bienvenida"><span class="etiqueta">${esc(tipo)}</span>` +
    `<h1 tabindex="-1">Hola, ${esc(c.usuario)}</h1>` +
    `<p>Ya tienes acceso a Leadify. Mira el formulario que viven tus clientes, para comprar o para arrendar.</p>` +
    `<p><a class="boton" href="/experiencia/index.html?marca=leadify">Abrir el formulario</a></p>` +
    `<p class="pronto-titulo">Próximamente</p><ul class="pronto">` +
    `<li>${ic('personas')}Tus leads calificados</li><li>${ic('telefono')}Llamadas de Manuela</li><li>${ic('grafica')}Resultados</li></ul>` +
    `</div></main></div>`
  );
}

async function arrancar(): Promise<void> {
  const sesion = await p.sesionActual().catch(() => null);
  if (!sesion) return location.replace(rutaDeAcceso(location.pathname));
  const c = sesion.cuenta;
  raiz.innerHTML = c.estado === 'aprobada' ? pantallaBienvenida(c) : pantallaTarjeta(c);
  document.title = (c.estado === 'aprobada' ? 'Inicio' : c.estado === 'pendiente' ? 'Cuenta en revisión' : 'Cuenta no aprobada') + ' · Leadify';
  (raiz.querySelector('h1') as HTMLElement).focus();
  const salir = document.getElementById('salir') as HTMLButtonElement;
  salir.addEventListener('click', async () => {
    await ocupado(salir, () => p.salir());
    olvidarGoogle();
    location.assign(RUTA_ACCESO);
  });
  montarHerramientasDePrueba(p);
}

void arrancar();
