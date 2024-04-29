// chart.js
// Datos de ejemplo
var temperaturesAmbData = [22, 23, 24, 25, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6];
var humidityAmbData = [50, 52, 55, 60, 62, 65, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 90, 88, 85, 82, 80, 78, 75, 72];
var hoursAmbData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];

// Datos de ejemplo
var pagosOnline = [25, 35, 40]; // Cantidad de pagos online
var pagosEfectivo = [20, 30, 50]; // Cantidad de pagos en efectivo
var pagosTransferencia = [10, 15, 75]; // Cantidad de pagos por transferencia

//var temperaturesAmbData = {{ temperatures_amb|tojson }};
//var humidityAmbData = {{ humidity_amb|tojson }};
//var hoursAmbData = {{ hours_amb|tojson }};

//var humiditySoilData = {{ humidity_soil|tojson }};
//var hoursSoilData = {{ hours_soil|tojson }};

// Funciones para inicializar las gráficas
function inicializarGraficaAmbiental() {
    var ctx = document.getElementById('grafica-amb').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hoursAmbData,  // Utiliza las horas desde Flask
            datasets: [{
                label: 'Temperatura (°C)',
                data: temperaturesAmbData,  // Utiliza las temperaturas desde Flask
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            },{
                label: 'Humedad (%)',
                data: humidityAmbData,
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    min: 1,   // Mínimo en el eje x
                    max: 24,  // Máximo en el eje x
                    step: 1,   // Paso entre etiquetas
                    title:{
                        display: true,
                        text: 'Horas del dia'
                    }
                },
                y: {
                    beginAtZero: true,
                    title:{
                        display: true,
                        text:'Temperatura y Humedad'
                    }
                }
            },
            plugins:{
                legent:{
                    display: true,
                    position: 'top'
                }
            },
            maintainAspectRatio: false, // Esto permite que el gráfico ocupe todo el tamaño del canvas
            responsive: true // Esto hace que el gráfico sea responsive
        }
    });
}



// Suma de los totales de cada tipo de pago
var totalPagosOnline = pagosOnline.reduce((a, b) => a + b, 0);
var totalPagosEfectivo = pagosEfectivo.reduce((a, b) => a + b, 0);
var totalPagosTransferencia = pagosTransferencia.reduce((a, b) => a + b, 0);

// Calcular porcentajes
var porcentajeOnline = totalPagosOnline / (totalPagosOnline + totalPagosEfectivo + totalPagosTransferencia) * 100;
var porcentajeEfectivo = totalPagosEfectivo / (totalPagosOnline + totalPagosEfectivo + totalPagosTransferencia) * 100;
var porcentajeTransferencia = totalPagosTransferencia / (totalPagosOnline + totalPagosEfectivo + totalPagosTransferencia) * 100;

// Funciones para inicializar las gráficas
function inicializarGraficaPagos() {
    var ctx = document.getElementById('grafico-pagos').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Pagos Online', 'Efectivo', 'Transferencia'],
            datasets: [{
                label: 'Pagos',
                data: [porcentajeOnline, porcentajeEfectivo, porcentajeTransferencia],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],

            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Distribución de Pagos'
            }
        }
    })};