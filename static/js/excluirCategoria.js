// Seleciona o modal
const excluirModal = document.getElementById('excluirCategoria');

excluirModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    const categoriaId = button.getAttribute('data-id');
    const categoriaNome = button.getAttribute('data-nome');

    const nomeCategoria = excluirModal.querySelector('#nomeCategoria');
    nomeCategoria.textContent = categoriaNome;

    const form = excluirModal.querySelector('#formExcluirCategoria');
    form.action = `/categorias/${categoriaId}/excluir/`;
});
