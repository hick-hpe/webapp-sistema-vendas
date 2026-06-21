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


// ===== GRAFICO PRODUTOS POR CATEGORIAS =====

const ctxProdutosPorCategorias = document.getElementById("graficoProdutosPorCategorias");

const labelsProdutosPorCategorias = JSON.parse(ctxProdutosPorCategorias.dataset.labels || "[]");
const valoresProdutosPorCategorias = JSON.parse(ctxProdutosPorCategorias.dataset.valores || "[]");

new Chart(ctxProdutosPorCategorias, {
    type: "bar",
    data: {
        labels: labelsProdutosPorCategorias,
        datasets: [{
            label: "Produtos vendidos",
            data: valoresProdutosPorCategorias,
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


// ===== GRAFICO VENDAS POR CATEGORIAS =====

const ctxVendasPorCategoria = document.getElementById("graficoVendasCategoria");

const labelsVendasPorCategoria = JSON.parse(ctxVendasPorCategoria.dataset.labels || "[]");
const valoresVendasPorCategoria = JSON.parse(ctxVendasPorCategoria.dataset.valores || "[]");

new Chart(ctxVendasPorCategoria, {
    type: "bar",
    data: {
        labels: labelsVendasPorCategoria,
        datasets: [{
            label: "Valor (R$)",
            data: valoresVendasPorCategoria,
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


// ===== GRAFICO VENDAS =====

const ctxVendas = document.getElementById("graficoVendas");

const labelsVendas = JSON.parse(ctxVendas.dataset.labels || "[]");
const valoresVendas = JSON.parse(ctxVendas.dataset.valores || "[]");

new Chart(ctxVendas, {
    type: "bar",
    data: {
        labels: labelsVendas,
        datasets: [{
            label: "Valor vendido",
            data: valoresVendas,
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

