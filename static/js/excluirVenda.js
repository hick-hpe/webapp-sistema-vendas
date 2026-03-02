// Seleciona o modal
const excluirModal = document.getElementById('excluirVenda');

excluirModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    const vendaId = button.getAttribute('data-id');
    const vendaNome = button.getAttribute('data-nome');

    console.log('ID: ', vendaId)

    const nomeVenda = excluirModal.querySelector('#nomeVenda');
    nomeVenda.textContent = vendaNome.includes("-") ? `#${vendaId}` : vendaNome;

    const form = excluirModal.querySelector('#formExcluirVenda');
    form.action = `/vendas/${vendaId}/excluir/`;
});
