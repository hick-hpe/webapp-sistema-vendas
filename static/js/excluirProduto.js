// Seleciona o modal
const excluirModal = document.getElementById('excluirProduto');

excluirModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    const produtoId = button.getAttribute('data-id');
    const produtoNome = button.getAttribute('data-nome');
    console.log('Produto ID:', produtoId);
    console.log('Produto Nome:', produtoNome);

    const nomeProduto = excluirModal.querySelector('#nomeProduto');
    nomeProduto.textContent = produtoNome;

    const form = excluirModal.querySelector('#formExcluirProduto');
    form.action = `/produtos/${produtoId}/excluir/`;
});
