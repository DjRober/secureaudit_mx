// Página de resultados (templates/resultados/dashboard.html): gráfica de radar con el
// riesgo de cada control (RF-06.2). Chart.js se sirve desde static/js/vendor/ (ADR-01):
// es un script clásico (UMD) cargado antes que este módulo y expone window.Chart.
// Los datos llegan en data-controles como JSON (sin Jinja dentro del JS).

const lienzo = document.getElementById("radar");

if (lienzo && window.Chart) {
  const controles = JSON.parse(lienzo.dataset.controles);
  const raiz = document.documentElement;

  // Mismos tokens que el semáforo (css/componentes/riesgo.css): un punto por control
  // con el color de su nivel
  const TOKEN_NIVEL = {
    critico: "--danger-text",
    alto: "--danger-text",
    medio: "--warning-text",
    bajo: "--success-text",
    ne: "--neutral-text",
  };
  const token = (nombre) => getComputedStyle(raiz).getPropertyValue(nombre).trim();
  // Los tokens de color son #rrggbb: se agrega el canal alfa en hexadecimal
  const conAlfa = (hex, alfa) => hex + Math.round(alfa * 255).toString(16).padStart(2, "0");

  Chart.defaults.font.family = token("--font-sans");

  // Los colores son funciones (opciones "scriptable" de Chart.js): se vuelven a leer de
  // los tokens en cada chart.update(), así la gráfica sigue al modo claro/oscuro
  const grafica = new Chart(lienzo, {
    type: "radar",
    data: {
      labels: controles.map((c) => String(c.numero)),
      datasets: [
        {
          label: "Riesgo",
          // null = no evaluable. Con spanGaps en false (el default) la línea se corta en
          // ese control en vez de bajar a 0, que en el radar se leería como "sin riesgo"
          data: controles.map((c) => c.score),
          borderWidth: 2,
          borderColor: () => token("--brand"),
          backgroundColor: () => conAlfa(token("--brand"), 0.15),
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBorderWidth: 2,
          pointBackgroundColor: (ctx) => token(TOKEN_NIVEL[controles[ctx.dataIndex].clase]),
          pointBorderColor: () => token("--surface-200"),
        },
      ],
    },
    options: {
      animation: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? false : undefined,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: (items) => {
              const c = controles[items[0].dataIndex];
              return `Control ${c.numero}: ${c.nombre}`;
            },
            label: (item) => {
              const c = controles[item.dataIndex];
              return ` ${c.score} % · ${c.nivel}`;
            },
          },
        },
      },
      scales: {
        r: {
          // Escala fija 0-100: sin min/max, Chart.js la ajusta a los datos y exagera las
          // diferencias. Cada anillo (25, 50, 75) es un límite de nivel de RF-05.4.
          // Sin etiquetas en los anillos: caen sobre el eje del control 1 y tapan sus puntos
          // (el valor exacto está en el tooltip y en el semáforo por control)
          min: 0,
          max: 100,
          ticks: { stepSize: 25, display: false },
          grid: { color: () => token("--border") },
          angleLines: { color: () => token("--border") },
          pointLabels: {
            color: () => token("--ink-muted"),
            font: { size: 12, weight: "600" },
          },
        },
      },
    },
  });

  // Cambio de tema: botón #theme-toggle (atributo data-theme) o preferencia del sistema
  const repintar = () => grafica.update();
  new MutationObserver(repintar).observe(raiz, { attributes: true, attributeFilter: ["data-theme"] });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", repintar);
}
