const inputBuscarCategorias = document.querySelector('#buscar-categorias');
const btnFiltrar = document.querySelector('#btn-filtrar');

btnFiltrar.addEventListener('click', function () {

    const termo = inputBuscarCategorias.value.toLowerCase();

    const linhas = document.querySelectorAll('tbody tr');

    linhas.forEach(linha => {
        const nome = linha.querySelector('.nome-categoria')
            .textContent
            .toLowerCase();

        if (nome.includes(termo)) {
            linha.style.display = '';
        } else {
            linha.style.display = 'none';
        }
    });

});