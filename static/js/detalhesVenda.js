const detalhesModal = document.getElementById('detalhesVenda');

detalhesModal.addEventListener('show.bs.modal', function (event) {

    const button = event.relatedTarget;

    const id = button.getAttribute('data-venda-id');
    const cliente = button.getAttribute('data-venda-cliente');
    const descricao = button.getAttribute('data-venda-descricao');
    const data = button.getAttribute('data-venda-data');
    const total = button.getAttribute('data-venda-total');
    const formaPagamento = button.getAttribute('data-forma-pagamento');
    const produtos = button.getAttribute('data-venda-produtos');

    document.getElementById('modalVendaId').innerText = id;
    document.getElementById('modalVendaCliente').innerText = (cliente == "None" ? "Não especificado" : cliente);
    document.getElementById('modalVendaDescricao').innerText = descricao;
    document.getElementById('modalVendaData').innerText = data;
    document.getElementById('modalVendaTotal').innerText = total;
    document.getElementById('modalVendaFormaPagamento').innerText = formaPagamento;
    document.getElementById('modalVendaProdutos').innerText = produtos;
});