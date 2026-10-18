// Página del cuestionario (templates/cuestionario/control.html).
// Es un módulo ES: se carga con <script type="module">, que el navegador
// ejecuta cuando el HTML ya está listo, y puede importar componentes.
//
// 1. Progreso en vivo (RF-04.4): barra del control actual y barra global.
// 2. Autoguardado (RF-04.6, RNF-06.1): cada respuesta se guarda al marcarla y
//    cada comentario al dejar de escribir, sin presionar ningún botón. El envío
//    normal del formulario sigue funcionando como respaldo (sin JavaScript).
// Los datos del servidor llegan como atributos data-* (sin Jinja dentro del JS).
import { pintarBarra } from "../componentes/progreso.js";
import { crearAutoguardado } from "../componentes/autoguardado.js";

const ESPERA_COMENTARIO_MS = 800;

const form = document.getElementById("form-cuestionario");

if (form) {
  // ===== 1. Progreso en vivo =====
  const grupos = form.querySelectorAll(".sa-toggle[data-question]");
  const totalControl = grupos.length;
  const barraControl = document.getElementById("ctrl-progress");
  const barraGlobal = document.getElementById("global-progreso");
  const totalGlobal = Number(barraGlobal.dataset.total);
  // Respondidas en los DEMÁS controles según la BD; las de este se cuentan en vivo
  const respondidasOtros = Number(barraGlobal.dataset.otros);

  const contarRespondidas = () =>
    [...grupos].filter((g) => g.querySelector(".sa-toggle__input:checked")).length;

  function actualizar() {
    const n = contarRespondidas();
    pintarBarra(barraControl, n, totalControl);
    document.getElementById("ctrl-meta").textContent =
      totalControl + " preguntas · " + n + " respondidas";
    document.getElementById("footer-count").textContent =
      n + " / " + totalControl + " respondidas";

    const g = respondidasOtros + n;
    const pct = pintarBarra(barraGlobal, g, totalGlobal);
    document.getElementById("global-count").textContent =
      g + " de " + totalGlobal + " respondidas · " + pct + "%";
  }

  // "change" burbujea: un solo listener en el form atiende todos los radios
  form.addEventListener("change", actualizar);
  actualizar();

  // ===== 2. Autoguardado (solo si la sesión admite cambios) =====
  if (form.dataset.editable === "true") {
    const indicador = document.getElementById("estado-guardado");
    const pasoActual = document.querySelector('.sa-step[aria-current="step"]');
    let ocultarIndicador = null;

    function mostrarEstado(texto, tipo = "", autoOcultar = false) {
      clearTimeout(ocultarIndicador);
      indicador.textContent = texto;
      indicador.className = "sa-guardado" + (tipo ? " sa-guardado--" + tipo : "");
      if (autoOcultar) ocultarIndicador = setTimeout(() => (indicador.textContent = ""), 2500);
    }

    // El paso del mapa (RF-04.7) refleja lo guardado: se actualiza tras cada guardado
    function actualizarPaso() {
      if (!pasoActual) return;
      const n = contarRespondidas();
      const estado = n === totalControl ? "completo" : n > 0 ? "parcial" : "pendiente";
      pasoActual.classList.remove("sa-step--pendiente", "sa-step--parcial", "sa-step--completo");
      pasoActual.classList.add("sa-step--" + estado);
      const etiqueta = pasoActual.getAttribute("aria-label").replace(/ — .*$/, ` — ${estado} (${n} de ${totalControl})`);
      pasoActual.setAttribute("aria-label", etiqueta);
      pasoActual.setAttribute("title", etiqueta);
    }

    const auto = crearAutoguardado({
      url: form.dataset.autoguardarUrl,
      token: form.elements.csrf_token.value,
      base: { numero_control: Number(form.elements.numero_control.value) },
      alCambiarEstado(estado, detalle = {}) {
        if (estado === "guardando") mostrarEstado("Guardando…");
        else if (estado === "sin-conexion") mostrarEstado("Sin conexión: se reintentará", "aviso");
        else if (estado === "rechazado") mostrarEstado(detalle.error || "No se pudo guardar. Recarga la página.", "error");
        else if (detalle.comentarios_sin_respuesta) mostrarEstado("Elige una respuesta para guardar el comentario", "aviso");
        else {
          mostrarEstado("Guardado", "exito", true);
          actualizarPaso();
        }
      },
    });

    // Estado completo de una pregunta: su respuesta marcada (si hay) y su comentario
    const idDe = (campo) => campo.name.split("_")[1];
    function camposDe(id) {
      const campos = { [`comentario_${id}`]: form.elements[`comentario_${id}`].value };
      const marcado = form.querySelector(`input[name="respuesta_${id}"]:checked`);
      if (marcado) campos[`respuesta_${id}`] = marcado.value;
      return campos;
    }

    form.addEventListener("change", (e) => {
      if (e.target.matches(".sa-toggle__input")) auto.agregar(camposDe(idDe(e.target)));
    });

    // Comentarios: se guardan cuando se deja de escribir, no en cada tecla
    const esperas = new Map();
    form.addEventListener("input", (e) => {
      if (!e.target.matches(".sa-comentario__campo")) return;
      const id = idDe(e.target);
      clearTimeout(esperas.get(id));
      esperas.set(id, setTimeout(() => {
        esperas.delete(id);
        auto.agregar(camposDe(id));
      }, ESPERA_COMENTARIO_MS));
    });

    // Al salir: los comentarios que esperaban se mandan ya (keepalive termina el envío
    // aunque la pestaña se cierre). Solo se pregunta si algo quedó en cola sin enviar,
    // por ejemplo sin conexión. Los botones de navegación envían el form completo: ahí no.
    let navegando = false;
    form.addEventListener("submit", () => (navegando = true));
    window.addEventListener("beforeunload", (e) => {
      for (const [id, espera] of esperas) {
        clearTimeout(espera);
        auto.agregar(camposDe(id));
      }
      esperas.clear();
      if (!navegando && auto.sinEnviar()) e.preventDefault();
    });
  }
}
