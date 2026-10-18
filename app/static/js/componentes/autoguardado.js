// Autoguardado (RF-04.6, RNF-06.1): manda al servidor cada cambio con fetch,
// sin que el usuario presione nada. Módulo ES reutilizable por cualquier
// formulario que tenga un endpoint JSON con la misma forma que el del cuestionario.
//
// - Un envío a la vez: los cambios que llegan mientras hay uno en curso se
//   juntan en el siguiente (el último valor de cada campo gana). Así dos
//   peticiones nunca se cruzan y un valor viejo no puede pisar a uno nuevo.
// - keepalive: el navegador termina el envío aunque se cierre la pestaña.
// - Sin conexión: el lote vuelve a la cola y se reintenta. Si el servidor lo
//   rechaza (400, 409...) no se reintenta, porque fallaría igual: se avisa.

const REINTENTO_MS = 3000;

/**
 * @param {object} opciones
 * @param {string} opciones.url        endpoint JSON (POST)
 * @param {string} opciones.token      token CSRF; viaja en el header X-CSRFToken
 * @param {object} opciones.base       campos que van en todos los envíos (ej. numero_control)
 * @param {(estado: string, detalle?: object) => void} opciones.alCambiarEstado
 *        estado: "guardando" | "guardado" | "sin-conexion" | "rechazado"
 */
export function crearAutoguardado({ url, token, base, alCambiarEstado }) {
  let pendientes = {};
  let enviando = false;
  let temporizador = null;

  const hayPendientes = () => Object.keys(pendientes).length > 0;

  async function enviar() {
    if (enviando || !hayPendientes()) return;
    enviando = true;
    clearTimeout(temporizador);
    const lote = pendientes;
    pendientes = {};
    alCambiarEstado("guardando");

    let sinConexion = false;
    try {
      const respuesta = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": token },
        body: JSON.stringify({ ...base, ...lote }),
        credentials: "same-origin",
        keepalive: true,
      });
      // Un error de CSRF devuelve HTML, no JSON: por eso el catch
      const datos = await respuesta.json().catch(() => ({}));
      alCambiarEstado(respuesta.ok ? "guardado" : "rechazado", { status: respuesta.status, ...datos });
    } catch {
      // Red caída: el lote vuelve a la cola sin pisar cambios más nuevos
      sinConexion = true;
      pendientes = { ...lote, ...pendientes };
      alCambiarEstado("sin-conexion");
      temporizador = setTimeout(enviar, REINTENTO_MS);
    } finally {
      enviando = false;
    }
    // Lo que se acumuló mientras se enviaba sale en el siguiente lote
    if (!sinConexion) enviar();
  }

  return {
    /** Agrega campos al siguiente envío, ej. { respuesta_5: "si", comentario_5: "" } */
    agregar(campos) {
      Object.assign(pendientes, campos);
      enviar();
    },
    /** true si hay cambios en cola que todavía no salieron (ej. sin conexión).
     *  Lo que ya está en vuelo no cuenta: keepalive lo termina aunque se cierre la pestaña. */
    sinEnviar: () => hayPendientes(),
  };
}
