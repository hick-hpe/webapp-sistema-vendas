const btnCloseSidebar = document.getElementById('close-sidebar');
const btnOpenSidebar = document.getElementById('open-sidebar');
const sidebar = document.getElementById('sidebar');

btnOpenSidebar.addEventListener('click', () => {
    sidebar.classList.add('show');
});

btnCloseSidebar.addEventListener('click', () => {
    sidebar.classList.remove('show');
});