// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var clientesData = JSON.parse(document.getElementById('clientes-data').textContent);

new Chart(document.getElementById("myPieChart"), {
  type: 'doughnut',
  data: {
    labels: clientesData.map(c => c.cliente__nombre || `Cliente ${c.cliente_id}`),
    datasets: [{
      data: clientesData.map(c => c.total),
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    legend: { display: true, position: 'bottom' },
    cutoutPercentage: 60,
  },
});