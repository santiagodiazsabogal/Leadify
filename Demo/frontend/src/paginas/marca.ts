/* LEADIFY — El logo del login: la palabra "Leadify" con el punto en coral. */

/** El logo completo. `chico` = versión de la barra superior. */
export function logoHtml(chico = false): string {
  return `<span class="logo${chico ? ' chico' : ''}" role="img" aria-label="Leadify">Leadify<span class="punto" aria-hidden="true">.</span></span>`;
}
