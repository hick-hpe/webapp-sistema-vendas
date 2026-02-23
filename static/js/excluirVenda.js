// Seleciona o modal
const excluirModal = document.getElementById('excluirVenda');

excluirModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    const vendaId = button.getAttribute('data-id');
    const vendaNome = button.getAttribute('data-nome');

    const nomeVenda = excluirModal.querySelector('#nomeVenda');
    nomeVenda.textContent = vendaNome;

    const form = excluirModal.querySelector('#formExcluirVenda');
    form.action = `/vendas/${vendaId}/excluir/`;
});
