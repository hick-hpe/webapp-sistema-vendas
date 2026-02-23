const pagarModal = document.getElementById('pagarVendaFiado');

pagarModal.addEventListener('show.bs.modal', function (event) {

    const button = event.relatedTarget;
    const vendaFiadoId = button.getAttribute('data-id');
    document.getElementById('pagarVendaFiadoId').value = vendaFiadoId;
    const form = document.getElementById('pagarVendaFiadoForm');
    form.action = `/vendas-fiado/${vendaFiadoId}/pagar/`;
});
