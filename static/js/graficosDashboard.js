// ===== GRAFICO DESCONTO =====

const ctxDesconto = document.getElementById("graficoDesconto");

const comDesconto = Number(ctxDesconto.dataset.comDesconto);
const semDesconto = Number(ctxDesconto.dataset.semDesconto);
const fiado = Number(ctxDesconto.dataset.fiado);

new Chart(ctxDesconto, {
    type: "pie",
    data: {
        labels: ["Com desconto", "Sem desconto", "Fiado"],
        datasets: [{
            data: [comDesconto, semDesconto, fiado],
            backgroundColor: ["#FFC107", "#0D6EFD", "#DC3545"]
        }]
    }
});


// ===== GRAFICO VENDAS =====

const ctxVendas = document.getElementById("graficoVendas");

const labels = JSON.parse(ctxVendas.dataset.labels || "[]");
const valores = JSON.parse(ctxVendas.dataset.valores || "[]");

new Chart(ctxVendas, {
    type: "bar",
    data: {
        labels: labels,
        datasets: [{
            label: "Valor vendido",
            data: valores,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});