document.addEventListener("DOMContentLoaded", () => {
  const backgroundColors = ['#4f6d7a', '#c0d6df', '#f5f0e6', '#d9d4ca', '#d8b4a0'];

  // Pie Chart
  new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
      labels: chartLabels,
      datasets: [{
        label: 'Item Types',
        data: chartValues,
        backgroundColor: backgroundColors,
        hoverOffset: 10
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Inventory by Type (Pie Chart)',
          font: { size: 18 }
        }
      }
    }
  });

  // Bar Chart
  new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: chartLabels,
      datasets: [{
        label: 'Inventory Count',
        data: chartValues,
        backgroundColor: backgroundColors,
        borderRadius: 10
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Inventory by Type (Bar Chart)',
          font: { size: 18 }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 10
          }
        }
      }
    }
  });
});
