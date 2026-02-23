const detalhesModal = document.getElementById('detalhesVendaFiado');

detalhesModal.addEventListener('show.bs.modal', function (event) {

    const button = event.relatedTarget;

    const id = button.getAttribute('data-venda-id');
    const cliente = button.getAttribute('data-venda-cliente');
    const descricao = button.getAttribute('data-venda-descricao');
    const data = button.getAttribute('data-venda-data');
    const total = button.getAttribute('data-venda-total');
    const totalPago = button.getAttribute('data-venda-total-pago');
    const totalPendente = button.getAttribute('data-venda-total-pendente');
    const status = button.getAttribute('data-venda-status');
    const produtos = button.getAttribute('data-venda-produtos');

    document.getElementById('vendaFiadoId').innerText = id;
    document.getElementById('vendaFiadoCliente').innerText = (cliente == "None" ? "Não especificado" : cliente);
    document.getElementById('vendaFiadoDescricao').innerText = descricao;
    document.getElementById('vendaFiadoData').innerText = data;
    document.getElementById('vendaFiadoTotal').innerText = total;
    document.getElementById('vendaFiadoTotalPago').innerText = totalPago;
    document.getElementById('vendaFiadoTotalPendente').innerText = totalPendente;
    document.getElementById('vendaFiadoProdutos').innerText = produtos;

    // Badge status
    let statusText = "";
    if (status === "pendente") {
        statusText = "Pendente";
    } else if (status === "parcial") {
        statusText = "Parcialmente Pago";
    } else {
        statusText = "Pago";
    }

    document.getElementById('vendaFiadoStatus').innerText = statusText;
});