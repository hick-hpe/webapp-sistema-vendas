// Seleciona o modal
const excluirModal = document.getElementById('excluirVendaFiado');

excluirModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    const vendaId = button.getAttribute('data-id');
    const vendaNome = button.getAttribute('data-nome');

    const nomeVenda = excluirModal.querySelector('#vendaFiadoNome');
    nomeVenda.textContent = vendaNome;

    const form = excluirModal.querySelector('#excluirVendaFiadoForm');
    form.action = `/vendas-fiado/${vendaId}/excluir/`;
});
