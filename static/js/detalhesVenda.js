const detalhesModal = document.getElementById('detalhesVenda');

detalhesModal.addEventListener('show.bs.modal', (event) => {

    const button = event.relatedTarget;

    const id = button.getAttribute('data-venda-id');
    const cliente = button.getAttribute('data-venda-cliente');
    const descricao = button.getAttribute('data-venda-descricao');
    const data = button.getAttribute('data-venda-data');
    const total = button.getAttribute('data-venda-total');
    const desconto = button.getAttribute('data-venda-desconto');
    const formaPagamento = button.getAttribute('data-forma-pagamento');
    const produtos = button.getAttribute('data-venda-produtos');

    const badge = document.getElementById('modalVendaFormaPagamento');

    badge.className = 'badge';

    switch (formaPagamento) {
        case 'Pix':
            badge.classList.add('text-bg-success');
            break;

        case 'Dinheiro':
            badge.classList.add('text-bg-primary');
            break;

        case 'Cartão':
            badge.classList.add('text-bg-warning');
            break;

        default:
            badge.classList.add('text-bg-secondary');
    }

    document.getElementById('modalVendaId').innerText = id;
    document.getElementById('modalVendaCliente').innerText = (cliente == "None" ? "Não especificado" : cliente);
    document.getElementById('modalVendaDescricao').innerText = descricao;
    document.getElementById('modalVendaData').innerText = data;
    document.getElementById('modalVendaTotal').innerText = total;
    document.getElementById('modalVendaDesconto').innerText = desconto;
    document.getElementById('modalVendaFormaPagamento').innerText = formaPagamento;
    document.getElementById('modalVendaProdutos').innerText = produtos;
});