// Configuración de entorno para este front vanilla (sin build step, sin
// bundler => sin process.env ni import.meta.env nativos). Es el único sitio
// donde se edita a mano a dónde apunta la app.
//
// Se carga ANTES que js/leadify.js en index.html.
window.GDF_CONFIG = {
  // El servicio del modelo de recomendación: backend/api/app.py, YA
  // desplegado en Render (ver render.yaml) y con CORS abierto a propósito.
  // Expone /api/recomendar y agrega las fotos de cada proyecto (relativas a
  // ESTE MISMO front, no al backend — ver el comentario de _fotos_de() en
  // app.py y de urlDeFoto() en recommender.js).
  //
  // Si el modelo no está levantado, integracion/fake_leadify.py habla el mismo
  // contrato y recomienda sobre el MISMO catálogo real (los 96 proyectos de
  // Bogotá) con sus fotos. No es el modelo —son reglas— y lo dice en el campo
  // `motor` de cada respuesta, que sale por consola:
  //   python integracion/fake_leadify.py     -> escucha en el mismo puerto
  // En localhost apunta al backend de tu máquina (`uvicorn api.app:app --port 8100`
  // desde Demo/backend); en cualquier otro host, al servicio de Render.
  LEADIFY_BASE:
    location.hostname === 'localhost' || location.hostname === '127.0.0.1'
      ? 'http://localhost:8100/api'
      : 'https://leadify-gmqj.onrender.com/api',

  // De dónde salen los proyectos recomendados (ver js/recommender.js):
  //   'leadify' -> las 7 respuestas viajan al modelo, que devuelve el Top 6 con
  //               su compatibilidad y las fotos de cada proyecto.
  //   'local'  -> solo el motor de reglas de js/matching.js, sin tocar la red.
  //               Es el respaldo cuando el servicio no responde, y se marca
  //               siempre como aproximado para no engañar a nadie.
  RECOMMENDER: 'leadify',

  // MODO DEMO SIN RED. En true la app no llama al modelo en ningún momento y
  // las recomendaciones salen del motor local. Existe para la versión de UN
  // SOLO ARCHIVO (tools/empaquetar_demo.py), pensada para compartir por link:
  // ahí la política de seguridad del visor bloquea cualquier petición externa.
  // El plan gratuito de Render duerme el servicio tras un rato sin uso: la
  // primera consulta del día puede tardar ~20 s en despertar (se ve como
  // "Calculando tu match..." un rato largo, no como un error).
  SIN_BACKEND: false,

  // El mismo backend (Demo/backend/api/app.py) que LEADIFY_BASE, sin el /api.
  // Va aparte porque SIN_BACKEND solo apaga el cálculo de recomendaciones, no
  // la llamada de Manuela: esa necesita la API key de Dapta, que nunca puede
  // viajar al navegador.
  DAPTA_LLAMADA_BASE:
    location.hostname === 'localhost' || location.hostname === '127.0.0.1'
      ? 'http://localhost:8100'
      : 'https://leadify-gmqj.onrender.com',

  // El número al que escribe el botón "WhatsApp" de la tarjeta elegida, en
  // formato internacional y sin "+" (57 + celular de 10 dígitos). Vacío, el
  // enlace abre WhatsApp con el mensaje listo y la persona elige el contacto.
  WHATSAPP_NUMERO: '',

  // Base de datos persistente de leads (ver js/datos.js y
  // supabase/migrations/). SIEMPRE la clave PUBLICABLE/anon -- nunca la
  // service_role -- porque viaja al navegador. Es segura de exponer: las
  // tablas están cerradas (RLS sin políticas) y esta clave solo puede
  // ejecutar las 4 funciones SECURITY DEFINER de la migración. Vacías, la
  // app funciona igual: js/datos.js nunca bloquea el formulario si no hay
  // configuración o si Supabase no responde.
  // DATOS PERSONALES (design/login/REVISION_LEGAL.md y TEXTOS_AUTORIZACION_V2.md).
  // Marcas con un acuerdo firmado: solo con ellas el formulario con su marca (?marca=) guarda datos y
  // llama, con Leadify como encargado. Cualquier otra marca es SOLO una demostración: no guarda nada ni
  // llama. El backend tiene la misma lista en MARCAS_CON_ACUERDO.
  MARCAS_CON_ACUERDO: [],
  // Compartir el lead con la constructora dueña del proyecto (hoja "Antes de llamarte"). Apagado hasta
  // que haya empresas clientes con acuerdo: sin eso la hoja pediría permiso para compartir con empresas
  // que nunca recibirían el lead (Ariel, mensaje 2).
  COMPARTIR_CON_DUENOS: false,
  SUPABASE_URL: 'https://jovuwfqmxcxectjwmeqq.supabase.co',
  SUPABASE_ANON_KEY: 'sb_publishable_LTtDM90Kub2pNI7pjr6iuA_U_dQQMAi',
};
