/* LEADIFY — /acceso/: entrar y crear la cuenta de la empresa. La lógica vive en src/auth/; aquí solo pantalla.
 *
 * Vistas (el hash permite compartir el enlace): #entrar (por defecto) y #crear.
 * Sin confirmación de correo ni revisión: la cuenta queda activa al crearla y se entra en el acto.
 * Parámetro: ?volver=/ruta (a dónde ir al entrar).
 */

import './estilos.css';
import { ErrorAuth, googleClientId, proveedor } from '../auth/index.ts';
import { montarBotonGoogle } from '../auth/google.ts';
import { destinoSeguro } from '../auth/sesion.ts';
import { validarClave, validarCorreo, validarRegistro, validarUsuario } from '../auth/validacion.ts';
import { logoHtml } from './marca.ts';
import {
  $, avisoHtml, campoHtml, conectarMedidor, conectarOjos, errorCampo, ic, mensajeDeError, montarHerramientasDePrueba,
  ocupado, validarEnVivo, valor,
} from './ui.ts';

const RUTA_PRIVACIDAD = '/privacidad/';
const p = proveedor();
const params = new URLSearchParams(location.search);
const volver = destinoSeguro(params.get('volver'));

type Vista = 'entrar' | 'crear';
let vista: Vista = 'entrar';
let correoActual = '';

const raiz = document.getElementById('app') as HTMLElement;
raiz.innerHTML =
  `<div class="centrada"><header class="cabeza"><a href="/" aria-label="Leadify, ir al inicio">${logoHtml()}</a></header>` +
  `<main class="tarjeta" id="tarjeta"></main>` +
  `<p class="pie">Al continuar aceptas la <a href="${RUTA_PRIVACIDAD}">Política de privacidad</a> de Leadify.</p></div>`;
const tarjeta = $('#tarjeta');
conectarOjos(tarjeta);

// ---------------------------------------------------------------- plantillas
function selector(activa: 'entrar' | 'crear'): string {
  const b = (v: 'entrar' | 'crear', t: string) => `<button type="button" data-ir="${v}"${activa === v ? ' aria-current="page"' : ''}>${t}</button>`;
  return `<nav class="selector" aria-label="Entrar o crear cuenta">${b('entrar', 'Entrar')}${b('crear', 'Crear cuenta')}</nav>`;
}

function bloqueGoogle(): string {
  return googleClientId() ? `<div class="google" id="google"></div><div class="separador">o con tu correo</div>` : '';
}

const PLANTILLAS: Record<Vista, () => string> = {
  entrar: () =>
    selector('entrar') +
    `<h1 tabindex="-1">Bienvenido de nuevo</h1><p class="sub">Entra a la cuenta de tu empresa en Leadify.</p>` +
    bloqueGoogle() +
    `<form id="form" novalidate>` +
    campoHtml({ id: 'correo', etiqueta: 'Correo', tipo: 'email', autocomplete: 'username', placeholder: 'tu@empresa.com', valor: correoActual }) +
    campoHtml({ id: 'clave', etiqueta: 'Contraseña', tipo: 'password', autocomplete: 'current-password', placeholder: 'Tu contraseña' }) +
    `<div class="fila"><label class="casilla"><input type="checkbox" id="recordar" checked><span class="caja">${ic('check')}</span>Recordarme</label></div>` +
    `<div id="error-form"></div>` +
    `<button class="boton" type="submit" id="enviar">Entrar</button></form>` +
    `<p class="debajo">¿Tu empresa aún no tiene cuenta? <button type="button" class="enlace" data-ir="crear">Crear cuenta</button></p>`,

  crear: () =>
    selector('crear') +
    `<h1 tabindex="-1">Crea la cuenta de tu empresa</h1><p class="sub">Para constructoras e inmobiliarias. Queda activa al instante.</p>` +
    bloqueGoogle() +
    `<form id="form" novalidate>` +
    campoHtml({ id: 'usuario', etiqueta: 'Nombre de usuario', autocomplete: 'username', placeholder: 'Ej.: constructora-andes', ayuda: 'Minúsculas, números, puntos o guiones.' }) +
    campoHtml({ id: 'correo', etiqueta: 'Correo', tipo: 'email', autocomplete: 'email', placeholder: 'tu@empresa.com', valor: correoActual }) +
    campoHtml({ id: 'clave', etiqueta: 'Contraseña', tipo: 'password', autocomplete: 'new-password', placeholder: 'Mínimo 10 caracteres', medidor: true, ayuda: 'Una frase larga es más segura que símbolos raros.' }) +
    `<label class="casilla legal" id="acepto-caja"><input type="checkbox" id="acepto"><span class="caja">${ic('check')}</span>` +
    `<span>Acepto la <a href="${RUTA_PRIVACIDAD}" target="_blank" rel="noopener">Política de privacidad</a> y el tratamiento de mis datos.</span></label>` +
    `<div id="error-form"></div>` +
    `<button class="boton" type="submit" id="enviar">Crear cuenta</button></form>` +
    `<p class="debajo">¿Ya tienes cuenta? <button type="button" class="enlace" data-ir="entrar">Entrar</button></p>`,

};

// ---------------------------------------------------------------- navegación entre vistas
function ir(v: Vista, { enfocar = true, hash = true } = {}): void {
  // Lo escrito en "Correo" pasa a la vista siguiente.
  const actual = document.getElementById('correo') as HTMLInputElement | null;
  if (actual?.value) correoActual = actual.value.trim();
  vista = v;
  tarjeta.innerHTML = PLANTILLAS[v]();
  tarjeta.classList.remove('entra');
  void tarjeta.offsetWidth;
  tarjeta.classList.add('entra');
  if (hash) history.replaceState(null, '', `${location.pathname}${location.search}${v === 'entrar' ? '' : '#' + v}`);
  document.title = (v === 'crear' ? 'Crear cuenta' : 'Entrar') + ' · Leadify';
  conectar();
  if (enfocar) $<HTMLElement>('h1', tarjeta).focus();
}

tarjeta.addEventListener('click', (e) => {
  const b = (e.target as HTMLElement).closest<HTMLElement>('[data-ir]');
  if (b) ir(b.dataset.ir as Vista);
});

window.addEventListener('hashchange', () => {
  const v = location.hash.slice(1);
  if ((v === 'crear' || v === '' || v === 'entrar') && v !== vista) ir((v || 'entrar') as Vista);
});

function errorFormulario(texto: string): void {
  const caja = document.getElementById('error-form');
  if (caja) caja.innerHTML = texto ? avisoHtml(texto, 'error') : '';
}

function irA(destino: string): void {
  location.assign(destino);
}

// ---------------------------------------------------------------- comportamiento de cada vista
function conectar(): void {
  const form = document.getElementById('form') as HTMLFormElement | null;
  const enviar = document.getElementById('enviar') as HTMLButtonElement | null;

  if (vista === 'entrar' || vista === 'crear') void montarGoogle();

  if (vista === 'entrar' && form && enviar) {
    validarEnVivo('correo', () => validarCorreo(valor('correo')));
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      errorFormulario('');
      const errCorreo = validarCorreo(valor('correo'));
      const errClave = valor('clave') ? null : 'Escribe tu contraseña.';
      errorCampo('correo', errCorreo);
      errorCampo('clave', errClave);
      if (errCorreo || errClave) return void document.getElementById(errCorreo ? 'correo' : 'clave')?.focus();
      try {
        await ocupado(enviar, () => p.entrar({ correo: valor('correo'), clave: valor('clave'), recordar: (document.getElementById('recordar') as HTMLInputElement).checked }));
        irA(volver);
      } catch (err) {
        errorFormulario(mensajeDeError(err));
        (document.getElementById('clave') as HTMLInputElement).value = '';
      }
    });
  }

  if (vista === 'crear' && form && enviar) {
    validarEnVivo('usuario', () => validarUsuario(valor('usuario')));
    validarEnVivo('correo', () => validarCorreo(valor('correo')));
    validarEnVivo('clave', () => validarClave(valor('clave'), { usuario: valor('usuario'), correo: valor('correo') }));
    conectarMedidor('clave');
    const acepto = document.getElementById('acepto') as HTMLInputElement;
    acepto.addEventListener('change', () => document.getElementById('acepto-caja')?.classList.toggle('mal', false));
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      errorFormulario('');
      const datos = { usuario: valor('usuario'), correo: valor('correo'), clave: valor('clave') };
      const errores = validarRegistro(datos);
      (['usuario', 'correo', 'clave'] as const).forEach((c) => errorCampo(c, errores[c]));
      const primero = (['usuario', 'correo', 'clave'] as const).find((c) => errores[c]);
      if (primero) return void document.getElementById(primero)?.focus();
      if (!acepto.checked) {
        document.getElementById('acepto-caja')?.classList.add('mal');
        errorFormulario('Para crear la cuenta tienes que aceptar la Política de privacidad.');
        return void acepto.focus();
      }
      try {
        await ocupado(enviar, async () => {
          const r = await p.crearCuenta(datos);
          await p.entrar({ correo: r.correo, clave: datos.clave, recordar: true });
        });
        irA(volver);
      } catch (err) {
        if (err instanceof ErrorAuth && err.codigo === 'datos_invalidos') {
          (['usuario', 'correo', 'clave'] as const).forEach((c) => errorCampo(c, err.campos[c]));
        } else if (err instanceof ErrorAuth && err.codigo === 'correo_ocupado') {
          errorCampo('correo', err.message);
          document.getElementById('correo')?.focus();
        } else if (err instanceof ErrorAuth && err.codigo === 'usuario_ocupado') {
          errorCampo('usuario', err.message);
          document.getElementById('usuario')?.focus();
        } else {
          errorFormulario(mensajeDeError(err));
        }
      }
    });
  }
}

async function montarGoogle(): Promise<void> {
  const cont = document.getElementById('google');
  if (!cont) return;
  const montado = await montarBotonGoogle(cont, {
    clientId: googleClientId(),
    texto: vista === 'crear' ? 'signup_with' : 'signin_with',
    ancho: cont.clientWidth || 360,
    alRecibir: async ({ idToken, nonce }) => {
      try {
        const recordar = (document.getElementById('recordar') as HTMLInputElement | null)?.checked ?? true;
        await p.entrarConGoogle({ idToken, nonce, recordar });
        irA(volver);
      } catch (err) {
        errorFormulario(mensajeDeError(err));
      }
    },
    alFallar: () => {
      cont.nextElementSibling?.remove();
      cont.remove();
    },
  });
  if (!montado && cont.isConnected) {
    cont.nextElementSibling?.remove();
    cont.remove();
  }
}

// ---------------------------------------------------------------- arranque
async function arrancar(): Promise<void> {
  const sesion = await p.sesionActual().catch(() => null);
  if (sesion) return irA(volver);
  const inicial = location.hash.slice(1);
  ir(inicial === 'crear' ? 'crear' : 'entrar', { enfocar: false, hash: false });
  montarHerramientasDePrueba(p);
}

void arrancar();
