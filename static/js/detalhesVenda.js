const detalhesModal = document.getElementById('detalhesVenda');

detalhesModal.addEventListener('show.bs.modal', function (event) {

    const button = event.relatedTarget;

    const id = button.getAttribute('data-venda-id');
    const descricao = button.getAttribute('data-venda-descricao');
    const data = button.getAttribute('data-venda-data');
    const total = button.getAttribute('data-venda-total');
    const produtos = button.getAttribute('data-venda-produtos');
    console.log(produtos);

    document.getElementById('modalVendaId').innerText = id;
    document.getElementById('modalVendaDescricao').innerText = descricao;
    document.getElementById('modalVendaData').innerText = data;
    document.getElementById('modalVendaTotal').innerText = total;
    document.getElementById('modalVendaProdutos').innerText = produtos;
});