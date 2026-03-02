const descontoInput = document.getElementById("desconto");
descontoInput.addEventListener("input", aplicarDesconto);

const btnAdicionar = document.querySelector("#btnAdicionar");
btnAdicionar.addEventListener("click", adicionarItem);

const fiadoCheck = document.querySelector("#fiadoCheck");
fiadoCheck.addEventListener("change", toggleFiado);

const finalizarVendaBtn = document.querySelector("#finalizarVenda");
finalizarVendaBtn.addEventListener("click", finalizarVenda);

let totalGeral = 0;
let fiado = false;

function aplicarDesconto() {
    const desconto = parseFloat(document.getElementById("desconto").value) || 0;

    const totalComDesconto = totalGeral - desconto;

    document.getElementById("valorTotal").innerText = totalComDesconto.toFixed(2);
}

function toggleFiado() {
    fiado = fiadoCheck.checked;
}

function adicionarItem() {
    const select = document.getElementById("produtoSelect");
    const quantidade = parseInt(document.getElementById("quantidade").value);

    if (!select.value || quantidade <= 0) return;

    const produtoId = select.value;
    const nome = select.options[select.selectedIndex].dataset.nome;
    const preco = parseFloat(select.options[select.selectedIndex].dataset.preco);

    const tbody = document.getElementById("listaItens");

    // 🔥 Verifica se já existe
    const linhaExistente = tbody.querySelector(`tr[data-produto-id="${produtoId}"]`);

    if (linhaExistente) {

        const qtdCell = linhaExistente.children[1];

        let qtdAtual = parseInt(qtdCell.innerText);

        const novaQtd = qtdAtual + quantidade;

        qtdCell.innerText = novaQtd;

        recalcular();
        return;
    }

    // 🔥 Se não existir, cria normal
    const totalItem = preco * quantidade;

    const row = document.createElement("tr");
    row.dataset.produtoId = produtoId;

    row.innerHTML = `
        <td>${nome}</td>
        <td contenteditable="true">${quantidade}</td>
        <td contenteditable="true">${preco.toFixed(2)}</td>
        <td class="total-item">${totalItem.toFixed(2)}</td>
        <td>
            <button class="btn btn-sm btn-danger" onclick="removerItem(this, ${totalItem})">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    `;

    tbody.appendChild(row);

    // limpar campos
    select.value = "";
    document.getElementById("quantidade").value = "1";

    recalcular();
}

function removerItem(btn, valor) {
    btn.closest("tr").remove();
    totalGeral -= valor;
    atualizarTotal();
}

function atualizarTotal() {
    document.getElementById("valorTotal").innerText = totalGeral.toFixed(2);
}

function recalcular() {
    totalGeral = 0;
    document.querySelectorAll("#listaItens tr").forEach(row => {
        const qtd = parseFloat(row.children[1].innerText);
        const preco = parseFloat(row.children[2].innerText);
        const total = qtd * preco;

        totalGeral += total;
    });

    atualizarTotal();
}

function finalizarVenda() {
    const itens = [];

    document.querySelectorAll("#listaItens tr").forEach(row => {
        const produtoId = row.dataset.produtoId;
        const nome = row.children[0].innerText;
        const quantidade = parseInt(row.children[1].innerText);
        const preco = parseFloat(row.children[2].innerText);

        itens.push({
            id: produtoId,
            nome: nome,
            quantidade: quantidade,
            preco: preco
        });
    });

    const fiado = document.getElementById("fiadoCheck").checked;
    const clienteFiado = document.getElementById("clienteFiado").value;
    const formaPagamento = document.getElementById("forma-pagamento").value;
    const desconto = Number(document.getElementById("desconto").value);

    const descricao = document.getElementById("descricaoVenda").value;
    const dados = {
        itens: itens,
        fiado: fiado,
        clienteFiado: clienteFiado,
        descricao: descricao,
        desconto: desconto,
        formaPagamento: formaPagamento
    };

    console.log(dados);

    const csrftoken = getCookie('csrftoken');
    const URL_VENDA = finalizarVendaBtn.dataset.url;
    fetch(URL_VENDA, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(dados)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {

                const modal = new bootstrap.Modal(
                    document.getElementById('vendaSucessoModal')
                );

                modal.show();

                document
                    .getElementById('vendaSucessoModal')
                    .addEventListener('hidden.bs.modal', function () {
                        window.location.href = "/vendas/";
                    });
            } else {
                alert("Erro: " + data.message);
            }
        })
        .catch(error => {
            console.error("Erro:", error);
        });
}

// evento dos campos "editable"
document.addEventListener('input', (e) => {
    if (e.target.classList.contains('total-item')) {
        recalcular();
    } else if (e.target.contentEditable === 'true') {
        const linha = e.target.closest('tr');
        const precoUnitario = parseFloat(e.target.textContent);
        const quantidade = parseInt(linha.children[1].textContent);
        const totalItem = precoUnitario * quantidade;
        linha.querySelector('.total-item').textContent = totalItem.toFixed(2);
        recalcular();
    }
});
