import { BarElement, CategoryScale, Chart, Legend, LinearScale, LineElement, PointElement, Tooltip } from 'chart.js'

/** Registro único de Chart.js para todos los gráficos. */
export default defineNuxtPlugin(() => {
  Chart.register(BarElement, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)
  Chart.defaults.color = '#71717a' // gris medio: legible en modo claro y oscuro
  Chart.defaults.borderColor = 'rgba(113,113,122,.25)'
})
