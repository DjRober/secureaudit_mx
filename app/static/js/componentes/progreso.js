// Componente sa-progress (css/componentes/progress.css): pinta una barra de
// progreso y la marca como completa al llegar al total. Módulo ES reutilizable
// en cualquier página: import { pintarBarra } from "../componentes/progreso.js".

/**
 * @param {HTMLElement} barra  elemento .sa-progress
 * @param {number} respondidas
 * @param {number} total
 * @returns {number} porcentaje redondeado (0-100)
 */
export function pintarBarra(barra, respondidas, total) {
  const pct = total ? Math.round((respondidas / total) * 100) : 0;
  barra.querySelector(".sa-progress__fill").style.width = pct + "%";
  barra.classList.toggle("sa-progress--complete", total > 0 && respondidas === total);
  return pct;
}
