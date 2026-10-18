// Modo oscuro: sigue la preferencia del sistema por defecto; el botón
// #theme-toggle permite forzar un tema y la elección se recuerda entre páginas.
// Se carga en <head> para aplicar el tema guardado antes de pintar (sin parpadeo).
(function () {
  var CLAVE = "secureaudit-tema";
  var raiz = document.documentElement;

  try {
    var guardado = localStorage.getItem(CLAVE);
    if (guardado === "light" || guardado === "dark") raiz.setAttribute("data-theme", guardado);
  } catch (e) {
    // Sin acceso a localStorage (modo privado, etc.): se usa la preferencia del sistema
  }

  var mql = window.matchMedia("(prefers-color-scheme: dark)");

  function esOscuro() {
    var forzado = raiz.getAttribute("data-theme");
    return forzado ? forzado === "dark" : mql.matches;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var boton = document.getElementById("theme-toggle");
    if (!boton) return;

    function sincronizarEtiqueta() {
      boton.textContent = esOscuro() ? "Modo claro" : "Modo oscuro";
    }

    boton.addEventListener("click", function () {
      var siguiente = esOscuro() ? "light" : "dark";
      raiz.setAttribute("data-theme", siguiente);
      try {
        localStorage.setItem(CLAVE, siguiente);
      } catch (e) {}
      sincronizarEtiqueta();
    });
    mql.addEventListener("change", function () {
      if (!raiz.getAttribute("data-theme")) sincronizarEtiqueta();
    });
    sincronizarEtiqueta();
  });
})();
