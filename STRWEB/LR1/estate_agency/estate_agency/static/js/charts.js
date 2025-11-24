function calculateMaclaurinSeries(x, terms = 50) {
  if (Math.abs(x) >= 1) {
    return null;
  }

  let sum = 0;
  for (let n = 1; n <= terms; n++) {
    const term = Math.pow(-1, n - 1) * Math.pow(x, n) / n;
    sum += term;
  }
  return sum;
}

function calculateExactFunction(x) {
  if (x <= -1) {
    return null;
  }
  return Math.log(1 + x);
}

function generateChartData() {
  const dataPoints = 200;
  const xMin = -0.99;
  const xMax = 0.99;
  const step = (xMax - xMin) / dataPoints;
  const terms = 50;

  const seriesData = [];
  const exactData = [];

  for (let i = 0; i <= dataPoints; i++) {
    const x = xMin + i * step;
    const seriesValue = calculateMaclaurinSeries(x, terms);
    const exactValue = calculateExactFunction(x);

    seriesData.push({ x: x, y: seriesValue });
    exactData.push({ x: x, y: exactValue });
  }
  
  return {
    seriesData: seriesData,
    exactData: exactData,
    terms: terms
  };
}

function createChart() {
  const canvasElement = document.getElementById('functionChart');

  const data = generateChartData();

  const ctx = canvasElement.getContext('2d');

  if (typeof Chart === 'undefined') {
    console.error('Chart.js is not loaded');
    return;
  }
  if (typeof chartjsPluginAnnotation !== 'undefined') {
    Chart.register(chartjsPluginAnnotation);
  }

  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'Ряд',
          data: data.seriesData,
          borderColor: 'rgb(40, 33, 185)',
          borderWidth: 2,
          pointRadius: 0,
          pointHoverRadius: 3,
          tension: 0.1,
        },
        {
          label: 'ln(1+x)',
          data: data.exactData,
          borderColor: 'rgb(255, 99, 132)',
          borderWidth: 2,
          pointRadius: 0,
          pointHoverRadius: 3,
          tension: 0.1,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 1000,
        easing: 'easeInOutQuart'
      },
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        title: {
          display: true,
          text: 'Сравнение разложения в ряд Маклорена и точной функции ln(1+x)',
          font: {
            size: 16,
            weight: 'bold'
          },
          padding: {
            top: 10,
            bottom: 20
          }
        },
        legend: {
          display: true,
          position: 'top',
          labels: {
            padding: 15,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          enabled: true,
          callbacks: {
            title: function(context) {
              return 'x = ' + context[0].parsed.x.toFixed(4);
            },
            label: function (context) {
              const value = context.parsed.y;
              if (value === null || isNaN(value)) {
                return context.dataset.label + ': не определено';
              }
              return context.dataset.label + ': ' + value.toFixed(6);
            }
          }
        },
        annotation: {
          annotations: {
            xAxisZero: {
              type: 'line',
              xMin: 0,
              xMax: 0,
              borderColor: 'rgb(128, 128, 128)',
              borderWidth: 1,
              borderDash: [5, 5],
              label: {
                display: true,
                content: 'x = 0',
                position: 'end',
                backgroundColor: 'rgba(128, 128, 128, 0.7)',
                color: '#fff',
                font: {
                  size: 10
                }
              }
            },
            yAxisZero: {
              type: 'line',
              yMin: 0,
              yMax: 0,
              borderColor: 'rgb(128, 128, 128)',
              borderWidth: 1,
              borderDash: [5, 5],
              label: {
                display: true,
                content: 'y = 0',
                position: 'end',
                backgroundColor: 'rgba(128, 128, 128, 0.7)',
                color: '#fff',
                font: {
                  size: 10
                }
              }
            },
          }
        }
      },
      scales: {
        x: {
          type: 'linear',
          position: 'bottom',
          title: {
            display: true,
            text: 'x',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          grid: {
            display: true,
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            callback: function (value) {
              return value.toFixed(2);
            }
          }
        },
        y: {
          title: {
            display: true,
            text: 'y = ln(1+x)',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          grid: {
            display: true,
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            callback: function (value) {
              return value.toFixed(2);
            }
          }
        }
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  createChart();
});