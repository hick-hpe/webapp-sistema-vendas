from django.urls import path
from . import views

urlpatterns = [
    # login
    path('', views.login_view, name='login'),

    # dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # categorias
    path('categorias/', views.categorias_view, name='categorias'),
    path('categorias/<int:id>/editar/', views.categorias_editar_view, name='categorias_editar'),
    path('categorias/<int:id>/excluir/', views.categorias_excluir_view, name='categorias_excluir'),
    
    # produtos
    path('produtos/', views.produtos_view, name='produtos'),

    # vendas
    path('vendas/', views.vendas_view, name='vendas'),

    # compras-fiado
    path('compras-fiado/', views.compras_fiado_view, name='compras_fiado'),

    # offline
    path('offline/', views.offline_view, name='offline'),

    # logout
    path('logout/', views.logout_view, name='logout'),
]