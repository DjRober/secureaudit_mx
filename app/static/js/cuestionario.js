// Progreso en vivo del cuestionario (RF-04.4): barra del control actual y
// barra global, recalculadas cada vez que se marca un radio. Los datos que
// vienen del servidor llegan como atributos data-* (sin Jinja dentro del JS).
(function () {
  var form = document.getElementById("form-cuestionario");
  if (!form) return;

  var grupos = form.querySelectorAll(".sa-toggle[data-question]");
  var totalControl = grupos.length;
  var global = document.getElementById("global-progreso");
  var totalGlobal = Number(global.dataset.total);
  // Respondidas en los DEMÁS controles según la BD; las de este se cuentan en vivo
  var respondidasOtros = Number(global.dataset.otros);

  function contarRespondidas() {
    var n = 0;
    grupos.forEach(function (g) {
      if (g.querySelector(".sa-toggle__input:checked")) n++;
    });
    return n;
  }

  function pintarBarra(id, respondidas, total) {
    var barra = document.getElementById(id);
    var pct = total ? Math.round((respondidas / total) * 100) : 0;
    barra.querySelector(".sa-progress__fill").style.width = pct + "%";
    barra.classList.toggle("sa-progress--complete", total > 0 && respondidas === total);
    return pct;
  }

  function actualizar() {
    var n = contarRespondidas();
    pintarBarra("ctrl-progress", n, totalControl);
    document.getElementById("ctrl-meta").textContent =
      totalControl + " preguntas · " + n + " respondidas";
    document.getElementById("footer-count").textContent =
      n + " / " + totalControl + " respondidas";

    var g = respondidasOtros + n;
    var pct = pintarBarra("global-progreso", g, totalGlobal);
    document.getElementById("global-count").textContent =
      g + " de " + totalGlobal + " respondidas · " + pct + "%";
  }

  // "change" burbujea: un solo listener en el form atiende todos los radios
  form.addEventListener("change", actualizar);
  actualizar();
})();
