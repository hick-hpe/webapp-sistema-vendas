const btnAdicionar = document.querySelector("#btnAdicionar");
btnAdicionar.addEventListener("click", adicionarItem);

const fiadoCheck = document.querySelector("#fiadoCheck");
fiadoCheck.addEventListener("change", toggleFiado);

const finalizarVendaBtn = document.querySelector("#finalizarVenda");
finalizarVendaBtn.addEventListener("click", finalizarVenda);

let totalGeral = 0;

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
        const precoCell = linhaExistente.children[2];

        let qtdAtual = parseInt(qtdCell.innerText);
        let precoAtual = parseFloat(precoCell.innerText);

        const novaQtd = qtdAtual + quantidade;

        qtdCell.innerText = novaQtd;

        recalcular();
        return; // 🔥 Não cria nova linha
    }

    // 🔥 Se não existir, cria normal
    const totalItem = preco * quantidade;

    const row = document.createElement("tr");
    row.dataset.produtoId = produtoId;

    row.innerHTML = `
        <td>${nome}</td>
        <td>${quantidade}</td>
        <td contenteditable="true">${preco.toFixed(2)}</td>
        <td class="total-item">${totalItem.toFixed(2)}</td>
        <td>
            <button class="btn btn-sm btn-danger">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    `;

    tbody.appendChild(row);

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

        row.querySelector(".total-item").innerText = total.toFixed(2);
        totalGeral += total;
    });

    atualizarTotal();
}

function toggleFiado() {
    const div = document.getElementById("clienteFiadoDiv");
    div.classList.toggle("d-none");
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

    const descricao = document.getElementById("descricaoVenda").value;
    const dados = {
        itens: itens,
        fiado: fiado,
        clienteFiado: clienteFiado,
        descricao: descricao
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
                        location.reload();
                    });
            } else {
                alert("Erro: " + data.message);
            }
        })
        .catch(error => {
            console.error("Erro:", error);
        });
}


