from django.urls import path
from . import views

urlpatterns = [
    # auth
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('configuracoes/', views.configuracoes_view, name='configuracoes'),

    # dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # categorias
    path('categorias/', views.categorias_view, name='categorias'),
    path('categorias/<int:id>/editar/', views.categorias_editar_view, name='categorias_editar'),
    path('categorias/<int:id>/excluir/', views.categorias_excluir_view, name='categorias_excluir'),
    
    # produtos
    path('produtos/', views.produtos_view, name='produtos'),
    path('produtos/<int:id>/editar/', views.produtos_editar_view, name='produtos_editar'),
    path('produtos/<int:id>/excluir/', views.produtos_excluir_view, name='produtos_excluir'),

    # vendas
    path('vendas/', views.vendas_view, name='vendas'),
    path('vendas/realizar/', views.realizar_venda_view, name='realizar_venda'),
    path('vendas/<int:id>/excluir/', views.vendas_excluir_view, name='vendas_excluir'),

    # vendas-fiado
    path('vendas-fiado/', views.vendas_fiado_view, name='vendas_fiado'),
    path('vendas-fiado/<int:id>/pagar/', views.vendas_fiado_pagar_view, name='vendas_fiado_pagar'),
    path('vendas-fiado/<int:id>/excluir/', views.vendas_fiado_excluir_view, name='vendas_fiado_excluir'),

    # offline
    path('offline/', views.offline_view, name='offline'),

    # logout
    path('logout/', views.logout_view, name='logout'),
]