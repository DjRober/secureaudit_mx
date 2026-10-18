// Página del cuestionario (templates/cuestionario/control.html).
// Es un módulo ES: se carga con <script type="module">, que el navegador
// ejecuta cuando el HTML ya está listo, y puede importar componentes.
//
// Progreso en vivo (RF-04.4): barra del control actual y barra global,
// recalculadas cada vez que se marca un radio. Los datos que vienen del
// servidor llegan como atributos data-* (sin Jinja dentro del JS).
import { pintarBarra } from "../componentes/progreso.js";

const form = document.getElementById("form-cuestionario");

if (form) {
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
}
